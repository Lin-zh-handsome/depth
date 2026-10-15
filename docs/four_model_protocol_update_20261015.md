

## 四模型正式协议生效 2026-10-15T18:37:57.370028+08:00
用户新增M3=CNN-DP+Geometry-associated TokenLearner，不启用GSA，直接复用M2相同DepthTokenLearner类、8个token、同权重(u,v,d,rho)与投影残差融合。新包附件未发现，明确按本轮用户指令执行。原45训练225正式评测的ID、数据库与实际状态保留，只追加M3的15训练75评测；总计60训练300评测21000回合。沿用既定训练预算、每run五次正式评测、Best-of-5与低存储规则。不重新训练旧合规模型。每任务变为12训练60正式评测，全部完成才换任务；仍先Threading，只用GPU2，平均利用率目标70%，GPU5不操作。M2已完成，原M0/M1工作进程保持运行，新增M3按空闲队列立即正式调度。四模型主表、模块消融及M1-M0/M3-M0/M2-M1/M2-M3/M2-M0增量、成功率曲线与真实可视化已更新。无GSA的M3只展示真实TokenLearner权重，不伪称GSA注意力。证据docs/m3_migration_report.json、docs/m3_structure_consistency.json。
