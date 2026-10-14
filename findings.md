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
