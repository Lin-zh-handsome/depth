# Findings

正式协议为唯一研究依据；服务器现有两项ManiSkill各1000条RGB-D、pd_joint_pos、128²双相机，固定前100条训练。官方DP/MimicGen/DFormer干净源码已下载；三项MimicGen Core正经hf-mirror并行下载。GPU2单卡绑定，CPU192、RAM available1.2TiB、磁盘2.2TiB。

时序Query权重使用真实轴向传播 Ah(query_y,key_y at query_x)*Aw(query_x,key_x at key_y)，按head平均，排除LEPE/残差，不能标作Full GSA。Token保留真实K图和uv/d/rho。E0/E1输入梯度显著性固定t50去噪输出能量探针，不称注意力。环境实际control_freq给出视频时间；阶段仅官方predicate或明确标注。独立analysis_jobs默认从E0/E1/E6相同保存点评测完成后触发，正式evaluate不存储注意力。


## GitHub 工程发布
仓库main已推送。GitHub身份认证通过本机既有Git凭据完成，未将认证信息写入工程。三个官方依赖采用子模块；实际日志、逐回合轨迹、队列及检查点元数据保留在artifacts/snapshot_20261013。数据本体和模型权重按用户要求排除。


## 2026-10-14 实际评测调度问题
评测保存点编号单位不同，原ORDER BY checkpoint_step使MimicGen epoch 5–250先于ManiSkill update 5000–100000，产生跨benchmark饥饿；改为入队ID先到先评。接管评测进程完成标记改按benchmark选择epoch/update目录。全部五任务数据已就绪；当前完整评测950回合仍为早期结果，非最终BEST/LAST10统计。


## 用户暂停全部训练
本轮8项训练通过SIGTERM处理保存recovery.pt后退出；额外本账号旧训练1项已停止。当前训练进程0。jobs/PAUSED_BY_USER.json阻止控制器意外重启；每小时巡检暂停。新方案明确后再决定复用哪些保存点、调整队列及解除暂停标记。数据和已有模型权重保留。


## 2026-10-14 新45-run协议接管
已读取planning-with-files完整SKILL及执行包全部文件。此前暂停已由本次正式启动指令撤销。范围M0=e0、M1=e3、M2=e6；只保留五任务三种子。旧关节位置控制ManiSkill结果保留为历史，不能合并末端增量控制协议。GPU2独卡；可用显存143152MiB、RAM1.3TiB、/home可用1.3TiB。MimicGen M0两恢复点约200/230epochs可复用。新专用ch3_queue.db保留旧queue.db记录。哈希字段不重算，按用户要求使用真实配置、示范ID、源提交、原子保存元数据及逐reset日志溯源。


## 用户暂停本次GPU2训练 2026-10-14T03:50:24.925544+00:00
已设置持久暂停标记，停止调度器，向6个本次GPU2训练发送SIGTERM保存恢复点。GPU5明确排除。现有独立评测/数据转换未收到停止信号。训练退出待确认。


停止已确认：本次GPU2的6个训练进程均退出，6个recovery.pt完整文件已保存。持久暂停标记阻止重新调度。GPU2已有2项评测和1项官方数据转换继续。GPU5当前无计算进程；其seed42旧训练PID3245588在上一轮收敛45-run范围时已收到SIGTERM，本次停止指令未向GPU5发送信号。


## 最终225评测协议接管
45训练、225评测、15750回合；取消Last10和旧1710队列。MimicGen50/100/150/200/250，ManiSkill20k/40k/60k/80k/100k；并列最佳选最早位置。正式训练继续只用GPU2，GPU5不操作。旧35/40epoch评测停止保留部分日志，全部旧结果仅精确五位置可合并。修复M0恢复后normalizer留CPU问题；checkpoint保留best+latest及有界临时快照。用户禁止冗余哈希，因此字段留空并记录元数据溯源。


## 最终协议正式执行 2026-10-14T12:10:33.001532+08:00
已部署提交6416b92/ab5f0f8；45训练225正式评测15750回合清单已实查通过。只计算五指定位置Best-of-5，并列选最早位置；三个seed均值和样本标准差。旧35/40轮评测已停止，其部分日志和旧1710清单归档保留，不参与新统计。GPU2单卡实际启动，调度器PID3430126；GPU5及独立seed42任务明确不操作。运行状态 [["eval", "queued", 223], ["eval", "running", 2], ["train", "queued", 39], ["train", "running", 6]]。
实际进程 [{"id": 10, "kind": "train", "task": "threading_d2", "method": "e6", "seed": 0, "pid": 3433612}, {"id": 11, "kind": "train", "task": "threading_d2", "method": "e6", "seed": 1, "pid": 3435319}, {"id": 13, "kind": "train", "task": "threading_d2", "method": "e3", "seed": 0, "pid": 3436999}, {"id": 14, "kind": "train", "task": "threading_d2", "method": "e3", "seed": 1, "pid": 3439300}, {"id": 16, "kind": "train", "task": "threading_d2", "method": "e0", "seed": 0, "pid": 3441539}, {"id": 17, "kind": "train", "task": "threading_d2", "method": "e0", "seed": 1, "pid": 3443211}, {"id": 76, "kind": "eval", "task": "stack_three_d1", "method": "e0", "seed": 0, "pid": 3430198}, {"id": 77, "kind": "eval", "task": "stack_three_d1", "method": "e0", "seed": 0, "pid": 3431847}]
M2 Threading种子0/1已从294/273更新恢复，均已实际到300更新并记录有限loss。M1两种子从255/241更新恢复。M0种子0从158383更新恢复，当前因4个新协议旧保存点等待评测而回压，未重新训练。MimicGen已有两项M0恢复权重复用；目前新协议完整评测DONE=0，不引用旧非五位置成功率。PegInsertionSide100条pd_ee_delta_pose RGB-D转换完成；StackCube转换仍在运行，manifest完成后自动放行。每小时巡检gsc-dp已ACTIVE并使用ch3_final_queue.db。
新权重预计约100GB、建议预留150GB，旧权重和数据另计。best/latest/临时快照回收代码已部署；真实回收尚待第一个完整正式评测，不能称已验证完成。最新完整恢复文件随必要恢复点原子替换；长期只保留best。正式evaluate不采集注意力，三方法五点完成后独立best轨迹分析导出至thesis/chapter3。
恢复命令：cd /home/linzhenghong/project/gsc_dp_chapter3/campaign_v1 && PYTHONNOUSERSITE=1 nohup /home/linzhenghong/miniconda3/envs/gsc-robodiff/bin/python jobs/scheduler.py > logs/final_scheduler.log 2>&1 &


## 实际运行状态（自动更新）
2026-10-14T10:55:48.798390+00:00
45训练、225正式评测。{"train": {"queued": 38, "running": 1, "held_for_full_method": 5, "finished": 1}, "eval": {"queued": 214, "finished": 10, "held_for_full_method": 1}, "analysis": {}}；完整回合 500。全部工作只用物理GPU2。队列入队不等于实验完成。

## 2026-10-14T13:00:53.031961+08:00 数据转换与运行进展
StackCube pd_ee_delta_pos和PegInsertionSide pd_ee_delta_pose固定100条RGB-D清单均已出现，配置自动刷新45项。M0恢复训练的回压有明确等待保存点评测，不能以长时间无loss日志判定卡死；四项M1/M2实际loss有限且较启动时推进。当前正式评测仅部分回合，不纳入Best-of-5。


## 2026-10-14T14:08:47.225581+08:00 首批完整正式结果与权重生命周期
Stack Three M0 seed0的50/100轮正式评测分别28%/42%，每点50条指定reset完整；暂时best对应100轮，最终五点评测和其他训练种子尚待完成。实际best更新及38份逐文件快照回收已执行；best与恢复权重同时存在。Threading M0等待历史合法保存点评测，其余训练持续推进。


## 2026-10-14T15:06:01.203105+08:00 规划备注被自动导出截断
原按自动状态标题split只保留前半段，丢失后来追加章节；改为替换自动状态章节至下一Markdown标题的范围，已从Git提交恢复丢失备注。科学配置和预算未改动。


## 巡检发现 2026-10-14T16:04:33.642804+08:00
新增正式保存点：threading_d2/e0/seed0/50: 6/50=12%; threading_d2/e0/seed0/150: 6/50=12%; threading_d2/e0/seed0/200: 4/50=8%。异常：无。当前仅记录完整逐回合结果；未完成五点及三种子前不报告最终统计。


## 巡检发现 2026-10-14T17:02:57.075907+08:00
新增正式保存点：threading_d2/e0/seed1/50: 2/50=4%。异常：无。当前仅记录完整逐回合结果；未完成五点及三种子前不报告最终统计。


## 巡检发现 2026-10-14T18:02:01.328847+08:00
新增正式保存点：threading_d2/e0/seed0/250: 5/50=10%。异常：无。当前仅记录完整逐回合结果；未完成五点及三种子前不报告最终统计。


## 用户改为按任务串行推进 2026-10-14T18:32:46.777107+08:00
当前Threading为唯一可启动训练/正式评测的任务。同任务内三模型三种子可并行，M2优先；必须9项训练和45次正式评测全部完成后，才切换PegInsertionSide、Stack Three、Coffee、StackCube。修正此前表述：一个任务共45次正式评测，不是15次。其余任务保持已入队，已有结果和权重保留；不改变训练预算、五个位置和每点回合数。仅重启调度器，六个现有Threading训练进程不停止。GPU5不操作。


## 裁剪同步瓶颈修复 2026-10-14T18:42:51.635821+08:00
M1/M2逐张裁剪使用CUDA标量作为Python slice边界，单相机128观测触发1536次aten::item和本地标量读取，实际单次操作约1.047秒。批量gather裁剪无标量读取，约0.080秒；相同随机状态下RGB/Depth/valid输出及RGB梯度完全相同。仅修复执行路径，无参数或科学协议变化。这是运行瓶颈诊断，不是论文效率对比。四个M1/M2训练均SIGTERM原子保存恢复点后部署等价裁剪；M0、GPU5及其他任务未停止。55小时只是旧慢速外推，修复后重新按实际训练日志估算。证据logs/crop_diagnosis.json、docs/crop_optimization_restart.json。


## 裁剪修复后实际训练进展 2026-10-14T18:45:38.046049+08:00
四项M1/M2已从12730/12697/12803/12703更新完整恢复，无重训和预算改动。短窗口实际速率 [{"method": "e3", "seed": 0, "pid": 492122, "updates_measured": 100, "seconds": 23.97092366218567, "updates_per_hour": 15018.194754334936, "full_250epochs_hours": 11.45277463859982, "latest_loss": 0.052587706595659256}, {"method": "e6", "seed": 0, "pid": 489094, "updates_measured": 400, "seconds": 83.71960353851318, "updates_per_hour": 17200.27256624027, "full_250epochs_hours": 9.999841533766851, "latest_loss": 0.05722839757800102}, {"method": "e6", "seed": 1, "pid": 490507, "updates_measured": 300, "seconds": 65.39141297340393, "updates_per_hour": 16515.93001116613, "full_250epochs_hours": 10.414187992060626, "latest_loss": 0.05358270928263664}]。旧55小时及其整套4–6周估计基于已修复的慢速路径，应作废；新的耗时以更长实际训练区间持续校正。


## 优先完整方法已生效 2026-10-14T18:56:16.539637+08:00
当前只运行Threading M2 seed0 PID489094及其五点评测；五个其他训练均在SIGTERM后写出完整最新恢复文件并退出，M0 seed1评测保留部分回合。M0等待评测时的停止分支保存恢复点但不打印recoverable stop，已按退出状态和停止后原子恢复文件时间确认，不重复停止或重训。focus_scheduler PID524143。M2依次完成种子0/1/2，各250轮及5次50回合，随后恢复当前任务其他模型。held_for_full_method为用户指定等待，不是失败。GPU5不操作。
