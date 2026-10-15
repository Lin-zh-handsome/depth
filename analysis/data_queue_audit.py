"""Inspect actual datasets, window sampler, immutable configs and current queue."""
import sys,json,math,csv,sqlite3,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'source/diffusion_policy')]
import numpy as np,h5py,zarr
from gsc_dp.dataset import ManiSkillRGBDImageDataset
OUT=ROOT/'docs/audit_55951414';OUT.mkdir(parents=True,exist_ok=True)
protocol=json.loads((ROOT/'configs/protocol.json').read_text())
budget=[];comparisons=[]
for t in protocol['tasks']:
    configs=[json.loads(p.read_text()) for p in (ROOT/'configs/runs'/t['benchmark']/t['task']).glob('*/seed_*.json') if p.parent.name in ['e0','e3','e6','m3']]
    batches=sorted(set(c['batch_size'] for c in configs));assert len(configs)==12 and len(batches)==1
    cfg=configs[0];d=ManiSkillRGBDImageDataset(cfg['zarr_path'],horizon=16,pad_before=1,pad_after=7,n_obs_steps=2,seed=0,val_ratio=0)
    lengths=np.diff(np.r_[0,d.replay_buffer.episode_ends]);windows=len(d);b=cfg['batch_size'];per_epoch=math.ceil(windows/b)
    row=dict(benchmark=t['benchmark'],task=t['task'],episodes=len(lengths),steps=int(lengths.sum()),batch_size=b,sequence_length=16,pad_before=1,pad_after=7,validation_episodes=int((~d.train_mask).sum()),true_window_count=windows,sampler_index_shape=list(d.sampler.indices.shape),optimizer_updates_per_complete_epoch=per_epoch,last_batch_size=windows%b or b,drop_last=False,gradient_accumulation=1,training_budget=t['budget'],training_budget_unit=t['progress_unit'],total_optimizer_updates=per_epoch*t['budget'] if t['benchmark']=='mimicgen' else t['budget'],eval_positions=cfg['eval_positions'],processed_path=cfg['zarr_path'],existing_run_budget_metadata=[])
    for p in (ROOT/'runs'/t['benchmark']/t['task']).glob('*/seed_*/dataset_window_budget.json'):
        m=json.loads(p.read_text());row['existing_run_budget_metadata'].append(dict(path=str(p),matches=m['dataset_window_count']==windows and m['batch_size']==b and m['total_optimizer_updates']==row['total_optimizer_updates']))
    budget.append(row)
    canonical={k:v for k,v in cfg.items() if k not in ['method','seed']}
    comparisons.append(dict(task=t['task'],configs=len(configs),all_configs_equal_except_method_and_seed=all({k:v for k,v in x.items() if k not in ['method','seed']}==canonical for x in configs),same_zarr_path=len({c['zarr_path'] for c in configs})==1,same_shape_meta=all(c['shape_meta']==cfg['shape_meta'] for c in configs),same_crop_shape=all(c['crop_shape']==cfg['crop_shape'] for c in configs)))
(OUT/'window_update_budgets.json').write_text(json.dumps(budget,indent=2))
(ROOT/'experiments/ch3/dataset_budget_metadata.json').write_text(json.dumps(budget,indent=2))
(OUT/'controlled_configs.json').write_text(json.dumps(comparisons,indent=2))

m=json.loads((ROOT/'data/manifests/PegInsertionSide-v1_100.json').read_text());srcmeta=json.loads(Path(m['source']).with_suffix('.json').read_text());repmeta=json.loads(Path(m['raw_replay_metadata']).read_text())
source_by_id={e['episode_id']:e for e in srcmeta['episodes']};cache=zarr.open(m['processed_path'],'r');ends=cache['meta/episode_ends'][:]
peg=[]
with h5py.File(m['source'],'r') as src,h5py.File(Path(m['raw_replay_metadata']).with_suffix('.h5'),'r') as replay:
    for i,(sid,eid,ep) in enumerate(zip(m['subset_ids'],m['replay_episode_ids'],repmeta['episodes'])):
        s=source_by_id[sid];g=replay[f'traj_{eid}'];n=len(g['actions']);start=int(ends[i-1]) if i else 0;stop=int(ends[i]);a=cache['data/action'][start:stop]
        obs=g['obs'];proprio=np.concatenate([obs['agent/qpos'][:n],obs['agent/qvel'][:n],obs['extra/tcp_pose'][:n]],-1).astype('f4')
        visual={}
        for cam in m['cameras']:
            ts=np.unique([0,n//2,n-1]);raw_rgb=obs[f'sensor_data/{cam}/rgb'][ts];raw_depth=obs[f'sensor_data/{cam}/depth'][ts].astype('f4')*.001
            visual[cam]=dict(rgb_exact=bool(np.array_equal(cache['data'][cam+'_image'][start+ts],raw_rgb)),depth_max_abs_m=float(np.abs(cache['data'][cam+'_depth'][start+ts]-raw_depth).max()))
        peg.append(dict(source_episode_id=sid,replay_episode_id=eid,source_success=s.get('success'),replay_success=ep.get('success'),source_seed=s.get('episode_seed'),replay_seed=ep.get('episode_seed'),source_reset_kwargs=s.get('reset_kwargs'),replay_reset_kwargs=ep.get('reset_kwargs'),source_action_shape=list(src[f'traj_{sid}/actions'].shape),replay_action_shape=list(g['actions'].shape),train_cache_window=[start,stop],cached_steps=stop-start,source_steps=s.get('elapsed_steps'),replay_steps=ep.get('elapsed_steps'),action_exact=bool(np.array_equal(a,g['actions'][:].astype('f4'))),proprio_exact=bool(np.array_equal(cache['data/agent_pos'][start:stop],proprio)),visual=visual))
result=dict(task=m['task'],source_path=m['source'],replay_path=str(Path(m['raw_replay_metadata']).with_suffix('.h5')),processed_path=m['processed_path'],n_trajectories=len(peg),source_success_counts={str(x):sum(p['source_success']==x for p in peg) for x in [True,False,None]},replay_success_counts={str(x):sum(p['replay_success']==x for p in peg) for x in [True,False,None]},failed_replay_source_ids=[p['source_episode_id'] for p in peg if p['replay_success'] is False],all_replay_actions_in_training=all(p['action_exact'] for p in peg),all_replay_proprio_in_training=all(p['proprio_exact'] for p in peg),trajectory_records=peg)
(OUT/'peg_100_source_replay_cache.json').write_text(json.dumps(result,indent=2))
db=sqlite3.connect(ROOT/'jobs/ch3_final_queue.db');db.row_factory=sqlite3.Row
jobs=[dict(x) for x in db.execute('SELECT * FROM jobs')];formal=[r for r in jobs if r['kind'] in ['train','eval']]
bad=[]
for r in formal:
    cfg=json.loads(Path(r['config_path']).read_text()) if r['config_path'] and Path(r['config_path']).exists() else None
    if r['method'] not in ['e0','e3','e6','m3']:bad.append(dict(id=r['id'],reason='unsupported method'))
    t=next(t for t in protocol['tasks'] if t['task']==r['task']);positions=list(range(t['interval'],t['budget']+1,t['interval']))
    if r['kind']=='eval' and r['checkpoint_step'] not in positions:bad.append(dict(id=r['id'],reason='non-protocol checkpoint'))
    if cfg and cfg['benchmark']=='maniskill' and cfg['control_mode']!={'PegInsertionSide-v1':'pd_ee_delta_pose','StackCube-v1':'pd_ee_delta_pos'}[r['task']]:bad.append(dict(id=r['id'],reason='historical control mode'))
queue=dict(checked_at=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),source='jobs/ch3_final_queue.db',train_count=sum(r['kind']=='train' for r in formal),eval_count=sum(r['kind']=='eval' for r in formal),methods=sorted({r['method'] for r in formal}),errors=bad,counts=[dict(r) for r in db.execute('select kind,status,count(*) n from jobs group by kind,status')],running=[{k:r[k] for k in ['id','kind','task','method','seed','checkpoint_step','pid']} for r in formal if r['status']=='running'])
(OUT/'queue_scope.json').write_text(json.dumps(queue,indent=2));db.close()
print(json.dumps(dict(budgets=[{k:r[k] for k in ['task','steps','true_window_count','optimizer_updates_per_complete_epoch','total_optimizer_updates']} for r in budget],peg_source=result['source_success_counts'],peg_replay=result['replay_success_counts'],failed_replay_ids=result['failed_replay_source_ids'],cache_actions=result['all_replay_actions_in_training'],controlled_configs=comparisons,queue=queue),ensure_ascii=False),flush=True)
