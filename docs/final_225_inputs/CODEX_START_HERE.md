# Codex 立即执行｜第三章 CNN-DP + GSA + TokenLearner

**本包覆盖旧版“1710评测点/Last10SR/每5epoch评一次”的安排，所有旧包有冲突的规则以本包为准。**

1. 在当前 H200 实验仓库中读取已安装 `planning-with-files` 的真实 `SKILL.md`，恢复并更新 `task_plan.md`、`findings.md`、`progress.md`。若技能不可用，继续使用这三份文件式记录，不要宣称已加载不可用的技能。
2. 完整阅读 `EXPERIMENT_SPEC.md` 和 `CHECKPOINT_STORAGE_POLICY.md`。首先核对仓库、数据、进程、历史结果、现有权重及日志的实际状态；不要将随包提供的 PENDING_UNVERIFIED 当作当前服务器真实状态，也不要无故终止已有合规训练。
3. 在任务管理系统中以 `experiments/ch3/run_manifest.csv` 中45条 `(task,model,seed)` 为唯一正式训练队列，以 `experiments/ch3/eval_manifest.csv` 中225条为**唯一正式评测计划**，禁止生成任何额外周期性评测任务。
4. 训练总预算：MimicGen 200 demos 对应250完整dataset epochs；ManiSkill StackCube/PegInsertionSide 每个100000 optimizer updates。同任务所有方法与seed训练预算相同。优先M2、有资源就并行启动M1/M0，所有45次运行一次性纳入队列，不设置等待用户确认的阶段门槛。
5. 每个run只评测5个指定时间点；每时间点MimicGen 50 episodes，ManiSkill 100 episodes。每种子5次SR取max，最终对3个seed取mean±sample std (ddof=1)。**不计算Last10；不额外做验证集选checkpoint。** 结果须清楚标注为训练期间 Best-of-5 rollout SR。
6. 评测通过独立进程**加载真实磁盘推理快照**，按标准闭环环境reset执行。保存每条episode success及评测manifest；非最佳快照安全删除。只有BEST推理权重和运行中的LATEST完整训练状态按保存策略保留。
7. 严格只做M0(原CNN-DP)、M1(CNN-DP+GSA)、M2(CNN-DP+GSA+几何关联TokenLearner)；五任务、三个训练种子。导出成功率表、5点SR曲线、递进模块增益、真实GSA空间注意力、TokenLearner空间权重和操作视频。**不进行任何计算效率、额外网络/编码器/注意力/数据效率或第四章实验。**
8. 对已有run采取保守迁移：只有5个新指定位置的、配置匹配且可验证的旧评测结果才记为新协议 DONE；旧协议其它时间点结果存历史归档，不得纳入本次 Best-of-5。旧权重须先完成占用、引用、恢复状态审计再清理，不删除未完成评测仍依赖的快照。
9. 不是只改文档：必须使实际训练回调、评测事件调度、manifest、模型保存/清理、汇总脚本与此新协议完全一致，然后正式实施。汇报实跑PID/GPU、已复用结果、缺少项、磁盘占用和恢复命令。不可把计划或模拟数字冒充训练成功率。
