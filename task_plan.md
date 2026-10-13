# GSC-DP 第三章：最终协议研究工程

## Goal
在 linzhenghong@10.0.8.2 的现有工程中，完成五任务、三种子、全部真实结果与第三章证据产出。

## Current Phase
Phase D 已启动ManiSkill正式训练；B/C及新增Phase G时序分析并行推进。

## Next Step
部署新增图3-15自动分析导出，扩展单卡队列至资源允许的并发并推进MimicGen RGB-D。

## Scope and precedence
- 用户2026-10-13最新指令：训练、评测、渲染只使用物理GPU2，可单卡并发。
- 用户禁止无意义冒烟、哈希和重复核验：采用原子checkpoint写入、元数据和源代码commit溯源，不堆权重哈希。
- 最终协议优先于旧计划；只复用旧数据和代码仓库；按用户最新要求不考虑旧规划和历史实验。
- 当前工程 /home/linzhenghong/project/gsc_dp_chapter3；新实验 campaign_v1；旧运行中源码保持独立。

## Phases
### Phase A: 恢复、资源、来源、协议、证据契约
Status: complete
完成标准：建立全新规划与资源记录；记录GPU/CPU/内存/磁盘；干净官方DP来源；协议与23项图表契约落盘。
产物：docs/protocol_sources.md, configs/protocol.json, thesis/figure_table_contract.yaml。
### Phase B: 五任务RGB-D与环境
Status: in_progress
完成标准：官方数据、同帧观测动作、单位、固定子集manifest、训练/在线一致性。
并行依赖：各任务独立，MimicGen尚需下载和兼容1.4仿真环境；ManiSkill已具备原始1000条RGB-D。
### Phase C: 基线与几何编码器
Status: in_progress
完成标准：原始动作U-Net/FiLM/噪声目标不变；GSA官方算子适配和Token几何真实梯度，必要的单次加载核对。
### Phase D: 正式训练与保存点评测
Status: in_progress
完成标准：0/1/2种子，MimicGen250epoch/每5/50episodes，ManiSkill100k更新/每5k/100episodes；独立不可变保存点、持久双队列、恢复。
### Phase E: 主流算法
Status: pending
依赖：相应官方模型适配和数据。未实现方法保持明确前置条件，不运行替代模型。
### Phase F: 完整消融、编码器、数据效率
Status: pending
依赖：核心实现；记录嵌套100/200/1000子集与交互。
### Phase G: 机制、干预、全部表图
Status: in_progress
新增独立任务G-T：机器人闭环执行过程中的时序注意力可视化（Fig 3-15）。
- [x] 复用现有GSA/Token capture接口，不重复静态开发。
- [x] 指定磁盘checkpoint真实独立rollout，按重新规划采集RGB/Depth/Query轴向注意力/K Token/状态/动作/episode。
- [x] MP4、4–6关键时刻PNG和JSON/NPZ元数据导出；E0/E1显著性与E6注意力明确区分。
- [x] 同reset E0/E1/E6真实成功失败成对导出及自动队列触发代码。
- [x] 环境直接事件或明确离线标注命名阶段，无标注只记时间点。
- [ ] 新协议E6真实保存点产生后运行分析，核对导出视频、图与实际轨迹对应。
- [x] MimicGen官方环境时序适配代码（实际数据配置/已训练checkpoint到位后核对）。
完成标准：指定保存点真实成功/失败轨迹、对应相同reset三方法对比、源文件和导出脚本可重建。
产物：analysis/temporal_paired, thesis/figure_table_contract.yaml::Fig 3-15。
正式训练预算、评测保存点和episode数完全保持最终协议。
依赖：真实权重/逐episode日志/离线GT；独占GPU时延需隔离时间窗口。
### Phase H: 完成度审查与论文证据交付
Status: pending
完成标准：所有图表结果可追溯、失败和未验证项明确、代码commit及复现说明。

## Errors Encountered
- 旧规划记录停留在“未启动”，实测已有10个历史训练；以实际进程、日志恢复。
- 历史tail查询logs.json.txt不存在：实际文件为metrics.jsonl。
- DFormer猜测路径models/DFormerv2.py 404：改为从官方checkout发现路径。


## Latest actual execution
Phase A协议/资源/官方源码/图表契约落盘；Phase B两ManiSkill固定100条子集完成；Phase C原版E0及官方GSA迁移代码已部署；Phase D两ManiSkill E0 seed0真实训练启动，首批>1000 updates。队列162项，48项核心/扩展ManiSkill配置已具备条件。MimicGen Threading/Coffee原始文件下载完成，Stack Three国内源中断待断点续传。

新增任务G-T部署状态：代码、两benchmark适配和契约已落盘，早期/最终保存点自动独立分析已入调度逻辑；尚未产生新协议E6时序MP4/PNG。该项不可标为真实结果完成。


## GitHub 发布追加任务
Status: complete
仓库 https://github.com/Lin-zh-handsome/depth，main分支。当前工程、规划及真实结果快照已发布；数据集和模型权重不上传。训练和评测继续在原服务器单卡队列运行。
