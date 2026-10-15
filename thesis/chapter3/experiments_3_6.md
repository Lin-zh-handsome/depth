# 第三章 3.6 实验结果
## 3.6.1 实验平台和评价指标
两个Benchmark、五任务、四方法、三种子；固定预算见table3_1.csv。Best为周期评测最大值，具有择优偏差；Best-of-5限定五个预注册位置，并列选最早；跨种子样本标准差ddof=1。

MimicGen主指标为success_once（在固定400步执行过程中至少一次达到官方成功条件），ManiSkill主指标为success_at_end（固定回合结束时满足官方成功条件）；两者均保留另一标志用于追溯，但不混写为统一末步成功率，也不跨基准计算单一平均成功率。每个任务内部四模型共享reset（重置）列表及评测回合数。主表和成功率源数据逐行标注success_definition（成功定义）。

PegInsertionSide-v1固定使用原始官方前100条运动规划示范，经官方pd_joint_pos（关节位置）至pd_ee_delta_pose（末端位姿增量）控制转换后，成功90条、失败10条；训练缓存保留全部100条转换轨迹，而非100条成功的末端控制示范。原始轨迹100条均标记成功；转换回放失败的原始轨迹编号为1、2、14、17、19、20、22、60、63、96。各模型/种子共用该既定缓存，无数据筛选或重训。完整来源和缓存区间见docs/audit_55951414/peg_100_source_replay_cache.json。

固定batch size（批大小）64、drop_last=False（保留末批）、无梯度累积。三个MimicGen任务实际250轮总更新数分别为Stack Three 193750、Threading 172000、Coffee 169000；两个ManiSkill任务固定100000次更新，详见table3_1.csv及experiments/ch3/dataset_budget_metadata.json。

四模型共用ResNet18主干结构、GroupNorm（组归一化）、同一一维扩散U-Net、DDPM（去噪扩散概率模型）和训练缓存。M0仅消费RGB与本体状态，M1/M2/M3另有几何深度输入。M2/M3的TokenLearner类、u/v/d/rho字段、8个Token及残差融合路径完全相同；隔离GSA后，真实输入上的特征及Token空间权重差值为0。M0沿用官方相机初始化复制和裁剪实现，改进模型为逐相机初始化及自定义对齐裁剪；官方M0的84→76裁剪起点为0..7，改进模型为0..8；128→112相应为0..15和0..16。评测中心裁剪相同。不宣称各模型初始权重或裁剪抽样端点相同，详见审查报告，既有训练保持原实现。
## 3.6.2 五任务成功率比较
TODO：60-run矩阵完整数据到齐后引用table3_2_best.csv。
## 3.6.3 GSA与TokenLearner递进式效果分析
TODO：module_deltas.csv。M0→M1包含Depth和GSA；M1→M2保持相同Depth/GSA。
## 3.6.4 空间注意力与时序关注可视化
TODO：独立checkpoint真实闭环轨迹、轴向GSA Query传播权重、8个Token空间权重；阶段名称来自环境事件或明确标注。
## 3.6.5 典型操作过程与失败案例
TODO：相同reset的M0/M1/M2/M3成功和失败轨迹；正式成功率评测不采集完整注意力张量。

四模型消融新增M3：与M2相同的几何关联TokenLearner、关闭GSA。主表和模块消融由自动导出真实结果更新，未完成保持TODO。M3-M0同时包含Depth与TokenLearner增量；M2-M3保持相同Depth/TokenLearner、比较GSA增量。
