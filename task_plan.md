# 研究计划｜仅硕士论文第三章GSC-DP

本文件为Codex可持续更新的planning-with-files合同。2026-10-14更新：**取代旧1710次eval/Last10SR规则**。预生成状态不表示服务器已启动作业。

## 固定目标

- 仅三网络M0、M1、M2；两个Benchmark五任务；seed 0/1/2。
- 45个独立训练run、每run5次周期性rollout，共225个eval点、15750个episodes（无复用的满额理论值）。
- MimicGen每任务200 demos，250 dataset epochs；ManiSkill每任务100 demos，100000 optimizer updates。
- 主结果为`Best-of-5`：各seed5个checkpoint取最大SR，再跨3种子算mean±sample_std。
- 只做SR对比、递进式模块增益、5点评测曲线、GSA/TokenLearner真实可视化及执行案例；不做效率、编码器、注意力变体、数据效率、第四章。
- checkpoint best推理权重一份/run + latest训练状态一份/活跃run + 有界短生命周期eval临时权重；不堆积历史模型。

## 一次性创建全部任务，不设置人工审批阶段

- [ ] A 接管当前H200仓库、正在运行的45run候选与旧eval队列，收集数据/配置/版本/日志hash，标注历史可复用结果。禁止把预生成状态当实际情况。
- [ ] B 使训练入口与固定预算、指定5个评测时点一致；GSA及关联TokenLearner实现完全吻合CNN-DP骨干；Depth数据/动作控制模式统一。
- [ ] C 取消旧周期性快照逻辑，实现225条新eval manifest、独立加载磁盘快照的rollout、可恢复队列、最佳权重安全更新与快照回收。
- [ ] D H200资源可用时优先M2、并行M1/M0；全部45run一次性入队；不重复合法的已完成训练。
- [ ] E 完成225个真实评测点或复用合规同位置旧数据，保留每个episode完整记录；汇总Best-of-5的三种子mean±std，不生成Last10。
- [ ] F 导出五任务表、5点SR曲线、真实GSA/TokenLearner热图、操作关键帧与MP4，记录其checkpoint SHA。
- [ ] G 审计并安全回收旧已失效checkpoint，维护安全清理清单、磁盘占用、PID/GPU与可恢复命令。
- [ ] H 将真实结果同步写入`thesis/chapter3/`，填补图表和中文分析。未完成项目保持TODO，不能虚构。

执行优先级仅用于队列排序，不代表分阶段开工。所有报告都需要区分PENDING与DONE。
