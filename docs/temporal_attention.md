# 机器人闭环执行过程中的时序空间关注分析

新增图3-15，独立于静态 GSA / TokenLearner（几何自注意力／自适应空间特征聚合）分析。训练预算、周期性成功率评测点和回合数均不改变。

环境：Conda `gsc-thesis-eval`。所有分析只能在物理GPU2运行；推理设备 `cuda:0` 指向唯一暴露的GPU2，SAPIEN（机器人仿真渲染后端）使用 `sapien_cuda:0`。

```bash
cd /home/linzhenghong/project/gsc_dp_chapter3/campaign_v1
export CUDA_VISIBLE_DEVICES=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9
export GSC_GPU=2 MUJOCO_EGL_DEVICE_ID=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
export PYTHONNOUSERSITE=1
PY=/home/linzhenghong/miniconda3/envs/gsc-thesis-eval/bin/python
# 指定真实保存点、reset及原始图像归一化Query(x,y)
"$PY" analysis/temporal_attention.py collect \
  --checkpoint runs/maniskill/StackCube-v1/e6/seed_0/checkpoints/update_100000.pt \
  --reset-id 100000 --query 0.5 0.5 --save-axes
# 已采集的原始NPZ可离线重导出，无需重新运行策略
"$PY" analysis/temporal_attention.py export --input <实际分析轨迹目录>
# 自动从实际E6成功/失败各选最小共同reset，运行E0/E1/E6成对分析
"$PY" analysis/dispatch_temporal.py --task StackCube-v1 --seed 0 --step 100000
```

默认调度器在相同任务/种子/100000更新的E0/E1/E6正式评测全部完成后，自动进入独立 `analysis_jobs`（分析队列）。其他指定保存点可用上面的命令直接分析。若没有真实成功或失败样本，选择清单明确写缺失原因，不补假轨迹。

每个重新规划时刻记录：原始RGB、米制Depth、机器人本体状态、规划动作块、实际执行动作、回合/重置ID；E6另外记录真实GSA轴向权重、指定Query派生传播权重、K个Token空间Softmax（归一化）权重及uv/d/rho。数据只在此分析流程采集，正式 `evaluate.py` 不存储注意力张量。

Query图来自实际宽轴、再高轴的注意力传播乘积，按头平均，**不包括残差和LEPE（局部位置编码）项**，不声称是完整Full-GSA矩阵。原始轴向权重可通过 `--save-axes` 保存。Token图是真实空间权重，不能称作分割真值。

E0/E1使用输入梯度显著性：固定扩散t=50、零归一化带噪动作的去噪epsilon输出平方均值对当前RGB求梯度。这是明确定义的敏感性探针，不是GSA注意力，也不声称直接解释随机采样动作的因果贡献。

阶段只来自直接官方环境事件或离线标注。StackCube可标记官方抓取/放置谓词；Peg仅标记官方插入成功事件。接近、搬运、对准等无直接事件的名称需提供明确标注：

```json
{"events": []}
```

添加标注时每项必须含 `name`, `start_step`, `end_step`, `source_kind`（`environment_event` 或 `offline_annotation`）及 `source`（环境源码谓词，或标注者/标注文件依据）。通过 `--stages path.json` 传入。无标注的帧仅称“时间点”，不会猜测操作阶段。

产物：完整MP4、每个关键时刻PNG、4–6时刻拼图、原始NPZ、`replans.jsonl`、`episode.json`、`temporal_manifest.json`；成对导出另外提供 `selection_manifest.json`、`comparison.json`、三方法同步MP4/PNG。视频在各动作执行期间保持对应重新规划观测，不把保持帧说成新的注意力采样。保留显示归一化方法与真实原始数值。

当前实现支持ManiSkill两任务；MimicGen适配依赖其真实RGB-D环境接口完成。没有指定的已训练新协议E6检查点时，不生成随机模型的论文结果。
