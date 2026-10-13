"""Resolve only runnable formal configs from actual fixed-subset manifests."""
import json
from pathlib import Path
import zarr
from jobs.registry import connect
ROOT=Path(__file__).resolve().parent
protocol=json.loads((ROOT/'configs/protocol.json').read_text())
db=connect()
for task in protocol['tasks']:
    if task['benchmark']!='maniskill': continue
    manifest=ROOT/'data/manifests'/f"{task['task']}_100.json"
    if not manifest.exists(): continue
    m=json.loads(manifest.read_text());r=zarr.open(m['processed_path'],'r')
    shape={'obs':{},'action':{'shape':[r['data/action'].shape[-1]]}}
    for key in r['data'].array_keys():
        if key=='action':continue
        a=r['data'][key]
        image=key.endswith(('_image','_depth'))
        shape['obs'][key]=dict(shape=([a.shape[-1],*a.shape[1:3]] if image else list(a.shape[1:])),
            type='rgb' if key.endswith('_image') else 'depth' if key.endswith('_depth') else 'low_dim')
    for row in db.execute("SELECT * FROM train_jobs WHERE task=? AND method LIKE 'e%'",(task['task'],)).fetchall():
        cfg=dict(task,method=row['method'],seed=row['seed'],shape_meta=shape,crop_shape=[112,112],
            zarr_path=m['processed_path'],dataset_manifest=str(manifest),batch_size=64,
            optimizer='AdamW',lr=1e-4,ddpm_steps=100,observation_horizon=2,prediction_horizon=16,
            action_horizon=8,control_mode=m['control_mode'],weight_initialization='random; no pretrained weights',
            budget_source='StackCube official visual DP; Peg visual CNN-DP budget fixed by this study')
        path=Path(row['config_path']);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(cfg,indent=2))
        db.execute('UPDATE jobs SET prerequisite=NULL WHERE id=?',(row['id'],))
db.commit();print('ready formal configs',db.execute('SELECT count(*) FROM train_jobs WHERE prerequisite IS NULL').fetchone()[0]);db.close()
