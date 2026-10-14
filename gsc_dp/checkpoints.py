"""Five-point snapshots, atomic best/latest, bounded queue and per-file cleanup."""
import json,os,time
from pathlib import Path
import torch
from jobs.registry import ROOT,connect
SCHEDULE_FIELDS={'interval','savepoints','eval_positions'}
def same_training_config(a,b):
    return {k:v for k,v in a.items() if k not in SCHEDULE_FIELDS}=={k:v for k,v in b.items() if k not in SCHEDULE_FIELDS}
def atomic_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w') as f:json.dump(value,f,indent=2);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
def atomic_save(path,payload):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_name(path.name+'.tmp')
    with tmp.open('wb') as f:torch.save(payload,f);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
def wait_for_evaluation(cfg,stop):
    announced=False
    while not stop[0]:
        db=connect();n=db.execute("SELECT count(*) FROM eval_jobs WHERE benchmark=? AND task=? AND method=? AND seed=? AND checkpoint_path IS NOT NULL AND status!='finished' AND prerequisite IS NULL",(cfg['benchmark'],cfg['task'],cfg['method'],cfg['seed'])).fetchone()[0];db.close()
        if n==0:return True
        if not announced:print('run backpressure: awaiting scheduled evaluation',n,flush=True);announced=True
        time.sleep(5)
    return False
def save(run,payload,scheduled=False):
    latest=run/'checkpoints/recovery.pt';atomic_save(latest,payload)
    if not scheduled:return latest
    cfg=payload['config'];progress=payload.get('checkpoint_step',payload['optimizer_updates'])
    if progress not in cfg['eval_positions']:raise ValueError('outside five prescribed eval positions')
    tag='epoch' if cfg['benchmark']=='mimicgen' else 'update';path=run/'checkpoints'/f'{tag}_{progress:06d}.pt'
    db=connect()
    while True:
        db.execute('BEGIN IMMEDIATE')
        n=db.execute("SELECT count(*) FROM eval_jobs WHERE status!='finished' AND (prerequisite='writing snapshot' OR (prerequisite IS NULL AND checkpoint_path IS NOT NULL))").fetchone()[0]
        if n<4:
            count=db.execute("UPDATE jobs SET prerequisite='writing snapshot' WHERE kind='eval' AND benchmark=? AND task=? AND method=? AND seed=? AND checkpoint_step=? AND status!='finished'",(cfg['benchmark'],cfg['task'],cfg['method'],cfg['seed'],progress)).rowcount;db.commit()
            if not count:raise ValueError('eval event missing or already completed')
            break
        db.rollback();time.sleep(5)
    if path.exists():raise FileExistsError(path)
    compact={k:payload[k] for k in ['config','ema_model','optimizer_updates','code_revision','gpu_uuid']};compact['checkpoint_step']=progress
    atomic_save(path,compact)
    atomic_json(path.with_suffix('.json'),dict(benchmark=cfg['benchmark'],task=cfg['task'],method=cfg['method'],seed=cfg['seed'],checkpoint_step=progress,checkpoint_path=str(path),code_revision=payload['code_revision'],dataset_manifest=cfg['dataset_manifest'],gpu_uuid=payload['gpu_uuid'],write_status='atomic_complete',snapshot_type='temporary_exact_fp32_ema',full_resume_checkpoint=str(latest),integrity='actual config, atomic metadata; hashing omitted by user request'))
    db.execute("UPDATE jobs SET checkpoint_path=?,config_path=?,prerequisite=NULL WHERE kind='eval' AND benchmark=? AND task=? AND method=? AND seed=? AND checkpoint_step=?",(str(path),str(run/'config_resolved.json'),cfg['benchmark'],cfg['task'],cfg['method'],cfg['seed'],progress));db.commit();db.close();return path
def opened(path):
    target=path.resolve()
    for proc in Path('/proc').iterdir():
        if not proc.name.isdigit():continue
        try:
            if proc.stat().st_uid!=os.getuid():continue
            for fd in (proc/'fd').iterdir():
                try:
                    if fd.resolve()==target:return True
                except (OSError,RuntimeError):pass
        except OSError:pass
    return False
def finalize(run):
    cfg=json.loads((run/'config_resolved.json').read_text());tag='epoch' if cfg['benchmark']=='mimicgen' else 'update';results=[]
    for point in cfg['eval_positions']:
        p=run/'eval'/f'{tag}_{point:06d}'/'eval_summary.json'
        if p.exists():results.append(json.loads(p.read_text()))
    if not results:return
    chosen=min(results,key=lambda r:(-r['success_rate'],r['checkpoint_step']))
    best=run/'best/best.pt';bm=best.with_suffix('.json');old=json.loads(bm.read_text()) if bm.exists() else None
    if old is None or old['checkpoint_step']!=chosen['checkpoint_step']:
        source=Path(chosen['checkpoint_path'])
        if not source.exists():raise FileNotFoundError('winning snapshot missing '+str(source))
        payload=torch.load(source,map_location='cpu',weights_only=False)
        compact={k:payload[k] for k in ['config','ema_model','optimizer_updates','code_revision','gpu_uuid']};compact['checkpoint_step']=chosen['checkpoint_step']
        atomic_save(best,compact);atomic_json(bm,dict(chosen,best_checkpoint_path=str(best),selection='highest of five prescribed points; earliest on ties'));del payload,compact
    db=connect()
    for r in results:
        row=db.execute("SELECT * FROM eval_jobs WHERE benchmark=? AND task=? AND method=? AND seed=? AND checkpoint_step=?",(cfg['benchmark'],cfg['task'],cfg['method'],cfg['seed'],r['checkpoint_step'])).fetchone()
        if not row or row['status']!='finished':continue
        cp=Path(r['checkpoint_path'])
        if not cp.exists():continue
        physical=cp.resolve()
        refs=db.execute("SELECT 1 FROM jobs WHERE checkpoint_path=? AND status IN ('running','queued')",(str(cp),)).fetchone()
        if refs or opened(cp) or physical==best.resolve() or physical==(run/'checkpoints/recovery.pt').resolve():continue
        if physical.stat().st_uid!=os.getuid() or not physical.is_relative_to(ROOT):continue
        audit=dict(timestamp=time.time(),path=str(cp),physical=str(physical),bytes=physical.stat().st_size,result=r['episodes_path'],best=str(best),reason='complete eval, atomic best, no live reference/open file',hash='omitted by user instruction')
        audit_path=ROOT/'experiments/ch3/checkpoint_cleanup.jsonl'
        with audit_path.open('a') as f:f.write(json.dumps(dict(audit,action='candidate'))+'\n')
        if cp.is_symlink():cp.unlink();physical.unlink()
        else:cp.unlink()
        with audit_path.open('a') as f:f.write(json.dumps(dict(audit,action='deleted'))+'\n')
    latest=run/'checkpoints/recovery.pt'
    if (run/'training_complete.json').exists() and len(results)==5 and best.exists() and latest.exists() and not opened(latest):
        if not db.execute("SELECT 1 FROM train_jobs WHERE benchmark=? AND task=? AND method=? AND seed=? AND status!='finished'",(cfg['benchmark'],cfg['task'],cfg['method'],cfg['seed'])).fetchone():
            size=latest.stat().st_size;latest.unlink()
            with (ROOT/'experiments/ch3/checkpoint_cleanup.jsonl').open('a') as f:f.write(json.dumps(dict(action='deleted_completed_latest',path=str(latest),bytes=size,timestamp=time.time(),best=str(best)))+'\n')
    db.close()
