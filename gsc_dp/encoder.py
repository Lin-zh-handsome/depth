"""Configurable RGB-D observation encoder for chapter 3 GSC-DP experiments.

The output dimension equals the official MultiImageObsEncoder: 512 per RGB view,
followed by unchanged low-dimensional observations. Depth is a side input only.
"""
from __future__ import annotations

import copy
import torch
from torch import nn
from torch.nn import functional as F
import torchvision

from diffusion_policy.model.common.module_attr_mixin import ModuleAttrMixin
from diffusion_policy.common.pytorch_util import replace_submodules
from gsc_dp.depth_token_learner import DepthTokenLearner
from gsc_dp.geometry_attention_adapter import GeometryAttentionAdapter


_METHODS = {
    "e0": (False, None, False, False),
    "e1": (True, None, False, False),
    "e2": (False, "plain", False, False),
    "e3": (False, "gsa", False, False),
    "e4": (False, None, True, True),
    "e5": (False, "gsa", True, False),
    "e6": (False, "gsa", True, True),
    "e7": (True, "plain", False, False),
}


class _ResNetGeometryView(nn.Module):
    def __init__(self, method, insert_after="layer2", num_tokens=8,
                 fusion="add", attention_mode=None, use_uv=True,
                 use_depth=True, use_rho=True, heads=4):
        super().__init__()
        rgbd, default_attention, token_enabled, geometry = _METHODS[method]
        self.rgbd = rgbd
        self.attention_mode = attention_mode or default_attention
        self.token_enabled = token_enabled
        self.insert_after = insert_after
        if insert_after not in {"layer2", "layer3"}:
            raise ValueError("insert_after must be layer2 or layer3")
        net = torchvision.models.resnet18(weights=None)
        net.fc = nn.Identity()
        if rgbd:
            net.conv1 = nn.Conv2d(4, 64, 7, stride=2, padding=3, bias=False)
            nn.init.kaiming_normal_(net.conv1.weight, mode='fan_out', nonlinearity='relu')
        self.net = replace_submodules(
            root_module=net,
            predicate=lambda x: isinstance(x, nn.BatchNorm2d),
            func=lambda x: nn.GroupNorm(x.num_features // 16, x.num_features))
        channels = 128 if insert_after == "layer2" else 256
        self.attention = None
        if self.attention_mode is not None:
            self.attention = GeometryAttentionAdapter(channels, heads, self.attention_mode)
        self.token_learner = None
        self.fusion = fusion
        if token_enabled:
            if not geometry:
                use_uv = use_depth = use_rho = False
            self.token_learner = DepthTokenLearner(
                channels, num_tokens, use_uv=use_uv, use_depth=use_depth, use_rho=use_rho)
            self.token_projection = nn.Linear(num_tokens * self.token_learner.output_dim, 512)
            nn.init.zeros_(self.token_projection.weight)
            nn.init.zeros_(self.token_projection.bias)
            if fusion == "concat_mlp":
                self.fuse = nn.Sequential(nn.Linear(1024, 512), nn.GELU(), nn.Linear(512, 512))
            elif fusion != "add":
                raise ValueError(f"unsupported fusion {fusion}")

    def forward(self, rgb, depth_m=None, valid=None, capture=False):
        x = torch.cat((rgb, depth_m), dim=1) if self.rgbd else rgb
        net = self.net
        x = net.maxpool(net.relu(net.bn1(net.conv1(x))))
        x = net.layer1(x)
        x = net.layer2(x)
        artifacts = {}
        if self.insert_after == "layer2":
            x, artifacts = self._intermediate(x, depth_m, valid, capture)
        x = net.layer3(x)
        if self.insert_after == "layer3":
            x, artifacts = self._intermediate(x, depth_m, valid, capture)
        x = net.layer4(x)
        base = torch.flatten(net.avgpool(x), 1)
        if self.token_learner is not None:
            geo = self.token_projection(self._tokens.flatten(1))
            base = base + geo if self.fusion == "add" else self.fuse(torch.cat((base, geo), dim=-1))
        return (base, artifacts) if capture else base

    def _intermediate(self, x, depth_m, valid, capture):
        artifacts = {}
        if self.attention is not None:
            if capture:
                x, info = self.attention(x, depth_m, valid, capture=True)
                artifacts.update(info)
            else:
                x = self.attention(x, depth_m, valid)
        if self.token_learner is not None:
            if capture:
                self._tokens, info = self.token_learner(x, depth_m, valid, capture=True)
                artifacts.update({f"token_{k}": v for k, v in info.items()})
            else:
                self._tokens = self.token_learner(x, depth_m, valid)
        return x, artifacts


class RGBDGeometryObsEncoder(ModuleAttrMixin):
    def __init__(self, shape_meta: dict, method: str = "e6", insert_after="layer2",
                 num_tokens=8, fusion="add", attention_mode=None,
                 use_uv=True, use_depth=True, use_rho=True,
                 crop_shape=(76, 76), random_crop=True, imagenet_norm=True,
                 heads=4):
        super().__init__()
        method = method.lower()
        if method not in _METHODS:
            raise ValueError(f"unknown method {method}")
        self.shape_meta = shape_meta
        self.method = method
        self.crop_shape = crop_shape
        self.random_crop = random_crop
        self.imagenet_norm = imagenet_norm
        self.rgb_keys = sorted(k for k, v in shape_meta["obs"].items() if v.get("type") == "rgb")
        self.depth_keys = {key: key[:-6] + "_depth" for key in self.rgb_keys if key.endswith("_image")}
        self.lowdim_keys = sorted(k for k, v in shape_meta["obs"].items()
                                  if v.get("type", "low_dim") == "low_dim")
        self.views = nn.ModuleDict({key: _ResNetGeometryView(
            method, insert_after, num_tokens, fusion, attention_mode,
            use_uv, use_depth, use_rho, heads) for key in self.rgb_keys})
        self.register_buffer("rgb_mean", torch.tensor([0.485, 0.456, 0.406])[None, :, None, None])
        self.register_buffer("rgb_std", torch.tensor([0.229, 0.224, 0.225])[None, :, None, None])
        self.feature_dim = 512 * len(self.rgb_keys) + sum(
            shape_meta["obs"][key]["shape"][0] for key in self.lowdim_keys)

    def _prepare(self, rgb, depth):
        b, _, h, w = rgb.shape
        if depth is None:
            depth = rgb.new_zeros((b, 1, h, w))
        valid = torch.isfinite(depth) & (depth > 0)
        depth = torch.where(valid, depth, torch.zeros_like(depth))
        if self.crop_shape is not None:
            ch, cw = self.crop_shape
            if ch > h or cw > w:
                raise ValueError("crop larger than image")
            if self.training and self.random_crop:
                ys = torch.randint(h - ch + 1, (b,), device=rgb.device)
                xs = torch.randint(w - cw + 1, (b,), device=rgb.device)
            else:
                ys = torch.full((b,), (h - ch) // 2, device=rgb.device)
                xs = torch.full((b,), (w - cw) // 2, device=rgb.device)
            rgb = torch.stack([rgb[i, :, ys[i]:ys[i]+ch, xs[i]:xs[i]+cw] for i in range(b)])
            depth = torch.stack([depth[i, :, ys[i]:ys[i]+ch, xs[i]:xs[i]+cw] for i in range(b)])
            valid = torch.stack([valid[i, :, ys[i]:ys[i]+ch, xs[i]:xs[i]+cw] for i in range(b)])
        if self.imagenet_norm:
            rgb = (rgb - self.rgb_mean) / self.rgb_std
        return rgb, depth, valid

    def forward(self, obs_dict, capture=False):
        features, artifacts = [], {}
        for key in self.rgb_keys:
            depth_key = self.depth_keys.get(key)
            depth = obs_dict.get(depth_key) if depth_key else None
            if self.method != "e0" and depth is None and self.method != "e2":
                raise KeyError(f"{key} requires aligned {depth_key}")
            rgb, depth, valid = self._prepare(obs_dict[key], depth)
            output = self.views[key](rgb, depth, valid, capture=capture)
            if capture:
                output, artifacts[key] = output
                artifacts[key]["input_rgb"] = ((rgb * self.rgb_std + self.rgb_mean)
                                                if self.imagenet_norm else rgb).detach()
                artifacts[key]["input_depth"] = depth.detach()
            features.append(output)
        features.extend(obs_dict[key] for key in self.lowdim_keys)
        vector = torch.cat(features, dim=-1)
        return (vector, artifacts) if capture else vector

    def output_shape(self):
        return (self.feature_dim,)
