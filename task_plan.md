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
2026-10-16T06:02:36.635631+00:00
60训练、300正式评测。{"train": {"queued": 49, "finished": 8, "running": 3}, "eval": {"queued": 246, "finished": 52, "running": 2}, "analysis": {}}；完整回合 2600。全部工作只用物理GPU2。队列入队不等于实验完成。

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


## 优先完整方法已生效 2026-10-14T18:56:16.539637+08:00
当前只运行Threading M2 seed0 PID489094及其五点评测；五个其他训练均在SIGTERM后写出完整最新恢复文件并退出，M0 seed1评测保留部分回合。M0等待评测时的停止分支保存恢复点但不打印recoverable stop，已按退出状态和停止后原子恢复文件时间确认，不重复停止或重训。focus_scheduler PID524143。M2依次完成种子0/1/2，各250轮及5次50回合，随后恢复当前任务其他模型。held_for_full_method为用户指定等待，不是失败。GPU5不操作。


## M2三个种子优先并行 2026-10-14T19:01:38.212412+08:00
用户撤销独占串行训练，要求并行但先完成M2所有实验。当前任务Threading的M2种子0/1/2最多三训练并行，正式评测最多两进程；三个种子均250轮及五点评测共15点评测完成后，才恢复M1/M0。仍保持当前任务9训练45评测全部完成后再换任务，不跨任务。M2种子0现有进程保留，种子1从暂停恢复文件续训，种子2新启动完整预算。M1/M0继续held_for_full_method；GPU5不操作。


## 巡检进度 2026-10-14T19:02:30.956908+08:00
完整正式评测10/225；新增无。全部训练评测保持原预算、控制模式与GPU2绑定。


## GPU2负载目标 2026-10-14T19:06:28.202659+08:00
用户希望GPU利用率约70%。增加独立运行时负载控制器，按NVML滚动读数自适应占空比，仅短时暂停/继续本账号本工程绑定GPU2的训练评测进程；保持M2三种子并行优先，不改模型、批量、训练更新数、随机状态或评测回合。目标为65–75%附近的平均利用率，瞬时读数允许波动；GPU5和其他用户进程完全排除。配置jobs/gpu_load_target.json，状态jobs/gpu_load_state.json。目标限载会增加墙钟时间，后续耗时需重新按实际进度估计。


## 巡检进度 2026-10-14T20:04:34.667278+08:00
完整正式评测10/225；新增无。全部训练评测保持原预算、控制模式与GPU2绑定。


## 首个M2正式评测已启动 2026-10-14T20:04:34.667278+08:00
Threading M2 seed0到达第50完整dataset epoch/34400更新，已原子保存磁盘推理快照并独立评测（PID708025，本次巡检7/50回合）；训练等待该点完整评测是预定回压，不是卡死。seed1约49轮，seed2约27轮，有限loss且更新数增长。M2尚无完整正式评测成绩，不汇报部分SR。GPU2近期平均利用率约68.9%，瞬时读数可达100%；负载控制器持续工作。M1/M0有意等待，GPU5不操作。


## 巡检进度 2026-10-14T21:09:33.618620+08:00
完整正式评测11/225；新增threading_d2/e6/seed0/50: 5/50=10%。全部训练评测保持原预算、控制模式与GPU2绑定。


## 首个M2完整正式评测 2026-10-14T21:09:33.618620+08:00
Threading M2种子0第50轮完成固定50回合真实闭环评测，5/50=10%，reset列表完整且唯一。best/best.pt及元数据已真实保留，种子0继续约52轮训练。种子1第50轮评测47/50回合，其训练等待评测为预定回压；种子2约49轮。未完成五点和三种子，10%只能标为第50轮SR，不能称最终Best-of-5或方法报告值。GPU2近期平均约70.1%，限载正常。总正式评测11/225、完整550回合，三项M2持续推进；M1/M0有意等待，其他任务与GPU5不操作。


## 巡检进度 2026-10-14T22:11:25.152002+08:00
完整正式评测13/225；新增threading_d2/e6/seed1/50: 5/50=10%; threading_d2/e6/seed2/50: 6/50=12%。全部训练评测保持原预算、控制模式与GPU2绑定。


## M2三个种子首点评测齐全 2026-10-14T22:11:25.152002+08:00
Threading M2第50轮三个种子均完成固定50回合：seed0=5/50(10%)、seed1=5/50(10%)、seed2=6/50(12%)；各best文件真实存在，保留该阶段原始回合及源数据。当前训练进度分别约75/70/52轮，三进程存活、有限loss、GPU2绑定正确。M2正式评测完成3/15，总完成13/225(650完整回合)。后续100/150/200/250轮尚未完成，不计算最终Best-of-5或三seed方法报告值。GPU2近期平均约71.0%，限载正常；M1/M0仍按用户要求等待，无异常。


## 巡检进度 2026-10-15T14:43:28.453143+08:00
完整正式评测29/225；新增threading_d2/e6/seed0/100: 5/50=10%; threading_d2/e6/seed0/150: 7/50=14%; threading_d2/e6/seed0/200: 6/50=12%; threading_d2/e6/seed0/250: 4/50=8%; threading_d2/e6/seed1/100: 5/50=10%; threading_d2/e6/seed1/150: 8/50=16%; threading_d2/e6/seed1/200: 5/50=10%; threading_d2/e6/seed1/250: 5/50=10%; threading_d2/e6/seed2/100: 9/50=18%; threading_d2/e6/seed2/150: 3/50=6%; threading_d2/e6/seed2/200: 11/50=22%; threading_d2/e6/seed2/250: 11/50=22%; threading_d2/e3/seed0/50: 1/50=2%; threading_d2/e3/seed1/50: 2/50=4%; threading_d2/e0/seed1/100: 4/50=8%; threading_d2/e0/seed2/50: 2/50=4%。全部训练评测保持原预算、控制模式与GPU2绑定。


## M2全部完成及后续恢复巡检 2026-10-15T14:43:28.453143+08:00
Threading M2三个种子250轮和15次正式评测全部完成，五点评测最佳依次14%/16%/22%，均值17.3333%、样本标准差4.1633个百分点；best推理权重保留，结果由真实逐回合数据汇总。焦点配置已自动completed，Threading M0/M1已正常恢复，符合用户最新指令，不是误解除等待。当前M1种子0/1约86/83轮，M0种子1到150轮并评测20/50回合，种子2约98轮；四项训练和一项正式评测存活，未发现失败。整体4/45训练、29/225正式评测完成，1450完整回合。M1种子2尚排队，仍不跨任务。GPU2近期平均约70.3%，限载正常，GPU5不操作。完整结果已在本对话用户查询时报告，不将部分评测计作完成。


## 巡检进度 2026-10-15T15:44:00.510504+08:00
完整正式评测30/225；新增threading_d2/e0/seed1/150: 5/50=10%。全部训练评测保持原预算、控制模式与GPU2绑定。


## 每小时推进确认 2026-10-15T15:44:00.510504+08:00
新增Threading M0 seed1第150轮完整正式评测5/50=10%，精确reset列表通过。整体正式评测30/225、1500完整回合，训练完成4/45；四项M0/M1训练和两项正式评测仍在运行。M1 seed0到100轮等待评测(8/50回合)、seed1约97轮；M0 seed1约153轮、seed2到100轮等待评测(31/50回合)。等待是预定回压，不是卡死，无失败或非有限loss。M2三种子已完整完成，最终17.3333%±4.1633%保持不变；不对未完M0/M1计算最终均值。GPU2近期平均约68.9%，限载正常；只推进Threading，不影响GPU5。


## 巡检进度 2026-10-15T16:48:34.158612+08:00
完整正式评测32/225；新增threading_d2/e3/seed0/100: 3/50=6%; threading_d2/e0/seed2/100: 2/50=4%。全部训练评测保持原预算、控制模式与GPU2绑定。


## 新增完整评测与运行确认 2026-10-15T16:48:34.158612+08:00
本小时新增Threading M1 seed0第100轮3/50=6%，M0 seed2第100轮2/50=4%；均完成固定50回合且reset列表完整。累计32/225正式评测、1600完整回合，训练4/45完成。M1种子0已约101轮、种子1到100轮等待评测(27/50回合)；M0种子1约167轮、种子2约110轮。四训练和一评测进程存活且GPU2绑定正确，等待为既定回压，无失败或非有限loss。GPU2近期平均约71.0%，限载正常；未跨任务，GPU5不操作。M0/M1尚未完整三种子五点，不能将当前单点评测写为最终方法结果。


## 巡检进度 2026-10-15T17:47:30.163411+08:00
完整正式评测33/225；新增threading_d2/e3/seed1/100: 4/50=8%。全部训练评测保持原预算、控制模式与GPU2绑定。


## 当前训练与负载巡检 2026-10-15T17:47:30.163411+08:00
新增Threading M1 seed1第100轮完整正式评测4/50=8%，固定reset列表完整。正式评测累计33/225、1650完整回合，训练完成4/45。M1种子0/1约119/109轮，M0种子1/2约184/130轮；四项训练实际增长且loss有限，目前没有就绪的运行中评测，等待下一指定保存点是正常状态。无异常、无跨任务；GPU2近期平均约73.4%，限载控制正常，GPU5不操作。所有未完成模型的阶段成功率保留真实结果，不提前计算三种子最终统计。


## 四模型正式协议生效 2026-10-15T18:37:57.370028+08:00
用户新增M3=CNN-DP+Geometry-associated TokenLearner，不启用GSA，直接复用M2相同DepthTokenLearner类、8个token、同权重(u,v,d,rho)与投影残差融合。新包附件未发现，明确按本轮用户指令执行。原45训练225正式评测的ID、数据库与实际状态保留，只追加M3的15训练75评测；总计60训练300评测21000回合。沿用既定训练预算、每run五次正式评测、Best-of-5与低存储规则。不重新训练旧合规模型。每任务变为12训练60正式评测，全部完成才换任务；仍先Threading，只用GPU2，平均利用率目标70%，GPU5不操作。M2已完成，原M0/M1工作进程保持运行，新增M3按空闲队列立即正式调度。四模型主表、模块消融及M1-M0/M3-M0/M2-M1/M2-M3/M2-M0增量、成功率曲线与真实可视化已更新。无GSA的M3只展示真实TokenLearner权重，不伪称GSA注意力。证据docs/m3_migration_report.json、docs/m3_structure_consistency.json。


## Four-model formal execution 2026-10-15T18:42:27+08:00
M3 reuses the exact M2 Geometry-associated TokenLearner and geometry processing, with GSA removed. Preserved original 45 training / 225 evaluation event identities; appended only 15 training / 75 evaluation events. Threading M3 launch state: [{'id': 274, 'seed': 0, 'status': 'running', 'pid': 467460}, {'id': 275, 'seed': 1, 'status': 'running', 'pid': 469064}, {'id': 276, 'seed': 2, 'status': 'queued', 'pid': None}]. Both launched M3 seeds recorded finite loss and nonzero TokenLearner gradients at update100. Existing M0/M1 workers preserved. Queue: [{'kind': 'eval', 'status': 'finished', 'n': 33}, {'kind': 'eval', 'status': 'queued', 'n': 266}, {'kind': 'eval', 'status': 'running', 'n': 1}, {'kind': 'train', 'status': 'finished', 'n': 4}, {'kind': 'train', 'status': 'queued', 'n': 50}, {'kind': 'train', 'status': 'running', 'n': 6}]. CSV BOM read failure during migration was fixed using utf-8-sig before successful append; original states were not overwritten. New four-model ZIP was not found; latest direct user instructions govern this revision. GPU2 only, all prior budgets/evaluation/reset/storage rules retained.


## GitHub代码审查发布 2026-10-15T18:44:47+08:00
用户明确授权推送除checkpoint与数据集外的工程内容。同步四模型60训练/300评测代码、配置、当前真实日志/结果快照与代码审查入口。快照来自ch3_final_queue.db一致性备份，原始轨迹保留；所有模型权重和数据集本体留在服务器。训练评测持续运行。发布准备完成，推送结果以Git命令回执为准。


## GitHub发布范围更新 2026-10-15T18:47:59+08:00
用户明确要求评测轨迹不用上传，只传成功率结果。已将本次新增快照中的2765个原始trajectory JSON从发布索引移除，文件仍保留在服务器。保留代码、配置、成功率汇总、每个正式保存点评测结果、逐回合成功标记及论文图表。尚未推送的发布提交将据此修订，不上传该轨迹提交历史。发布脚本相对父路径错误已更正为绝对工程路径。


## GitHub审查版本已推送 2026-10-15T18:48:41+08:00
已成功推送 https://github.com/Lin-zh-handsome/depth 的 main 分支，代码与结果提交a9583ad（Git push回执bb8e55b..a9583ad）。本次新增发布内容不包含原始评测trajectory JSON、checkpoint、模型权重和数据集。四模型代码、配置、成功率结果及审查说明见docs/CODE_REVIEW_GUIDE.md与thesis/chapter3/tables/。此前尝试打包轨迹的未发布提交已修订，不在本次推送的可达历史中；原始轨迹仍保留服务器。训练/评测未停止。


## 巡检进度 2026-10-15T18:50:06.852641+08:00
完整正式评测33/300；新增无。全部训练评测保持原预算、控制模式与GPU2绑定。


## Targeted audit against 55951414 - in progress
Eight requested checks: real-state MimicGen offline/online parity; Peg source/replay success labels; actual window/update budgets; benchmark success definitions; model controlled comparisons; Threading M2 15-point EMA/result lineage; four-model current queue isolation; preserve valid live workers. No extra training or protocol change. Evidence and amendments go to docs/audit_55951414/.


## 巡检进度 2026-10-15T19:10:17.433551+08:00
完整正式评测33/300；新增无。全部训练评测保持原预算、控制模式与GPU2绑定。


## 55951414针对性修正完成 2026-10-15T19:12:35+08:00
真实状态核对18状态/36双相机对比，RGB/米制Depth/本体一致、六次相同动作转移差0；Peg原始100成功、控制转换后90成功10失败且全部进入训练；五任务窗口及固定预算已写元数据。M2的15点750回合、三个best EMA及归一化证据核对通过，17.33%±4.16个百分点明确为success_once。修复提交23e5472：口径标签、未来评测代码提交/EMA来源、失败原因、四模型正式配置拒绝旧组/旧位置/旧控制模式、论文/数据说明。已披露M0相机初始化及裁剪端点差异，不宣称完全一致，不改已有训练。临时历史张量及旧评测代码提交缺少直接证据，明确保留限制，不伪造补齐。INVALID为空、重训/重评0；全部现有合规训练评测保持原PID继续执行。详见docs/audit_55951414/REPORT.md。


## 巡检进度 2026-10-16T10:18:09.352046+08:00
完整正式评测49/300；新增threading_d2/e3/seed0/150: 6/50=12%; threading_d2/e3/seed0/200: 4/50=8%; threading_d2/e3/seed0/250: 3/50=6%; threading_d2/e3/seed1/150: 9/50=18%; threading_d2/e3/seed1/200: 6/50=12%; threading_d2/e3/seed1/250: 8/50=16%; threading_d2/e0/seed1/200: 5/50=10%; threading_d2/e0/seed1/250: 3/50=6%; threading_d2/e0/seed2/150: 6/50=12%; threading_d2/e0/seed2/200: 7/50=14%; threading_d2/e0/seed2/250: 6/50=12%; threading_d2/m3/seed0/50: 8/50=16%; threading_d2/m3/seed0/100: 9/50=18%; threading_d2/m3/seed0/150: 9/50=18%; threading_d2/m3/seed1/50: 5/50=10%; threading_d2/m3/seed1/100: 5/50=10%。全部训练评测保持原预算、控制模式与GPU2绑定。


## 夜间进展核实 2026-10-16T10:19:58+08:00
Threading M0三种子已完成250轮及全部15次正式评测，Best-of-5依次12%、10%、14%，三种子均值12.00%、样本标准差2.00个百分点，success_once口径（过程中曾成功）。M1种子0/1完成250轮和五点评测，Best分别12%、18%，种子2在第50轮评测，暂不计算三种子最终统计。M3种子0约155轮、种子1第150轮等待其评测，种子2按既定同方法并行上限排队。全局8/60训练、49/300正式评测完成，2450完整回合；3训练、2评测运行。现有进程及更新/回合增长正常，两项训练等待自身评测是有意回压。GPU2近期平均68.9%，调度器467412和负载控制器555733存活；可用内存1.8TiB、磁盘约1461GiB，无暂停标记、无异常、不改预算、不操作GPU5。Threading 12训练/60评测全部完成后才换任务。


## 巡检进度 2026-10-16T11:16:56.987108+08:00
完整正式评测51/300；新增threading_d2/e3/seed2/50: 1/50=2%; threading_d2/m3/seed1/150: 7/50=14%。全部训练评测保持原预算、控制模式与GPU2绑定。


## 本轮巡检确认 2026-10-16T11:17:37+08:00
新增两项完整正式保存点评测：Threading M1种子2第50轮1/50=2%，M3种子1第150轮7/50=14%，均为success_once（过程中曾成功），尚非完整五点Best-of-5。累计51/300次正式评测、2550完整回合、8/60项训练完成，3训练进程继续实际增长；无运行中评测是等待下一指定保存点的正常状态。GPU2平均约70.1%，调度及负载控制存活、无暂停标记，恢复权重保持更新，资源充足，无需修复，不修改预算/批大小/示范/reset/控制模式，不操作GPU5。


## 巡检进度 2026-10-16T12:20:16.879315+08:00
完整正式评测51/300；新增无。全部训练评测保持原预算、控制模式与GPU2绑定。


## 巡检进度 2026-10-16T13:24:19.062207+08:00
完整正式评测51/300；新增无。全部训练评测保持原预算、控制模式与GPU2绑定。


## 共享GPU资源变化 2026-10-16T13:25:22+08:00
无新增完整评测，仍完成8/60训练、51/300评测。M3种子0第200轮评测47/50回合、种子1第200轮3/50；M1种子2约96轮。发现共享GPU2新增其他用户进程PID3724401，占54518MiB显存；整卡近一分钟平均82.9%，本工程负载控制器已达到既定最低运行比例20%，因此当前无法仅靠本工程将整卡稳定到70%。调度器和负载控制器存活，进程/回合有增长，未暂停用户任务、未改模型预算或并行规则、未操作他人进程或GPU5。该资源变化会影响本工程墙钟耗时，应通知用户；不自行换GPU。资源证据写入monitoring_manifest.json的shared_gpu_resource_observation。


## 巡检进度 2026-10-16T14:28:22.557372+08:00
完整正式评测52/300；新增threading_d2/m3/seed0/200: 8/50=16%。全部训练评测保持原预算、控制模式与GPU2绑定。


## 本轮完整结果与资源恢复 2026-10-16T14:29:07+08:00
新增Threading M3种子0第200轮完整正式评测8/50=16%（success_once，过程中曾成功），四个已完成点依次16%、18%、18%、16%，250轮尚未评测，当前最佳18%并非最终Best-of-5。全局8/60训练、52/300评测、2600完整回合；M3种子0约213轮，种子1等待第200轮评测、M1种子2等待第100轮评测，回压正常且回合在增长。 GPU2近期平均68.6%，其他用户GPU2进程当前观测为[]；上轮资源竞争已缓解，控制器正常。未修改他人任务、GPU5、训练预算、批大小、控制模式、reset或保存点，无需修复。
