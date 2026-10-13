"""Atomic resumable snapshots and independent savepoint evaluation registration."""
import json
import os
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
    progress=payload['optimizer_updates']
    path=run/'checkpoints'/('update_%06d.pt'%progress if scheduled else 'recovery.pt')
    if scheduled and path.exists():
        raise FileExistsError(f'immutable scheduled snapshot exists: {path}')
    atomic_save(path,payload)
    if scheduled:
        cfg=payload['config']
        meta=dict(benchmark=cfg['benchmark'],task=cfg['task'],method=cfg['method'],seed=cfg['seed'],
            checkpoint_step=progress,checkpoint_path=str(path),code_revision=payload['code_revision'],
            dataset_manifest=cfg['dataset_manifest'],gpu_uuid=payload['gpu_uuid'],
            optimizer_and_ema_saved=True,write_status='atomic_complete',
            integrity='atomic completed file + recorded metadata; no redundant hashing')
        path.with_suffix('.json').write_text(json.dumps(meta,indent=2))
        db=connect()
        db.execute('INSERT OR IGNORE INTO jobs(kind,benchmark,task,method,seed,checkpoint_step,checkpoint_path,config_path,prerequisite) VALUES(?,?,?,?,?,?,?,?,?)',
            ('eval',cfg['benchmark'],cfg['task'],cfg['method'],cfg['seed'],progress,str(path),
             str(run/'config_resolved.json'),'atomic_complete snapshot'))
        db.commit();db.close()
    return path
