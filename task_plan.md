# 第三章 GSC-DP：文件化实验总计划

> 2026-10-14 初始化。此计划是执行合同，不表示服务器上的任何任务已启动。由 Codex 使用其实际已安装的 `planning-with-files` 技能读取和持续维护。

## 固定范围与验收

- 仅第三章，唯一正式网络：M0 原始 RGB CNN-DP，M1 原始 CNN-DP+GSA，M2 在 M1 基础上+Geometry-associated TokenLearner。
- 仅五项任务：MimicGen Core `stack_three_d1`、`threading_d2`、`coffee_d2`；ManiSkill3 `StackCube-v1`、`PegInsertionSide-v1`。
- 3 个独立种子 `[0, 1, 2]`，共 45 个唯一训练 run；按已确定协议共 1,710 个 checkpoint eval、103,500 个仿真 episodes（全部完成且没有可复用结果时）。
- 数据预处理、算法定义、官方基线不变、模型 checkpoint 独立评测、3-seed 成功率统计、真实注意力和 Token 权重可视化，详见 `EXPERIMENT_SPEC.md`。
- 完成的定义：所有可用 run 的逐 seed BestSR / Last10SR、每次 checkpoint rollout 原始 episode、真实表图和可追溯脚本；不以队列创建代替完成。
- 不做：计算效率（FLOPs/参数量/推理时延/显存）对比；附加注意力、编码器、RGB-D baseline、无 GSA Token、数据效率、深度扰动或第四章等训练组；不重训 ACT/DP3/EquiDiff。

## 全部任务一次性入队（以下为工作项而非需依次完成的阶段）

- [ ] **A / 现存资产接管**：读取旧规划文件、服务器仓库/data/checkpoints/eval/logs，建立每项运行的配置、数据 hash 与 checkpoint SHA；在 `experiments/ch3/run_manifest.csv` 和 `eval_manifest.csv` 中标出 DONE/RUNNING/MISSING/INVALID，复用合法结果；不得重启合法的在训进程。
- [ ] **B / 模型与数据就绪**：忠实保留 M0 CNN-DP；对齐 GSA 与 TokenLearner 的实现、RGB-D、多相机时序、Depth 单位、动作与观测；做最少必要的真实数值/梯度/独立 checkpoint 加载检查，随后直接正式运行。
- [ ] **C / 训练调度**：一次性入队全部 45 个任务，调度优先 `M2 > M1 > M0`、任务顺序 `threading_d2 > PegInsertionSide-v1 > stack_three_d1 > coffee_d2 > StackCube-v1`；资源足够并行，不设置先后完成门槛；可恢复任务日志。
- [ ] **D / 异步评测**：每个有效 checkpoint 写盘后即可排队独立闭环 rollout，不等待整模型训练完；固定同任务评测 reset manifest；原子写盘与去重。
- [ ] **E / 成绩统计**：计算每 seed 各 checkpoint SR、BestSR、按时间最后十个 checkpoint 的平均 Last10SR、3-seed mean±sample std、M1-M0 与 M2-M1 递进增益。
- [ ] **F / 可视化**：M1/M2 的真实 GSA attention、TokenLearner 8 个空间权重、逐时刻执行图/MP4、同初态对照成功/失败关键帧；只用已训练模型，不追加训练组。
- [ ] **G / 论文交付**：`thesis/chapter3/` 下自动导出实验协议、五任务成功率表、曲线、模块递进表、真实注意力/Token 可视化、视频、中文说明；文献外部数字明确单列 Published。
- [ ] **H / 持久化与恢复**：维护本文件、`findings.md`、`progress.md`、manifest、异常及准确恢复命令；说明服务器进程 PID、GPU 与日志；队列状态不能凭空更新。

## 优先级说明

所有 A–H 工作都必须执行，优先级仅影响有限资源下抢先获取本方法 M2 及 M1/M0 受控成功率的顺序，不表示延后其他任务立项；模型代码准备与下载可并行推进，训练/评测/绘图可以同时运行。

## 训练/评测协议

| Benchmark | Task | Demos | Budget | Save/eval every | Episodes | Max horizon |
|---|---|---:|---|---|---:|---:|
| MimicGen Core | stack_three_d1 | 200 | 250 epochs | 5 epochs | 50 | 400 |
| MimicGen Core | threading_d2 | 200 | 250 epochs | 5 epochs | 50 | 400 |
| MimicGen Core | coffee_d2 | 200 | 250 epochs | 5 epochs | 50 | 400 |
| ManiSkill 3 | StackCube-v1 | 100 | 100,000 updates | 5,000 updates | 100 | 200 |
| ManiSkill 3 | PegInsertionSide-v1 | 100 | 100,000 updates | 5,000 updates | 100 | 300 |

**禁止**因 250 epochs 历时较久而自行减少训练量、评测频率、种子或单 checkpoint episodes。可优化数据缓存、实际运行并行、使用已有结果。

## 固定论文表图

- 表：任务协议；M0/M1/M2 的五任务 BestSR；五任务 Last10SR；可选文献参考表（标明来源与协议差异）。
- 图：三模型关键结构图；五任务 checkpoint SR 曲线；真实 GSA Query 级空间权重；M2 八个 TokenLearner 分配图 `(u,v,d,rho)`；机器人执行阶段的图/视频和同 reset 成功/失败案例。
- 没有真实数据不填数字。禁止效率对比表。

## 项目状态

2026-10-14 当前状态：**本地仅创建了执行文件和初始 manifest；服务器状态尚未接管，所有 run/eval 都标记 `PENDING_UNVERIFIED`。** Codex 首次工作必须先扫描并纠正这批状态，而不是假定全部尚未训练。

## 实际接管状态
A in_progress：已核实服务器、数据与旧暂停状态。B in_progress：MimicGen数据可复用；ManiSkill需官方动作转换。C/D in_progress：部署45-run/1710-eval专用队列；正式启动待记录真实PID。E/F/G pending真实结果。H in_progress。
