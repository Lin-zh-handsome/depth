"""Inspect actual architecture and compare M2/M3 shared path on a real input."""
import sys,json,gc
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'source/diffusion_policy')]
import torch,numpy as np,zarr
from gsc_dp.policy_factory import create
from gsc_dp.encoder import RGBDGeometryObsEncoder
torch.set_num_threads(2)
out=ROOT/'docs/audit_55951414'
cfg=json.loads((ROOT/'configs/runs/mimicgen/threading_d2/e6/seed_0.json').read_text());records=[]
for method in ['e0','e3','e6','m3']:
    c=dict(cfg,method=method);p=create(c);enc=p.obs_encoder
    views=list(enc.key_model_map.values()) if method=='e0' else [v.net for v in enc.views.values()]
    records.append(dict(method=method,policy_class=type(p).__module__+'.'+type(p).__name__,diffusion_class=type(p.model).__module__+'.'+type(p.model).__name__,diffusion_parameter_shapes={k:list(v.shape) for k,v in p.model.state_dict().items()},feature_shape=list(enc.output_shape()),backbones=[dict(class_name=type(v).__name__,conv1_shape=list(v.conv1.weight.shape),groupnorm_count=sum(isinstance(x,torch.nn.GroupNorm) for x in v.modules()),batchnorm_count=sum(isinstance(x,torch.nn.BatchNorm2d) for x in v.modules()),backbone_parameter_shapes={k:list(x.shape) for k,x in v.state_dict().items()}) for v in views],rgb_keys=enc.rgb_keys,lowdim_keys=enc.low_dim_keys if method=='e0' else enc.lowdim_keys,depth_consumed=method!='e0',imagenet_mean=[.485,.456,.406],imagenet_std=[.229,.224,.225],backbone_initialization='random; no pretrained weights',camera_initialization='official deep copies of one initialized ResNet18' if method=='e0' else 'independently initialized per-camera ResNet18',normalizer='shared dataset LinearNormalizer limits for action/proprio; shared image range transform; identity metric depth',scheduler_class=type(p.noise_scheduler).__name__,scheduler_config=dict(p.noise_scheduler.config)))
    del p,enc,views;gc.collect()
torch.manual_seed(7)
m2=RGBDGeometryObsEncoder(cfg['shape_meta'],method='e6',crop_shape=cfg['crop_shape']).eval()
m3=RGBDGeometryObsEncoder(cfg['shape_meta'],method='m3',crop_shape=cfg['crop_shape']).eval()
best_path=ROOT/'runs/mimicgen/threading_d2/e6/seed_0/best/best.pt'
payload=torch.load(best_path,map_location='cpu',weights_only=False)
trained_encoder={k[len('obs_encoder.'):]:v for k,v in payload['ema_model'].items() if k.startswith('obs_encoder.')}
m2.load_state_dict(trained_encoder,strict=True)
del payload,trained_encoder
common={k:v for k,v in m2.state_dict().items() if '.attention.' not in k}
m3.load_state_dict(common,strict=True)
z=zarr.open(cfg['zarr_path'],'r');obs={}
for key,v in cfg['shape_meta']['obs'].items():
    x=z['data'][key][0]
    if v['type']=='rgb':x=np.moveaxis(x,-1,0).astype('f4')/255
    elif v['type']=='depth':x=np.moveaxis(x,-1,0).astype('f4')
    obs[key]=torch.as_tensor(x,dtype=torch.float32)[None]
# Dataset image normalization is common upstream of both encoders. This check
# compares the shared encoder path and does not alter any retained model.
token_details=[]
for key in m2.views:
    a,b=m2.views[key],m3.views[key]
    token_details.append(dict(camera=key,same_class=type(a.token_learner) is type(b.token_learner),fields_m2=[a.token_learner.use_uv,a.token_learner.use_depth,a.token_learner.use_rho],fields_m3=[b.token_learner.use_uv,b.token_learner.use_depth,b.token_learner.use_rho],num_tokens=a.token_learner.num_tokens,projection_shape=list(a.token_projection.weight.shape),fusion=a.fusion,m2_gsa_present=a.attention is not None,m3_gsa_absent=b.attention is None))
    a.attention=None
with torch.no_grad():
    a,aa=m2(obs,capture=True);b,bb=m3(obs,capture=True)
    shared=dict(source_real_input=cfg['zarr_path']+' data index0',shared_weight_source=str(best_path),trained_token_projection_nonzero=all(bool(torch.count_nonzero(v.token_projection.weight)) for v in m2.views.values()),m2_gsa_disabled_only_in_audit_object=True,common_weights_copied_only_in_audit_object=True,feature_max_abs=float((a-b).abs().max()),token_weights_max_abs={key:float((aa[key]['token_weights']-bb[key]['token_weights']).abs().max()) for key in aa})
result=dict(architectures=records,all_diffusion_shapes_equal=all(r['diffusion_parameter_shapes']==records[0]['diffusion_parameter_shapes'] for r in records),all_backbone_shapes_equal=all(r['backbones'][0]['backbone_parameter_shapes']==records[0]['backbones'][0]['backbone_parameter_shapes'] for r in records),tokenlearner=token_details,real_input_shared_path_check=shared,controlled_exceptions=['M0 consumes RGB and proprio only; M1/M2/M3 additionally consume aligned metric depth as geometric side input.', 'Official M0 clones the initial RGB backbone across cameras; custom module encoders initialize each camera separately. The random initial tensors are not matched across methods. No existing initialization is changed or result invalidated.'])
(out/'controlled_model_architecture.json').write_text(json.dumps(result,indent=2))
print(json.dumps(dict(same_diffusion=result['all_diffusion_shapes_equal'],same_backbone=result['all_backbone_shapes_equal'],tokenlearner=token_details,real_input=shared)),flush=True)
