# 给 Codex 的直接执行指令

我现在只做硕士论文第三章。请**先使用已安装的 `planning-with-files` 技能**，查找并完整读取该技能的 `SKILL.md`，然后以它的文件更新/恢复规范继续执行。不得仅口头声称使用了技能。

以下全部文件为本次统一任务的输入：
- `EXPERIMENT_SPEC.md`：唯一实验/算法/数据/评测/图表执行标准；
- `task_plan.md`：一次性全部入队的完整计划；
- `findings.md`：已确定事实和 H200 上待核查事项；
- `progress.md`：初始进度及日志更新规范；
- `experiments/ch3/run_manifest.csv`：全部 45 个训练 run；
- `experiments/ch3/eval_manifest.csv`：1,710 次 checkpoint rollout 作业。

操作顺序：
1. 先读实际 skill 指令；按其要求接管本项目的 `task_plan.md/findings.md/progress.md`。如果 Codex 环境也没有该技能，明确报告缺失并按这三个文件执行，不得假称 skill 已加载。
2. 扫描 H200 上原仓库、真实数据、训练进程、已经保存的 ckpt 和已有评测。合并本包 manifest 时以**实际远端证据优先**，按配置 hash、数据 hash、seed、ckpt SHA 和 eval reset 复用合法数据；千万不要用初始化的 `PENDING_UNVERIFIED` 覆盖真实 DONE 记录。
3. 按 `EXPERIMENT_SPEC.md` 只实施 M0/M1/M2×五任务×三种子；所有合法待处理作业一次性入队。优先 M2，其他有空闲资源即可并行；ckpt 生成后独立、异步、真正执行 closed-loop rollout。
4. 自动增量生成仅成功率、递进消融、真实注意力与 TokenLearner 权重、典型闭环执行关键帧和轨迹等论文产出；不加效率/编码器/数据效率/无关消融实验。
5. 关键动作后持续回写三个 planning 文件和作业 manifest，最后报告实际完成/运行中/未完成数量、已有合法复用、真实 PID/log/ckpt/rollout 文件与准确恢复命令。未知就写 UNKNOWN，未完成就写 NOT DONE。

不要只输出一份计划或停留在代码审查，也不要先做与既定课题无关的大量小样本试验。只允许必要的数据/模型/checkpoint 一致性确认，然后直接实施正式训练与评测。当前用户只研究第三章，不涉及第四章。
