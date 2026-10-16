"""Export the already collected successful rollout; never train or add formal evals."""
from pathlib import Path
import json,shutil,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/temporal/threading_d2/e6/seed_2/epoch_000200/reset_100042'
rows=[json.loads(x) for x in (OUT/'replans.jsonl').read_text().splitlines()]
episode=json.loads((OUT/'episode.json').read_text())
if not (episode['success_once'] and episode['success_at_end']):
    raise RuntimeError('This artifact must not be presented as terminal-success unless actually confirmed')
formal=ROOT/'runs/mimicgen/threading_d2/e6/seed_2/eval/epoch_000200/reset_100042_trajectory.json'
old=json.loads(formal.read_text())
actual=np.asarray([a['action'] for r in rows for a in r['executed_actions']])
expected=np.asarray([x['action'] for x in old])
sums=[]
for row in rows:
    with np.load(row['raw_path']) as data:
        for camera in row['cameras']:
            g=data[camera+'_gsa_query'];w=data[camera+'_token_weights']
            sums.append(dict(plan_id=row['plan_id'],camera=camera,gsa_shape=list(g.shape),gsa_sum=float(g.sum()),token_shape=list(w.shape),token_sum_max_error=float(np.max(np.abs(w.sum(axis=(-2,-1))-1)))))
success_steps=[a['step'] for r in rows for a in r['executed_actions'] if a['success']]
info=dict(task='threading_d2',method='M2',seed=2,checkpoint_epoch=200,reset_id=100042,
          collection_mode='independent_analysis_rollout',formal_evaluation_count_unchanged=True,
          first_official_success_step=min(success_steps),success_at_end=episode['success_at_end'],success_once=episode['success_once'],
          formal_action_source=str(formal),formal_vs_analysis_actions_max_abs=float(np.max(np.abs(actual-expected))),
          attention_kind='actual captured width-to-height GSA query propagation, averaged over heads; excludes residual and LEPE; not a full GSA attention matrix',
          token_kind='all 8 actual softmax spatial weights; not feature response or object segmentation',
          attention_query_original_pixel_xy=[44,44],attention_sampling='one observation and heatmap per actual 8-step policy replanning; final map at step392 controls steps393..400; official success first occurs at step395',
          numerical_checks=sums)
(OUT/'visualization_provenance.json').write_text(json.dumps(info,indent=2))
hand=OUT/'camera_robot0_eye_in_hand';hand.mkdir(exist_ok=True)
for name in ['episode.json','replans.jsonl']:
    shutil.copyfile(OUT/name,hand/name)
print(json.dumps({k:v for k,v in info.items() if k!='numerical_checks'}),flush=True)
