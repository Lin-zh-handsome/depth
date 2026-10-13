# Progress

2026-10-13：根据用户最新指令创建新protocol_v1规划，不继续旧规划。已读取三个附件全文，SSH连接和资源盘点完成；新协议工程campaign_v1 bootstrap PID4091209运行。
错误：本地GBK默认读取中文规划失败，改为显式UTF-8。

16:37：服务器提交28a1444，生成162训练任务、48可执行ManiSkill配置。scheduler PID4124932，E0 StackCube seed0 PID4125008，Peg seed0 PID4126518；Peg已1600update/loss0.0341679，峰值显存约8.16GB。评测Conda gsc-thesis-eval安装完成。新增G-T代码支持独立闭环注意力视频/关键帧/同reset三方法和自动分析队列；真实分析结果待新训练保存点。
错误：Stack Three hf-mirror下载curl18中断，保留727493813字节part文件断点续传，不重下已完成Threading/Coffee。

时序分析部署：c9884c7，独立采集/重导出/成对导出CLI已在gsc-thesis-eval加载成功。首次CLI受用户级accelerate污染ImportError影响，改为与worker一致的PYTHONNOUSERSITE=1后解决，未改旧环境。
正式队列资源更新：scheduler_v2 PID4159884，GPU2上E0/E1/E6×StackCube/Peg×seed0共6作业并行。E6 update100实际GSA/Token梯度：StackCube 0.0139133/4.25935e-5，Peg 0.00791827/1.57059e-4；证明真实训练中两几何分支已收到梯度。三项MimicGen Core均已下载完成（Stack恢复国内镜像续传成功），MimicGen独立Conda环境安装进行中。

新增时序任务最终实现：MimicGen/ManiSkill两类独立analysis_env，MimicGen按原始元数据创建1.4.1官方任务；源码GSA真实轴向传播Query导出、K权重及uv/d/rho、机器人状态与执行动作，MP4/PNG/JSON/NPZ完整导出。自动分析触发首个/最终保存点成对正式评测完成，不加入正式SR样本。当前尚无新协议E6指定保存点时序结果，保持pending actual artifacts。
Phase B继续实际RGB-D：官方200-demo Stack Three转换已完成68/200轨迹，物理EGL GPU2明确锁定；0.3缺少Depth API，独立环境恢复官方0.4兼容Depth转换，成功进入真实转换。
Phase D：首个StackCube E0 seed0 5000更新pt已原子保存，独立正式评测PID4190691实际闭环已14/100回合；不得把部分回合结果当最终SR。

2026-10-13 队列盘点：162训练、5940周期评测、369000回合。发现调度器被MimicGen manifest缺少control_mode中断；使用实际action_semantics字段恢复，已完成的评测通过eval_summary登记finished而不重复执行。现有6训练保留。

2026-10-13T13:48:22.068954+00:00 Dataset manifests available: PegInsertionSide-v1_100.json, StackCube-v1_100.json, coffee_d2_200.json, stack_three_d1_200.json, threading_d2_200.json. Runnable configs refreshed without reducing any budget.

2026-10-13T13:48:22.217748+00:00 Job 176 eval StackCube-v1/e1/seed_0/point_5000 launched PID=843518, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=77746; logs/job_176.log

2026-10-13T13:48:52.626250+00:00 Job 177 eval PegInsertionSide-v1/e1/seed_0/point_5000 launched PID=845167, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=75280; logs/job_177.log

2026-10-13T13:49:22.814360+00:00 Job 1 train stack_three_d1/e0/seed_0/point_-1 launched PID=846882, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=72814; logs/job_1.log

2026-10-13T13:49:53.048272+00:00 Job 28 train threading_d2/e0/seed_0/point_-1 launched PID=848487, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=64115; logs/job_28.log


## GitHub 工程发布准备 2026-10-13T22:24:55.496485+08:00
用户指定 Lin-zh-handsome/depth。整理全部工程代码、配置、论文材料、真实日志与评测轨迹快照；排除数据集本体。单个模型检查点约5.3GB，超过普通GitHub Git单文件限制，保留服务器路径清单。训练评测持续运行；GitHub推送结果待记录。
