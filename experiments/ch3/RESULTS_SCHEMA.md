# 原始结果与汇总数据结构

`episode_results.csv/jsonl` 每episode至少字段：`eval_id, run_id, checkpoint_sha, task, method, seed, eval_index, progress, reset_id, success_at_end, success_once_if_supported, env_version, control_mode`。

`eval_results.csv` 每次评测至少字段：`eval_id, run_id, successes, episodes, sr, checkpoint_sha, result_file, status`，其中`sr = successes/episodes`。

`best_per_seed.csv`：每run恰好5个DONE且episodes齐全后，选最高SR；并列选**最早eval_index**，记录`best_sr`, `best_checkpoint_progress`, `best_checkpoint_sha`。

`final_results.csv`：对每任务每方法3seed的best_sr算mean、sample_std(ddof=1)和3个seed的明细；M1-M0、M2-M1的百分点增益需按对应任务完整实际结果计算。

注意：训练历史checkpoint不在新5点之一的成绩只可归档historical，绝不加入Best-of-5。未完成显示`PENDING`或`NOT_AVAILABLE`，不得补写。
