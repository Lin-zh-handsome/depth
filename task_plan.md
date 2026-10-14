# 研究计划｜仅硕士论文第三章GSC-DP

本文件为Codex可持续更新的planning-with-files合同。2026-10-14更新：**取代旧1710次eval/Last10SR规则**。预生成状态不表示服务器已启动作业。

## 固定目标

- 仅三网络M0、M1、M2；两个Benchmark五任务；seed 0/1/2。
- 45个独立训练run、每run5次周期性rollout，共225个eval点、15750个episodes（无复用的满额理论值）。
- MimicGen每任务200 demos，250 dataset epochs；ManiSkill每任务100 demos，100000 optimizer updates。
- 主结果为`Best-of-5`：各seed5个checkpoint取最大SR，再跨3种子算mean±sample_std。
- 只做SR对比、递进式模块增益、5点评测曲线、GSA/TokenLearner真实可视化及执行案例；不做效率、编码器、注意力变体、数据效率、第四章。
- checkpoint best推理权重一份/run + latest训练状态一份/活跃run + 有界短生命周期eval临时权重；不堆积历史模型。

## 一次性创建全部任务，不设置人工审批阶段

- [ ] A 接管当前H200仓库、正在运行的45run候选与旧eval队列，收集数据/配置/版本/日志hash，标注历史可复用结果。禁止把预生成状态当实际情况。
- [ ] B 使训练入口与固定预算、指定5个评测时点一致；GSA及关联TokenLearner实现完全吻合CNN-DP骨干；Depth数据/动作控制模式统一。
- [ ] C 取消旧周期性快照逻辑，实现225条新eval manifest、独立加载磁盘快照的rollout、可恢复队列、最佳权重安全更新与快照回收。
- [ ] D H200资源可用时优先M2、并行M1/M0；全部45run一次性入队；不重复合法的已完成训练。
- [ ] E 完成225个真实评测点或复用合规同位置旧数据，保留每个episode完整记录；汇总Best-of-5的三种子mean±std，不生成Last10。
- [ ] F 导出五任务表、5点SR曲线、真实GSA/TokenLearner热图、操作关键帧与MP4，记录其checkpoint SHA。
- [ ] G 审计并安全回收旧已失效checkpoint，维护安全清理清单、磁盘占用、PID/GPU与可恢复命令。
- [ ] H 将真实结果同步写入`thesis/chapter3/`，填补图表和中文分析。未完成项目保持TODO，不能虚构。

执行优先级仅用于队列排序，不代表分阶段开工。所有报告都需要区分PENDING与DONE。


## 最终协议正式执行 2026-10-14T12:10:33.001532+08:00
已部署提交6416b92/ab5f0f8；45训练225正式评测15750回合清单已实查通过。只计算五指定位置Best-of-5，并列选最早位置；三个seed均值和样本标准差。旧35/40轮评测已停止，其部分日志和旧1710清单归档保留，不参与新统计。GPU2单卡实际启动，调度器PID3430126；GPU5及独立seed42任务明确不操作。运行状态 [["eval", "queued", 223], ["eval", "running", 2], ["train", "queued", 39], ["train", "running", 6]]。
实际进程 [{"id": 10, "kind": "train", "task": "threading_d2", "method": "e6", "seed": 0, "pid": 3433612}, {"id": 11, "kind": "train", "task": "threading_d2", "method": "e6", "seed": 1, "pid": 3435319}, {"id": 13, "kind": "train", "task": "threading_d2", "method": "e3", "seed": 0, "pid": 3436999}, {"id": 14, "kind": "train", "task": "threading_d2", "method": "e3", "seed": 1, "pid": 3439300}, {"id": 16, "kind": "train", "task": "threading_d2", "method": "e0", "seed": 0, "pid": 3441539}, {"id": 17, "kind": "train", "task": "threading_d2", "method": "e0", "seed": 1, "pid": 3443211}, {"id": 76, "kind": "eval", "task": "stack_three_d1", "method": "e0", "seed": 0, "pid": 3430198}, {"id": 77, "kind": "eval", "task": "stack_three_d1", "method": "e0", "seed": 0, "pid": 3431847}]
M2 Threading种子0/1已从294/273更新恢复，均已实际到300更新并记录有限loss。M1两种子从255/241更新恢复。M0种子0从158383更新恢复，当前因4个新协议旧保存点等待评测而回压，未重新训练。MimicGen已有两项M0恢复权重复用；目前新协议完整评测DONE=0，不引用旧非五位置成功率。PegInsertionSide100条pd_ee_delta_pose RGB-D转换完成；StackCube转换仍在运行，manifest完成后自动放行。每小时巡检gsc-dp已ACTIVE并使用ch3_final_queue.db。
新权重预计约100GB、建议预留150GB，旧权重和数据另计。best/latest/临时快照回收代码已部署；真实回收尚待第一个完整正式评测，不能称已验证完成。最新完整恢复文件随必要恢复点原子替换；长期只保留best。正式evaluate不采集注意力，三方法五点完成后独立best轨迹分析导出至thesis/chapter3。
恢复命令：cd /home/linzhenghong/project/gsc_dp_chapter3/campaign_v1 && PYTHONNOUSERSITE=1 nohup /home/linzhenghong/miniconda3/envs/gsc-robodiff/bin/python jobs/scheduler.py > logs/final_scheduler.log 2>&1 &


## 实际运行状态（自动更新）
2026-10-14T10:49:18.521291+00:00
45训练、225正式评测。{"train": {"queued": 38, "running": 6, "finished": 1}, "eval": {"queued": 214, "finished": 10, "running": 1}, "analysis": {}}；完整回合 500。全部工作只用物理GPU2。队列入队不等于实验完成。

## 当前巡检结论 2026-10-14T13:00:53.031961+08:00
五任务数据清单已就绪；实际6训练和2评测推进。正式完整评测0/225，待50/100轮首批评测完成后检验实际best权重更新及逐文件回收。训练总预算、控制模式、reset集合及五评测位置均保持最终协议；详见monitoring_manifest.json。


## 当前巡检结论 2026-10-14T14:08:47.225581+08:00
首批完整正式评测已完成，最佳权重更新与按引用逐文件回收链路已实际执行。保持45训练225评测预算，继续完成其余保存点；三种子统计不提前计算。详见experiments/ch3/monitoring_manifest.json和thesis/chapter3/source_data/checkpoint_sr.csv。


## 巡检进度 2026-10-14T15:07:34.168016+08:00
完整正式评测5/225；新增stack_three_d1/e0/seed0/150: 26/50=52%; stack_three_d1/e0/seed0/200: 22/50=44%; threading_d2/e0/seed0/100: 2/50=4%。规划备注截断已修复，全部训练评测保持原预算、控制模式与GPU2绑定。


## 巡检进度 2026-10-14T16:04:33.642804+08:00
完整正式评测8/225；新增threading_d2/e0/seed0/50: 6/50=12%; threading_d2/e0/seed0/150: 6/50=12%; threading_d2/e0/seed0/200: 4/50=8%。全部训练评测保持原预算、控制模式与GPU2绑定。


## 巡检进度 2026-10-14T17:02:57.075907+08:00
完整正式评测9/225；新增threading_d2/e0/seed1/50: 2/50=4%。全部训练评测保持原预算、控制模式与GPU2绑定。


## 巡检进度 2026-10-14T18:02:01.328847+08:00
完整正式评测10/225；新增threading_d2/e0/seed0/250: 5/50=10%。全部训练评测保持原预算、控制模式与GPU2绑定。


## 用户改为按任务串行推进 2026-10-14T18:32:46.777107+08:00
当前Threading为唯一可启动训练/正式评测的任务。同任务内三模型三种子可并行，M2优先；必须9项训练和45次正式评测全部完成后，才切换PegInsertionSide、Stack Three、Coffee、StackCube。修正此前表述：一个任务共45次正式评测，不是15次。其余任务保持已入队，已有结果和权重保留；不改变训练预算、五个位置和每点回合数。仅重启调度器，六个现有Threading训练进程不停止。GPU5不操作。


## 裁剪同步瓶颈修复 2026-10-14T18:42:51.635821+08:00
M1/M2逐张裁剪使用CUDA标量作为Python slice边界，单相机128观测触发1536次aten::item和本地标量读取，实际单次操作约1.047秒。批量gather裁剪无标量读取，约0.080秒；相同随机状态下RGB/Depth/valid输出及RGB梯度完全相同。仅修复执行路径，无参数或科学协议变化。这是运行瓶颈诊断，不是论文效率对比。四个M1/M2训练均SIGTERM原子保存恢复点后部署等价裁剪；M0、GPU5及其他任务未停止。55小时只是旧慢速外推，修复后重新按实际训练日志估算。证据logs/crop_diagnosis.json、docs/crop_optimization_restart.json。


## 裁剪修复后实际训练进展 2026-10-14T18:45:38.046049+08:00
四项M1/M2已从12730/12697/12803/12703更新完整恢复，无重训和预算改动。短窗口实际速率 [{"method": "e3", "seed": 0, "pid": 492122, "updates_measured": 100, "seconds": 23.97092366218567, "updates_per_hour": 15018.194754334936, "full_250epochs_hours": 11.45277463859982, "latest_loss": 0.052587706595659256}, {"method": "e6", "seed": 0, "pid": 489094, "updates_measured": 400, "seconds": 83.71960353851318, "updates_per_hour": 17200.27256624027, "full_250epochs_hours": 9.999841533766851, "latest_loss": 0.05722839757800102}, {"method": "e6", "seed": 1, "pid": 490507, "updates_measured": 300, "seconds": 65.39141297340393, "updates_per_hour": 16515.93001116613, "full_250epochs_hours": 10.414187992060626, "latest_loss": 0.05358270928263664}]。旧55小时及其整套4–6周估计基于已修复的慢速路径，应作废；新的耗时以更长实际训练区间持续校正。
