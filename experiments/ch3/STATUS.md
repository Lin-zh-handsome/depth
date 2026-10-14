# 第三章实际状态

2026-10-14T03:34:45.067171+00:00

{"train": {"queued": 45}, "eval": {"finished": 13, "queued": 1697}, "analysis": {}}

完整回合 650；已保存规定检查点 86。剩余GPU小时 UNKNOWN。

恢复：
```bash
cd /home/linzhenghong/project/gsc_dp_chapter3/campaign_v1 && PYTHONNOUSERSITE=1 nohup /home/linzhenghong/miniconda3/envs/gsc-robodiff/bin/python jobs/scheduler.py > logs/ch3_scheduler.log 2>&1 &
```

磁盘不足时资源门槛会暂停新作业；不删除真实权重。
