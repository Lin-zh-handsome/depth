"""Record additive audit metadata without changing scientific configs or data."""
import json,sqlite3,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/audit_55951414'
db=sqlite3.connect(ROOT/'jobs/ch3_final_queue.db');db.row_factory=sqlite3.Row
backup=[]
for r in db.execute("SELECT * FROM jobs WHERE kind='eval' AND status='finished'"):
    run=ROOT/'runs'/r['benchmark']/r['task']/r['method']/f"seed_{r['seed']}";tag='epoch' if r['benchmark']=='mimicgen' else 'update'
    for p in [run/f"eval/{tag}_{r['checkpoint_step']:06d}/eval_summary.json",run/'best/best.json']:
        if p.exists() and not any(x['path']==str(p) for x in backup):backup.append(dict(path=str(p),original=json.loads(p.read_text())))
p=OUT/'result_metadata_before_annotation.json'
if not p.exists():p.write_text(json.dumps(backup,indent=2))
peg=json.loads((OUT/'peg_100_source_replay_cache.json').read_text());manifest=ROOT/'data/manifests/PegInsertionSide-v1_100.json';value=json.loads(manifest.read_text())
original=OUT/'peg_manifest_before_annotation.json'
if not original.exists():original.write_text(json.dumps(value,indent=2))
value.update(source_success_count=100,source_failure_count=0,replay_success_count=90,replay_failure_count=10,training_retains_failed_controller_replays=True,failed_controller_replay_source_ids=peg['failed_replay_source_ids'],training_trajectory_evidence=str(OUT/'peg_100_source_replay_cache.json'))
tmp=manifest.with_suffix('.audit_tmp');tmp.write_text(json.dumps(value,indent=2));tmp.replace(manifest)
print('BACKED_UP_RESULT_METADATA',len(backup),'PEG_ANNOTATED_NO_DATA_CHANGE')
