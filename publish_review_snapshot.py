"""Publish current code and actual run artifacts, leaving datasets and weights on server."""
from pathlib import Path
import datetime
import json
import shutil
import sqlite3
import subprocess

root = Path('/home/linzhenghong/project/gsc_dp_chapter3/campaign_v1')
plan = root.parent / '.planning/protocol_v1'
snapshot = root / 'artifacts/snapshot_20261015'
snapshot.mkdir(parents=True, exist_ok=True)
stamp = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='seconds')
allowed = {'.log', '.txt', '.json', '.jsonl', '.csv', '.png', '.mp4', '.pdf', '.yaml', '.yml'}
copied = 0
total = 0
for dirname in ['logs', 'runs']:
    for src in (root / dirname).rglob('*'):
        if not src.is_file() or src.is_symlink() or '__pycache__' in src.parts or src.suffix.lower() not in allowed or src.name.endswith('_trajectory.json'):
            continue
        dst = snapshot / src.relative_to(root)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        copied += 1
        total += dst.stat().st_size

db = sqlite3.connect(root / 'jobs/ch3_final_queue.db', timeout=30)
with sqlite3.connect(snapshot / 'ch3_final_queue_snapshot.sqlite3') as backup:
    db.backup(backup)
db.close()
db = sqlite3.connect(snapshot / 'ch3_final_queue_snapshot.sqlite3')
db.row_factory = sqlite3.Row
counts = [dict(row) for row in db.execute('SELECT kind,status,count(*) n FROM jobs GROUP BY kind,status')]
jobs = [dict(row) for row in db.execute('SELECT * FROM jobs ORDER BY id')]
(snapshot / 'queue_jobs.json').write_text(json.dumps(jobs, ensure_ascii=False, indent=2), encoding='utf-8')
db.close()
catalog = []
for directory in ['runs', 'checkpoint_store']:
    p = root / directory
    if p.exists():
        for src in p.rglob('*'):
            if src.is_file() and src.suffix.lower() in {'.pt', '.ckpt', '.pth', '.safetensors'}:
                catalog.append({'server_path': str(src), 'bytes': src.stat().st_size, 'included': False})
(snapshot / 'checkpoint_catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding='utf-8')
info = {'captured_at_asia_shanghai': stamp, 'protocol': 'four_models_60_train_300_eval',
        'queue_counts': counts, 'copied_files': copied, 'copied_bytes': total,
        'source_queue': 'jobs/ch3_final_queue.db', 'excluded': ['datasets', 'all model weights and checkpoints'],
        'note': 'Running logs and unfinished episode files are partial snapshots. Only complete scheduled evaluation summaries enter official statistics. Historical directories retain their original protocol labels.'}
(snapshot / 'snapshot_metadata.json').write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding='utf-8')
(root / 'docs/current_status.json').write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding='utf-8')

guide = '''# 四模型第三章代码审查入口

当前协议：M0=e0、M1=e3、M2=e6、M3=m3，五任务、三个种子，共60次训练、300次正式评测。
M3复用M2的同一Geometry-associated TokenLearner（几何关联空间标记学习器）及几何处理，唯一模块差异为取消GSA（几何空间注意力）。

| 审查内容 | 文件 |
| --- | --- |
| 四模型开关、共享编码器和TokenLearner | `gsc_dp/encoder.py` |
| M3结构一致性证据 | `docs/m3_structure_consistency.json` |
| 旧事件保留及M3追加迁移 | `migrate_m3.py`、`docs/m3_migration_report.json` |
| 正式训练与独立闭环评测 | `train.py`、`evaluate.py` |
| 60训练/300评测及固定reset（重置）列表 | `experiments/ch3/run_manifest.csv`、`experiments/ch3/eval_manifest.csv`、`experiments/ch3/eval_resets/` |
| 可恢复队列、同任务并行、任务间串行 | `jobs/registry.py`、`jobs/scheduler.py`、`jobs/task_dispatch_state.json` |
| 约70% GPU负载控制 | `jobs/gpu_load_governor.py`、`jobs/gpu_load_target.json` |
| best/latest（最佳/恢复）与临时checkpoint（检查点）管理 | `gsc_dp/checkpoints.py`、`jobs/maintain_checkpoints.py` |
| Best-of-5（五次取最佳）、三种子样本标准差、四模型主表与消融 | `jobs/export_ch3.py`、`thesis/chapter3/tables/` |
| 真实注意力、Token空间权重与基线显著性 | `analysis/temporal_attention.py`、`analysis/dispatch_temporal.py` |
| 论文图表自动导出要求 | `thesis/figure_table_contract.yaml` |
| 本次真实日志、逐回合成功记录和队列快照 | `artifacts/snapshot_20261015/` |

MimicGen：250 epochs（完整数据轮次），只在50/100/150/200/250轮各评测50回合。
ManiSkill：100000 optimizer updates（优化器更新），只在20k/40k/60k/80k/100k各评测100回合。
每个种子五次取最佳，并列选最早；三个种子完整后计算均值和样本标准差。
当前实验仍在执行，未完成项为空，不代表零成功率。早期1710次安排、历史控制模式和旧快照不进入最新正式统计。
不开展计算效率、编码器、数据效率及第四章实验。原有45训练/225评测身份保留，M3仅追加15训练/75评测。
M0不输入Depth（深度），因此M1−M0和M3−M0不单独归因于某一模块；M2−M1和M2−M3分别用于隔离TokenLearner和GSA的条件增益。

模型权重和数据集本体均留在服务器；仓库保留来源、配置与路径元数据。官方依赖以Git submodule（子模块）保留。
'''
(root / 'docs/CODE_REVIEW_GUIDE.md').write_text(guide, encoding='utf-8')
readme = (root / 'README.md').read_text(encoding='utf-8')
readme = readme.replace('五任务、三训练种子的 GSC-DP', '四模型、五任务、三训练种子的 GSC-DP')
readme = readme.replace('训练和评测依据 `docs/inputs/GSC_DP_第三章最终实验协议.md`', '当前唯一执行口径为60次训练、300次正式评测，详见 [代码审查入口](docs/CODE_REVIEW_GUIDE.md) 和 `docs/four_model_protocol_update_20261015.md`；历史输入文档中冲突规则已被最新四模型要求覆盖')
readme = readme.replace('时序注意力任务及数据效率等后续实验的完成情况以规划文件和真实产物为准。', '时序注意力任务的完成情况以规划文件和真实产物为准。不开展计算效率、编码器、数据效率及第四章实验。')
readme += '\n\n本次代码审查快照：`artifacts/snapshot_20261015/`，包含真实训练日志、逐回合成功记录、60训练/300评测队列快照和检查点路径清单。旧快照保留其历史日期。\n'
(root / 'README.md').write_text(readme, encoding='utf-8')
ignore = (root / '.gitignore').read_text(encoding='utf-8')
for line in ['/checkpoint_store/', '*.safetensors', '*.onnx', '.env', '.env.*', '*.pem', '*.key']:
    if line not in ignore.splitlines():
        ignore += '\n' + line
(root / '.gitignore').write_text(ignore.rstrip() + '\n', encoding='utf-8')
for name in ['task_plan.md', 'findings.md', 'progress.md']:
    note = f'\n\n## GitHub代码审查发布 {stamp}\n用户明确授权推送除checkpoint与数据集外的工程内容。同步四模型60训练/300评测代码、配置、当前真实日志/结果快照与代码审查入口。快照来自ch3_final_queue.db一致性备份，原始轨迹仅留服务器；所有模型权重和数据集本体留在服务器。训练评测持续运行。发布准备完成，推送结果以Git命令回执为准。\n'
    with (plan / name).open('a', encoding='utf-8') as f:
        f.write(note)
    shutil.copyfile(plan / name, root / name)
print(json.dumps(info, ensure_ascii=False))
