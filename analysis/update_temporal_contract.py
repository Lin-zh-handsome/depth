"""Append the temporal figure contract without altering training/eval budgets."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'thesis/figure_table_contract.yaml'
contract=json.loads(p.read_text())
entry=dict(id='Fig 3-15',name='temporal_spatial_attention_evolution',
    question='机器人闭环执行过程中的空间关注如何随时间变化，以及成功失败轨迹之间有何差异',
    sampling='independent specified-checkpoint rollout; record each actual replanning event; paired E0/E1/E6 same reset',
    metric='actual GSA axial attention query weights; K token softmax weights and uv/d/rho; baseline denoiser input-gradient saliency separately labeled',
    units='environment steps, seconds from actual control frequency, depth m, normalized image coordinates',
    required_fields=['episode_id','reset_id','seed','checkpoint_path','checkpoint_step','code_revision',
        'plan_id','env_step','time_seconds','RGB','Depth','GSA_attention_width','GSA_attention_height',
        'query_original_xy','query_grid_yx','token_spatial_weights','token_uv_d_rho','robot_state',
        'planned_actions','executed_actions','success_at_end','success_once','stage.source_kind','stage.source'],
    gt_source='environment event or explicit offline annotation only; unannotated frames use neutral timepoints',
    script='analysis/temporal_attention.py; analysis/dispatch_temporal.py',
    output='analysis/temporal_paired/{task}/seed_{seed}/update_{step}/reset_{reset}/{method}',
    formats=['mp4','png','json','jsonl','npz'],
    source_manifest='temporal_manifest.json + selection_manifest.json + comparison.json',
    reproducibility_status='implementation_ready; actual rollout artifacts pending specified trained checkpoint',
    unavailable_rule='no explicit attention in E0/E1: saliency only; missing success/failure outcome or stages explicitly unavailable',
    stage_selection='first actual occurrence of annotated stages; fill 4–6 neutral timepoints without inventing stage labels',
    automatic_trigger='final scheduled E0/E1/E6 evaluations for same task/seed/step completed; independent analysis queue',
    scope='analysis only; no change to training budget, scheduled evaluation, episode counts, or formal success rates',
    figure_layout='4–6 actual moments with RGB, GSA query attention and all K TokenLearner maps',
    storage_policy='capture only in dedicated analysis; formal evaluate.py never stores attention tensors')
contract['records']=[r for r in contract['records'] if r['id']!='Fig 3-15']+[entry]
p.write_text(json.dumps(contract,ensure_ascii=False,indent=2))
print('Fig 3-15 contract registered')
