"""Independent disk-checkpoint rollout under the preregistered task protocol."""
import argparse
from collections import deque
import json
import os
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'source/diffusion_policy'))
import numpy as np
import torch
from gsc_dp.policy_factory import create
from gsc_dp.analysis_env import create_analysis_env

def flat(raw):
    obs={}
    for cam in ['base_camera','hand_camera']:
        obs[cam+'_image']=np.moveaxis(np.asarray(raw['sensor_data'][cam]['rgb']),-1,0).astype('f4')/255
        mm=np.asarray(raw['sensor_data'][cam]['depth'])
        obs[cam+'_depth']=np.moveaxis(np.where(mm>0,mm.astype('f4')*.001,0),-1,0)
    obs['agent_pos']=np.concatenate([raw['agent']['qpos'],raw['agent']['qvel'],raw['extra']['tcp_pose']]).astype('f4')
    return obs

def scalar(x):
    if isinstance(x,torch.Tensor):x=x.detach().cpu().numpy()
    return bool(np.asarray(x).reshape(-1)[0])

def gt(task):
    def pose(obj):
        value=obj.pose if hasattr(obj,'pose') else obj
        return dict(p=value.p.detach().cpu().numpy().tolist(),q=value.q.detach().cpu().numpy().tolist())
    result={'tcp':pose(task.agent.tcp)}
    if hasattr(task,'cubeA'):result.update(cubeA=pose(task.cubeA),cubeB=pose(task.cubeB))
    if hasattr(task,'peg_head_pose'):result.update(peg_head=pose(task.peg_head_pose),hole=pose(task.box_hole_pose))
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--checkpoint',type=Path,required=True);args=ap.parse_args()
    ckpt=args.checkpoint
    meta=json.loads(ckpt.with_suffix('.json').read_text())
    if meta['write_status']!='atomic_complete':raise RuntimeError('snapshot not ready')
    payload=torch.load(ckpt,map_location='cpu',weights_only=False);cfg=payload['config']
    policy=create(cfg);policy.load_state_dict(payload['ema_model']);policy.to('cuda:0').eval()
    run=ROOT/'runs'/cfg['benchmark']/cfg['task']/cfg['method']/f"seed_{cfg['seed']}"
    coordinate=payload.get('checkpoint_step',payload['optimizer_updates'])
    tag='epoch' if cfg['benchmark']=='mimicgen' else 'update'
    output=run/'eval'/f"{tag}_{coordinate:06d}"
    output.mkdir(parents=True,exist_ok=True)
    path=output/'episodes.jsonl'
    completed={}
    if path.exists():
        for line in path.read_text().splitlines():
            row=json.loads(line);completed[row['reset_id']]=row
    env=create_analysis_env(cfg)
    (output/'render_device.json').write_text(json.dumps(dict(visible_gpu_uuid=os.environ['CUDA_VISIBLE_DEVICES'],
        physical_gpu=2,render_backend='MuJoCo EGL' if cfg['benchmark']=='mimicgen' else 'sapien_cuda:0',device=env.render_device)))
    try:
        with path.open('a',buffering=1) as log:
            for reset in cfg['reset_ids']:
                if reset in completed:continue
                torch.manual_seed(reset);torch.cuda.manual_seed_all(reset)
                frame,_=env.reset(seed=reset)
                history=deque([frame]*2,maxlen=2);once=False;at_end=False;steps=0;trajectory=[]
                policy.reset()
                while steps<cfg['horizon']:
                    obs={k:torch.from_numpy(np.stack([x[k] for x in history]))[None].to('cuda:0') for k in frame}
                    with torch.no_grad():actions=policy.predict_action(obs)['action'][0].cpu().numpy()
                    for action in actions:
                        frame,_,terminated,truncated,info=env.step(action);steps+=1
                        at_end=scalar(info.get('success',False));once|=at_end
                        trajectory.append(dict(step=steps,action=action.tolist(),success=at_end,gt_offline=env.gt()))
                        history.append(frame)
                        if steps>=cfg['horizon'] or terminated or truncated:break
                    if steps>=cfg['horizon'] or terminated or truncated:break
                traj=output/f'reset_{reset}_trajectory.json'
                traj.write_text(json.dumps(trajectory))
                record=dict(benchmark=cfg['benchmark'],task=cfg['task'],method=cfg['method'],seed=cfg['seed'],
                    reset_id=reset,checkpoint_step=coordinate,optimizer_updates=payload['optimizer_updates'],checkpoint_path=str(ckpt),
                    code_revision=payload['code_revision'],dataset_manifest=cfg['dataset_manifest'],
                    camera=cfg['cameras'],horizon=cfg['horizon'],actual_steps=steps,
                    success_at_end=at_end,success_once=once,success=once if cfg['benchmark']=='mimicgen' else at_end,
                    failure_reason=None if at_end else 'official_success_false_at_episode_end',
                    trajectory_path=str(traj),gpu_uuid=os.environ['CUDA_VISIBLE_DEVICES'])
                log.write(json.dumps(record)+'\n');completed[reset]=record
                print(json.dumps(dict(reset_id=reset,success_at_end=at_end,episodes_completed=len(completed))),flush=True)
    finally:env.close()
    if set(completed)!=set(cfg['reset_ids']):raise RuntimeError('reset set incomplete')
    numerator=sum(r['success'] for r in completed.values());denominator=cfg['episodes']
    summary=dict(meta,success_count=numerator,n_episodes=denominator,success_rate=numerator/denominator,
        success_definition='official task success over rollout (original DP max reward convention)' if cfg['benchmark']=='mimicgen' else 'success_at_end',success_once_count=sum(r['success_once'] for r in completed.values()),
        episodes_path=str(path),latency_status='unavailable: this concurrent rollout is not an isolated timing measurement')
    (output/'eval_summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
