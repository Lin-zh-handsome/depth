# Codex 执行指令｜硕士论文第三章 GSC-DP 五任务实验（最终精简版）

> **把下面的全部内容作为一个完整任务执行，而不是只回答计划。使用 planning-with-files 技能管理可恢复的执行记录，直接在当前 H200 服务器项目上实施代码、训练、异步评测、统计、可视化与第三章图表导出。**
>
> 本指令高于仓库内以往所有第三章过时实验规划，特别是取消之前的“计算效率分析”任务及相关表格。只调整实验范围和执行顺序；已经产生的合法数据、配置、权重、日志、评测不得删除。不要询问我是否继续下一组；所有必做实验提前确定并全部入队。不要把工作拆成需等待人工批准的多阶段计划。

## 0. 唯一目标和绝对边界

我目前**只完成硕士论文第三章**，基线为 Stanford RSS 2023 的 **CNN-based Diffusion Policy**（ResNet18 视觉编码 + Conditional 1D U-Net + FiLM + 原有扩散训练/推理）；第三章的方法为 **GSC-DP（Geometry-aware Spatial Conditioning Diffusion Policy）**。保留原始 CNN-DP 的动作空间、扩散调度器、预测目标、动作预测/执行时域及其实际任务适配，不为了优化结果擅自改动去噪骨干。

**唯一允许的正式训练方法：**

- `M0`：原始 RGB CNN-DP。输入训练/推理可用 RGB 和统一低维机器人状态，不读取 Depth 作为策略特征。
- `M1`：`M0 + GSA`。在 ResNet18 合适的低分辨率中间特征位置插入来自 DFormerv2 思路的 **Depth-conditioned Geometry Self-Attention**；输入当前真实相机 Depth，保留原来的 RGB 主干和 CNN-DP 去噪网络。
- `M2`：`M1 + Geometry-associated TokenLearner`。在经过 GSA 增强的二维视觉特征上提取 8 个学习的空间 Token，复用每个 Token 的**同一权重图**计算 `(u,v,d,rho)` 几何属性，经投影残差融合回原始全局观测条件。M2 的 GSA 和 Depth 前处理与 M1 **完全同构**。

**唯一正式任务：**

- MimicGen Core：`stack_three_d1`、`threading_d2`、`coffee_d2`；每任务 200 条完整训练示范。
- ManiSkill 3：`StackCube-v1`、`PegInsertionSide-v1`；每任务 100 条官方 motionplanning 示范。
- 这叫**两个 Benchmark、五个任务**，不是五个 Benchmark。
- 训练种子固定：`0, 1, 2`；总共 `3 models × 5 tasks × 3 seeds = 45` 个唯一 `(method,task,seed)` 配置。任何合法已完成运行要复用。**没有其他方法需要训练**。

**明确禁止自行增加：** 参数量、FLOPs、推理延迟、峰值显存等计算效率对比或测速实验；RGB-D 4 通道 CNN-DP 对照；普通自注意力或其他注意力结构对照；没有 GSA 的 TokenLearner；普通 TokenLearner；ResNet34/50 或编码器比较；Token 数 K 的比较；坐标/深度删减微消融；示范数量/数据效率试验；深度扰动专项实验；额外 benchmark；ACT、Transformer-DP、BC-RNN、DP3、EquiDiff 的本地重训；第四章的任何内容。现有论文已发表的相关成绩只能**单独作为文献参考**，不可冒充本地统一协议下的复现对比。

## 1. 唯一训练矩阵与评测协议——全部固定，不得擅改

| 基准 | 环境 ID | Demos | 训练总量 | 周期性 checkpoint 间隔 | 每个 checkpoint 的闭环评测 episodes | max episode steps | 每 seed checkpoints |
|---|---|---:|---:|---:|---:|---:|---:|
| MimicGen Core | `stack_three_d1` | 200 | 250 dataset epochs | 每 5 epochs | 50 | 400 | 50 |
| MimicGen Core | `threading_d2` | 200 | 250 dataset epochs | 每 5 epochs | 50 | 400 | 50 |
| MimicGen Core | `coffee_d2` | 200 | 250 dataset epochs | 每 5 epochs | 50 | 400 | 50 |
| ManiSkill 3 | `StackCube-v1` | 100 | 100,000 optimizer updates | 每 5,000 updates | 100 | 200 | 20 |
| ManiSkill 3 | `PegInsertionSide-v1` | 100 | 100,000 optimizer updates | 每 5,000 updates | 100 | 300 | 20 |

- MimicGen 250 epoch / 5 epoch checkpoint 沿用现有实验协议，参考 2026 IJRR EquiDiff 的 200-demo 训练预算；**50 rollout episodes 是本研究选定数值，不要称为 MimicGen 官方要求**。
- ManiSkill StackCube 的 100k iterations 来自官方 RGB 视觉 DP 基线的参考设置；PegInsertionSide 的视觉 DP 100k 是我们以同任务官方 state-DP/视觉 ACT 配置为参照做出的统一研究约定，**不要写成官方已经发布的 RGB-D DP 最优配置**。
- **一个 epoch 在实际代码里必须是完整遍历 DataLoader 的训练窗口，且保存每 epoch optimizer updates、DataLoader batches、dataset window count 和 batch size。** `optimizer updates` 以真实 `optimizer.step` 数计。不得人为将 250 epoch 理解成 250 个 batch。
- 学习率计划、EMA、训练集、归一化、视觉分辨率、相机数、观测时域、动作时域、Batch Size、Diffusion inference steps 和动作控制模式在**同任务 M0/M1/M2**上尽可能相同且固定；三方法只有上述指定结构与 Depth 输入差异。优先沿用已有合规配置；如果既有配置违反公平性，则记录、修正并明确指出哪些旧 checkpoint 无法合并报告。
- 本次已知有过单次 250 epoch 约 9h 的训练。**不能因为耗时擅自缩短以上预算，不能删掉周期性正式 rollout，也不能以更少种子替代完整结果。** 可优化缓存、GPU 并行、环境并行、数据读取、评测调度；不能损害统计口径。实际耗时和瓶颈必须记录。
- 如果早已保存的 checkpoint 已经通过同样的 50/100 episode 评测，按 checksum、配置及 reset-manifest 验证后**直接复用，不重复 rollout**。

完整矩阵最多产生 45 次训练；对应已约定 checkpoint 评测总数为 MimicGen `27×50×50=67,500` episodes、ManiSkill `18×20×100=36,000` episodes，合计 **103,500 episodes**（若有既有结果则只补缺，不额外增加）。

## 2. 真正接入官方 CNN-DP 的技术要求

1. 从当前仓库真实源码定位并保留 `DiffusionUnetImagePolicy` 或实际等价实现、原始 `MultiImageObsEncoder`、ResNet18、SpatialSoftmax/图像特征汇聚、`ConditionalUnet1D`、FiLM、Normalizers、NoiseScheduler、训练入口与 rollout 入口。记录上游 Git SHA 和实验项目 Git SHA，不能把另一个重写网络伪装成原始 CNN-DP。
2. **M1/GSA**：根据 DFormerv2 的 `GeoPriorGen` / `Decomposed_GSA` 原始代码与公式适配一层轻量低分辨率空间注意力。必要的通道投影、深度插值与有效像素处理必须与特征网格精确对齐。按 `F_g = F + gamma * GSA(F,D)` 残差融合；位置在中间视觉编码阶段，不能为 M1 替换整个 backbone 或修改动作去噪器。不得将深度值本身当成像素语义标签。
3. **M2/关联 TokenLearner**：对 `F_g ∈ R^{B×C×H'×W'}` 为每个 Token `j=1..8` 产生空间分数，沿 `H'W'` softmax 得到 `pi_j(u,v)`；计算 `z_j = Σ pi_j F_g`。用**完全相同的 pi_j**计算归一化图像坐标 `(u_j,v_j)`、带有效深度 mask 的 `d_j = Σ(pi_j*m*D)/(Σ(pi_j*m)+eps)`、深度有效比例 `rho_j=Σ(pi_j*m)`。深度有效像素为零要有显式数值策略。构造每 Token 的视觉特征与 `(u,v,d,rho)` 关联表示，投影/残差融合到原始 CNN-DP 的 `global_cond`，不改变原有 Cond1D U-Net 输入输出尺寸和预测目标。
4. `(u,v,d,rho)` 是像素位置加深度的 **2.5D 几何描述**；没有使用相机标定反投影时不可命名为世界系 3D 位姿/点云。输入相机及时间索引不得错误混合；多相机/多帧可按已有观测编码拼接逻辑分别编码并聚合。
5. GSA 和 TokenLearner 仅在每次**新观测编码**时计算一次、在该次动作块多个去噪步间复用，禁止每个 diffusion timestep 都重新执行视觉 backbone。
6. M0 原始 RGB 的数据增强/归一化及低维状态输入应与两种改进模型的公共部分一致。M1 和 M2 **不得从测试环境中读取未来状态、完整场景 Oracle 位姿、目标位置、仿真 segmentation GT 等作为策略输入**。这些真值只允许做离线可视化和误差分析。
7. 不新增训练辅助损失。M0/M1/M2 使用相同的官方 CNN-DP Diffusion Policy 训练损失；是否 `prediction_type=epsilon/sample` 以本次锁定的真实任务配置为准，不能公式和代码互不一致。
8. 完整实现训练加载/模型保存/独立推理/恢复，确保 M1、M2 的额外模块参数确实进入 optimizer、EMA 和 checkpoint；训练和推理使用一致的 Depth 单位与缺失值规则。

## 3. 五个任务的真实数据与环境复现

### MimicGen（200 demos/task）

- 使用官方 **Core** 数据集（不得误用 Source、large_interpolation 或同名 D0/D2 变体）。记录官方 task ID、HDF5 文件 SHA、原始示范 ID 和选中的 200 条 ID；对 M0/M1/M2、三种子固定相同的 demonstration 子集，并持久化为 `dataset_manifest.json`。若数据本身不足 200 条，只能继续下载对应完整数据，不能偷偷缩减。
- 核查 HDF5 是否包含可直接使用的**同步 RGB+真实 Depth+相机观测**；若没有，应按照官方状态回放及相机接口对真实示范生成匹配的两机位（或所选固定机位）RGB-D。必须匹配相机视角、分辨率、相机内外参/Depth 定义、时间戳、obs/action 对齐、action control 语义和原始 reset/environment 配置。**不得用 RGB 灰度、任意估计深度或随机贴图伪装真实深度**。
- checkpoint rollout 重新构建官方任务环境，以官方 success 判定；episode horizon 400，并保存每个评测 episode 的 seed/reset ID、实际执行步数和 success。必要时固定一批同任务跨方法共享的 eval reset seeds，不能在测试时用示范未来状态喂策略。

### ManiSkill 3（100 demos/task）

- StackCube：官方 motionplanning `pd_ee_delta_pos` 数据和对应图像/Depth；PegInsertionSide：官方 motionplanning `pd_ee_delta_pose` 数据。检查本机官方数据的真实文件名与 metadata，必要时依照官方轨迹 replay/RGB-D re-render 工具重建与控制模式完全一致的数据。严禁将不同控制模式动作静默混用。
- 按环境版本确定 `obs_mode` 中的 RGB-D 数据接口、单位、depth tensor、相机一致性和有效深度掩码；记录任务的 `sim_backend` 和并行仿真设置。
- 使用官方成功判定，优先主要报告 episode 结束时的 `success_at_end`，同时记录 `success_once`；如果版本 API 不存在对应字段，检查环境官方成功标志并把准确对应关系写入文档，**不要自行把 success_once 当最终成功率**。
- StackCube max 200 steps，PegInsertionSide max 300；同任务所有模型在一致的初始状态分布和控制空间评测。

## 4. H200 统一任务队列：全部提前生成，无阶段门槛

- 使用 `planning-with-files`：读已有 `task_plan.md`、`findings.md`、`progress.md`；生成/维护一个可靠的单一真相源，如 `experiments/ch3/run_manifest.csv` 或 sqlite，枚举 **45 个唯一训练 run**、各 run 所需 checkpoint、全部 rollout 作业及其状态（PENDING/RUNNING/DONE/FAILED）、配置 hash、提交时间、GPU、日志路径、ckpt 文件/SHA 和结果源。
- 启动前实际读取当前 H200 **可用卡数/可用显存及共享使用情况**、CPU、内存、磁盘、GPU 利用率、显式/无头渲染能力；绝不能假定“八张 H200 全归我独占”。
- 所有作业按如下**优先级，不是阶段**进行调度：同等资源情况下 M2 最高、M1 次之、M0 再次；任务优先 `threading_d2 → PegInsertionSide-v1 → stack_three_d1 → coffee_d2 → StackCube-v1`。但只要资源足够，45 个 run 可以同时部分启动，**不能因 M2 未训练完而阻挡 M1/M0**。
- 每个 run 用真实目录、配置和原始日志；进程需要支持 SSH 断开后继续（例如 `nohup`/`tmux`，视机器现有环境选择，无 root 权限不得依赖 sudo）。GPU 资源用明确锁/配额控制，避免与他人作业争抢和同卡意外超额。
- 设置 `train_queue`、`eval_queue` 和 `viz_export_queue` 三个可恢复队列；训练成功保存每个规定 checkpoint 后**原子落盘**（tmp→rename），完整写入 manifest，再由独立评测进程加载磁盘 checkpoint 执行对应 rollout。不得使用训练内存模型替代 ckpt 评测。可同时执行训练、评测、离线出图；队列异常自动恢复，确保 job 去重。
- 利用 ManiSkill 官方 GPU vectorized env 等可用加速方式，但不可改变 episode 数、每 episode 独立重置逻辑或 success 定义。MimicGen CPU/GPU 渲染并行要以资源测量为依据，不能让 50 episodes 都在同一 random seed 下重复相同初态。
- 在不降低工作量的前提下优化读取：例如将固定 RGB-D 数据预渲染为训练友好格式、顺序存储、pin_memory、persistent_workers、缓存，而不是每次反复通过仿真生成相同训练帧。仅为服务器排队、异常恢复和资源分配记录 CUDA 利用率、data loader wait、steps/s、rollouts/s、单次训练耗时；这些是运行日志，不形成论文中的计算效率实验或对比结论。
- 不要提出大堆无关审查报告或数百个小样本冒烟训练；只实施必要的一次数据/动作/Depth 一致性、参数梯度及 checkpoint 独立加载核查，然后直接按完整协议执行正式训练。不要以测试成功率不理想为由跳过负结果模型/种子。

## 5. 周期性评测和严格统计定义

所有 success 数据必须来自实际 checkpoint 的真实 closed-loop rollout。保存**每一条 episode**和每个 checkpoint 的统计；每任务所有模型在相同的可控 reset 列表/初始状态种子（若环境允许），其中困难随机任务优先固定 rollout reset 列表以减少方法比较噪声。

对每个 `(task,method,seed)` 的第 i 个 checkpoint：

`SR_i = successes_i / episodes_i`。

- `BestSR_seed = max_i SR_i`，不能把 `mean(train loss)` 作为选 ckpt 标准，也不能“偷看一个独立最终测试集再重新调参”。必须注明它是**周期性 rollout 的最佳值**，有择优偏差，不称独立 holdout test。
- `Last10SR_seed = mean(SR_{N-9}, ..., SR_N)`，取最后 **10 个按实际训练进度排序** 的 checkpoint，不是成绩排名前十个；MimicGen 对应最后50 epoch内十个点，ManiSkill 对应最后50k updates内十个点。
- 3 个独立 seed 先各自算 Best/Last10，再报告 `mean ± sample_std (ddof=1)`；不能把不同 seed 的 episode 混合当作 150/300 次单一测试，也不能把 50 次 checkpoint 的最高 episode 当作真实成功率。
- 计算 `Δ_GSA = SR(M1)-SR(M0)`、`Δ_Token|GSA = SR(M2)-SR(M1)`、`Δ_full = SR(M2)-SR(M0)`，每个比较以相同定义的 Best/Last10 独立给出；主结果用任务成功率，训练/验证 diffusion loss 辅助报告但不代替成功率。
- 可用 paired seed 和同初态复用分析操作失败案例，但不强制引入额外假设检验和新训练。结果不论正负都入表，不得挑任务/挑 seed。
- 注意结论边界：M0→M1 **同时引入 Depth 和 GSA**，故能得出整个 Geometry-GSA 策略的增量，而不能独立归因“普通 RGB-D 无效、只有 GSA 有效”；M1→M2 深度和 GSA 相同，能更清楚检验关联 TokenLearner 的增量。论文不应超出这些数据声称因果。

## 6. 直接从现有权重生成第三章成功率与可视化图表，避免重复训练

所有图表必须由真实代码、日志、轨迹和 checkpoint 自动产生，禁止人工补成绩、伪造热图、填模拟数据。图表文件下面必须有同名可追溯 JSON/CSV 数据源与 `task/method/seed/checkpoint_sha/eval_manifest`。

**必须交付（只涉及任务成功率、逐模块效果与空间注意力/执行过程可视化，不需要计算效率类论文图表）：**

1. `表3-1`：五个任务名称、Benchmark、示范条数、训练预算、评测 episodes、horizon、输入模态与控制模式。
2. `表3-2`：**M0/M1/M2 × 五任务** 的三个种子 `BestSR(mean±std)`；同表附各模型平均提升百分点，或生成独立差值表。
3. `表3-3`：M0/M1/M2 × 五任务的 `Last10SR(mean±std)`，不与 Best 混淆。
4. `图3-X`：五任务的周期性闭环成功率训练曲线（用 optimizer updates 或 benchmark 自身单位标注横坐标；三 seed 均值/波动，保留原始逐 seed 曲线数据）。也保存 loss 曲线供训练分析。
5. `图3-X`：本章三模型结构示意，明确 GSA 插在 ResNet18 的位置、TokenLearner 在 GSA 之后及其 `(u,v,d,rho)` 的计算、融合到 `global_cond` 的路线；网络结构图必须对应真实代码（不凭空画新分支）。
6. `图3-X`：**真实 GSA 注意力可视化**，展示 RGB、Depth、选定 Query 对其他位置的空间权重热图；注意 DFormerv2 Decomposed_GSA 的轴向 attention 不等于任意假定的完整二维 attention。如需二维展示，须基于代码中实际注意力权重严格构造或明确标注近似/轴向视图，不能用任意激活图冒充注意力。
7. `图3-X`：M2 的 8 个 TokenLearner 空间权重图叠加 RGB，记录每个 Token 的 `(u,v,d,rho)` 和有效 Depth mask，解释为 learned spatial aggregation weights，不凭空赋予“抓取点/目标物体”语义标签。
8. `图3-X`：从代表性 checkpoint 的真实成功/失败 rollout 中提取**接近、抓取、搬运、对齐、插入/放置**的4–6关键时刻，绘制 RGB + GSA 注意力 + TokenLearner 权重 + 当前机器人/任务状态并导出 MP4；按环境真实事件或明确人工/离线标注定义阶段。注意策略按 action chunk 重新规划时才更新观测编码，不能误写为每次仿真小步都重算注意力。
9. `图3-X`：同一初始 reset 下三模型的成功/失败典型轨迹（必要时用末端执行器/物体 GT 仅做离线标注）；不强制额外标注昂贵的密集真值指标。

输出目录建议：`thesis/chapter3/{tables,figures,source_data,videos}`，另写 `thesis/chapter3/experiments_3_6.md`，按照 `3.6.1 实验平台和评价指标 / 3.6.2 五任务成功率比较 / 3.6.3 GSA与TokenLearner递进式效果分析 / 3.6.4 空间注意力与时序关注可视化 / 3.6.5 典型操作过程与失败案例` 记录设置、引用来源、真实结果和分析；**数值未跑出之前用 TODO，不得虚构**。必要时生成可直接粘贴到硕士论文的中文图题、表题及简洁结果分析；不输出任何模型参数量/FLOPs/推理时延/显存比较表，不要擅自扩展第四章。

## 7. 论文文献结果的处理方式

相关研究（CNN-DP、ACT、DP3、EquiDiff、Transformer-DP 等）已有正式发表成绩时，优先收录来源、发表年份、对应具体任务、示范数、传感模态、评测回合、成功率统计口径到 `thesis/chapter3/literature_results.csv`。

- **不要求重新训练上述其他方法**；与我们 MimicGen 三任务匹配的已发表数据可以在**独立的“文献结果参考”表**中标明 Published，不得当作与 M0/M1/M2 完全相同的 reset/seed 条件获得的数据。
- 不在主消融表混排不同协议的数字，不做不具可比性的百分点归因，无法确认元数据的文献结果标记 `not directly comparable`。
- ManiSkill 若没有同任务同设置的可信正式发表结果，就保留 M0/M1/M2 自己的五任务结果，不硬填 ACT/DP3 成绩。

## 8. Codex 应实际产出的文件与运行证明

必须修改/生成实际可运行程序和配置，不仅仅输出 markdown 方案。最少包括：

- `task_plan.md`、`findings.md`、`progress.md`，明确取消所有旧额外实验任务，保留完整 45-run 固定矩阵和已完成进度；`docs/research_decisions.md` 写下“第三章效果优先、已有文献结果不默认重训、只做三网络五任务、不做计算效率实验或额外消融”的长期决策。
- `experiments/ch3/run_manifest.csv` 或 SQLite、所有任务 `configs`、`dataset_manifest` / eval resets manifest、独立 train launcher、checkpoint writer、独立 eval runner、可恢复 job queue、合规 ckpt 自动复用逻辑、自动汇总统计脚本。
- 深度渲染/缓存脚本及一致性说明、CNN-DP/M1/M2 的模型实现和开关、导出注意力与 Token 权重的稳定 instrumentation；不要让保存 attention 改变模型推理结果。
- 全量原始训练与 rollout 日志：每个 run 对应固定配置、Git SHA、数据 SHA、seed、optimizer updates、每次 rollout 原始 episode success、设备 ID、checkpoint SHA。
- `thesis/chapter3/` 全部 CSV、PNG/PDF 图表（论文插图优先矢量格式）、可视化 MP4 和 `experiments_3_6.md`。图题、来源、单位和统计说明齐全。
- `experiments/ch3/STATUS.md`：矩阵已完成/运行中/待处理、成功 checkpoint 数、rollout 实际完成 episodes、估算剩余 GPU-hours、异常原因、准确的一键恢复命令。**不能将队列已创建写成实验已完成**。
- 对目前运行中的任务：能安全复用就继续，不要无故中断训练；如发现旧实验还在运行本次明确取消的额外方法，核对资源与所有者后停止本项目专属的旧作业，绝不杀掉其他用户进程。先保留记录。

## 9. 实施与报告的硬性要求

1. 当前请直接定位仓库、现存 checkpoint/日志、服务器资源和 demo 数据；建立全部 45-run manifest 和 rollout 队列；完成必要的真实数据/模型接口检查后，**开始完整正式训练和异步评测**。不要只给方案。
2. 优先 M2 评测得到方法效果，M1/M0 尽可能并行。任何完成的任务立即增量更新论文表格和图，不必等全部跑完才导出。
3. 不要向我提出“先做 5 条演示/1 epoch 冒烟试验再决定”这样的替代方案。只做必要工程验收，不做额外小数据研究实验。
4. 同一任务中，M0/M1/M2 的训练协议、示范 ID、评测 reset 和 checkpoint schedule 不得随意变化。已有结果有历史协议差异要标注并按同一预定规则补齐，不允许直接合并错配结果。
5. 失败任务自动记录错误并继续其他可运行队列；修复后恢复。不得把 3 seeds 减成 1 seed、不得用验证 loss 冒充成功率、不得根据希望的最终结果筛选时间点。
6. 你最后应向我报告**已经实际修改/创建的代码、当前真实启动的作业 PID/资源、已复用权重、已跑完 checkpoint 和真实评测结果、剩余队列与恢复命令**。没有实际启动/没有结果必须明确说明，不得声称已经完成。SSH/会话中断后仍有明确持续运行机制；不是 Codex 文本回复后假装在后台进行。
7. 除本文件明确的三网络×五任务、既定周期性 eval、可视化与执行案例外，**禁止新增任何训练组或计算效率实验**。不规划第四章。

## 10. 直接查阅的原始代码/协议来源（请 pin Git SHA）

- CNN-DP 官方：https://github.com/real-stanford/diffusion_policy
- MimicGen 官方（Core 数据、任务注册与 horizon）：https://github.com/NVlabs/mimicgen
- ManiSkill 官方：https://github.com/mani-skill/ManiSkill ，重点参考 `examples/baselines/diffusion_policy/baselines.sh`、`train_rgbd.py` 及轨迹回放工具
- DFormerv2 Geometry Self-Attention 原始实现：https://github.com/VCIP-RGBD/DFormer/blob/main/models/encoders/DFormerv2.py ，关注 `GeoPriorGen` 与 `Decomposed_GSA`
- TokenLearner 官方参考：https://github.com/google-research/scenic/tree/main/scenic/projects/token_learner
- MimicGen 200-demo 训练预算参考：*Equivariant Diffusion Policy for Sample-Efficient Robotic Manipulation*, IJRR 2026。仅借用相应训练预算依据，不能宣称该论文全部协议/结果与本实验一致。

**最终验收条件：** 真实有效的 45-run 矩阵（含复用）、两个 Benchmark 五任务的 BestSR/Last10SR、模块递进差异、可复现原始 episode 日志、真实 GSA 与 TokenLearner 时序可视化、典型成功/失败执行案例及一套能够直接写入硕士论文第三章 3.6 节的表图和中文分析。除此之外，不进行其他训练实验。
