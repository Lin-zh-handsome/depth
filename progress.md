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

2026-10-14T03:34:46.928070+00:00 Dataset manifests available: PegInsertionSide-v1_100.json, StackCube-v1_100.json, coffee_d2_200.json, stack_three_d1_200.json, threading_d2_200.json. Runnable configs refreshed without reducing any budget.

2026-10-14T03:34:47.150526+00:00 Job 52 eval stack_three_d1/e0/seed_0/point_35 launched PID=3329385, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=143152; logs/ch3_job_52.log

2026-10-14T03:35:17.687840+00:00 Job 53 eval stack_three_d1/e0/seed_0/point_40 launched PID=3331302, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=139777; logs/ch3_job_53.log

2026-10-14T03:35:48.618006+00:00 Job 10 train threading_d2/e6/seed_0/point_-1 launched PID=3332790, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=137306; logs/ch3_job_10.log

2026-10-14T03:36:19.285797+00:00 Job 11 train threading_d2/e6/seed_1/point_-1 launched PID=3334281, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=128406; logs/ch3_job_11.log

2026-10-14T03:36:50.247743+00:00 Job 13 train threading_d2/e3/seed_0/point_-1 launched PID=3336087, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=119507; logs/ch3_job_13.log

2026-10-14T03:37:20.723819+00:00 Job 14 train threading_d2/e3/seed_1/point_-1 launched PID=3337903, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=110645; logs/ch3_job_14.log

2026-10-14T03:37:51.179433+00:00 Job 16 train threading_d2/e0/seed_0/point_-1 launched PID=3339537, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=101781; logs/ch3_job_16.log

2026-10-14T03:38:21.660162+00:00 Job 17 train threading_d2/e0/seed_1/point_-1 launched PID=3341194, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=96136; logs/ch3_job_17.log

2026-10-14T03:38:51.958697+00:00 Job 16 train threading_d2/e0/seed_0 queued, exit=1; logs/ch3_job_16.log

2026-10-14T03:38:52.218531+00:00 Job 16 train threading_d2/e0/seed_0/point_-1 launched PID=3343109, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=93082; logs/ch3_job_16.log

2026-10-14T03:39:52.768834+00:00 Job 16 train threading_d2/e0/seed_0 failed, exit=1; logs/ch3_job_16.log

2026-10-14T03:39:52.910842+00:00 Job 18 train threading_d2/e0/seed_2/point_-1 launched PID=3346517, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=93082; logs/ch3_job_18.log


## 用户暂停本次GPU2训练 2026-10-14T03:50:24.925544+00:00
已设置持久暂停标记，停止调度器，向6个本次GPU2训练发送SIGTERM保存恢复点。GPU5明确排除。现有独立评测/数据转换未收到停止信号。训练退出待确认。


停止已确认：本次GPU2的6个训练进程均退出，6个recovery.pt完整文件已保存。持久暂停标记阻止重新调度。GPU2已有2项评测和1项官方数据转换继续。GPU5当前无计算进程；其seed42旧训练PID3245588在上一轮收敛45-run范围时已收到SIGTERM，本次停止指令未向GPU5发送信号。


## 最终225评测协议接管
45训练、225评测、15750回合；取消Last10和旧1710队列。MimicGen50/100/150/200/250，ManiSkill20k/40k/60k/80k/100k；并列最佳选最早位置。正式训练继续只用GPU2，GPU5不操作。旧35/40epoch评测停止保留部分日志，全部旧结果仅精确五位置可合并。修复M0恢复后normalizer留CPU问题；checkpoint保留best+latest及有界临时快照。用户禁止冗余哈希，因此字段留空并记录元数据溯源。

2026-10-14T04:06:03.404400+00:00 Dataset manifests available: PegInsertionSide-v1_100.json, StackCube-v1_100.json, coffee_d2_200.json, stack_three_d1_200.json, threading_d2_200.json. Runnable configs refreshed without reducing any budget.

2026-10-14T04:06:04.085945+00:00 Job 76 eval stack_three_d1/e0/seed_0/point_50 launched PID=3430198, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=142249; logs/final_job_76.log

2026-10-14T04:06:35.424720+00:00 Job 77 eval stack_three_d1/e0/seed_0/point_100 launched PID=3431847, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=139777; logs/final_job_77.log

2026-10-14T04:07:07.086585+00:00 Job 10 train threading_d2/e6/seed_0/point_-1 launched PID=3433612, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=137306; logs/final_job_10.log

2026-10-14T04:07:39.477225+00:00 Job 11 train threading_d2/e6/seed_1/point_-1 launched PID=3435319, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=131638; logs/final_job_11.log

2026-10-14T04:08:11.064225+00:00 Job 13 train threading_d2/e3/seed_0/point_-1 launched PID=3436999, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=122629; logs/final_job_13.log

2026-10-14T04:08:42.443201+00:00 Job 14 train threading_d2/e3/seed_1/point_-1 launched PID=3439300, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=113639; logs/final_job_14.log

2026-10-14T04:09:14.814227+00:00 Job 16 train threading_d2/e0/seed_0/point_-1 launched PID=3441539, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=104666; logs/final_job_16.log


## 实际运行状态（自动更新）
2026-10-14T04:09:16.323754+00:00
45训练、225正式评测。{"train": {"queued": 40, "running": 5}, "eval": {"queued": 223, "running": 2}, "analysis": {}}；完整回合 0。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T04:09:46.513577+00:00 Job 17 train threading_d2/e0/seed_1/point_-1 launched PID=3443211, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=95696; logs/final_job_17.log


## 实际运行状态（自动更新）
2026-10-14T04:09:48.441108+00:00
45训练、225正式评测。{"train": {"queued": 39, "running": 6}, "eval": {"queued": 223, "running": 2}, "analysis": {}}；完整回合 0。全部工作只用物理GPU2。队列入队不等于实验完成。


## 最终协议正式执行 2026-10-14T12:10:33.001532+08:00
已部署提交6416b92/ab5f0f8；45训练225正式评测15750回合清单已实查通过。只计算五指定位置Best-of-5，并列选最早位置；三个seed均值和样本标准差。旧35/40轮评测已停止，其部分日志和旧1710清单归档保留，不参与新统计。GPU2单卡实际启动，调度器PID3430126；GPU5及独立seed42任务明确不操作。运行状态 [["eval", "queued", 223], ["eval", "running", 2], ["train", "queued", 39], ["train", "running", 6]]。
实际进程 [{"id": 10, "kind": "train", "task": "threading_d2", "method": "e6", "seed": 0, "pid": 3433612}, {"id": 11, "kind": "train", "task": "threading_d2", "method": "e6", "seed": 1, "pid": 3435319}, {"id": 13, "kind": "train", "task": "threading_d2", "method": "e3", "seed": 0, "pid": 3436999}, {"id": 14, "kind": "train", "task": "threading_d2", "method": "e3", "seed": 1, "pid": 3439300}, {"id": 16, "kind": "train", "task": "threading_d2", "method": "e0", "seed": 0, "pid": 3441539}, {"id": 17, "kind": "train", "task": "threading_d2", "method": "e0", "seed": 1, "pid": 3443211}, {"id": 76, "kind": "eval", "task": "stack_three_d1", "method": "e0", "seed": 0, "pid": 3430198}, {"id": 77, "kind": "eval", "task": "stack_three_d1", "method": "e0", "seed": 0, "pid": 3431847}]
M2 Threading种子0/1已从294/273更新恢复，均已实际到300更新并记录有限loss。M1两种子从255/241更新恢复。M0种子0从158383更新恢复，当前因4个新协议旧保存点等待评测而回压，未重新训练。MimicGen已有两项M0恢复权重复用；目前新协议完整评测DONE=0，不引用旧非五位置成功率。PegInsertionSide100条pd_ee_delta_pose RGB-D转换完成；StackCube转换仍在运行，manifest完成后自动放行。每小时巡检gsc-dp已ACTIVE并使用ch3_final_queue.db。
新权重预计约100GB、建议预留150GB，旧权重和数据另计。best/latest/临时快照回收代码已部署；真实回收尚待第一个完整正式评测，不能称已验证完成。最新完整恢复文件随必要恢复点原子替换；长期只保留best。正式evaluate不采集注意力，三方法五点完成后独立best轨迹分析导出至thesis/chapter3。
恢复命令：cd /home/linzhenghong/project/gsc_dp_chapter3/campaign_v1 && PYTHONNOUSERSITE=1 nohup /home/linzhenghong/miniconda3/envs/gsc-robodiff/bin/python jobs/scheduler.py > logs/final_scheduler.log 2>&1 &

2026-10-14T04:23:07.858571+00:00 Dataset manifests available: PegInsertionSide-v1_100.json, StackCube-v1_100.json, coffee_d2_200.json, stack_three_d1_200.json, threading_d2_200.json. Runnable configs refreshed without reducing any budget.


## 每小时实际巡检 2026-10-14T13:00:53.031961+08:00
新45训练/225正式评测协议继续执行；暂停标记不存在，最终启动指令已记录撤销此前暂停。6训练、2正式评测进程均存活且CUDA_VISIBLE_DEVICES绑定物理GPU2 UUID；未操作GPU5或独立seed42。Threading M2种子0/1与M1种子0/1均已推进约1400更新、2轮，最近loss有限；M0种子1已推进13700更新、约19轮；M0种子0等待4个合法旧保存点评测，属于有界快照回压，未误判死锁。Stack Three M0种子0的50/100轮评测当前约43/41回合，仍未达到完整50回合，不能计正式DONE或SR。两项ManiSkill末端增量控制数据转换已完成，五任务manifest就绪，配置已自动刷新为45项。GPU2空余约85GB，内存可用1.2TiB，磁盘空余约1.3TB；当前无异常修复需求。真实巡检明细 experiments/ch3/monitoring_manifest.json；完整正式评测仍0/225。


## 实际运行状态（自动更新）
2026-10-14T05:08:15.320121+00:00
45训练、225正式评测。{"train": {"queued": 39, "running": 6}, "eval": {"queued": 223, "finished": 1, "running": 1}, "analysis": {}}；完整回合 50。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T05:08:47.977628+00:00 Job 76 eval stack_three_d1/e0/seed_0 finished, exit=0; logs/final_job_76.log

2026-10-14T05:08:48.248388+00:00 Job 78 eval stack_three_d1/e0/seed_0/point_150 launched PID=3631017, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=89591; logs/final_job_78.log


## 实际运行状态（自动更新）
2026-10-14T05:08:49.515548+00:00
45训练、225正式评测。{"train": {"queued": 39, "running": 6}, "eval": {"queued": 222, "finished": 1, "running": 2}, "analysis": {}}；完整回合 50。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T05:09:51.585779+00:00 Job 77 eval stack_three_d1/e0/seed_0 finished, exit=0; logs/final_job_77.log

2026-10-14T05:09:51.879000+00:00 Job 79 eval stack_three_d1/e0/seed_0/point_200 launched PID=3634251, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=89591; logs/final_job_79.log


## 实际运行状态（自动更新）
2026-10-14T05:10:00.716021+00:00
45训练、225正式评测。{"train": {"queued": 39, "running": 6}, "eval": {"queued": 221, "finished": 2, "running": 2}, "analysis": {}}；完整回合 100。全部工作只用物理GPU2。队列入队不等于实验完成。


## 每小时实际巡检 2026-10-14T14:08:47.225581+08:00
正式评测已完成2/225个保存点，共100完整回合。Stack Three M0 seed0第50轮14/50=28%，第100轮21/50=42%；两个reset集合完整。当前暂时best保存为100轮，best.pt和完整recovery.pt均存在。自动逐文件回收已执行38个失效/已评快照，释放200254889836字节（约200GB），每项记录于checkpoint_cleanup.jsonl；未执行新的手工删除。当前6训练和2评测实际进程存活且GPU2绑定正确；Threading四组M1/M2较上次增长约1500–1600更新，M0种子1增长约1.54万更新；M0种子0等待合法保存点评测属于预期回压。GPU2空余约85GB，RAM可用约1.2TiB，磁盘空余约1.5TB；无新的失败/非有限loss。thesis/chapter3真实结果已增量导出，不把当前2点暂时最佳当作最终五点/三种子统计。

2026-10-14T06:11:58.775280+00:00 Job 78 eval stack_three_d1/e0/seed_0 finished, exit=0; logs/final_job_78.log

2026-10-14T06:11:59.401561+00:00 Job 121 eval threading_d2/e0/seed_0/point_50 launched PID=3830414, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=89591; logs/final_job_121.log


## 实际运行状态（自动更新）
2026-10-14T06:12:09.853718+00:00
45训练、225正式评测。{"train": {"queued": 39, "running": 6}, "eval": {"queued": 220, "finished": 3, "running": 2}, "analysis": {}}；完整回合 150。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T06:12:42.552562+00:00 Job 79 eval stack_three_d1/e0/seed_0 finished, exit=0; logs/final_job_79.log

2026-10-14T06:12:43.114803+00:00 Job 122 eval threading_d2/e0/seed_0/point_100 launched PID=3832760, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=89625; logs/final_job_122.log


## 实际运行状态（自动更新）
2026-10-14T06:12:45.006309+00:00
45训练、225正式评测。{"train": {"queued": 39, "running": 6}, "eval": {"queued": 219, "finished": 4, "running": 2}, "analysis": {}}；完整回合 200。全部工作只用物理GPU2。队列入队不等于实验完成。


## 巡检备注保留修复 2026-10-14T15:06:01.203105+08:00
发现jobs/export_ch3.py更新task_plan/findings时直接截断自动状态标题后的全部内容，造成后续巡检备注消失。已改为仅替换自动状态章节、保留下一个Markdown标题后的内容；从已提交的1dde8dc/b112f58恢复缺失巡检备注4项。导出程序由调度器逐轮新进程加载，无需重启训练、评测或调度器。


## 每小时巡检 2026-10-14T15:07:34.168016+08:00
完整正式评测5/225，共250回合；新增：stack_three_d1/e0/seed0/150: 26/50=52%; stack_three_d1/e0/seed0/200: 22/50=44%; threading_d2/e0/seed0/100: 2/50=4%。队列[{"kind": "eval", "status": "finished", "count": 5}, {"kind": "eval", "status": "queued", "count": 219}, {"kind": "eval", "status": "running", "count": 1}, {"kind": "train", "status": "queued", "count": 39}, {"kind": "train", "status": "running", "count": 6}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。本轮修复规划状态导出截断后续备注的问题，已恢复4项历史巡检备注，工作进程无需重启。

2026-10-14T07:07:38.620726+00:00 Job 122 eval threading_d2/e0/seed_0 finished, exit=0; logs/final_job_122.log

2026-10-14T07:07:39.413976+00:00 Job 123 eval threading_d2/e0/seed_0/point_150 launched PID=4007389, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=89701; logs/final_job_123.log


## 实际运行状态（自动更新）
2026-10-14T07:07:49.033348+00:00
45训练、225正式评测。{"train": {"queued": 39, "running": 6}, "eval": {"queued": 218, "finished": 6, "running": 1}, "analysis": {}}；完整回合 300。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T07:08:20.669997+00:00 Job 121 eval threading_d2/e0/seed_0 finished, exit=0; logs/final_job_121.log

2026-10-14T07:08:21.441504+00:00 Job 124 eval threading_d2/e0/seed_0/point_200 launched PID=4009559, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=89625; logs/final_job_124.log


## 实际运行状态（自动更新）
2026-10-14T07:08:22.873893+00:00
45训练、225正式评测。{"train": {"queued": 39, "running": 6}, "eval": {"queued": 217, "finished": 6, "running": 2}, "analysis": {}}；完整回合 300。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T08:00:13.563577+00:00 Job 123 eval threading_d2/e0/seed_0 finished, exit=0; logs/final_job_123.log

2026-10-14T08:00:13.835375+00:00 Job 126 eval threading_d2/e0/seed_1/point_50 launched PID=4177936, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=89626; logs/final_job_126.log


## 实际运行状态（自动更新）
2026-10-14T08:00:15.555056+00:00
45训练、225正式评测。{"train": {"queued": 39, "running": 6}, "eval": {"queued": 216, "finished": 7, "running": 2}, "analysis": {}}；完整回合 350。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T08:00:48.322479+00:00 Job 124 eval threading_d2/e0/seed_0 finished, exit=0; logs/final_job_124.log


## 实际运行状态（自动更新）
2026-10-14T08:00:50.735721+00:00
45训练、225正式评测。{"train": {"queued": 39, "running": 6}, "eval": {"queued": 216, "finished": 8, "running": 1}, "analysis": {}}；完整回合 400。全部工作只用物理GPU2。队列入队不等于实验完成。


## 每小时巡检 2026-10-14T16:04:33.642804+08:00
完整正式评测8/225，共400回合；新增：threading_d2/e0/seed0/50: 6/50=12%; threading_d2/e0/seed0/150: 6/50=12%; threading_d2/e0/seed0/200: 4/50=8%。队列[{"kind": "eval", "status": "finished", "count": 8}, {"kind": "eval", "status": "queued", "count": 216}, {"kind": "eval", "status": "running", "count": 1}, {"kind": "train", "status": "queued", "count": 39}, {"kind": "train", "status": "running", "count": 6}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。

2026-10-14T08:45:10.414159+00:00 Job 126 eval threading_d2/e0/seed_1 finished, exit=0; logs/final_job_126.log


## 实际运行状态（自动更新）
2026-10-14T08:45:16.059088+00:00
45训练、225正式评测。{"train": {"queued": 39, "running": 6}, "eval": {"queued": 216, "finished": 9}, "analysis": {}}；完整回合 450。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T08:50:38.652057+00:00 Job 16 train threading_d2/e0/seed_0 finished, exit=0; logs/final_job_16.log

2026-10-14T08:50:39.425067+00:00 Job 125 eval threading_d2/e0/seed_0/point_250 launched PID=146144, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=97708; logs/final_job_125.log


## 实际运行状态（自动更新）
2026-10-14T08:50:41.424223+00:00
45训练、225正式评测。{"train": {"queued": 39, "running": 5, "finished": 1}, "eval": {"queued": 215, "finished": 9, "running": 1}, "analysis": {}}；完整回合 450。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T08:51:11.882672+00:00 Job 18 train threading_d2/e0/seed_2/point_-1 launched PID=147818, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=95271; logs/final_job_18.log


## 实际运行状态（自动更新）
2026-10-14T08:51:13.660808+00:00
45训练、225正式评测。{"train": {"queued": 38, "running": 6, "finished": 1}, "eval": {"queued": 215, "finished": 9, "running": 1}, "analysis": {}}；完整回合 450。全部工作只用物理GPU2。队列入队不等于实验完成。


## 每小时巡检 2026-10-14T17:02:57.075907+08:00
完整正式评测9/225，共450回合；新增：threading_d2/e0/seed1/50: 2/50=4%。队列[{"kind": "eval", "status": "finished", "count": 9}, {"kind": "eval", "status": "queued", "count": 215}, {"kind": "eval", "status": "running", "count": 1}, {"kind": "train", "status": "finished", "count": 1}, {"kind": "train", "status": "queued", "count": 38}, {"kind": "train", "status": "running", "count": 6}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。

2026-10-14T09:44:48.001661+00:00 Job 125 eval threading_d2/e0/seed_0 finished, exit=0; logs/final_job_125.log


## 实际运行状态（自动更新）
2026-10-14T09:44:50.731524+00:00
45训练、225正式评测。{"train": {"queued": 38, "running": 6, "finished": 1}, "eval": {"queued": 215, "finished": 10}, "analysis": {}}；完整回合 500。全部工作只用物理GPU2。队列入队不等于实验完成。


## 每小时巡检 2026-10-14T18:02:01.328847+08:00
完整正式评测10/225，共500回合；新增：threading_d2/e0/seed0/250: 5/50=10%。队列[{"kind": "eval", "status": "finished", "count": 10}, {"kind": "eval", "status": "queued", "count": 215}, {"kind": "train", "status": "finished", "count": 1}, {"kind": "train", "status": "queued", "count": 38}, {"kind": "train", "status": "running", "count": 6}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。


## 用户改为按任务串行推进 2026-10-14T18:32:46.777107+08:00
当前Threading为唯一可启动训练/正式评测的任务。同任务内三模型三种子可并行，M2优先；必须9项训练和45次正式评测全部完成后，才切换PegInsertionSide、Stack Three、Coffee、StackCube。修正此前表述：一个任务共45次正式评测，不是15次。其余任务保持已入队，已有结果和权重保留；不改变训练预算、五个位置和每点回合数。仅重启调度器，六个现有Threading训练进程不停止。GPU5不操作。
