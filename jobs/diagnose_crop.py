"""One real-shape crop diagnosis; no training, rollout or scientific efficiency comparison."""
import os,sys,time,json
from pathlib import Path
import torch
from torch import nn
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'source/diffusion_policy'))
from gsc_dp.encoder import RGBDGeometryObsEncoder
obj=RGBDGeometryObsEncoder.__new__(RGBDGeometryObsEncoder);nn.Module.__init__(obj)
obj.crop_shape=(76,76);obj.random_crop=True;obj.imagenet_norm=True
obj.register_buffer('rgb_mean',torch.tensor([.485,.456,.406],device='cuda')[None,:,None,None]);obj.register_buffer('rgb_std',torch.tensor([.229,.224,.225],device='cuda')[None,:,None,None]);obj.train()
rgb=torch.rand(128,3,84,84,device='cuda',requires_grad=True);depth=torch.rand(128,1,84,84,device='cuda')
def vectorized(self,rgb,depth):
 b,_,h,w=rgb.shape;valid=torch.isfinite(depth)&(depth>0);depth=torch.where(valid,depth,torch.zeros_like(depth));ch,cw=self.crop_shape
 ys=torch.randint(h-ch+1,(b,),device=rgb.device);xs=torch.randint(w-cw+1,(b,),device=rgb.device)
 rows=ys[:,None,None]+torch.arange(ch,device=rgb.device)[None,:,None];cols=xs[:,None,None]+torch.arange(cw,device=rgb.device)[None,None,:];index=(rows*w+cols).reshape(b,1,ch*cw)
 def crop(x):return x.flatten(2).gather(2,index.expand(-1,x.shape[1],-1)).reshape(b,x.shape[1],ch,cw)
 return (crop(rgb)-self.rgb_mean)/self.rgb_std,crop(depth),crop(valid)
old=obj._prepare
state=torch.cuda.get_rng_state();a=old(rgb,depth);torch.cuda.set_rng_state(state);b=vectorized(obj,rgb,depth)
equal=[torch.equal(x,y) for x,y in zip(a,b)];ga=torch.autograd.grad(a[0].sum(),rgb)[0];gb=torch.autograd.grad(b[0].sum(),rgb)[0]
assert all(equal) and torch.equal(ga,gb)
results={}
for name,fn in [('old_crop',old),('vectorized_crop',lambda x,y:vectorized(obj,x,y))]:
 torch.cuda.synchronize();begin=time.perf_counter()
 with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU]) as prof:
  out=fn(rgb,depth);torch.cuda.synchronize()
 elapsed=time.perf_counter()-begin
 results[name]=dict(single_call_seconds=elapsed,scalar_item_calls=sum(e.count for e in prof.key_averages() if e.key=='aten::item'),local_scalar_calls=sum(e.count for e in prof.key_averages() if e.key=='aten::_local_scalar_dense'))
print(json.dumps(dict(operation='aligned RGB/depth/valid crop, 128 observations per view',equal_rgb_depth_mask=equal,equal_rgb_gradient=torch.equal(ga,gb),results=results,scope='operational diagnosis only; not a paper efficiency experiment'),indent=2),flush=True)
