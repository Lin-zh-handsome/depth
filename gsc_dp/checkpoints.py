"""Atomic resumable snapshots and independent savepoint evaluation registration."""
import json
import os
import shutil
from pathlib import Path
import torch
from jobs.registry import connect

def atomic_save(path, payload):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.tmp')
    with tmp.open('wb') as f:
        torch.save(payload,f);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
    fd=os.open(path.parent,os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)

def save(run, payload, scheduled=False):
    progress=payload.get('checkpoint_step',payload['optimizer_updates'])
    tag='epoch' if payload['config']['benchmark']=='mimicgen' else 'update'
    path=run/'checkpoints'/(f'{tag}_{progress:06d}.pt' if scheduled else 'recovery.pt')
    if scheduled and path.exists():
        raise FileExistsError(f'immutable scheduled snapshot exists: {path}')
    if scheduled:
        # Exact FP32 EMA for independent evaluation; full latest training state for recovery.
        # Existing historical checkpoints are never rewritten or deleted.
        atomic_save(run/'checkpoints/recovery.pt',payload)
        compact={k:payload[k] for k in ['config','ema_model','optimizer_updates','code_revision','gpu_uuid']}
        if 'checkpoint_step' in payload:compact['checkpoint_step']=payload['checkpoint_step']
        stores=[Path(p) for p in json.loads((Path(__file__).resolve().parents[1]/'configs/checkpoint_stores.json').read_text())]
        store=max(stores,key=lambda p:shutil.disk_usage(p).free)
        if shutil.disk_usage(store).free<75*1024**3:raise OSError('checkpoint storage below 75 GiB reserve')
        relative=Path(payload['config']['benchmark'])/payload['config']['task']/payload['config']['method']/f"seed_{payload['config']['seed']}"/path.name
        physical=store/relative
        if physical.exists():raise FileExistsError(physical)
        atomic_save(physical,compact)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.symlink_to(physical)
    else:
        atomic_save(path,payload)
    if scheduled:
        cfg=payload['config']
        meta=dict(benchmark=cfg['benchmark'],task=cfg['task'],method=cfg['method'],seed=cfg['seed'],
            checkpoint_step=progress,checkpoint_path=str(path),code_revision=payload['code_revision'],
            dataset_manifest=cfg['dataset_manifest'],gpu_uuid=payload['gpu_uuid'],
            optimizer_and_ema_saved=False,write_status='atomic_complete',snapshot_type='exact_fp32_ema_for_evaluation',
            physical_checkpoint_path=str(physical),full_resume_checkpoint=str(run/'checkpoints/recovery.pt'),
            integrity='atomic completed file + recorded metadata; no redundant hashing')
        path.with_suffix('.json').write_text(json.dumps(meta,indent=2))
        db=connect()
        db.execute('INSERT OR IGNORE INTO jobs(kind,benchmark,task,method,seed,checkpoint_step,checkpoint_path,config_path,prerequisite) VALUES(?,?,?,?,?,?,?,?,?)',
            ('eval',cfg['benchmark'],cfg['task'],cfg['method'],cfg['seed'],progress,str(path),
             str(run/'config_resolved.json'),'atomic_complete snapshot'))
        db.execute("UPDATE jobs SET checkpoint_path=?,config_path=?,prerequisite=NULL WHERE kind='eval' AND benchmark=? AND task=? AND method=? AND seed=? AND checkpoint_step=?",
            (str(path),str(run/'config_resolved.json'),cfg['benchmark'],cfg['task'],cfg['method'],cfg['seed'],progress))
        db.commit();db.close()
    return path
