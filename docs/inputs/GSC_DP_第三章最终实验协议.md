# GSC-DP 硕士论文第三章：正式实验协议 v1.0

> 协议性质：实验实施规范（不是已获得的结果）。制定日期：2026-10-13。主方法为原版 CNN Diffusion Policy 上的 GSA + 深度关联 TokenLearner。训练、评测均运行在实际可用的 H200 服务器上。每个 Benchmark 采用其自身可复现的研究惯例；**同一任务内所有方法必须接受相同的示范与闭环评测设置**。有关官方已发布的参数与本文自行选择的参数，在下文逐项标识。

## 1. 固定研究问题与任务

研究问题 RQ1：加入真实 RGB-D 几何信息，相对 RGB CNN-DP 是否改善闭环操作成功率？

RQ2：相对于直接拼接 RGB-D、普通注意力和更大的 CNN，GSA 的显式深度几何先验是否有独立增益？

RQ3：加入局部加权位置、绝对深度和深度有效性的 Token 是否有独立增益？GSA 与 Token 模块是否存在正交互？

RQ4：该收益是否转化为更准确的物体—目标相对位姿、更小的操作阶段误差和可接受的规划开销？

正式任务集：

| Benchmark | Task ID | 主训练示范 | 操作类型 | Episode horizon | 官方依据及性质 |
|---|---|---:|---|---:|---|
| MimicGen Core | `stack_three_d1` | 200 | 多物体堆叠、空间区分 | 400 | MimicGen 官方任务；200 demos 为 IJRR 2026 对比论文的数据量档位 |
| MimicGen Core | `threading_d2` | 200 | 针/支架对准与穿入 | 400 | 同上 |
| MimicGen Core | `coffee_d2` | 200 | 多阶段操作 | 400 | 同上 |
| ManiSkill 3 | `StackCube-v1` | 100 | 抓取与堆叠 | 200 | 官方视觉 DP `baselines.sh` 明确含此任务，100 demos / horizon 200 |
| ManiSkill 3 | `PegInsertionSide-v1` | 100 | 精细插入 | 300 | 官方状态 DP 与视觉 ACT 含此任务；视觉 CNN-DP 总更新数为本文参照制定 |

MimicGen 的 400 步来自官方注册的 evaluation horizon；在没有确认具体数据版本环境元数据之前，禁止自行覆盖成 500/700 步。ManiSkill 的 200、300 是其官方 DP/ACT baseline 推荐的 `max_episode_steps`。训练动作控制模式、采集后端与观测相机以下载示范的实际元数据为准，确认后锁定并记录。

## 2. 固定训练与周期性闭环评测

| Benchmark / Task | 训练长度 | 保存 checkpoint | 从磁盘 checkpoint 启动的 rollout | 单 checkpoint episodes | 保存点评测数/训练种子 | 来源说明 |
|---|---:|---:|---:|---:|---:|---|
| MimicGen Stack Three D1 | **250 epochs** | 每 **5 epoch** | 每 **5 epoch** | **50** | 50 | 250/5 源于 IJRR 2026；50 episodes 是本文固定值 |
| MimicGen Threading D2 | **250 epochs** | 每 **5 epoch** | 每 **5 epoch** | **50** | 50 | 同上 |
| MimicGen Coffee D2 | **250 epochs** | 每 **5 epoch** | 每 **5 epoch** | **50** | 50 | 同上 |
| ManiSkill StackCube-v1 | **100,000 optimizer updates** | 每 **5,000 updates** | 每 **5,000 updates** | **100** | 20 | 官方视觉 DP `baselines.sh` 与 `train_rgbd.py` 默认评测参数 |
| ManiSkill PegInsertionSide-v1 | **100,000 optimizer updates** | 每 **5,000 updates** | 每 **5,000 updates** | **100** | 20 | 100k 参照官方状态 DP/视觉 ACT；5k/100 参照官方视觉 DP 通用参数，**非官方已调优视觉 DP 配置** |

MimicGen 的 2026 IJRR 参考实验：训练 `50000/N_demo` epochs，每 `1000/N_demo` epochs 评测一次，总计 50 个评测点；200 demos 时得到上表的 250 与 5。该论文采用观察历史 2、预测动作长度 16、执行 8、DDPM 去噪 100 步、AdamW lr=1e-4、warmup 500、EMA；本章 CNN-DP 家族优先沿用这些固定配置并通过实际 YAML 固化。**50 episodes 是本章预注册的统一取值，不冒称参考论文的原文数值。**

ManiSkill 官方 RGB 基线使用 100k updates 的 StackCube、`eval_freq=5000`、`num_eval_episodes=100`；PegInsertion 视觉 ACT 也提供 100k 配置。ManiSkill 的 100k 不称为 epoch。建议观测 128×128，但必须核对实际版本脚本及任务相机视角，并且**同一 ManiSkill 任务的所有图像策略使用同一相机集合、分辨率和信息可见性**。

三个训练种子：`0,1,2`。所有方法对照均采用相同示范子集 manifest、同一评测 reset 列表、同一 episode horizon 和同一主指标。不同 seed 的随机权重初始化独立；评测环境 reset 集合固定在训练种子之间也相同。checkpoint `0` 不纳入 50/20 个统计点。任何缺失保存点必须显式失败或标注缺失，不得悄悄缩小分母。

## 3. 成功率报告口径（全部从独立加载 checkpoint 的闭环 rollout 计算）

每个方法 m、任务 q、训练种子 s、保存点 e：`SR_{m,q,s,e} = success_count / N_eval`。MimicGen 使用任务官方 success 条件；ManiSkill **主指标 `success_at_end`，辅指标 `success_once`**。不能把 success_once 与其他任务主指标平均。

- **Best SR（论文主表）**：每个训练种子所有规定保存点的 `max_e SR_e`，跨三个训练种子报告 `mean ± sample std`。这是“训练期间观察到的最佳周期性闭环性能”，存在选择最大值的正偏差；不能称为独立 holdout test 精度。
- **Last-10 SR（论文独立附表/图）**：最后 **10 个按训练进度连续的保存点** 的平均 SR，之后在三个种子上统计 `mean ± sample std`。它不是“全训练过程中最佳 10 个”。
- **学习曲线**：训练进度横轴按 Benchmark 独立单位记录（MimicGen epoch；ManiSkill optimizer updates），每点展示三个种子均值与标准差，原始每种子曲线同时保留。
- 另外保留每 checkpoint 逐 episode `(seed, reset_id, success, horizon, failure_reason, checkpoint_hash)`，可计算 Wilson CI、同一初始状态配对差异及交互效应，但不能将高度相关的 checkpoint 当作独立训练种子。
- 同 Bench 内可给任务宏平均，**跨两个 Bench 不默认计算一个无定义的总 SR**。

## 4. 主流模型对比与信息公平

| Model | 论文主表名称 | 模态 | 研究用途 | 具体可复现要求 |
|---|---|---|---|---|
| M0 | CNN-DP (E0) | RGB | 直接基线 | 原版 `real-stanford/diffusion_policy`、ResNet18、Conditional 1D U-Net |
| M1 | Transformer-DP | RGB | 动作网络骨干对比 | 原版 DP Transformer；保留其原始动作预测与执行参数并记录 |
| M2 | ACT | RGB | 非扩散动作块方法 | 官方 `tonyzhaozh/act`；MimicGen 可参考 IJRR 2026 chunk=10, KL=10, batch=64, lr=5e-5，非统一改成 U-Net 参数 |
| M3 | BC-RNN | RGB | 经典序列模仿学习 | robomimic 官方 BC-RNN/LSTM-GMM；按照方法合理 action semantics，记录是否相对控制 |
| M4 | DP3 | 同源深度反投影点云 | 3D 几何竞争方法 | 使用与 GSC 相同的深度相机、内外参；禁止完整场景 GT point cloud 或对象状态作为策略输入 |
| M5 | GSC-DP (E6) | RGB-D | 本文完整方法 | GSA + Depth-associated TokenLearner，扩散动作 U-Net 不变 |

主表应该按方法输入模态分组，且额外给同模态强对照 `RGB-D CNN-DP (E1)`；这样不会误把 RGB 与 RGB-D 的信息差别全归因于 GSA。比较 ACT/BC-RNN/DP3 等方法时，**不强制相同 obs_horizon、chunk size、action representation**，采用它们公开且合理的设置，保持数据、控制环境、episode horizon、评测条件一致并记录差异；禁止把不同控制语义造成的差异隐瞒。优先复用已发表公开实现，同任务若确实不支持应记录修复/适配，不得贴不同论文的数值充当本次实测。

## 5. 关键模块消融 / 编码器对比

| ID | 方法 | 首批任务覆盖 | 归因意义 |
|---|---|---|---|
| E0 | RGB ResNet18 CNN-DP | 5 个任务 | RGB 直接基线 |
| E1 | RGB-D 4-channel ResNet18 CNN-DP | 5 个任务 | 深度数据本身的贡献 |
| E2 | RGB ResNet18 + plain SA | Threading、StackCube、PegInsertion | 额外注意力容量 |
| E3 | RGB ResNet18 + Depth GSA | 5 个任务 | 工作点一 |
| E4 | RGB + Depth-associated TokenLearner（无 GSA） | 5 个任务 | 工作点二 |
| E5 | GSA + vanilla visual TokenLearner（无 u/v/d/rho） | 3 个机制任务 | 几何 Token 的增量 |
| E6 | GSA + Depth-associated TokenLearner | 5 个任务 | 完整方法 |
| E7 | RGB-D CNN + plain SA | 3 个机制任务 | 区分 GSA 与“输入深度 + 注意力” |

编码器：`RGB-D ResNet18 / ResNet34 / ResNet50 / ResNet18+plain SA / ResNet18+GSA`。至少 Threading D2 与 PegInsertion 两项代表性任务比较；所有结构必须使用原始相同 U-Net 条件维度和相同训练与评测，统计参数量、FLOPs/延迟、显存和成功率。

**核心设计要点**：E3 与 E4 在无 GSA/Token 时仍保留一条与原版 DP 一致的视觉基础分支。`E5` 的 Token 聚合与 `E6` 的 Token 数、位置、投影参数规模尽量匹配，差异集中在几何值是否提供。为检验区域深度与图像位置作用，额外做 `-uv`, `-d`, `-rho`, `K=4/8/16` 等微消融，在 Threading + PegInsertion 做，不必在全部任务复制。

## 6. 数据效率 / 干预 / 效率

数据效率选择 MimicGen Stack Three D1、Threading D2：100/200/1000 条，至少 E0/E1/E6，示范集合嵌套，三种子。遵循 IJRR 训练对齐公式：100 demos → 500 epochs、每 10；200 demos → 250 epochs、每 5；1000 demos → 50 epochs、每 1；各 50 个保存点，每点 50 episode 为本研究取值。

深度干预只作为**额外研究设置**：`Depth clean`, `structured depth noise`, `invalid patches`, `depth shuffled per patch`, `remove token depth`, `disable depth prior`。在同 checkpoint、同环境初始状态、同方法的配对比较中进行；不得在主 benchmark success 表中混入干预结果。注意 depth shuffle 导致的 out-of-distribution 性能下降不能单独证明 GSA 的几何机理，只能作为配合注意力与动作误差证据的因果敏感性分析。

性能：计算参数量、batch=1 视觉时间、完整规划时间（含所有 DDPM/DDIM step）、端到端 action latency、peak GPU alloc；GPU 正确 warm-up、synchronize、隔离其他 GPU 负载、固定图像大小。并行运行期间的 latency 不可与独占 GPU latency 混作公平比较，统一在独占时段重测。

## 7. H200 并行计算与结果不串扰

- 首次运行探测 `nvidia-smi --query-gpu`、显存、GPU 数量、CPU 逻辑核心、RAM、仿真渲染 EGL/PhysX 后端；不得假设有 2 张 H200 或固定可用显存。
- 使用两条持久化工作队列 `train_queue` 和 `eval_queue`，调度单位 `(benchmark,task,method,seed,ckpt)`；训练 run 与评测 run 在**不同独立进程**中运行，评测只能读取原子写入并验证 SHA256 后的 checkpoint。
- GPU 资源监控与抢占保护：依据实际可用显存和 CPU/仿真资源，允许单卡或多卡上多个作业并发；为每作业设置设备绑定和最大容许 GPU/CPU 资源，开跑前验证不与现有进程过量抢占；若资源不够则等待**队列中的下一次调度**，不缩减训练规模。
- 训练与评测可交错并行。推荐策略是“checkpoint 原子落盘 → 评测队列增量入队 → 有空闲资源即异步评测”，不必等所有 epoch 训练结束；每个独立评测仍只加载保存的 checkpoint。
- RNG、数据加载 worker、环境 seed、CUDA 显存、图形渲染上下文和输出路径隔离；MuJoCo 的 EGL 设备与 CUDA_VISIBLE_DEVICES 的物理 GPU 映射要一一记录，避免渲染跑到另一张卡。
- 训练结果与评测输入去重：每个 `run_id` 唯一，文件写入 temp 后 atomic rename，数据库/manifest 状态枚举 `queued/running/finished/failed`，失败原因可追溯，断点恢复不覆盖已有数据。
- 论文时延评测需在**无其他 GPU 作业**的隔离窗口执行；多进程吞吐/资源利用率可另出一张工程表，不等同于单策略推理时延。

## 8. 论文证据及自动化输出契约

下列为必须覆盖的表/图（正式稿编号可微调）。每项产出附 `figure_manifest`：原始数据路径、模型 SHA、任务、相机、reset_id、训练种子、脚本 SHA、绘图参数、定义、单位。

| 输出 | 来源 | 检验的研究论断 |
|---|---|---|
| 表3-1 任务与超参数 | data manifest/config | 训练与评测可复现 |
| 表3-2 主流方法成功率 | eval episode JSONL | M0-M5 竞争力；Best/Last-10 分列 |
| 表3-3 E0-E7 消融 | eval JSONL | 两工作点和 GSA 深度先验作用 |
| 表3-4 编码器及容量对比 | weights/profiler + eval | 是否只是更大模型 |
| 表3-5 数据效率 | subset manifest + eval | 低示范量是否有收益 |
| 表3-6 几何注意力统计 | saved actual Q/K/weights + GT instances | 同物体/跨物体权重质量及特征相似度 |
| 表3-7 Token 统计 | actual mask, D, valid + GT | token 覆盖、深度与位置误差 |
| 表3-8 动作误差 | rollout state GT only offline | 距离/姿态误差与成功率的联系 |
| 表3-9 时延显存 | isolated profiler | 代价是否可接受 |
| 图3-4/5 主流对比与消融柱形图 | per-seed result | 主要结论 |
| 图3-6/7 训练进度与 last10 | per-checkpoint eval | 收敛与末期稳定性 |
| 图3-8 几何先验与 GSA 注意力 | actual observed tensor | 位置间交互机制 |
| 图3-9 原始特征/GSA 后特征 | actual tensors | 特征结构差异，不把 norm 称 attention |
| 图3-10 Token mask 和中心深度 | actual token/depth | 局部视觉-几何表示 |
| 图3-11 动作误差 | rollout state | 感知信息如何作用到控制 |
| 图3-12 成功/失败视频帧 | paired reset | 典型可解释案例 |
| 图3-13 深度干预 | paired test | 对深度输入的敏感性 |
| 图3-14 数据效率与延迟 | official eval + profiler | 有效性与成本 |

**注意**：无物体实例 GT 时，不填注意力“物体纯度”；TokenLearner 不是天然的物体分割器，目标 Token 关联需要事先登记算法规则，不能事后挑最大相似度的个例冒充整体。不得向策略泄漏 GT 分割、真值抓取姿态、任务进度标签。

## 9. 复现实验产物与完成标准

每个 `run` 保存 `config_resolved.yaml`, `versions.lock`, `dataset_manifest.json`, `seed`, `checkpoints/*.pt`, `train_metrics.jsonl`, `eval/<step>/episodes.jsonl`, `eval_summary.json`, `weights.sha256`, `gpu_job.json`, `artifact_manifest.json`。所有图表只从实际日志导出；任何不可计算字段留 `NA(reason)`。

论文第三章“完成实验”定义：5 任务 × (6 主流方法 + 额外 RGB-D 基线) × 3 种子的主表，5任务核心 E0/E1/E3/E4/E6 消融，3任务扩展注意力对照，2任务编码器/数据效率，代表性任务深度干预与动作误差分析，均有可复现实验记录、表图导出和明确失败日志。数据集和模型许可/版本同时归档。

## 10. 官方参考与使用说明

1. Diffusion Policy 代码与任务配置：https://github.com/real-stanford/diffusion_policy
2. MimicGen datasets（core、各任务轨迹）：https://mimicgen.github.io/docs/datasets/mimicgen_corl_2023.html
3. MimicGen 官方任务及 horizon：https://github.com/NVlabs/mimicgen/blob/main/mimicgen/__init__.py
4. Wang et al., *Equivariant diffusion policy for sample-efficient robotic manipulation*, IJRR 2026，尤其 §Simulation / Appendix Training Detail：https://doi.org/10.1177/02783649261424445
5. ManiSkill 官方 DP 训练脚本：https://github.com/mani-skill/ManiSkill/tree/main/examples/baselines/diffusion_policy
6. ManiSkill 官方轨迹重放：https://maniskill.readthedocs.io/en/latest/user_guide/datasets/replay.html
7. robomimic 图像+深度转换：https://robomimic.github.io/docs/datasets/robosuite.html
8. DFormerv2 (CVPR 2025)：https://github.com/VCIP-RGBD/DFormer
9. TokenLearner (NeurIPS 2021)：https://github.com/google-research/scenic/tree/main/scenic/projects/token_learner
10. DP3：https://github.com/YanjieZe/3D-Diffusion-Policy
11. ACT：https://github.com/tonyzhaozh/act

> 版本说明：文献与官网核验截至 2026-10-13，具体可执行 CLI 参数须由 Codex 在 H200 上根据已锁定的 git commit/实际 `--help` 二次核对。论文“已验证结果”只能由运行后的输出填入。
