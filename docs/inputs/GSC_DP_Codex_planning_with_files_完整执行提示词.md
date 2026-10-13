# Codex 总执行提示词：GSC-DP 硕士论文第三章（planning-with-files + H200 并行）

你是负责完成我的硕士论文第三章所有研究实验的 Codex 研究工程代理。**立即在 H200 服务器上真实执行**，不是只提交一份计划。第一步激活已安装的 `planning-with-files` skill（若用户安装路径不同，使用可发现的 SKILL.md），严格遵循其规范，长期将任务进度写入磁盘。

**请先完整阅读同目录的 `GSC_DP_第三章最终实验协议.md`、`GSC_DP_第三章论文初稿_20261013.docx`（若 Word 不方便解析，使用提供的同名 Markdown 文本），并将其中的研究目标、正式训练/评测数量、图表编号视作任务契约。** 若用户尚未将文件上传服务器，应先从当前会话输入获取它们的内容并保存为项目文档，不得假装已经读取。

## 0. 项目边界及核心交付

根目录建议 `/home/hanjinwei/p1/project/GSC_DP_Thesis`；如已存在真正的当前项目目录，先检查实际位置并沿用，不得覆盖已有有效实验。Baseline 唯一来自 `https://github.com/real-stanford/diffusion_policy` 的干净 commit，在独立实验分支开发 CNN-DP 的 RGB-D/GSA/TokenLearner 视觉编码部分，**动作扩散 U-Net、FiLM、噪声目标、动作表示保持所选原始配置**，不混入自条件和自适应采样等历史改动。

正式任务为：MimicGen Core `stack_three_d1`, `threading_d2`, `coffee_d2`；ManiSkill 3 `StackCube-v1`, `PegInsertionSide-v1`。

正式方法包含：RGB CNN-DP、RGB-D CNN-DP、Transformer-DP、ACT、BC-RNN/LSTM-GMM、DP3、GSC-DP；完整消融 E0-E7；视觉编码器对比；数据效率；空间机制；深度干预；效率/资源；均需得到可用于写论文的真实数字、图表和可追溯日志。

## 1. 立即启用 planning-with-files

- 先检查项目根目录 `task_plan.md`, `findings.md`, `progress.md` 是否已存在；若有，先读全部并检查 git diff、真实训练进程、文件状态，再恢复已有进度，不得重置进度。
- 若不存在，依照当前安装版本 planning-with-files 的 SKILL.md 模板创建这三个文件。规划按 Phase A～H 分解；每阶段定义完成标准、阻塞状态、可并行依赖和产物路径。必要时按 skill 的 isolated plan 方式安排并行子计划，但必须在总项目的 `task_plan.md` 留主索引。
- `findings.md` 记录官网、源码路径、版本兼容、obs/action 数据结构、测试采样规则、遇到的问题和已解决方案，逐项标注依据链接。
- `progress.md` 记录每次实际命令、起止时间、PID/job_id、H200 物理 GPU、运行状态、损失/成功率、代码 SHA、产出文件。错误不能略过；失败要记录原因和重试次数。
- 长事务断线、上下文压缩或 Codex 重启后，首先根据磁盘三文件、git status、`runs/index.csv`、调度队列恢复状态，不能凭语言记忆续跑。
- 每阶段至少交付一次可复用成果，不要只更新文档而不动代码或不开训练。

## 2. 官网协议与环境兼容，先做必要确认后直接实现

来源：
1. `real-stanford/diffusion_policy` 原始视觉 CNN-DP 工作区；
2. `NVlabs/mimicgen` 官方数据及环境；
3. IJRR 2026 `Equivariant diffusion policy for sample-efficient robotic manipulation` 50 保存点训练协议；
4. `mani-skill/ManiSkill/examples/baselines/diffusion_policy` 的 `baselines.sh` 与 `train_rgbd.py`；
5. ACT、robomimic BC-RNN、DP3 的官方实现；
6. DFormerv2 的 `GeoPriorGen`/`Decomposed_GSA` 与官方 TokenLearner。

核对任务名称、存储链接、示范数量、环境版本、相机键、深度单位、动作控制模式、仿真后端和环境成功定义。MimicGen `stack_three_d1/threading_d2/coffee_d2` 的官方注册 horizon 是 400；ManiSkill StackCube 官方视觉 DP 使用 200，PegInsertion 官方相关基线使用 300。

**特别说明：** 对 PegInsertionSide 的视觉 CNN-DP 没有一条官方已调优配置可直接照搬，采用 100k optimizer updates 是参考该任务官方状态 DP 与视觉 ACT 所定的本研究预算，必须在 `protocol_sources.md` 标注为「本文固定」，不能写成「官网规定」。

## 3. H200 资源并行调度（禁止全部串行）

服务器实际 GPU 数量、H200 可用显存、MIG 情况、CPU 核数、RAM、数据盘和 GPU 当前占用必须先通过工具获取，不得预设有多卡。

建两个持久化队列：`train_jobs`、`eval_jobs`。按 `(benchmark, task, method, seed, checkpoint)` 唯一标识任务；实现 CSV/SQLite job registry、status、重试和 resume 功能。训练 checkpoint 保存要使用 `tmp → fsync → atomic rename`，保存权重哈希和 metadata；评测只读取已完成、哈希正确、不可变的 checkpoint。

训练与评测**可以同时并行运行**：保存点产生后立即进入评测队列，在 GPU/CPU/模拟器有空余资源时启动独立 rollout 进程，不用等整组训练结束。若同一 H200 资源足够允许训练与评测并发，优先运行独立任务；若不够则自动调整同时运行的 job 数量，而不是减少 demo、epoch 或 episode。先采集每类作业稳定显存和 CPU/渲染需求，再设置并发上限，避免 OOM 和 EGL/PhysX 资源互相污染。支持 CPU 仿真并行和 GPU 策略批量推理。

训练并发吞吐图是辅助工程统计；**公平单次推理时延必须在独占 GPU、固定 batch、预热与同步条件下另测**。若只有 1 张 H200，不得报告虚假的「双卡并行」。所有 `CUDA_VISIBLE_DEVICES`, EGL 设备和实机 GPU UUID 必须日志可追溯。

## 4. 数据与对齐（正式数据，不做一堆无效 toy 小训练）

MimicGen：官方 Core 数据，单任务选固定 200 demos，保存按 ID 排序的 `subset_200.json`；额外数据效率 100 和 1000 demos 必须形成嵌套子集。通过官方 robomimic `dataset_states_to_obs.py --depth`/兼容渲染器从原始仿真状态重建逐帧 RGB-D。统一使用原版 DP 可用的 agent-view / eye-in-hand 相机配置，固定 84×84；对实际数据元数据中的相机名进行显式映射。仿真端在线 Depth 的数据单位、RGB/Depth 翻转、同帧一致性、有效像素掩码必须与训练相同。若需要绝对动作字段或控制转换，使用现有权威流程，不要静默从相对改成绝对动作。

ManiSkill：官方 motion-planning demos 每任务 100 条，调用官方轨迹 replay，输入原生 `rgb+depth` 或 `rgbd`，按脚本实际版本确认 RGB/Depth 值域和单位；保存与动作、状态同步的 RGB-D，记录 `use-env-states` 或 `use-first-env-state` 的选择及原因。StackCube 控制模式优先 `pd_ee_delta_pos`；PegInsertionSide 优先 `pd_ee_delta_pose`，必须以下载数据的元数据最终确认。使用官方 Gymnasium/ManiSkill eval API 评测。

数据生成需要多进程、可恢复、CRC/hash 验证、缓存与磁盘空间保护；同一任务 7 种策略共享一个完全相同的示范数据 manifest。测试前只做必需的观测/动作 shape/深度值域/梯度/闭环加载 smoke 检查一次；完成就进入正式训练。

## 5. 模型实现与公平比较

### 本文方法

GSA：根据 DFormerv2 的 Depth geometry prior，使用 ResNet18 中间层单层轻量分解式几何注意力 + residual `F_g = F + gamma*GSA(F,D)`，真实实现要记录与原论文差异；允许 config 关闭 depth prior 和普通 SA 替换。

TokenLearner：Softmax 空间权重、K=8 默认，聚合视觉 token 同时关联归一化位置 `(u,v)`、有效加权深度 `d` 与 `rho`；`d = Σ(pi*valid*D)/(Σ(pi*valid)+eps)`；Depth 无效时避免 nan；不同相机分别处理；将几何 token 经 projection 作为 observation condition 的增量，不改变 U-Net 主干。

### 核心全任务消融

`E0 RGB DP`, `E1 RGB-D 4ch DP`, `E3 GSA-only`, `E4 Geometry Token-only`, `E6 GSA + Geometry Token`：5 个任务 × 3 seeds 均需运行。

### 扩展三任务消融

`E2 RGB+plain SA`, `E5 GSA+vanilla TokenLearner`, `E7 RGB-D+plain SA`：MimicGen Threading D2、ManiSkill StackCube、PegInsertionSide；`-uv`, `-d`, `-rho`, `K=4/8/16`, GSA 插入层对比优先在 Threading 与 PegInsertion 两任务做。

### 主流竞争算法

RGB CNN-DP、RGB Transformer-DP、RGB ACT、RGB BC-RNN、同源深度生成点云 DP3、RGB-D GSC-DP，并额外将 E1 作为强 RGB-D 对照呈现在主表。

**不可为了强求所有网络超参数相同而篡改公开方法原本有效配置**：同任务共享示范轨迹、场景初始状态、episode horizon、成功定义和固定评测点/次数；观测步数、动作块长度、动作预测器/损失按各方法公开可复现配置，记录为独立字段。2026 IJRR 对比中 DP3/ACT/BC-RNN 的 chunk/action 控制设定并不完全一致。若对方法作了适配，列出原始配置、改动及原因，并避免使用额外的机器人真值特征。DP3 点云须由与 GSC 相同的 Depth 传感器和相机标定生成，不能调用完整真值 point cloud。

### 编码器

在 Threading D2、PegInsertionSide 比较 RGB-D ResNet18/34/50、RGB+SA、RGB+GSA、RGB-D+SA，并记录训练参数量、推理开销与闭环性能；保持 Conditional 1D U-Net、条件维度与训练预算一致。

## 6. 逐任务正式训练—保存—评测协议【严格执行】

| 任务 | 数据 | 训练预算 | checkpoint/rollout 频率 | 每点 rollout | 种子 |
|---|---|---|---|---|---|
| MimicGen `stack_three_d1` | 200 demos | 250 epochs | 5 epochs | 50 episodes | 0,1,2 |
| MimicGen `threading_d2` | 200 demos | 250 epochs | 5 epochs | 50 episodes | 0,1,2 |
| MimicGen `coffee_d2` | 200 demos | 250 epochs | 5 epochs | 50 episodes | 0,1,2 |
| ManiSkill `StackCube-v1` | 100 demos | 100000 optimizer updates | 5000 updates | 100 episodes | 0,1,2 |
| ManiSkill `PegInsertionSide-v1` | 100 demos | 100000 optimizer updates | 5000 updates | 100 episodes | 0,1,2 |

MimicGen 固定上述协议参考 IJRR 2026（`50000/Ndemo` 和 `1000/Ndemo`），50 episodes 为本文预注册的统一次数；ManiSkill 参考其视觉 DP `eval_freq=5000`, `num_eval_episodes=100`，PegInsertion 视觉 DP 100k 按官网相关方法选择。本章**每个方法**在同一任务都接受同样 checkpoint 时间坐标与 rollout episode 数，但模型具体训练实现可以尊重原始论文参数；如某模型原始训练是迭代式，须锁定与任务预算等量的优化更新或对应样本消费量、记录换算细节，不得虚报等量 epoch。

训练时按间隔存储每个 checkpoint，使用完整可恢复的 optimizer/EMA state；评测 worker **独立从磁盘读取**；允许异步评测但不得直接拿训练进程当前内存权重评测。相同任务的 reset_id 列表固定，跨模型、seed、保存点相同；MimicGen 官方 success、ManiSkill 主 `success_at_end`/辅 `success_once`。

每模型/任务/seed 计算：

`BEST = max(SR over scheduled checkpoints)`；`LAST10 = average(SR of last 10 scheduled checkpoints)`；跨 3 训练种子 `mean ± sample std`；同时输出每 50/100 回合成功的原始分子分母。报告模型间配对 episode 统计。不要引入额外“验证 rollout 场景 + 最终测试 rollout 场景”的强制三分法；但应如实写明 BEST 具有 winner's curse，不能宣称无偏。

### 数据效率

MimicGen 选 Stack Three D1 和 Threading D2：100 demos → 500 epochs、每10 epoch；200 demos → 250 epochs、每5 epoch；1000 demos → 50 epochs、每1 epoch。50 个周期评测点，每点 50 episodes，为 E0/E1/E6 三方法、3 seeds。

## 7. 论文图表不是训练后再补，必须先建立 schema

在**启动任何正式训练前**先建立 `thesis/figure_table_contract.yaml`，每条记录含：图/表 ID、科学问题、取样与指标公式、必需日志字段、GT 来源/策略输入隔离、脚本文件、输出路径、可复现状态。

全量必需产出：

- Table 3-1：五任务数据和评测协议，来源 manifest/config，不靠手打。
- Table 3-2：七方法主流比较（含 RGB-D E1），Best SR/Last-10 SR，per seed 三次统计。
- Table 3-3：E0-E7 消融，两个工作点交互作用；`interaction = SR_E6 - SR_E3 - SR_E4 + SR_E0`，标注它是交互效应不是因果证明。
- Table 3-4：ResNet18/34/50 及普通注意力/几何注意力，参数量、计算量、SR。
- Table 3-5：100/200/1000 demos 数据效率。
- Table 3-6：GSA 目标/背景区域实际注意力质量、特征相似度（必须有离线 instance GT）。
- Table 3-7：Token 区域中心、深度、无效比例与 GT 目标关联误差。
- Table 3-8：任务阶段空间误差、与成功率关系。
- Table 3-9：独占 GPU 时延、参数、峰值显存。
- Fig 3-1/2/3：本文整体架构、GSA、Token 几何聚合原理图（结构示意，不用模拟实验数）。
- Fig 3-4/5：主流算法成功率/消融成功率。
- Fig 3-6：Best/Last-10 以及随 epoch/update 的真实稳定性曲线。
- Fig 3-7：编码器对比与数据效率。
- Fig 3-8：真实 RGB-D + Query + depth prior + Decomposed GSA 轴向注意力图。
- Fig 3-9：真实 GSA 前后中间特征与区分度。
- Fig 3-10：真实 TokenLearner mask, `(u,v,d,rho)` 及对应相机图像。
- Fig 3-11：动作误差对比与 traj。
- Fig 3-12：同 reset ID 下 E0/E1/E6 成功失败成对案例图+视频。
- Fig 3-13：Depth 干预成功率/误差变化。
- Fig 3-14：速度-成功率与工程成本权衡。

每一张定量图/表必须有 `source_manifest`，追溯到 checkpoint SHA、episode JSONL、camera/reset/seed 及绘图脚本版本，输出 `csv + markdown + latex` 表格、`png + svg/pdf` 图片。所有标题带单位、指标定义、误差棒；失败示例的筛选依据也要可复现。无 GT 则标记 `unavailable(reason)`，禁止补假值。

**真正支撑方法故事的机制闭环**：深度先验改变注意力→更多目标相关视觉信息被保留（实际 instance GT/特征相似度）→Token 空间位置/深度与目标相关→物体/末端相对位姿误差变化→成功率改变。每个箭头都要有独立的度量，不能拿特征 norm 冒充 attention，也不能把 Token 热图当作对象监督分割，不能把相关性直接写成因果。支持同一 checkpoint 的 Depth shuffle / dropout / token depth masking 作为额外干预实验，且标明为非官网标准评测。

## 8. 运行目录、状态及质量门槛

项目建议结构：

```
GSC_DP_Thesis/
  task_plan.md
  findings.md
  progress.md
  configs/{benchmarks,methods,ablations}/
  data/{raw,processed,manifests}/
  gsc_dp/{vision,datasets,runners}/
  jobs/{queue.db,launch_jobs.py,monitor.py,resume.py}/
  checkpoints/{benchmark}/{task}/{method}/{seed}/
  eval/{benchmark}/{task}/{method}/{seed}/{checkpoint_step}/episodes.jsonl
  analysis/{gsa,token,motion,robustness}/
  thesis/{figure_table_contract.yaml,figures,tables,source_manifests}/
  docs/{protocol_sources.md,method_details.md,experiment_registry.md}
```

质量检查：

1. 验证所有轨迹的 `RGB/Depth/action/robot state` 帧长一致、深度单位固定、有效掩码无 NaN、训练/推理归一化一致、相机外参合法。
2. 每个训练 run 有且只有一条唯一配置与 manifest，写出固定预期 savepoint count；loss 和 checkpoint 可恢复；已经写好的文件不可无声覆盖。
3. 每个 checkpoint 对应恰好 N_eval 条 episode JSONL，且统计成功数/总数吻合；异步完成顺序不能影响 best/last10 计算顺序。
4. 模型对比没有遗漏 E1 RGB-D 强基线、没有把 DP3 的真值几何当输入、没有偷用 instance GT 标签指导 GSA/Token。
5. 每个图表可通过一个命令从保存的原始数据完整重建。论文中所有数字可自动追溯。

## 9. 排期与执行依赖（写入 task_plan）

Phase A：恢复/创建 planning files、H200 资源盘点、固定源码版本、锁定实验协议并写 source ledger。

Phase B：并行下载/生成 5 任务官方 RGB-D 示范与 environment adapters；在不更改数据意义前提下实现缓存和校验。

Phase C：实现 GSA + geometry TokenLearner + E0/E1/E3/E4/E6 参数化编码器；做一次必要的 shape、depth、gradient、checkpoint、eval api 核验。

Phase D：**尽早投入正式训练**，优先每个 benchmark 选一个任务并行启动 E0/E1/E6 三种子，其余按依赖和 GPU 资源排队，不等全部模块/可视化写完。训练产生 checkpoint 即可异步调度离线 rollout，持续落盘。

Phase E：加入完整主流模型 BC-RNN、ACT、DP-T、DP3；按 task/seed 主矩阵跑完。保持各方法原始合理配置与公开可追溯性。

Phase F：补充 E2/E5/E7、结构与编码器消融、数据效率，自动计算交互项。

Phase G：完成真实注意力/Token/运动误差/深度干预可视化，独占 GPU 时延，出第三章全部表图并写结论证据矩阵。

Phase H：审查 `figure_table_contract` 全项完成度；每个结果都能追溯；生成 `thesis/chapter3_results_for_writing.md`，填列真正获得的结果以及统计不确定性，列出未验证/负结果；提交代码 commit 与复现实验说明。

当独立任务没有阻塞时，**主动并行推进，不要要求我重复授权**。因缺失 SSH/GPU 权限/下载鉴权/未提供实际文件而无法操作时，准确记录 blocker 和必要的唯一操作请求，不得谎报已完成训练。

## 10. 每次向我报告进度的格式

用小表格报告：Phase、任务、方法、Seed、GPU UUID、当前 Epoch/Update、已完成 checkpoint 数/计划数、已完成 rollout 数/计划数、训练进程、最新真实 SR、日志路径、异常；附下一组自动执行队列。不要只给我审查建议。不要增加无意义的数次小训练。重视实验效率，但不能丢失任何论文需要的证据字段。

现在开始：优先按当前项目根目录读取 planning-with-files 的三个文件（若存在），完成服务器资源盘点、源码/数据锁定、图表字段契约；随后启动并行数据处理、模型实现与正式训练，按上述 Phase 的完成条件持续执行。
