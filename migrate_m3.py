"""Append only M3 events; preserve all previous IDs and actual queue states."""
import csv,json,sqlite3,copy
from pathlib import Path
from jobs.registry import ROOT,connect,initialize

def append_csv(path,method_model):
    with path.open(newline='',encoding='utf-8-sig') as f:reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
    key='run_id' if path.name=='run_manifest.csv' else 'eval_id';known={r[key] for r in rows};new=[]
    for row in rows:
        if row['method']!='M2':continue
        item=dict(row)
        item['method']='M3';item['run_id']=row['run_id'].replace('_m2_','_m3_')
        if 'eval_id' in item:item['eval_id']=row['eval_id'].replace('_m2_','_m3_')
        if item[key] in known:continue
        for field in ['dataset_hash','config_hash','git_sha','best_inference_path','latest_resume_path','log_path','checkpoint_sha','result_path','eval_snapshot_path']: 
            if field in item:item[field]=''
        if 'model' in item:item['model']='cnn_dp_geometry_associated_tokenlearner'
        if 'snapshot_artifact_state' in item:item['snapshot_artifact_state']='NOT_CREATED'
        item['status']='PENDING';item['notes']='M3: exact M2 geometry TokenLearner class/config, GSA disabled'
        new.append(item);known.add(item[key])
    with path.open('a',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writerows(new)
    return len(new)

def main():
    db=connect();old=[dict(r) for r in db.execute("SELECT * FROM jobs WHERE kind IN ('train','eval') AND method!='m3'")]
    archive=ROOT/'experiments/ch3/before_m3';archive.mkdir(exist_ok=True)
    backup=sqlite3.connect(archive/'queue_before_m3.db');db.backup(backup);backup.close()
    for filename in ['run_manifest.csv','eval_manifest.csv']:
        p=ROOT/'experiments/ch3'/filename
        if not (archive/filename).exists():(archive/filename).write_bytes(p.read_bytes())
    ntrain=append_csv(ROOT/'experiments/ch3/run_manifest.csv',True);neval=append_csv(ROOT/'experiments/ch3/eval_manifest.csv',False)
    initialize();methods={'M0':'e0','M1':'e3','M2':'e6','M3':'m3'}
    for row in csv.DictReader((ROOT/'experiments/ch3/eval_manifest.csv').open()):
        if row['method']!='M3':continue
        bm='maniskill' if row['benchmark']=='maniskill3' else row['benchmark']
        db.execute("INSERT OR IGNORE INTO jobs(kind,benchmark,task,method,seed,checkpoint_step,prerequisite) VALUES('eval',?,?,'m3',?,?,'waiting for scheduled atomic checkpoint')",(bm,row['task'],int(row['seed']),int(row['checkpoint_progress'])))
    db.commit()
    # Identity preservation, not a model hash or repeated evaluation.
    for row in old:
        now=dict(db.execute('SELECT * FROM jobs WHERE id=?',(row['id'],)).fetchone())
        for field in ['id','kind','benchmark','task','method','seed','checkpoint_step']:
            if now[field]!=row[field]:raise RuntimeError('existing job identity changed')
    counts=[tuple(x) for x in db.execute('SELECT kind,method,count(*) FROM jobs GROUP BY kind,method')]
    assert db.execute('SELECT count(*) FROM train_jobs').fetchone()[0]==60
    assert db.execute('SELECT count(*) FROM eval_jobs').fetchone()[0]==300
    report=dict(added_manifest_training_rows=ntrain,added_manifest_evaluation_rows=neval,old_events_preserved=len(old),counts=counts,old_state_policy='migration issues INSERT OR IGNORE only; live workers may advance states normally',missing_new_attachment='four-model instructions supplied in user message; no new ZIP found')
    (ROOT/'docs/m3_migration_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=='__main__':main()
