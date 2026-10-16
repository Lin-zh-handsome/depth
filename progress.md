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

2026-10-14T10:32:46.995425+00:00 Dataset manifests available: PegInsertionSide-v1_100.json, StackCube-v1_100.json, coffee_d2_200.json, stack_three_d1_200.json, threading_d2_200.json. Runnable configs refreshed without reducing any budget.

2026-10-14T10:32:46.996855+00:00 Sequential task scheduling: active task threading_d2. Switch only after all 9 training runs and 45 evaluations finish.


## 裁剪同步瓶颈修复 2026-10-14T18:42:51.635821+08:00
M1/M2逐张裁剪使用CUDA标量作为Python slice边界，单相机128观测触发1536次aten::item和本地标量读取，实际单次操作约1.047秒。批量gather裁剪无标量读取，约0.080秒；相同随机状态下RGB/Depth/valid输出及RGB梯度完全相同。仅修复执行路径，无参数或科学协议变化。这是运行瓶颈诊断，不是论文效率对比。四个M1/M2训练均SIGTERM原子保存恢复点后部署等价裁剪；M0、GPU5及其他任务未停止。55小时只是旧慢速外推，修复后重新按实际训练日志估算。证据logs/crop_diagnosis.json、docs/crop_optimization_restart.json。

2026-10-14T10:42:51.941378+00:00 Dataset manifests available: PegInsertionSide-v1_100.json, StackCube-v1_100.json, coffee_d2_200.json, stack_three_d1_200.json, threading_d2_200.json. Runnable configs refreshed without reducing any budget.

2026-10-14T10:42:51.942289+00:00 Sequential task scheduling: active task threading_d2. Switch only after all 9 training runs and 45 evaluations finish.

2026-10-14T10:42:52.090681+00:00 Job 10 train threading_d2/e6/seed_0/point_-1 launched PID=489094, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=125299; logs/final_job_10.log


## 实际运行状态（自动更新）
2026-10-14T10:42:53.619843+00:00
45训练、225正式评测。{"train": {"queued": 41, "running": 3, "finished": 1}, "eval": {"queued": 215, "finished": 10}, "analysis": {}}；完整回合 500。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T10:43:23.955195+00:00 Job 11 train threading_d2/e6/seed_1/point_-1 launched PID=490507, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=119632; logs/final_job_11.log


## 实际运行状态（自动更新）
2026-10-14T10:43:25.814340+00:00
45训练、225正式评测。{"train": {"queued": 40, "running": 4, "finished": 1}, "eval": {"queued": 215, "finished": 10}, "analysis": {}}；完整回合 500。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T10:43:56.130811+00:00 Job 13 train threading_d2/e3/seed_0/point_-1 launched PID=492122, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=110622; logs/final_job_13.log


## 实际运行状态（自动更新）
2026-10-14T10:43:57.735000+00:00
45训练、225正式评测。{"train": {"queued": 39, "running": 5, "finished": 1}, "eval": {"queued": 215, "finished": 10}, "analysis": {}}；完整回合 500。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T10:44:28.410743+00:00 Job 14 train threading_d2/e3/seed_1/point_-1 launched PID=493550, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=101633; logs/final_job_14.log


## 实际运行状态（自动更新）
2026-10-14T10:44:29.904687+00:00
45训练、225正式评测。{"train": {"queued": 38, "running": 6, "finished": 1}, "eval": {"queued": 215, "finished": 10}, "analysis": {}}；完整回合 500。全部工作只用物理GPU2。队列入队不等于实验完成。


## 裁剪修复后实际训练进展 2026-10-14T18:45:38.046049+08:00
四项M1/M2已从12730/12697/12803/12703更新完整恢复，无重训和预算改动。短窗口实际速率 [{"method": "e3", "seed": 0, "pid": 492122, "updates_measured": 100, "seconds": 23.97092366218567, "updates_per_hour": 15018.194754334936, "full_250epochs_hours": 11.45277463859982, "latest_loss": 0.052587706595659256}, {"method": "e6", "seed": 0, "pid": 489094, "updates_measured": 400, "seconds": 83.71960353851318, "updates_per_hour": 17200.27256624027, "full_250epochs_hours": 9.999841533766851, "latest_loss": 0.05722839757800102}, {"method": "e6", "seed": 1, "pid": 490507, "updates_measured": 300, "seconds": 65.39141297340393, "updates_per_hour": 16515.93001116613, "full_250epochs_hours": 10.414187992060626, "latest_loss": 0.05358270928263664}]。旧55小时及其整套4–6周估计基于已修复的慢速路径，应作废；新的耗时以更长实际训练区间持续校正。

2026-10-14T10:49:17.281357+00:00 Job 127 eval threading_d2/e0/seed_1/point_100 launched PID=507057, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=88729; logs/final_job_127.log


## 实际运行状态（自动更新）
2026-10-14T10:49:18.521291+00:00
45训练、225正式评测。{"train": {"queued": 38, "running": 6, "finished": 1}, "eval": {"queued": 214, "finished": 10, "running": 1}, "analysis": {}}；完整回合 500。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T10:55:47.152461+00:00 Dataset manifests available: PegInsertionSide-v1_100.json, StackCube-v1_100.json, coffee_d2_200.json, stack_three_d1_200.json, threading_d2_200.json. Runnable configs refreshed without reducing any budget.

2026-10-14T10:55:47.153648+00:00 Sequential task scheduling: active task threading_d2. Switch only after all 9 training runs and 45 evaluations finish.


## 实际运行状态（自动更新）
2026-10-14T10:55:48.798390+00:00
45训练、225正式评测。{"train": {"queued": 38, "running": 1, "held_for_full_method": 5, "finished": 1}, "eval": {"queued": 214, "finished": 10, "held_for_full_method": 1}, "analysis": {}}；完整回合 500。全部工作只用物理GPU2。队列入队不等于实验完成。


## 优先完整方法已生效 2026-10-14T18:56:16.539637+08:00
当前只运行Threading M2 seed0 PID489094及其五点评测；五个其他训练均在SIGTERM后写出完整最新恢复文件并退出，M0 seed1评测保留部分回合。M0等待评测时的停止分支保存恢复点但不打印recoverable stop，已按退出状态和停止后原子恢复文件时间确认，不重复停止或重训。focus_scheduler PID524143。M2依次完成种子0/1/2，各250轮及5次50回合，随后恢复当前任务其他模型。held_for_full_method为用户指定等待，不是失败。GPU5不操作。


## M2三个种子优先并行 2026-10-14T19:01:38.212412+08:00
用户撤销独占串行训练，要求并行但先完成M2所有实验。当前任务Threading的M2种子0/1/2最多三训练并行，正式评测最多两进程；三个种子均250轮及五点评测共15点评测完成后，才恢复M1/M0。仍保持当前任务9训练45评测全部完成后再换任务，不跨任务。M2种子0现有进程保留，种子1从暂停恢复文件续训，种子2新启动完整预算。M1/M0继续held_for_full_method；GPU5不操作。

2026-10-14T11:01:38.535129+00:00 Dataset manifests available: PegInsertionSide-v1_100.json, StackCube-v1_100.json, coffee_d2_200.json, stack_three_d1_200.json, threading_d2_200.json. Runnable configs refreshed without reducing any budget.

2026-10-14T11:01:38.537905+00:00 Sequential task scheduling: active task threading_d2. Switch only after all 9 training runs and 45 evaluations finish.

2026-10-14T11:01:38.860744+00:00 Job 11 train threading_d2/e6/seed_1/point_-1 launched PID=542763, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=133999; logs/final_job_11.log


## 实际运行状态（自动更新）
2026-10-14T11:01:40.089547+00:00
45训练、225正式评测。{"train": {"queued": 38, "running": 2, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 214, "finished": 10, "held_for_full_method": 1}, "analysis": {}}；完整回合 500。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T11:02:10.881003+00:00 Job 12 train threading_d2/e6/seed_2/point_-1 launched PID=544213, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=124989; logs/final_job_12.log


## 实际运行状态（自动更新）
2026-10-14T11:02:12.342810+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 214, "finished": 10, "held_for_full_method": 1}, "analysis": {}}；完整回合 500。全部工作只用物理GPU2。队列入队不等于实验完成。


## 每小时巡检 2026-10-14T19:02:30.956908+08:00
完整正式评测10/225，共500回合；新增：无。队列[{"kind": "eval", "status": "finished", "count": 10}, {"kind": "eval", "status": "held_for_full_method", "count": 1}, {"kind": "eval", "status": "queued", "count": 214}, {"kind": "train", "status": "finished", "count": 1}, {"kind": "train", "status": "held_for_full_method", "count": 4}, {"kind": "train", "status": "queued", "count": 37}, {"kind": "train", "status": "running", "count": 3}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。


## GPU2负载目标 2026-10-14T19:06:28.202659+08:00
用户希望GPU利用率约70%。增加独立运行时负载控制器，按NVML滚动读数自适应占空比，仅短时暂停/继续本账号本工程绑定GPU2的训练评测进程；保持M2三种子并行优先，不改模型、批量、训练更新数、随机状态或评测回合。目标为65–75%附近的平均利用率，瞬时读数允许波动；GPU5和其他用户进程完全排除。配置jobs/gpu_load_target.json，状态jobs/gpu_load_state.json。目标限载会增加墙钟时间，后续耗时需重新按实际进度估计。

2026-10-14T11:56:36.011531+00:00 Job 91 eval threading_d2/e6/seed_0/point_50 launched PID=708025, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=115824; logs/final_job_91.log


## 实际运行状态（自动更新）
2026-10-14T11:56:37.980836+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 213, "finished": 10, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 500。全部工作只用物理GPU2。队列入队不等于实验完成。


## 每小时巡检 2026-10-14T20:04:34.667278+08:00
完整正式评测10/225，共500回合；新增：无。队列[{"kind": "eval", "status": "finished", "count": 10}, {"kind": "eval", "status": "held_for_full_method", "count": 1}, {"kind": "eval", "status": "queued", "count": 213}, {"kind": "eval", "status": "running", "count": 1}, {"kind": "train", "status": "finished", "count": 1}, {"kind": "train", "status": "held_for_full_method", "count": 4}, {"kind": "train", "status": "queued", "count": 37}, {"kind": "train", "status": "running", "count": 3}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。


## 首个M2正式评测已启动 2026-10-14T20:04:34.667278+08:00
Threading M2 seed0到达第50完整dataset epoch/34400更新，已原子保存磁盘推理快照并独立评测（PID708025，本次巡检7/50回合）；训练等待该点完整评测是预定回压，不是卡死。seed1约49轮，seed2约27轮，有限loss且更新数增长。M2尚无完整正式评测成绩，不汇报部分SR。GPU2近期平均利用率约68.9%，瞬时读数可达100%；负载控制器持续工作。M1/M0有意等待，GPU5不操作。

2026-10-14T12:07:47.530179+00:00 Job 96 eval threading_d2/e6/seed_1/point_50 launched PID=743236, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=113396; logs/final_job_96.log


## 实际运行状态（自动更新）
2026-10-14T12:07:49.262090+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 212, "finished": 10, "running": 2, "held_for_full_method": 1}, "analysis": {}}；完整回合 500。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T13:01:38.693715+00:00 Job 91 eval threading_d2/e6/seed_0 finished, exit=0; logs/final_job_91.log


## 实际运行状态（自动更新）
2026-10-14T13:01:43.044486+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 212, "finished": 11, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 550。全部工作只用物理GPU2。队列入队不等于实验完成。


## 每小时巡检 2026-10-14T21:09:33.618620+08:00
完整正式评测11/225，共550回合；新增：threading_d2/e6/seed0/50: 5/50=10%。队列[{"kind": "eval", "status": "finished", "count": 11}, {"kind": "eval", "status": "held_for_full_method", "count": 1}, {"kind": "eval", "status": "queued", "count": 212}, {"kind": "eval", "status": "running", "count": 1}, {"kind": "train", "status": "finished", "count": 1}, {"kind": "train", "status": "held_for_full_method", "count": 4}, {"kind": "train", "status": "queued", "count": 37}, {"kind": "train", "status": "running", "count": 3}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。


## 首个M2完整正式评测 2026-10-14T21:09:33.618620+08:00
Threading M2种子0第50轮完成固定50回合真实闭环评测，5/50=10%，reset列表完整且唯一。best/best.pt及元数据已真实保留，种子0继续约52轮训练。种子1第50轮评测47/50回合，其训练等待评测为预定回压；种子2约49轮。未完成五点和三种子，10%只能标为第50轮SR，不能称最终Best-of-5或方法报告值。GPU2近期平均约70.1%，限载正常。总正式评测11/225、完整550回合，三项M2持续推进；M1/M0有意等待，其他任务与GPU5不操作。

2026-10-14T13:11:21.268604+00:00 Job 101 eval threading_d2/e6/seed_2/point_50 launched PID=945338, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=113396; logs/final_job_101.log


## 实际运行状态（自动更新）
2026-10-14T13:11:22.732343+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 211, "finished": 11, "running": 2, "held_for_full_method": 1}, "analysis": {}}；完整回合 550。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T13:12:24.729251+00:00 Job 96 eval threading_d2/e6/seed_1 finished, exit=0; logs/final_job_96.log


## 实际运行状态（自动更新）
2026-10-14T13:12:28.955891+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 211, "finished": 12, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 600。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T14:06:15.890546+00:00 Job 101 eval threading_d2/e6/seed_2 finished, exit=0; logs/final_job_101.log


## 实际运行状态（自动更新）
2026-10-14T14:06:20.355130+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 211, "finished": 13, "held_for_full_method": 1}, "analysis": {}}；完整回合 650。全部工作只用物理GPU2。队列入队不等于实验完成。


## 每小时巡检 2026-10-14T22:11:25.152002+08:00
完整正式评测13/225，共650回合；新增：threading_d2/e6/seed1/50: 5/50=10%; threading_d2/e6/seed2/50: 6/50=12%。队列[{"kind": "eval", "status": "finished", "count": 13}, {"kind": "eval", "status": "held_for_full_method", "count": 1}, {"kind": "eval", "status": "queued", "count": 211}, {"kind": "train", "status": "finished", "count": 1}, {"kind": "train", "status": "held_for_full_method", "count": 4}, {"kind": "train", "status": "queued", "count": 37}, {"kind": "train", "status": "running", "count": 3}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。


## M2三个种子首点评测齐全 2026-10-14T22:11:25.152002+08:00
Threading M2第50轮三个种子均完成固定50回合：seed0=5/50(10%)、seed1=5/50(10%)、seed2=6/50(12%)；各best文件真实存在，保留该阶段原始回合及源数据。当前训练进度分别约75/70/52轮，三进程存活、有限loss、GPU2绑定正确。M2正式评测完成3/15，总完成13/225(650完整回合)。后续100/150/200/250轮尚未完成，不计算最终Best-of-5或三seed方法报告值。GPU2近期平均约71.0%，限载正常；M1/M0仍按用户要求等待，无异常。

2026-10-14T15:08:06.070466+00:00 Job 92 eval threading_d2/e6/seed_0/point_100 launched PID=1265148, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=115824; logs/final_job_92.log


## 实际运行状态（自动更新）
2026-10-14T15:08:07.328921+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 210, "finished": 13, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 650。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T15:20:51.292036+00:00 Job 97 eval threading_d2/e6/seed_1/point_100 launched PID=1300429, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=113396; logs/final_job_97.log


## 实际运行状态（自动更新）
2026-10-14T15:20:52.884611+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 209, "finished": 13, "running": 2, "held_for_full_method": 1}, "analysis": {}}；完整回合 650。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T16:11:24.162971+00:00 Job 92 eval threading_d2/e6/seed_0 finished, exit=0; logs/final_job_92.log


## 实际运行状态（自动更新）
2026-10-14T16:11:26.276286+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 209, "finished": 14, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 700。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T16:14:08.982182+00:00 Job 102 eval threading_d2/e6/seed_2/point_100 launched PID=1446349, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=113396; logs/final_job_102.log


## 实际运行状态（自动更新）
2026-10-14T16:14:10.705715+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 208, "finished": 14, "running": 2, "held_for_full_method": 1}, "analysis": {}}；完整回合 700。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T16:26:21.081373+00:00 Job 97 eval threading_d2/e6/seed_1 finished, exit=0; logs/final_job_97.log


## 实际运行状态（自动更新）
2026-10-14T16:26:23.144182+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 208, "finished": 15, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 750。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T17:08:42.086392+00:00 Job 102 eval threading_d2/e6/seed_2 finished, exit=0; logs/final_job_102.log


## 实际运行状态（自动更新）
2026-10-14T17:08:46.780820+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 208, "finished": 16, "held_for_full_method": 1}, "analysis": {}}；完整回合 800。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T18:21:11.143918+00:00 Job 93 eval threading_d2/e6/seed_0/point_150 launched PID=1791490, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=115824; logs/final_job_93.log


## 实际运行状态（自动更新）
2026-10-14T18:21:13.108637+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 207, "finished": 16, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 800。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T18:33:58.123823+00:00 Job 98 eval threading_d2/e6/seed_1/point_150 launched PID=1827389, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=113396; logs/final_job_98.log


## 实际运行状态（自动更新）
2026-10-14T18:33:59.955801+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 206, "finished": 16, "running": 2, "held_for_full_method": 1}, "analysis": {}}；完整回合 800。全部工作只用物理GPU2。队列入队不等于实验完成。


## 实际运行状态（自动更新）
2026-10-14T19:21:21.512823+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 206, "finished": 17, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 850。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T19:21:53.160826+00:00 Job 93 eval threading_d2/e6/seed_0 finished, exit=0; logs/final_job_93.log

2026-10-14T19:21:53.335461+00:00 Job 103 eval threading_d2/e6/seed_2/point_150 launched PID=1957807, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=113396; logs/final_job_103.log


## 实际运行状态（自动更新）
2026-10-14T19:21:54.517505+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 205, "finished": 17, "running": 2, "held_for_full_method": 1}, "analysis": {}}；完整回合 850。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T19:37:10.916112+00:00 Job 98 eval threading_d2/e6/seed_1 finished, exit=0; logs/final_job_98.log


## 实际运行状态（自动更新）
2026-10-14T19:37:16.057355+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 205, "finished": 18, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 900。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T20:15:28.295756+00:00 Job 103 eval threading_d2/e6/seed_2 finished, exit=0; logs/final_job_103.log


## 实际运行状态（自动更新）
2026-10-14T20:15:30.688402+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 205, "finished": 19, "held_for_full_method": 1}, "analysis": {}}；完整回合 950。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T21:30:35.920886+00:00 Job 94 eval threading_d2/e6/seed_0/point_200 launched PID=2309289, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=115824; logs/final_job_94.log


## 实际运行状态（自动更新）
2026-10-14T21:30:37.517253+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 204, "finished": 19, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 950。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T21:47:03.453510+00:00 Job 99 eval threading_d2/e6/seed_1/point_200 launched PID=2352427, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=113396; logs/final_job_99.log


## 实际运行状态（自动更新）
2026-10-14T21:47:05.098276+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 203, "finished": 19, "running": 2, "held_for_full_method": 1}, "analysis": {}}；完整回合 950。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T22:30:37.667359+00:00 Job 94 eval threading_d2/e6/seed_0 finished, exit=0; logs/final_job_94.log

2026-10-14T22:30:37.854400+00:00 Job 104 eval threading_d2/e6/seed_2/point_200 launched PID=2464606, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=113396; logs/final_job_104.log


## 实际运行状态（自动更新）
2026-10-14T22:30:40.077431+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 202, "finished": 20, "running": 2, "held_for_full_method": 1}, "analysis": {}}；完整回合 1000。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T22:49:57.962623+00:00 Job 99 eval threading_d2/e6/seed_1 finished, exit=0; logs/final_job_99.log


## 实际运行状态（自动更新）
2026-10-14T22:50:00.187396+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 202, "finished": 21, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 1050。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-14T23:29:45.950970+00:00 Job 104 eval threading_d2/e6/seed_2 finished, exit=0; logs/final_job_104.log


## 实际运行状态（自动更新）
2026-10-14T23:29:51.842936+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 202, "finished": 22, "held_for_full_method": 1}, "analysis": {}}；完整回合 1100。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T00:35:58.731748+00:00 Job 95 eval threading_d2/e6/seed_0/point_250 launched PID=2789098, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=115824; logs/final_job_95.log


## 实际运行状态（自动更新）
2026-10-15T00:36:00.667664+00:00
45训练、225正式评测。{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 201, "finished": 22, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 1100。全部工作只用物理GPU2。队列入队不等于实验完成。


## 实际运行状态（自动更新）
2026-10-15T00:36:32.975872+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 2, "running": 2, "held_for_full_method": 4}, "eval": {"queued": 201, "finished": 22, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 1100。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T00:49:57.841414+00:00 Job 11 train threading_d2/e6/seed_1 finished, exit=0; logs/final_job_11.log

2026-10-15T00:49:58.034532+00:00 Job 100 eval threading_d2/e6/seed_1/point_250 launched PID=2824210, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=131692; logs/final_job_100.log


## 实际运行状态（自动更新）
2026-10-15T00:50:00.104076+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 3, "running": 1, "held_for_full_method": 4}, "eval": {"queued": 200, "finished": 22, "running": 2, "held_for_full_method": 1}, "analysis": {}}；完整回合 1100。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T01:38:47.310255+00:00 Job 95 eval threading_d2/e6/seed_0 finished, exit=0; logs/final_job_95.log


## 实际运行状态（自动更新）
2026-10-15T01:38:50.745114+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 3, "running": 1, "held_for_full_method": 4}, "eval": {"queued": 200, "finished": 23, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 1150。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T01:44:12.638216+00:00 Job 12 train threading_d2/e6/seed_2 finished, exit=0; logs/final_job_12.log

2026-10-15T01:44:13.475591+00:00 Job 105 eval threading_d2/e6/seed_2/point_250 launched PID=2978166, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=140959; logs/final_job_105.log


## 实际运行状态（自动更新）
2026-10-15T01:44:15.411817+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "held_for_full_method": 4}, "eval": {"queued": 199, "finished": 23, "running": 2, "held_for_full_method": 1}, "analysis": {}}；完整回合 1150。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T01:47:58.238212+00:00 Job 100 eval threading_d2/e6/seed_1 finished, exit=0; logs/final_job_100.log


## 实际运行状态（自动更新）
2026-10-15T01:48:01.290001+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "held_for_full_method": 4}, "eval": {"queued": 199, "finished": 24, "running": 1, "held_for_full_method": 1}, "analysis": {}}；完整回合 1200。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T02:09:29.411716+00:00 Job 105 eval threading_d2/e6/seed_2 finished, exit=0; logs/final_job_105.log

2026-10-15T02:09:29.414286+00:00 Full method three seeds and 15 scheduled evaluations completed; resume remaining work of the current task.

2026-10-15T02:09:30.120537+00:00 Job 127 eval threading_d2/e0/seed_1/point_100 launched PID=3057878, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=143152; logs/final_job_127.log


## 实际运行状态（自动更新）
2026-10-15T02:09:33.268383+00:00
45训练、225正式评测。{"train": {"queued": 41, "finished": 4}, "eval": {"queued": 199, "finished": 25, "running": 1}, "analysis": {}}；完整回合 1250。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T02:10:05.623791+00:00 Job 13 train threading_d2/e3/seed_0/point_-1 launched PID=3059587, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=140966; logs/final_job_13.log


## 实际运行状态（自动更新）
2026-10-15T02:10:07.548949+00:00
45训练、225正式评测。{"train": {"queued": 40, "finished": 4, "running": 1}, "eval": {"queued": 199, "finished": 25, "running": 1}, "analysis": {}}；完整回合 1250。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T02:10:38.142454+00:00 Job 14 train threading_d2/e3/seed_1/point_-1 launched PID=3061295, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=135063; logs/final_job_14.log


## 实际运行状态（自动更新）
2026-10-15T02:10:40.146568+00:00
45训练、225正式评测。{"train": {"queued": 39, "finished": 4, "running": 2}, "eval": {"queued": 199, "finished": 25, "running": 1}, "analysis": {}}；完整回合 1250。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T02:11:10.539382+00:00 Job 17 train threading_d2/e0/seed_1/point_-1 launched PID=3062877, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=129416; logs/final_job_17.log


## 实际运行状态（自动更新）
2026-10-15T02:11:12.494526+00:00
45训练、225正式评测。{"train": {"queued": 38, "finished": 4, "running": 3}, "eval": {"queued": 199, "finished": 25, "running": 1}, "analysis": {}}；完整回合 1250。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T02:11:43.232293+00:00 Job 18 train threading_d2/e0/seed_2/point_-1 launched PID=3065502, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=117066; logs/final_job_18.log


## 实际运行状态（自动更新）
2026-10-15T02:11:44.904468+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 199, "finished": 25, "running": 1}, "analysis": {}}；完整回合 1250。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T02:14:57.362295+00:00 Job 131 eval threading_d2/e0/seed_2/point_50 launched PID=3080105, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=107867; logs/final_job_131.log


## 实际运行状态（自动更新）
2026-10-15T02:14:58.558993+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 198, "finished": 25, "running": 2}, "analysis": {}}；完整回合 1250。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T03:29:13.553564+00:00 Job 127 eval threading_d2/e0/seed_1 finished, exit=0; logs/final_job_127.log


## 实际运行状态（自动更新）
2026-10-15T03:29:19.982361+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 198, "finished": 26, "running": 1}, "analysis": {}}；完整回合 1300。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T03:41:41.342981+00:00 Job 131 eval threading_d2/e0/seed_2 finished, exit=0; logs/final_job_131.log


## 实际运行状态（自动更新）
2026-10-15T03:41:47.304122+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 198, "finished": 27}, "analysis": {}}；完整回合 1350。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T03:45:35.963744+00:00 Job 106 eval threading_d2/e3/seed_0/point_50 launched PID=3375510, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=107026; logs/final_job_106.log


## 实际运行状态（自动更新）
2026-10-15T03:45:37.960930+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 197, "finished": 27, "running": 1}, "analysis": {}}；完整回合 1350。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T03:47:13.420889+00:00 Job 111 eval threading_d2/e3/seed_1/point_50 launched PID=3380197, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=104589; logs/final_job_111.log


## 实际运行状态（自动更新）
2026-10-15T03:47:15.435524+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 196, "finished": 27, "running": 2}, "analysis": {}}；完整回合 1350。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T05:01:30.782365+00:00 Job 106 eval threading_d2/e3/seed_0 finished, exit=0; logs/final_job_106.log


## 实际运行状态（自动更新）
2026-10-15T05:01:36.523077+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 196, "finished": 28, "running": 1}, "analysis": {}}；完整回合 1400。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T05:05:23.610621+00:00 Job 111 eval threading_d2/e3/seed_1 finished, exit=0; logs/final_job_111.log


## 实际运行状态（自动更新）
2026-10-15T05:05:29.350217+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 196, "finished": 29}, "analysis": {}}；完整回合 1450。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T06:15:36.238018+00:00 Job 128 eval threading_d2/e0/seed_1/point_150 launched PID=3903708, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=107026; logs/final_job_128.log


## 实际运行状态（自动更新）
2026-10-15T06:15:37.723714+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 195, "finished": 29, "running": 1}, "analysis": {}}；完整回合 1450。全部工作只用物理GPU2。队列入队不等于实验完成。


## 每小时巡检 2026-10-15T14:43:28.453143+08:00
完整正式评测29/225，共1450回合；新增：threading_d2/e6/seed0/100: 5/50=10%; threading_d2/e6/seed0/150: 7/50=14%; threading_d2/e6/seed0/200: 6/50=12%; threading_d2/e6/seed0/250: 4/50=8%; threading_d2/e6/seed1/100: 5/50=10%; threading_d2/e6/seed1/150: 8/50=16%; threading_d2/e6/seed1/200: 5/50=10%; threading_d2/e6/seed1/250: 5/50=10%; threading_d2/e6/seed2/100: 9/50=18%; threading_d2/e6/seed2/150: 3/50=6%; threading_d2/e6/seed2/200: 11/50=22%; threading_d2/e6/seed2/250: 11/50=22%; threading_d2/e3/seed0/50: 1/50=2%; threading_d2/e3/seed1/50: 2/50=4%; threading_d2/e0/seed1/100: 4/50=8%; threading_d2/e0/seed2/50: 2/50=4%。队列[{"kind": "eval", "status": "finished", "count": 29}, {"kind": "eval", "status": "queued", "count": 195}, {"kind": "eval", "status": "running", "count": 1}, {"kind": "train", "status": "finished", "count": 4}, {"kind": "train", "status": "queued", "count": 37}, {"kind": "train", "status": "running", "count": 4}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。


## M2全部完成及后续恢复巡检 2026-10-15T14:43:28.453143+08:00
Threading M2三个种子250轮和15次正式评测全部完成，五点评测最佳依次14%/16%/22%，均值17.3333%、样本标准差4.1633个百分点；best推理权重保留，结果由真实逐回合数据汇总。焦点配置已自动completed，Threading M0/M1已正常恢复，符合用户最新指令，不是误解除等待。当前M1种子0/1约86/83轮，M0种子1到150轮并评测20/50回合，种子2约98轮；四项训练和一项正式评测存活，未发现失败。整体4/45训练、29/225正式评测完成，1450完整回合。M1种子2尚排队，仍不跨任务。GPU2近期平均约70.3%，限载正常，GPU5不操作。完整结果已在本对话用户查询时报告，不将部分评测计作完成。

2026-10-15T06:52:33.471665+00:00 Job 132 eval threading_d2/e0/seed_2/point_100 launched PID=4014788, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=104589; logs/final_job_132.log


## 实际运行状态（自动更新）
2026-10-15T06:52:35.428475+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 194, "finished": 29, "running": 2}, "analysis": {}}；完整回合 1450。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T07:29:57.526651+00:00 Job 128 eval threading_d2/e0/seed_1 finished, exit=0; logs/final_job_128.log

2026-10-15T07:29:57.706206+00:00 Job 107 eval threading_d2/e3/seed_0/point_100 launched PID=4123986, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=104589; logs/final_job_107.log


## 实际运行状态（自动更新）
2026-10-15T07:30:02.688187+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 193, "finished": 30, "running": 2}, "analysis": {}}；完整回合 1500。全部工作只用物理GPU2。队列入队不等于实验完成。


## 每小时巡检 2026-10-15T15:44:00.510504+08:00
完整正式评测30/225，共1500回合；新增：threading_d2/e0/seed1/150: 5/50=10%。队列[{"kind": "eval", "status": "finished", "count": 30}, {"kind": "eval", "status": "queued", "count": 193}, {"kind": "eval", "status": "running", "count": 2}, {"kind": "train", "status": "finished", "count": 4}, {"kind": "train", "status": "queued", "count": 37}, {"kind": "train", "status": "running", "count": 4}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。


## 每小时推进确认 2026-10-15T15:44:00.510504+08:00
新增Threading M0 seed1第150轮完整正式评测5/50=10%，精确reset列表通过。整体正式评测30/225、1500完整回合，训练完成4/45；四项M0/M1训练和两项正式评测仍在运行。M1 seed0到100轮等待评测(8/50回合)、seed1约97轮；M0 seed1约153轮、seed2到100轮等待评测(31/50回合)。等待是预定回压，不是卡死，无失败或非有限loss。M2三种子已完整完成，最终17.3333%±4.1633%保持不变；不对未完M0/M1计算最终均值。GPU2近期平均约68.9%，限载正常；只推进Threading，不影响GPU5。

2026-10-15T08:08:27.177560+00:00 Job 132 eval threading_d2/e0/seed_2 finished, exit=0; logs/final_job_132.log

2026-10-15T08:08:27.331906+00:00 Job 112 eval threading_d2/e3/seed_1/point_100 launched PID=47374, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=104589; logs/final_job_112.log


## 实际运行状态（自动更新）
2026-10-15T08:08:29.583871+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 192, "finished": 31, "running": 2}, "analysis": {}}；完整回合 1550。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T08:44:32.631349+00:00 Job 107 eval threading_d2/e3/seed_0 finished, exit=0; logs/final_job_107.log


## 实际运行状态（自动更新）
2026-10-15T08:44:38.904767+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 192, "finished": 32, "running": 1}, "analysis": {}}；完整回合 1600。全部工作只用物理GPU2。队列入队不等于实验完成。


## 每小时巡检 2026-10-15T16:48:34.158612+08:00
完整正式评测32/225，共1600回合；新增：threading_d2/e3/seed0/100: 3/50=6%; threading_d2/e0/seed2/100: 2/50=4%。队列[{"kind": "eval", "status": "finished", "count": 32}, {"kind": "eval", "status": "queued", "count": 192}, {"kind": "eval", "status": "running", "count": 1}, {"kind": "train", "status": "finished", "count": 4}, {"kind": "train", "status": "queued", "count": 37}, {"kind": "train", "status": "running", "count": 4}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。


## 新增完整评测与运行确认 2026-10-15T16:48:34.158612+08:00
本小时新增Threading M1 seed0第100轮3/50=6%，M0 seed2第100轮2/50=4%；均完成固定50回合且reset列表完整。累计32/225正式评测、1600完整回合，训练4/45完成。M1种子0已约101轮、种子1到100轮等待评测(27/50回合)；M0种子1约167轮、种子2约110轮。四训练和一评测进程存活且GPU2绑定正确，等待为既定回压，无失败或非有限loss。GPU2近期平均约71.0%，限载正常；未跨任务，GPU5不操作。M0/M1尚未完整三种子五点，不能将当前单点评测写为最终方法结果。

2026-10-15T09:17:21.964271+00:00 Job 112 eval threading_d2/e3/seed_1 finished, exit=0; logs/final_job_112.log


## 实际运行状态（自动更新）
2026-10-15T09:17:27.021594+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 192, "finished": 33}, "analysis": {}}；完整回合 1650。全部工作只用物理GPU2。队列入队不等于实验完成。


## 每小时巡检 2026-10-15T17:47:30.163411+08:00
完整正式评测33/225，共1650回合；新增：threading_d2/e3/seed1/100: 4/50=8%。队列[{"kind": "eval", "status": "finished", "count": 33}, {"kind": "eval", "status": "queued", "count": 192}, {"kind": "train", "status": "finished", "count": 4}, {"kind": "train", "status": "queued", "count": 37}, {"kind": "train", "status": "running", "count": 4}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。


## 当前训练与负载巡检 2026-10-15T17:47:30.163411+08:00
新增Threading M1 seed1第100轮完整正式评测4/50=8%，固定reset列表完整。正式评测累计33/225、1650完整回合，训练完成4/45。M1种子0/1约119/109轮，M0种子1/2约184/130轮；四项训练实际增长且loss有限，目前没有就绪的运行中评测，等待下一指定保存点是正常状态。无异常、无跨任务；GPU2近期平均约73.4%，限载控制正常，GPU5不操作。所有未完成模型的阶段成功率保留真实结果，不提前计算三种子最终统计。

2026-10-15T10:33:05.857285+00:00 Job 129 eval threading_d2/e0/seed_1/point_200 launched PID=453202, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=107026; logs/final_job_129.log


## 实际运行状态（自动更新）
2026-10-15T10:33:07.413681+00:00
45训练、225正式评测。{"train": {"queued": 37, "finished": 4, "running": 4}, "eval": {"queued": 191, "finished": 33, "running": 1}, "analysis": {}}；完整回合 1650。全部工作只用物理GPU2。队列入队不等于实验完成。


## 实际运行状态（自动更新）
2026-10-15T10:37:54.363891+00:00
60训练、300正式评测。{"train": {"queued": 52, "finished": 4, "running": 4}, "eval": {"queued": 266, "finished": 33, "running": 1}, "analysis": {}}；完整回合 1650。全部工作只用物理GPU2。队列入队不等于实验完成。


## 四模型正式协议生效 2026-10-15T18:37:57.370028+08:00
用户新增M3=CNN-DP+Geometry-associated TokenLearner，不启用GSA，直接复用M2相同DepthTokenLearner类、8个token、同权重(u,v,d,rho)与投影残差融合。新包附件未发现，明确按本轮用户指令执行。原45训练225正式评测的ID、数据库与实际状态保留，只追加M3的15训练75评测；总计60训练300评测21000回合。沿用既定训练预算、每run五次正式评测、Best-of-5与低存储规则。不重新训练旧合规模型。每任务变为12训练60正式评测，全部完成才换任务；仍先Threading，只用GPU2，平均利用率目标70%，GPU5不操作。M2已完成，原M0/M1工作进程保持运行，新增M3按空闲队列立即正式调度。四模型主表、模块消融及M1-M0/M3-M0/M2-M1/M2-M3/M2-M0增量、成功率曲线与真实可视化已更新。无GSA的M3只展示真实TokenLearner权重，不伪称GSA注意力。证据docs/m3_migration_report.json、docs/m3_structure_consistency.json。

2026-10-15T10:37:57.718869+00:00 Dataset manifests available: PegInsertionSide-v1_100.json, StackCube-v1_100.json, coffee_d2_200.json, stack_three_d1_200.json, threading_d2_200.json. Runnable configs refreshed without reducing any budget.

2026-10-15T10:37:57.719817+00:00 Sequential task scheduling: active task threading_d2. Switch only after all 12 training runs and 60 evaluations finish.

2026-10-15T10:37:58.288229+00:00 Job 274 train threading_d2/m3/seed_0/point_-1 launched PID=467460, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=104589; logs/final_job_274.log


## 实际运行状态（自动更新）
2026-10-15T10:37:59.849648+00:00
60训练、300正式评测。{"train": {"queued": 51, "finished": 4, "running": 5}, "eval": {"queued": 266, "finished": 33, "running": 1}, "analysis": {}}；完整回合 1650。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T10:38:30.685941+00:00 Job 275 train threading_d2/m3/seed_1/point_-1 launched PID=469064, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=95849; logs/final_job_275.log


## 实际运行状态（自动更新）
2026-10-15T10:38:32.705044+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 4, "running": 6}, "eval": {"queued": 266, "finished": 33, "running": 1}, "analysis": {}}；完整回合 1650。全部工作只用物理GPU2。队列入队不等于实验完成。


## Four-model formal execution 2026-10-15T18:42:27+08:00
M3 reuses the exact M2 Geometry-associated TokenLearner and geometry processing, with GSA removed. Preserved original 45 training / 225 evaluation event identities; appended only 15 training / 75 evaluation events. Threading M3 launch state: [{'id': 274, 'seed': 0, 'status': 'running', 'pid': 467460}, {'id': 275, 'seed': 1, 'status': 'running', 'pid': 469064}, {'id': 276, 'seed': 2, 'status': 'queued', 'pid': None}]. Both launched M3 seeds recorded finite loss and nonzero TokenLearner gradients at update100. Existing M0/M1 workers preserved. Queue: [{'kind': 'eval', 'status': 'finished', 'n': 33}, {'kind': 'eval', 'status': 'queued', 'n': 266}, {'kind': 'eval', 'status': 'running', 'n': 1}, {'kind': 'train', 'status': 'finished', 'n': 4}, {'kind': 'train', 'status': 'queued', 'n': 50}, {'kind': 'train', 'status': 'running', 'n': 6}]. CSV BOM read failure during migration was fixed using utf-8-sig before successful append; original states were not overwritten. New four-model ZIP was not found; latest direct user instructions govern this revision. GPU2 only, all prior budgets/evaluation/reset/storage rules retained.


## GitHub代码审查发布 2026-10-15T18:44:47+08:00
用户明确授权推送除checkpoint与数据集外的工程内容。同步四模型60训练/300评测代码、配置、当前真实日志/结果快照与代码审查入口。快照来自ch3_final_queue.db一致性备份，原始轨迹保留；所有模型权重和数据集本体留在服务器。训练评测持续运行。发布准备完成，推送结果以Git命令回执为准。


## GitHub发布范围更新 2026-10-15T18:47:59+08:00
用户明确要求评测轨迹不用上传，只传成功率结果。已将本次新增快照中的2765个原始trajectory JSON从发布索引移除，文件仍保留在服务器。保留代码、配置、成功率汇总、每个正式保存点评测结果、逐回合成功标记及论文图表。尚未推送的发布提交将据此修订，不上传该轨迹提交历史。发布脚本相对父路径错误已更正为绝对工程路径。


## GitHub审查版本已推送 2026-10-15T18:48:41+08:00
已成功推送 https://github.com/Lin-zh-handsome/depth 的 main 分支，代码与结果提交a9583ad（Git push回执bb8e55b..a9583ad）。本次新增发布内容不包含原始评测trajectory JSON、checkpoint、模型权重和数据集。四模型代码、配置、成功率结果及审查说明见docs/CODE_REVIEW_GUIDE.md与thesis/chapter3/tables/。此前尝试打包轨迹的未发布提交已修订，不在本次推送的可达历史中；原始轨迹仍保留服务器。训练/评测未停止。


## 每小时巡检 2026-10-15T18:50:06.852641+08:00
完整正式评测33/300，共1650回合；新增：无。队列[{"kind": "eval", "status": "finished", "count": 33}, {"kind": "eval", "status": "queued", "count": 266}, {"kind": "eval", "status": "running", "count": 1}, {"kind": "train", "status": "finished", "count": 4}, {"kind": "train", "status": "queued", "count": 50}, {"kind": "train", "status": "running", "count": 6}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。

2026-10-15T10:50:16.047666+00:00 Job 133 eval threading_d2/e0/seed_2/point_150 launched PID=506586, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=86852; logs/final_job_133.log


## 实际运行状态（自动更新）
2026-10-15T10:50:17.955767+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 4, "running": 6}, "eval": {"queued": 265, "finished": 33, "running": 2}, "analysis": {}}；完整回合 1650。全部工作只用物理GPU2。队列入队不等于实验完成。


## Targeted audit against 55951414 - in progress
Eight requested checks: real-state MimicGen offline/online parity; Peg source/replay success labels; actual window/update budgets; benchmark success definitions; model controlled comparisons; Threading M2 15-point EMA/result lineage; four-model current queue isolation; preserve valid live workers. No extra training or protocol change. Evidence and amendments go to docs/audit_55951414/.

2026-10-15T11:08:24.309246+00:00 Dataset manifests available: PegInsertionSide-v1_100.json, StackCube-v1_100.json, coffee_d2_200.json, stack_three_d1_200.json, threading_d2_200.json. Runnable configs refreshed without reducing any budget.


## 每小时巡检 2026-10-15T19:10:17.433551+08:00
完整正式评测33/300，共1650回合；新增：无。队列[{"kind": "eval", "status": "finished", "count": 33}, {"kind": "eval", "status": "queued", "count": 265}, {"kind": "eval", "status": "running", "count": 2}, {"kind": "train", "status": "finished", "count": 4}, {"kind": "train", "status": "queued", "count": 50}, {"kind": "train", "status": "running", "count": 6}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。


## 55951414针对性修正完成 2026-10-15T19:12:35+08:00
真实状态核对18状态/36双相机对比，RGB/米制Depth/本体一致、六次相同动作转移差0；Peg原始100成功、控制转换后90成功10失败且全部进入训练；五任务窗口及固定预算已写元数据。M2的15点750回合、三个best EMA及归一化证据核对通过，17.33%±4.16个百分点明确为success_once。修复提交23e5472：口径标签、未来评测代码提交/EMA来源、失败原因、四模型正式配置拒绝旧组/旧位置/旧控制模式、论文/数据说明。已披露M0相机初始化及裁剪端点差异，不宣称完全一致，不改已有训练。临时历史张量及旧评测代码提交缺少直接证据，明确保留限制，不伪造补齐。INVALID为空、重训/重评0；全部现有合规训练评测保持原PID继续执行。详见docs/audit_55951414/REPORT.md。

2026-10-15T12:43:30.188398+00:00 Job 108 eval threading_d2/e3/seed_0/point_150 launched PID=881910, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=86851; logs/final_job_108.log


## 实际运行状态（自动更新）
2026-10-15T12:43:33.555338+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 4, "running": 6}, "eval": {"queued": 264, "finished": 34, "running": 2}, "analysis": {}}；完整回合 1700。全部工作只用物理GPU2。队列入队不等于实验完成。


## 实际运行状态（自动更新）
2026-10-15T12:57:33.295445+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 4, "running": 6}, "eval": {"queued": 264, "finished": 35, "running": 1}, "analysis": {}}；完整回合 1750。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T12:58:06.750476+00:00 Job 133 eval threading_d2/e0/seed_2 finished, exit=0; logs/final_job_133.log

2026-10-15T12:58:06.894086+00:00 Job 113 eval threading_d2/e3/seed_1/point_150 launched PID=919669, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=86852; logs/final_job_113.log


## 实际运行状态（自动更新）
2026-10-15T12:58:09.784048+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 4, "running": 6}, "eval": {"queued": 263, "finished": 35, "running": 2}, "analysis": {}}；完整回合 1750。全部工作只用物理GPU2。队列入队不等于实验完成。


## 实际运行状态（自动更新）
2026-10-15T14:29:19.539793+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 4, "running": 6}, "eval": {"queued": 263, "finished": 36, "running": 1}, "analysis": {}}；完整回合 1800。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T14:29:51.434593+00:00 Job 108 eval threading_d2/e3/seed_0 finished, exit=0; logs/final_job_108.log

2026-10-15T14:29:51.899188+00:00 Job 301 eval threading_d2/m3/seed_0/point_50 launched PID=1166694, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=86852; logs/final_job_301.log


## 实际运行状态（自动更新）
2026-10-15T14:29:58.444197+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 4, "running": 6}, "eval": {"queued": 262, "finished": 36, "running": 2}, "analysis": {}}；完整回合 1800。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T14:37:39.635554+00:00 Job 113 eval threading_d2/e3/seed_1 finished, exit=0; logs/final_job_113.log

2026-10-15T14:37:40.439534+00:00 Job 306 eval threading_d2/m3/seed_1/point_50 launched PID=1187616, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=86862; logs/final_job_306.log


## 实际运行状态（自动更新）
2026-10-15T14:37:45.783260+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 4, "running": 6}, "eval": {"queued": 261, "finished": 37, "running": 2}, "analysis": {}}；完整回合 1850。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T16:30:59.551637+00:00 Job 301 eval threading_d2/m3/seed_0 finished, exit=0; logs/final_job_301.log


## 实际运行状态（自动更新）
2026-10-15T16:31:06.059433+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 4, "running": 6}, "eval": {"queued": 261, "finished": 38, "running": 1}, "analysis": {}}；完整回合 1900。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T16:41:39.438102+00:00 Job 306 eval threading_d2/m3/seed_1 finished, exit=0; logs/final_job_306.log


## 实际运行状态（自动更新）
2026-10-15T16:41:45.815477+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 4, "running": 6}, "eval": {"queued": 261, "finished": 39}, "analysis": {}}；完整回合 1950。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T16:44:33.230539+00:00 Job 130 eval threading_d2/e0/seed_1/point_250 launched PID=1528619, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=98213; logs/final_job_130.log


## 实际运行状态（自动更新）
2026-10-15T16:44:36.081769+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 5, "running": 5}, "eval": {"queued": 260, "finished": 39, "running": 1}, "analysis": {}}；完整回合 1950。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T17:14:24.529823+00:00 Job 134 eval threading_d2/e0/seed_2/point_200 launched PID=1609266, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=95775; logs/final_job_134.log


## 实际运行状态（自动更新）
2026-10-15T17:14:26.501708+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 5, "running": 5}, "eval": {"queued": 259, "finished": 39, "running": 2}, "analysis": {}}；完整回合 1950。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T19:01:22.781890+00:00 Job 130 eval threading_d2/e0/seed_1 finished, exit=0; logs/final_job_130.log

2026-10-15T19:01:23.219521+00:00 Job 109 eval threading_d2/e3/seed_0/point_200 launched PID=1890513, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=95775; logs/final_job_109.log


## 实际运行状态（自动更新）
2026-10-15T19:01:26.383593+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 5, "running": 5}, "eval": {"queued": 258, "finished": 40, "running": 2}, "analysis": {}}；完整回合 2000。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T19:13:34.017402+00:00 Job 134 eval threading_d2/e0/seed_2 finished, exit=0; logs/final_job_134.log

2026-10-15T19:13:34.209457+00:00 Job 114 eval threading_d2/e3/seed_1/point_200 launched PID=1924264, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=95775; logs/final_job_114.log


## 实际运行状态（自动更新）
2026-10-15T19:13:40.047685+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 5, "running": 5}, "eval": {"queued": 257, "finished": 41, "running": 2}, "analysis": {}}；完整回合 2050。全部工作只用物理GPU2。队列入队不等于实验完成。


## 实际运行状态（自动更新）
2026-10-15T20:04:08.105110+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 5, "running": 5}, "eval": {"queued": 257, "finished": 42, "running": 1}, "analysis": {}}；完整回合 2100。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T20:04:40.769569+00:00 Job 109 eval threading_d2/e3/seed_0 finished, exit=0; logs/final_job_109.log

2026-10-15T20:04:40.939378+00:00 Job 302 eval threading_d2/m3/seed_0/point_100 launched PID=2059823, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=95775; logs/final_job_302.log


## 实际运行状态（自动更新）
2026-10-15T20:04:43.091561+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 5, "running": 5}, "eval": {"queued": 256, "finished": 42, "running": 2}, "analysis": {}}；完整回合 2100。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T20:20:32.837404+00:00 Job 114 eval threading_d2/e3/seed_1 finished, exit=0; logs/final_job_114.log

2026-10-15T20:20:33.584402+00:00 Job 307 eval threading_d2/m3/seed_1/point_100 launched PID=2102335, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=95785; logs/final_job_307.log


## 实际运行状态（自动更新）
2026-10-15T20:20:35.823038+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 5, "running": 5}, "eval": {"queued": 255, "finished": 43, "running": 2}, "analysis": {}}；完整回合 2150。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T21:49:57.340042+00:00 Job 302 eval threading_d2/m3/seed_0 finished, exit=0; logs/final_job_302.log


## 实际运行状态（自动更新）
2026-10-15T21:50:02.316747+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 5, "running": 5}, "eval": {"queued": 255, "finished": 44, "running": 1}, "analysis": {}}；完整回合 2200。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T22:12:37.232218+00:00 Job 307 eval threading_d2/m3/seed_1 finished, exit=0; logs/final_job_307.log


## 实际运行状态（自动更新）
2026-10-15T22:12:39.605985+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 5, "running": 5}, "eval": {"queued": 255, "finished": 45}, "analysis": {}}；完整回合 2250。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T22:31:58.159982+00:00 Job 135 eval threading_d2/e0/seed_2/point_250 launched PID=2448171, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=107136; logs/final_job_135.log


## 实际运行状态（自动更新）
2026-10-15T22:32:01.402651+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 6, "running": 4}, "eval": {"queued": 254, "finished": 45, "running": 1}, "analysis": {}}；完整回合 2250。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T23:06:54.503306+00:00 Job 110 eval threading_d2/e3/seed_0/point_250 launched PID=2537299, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=113836; logs/final_job_110.log


## 实际运行状态（自动更新）
2026-10-15T23:06:57.746586+00:00
60训练、300正式评测。{"train": {"queued": 50, "finished": 7, "running": 3}, "eval": {"queued": 253, "finished": 45, "running": 2}, "analysis": {}}；完整回合 2250。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-15T23:07:28.392446+00:00 Job 15 train threading_d2/e3/seed_2/point_-1 launched PID=2538838, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=111399; logs/final_job_15.log


## 实际运行状态（自动更新）
2026-10-15T23:07:30.789475+00:00
60训练、300正式评测。{"train": {"queued": 49, "finished": 7, "running": 4}, "eval": {"queued": 253, "finished": 45, "running": 2}, "analysis": {}}；完整回合 2250。全部工作只用物理GPU2。队列入队不等于实验完成。


## 实际运行状态（自动更新）
2026-10-15T23:34:35.394564+00:00
60训练、300正式评测。{"train": {"queued": 49, "finished": 8, "running": 3}, "eval": {"queued": 253, "finished": 45, "running": 2}, "analysis": {}}；完整回合 2250。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-16T00:42:53.968634+00:00 Job 135 eval threading_d2/e0/seed_2 finished, exit=0; logs/final_job_135.log

2026-10-16T00:42:54.120632+00:00 Job 115 eval threading_d2/e3/seed_1/point_250 launched PID=2780481, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=113948; logs/final_job_115.log


## 实际运行状态（自动更新）
2026-10-16T00:42:58.497769+00:00
60训练、300正式评测。{"train": {"queued": 49, "finished": 8, "running": 3}, "eval": {"queued": 252, "finished": 46, "running": 2}, "analysis": {}}；完整回合 2300。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-16T00:59:51.715401+00:00 Job 110 eval threading_d2/e3/seed_0 finished, exit=0; logs/final_job_110.log

2026-10-16T00:59:51.876201+00:00 Job 303 eval threading_d2/m3/seed_0/point_150 launched PID=2822878, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=113948; logs/final_job_303.log


## 实际运行状态（自动更新）
2026-10-16T00:59:56.284477+00:00
60训练、300正式评测。{"train": {"queued": 49, "finished": 8, "running": 3}, "eval": {"queued": 251, "finished": 47, "running": 2}, "analysis": {}}；完整回合 2350。全部工作只用物理GPU2。队列入队不等于实验完成。


## 实际运行状态（自动更新）
2026-10-16T01:51:58.140265+00:00
60训练、300正式评测。{"train": {"queued": 49, "finished": 8, "running": 3}, "eval": {"queued": 251, "finished": 48, "running": 1}, "analysis": {}}；完整回合 2400。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-16T01:52:30.267817+00:00 Job 115 eval threading_d2/e3/seed_1 finished, exit=0; logs/final_job_115.log

2026-10-16T01:52:30.406740+00:00 Job 308 eval threading_d2/m3/seed_1/point_150 launched PID=2998280, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=113958; logs/final_job_308.log


## 实际运行状态（自动更新）
2026-10-16T01:52:33.155996+00:00
60训练、300正式评测。{"train": {"queued": 49, "finished": 8, "running": 3}, "eval": {"queued": 250, "finished": 48, "running": 2}, "analysis": {}}；完整回合 2400。全部工作只用物理GPU2。队列入队不等于实验完成。

2026-10-16T02:04:40.091738+00:00 Job 303 eval threading_d2/m3/seed_0 finished, exit=0; logs/final_job_303.log

2026-10-16T02:04:40.345576+00:00 Job 116 eval threading_d2/e3/seed_2/point_50 launched PID=3033785, GPU=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9, freeMiB=113958; logs/final_job_116.log


## 实际运行状态（自动更新）
2026-10-16T02:04:43.339657+00:00
60训练、300正式评测。{"train": {"queued": 49, "finished": 8, "running": 3}, "eval": {"queued": 249, "finished": 49, "running": 2}, "analysis": {}}；完整回合 2450。全部工作只用物理GPU2。队列入队不等于实验完成。


## 每小时巡检 2026-10-16T10:18:09.352046+08:00
完整正式评测49/300，共2450回合；新增：threading_d2/e3/seed0/150: 6/50=12%; threading_d2/e3/seed0/200: 4/50=8%; threading_d2/e3/seed0/250: 3/50=6%; threading_d2/e3/seed1/150: 9/50=18%; threading_d2/e3/seed1/200: 6/50=12%; threading_d2/e3/seed1/250: 8/50=16%; threading_d2/e0/seed1/200: 5/50=10%; threading_d2/e0/seed1/250: 3/50=6%; threading_d2/e0/seed2/150: 6/50=12%; threading_d2/e0/seed2/200: 7/50=14%; threading_d2/e0/seed2/250: 6/50=12%; threading_d2/m3/seed0/50: 8/50=16%; threading_d2/m3/seed0/100: 9/50=18%; threading_d2/m3/seed0/150: 9/50=18%; threading_d2/m3/seed1/50: 5/50=10%; threading_d2/m3/seed1/100: 5/50=10%。队列[{"kind": "eval", "status": "finished", "count": 49}, {"kind": "eval", "status": "queued", "count": 249}, {"kind": "eval", "status": "running", "count": 2}, {"kind": "train", "status": "finished", "count": 8}, {"kind": "train", "status": "queued", "count": 49}, {"kind": "train", "status": "running", "count": 3}]。问题：无。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。


## 夜间进展核实 2026-10-16T10:19:58+08:00
Threading M0三种子已完成250轮及全部15次正式评测，Best-of-5依次12%、10%、14%，三种子均值12.00%、样本标准差2.00个百分点，success_once口径（过程中曾成功）。M1种子0/1完成250轮和五点评测，Best分别12%、18%，种子2在第50轮评测，暂不计算三种子最终统计。M3种子0约155轮、种子1第150轮等待其评测，种子2按既定同方法并行上限排队。全局8/60训练、49/300正式评测完成，2450完整回合；3训练、2评测运行。现有进程及更新/回合增长正常，两项训练等待自身评测是有意回压。GPU2近期平均68.9%，调度器467412和负载控制器555733存活；可用内存1.8TiB、磁盘约1461GiB，无暂停标记、无异常、不改预算、不操作GPU5。Threading 12训练/60评测全部完成后才换任务。
