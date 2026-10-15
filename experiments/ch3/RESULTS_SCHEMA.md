# 原始结果与汇总数据结构

`episode_results.csv/jsonl` 每episode至少字段：`eval_id, run_id, checkpoint_sha, task, method, seed, eval_index, progress, reset_id, success_at_end, success_once_if_supported, env_version, control_mode`。

`eval_results.csv` 每次评测至少字段：`eval_id, run_id, successes, episodes, sr, checkpoint_sha, result_file, status`，其中`sr = successes/episodes`。

`best_per_seed.csv`：每run恰好5个DONE且episodes齐全后，选最高SR；并列选**最早eval_index**，记录`best_sr`, `best_checkpoint_progress`, `best_checkpoint_sha`。

`final_results.csv`：对每任务每方法3seed的best_sr算mean、sample_std(ddof=1)和3个seed的明细；M1-M0、M2-M1的百分点增益需按对应任务完整实际结果计算。

注意：训练历史checkpoint不在新5点之一的成绩只可归档historical，绝不加入Best-of-5。未完成显示`PENDING`或`NOT_AVAILABLE`，不得补写。

2026-10-15审查修订：实际正式逐回合文件为`runs/.../eval/.../episodes.jsonl`；保留`success_once`（过程中曾成功）、`success_at_end`（末步成功）以及实际计分的`success`字段。MimicGen的`success=success_once`，ManiSkill的`success=success_at_end`。汇总CSV、论文主表/消融和JSON元数据均增加`success_definition`，禁止将两个Benchmark（基准）的口径混写为统一末步成功率。历史描述性`success_definition`保存在`success_definition_original`，原数值不改。

按用户要求不计算权重哈希：`checkpoint_sha`允许为空，实际追溯使用checkpoint（检查点）路径、训练源码提交、EMA（指数滑动平均）类型、训练更新数、固定reset（重置）列表、原始回合和安全清理记录；不凭空补写已回收张量的哈希或逐位一致性结论。当前四模型60训练/300评测，M3只追加既定15训练/75评测，旧ID不改。
