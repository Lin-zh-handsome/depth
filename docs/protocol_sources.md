# 最终协议与代码来源

唯一依据为 `docs/inputs/GSC_DP_第三章最终实验协议.md`。

- CNN-DP：`source/diffusion_policy`，原始官方 `train_diffusion_unet_image_workspace.yaml`。动作一维 U-Net、FiLM、DDPM epsilon 损失和动作截取调用原文件。官方来源：https://github.com/real-stanford/diffusion_policy
- GSA：`source/DFormer/models/encoders/DFormerv2.py` 的 `DWConv2d/angle_transform/GeoPriorGen/Decomposed_GSA` 原算子提取到 `gsc_dp/dformer_ops.py`；保留 RoPE（旋转位置编码）和 LEPE（局部位置编码）。仅增加真实权重导出、最近邻深度重采样和无效深度对处理；外部 LayerNorm（层归一化）、gamma=0.1 单层残差接入，未使用完整分割主干。来源：https://github.com/VCIP-RGBD/DFormer
- TokenLearner：从现有 PyTorch（张量与神经网络框架）迁移实现复用 Softmax（空间归一化权重）聚合结构；本章字段是同权重 uv/d/rho。技术来源：https://github.com/google-research/scenic/tree/main/scenic/projects/token_learner 。现有两层 MLP（多层感知机）为端口适配，并不声称逐行复现 JAX（数值计算框架）代码。
- MimicGen：官方 Core 三任务链接和 400 步 horizon（回合步数上限）已查官方注册。https://github.com/NVlabs/mimicgen/blob/main/mimicgen/__init__.py 。状态数据以 hf-mirror 国内镜像下载，不使用旧 Can/Square 数据代替。
- ManiSkill：官方 RGB StackCube 100k 更新和 200 步、状态 Peg 100k 和 300 步；通用视觉 DP 每 5000 更新评测 100 回合。https://github.com/mani-skill/ManiSkill/blob/main/examples/baselines/diffusion_policy/baselines.sh 。Peg 视觉 CNN-DP 的 100k 是**本文固定预算**，不是官方已调优配置。
- 本次复用的 motionplanning（运动规划示范）元数据和 RGB-D 重放均为 `pd_joint_pos`（关节位置控制）、双相机 128×128。按最终协议允许的“实际元数据最终确认”保持动作不变；未改成末端增量控制。固定前100条实际轨迹 ID，所有方法和训练种子共用。
- 训练 batch=64（批大小）沿用所选官方 CNN-DP；全部100条进入训练。无额外验证回合划分；Best/LAST10 均来自固定周期独立评测。
- 按用户直接要求，不做权重哈希或重复版本核验；checkpoint（检查点）用临时文件、fsync（落盘同步）、原子改名和完成元数据控制读写。保留源代码 Git 提交、数据路径和逐回合证据。

MimicGen兼容环境：独立Conda `gsc-thesis-mimic`采用数据对应的robosuite 1.4.1，复用官方robomimic 0.4源码的Depth转换API。0.3版不具备所需Depth API，已改为0.4；不改变相对OSC_POSE（操作空间位姿控制）动作。其主成功率保留原始DP rollout中官方任务成功的max-reward（全回合最大奖励）口径，另外保存末步标志；ManiSkill主指标始终为末步成功。

待完成：MimicGen 数据转换；主流其他模型端口；完整结构与数据效率矩阵；机制 GT（真值）及真实视频；独占时延。没有真实结果时不生成假数。
