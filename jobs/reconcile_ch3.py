"""Merge the supplied matrix with actual frozen configs and complete reset logs."""
import csv,json
from pathlib import Path
from registry import ROOT,connect,initialize

def main():
    initialize();db=connect()
    methods={'M0':'e0','M1':'e3','M2':'e6'}
    for row in csv.DictReader((ROOT/'experiments/ch3/eval_manifest.csv').open()):
        benchmark='maniskill' if row['benchmark']=='maniskill3' else row['benchmark']
        db.execute("INSERT OR IGNORE INTO jobs(kind,benchmark,task,method,seed,checkpoint_step,prerequisite) VALUES('eval',?,?,?,?,?,'waiting for scheduled atomic checkpoint')",
            (benchmark,row['task'],methods[row['method']],int(row['seed']),int(row['checkpoint_progress'])))
    for r in db.execute("SELECT * FROM train_jobs").fetchall():
        cfg_path=Path(r['config_path']);run=ROOT/'runs'/r['benchmark']/r['task']/r['method']/f"seed_{r['seed']}"
        frozen=run/'config_resolved.json'
        if not cfg_path.exists():continue
        cfg=json.loads(cfg_path.read_text())
        if frozen.exists() and json.loads(frozen.read_text())!=cfg:
            db.execute("UPDATE jobs SET status='failed',prerequisite='frozen configuration mismatch',error='cannot merge or resume incompatible configuration' WHERE id=?",(r['id'],));continue
        complete=run/'training_complete.json'
        if complete.exists():
            x=json.loads(complete.read_text())
            expected=cfg['budget'] if r['benchmark']=='maniskill' else None
            if (expected and x['optimizer_updates']==expected) or (r['benchmark']=='mimicgen' and x['completed_epochs']==cfg['budget']):
                db.execute("UPDATE jobs SET status='finished',error=NULL WHERE id=?",(r['id'],))
        for meta in (run/'checkpoints').glob('*.json'):
            m=json.loads(meta.read_text());cp=meta.with_suffix('.pt');point=m['checkpoint_step']
            if not cp.exists() or m.get('write_status')!='atomic_complete':continue
            if any(m[k]!=cfg[k] for k in ['benchmark','task','method','seed']):continue
            db.execute("UPDATE jobs SET checkpoint_path=?,config_path=?,prerequisite=NULL WHERE kind='eval' AND benchmark=? AND task=? AND method=? AND seed=? AND checkpoint_step=?",
                (str(cp),str(frozen),r['benchmark'],r['task'],r['method'],r['seed'],point))
            tag='epoch' if r['benchmark']=='mimicgen' else 'update'
            result=run/'eval'/f'{tag}_{point:06d}'/'eval_summary.json'
            if not result.exists():continue
            summary=json.loads(result.read_text());ep=Path(summary['episodes_path'])
            rows=[json.loads(x) for x in ep.read_text().splitlines()]
            resets=[x['reset_id'] for x in rows]
            valid=(len(rows)==cfg['episodes'] and len(set(resets))==len(rows) and set(resets)==set(cfg['reset_ids'])
                and summary['n_episodes']==cfg['episodes'] and summary['success_count']==sum(x['success'] for x in rows)
                and all(x['checkpoint_path']==str(cp) and x['horizon']==cfg['horizon'] and x['seed']==cfg['seed'] for x in rows))
            if valid:db.execute("UPDATE jobs SET status='finished',error=NULL WHERE kind='eval' AND benchmark=? AND task=? AND method=? AND seed=? AND checkpoint_step=?",(r['benchmark'],r['task'],r['method'],r['seed'],point))
    db.commit()
    print([tuple(r) for r in db.execute('SELECT kind,status,count(*) FROM jobs GROUP BY kind,status')])

if __name__=='__main__':main()
