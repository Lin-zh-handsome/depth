# 最终协议与代码来源

当前口径为四模型60次训练、300次正式评测；五任务、三种子、每run五个保存点。以用户最新明确要求、`configs/protocol.json`及`docs/four_model_protocol_update_20261015.md`为准。旧输入文档保留作历史来源，冲突规则不再生效。本次针对提交55951414的证据与修订见`docs/audit_55951414/REPORT.md`。

- CNN-DP：`source/diffusion_policy`，原始官方 `train_diffusion_unet_image_workspace.yaml`。动作一维 U-Net、FiLM、DDPM epsilon 损失和动作截取调用原文件。官方来源：https://github.com/real-stanford/diffusion_policy
- GSA：`source/DFormer/models/encoders/DFormerv2.py` 的 `DWConv2d/angle_transform/GeoPriorGen/Decomposed_GSA` 原算子提取到 `gsc_dp/dformer_ops.py`；保留 RoPE（旋转位置编码）和 LEPE（局部位置编码）。仅增加真实权重导出、最近邻深度重采样和无效深度对处理；外部 LayerNorm（层归一化）、gamma=0.1 单层残差接入，未使用完整分割主干。来源：https://github.com/VCIP-RGBD/DFormer
- TokenLearner：从现有 PyTorch（张量与神经网络框架）迁移实现复用 Softmax（空间归一化权重）聚合结构；本章字段是同权重 uv/d/rho。技术来源：https://github.com/google-research/scenic/tree/main/scenic/projects/token_learner 。现有两层 MLP（多层感知机）为端口适配，并不声称逐行复现 JAX（数值计算框架）代码。
- MimicGen：官方 Core 三任务链接和 400 步 horizon（回合步数上限）已查官方注册。https://github.com/NVlabs/mimicgen/blob/main/mimicgen/__init__.py 。状态数据以 hf-mirror 国内镜像下载，不使用旧 Can/Square 数据代替。
- ManiSkill：官方 RGB StackCube 100k 更新和 200 步、状态 Peg 100k 和 300 步；通用视觉 DP 每 5000 更新评测 100 回合。https://github.com/mani-skill/ManiSkill/blob/main/examples/baselines/diffusion_policy/baselines.sh 。Peg 视觉 CNN-DP 的 100k 是**本文固定预算**，不是官方已调优配置。
- ManiSkill原始motionplanning（运动规划示范）为`pd_joint_pos`（关节位置控制），经官方重放器转换为StackCube的`pd_ee_delta_pos`（末端位置增量）和Peg的`pd_ee_delta_pose`（末端位姿增量），双相机128×128。正式缓存仅使用转换后的动作/本体状态；旧关节控制缓存与结果保留在历史目录，不进入当前队列或统计。
- Peg的原始前100条轨迹全部标记成功；控制器转换后90条成功、10条失败，全部100条转换轨迹保留训练，不能表述为100条成功的末端控制示范。完整ID、回放标记及训练缓存区间见`docs/audit_55951414/peg_100_source_replay_cache.json`。
- 训练batch=64（批大小），全部既定示范进入训练，无额外验证集。每seed严格五点取最佳、并列最早，三seed用样本标准差；取消Last-10（末十次平均）及1710次旧安排。
- 按用户直接要求，不做权重哈希或重复版本核验；checkpoint（检查点）用临时文件、fsync（落盘同步）、原子改名和完成元数据控制读写。保留源代码 Git 提交、数据路径和逐回合证据。

MimicGen兼容环境：独立Conda `gsc-thesis-mimic`采用数据对应的robosuite 1.4.1，复用官方robomimic 0.4源码的Depth转换API。0.3版不具备所需Depth API，已改为0.4；不改变相对OSC_POSE（操作空间位姿控制）动作。其主成功率保留原始DP rollout中官方任务成功的max-reward（全回合最大奖励）口径，另外保存末步标志；ManiSkill主指标始终为末步成功。

三项MimicGen数据已完成转换，并通过18个真实保存状态、36组双相机RGB-D与本体/动作语义核对。剩余工作仅为当前四模型正式矩阵、已有图表与真实注意力/操作案例；不开展其他网络、效率、编码器、数据效率或第四章实验。未完成数值留空。

输入实现差异的如实说明：M0保持官方独立相机主干的初始化复制策略，M1/M2/M3分别构建各相机主干。所有模型同为随机初始化，但初始张量并非配对相等。MimicGen的84→76裁剪中，官方M0随机起点为0..7，自定义对齐裁剪为0..8；ManiSkill的128→112相应为0..15和0..16。裁剪尺寸及评测中心裁剪一致，M2/M3使用同一对齐裁剪。该现存实现差异明确披露，不通过悄悄修改已有训练/恢复的增强分布来抹平，也不据此宣称结果无效或自行重训。
