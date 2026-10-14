# 第三章最终实验合同｜45次训练 + 225次评测

## 研究范围

仅第三章GSC-DP，原始CNN Diffusion Policy为基线。仅训练三模型：

- M0：原始RGB CNN-DP，ResNet18 + Conditional 1D U-Net，原有动作空间/调度/目标不变。
- M1：M0 + 真实对齐Depth引导的GSA，复用同一RGB主干，不动扩散预测头和损失。
- M2：M1 + Geometry-associated TokenLearner，8个空间token，从同一权重图聚合视觉特征与归一化(u,v)、有效深度d、有效率rho，残差注入原global_cond。

M1和M2的GSA、Depth前处理必须一致；三个模型的训练演示、动作定义、seed、公共超参数、相机、观测历史、训练/推理噪声调度、action horizon、归一化与控制模式同任务固定。所有真实RGB-D由官方演示同步回放或真实数据获得，禁止估计深度冒充GT或使用仿真oracle物体真值作为模型输入。

## 五任务全部固定的训练/评测协议

| Benchmark | task | demos | train budget | 5 evaluation positions | episodes/eval | rollout horizon |
|---|---|---:|---:|---|---:|---:|
| MimicGen Core | stack_three_d1 | 200 | 250 dataset epochs | 50/100/150/200/250 epoch | 50 | 400 |
| MimicGen Core | threading_d2 | 200 | 250 dataset epochs | 50/100/150/200/250 epoch | 50 | 400 |
| MimicGen Core | coffee_d2 | 200 | 250 dataset epochs | 50/100/150/200/250 epoch | 50 | 400 |
| ManiSkill 3 | StackCube-v1 | 100 | 100,000 optimizer updates | 20k/40k/60k/80k/100k updates | 100 | 200 |
| ManiSkill 3 | PegInsertionSide-v1 | 100 | 100,000 optimizer updates | 20k/40k/60k/80k/100k updates | 100 | 300 |

- 训练种子：[0,1,2]。3方法×5任务×3种子=45个训练run。每run恰好5个scheduled rollout，合计225次评测点，不是225次独立训练。
- 27个MimicGen runs×5评测×50episodes=6750 episodes；18个ManiSkill runs×5评测×100episodes=9000；合计**15750个episode**（未计已有匹配结果复用）。
- MimicGen参考 IJRR 2026 EquiDiff 附录 50,000/n_demos 的统一训练预算：200 demos对应250 epochs；**该论文采用50次周期性评测，我们只借用训练预算而不复制评测频率。**
- ManiSkill官方视觉RGB CNN-DP StackCube示例100,000迭代，PegInsertionSide官方state DP示例100,000迭代；Peg视觉RGB-D的100k为同任务外推的**预先固定的研究预算**，不要宣称该视觉配置已经被官方单独调优。
- `epoch`必须由实际完整DataLoader epoch（遍历动作时间窗）定义，并记录 `len(dataset_windows)`, `batch_size`, `drop_last`, `gradient_accumulation`, `optimizer_steps_per_epoch`；`optimizer_update`仅指发生了`optimizer.step()`的真实更新，不能与数据批次数混淆。ManiSkill用optimizer updates做主预算，Codex可由实际窗口数及batch转换近似对应epoch数，写入配置与日志，不提前虚构epoch数。
- 训练设置在开始前锁定，不根据评测成绩调整epoch/步数、学习率、checkpoint位置、任务或seed。禁止因最终结果不理想减少种子或修改预算后只保留好结果。

## 评测与统计：用户指定的唯一标准

对于第s个训练种子，在5个指定进度点独立加载checkpoint，使用环境官方success判定真实closed-loop rollout。

`SR[s,i] = sum_episode_success / n_eval_episodes`, `i=1..5`；

`BestSR[s] = max_i SR[s,i]`；`BestCheckpoint[s] = argmax_i SR[s,i]`，若并列则选**最早**进度位置（确定性规则）。

`ReportedSR = mean(BestSR[0], BestSR[1], BestSR[2])`，同时报告三个seed的`sample_std(ddof=1)`，可选展示三个seed个别值。绘制5个训练进度点上的各模型success曲线与seed误差条；loss曲线仅辅助说明训练运行情况。

**不计算 Last10SR、不另设最终测试或选点过程、不额外评测第六个checkpoint**。应在论文中明确Best-of-5是在周期性rollout上取最大值，有选择偏差；与采用50次评测的已发表论文结果只能列文献参考表，不能直接归因为严格同协议超越。

同任务M0/M1/M2在所有seed使用固定一致的demo IDs，且每个评测点使用**同一任务共享的评测reset列表**，如环境支持精确reset/state复现则保存state/reset IDs；同模型不同checkpoint也使用同一批固定reset以提高可比性。不得读取episode未来数据作为策略输入。每条episode记录任务、方法、训练seed、eval点、reset_id、episode_success、env_version、control_mode、checkpoint_sha。

训练中阶段性checkpoint的success选优，是本研究采用的benchmark评测指标，而不是独立最终测试集上的无偏泛化估计，论文措辞必须准确。

## 训练和评测调度（不分需用户批准的阶段）

全部45次run、225次eval立即纳入可恢复队列。M2优先、M1第二、M0第三；任务按threading_d2、PegInsertionSide、stack_three_d1、coffee_d2、StackCube优先；实际空闲H200卡/CPU可用则并行，不用等高优先作业结束才允许其它训练。训练进程使用现存tmux/nohup保证SSH断开不影响，禁止占用别人GPU。

训练进度走到指定位置时原子保存 **临时推理权重** 并将独立评测事件入队；异步evaluator从磁盘checkpoint加载而不是直接用训练内存模型；评测结果与原始episode落盘后先原子更新best，再回收非best推理快照。保持latest训练恢复文件一份/运行中run；控制快照积压，必要时按run背压，不能为了磁盘满跳过既定五次评测。具体见CHECKPOINT_STORAGE_POLICY.md。

## 必需的实验和论文交付

- 表：3种方法×5任务的Best-of-5 SR `3 seeds mean±std`；递进差值 `(M1-M0)` 和 `(M2-M1)`，图中表中注明单位百分点。
- 曲线：训练中5个评测点的成功率变化（同任务方法共享纵轴与相同预算进度）；loss辅助曲线可选。
- 可视化：真实GSA Query级空间权重、TokenLearner 8权重掩码及对应(u,v,d,rho)，从真实checkpoint导出的执行过程关键帧/视频与典型成败案例，不增加新的模型训练。
- 外部文献：已发表ACT/Transformer-DP/DP3/EquiDiff结果单独列“Published参考”，保留论文、任务、示范、模态和不同评测次数来源；不在本地受控消融主表混入。
- 不做参数量/FLOPs/显存/推理速度等计算效率实验，不做普通自注意力/RGB-D baseline/无GSA TokenLearner/ResNet或数据效率对照，也不做第四章。

## 文献与实现依据

- IJRR 2026 EquiDiff论文（训练细节中明确 `epochs=50,000/n_demos`）：https://journals.sagepub.com/doi/10.1177/02783649261424445
- ManiSkill官方DP训练示例（RGB StackCube 100000，state PegInsertionSide 100000）：https://github.com/mani-skill/ManiSkill/blob/main/examples/baselines/diffusion_policy/baselines.sh
- CNN-DP原实现：https://github.com/real-stanford/diffusion_policy
- MimicGen：https://github.com/NVlabs/mimicgen
- DFormerv2代码：https://github.com/VCIP-RGBD/DFormer/blob/main/models/encoders/DFormerv2.py
- TokenLearner：https://github.com/google-research/scenic/tree/main/scenic/projects/token_learner

## 结果持久化字段

保留每个episode原始CSV/JSONL、每个评测点的成功次数、总次数、SR及checkpoint哈希。一个run的五个点完成后才计算BestSR；某种方法的3个seed完成后计算报告值。非最佳权重删除不影响全5点记录/曲线；统一使用仓库真实结果，无数据则显示`NOT_AVAILABLE`。
