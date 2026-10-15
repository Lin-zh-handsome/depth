# 四模型第三章代码审查入口

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
