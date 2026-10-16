# 第三章实际状态

2026-10-16T08:25:14.386354+00:00

{"train": {"queued": 48, "finished": 9, "running": 3}, "eval": {"queued": 245, "finished": 54, "running": 1}, "analysis": {}}

完整回合 2700；已保存规定检查点 1。剩余GPU小时 UNKNOWN。

恢复：
```bash
cd /home/linzhenghong/project/gsc_dp_chapter3/campaign_v1 && PYTHONNOUSERSITE=1 nohup /home/linzhenghong/miniconda3/envs/gsc-robodiff/bin/python jobs/scheduler.py > logs/final_scheduler.log 2>&1 &
```

磁盘不足时资源门槛会暂停新作业；每个run保留best，临时权重评测完成后按引用清单回收。
