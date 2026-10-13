# GSC-DP 硕士论文第三章研究工程

五任务、三训练种子的 GSC-DP（几何空间约束扩散策略）研究工程。训练和评测依据 `docs/inputs/GSC_DP_第三章最终实验协议.md`；当前实验正在执行，尚未完成全套论文实验。

## 仓库内容

- `train.py`、`evaluate.py`：正式训练及独立检查点评测。
- `gsc_dp/`：原始扩散策略接口、GSA（几何空间注意力）、TokenLearner（空间标记学习器）和几何描述。
- `jobs/`：可恢复训练、评测和独立分析队列；全部任务绑定服务器物理 GPU 2。
- `configs/`、`data/manifests/`：固定预算、模型配置及数据来源/示范子集清单；不包含数据本体。
- `analysis/`：真实闭环时序注意力、明确标注的基线显著性、同一重置编号对比和视频/图像导出。
- `thesis/figure_table_contract.yaml`：论文图表来源及自动导出契约。
- `task_plan.md`、`findings.md`、`progress.md`：发布时的当前规划快照。服务器持续更新的原件位于工程父目录 `.planning/protocol_v1/`。
- `docs/inputs/`：最终协议、完整执行说明和第三章论文初稿。
- `artifacts/snapshot_20261013/`：真实训练日志、逐回合评测记录、评测轨迹、队列状态及检查点路径清单。采集时仍在运行的日志保留部分进度，只有完整 `eval_summary.json` 表示该保存点评测完成；早期保存点结果不是最终论文结论。

## 官方依赖源码

`source/diffusion_policy`、`source/DFormer`、`source/mimicgen` 是固定源代码提交的 Git submodule（子模块）。下载工程及依赖：

```bash
git clone --recurse-submodules https://github.com/Lin-zh-handsome/depth.git
```

现有服务器环境采用 Conda：训练 `gsc-robodiff`、ManiSkill（机器人仿真基准）评测 `gsc-thesis-eval`、MimicGen（示范生成与仿真基准）评测 `gsc-thesis-mimic`。环境调整脚本依赖现有训练环境；MimicGen 使用已有官方 robomimic 0.4 源码。仓库目前保留实际服务器路径，迁移服务器需调整配置中的数据及环境路径，不宣称新机器开箱即用。

## 数据与模型权重

数据集原文件及转换后的训练数据位于服务器 `data/raw/`、`data/processed/`，按用户要求不上传。来源、示范编号、单位及控制模式保留在数据清单和 `docs/protocol_sources.md`。

单个完整训练检查点约 5.3 GB，超过普通 GitHub Git 单文件限制，权重继续保留在服务器。实际保存点和对应元数据记录在 `artifacts/snapshot_20261013/checkpoint_catalog.json`，本仓库没有可直接下载的训练权重。

时序注意力任务及数据效率等后续实验的完成情况以规划文件和真实产物为准。未产生的论文视频、图或最终统计不以示意结果代替。
