"""PyTorch TokenLearner V1.1 adaptation with optional 2.5D token descriptors."""
from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F


class DepthTokenLearner(nn.Module):
    def __init__(self, channels: int, num_tokens: int = 8, hidden_dim: int = 64,
                 use_uv: bool = True, use_depth: bool = True, use_rho: bool = True):
        super().__init__()
        self.num_tokens = int(num_tokens)
        self.use_uv, self.use_depth, self.use_rho = use_uv, use_depth, use_rho
        self.norm = nn.LayerNorm(channels)
        self.mask_mlp = nn.Sequential(nn.Linear(channels, hidden_dim), nn.GELU(),
                                      nn.Linear(hidden_dim, num_tokens))
        self.output_dim = channels + 2 * int(use_uv) + int(use_depth) + int(use_rho)

    def forward(self, feature: torch.Tensor, depth_m: torch.Tensor | None = None,
                valid: torch.Tensor | None = None, capture: bool = False):
        b, c, h, w = feature.shape
        flat = feature.flatten(2).transpose(1, 2)  # B,HW,C
        logits = self.mask_mlp(self.norm(flat)).transpose(1, 2)  # B,K,HW
        weights = torch.softmax(logits, dim=-1)
        visual = torch.bmm(weights, flat)  # B,K,C
        fields = [visual]
        u = torch.linspace(0, 1, w, device=feature.device, dtype=feature.dtype)
        v = torch.linspace(0, 1, h, device=feature.device, dtype=feature.dtype)
        vv, uu = torch.meshgrid(v, u, indexing="ij")
        center_u = torch.matmul(weights, uu.flatten())
        center_v = torch.matmul(weights, vv.flatten())
        if self.use_uv:
            fields.extend((center_u.unsqueeze(-1), center_v.unsqueeze(-1)))
        if depth_m is None:
            depth_m = feature.new_zeros((b, 1, h, w))
            valid = torch.zeros_like(depth_m, dtype=torch.bool)
        else:
            if valid is None:
                valid = torch.isfinite(depth_m) & (depth_m > 0)
            depth_m = F.interpolate(torch.where(valid, depth_m, torch.zeros_like(depth_m)),
                                    size=(h, w), mode="nearest")
            valid = F.interpolate(valid.float(), size=(h, w), mode="nearest") > 0.5
        valid_flat = valid.flatten(2).to(feature.dtype).transpose(1, 2)
        depth_flat = depth_m.flatten(2).transpose(1, 2)
        rho = torch.bmm(weights, valid_flat).clamp(0, 1)
        weighted_depth = torch.bmm(weights, depth_flat * valid_flat)
        d = weighted_depth / rho.clamp_min(1e-6)
        d = torch.where(rho > 0, d, torch.zeros_like(d))
        if self.use_depth:
            fields.append(d)
        if self.use_rho:
            fields.append(rho)
        tokens = torch.cat(fields, dim=-1)
        if not capture:
            return tokens
        return tokens, {"logits": logits.detach().reshape(b, self.num_tokens, h, w),
                        "weights": weights.detach().reshape(b, self.num_tokens, h, w),
                        "visual_tokens": visual.detach(), "u": center_u.detach(),
                        "v": center_v.detach(), "depth_m": d.detach(), "rho": rho.detach()}
