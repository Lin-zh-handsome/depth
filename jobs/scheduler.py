"""Single-physical-GPU, recoverable training and independent eval dispatcher."""
import csv
import fcntl
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from registry import ROOT, connect

GPU='GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9'
TRAIN_PY='/home/linzhenghong/miniconda3/envs/gsc-robodiff/bin/python'
EVAL_PY='/home/linzhenghong/miniconda3/envs/gsc-thesis-eval/bin/python'
MIMIC_PY='/home/linzhenghong/miniconda3/envs/gsc-thesis-mimic/bin/python'
def now():return datetime.now(timezone.utc).isoformat()
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
    for r in db.execute("SELECT * FROM eval_jobs WHERE status='finished' AND method='e6' AND ((benchmark='maniskill' AND checkpoint_step=100000) OR (benchmark='mimicgen' AND checkpoint_step=250))").fetchall():
        count=db.execute("SELECT count(*) FROM eval_jobs WHERE benchmark=? AND task=? AND seed=? AND checkpoint_step=? AND method IN ('e0','e1','e6') AND status='finished'",
            (r['benchmark'],r['task'],r['seed'],r['checkpoint_step'])).fetchone()[0]
        if count==3:
            db.execute("INSERT OR IGNORE INTO jobs(kind,benchmark,task,method,seed,checkpoint_step,prerequisite) VALUES('analysis',?,?,'paired_e0_e1_e6',?,?,NULL)",
                (r['benchmark'],r['task'],r['seed'],r['checkpoint_step']))
    db.commit()

def main():
    lock=(ROOT/'jobs/scheduler.lock').open('w')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    env=os.environ.copy();env.update(CUDA_VISIBLE_DEVICES=GPU,GSC_GPU='2',
        MUJOCO_EGL_DEVICE_ID='2',MUJOCO_GL='egl',OMP_NUM_THREADS='2',MKL_NUM_THREADS='2',
        OPENBLAS_NUM_THREADS='2',NUMEXPR_NUM_THREADS='2',PYTHONNOUSERSITE='1',
        PYTHONPATH=str(ROOT)+':'+str(ROOT/'source/diffusion_policy'),PYTHONUNBUFFERED='1')
    db=connect();children={}
    # Recover statuses after dispatcher interruption, preserving live workers.
    for r in db.execute("SELECT * FROM jobs WHERE status='running'").fetchall():
        if not pid_alive(r['pid']):
            db.execute("UPDATE jobs SET status='queued',error='dispatcher recovery: worker no longer alive' WHERE id=?",(r['id'],))
    db.commit()
    print('single GPU scheduler active',GPU,'pid',os.getpid(),flush=True)
    while True:
        for r in db.execute("SELECT * FROM jobs WHERE status='running'").fetchall():
            if r['id'] in children or pid_alive(r['pid']):continue
            run=ROOT/'runs'/r['benchmark']/r['task']/r['method']/f"seed_{r['seed']}"
            marker=run/'training_complete.json' if r['kind']=='train' else run/'eval'/f"update_{r['checkpoint_step']:06d}"/'eval_summary.json'
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
                (status,now(),code,None if code==0 else f'worker exit {code}; see logs/job_{id}.log',id))
            db.commit();del children[id]
            print('worker completed',id,status,code,flush=True)
        live=db.execute("SELECT * FROM jobs WHERE status='running'").fetchall()
        ntrain=sum(r['kind']=='train' for r in live);neval=sum(r['kind']=='eval' for r in live)
        nanalysis=sum(r['kind']=='analysis' for r in live)
        register_temporal(db)
        load=os.getloadavg()[0]
        free=gpu_free()
        if load<140 and free>20000:
            # Reserve one evaluation slot as soon as a snapshot is available;
            # only this selected physical GPU is ever exposed to any worker.
            ready=(ROOT/'logs/eval_env.ready').exists()
            kind='eval' if neval<1 and ready and db.execute("SELECT 1 FROM eval_jobs WHERE status='queued' LIMIT 1").fetchone() else 'analysis' if nanalysis<1 and ready and db.execute("SELECT 1 FROM analysis_jobs WHERE status='queued' LIMIT 1").fetchone() else 'train'
            cap=6 if kind=='train' else 1
            if {'train':ntrain,'eval':neval,'analysis':nanalysis}[kind]<cap:
                rows=db.execute("SELECT * FROM jobs WHERE kind=? AND status='queued' AND prerequisite IS NULL ORDER BY seed, CASE method WHEN 'e0' THEN 0 WHEN 'e1' THEN 1 WHEN 'e6' THEN 2 ELSE 3 END, id",(kind,)).fetchall()
                # Snapshot eval dependencies are already atomic-complete.
                if kind=='eval':
                    rows=db.execute("SELECT * FROM eval_jobs WHERE status='queued' ORDER BY checkpoint_step,id").fetchall()
                if rows:
                    r=rows[0]
                    if kind=='train': cmd=[TRAIN_PY,str(ROOT/'train.py'),'--config',r['config_path']]
                    elif kind=='eval':cmd=[EVAL_PY,str(ROOT/'evaluate.py'),'--checkpoint',r['checkpoint_path']]
                    else:cmd=[MIMIC_PY if r['benchmark']=='mimicgen' else EVAL_PY,
                        str(ROOT/'analysis/dispatch_temporal.py'),'--benchmark',r['benchmark'],
                        '--task',r['task'],'--seed',str(r['seed']),'--step',str(r['checkpoint_step'])]
                    log=(ROOT/'logs'/f"job_{r['id']}.log").open('a')
                    process=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True);log.close()
                    children[r['id']]=process
                    db.execute("UPDATE jobs SET status='running',pid=?,started=?,attempts=attempts+1,error=NULL WHERE id=?",(process.pid,now(),r['id']));db.commit()
                    print('launched',r['id'],kind,r['task'],r['method'],r['seed'],'pid',process.pid,'freeMiB',free,flush=True)
        snapshot(db)
        time.sleep(30)

if __name__=='__main__':main()
