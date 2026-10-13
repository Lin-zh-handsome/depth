"""Formal iteration-based CNN-DP training on fixed ManiSkill demonstration data.

The action model and loss come directly from the untouched official checkout.
All 100000 optimizer updates and 20 scheduled immutable snapshots are retained.
"""
import argparse
import copy
import json
import math
import os
import random
import signal
import subprocess
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'source/diffusion_policy'))
import numpy as np
import torch
from diffusers.optimization import get_scheduler
from diffusion_policy.common.pytorch_util import dict_apply, optimizer_to
from diffusion_policy.model.diffusion.ema_model import EMAModel
from gsc_dp.policy_factory import create
from gsc_dp.dataset import ManiSkillRGBDImageDataset
from gsc_dp.checkpoints import save

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--config',type=Path,required=True);a=ap.parse_args()
    cfg=json.loads(a.config.read_text())
    is_mimic=cfg['benchmark']=='mimicgen'
    run=ROOT/'runs'/cfg['benchmark']/cfg['task']/cfg['method']/f"seed_{cfg['seed']}"
    run.mkdir(parents=True,exist_ok=True)
    frozen=run/'config_resolved.json'
    if frozen.exists() and json.loads(frozen.read_text())!=cfg: raise ValueError('resume config changed')
    frozen.write_text(json.dumps(cfg,indent=2))
    seed=cfg['seed'];random.seed(seed);np.random.seed(seed);torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed);torch.set_num_threads(2)
    dataset=ManiSkillRGBDImageDataset(cfg['zarr_path'],horizon=16,pad_before=1,pad_after=7,
        n_obs_steps=2,seed=0,val_ratio=0)
    model=create(cfg);model.set_normalizer(dataset.get_normalizer());ema_model=copy.deepcopy(model)
    model.to('cuda:0');ema_model.to('cuda:0')
    optimizer=torch.optim.AdamW(model.parameters(),lr=1e-4,betas=(0.95,0.999),eps=1e-8,weight_decay=1e-6)
    total_updates=math.ceil(len(dataset)/cfg['batch_size'])*cfg['budget'] if is_mimic else cfg['budget']
    scheduler=get_scheduler('cosine',optimizer=optimizer,num_warmup_steps=500,num_training_steps=total_updates)
    ema=EMAModel(ema_model,update_after_step=0,inv_gamma=1,power=.75,min_value=0,max_value=.9999)
    updates=epoch=batch_offset=0
    candidates=list((run/'checkpoints').glob('*.pt'))
    if candidates:
        latest=max(candidates,key=lambda p:p.stat().st_mtime)
        payload=torch.load(latest,map_location='cpu',weights_only=False)
        model.load_state_dict(payload['model']);ema_model.load_state_dict(payload['ema_model'])
        optimizer.load_state_dict(payload['optimizer']);optimizer_to(optimizer,'cuda:0')
        scheduler.load_state_dict(payload['scheduler']);ema.optimization_step=payload['ema_optimization_step']
        updates=payload['optimizer_updates'];epoch=payload['data_epoch'];batch_offset=payload['next_batch']
        random.setstate(payload['python_rng']);np.random.set_state(payload['numpy_rng'])
        torch.set_rng_state(payload['torch_rng']);torch.cuda.set_rng_state_all(payload['cuda_rng'])
        print('resumed',latest,'optimizer_updates',updates,flush=True)
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    uuid=os.environ['CUDA_VISIBLE_DEVICES']
    (run/'gpu_job.json').write_text(json.dumps(dict(pid=os.getpid(),gpu_uuid=uuid,
        physical_gpu=2,visible_device='cuda:0',cpu_threads=2,dataloader_workers=0,code_revision=revision),indent=2))
    stop=[False]
    signal.signal(signal.SIGTERM,lambda *_:stop.__setitem__(0,True))
    def payload(next_batch):
        return dict(config=cfg,model=model.state_dict(),ema_model=ema_model.state_dict(),
            optimizer=optimizer.state_dict(),scheduler=scheduler.state_dict(),
            ema_optimization_step=ema.optimization_step,optimizer_updates=updates,data_epoch=epoch,
            next_batch=next_batch,python_rng=random.getstate(),numpy_rng=np.random.get_state(),
            torch_rng=torch.get_rng_state(),cuda_rng=torch.cuda.get_rng_state_all(),
            code_revision=revision,gpu_uuid=uuid)
    begin=time.time()
    with (run/'train_metrics.jsonl').open('a',buffering=1) as log:
        while updates<total_updates:
            generator=torch.Generator().manual_seed(seed+epoch*1000003)
            loader=torch.utils.data.DataLoader(dataset,batch_size=cfg['batch_size'],shuffle=True,
                generator=generator,num_workers=0,pin_memory=False,drop_last=False)
            for bi,batch in enumerate(loader):
                if bi<batch_offset: continue
                batch=dict_apply(batch,lambda x:x.to('cuda:0'))
                optimizer.zero_grad(set_to_none=True)
                loss=model.compute_loss(batch)
                if not torch.isfinite(loss): raise FloatingPointError(f'nonfinite loss at update {updates}')
                loss.backward()
                optimizer.step();scheduler.step();ema.step(model);updates+=1
                next_batch=bi+1
                if updates==1 or updates%100==0:
                    record=dict(optimizer_updates=updates,data_epoch=epoch,next_batch=next_batch,
                        train_loss=float(loss.detach()),lr=optimizer.param_groups[0]['lr'],
                        wall_seconds=time.time()-begin,gpu_peak_bytes=torch.cuda.max_memory_allocated())
                    if updates==100:
                        for family,needle in [('gsa','attention'),('token','token_learner')]:
                            terms=[p.grad.detach().square().sum() for name,p in model.named_parameters()
                                if needle in name and p.grad is not None]
                            if terms:record[family+'_gradient_l2']=float(torch.stack(terms).sum().sqrt())
                    log.write(json.dumps(record)+'\n');print(json.dumps(record),flush=True)
                if not is_mimic and updates%cfg['interval']==0: save(run,payload(next_batch),scheduled=True)
                if stop[0]:
                    save(run,payload(next_batch));print('recoverable stop',updates,flush=True);return 75
                if updates>=total_updates: break
            epoch+=1;batch_offset=0
            if is_mimic and epoch%cfg['interval']==0:
                completed=payload(0);completed['checkpoint_step']=epoch
                save(run,completed,scheduled=True)
    (run/'training_complete.json').write_text(json.dumps(dict(optimizer_updates=updates,completed_epochs=epoch,
        expected_savepoints=cfg['savepoints'],code_revision=revision)))
    return 0

if __name__=='__main__': sys.exit(main())
