# Findings

正式协议为唯一研究依据；服务器现有两项ManiSkill各1000条RGB-D、pd_joint_pos、128²双相机，固定前100条训练。官方DP/MimicGen/DFormer干净源码已下载；三项MimicGen Core正经hf-mirror并行下载。GPU2单卡绑定，CPU192、RAM available1.2TiB、磁盘2.2TiB。

时序Query权重使用真实轴向传播 Ah(query_y,key_y at query_x)*Aw(query_x,key_x at key_y)，按head平均，排除LEPE/残差，不能标作Full GSA。Token保留真实K图和uv/d/rho。E0/E1输入梯度显著性固定t50去噪输出能量探针，不称注意力。环境实际control_freq给出视频时间；阶段仅官方predicate或明确标注。独立analysis_jobs默认从E0/E1/E6相同保存点评测完成后触发，正式evaluate不存储注意力。
