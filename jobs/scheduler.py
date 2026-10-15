"""Single-physical-GPU, recoverable training and independent eval dispatcher."""
import csv
import fcntl
import json
import os
import signal
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from registry import ROOT, connect
sys.path.insert(0,str(ROOT))
from gsc_dp.protocol import FORMAL_METHODS,validate_formal_config

GPU='GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9'
TRAIN_PY='/home/linzhenghong/miniconda3/envs/gsc-robodiff/bin/python'
EVAL_PY='/home/linzhenghong/miniconda3/envs/gsc-thesis-eval/bin/python'
MIMIC_PY='/home/linzhenghong/miniconda3/envs/gsc-thesis-mimic/bin/python'
def now():return datetime.now(timezone.utc).isoformat()
def record_progress(message):
    path=ROOT.parent/'.planning/protocol_v1/progress.md'
    with path.open('a',encoding='utf-8') as f:f.write('\n'+now()+' '+message+'\n')
def gpu_free():
    s=subprocess.check_output(['nvidia-smi','-i',GPU,'--query-gpu=memory.free','--format=csv,noheader,nounits'],text=True)
    return int(s.strip())
def pid_alive(pid):
    try: os.kill(pid,0);return True
    except (ProcessLookupError,TypeError):return False
def snapshot(db):
    rows=db.execute('SELECT * FROM jobs ORDER BY id').fetchall()
    target=ROOT/'runs/index.csv';tmp=target.with_suffix('.tmp')
    with tmp.open('w',newline='') as f:
        w=csv.writer(f);w.writerow(rows[0].keys() if rows else [])
        for r in rows:w.writerow(tuple(r))
    os.replace(tmp,target)

def register_temporal(db):
    groups=db.execute("SELECT benchmark,task,seed,count(*) n FROM eval_jobs WHERE status='finished' GROUP BY benchmark,task,seed HAVING n=20").fetchall()
    for r in groups:
        db.execute("INSERT OR IGNORE INTO jobs(kind,benchmark,task,method,seed,checkpoint_step,prerequisite) VALUES('analysis',?,?,'paired_best',?,?,NULL)",
            (r['benchmark'],r['task'],r['seed'],250 if r['benchmark']=='mimicgen' else 100000))
    db.commit()

TASK_ORDER=['threading_d2','PegInsertionSide-v1','stack_three_d1','coffee_d2','StackCube-v1']
def active_task(db):
    for task in TASK_ORDER:
        train=db.execute("SELECT count(*),sum(status='finished') FROM train_jobs WHERE task=?",(task,)).fetchone()
        evaluation=db.execute("SELECT count(*),sum(status='finished') FROM eval_jobs WHERE task=?",(task,)).fetchone()
        if train[0]!=12 or train[1]!=12 or evaluation[0]!=60 or evaluation[1]!=60:return task
    return None

def focused_run(db):
    path=ROOT/'jobs/focus_run.json'
    if not path.exists():return None
    cfg=json.loads(path.read_text())
    if cfg.get('status')!='active':return None
    pending=[]
    for seed in cfg['seeds']:
        complete=db.execute("SELECT status FROM train_jobs WHERE task=? AND method=? AND seed=?",(cfg['task'],cfg['method'],seed)).fetchone()
        count=db.execute("SELECT count(*) FROM eval_jobs WHERE task=? AND method=? AND seed=? AND status='finished'",(cfg['task'],cfg['method'],seed)).fetchone()[0]
        if not complete or complete['status']!='finished' or count!=5:pending.append(seed)
    if pending:
        for seed in pending:
            db.execute("UPDATE jobs SET status='queued',error=NULL WHERE task=? AND method=? AND seed=? AND status='held_for_full_method'",(cfg['task'],cfg['method'],seed))
        db.commit()
        return dict(task=cfg['task'],method=cfg['method'],seeds=pending,max_train=cfg.get('max_training_workers',3))
    cfg['status']='completed';cfg['finished']=now();path.write_text(json.dumps(cfg,indent=2))
    db.execute("UPDATE jobs SET status='queued',error=NULL WHERE status='held_for_full_method'");db.commit()
    record_progress('Full method three seeds and 15 scheduled evaluations completed; resume remaining work of the current task.')
    return None

def in_focus(row,focus):
    return row['task']==focus['task'] and row['method']==focus['method'] and row['seed'] in focus['seeds']

def main():
    if (ROOT/'jobs/PAUSED_BY_USER.json').exists():
        print('Dispatcher paused by user; explicit rescheduling is required.',flush=True)
        return
    lock=(ROOT/'jobs/scheduler.lock').open('w')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES=GPU,GSC_GPU='2',
        MUJOCO_EGL_DEVICE_ID='2',MUJOCO_GL='egl',OMP_NUM_THREADS='2',MKL_NUM_THREADS='2',
        OPENBLAS_NUM_THREADS='2',NUMEXPR_NUM_THREADS='2',PYTHONNOUSERSITE='1',
        PYTHONPATH=str(ROOT)+':'+str(ROOT/'source/diffusion_policy'),PYTHONUNBUFFERED='1')
    db=connect();children={}
    seen_manifests={}
    previous_task=None
    # Recover statuses after dispatcher interruption, preserving live workers.
    for r in db.execute("SELECT * FROM jobs WHERE status='running'").fetchall():
        if not pid_alive(r['pid']):
            run=ROOT/'runs'/r['benchmark']/r['task']/r['method']/f"seed_{r['seed']}"
            tag='epoch' if r['benchmark']=='mimicgen' else 'update'
            marker=run/'training_complete.json' if r['kind']=='train' else run/'eval'/f"{tag}_{r['checkpoint_step']:06d}"/'eval_summary.json'
            status='finished' if marker.exists() else 'queued'
            db.execute("UPDATE jobs SET status=?,error=? WHERE id=?",(status,None if status=='finished' else 'dispatcher recovery: worker no longer alive',r['id']))
    db.commit()
    print('single GPU scheduler active',GPU,'pid',os.getpid(),flush=True)
    while True:
        manifests={p:(p.stat().st_mtime_ns,p.stat().st_size) for p in (ROOT/'data/manifests').glob('*.json')}
        if manifests!=seen_manifests:
            subprocess.run([TRAIN_PY,str(ROOT/'generate_run_configs.py')],cwd=ROOT,env=env,check=True)
            seen_manifests=manifests
            record_progress('Dataset manifests available: '+', '.join(sorted(p.name for p in manifests))+'. Runnable configs refreshed without reducing any budget.')
        for r in db.execute("SELECT * FROM jobs WHERE status='running'").fetchall():
            if r['id'] in children or pid_alive(r['pid']):continue
            run=ROOT/'runs'/r['benchmark']/r['task']/r['method']/f"seed_{r['seed']}"
            tag='epoch' if r['benchmark']=='mimicgen' else 'update'
            marker=run/'training_complete.json' if r['kind']=='train' else run/'eval'/f"{tag}_{r['checkpoint_step']:06d}"/'eval_summary.json'
            status='finished' if marker.exists() else 'queued' if r['attempts']<r['max_attempts'] else 'failed'
            db.execute('UPDATE jobs SET status=?,finished=?,error=? WHERE id=?',
                (status,now(),None if status=='finished' else 'adopted worker exited; inspect its job log',r['id']))
        db.commit()
        for id,process in list(children.items()):
            code=process.poll()
            if code is None:continue
            r=db.execute('SELECT * FROM jobs WHERE id=?',(id,)).fetchone()
            retry=code!=0 and r['attempts']<r['max_attempts']
            status='finished' if code==0 else 'queued' if retry else 'failed'
            db.execute('UPDATE jobs SET status=?,finished=?,exit_code=?,error=? WHERE id=?',
                (status,now(),code,None if code==0 else f'worker exit {code}; see logs/final_job_{id}.log',id))
            db.commit();del children[id]
            print('worker completed',id,status,code,flush=True)
            record_progress(f"Job {id} {r['kind']} {r['task']}/{r['method']}/seed_{r['seed']} {status}, exit={code}; logs/final_job_{id}.log")
        live=db.execute("SELECT * FROM jobs WHERE status='running'").fetchall()
        ntrain=sum(r['kind']=='train' for r in live);neval=sum(r['kind']=='eval' for r in live)
        nmimic=sum(r['kind']=='train' and r['benchmark']=='mimicgen' for r in live)
        nanalysis=sum(r['kind']=='analysis' for r in live)
        register_temporal(db)
        focus=focused_run(db)
        current_task=active_task(db)
        if current_task!=previous_task:
            state=dict(mode='one_task_at_a_time',task_order=TASK_ORDER,active_task=current_task,
                switch_condition='12 complete training runs and 60 complete scheduled evaluations',timestamp=now())
            (ROOT/'jobs/task_dispatch_state.json').write_text(json.dumps(state,indent=2))
            record_progress('Sequential task scheduling: active task '+str(current_task)+'. Switch only after all 12 training runs and 60 evaluations finish.')
            previous_task=current_task
        load=os.getloadavg()[0]
        free=gpu_free()
        if load<140 and free>20000 and shutil.disk_usage(ROOT).free>50*1024**3:
            # Reserve one evaluation slot as soon as a snapshot is available;
            # only this selected physical GPU is ever exposed to any worker.
            ready=(ROOT/'logs/eval_env.ready').exists()
            ready_evals=db.execute("SELECT * FROM eval_jobs WHERE status='queued' AND prerequisite IS NULL AND task=?",(current_task,)).fetchall()
            if focus:ready_evals=[r for r in ready_evals if in_focus(r,focus)]
            kind='eval' if neval<2 and ready and ready_evals else 'analysis' if not focus and nanalysis<1 and ready and db.execute("SELECT 1 FROM analysis_jobs WHERE status='queued' AND prerequisite IS NULL LIMIT 1").fetchone() else 'train'
            cap=(focus['max_train'] if focus else 6) if kind=='train' else 2 if kind=='eval' else 1
            if {'train':ntrain,'eval':neval,'analysis':nanalysis}[kind]<cap:
                rows=db.execute("SELECT * FROM jobs WHERE kind=? AND status='queued' AND prerequisite IS NULL ORDER BY CASE method WHEN 'e6' THEN 0 WHEN 'e3' THEN 1 WHEN 'm3' THEN 2 ELSE 3 END, CASE task WHEN 'threading_d2' THEN 0 WHEN 'PegInsertionSide-v1' THEN 1 WHEN 'stack_three_d1' THEN 2 WHEN 'coffee_d2' THEN 3 ELSE 4 END, seed, id",(kind,)).fetchall()
                # Snapshot eval dependencies are already atomic-complete.
                if kind=='eval':
                    # FIFO across benchmarks: epoch and optimizer-update indices have different units.
                    rows=db.execute("SELECT * FROM eval_jobs WHERE status='queued' AND prerequisite IS NULL ORDER BY CASE method WHEN 'e6' THEN 0 WHEN 'e3' THEN 1 WHEN 'm3' THEN 2 ELSE 3 END, id").fetchall()
                if kind in ['train','eval']:
                    rows=[r for r in rows if r['task']==current_task and r['method'] in FORMAL_METHODS]
                if focus:
                    rows=[r for r in rows if in_focus(r,focus)]
                if kind=='train':
                    # Two concurrent runs per method permit all three methods to progress.
                    rows=[r for r in rows if sum(x['kind']=='train' and x['method']==r['method'] for x in live)<(focus['max_train'] if focus else 2)]
                if rows:
                    r=rows[0]
                    if kind in ['train','eval']:
                        validate_formal_config(json.loads(Path(r['config_path']).read_text()))
                    if kind=='train': cmd=[TRAIN_PY,str(ROOT/'train.py'),'--config',r['config_path']]
                    elif kind=='eval':cmd=[MIMIC_PY if r['benchmark']=='mimicgen' else EVAL_PY,
                        str(ROOT/'evaluate.py'),'--checkpoint',r['checkpoint_path']]
                    else:cmd=[MIMIC_PY if r['benchmark']=='mimicgen' else EVAL_PY,
                        str(ROOT/'analysis/dispatch_temporal.py'),'--benchmark',r['benchmark'],
                        '--task',r['task'],'--seed',str(r['seed']),'--step',str(r['checkpoint_step'])]
                    log=(ROOT/'logs'/f"final_job_{r['id']}.log").open('a')
                    process=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True);log.close()
                    children[r['id']]=process
                    db.execute("UPDATE jobs SET status='running',pid=?,started=?,attempts=attempts+1,error=NULL WHERE id=?",(process.pid,now(),r['id']));db.commit()
                    print('launched',r['id'],kind,r['task'],r['method'],r['seed'],'pid',process.pid,'freeMiB',free,flush=True)
                    record_progress(f"Job {r['id']} {kind} {r['task']}/{r['method']}/seed_{r['seed']}/point_{r['checkpoint_step']} launched PID={process.pid}, GPU={GPU}, freeMiB={free}; logs/final_job_{r['id']}.log")
        snapshot(db)
        subprocess.run([TRAIN_PY,str(ROOT/'jobs/maintain_checkpoints.py')],cwd=ROOT,env=env,stdout=subprocess.DEVNULL)
        try:
            subprocess.run([TRAIN_PY,str(ROOT/'jobs/export_ch3.py')],cwd=ROOT,env=env,check=True,stdout=subprocess.DEVNULL)
        except Exception as exc:
            print('incremental export failed',repr(exc),flush=True)
        time.sleep(30)

if __name__=='__main__':main()
