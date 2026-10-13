"""Single residual official DFormerv2 GSA unit for a ResNet feature grid."""
import torch
from torch import nn
from torch.nn import functional as F
from gsc_dp.dformer_ops import GeoPriorGen, Decomposed_GSA

class GeometryAttentionAdapter(nn.Module):
    def __init__(self, channels, heads=4, mode='gsa', depth_scale_m=1.0):
        super().__init__()
        self.norm = nn.LayerNorm(channels)
        self.prior = GeoPriorGen(channels, heads, 2.0, 4.0)
        self.attention = Decomposed_GSA(channels, heads)
        self.gamma = nn.Parameter(torch.tensor(0.1))
        self.mode, self.depth_scale_m = mode, depth_scale_m

    def forward(self, feature, depth_m=None, valid=None, capture=False):
        b,c,h,w = feature.shape
        if depth_m is None:
            depth_m = feature.new_zeros(b,1,h,w)
        if valid is None:
            valid = torch.isfinite(depth_m) & (depth_m>0)
        d = F.interpolate(torch.where(valid,depth_m,torch.zeros_like(depth_m)),(h,w),mode='nearest')
        v = F.interpolate(valid.float(),(h,w),mode='nearest')>0.5
        prior = self.prior((h,w), d/self.depth_scale_m, split_or_not=True)
        (sin,cos),(mh,mw) = prior
        # Invalid measurements contribute no pairwise depth prior, while the
        # official spatial decay remains available.
        if self.mode == 'plain':
            mh,mw = torch.zeros_like(mh),torch.zeros_like(mw)
        else:
            depth_h = self.prior.generate_1d_depth_decay(h,w,(d/self.depth_scale_m).transpose(-2,-1))
            depth_w = self.prior.generate_1d_depth_decay(w,h,d/self.depth_scale_m)
            vh = v.transpose(-2,-1)
            pair_h = vh[..., :,None] & vh[...,None,:]
            pair_w = v[..., :,None] & v[...,None,:]
            if self.mode == 'gsa':
                mh = mh - self.prior.weight[1]*depth_h*(~pair_h)
                mw = mw - self.prior.weight[1]*depth_w*(~pair_w)
            elif self.mode == 'spatial':
                mh = mh - self.prior.weight[1]*depth_h
                mw = mw - self.prior.weight[1]*depth_w
            else:
                raise ValueError(self.mode)
        self.attention.capture = capture
        update = self.attention(self.norm(feature.permute(0,2,3,1)),((sin,cos),(mh,mw)),True)
        fused = feature + self.gamma*update.permute(0,3,1,2)
        if not capture: return fused
        return fused, dict(feature_before=feature.detach(),feature_after=fused.detach(),
            prior_height=mh.detach(),prior_width=mw.detach(),depth_m=d.detach(),
            depth_valid=v.detach(),**self.attention.captured)
