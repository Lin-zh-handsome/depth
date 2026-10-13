"""Create the preregistered protocol and figure/table evidence contracts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
def write(path, value):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

tasks = []
for name in ['stack_three_d1', 'threading_d2', 'coffee_d2', 'StackCube-v1', 'PegInsertionSide-v1']:
    mg = '-' not in name
    tasks.append(dict(benchmark='mimicgen' if mg else 'maniskill', task=name,
        demos=200 if mg else 100, budget=250 if mg else 100000,
        progress_unit='epoch' if mg else 'optimizer_update', interval=5 if mg else 5000,
        savepoints=50 if mg else 20, episodes=50 if mg else 100,
        horizon=400 if mg else (200 if name=='StackCube-v1' else 300),
        seeds=[0,1,2], reset_ids=list(range(100000,100050 if mg else 100100)),
        success_metric='official_task_success' if mg else 'success_at_end',
        control_mode='metadata_pending' if mg else 'pd_joint_pos',
        control_source='official downloaded motionplanning metadata; preserved without reinterpretation',
        cameras=['agentview','robot0_eye_in_hand'] if mg else ['base_camera','hand_camera'],
        image_resolution=[84,84] if mg else [128,128]))
write('configs/protocol.json', dict(protocol='20261013_final_v1', tasks=tasks,
    gpu=dict(physical_index=2, uuid='GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9', allowed_count=1),
    checkpoint_integrity='atomic write + metadata + git revision; no redundant weight hashing per direct user instruction',
    primary_statistics=dict(best='max of all scheduled checkpoints, upward selection bias acknowledged',
        last10='mean of final 10 scheduled points in chronological order', cross_seed='mean and sample std, ddof=1')))

tables = [
('tasks_protocol','数据和评测可复现','resolved config + dataset manifest','Table 3-3'),
('main_comparison','RQ1:七方法闭环比较','BEST/LAST10 per seed; mean ± sample std','Table 3-4'),
('ablations','RQ2/RQ3:单模块与交互','SR_E6-SR_E3-SR_E4+SR_E0','Table 3-5'),
('encoders','RQ2:容量与几何先验','SR, trainable params, isolated planning ms','Table 3-6'),
('data_efficiency','示范量与样本效率','100/200/1000 nested demos; BEST/LAST10','section 3.6.8'),
('attention','RQ2:真实轴向注意力','same/cross instance mass; feature cosine gap','section 3.6.9'),
('tokens','RQ3:几何Token关联','target overlap; pixel center error; surface depth error m','Table 3-7'),
('motion','RQ4:空间误差','task-defined position m and rotation rad; paired success','Table 3-8'),
('efficiency','RQ4:部署代价','batch1 synchronized isolated ms; GPU bytes; params','Table 3-9')]
figs = [
('architecture','整体架构','actual module/shape graph','Fig 3-1'),
('gsa_diagram','GSA计算','official operator + documented adaptation','Fig 3-2/3'),
('token_diagram','Token聚合','weighted uv/d/rho equations','Fig 3-4'),
('main_sr','RQ1','per-seed BEST/LAST10','Fig 3-8/9'),
('ablation_sr','RQ2/RQ3','per-seed SR and interaction','section 3.6.6'),
('learning','真实训练稳定性','scheduled checkpoint SR vs epoch/update','Fig 3-9'),
('encoder_data','容量和示范量','SR/params and nested demo SR','section 3.6.7/8'),
('attention_visual','真实几何先验与轴向注意力','actual query/prior/axis weights','Fig 3-10'),
('feature_visual','GSA前后特征','normalized features + instance cosine statistics','Fig 3-11'),
('token_visual','空间权重和几何','actual masks, uv/d/rho in meters','Fig 3-12'),
('motion_visual','动作误差','paired rollout GT only offline','Fig 3-13'),
('paired_cases','同reset成功失败','preregistered selection: first reset disagreement by ID','Fig 3-13'),
('depth_intervention','深度依赖','same checkpoint paired intervention, separate from main scores','section 3.6.12'),
('cost_tradeoff','速度/成功率代价','isolated latency vs measured SR','section 3.6.12')]
records = []
for kind, rows in [('Table',tables),('Fig',figs)]:
    for i,(name,question,formula,draft) in enumerate(rows,1):
        records.append(dict(id=f'{kind} 3-{i}', name=name, question=question,
            sampling='three independent train seeds; shared reset IDs; fixed scheduled checkpoints',
            metric=formula, units='SR fraction, position m, angle rad, time ms, memory bytes as applicable',
            required_fields=['benchmark','task','method','seed','checkpoint_step','checkpoint_path',
                'code_revision','dataset_manifest','camera','reset_id','success_at_end','success_once'],
            gt_source='simulator instance/state for offline analysis only; never policy input',
            script=f'analysis/export_{name}.py', output=f'thesis/{kind.lower()}s/{name}',
            formats=['csv','markdown','latex'] if kind=='Table' else ['png','svg','pdf'],
            source_manifest=f'thesis/source_manifests/{name}.json',
            draft_number=draft, reproducibility_status='pending',
            unavailable_rule='NA(reason) when required result or GT is absent'))
write('thesis/figure_table_contract.yaml',dict(schema_version=1, records=records,
    numbering='canonical final protocol; draft crosswalk recorded separately',
    token_gt_association='highest weighted overlap with target instance; overlap>=0.5; failures counted',
    mechanism='attention -> retained target information -> token geometry -> spatial error -> success; each arrow measured separately'))
print('protocol and 23 evidence contracts written')
