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


## GitHub 发布完成 2026-10-13T22:27:14.850593+08:00
已成功推送至 https://github.com/Lin-zh-handsome/depth 的 main 分支。首次工程提交60a4272；包含代码、全部现有配置、论文材料、官方依赖子模块、真实训练/评测日志与队列快照。用户明确要求不上传权重；数据集本体与所有模型权重均排除。运行中的结果仅为采集时快照，不替代最终论文统计。

2026-10-13T16:09:08.254937+00:00 Job 176 eval StackCube-v1/e1/seed_0 finished, exit=0; logs/job_176.log

2026-10-13T16:09:08.708761+00:00 Job 196 eval threading_d2/e0/seed_0/point_5 launched PID=1259999, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=57651; logs/job_196.log

2026-10-13T17:31:14.233086+00:00 Job 177 eval PegInsertionSide-v1/e1/seed_0 finished, exit=0; logs/job_177.log

2026-10-13T17:31:14.512301+00:00 Job 197 eval stack_three_d1/e0/seed_0/point_5 launched PID=1499815, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=57679; logs/job_197.log

2026-10-13T17:48:00.301067+00:00 Job 97 train StackCube-v1/e3/seed_0/point_-1 launched PID=1548863, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=64583; logs/job_97.log

2026-10-13T18:01:11.268872+00:00 Job 196 eval threading_d2/e0/seed_0 finished, exit=0; logs/job_196.log

2026-10-13T18:01:12.052934+00:00 Job 199 eval threading_d2/e0/seed_0/point_10 launched PID=1588152, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=57543; logs/job_199.log

2026-10-13T18:23:32.307585+00:00 Job 100 train StackCube-v1/e4/seed_0/point_-1 launched PID=1653220, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=64499; logs/job_100.log

2026-10-13T19:11:45.725722+00:00 Job 197 eval stack_three_d1/e0/seed_0 finished, exit=0; logs/job_197.log

2026-10-13T19:11:45.906312+00:00 Job 201 eval stack_three_d1/e0/seed_0/point_10 launched PID=1795024, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=57569; logs/job_201.log

2026-10-13T19:36:35.520989+00:00 Job 199 eval threading_d2/e0/seed_0 finished, exit=0; logs/job_199.log

2026-10-13T19:36:36.137475+00:00 Job 202 eval threading_d2/e0/seed_0/point_15 launched PID=1867350, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=57535; logs/job_202.log

2026-10-13T20:45:00.828163+00:00 Job 201 eval stack_three_d1/e0/seed_0 finished, exit=0; logs/job_201.log

2026-10-13T20:45:00.991759+00:00 Job 203 eval stack_three_d1/e0/seed_0/point_15 launched PID=2067303, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=57569; logs/job_203.log

2026-10-13T21:09:52.626729+00:00 Job 202 eval threading_d2/e0/seed_0 finished, exit=0; logs/job_202.log

2026-10-13T21:09:52.904247+00:00 Job 206 eval threading_d2/e0/seed_0/point_20 launched PID=2139915, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=57535; logs/job_206.log

2026-10-13T22:18:21.826499+00:00 Job 203 eval stack_three_d1/e0/seed_0 finished, exit=0; logs/job_203.log

2026-10-13T22:18:22.557268+00:00 Job 207 eval stack_three_d1/e0/seed_0/point_20 launched PID=2341488, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=57569; logs/job_207.log

2026-10-13T22:43:14.364179+00:00 Job 206 eval threading_d2/e0/seed_0 finished, exit=0; logs/job_206.log

2026-10-13T22:43:15.132329+00:00 Job 208 eval threading_d2/e0/seed_0/point_25 launched PID=2414160, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=57535; logs/job_208.log

2026-10-13T23:52:17.781951+00:00 Job 207 eval stack_three_d1/e0/seed_0 finished, exit=0; logs/job_207.log

2026-10-13T23:52:18.561511+00:00 Job 211 eval stack_three_d1/e0/seed_0/point_25 launched PID=2616230, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=57569; logs/job_211.log

2026-10-14T00:16:11.283948+00:00 Job 208 eval threading_d2/e0/seed_0 finished, exit=0; logs/job_208.log

2026-10-14T00:16:11.844497+00:00 Job 212 eval threading_d2/e0/seed_0/point_30 launched PID=2687015, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=57535; logs/job_212.log

2026-10-14T01:25:48.977422+00:00 Job 211 eval stack_three_d1/e0/seed_0 finished, exit=0; logs/job_211.log

2026-10-14T01:25:49.137560+00:00 Job 213 eval stack_three_d1/e0/seed_0/point_30 launched PID=2897777, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=57569; logs/job_213.log

2026-10-14T01:49:07.320643+00:00 Job 212 eval threading_d2/e0/seed_0 finished, exit=0; logs/job_212.log

2026-10-14T01:49:07.504491+00:00 Job 214 eval threading_d2/e0/seed_0/point_35 launched PID=2971275, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=57535; logs/job_214.log


## 巡检与调度修复 2026-10-14T10:13:37.760554+08:00
实际训练完成2/162，运行8，等待152；完整保存点评测15，运行2，已生成等待122，已完成950回合。全部运行进程存活。StackCube/Peg E0 seed0均完成100000更新；Stack Three/Threading E0约192/216轮；RGB-D E1/GSC-DP E6约20.6k–21.1k更新；StackCube E3/E4约7.1k–7.5k。五任务数据清单全部就绪。修复评测跨benchmark直接比较epoch和update数值导致ManiSkill积压的问题，改按入队ID先到先评；同时修复接管MimicGen评测进程完成时误查update目录的问题。仅重启调度控制器，训练与评测工作进程保留。GPU2剩余约54GB，系统可用内存1.3TiB，/home剩余1.4TB；长期权重保存将持续占用磁盘，未删除数据或权重。时序视频尚未生成；主流其他模型和完整数据效率等尚未完成。

2026-10-14T02:13:38.142223+00:00 Dataset manifests available: PegInsertionSide-v1_100.json, StackCube-v1_100.json, coffee_d2_200.json, stack_three_d1_200.json, threading_d2_200.json. Runnable configs refreshed without reducing any budget.


## 用户停止训练 2026-10-14T10:54:53.623540+08:00
用户准备重新安排训练。每小时自动巡检已暂停。停止本工程调度器，设置持久用户暂停标记；全部未完成训练队列置paused。向本账号9个训练进程发送SIGTERM，其中本轮8个及历史训练1个；本轮训练将尝试保存recovery.pt后退出。已有权重和结果保留。正在核实退出与恢复检查点。现有评测允许完成，未启动新评测。

停止完成核实 2026-10-14T10:56:26.252120+08:00：本账号9个训练进程均已退出，当前训练进程为0；本轮8个训练均已生成停止后的恢复检查点。160个未完成训练队列已paused，2个训练完成结果保留。旧训练保留既有文件，未确认停止瞬间新恢复点。自动巡检已PAUSED，调度器已停止并增加持久用户暂停入口；已有评测进程状态为[{"id": 213, "pid": 2897777, "alive": false}, {"id": 214, "pid": 2971275, "alive": true}]。等待用户重新安排，不自动恢复训练。


## 2026-10-14 新45-run协议接管
已读取planning-with-files完整SKILL及执行包全部文件。此前暂停已由本次正式启动指令撤销。范围M0=e0、M1=e3、M2=e6；只保留五任务三种子。旧关节位置控制ManiSkill结果保留为历史，不能合并末端增量控制协议。GPU2独卡；可用显存143152MiB、RAM1.3TiB、/home可用1.3TiB。MimicGen M0两恢复点约200/230epochs可复用。新专用ch3_queue.db保留旧queue.db记录。哈希字段不重算，按用户要求使用真实配置、示范ID、源提交、原子保存元数据及逐reset日志溯源。
