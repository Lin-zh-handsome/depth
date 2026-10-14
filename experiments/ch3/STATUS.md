# 第三章实际状态

2026-10-14T11:02:44.590660+00:00

{"train": {"queued": 37, "running": 3, "held_for_full_method": 4, "finished": 1}, "eval": {"queued": 214, "finished": 10, "held_for_full_method": 1}, "analysis": {}}

完整回合 500；已保存规定检查点 1。剩余GPU小时 UNKNOWN。

恢复：
```bash
cd /home/linzhenghong/project/gsc_dp_chapter3/campaign_v1 && PYTHONNOUSERSITE=1 nohup /home/linzhenghong/miniconda3/envs/gsc-robodiff/bin/python jobs/scheduler.py > logs/final_scheduler.log 2>&1 &
```

磁盘不足时资源门槛会暂停新作业；每个run保留best，临时权重评测完成后按引用清单回收。
