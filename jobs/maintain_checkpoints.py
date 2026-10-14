"""Recover interrupted best promotion and cleanup outside GPU workers."""
import sys
from registry import ROOT,connect
sys.path.insert(0,str(ROOT))
from gsc_dp.checkpoints import finalize
if __name__=='__main__':
    db=connect()
    for r in db.execute("SELECT DISTINCT benchmark,task,method,seed FROM eval_jobs WHERE status='finished'"):
        run=ROOT/'runs'/r['benchmark']/r['task']/r['method']/f"seed_{r['seed']}"
        try:finalize(run)
        except Exception as e:print('checkpoint maintenance failed',str(run),repr(e),flush=True)
