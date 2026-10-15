"""Actual final-protocol monitoring; never launches or stops a worker."""
from pathlib import Path
import datetime, json, math, os, shutil, sqlite3, subprocess, time

root = Path('/home/linzhenghong/project/gsc_dp_chapter3/campaign_v1')
planning = root.parent / '.planning/protocol_v1'
GPU = 'GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9'
for name in ['task_plan.md', 'findings.md', 'progress.md']:
    (planning / name).read_text(encoding='utf8')
target = root / 'experiments/ch3/monitoring_manifest.json'
previous = json.loads(target.read_text()) if target.exists() else {}
stamp = datetime.datetime.now().astimezone().isoformat()
db = sqlite3.connect(root / 'jobs/ch3_final_queue.db')
db.row_factory = sqlite3.Row
counts = [dict(x) for x in db.execute('SELECT kind,status,count(*) AS count FROM jobs GROUP BY kind,status')]
live, results, issues = [], [], []
for job in db.execute("SELECT * FROM jobs WHERE status IN ('running','finished','failed') ORDER BY kind,id"):
    row = {k: job[k] for k in ['id', 'kind', 'benchmark', 'task', 'method', 'seed', 'checkpoint_step', 'status', 'pid']}
    run = root / 'runs' / job['benchmark'] / job['task'] / job['method'] / f"seed_{job['seed']}"
    if job['status'] == 'failed':
        issues.append(f"job {job['id']} failed: {job['error']}")
    if job['status'] == 'running':
        proc = Path('/proc') / str(job['pid'])
        try:
            argv = proc.joinpath('cmdline').read_bytes().decode().replace('\0', ' ')
            env = dict(x.split('=', 1) for x in proc.joinpath('environ').read_bytes().decode().split('\0') if '=' in x)
            row['alive'] = proc.stat().st_uid == os.getuid() and str(root) in argv
            row['visible_gpu'] = env.get('CUDA_VISIBLE_DEVICES')
        except OSError:
            row['alive'] = False
        if not row['alive']:
            issues.append(f"job {job['id']} process missing")
        if row.get('visible_gpu') != GPU:
            issues.append(f"job {job['id']} GPU binding unexpected")
    if job['kind'] == 'train':
        p = run / 'train_metrics.jsonl'
        lines = p.read_text().splitlines() if p.exists() else []
        row['latest_metric'] = json.loads(lines[-1]) if lines else {}
        row['metric_age_seconds'] = round(time.time() - p.stat().st_mtime) if p.exists() else None
        old = next((x for x in previous.get('running', []) if x['id'] == job['id']), {}).get('latest_metric', {}).get('optimizer_updates')
        row['updates_since_last_poll'] = row['latest_metric'].get('optimizer_updates', old) - old if old is not None else None
        last_loss = next((json.loads(x) for x in reversed(lines) if 'train_loss' in x), None)
        if last_loss and not math.isfinite(last_loss['train_loss']):
            issues.append(f"job {job['id']} nonfinite loss")
        log = root / 'logs' / f"final_job_{job['id']}.log"
        row['waiting_for_eval'] = log.exists() and 'run backpressure: awaiting scheduled evaluation' in log.read_text() and (row['metric_age_seconds'] or 0) > 600
    elif job['kind'] == 'eval':
        tag = 'epoch' if job['benchmark'] == 'mimicgen' else 'update'
        folder = run / 'eval' / f"{tag}_{job['checkpoint_step']:06d}"
        p = folder / 'episodes.jsonl'
        episodes = [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []
        row['episodes_completed'] = len(episodes)
        p = folder / 'eval_summary.json'
        if job['status'] == 'finished' and p.exists():
            result = json.loads(p.read_text())
            cfg = json.loads((run / 'config_resolved.json').read_text())
            complete = len(episodes) == cfg['episodes'] and {x['reset_id'] for x in episodes} == set(cfg['reset_ids'])
            if not complete:
                issues.append(f"job {job['id']} finished but reset records incomplete")
            results.append({**row, **{k: result[k] for k in ['success_count', 'n_episodes', 'success_rate']}, 'exact_reset_list': complete, 'summary_path': str(p)})
    if job['status'] == 'running':
        live.append(row)

resources = {}
for label, cmd in [('cpu', ['uptime']), ('memory', ['free', '-h']), ('gpu2', ['nvidia-smi', '-i', GPU, '--query-gpu=uuid,memory.free,utilization.gpu', '--format=csv,noheader'])]:
    try:
        resources[label] = subprocess.run(cmd, capture_output=True, text=True, timeout=8).stdout.strip()
    except subprocess.TimeoutExpired:
        resources[label] = 'query timeout'
cleanup = root / 'experiments/ch3/checkpoint_cleanup.jsonl'
deleted = [json.loads(x) for x in cleanup.read_text().splitlines() if json.loads(x).get('action') == 'deleted'] if cleanup.exists() else []
best = root / 'runs/mimicgen/stack_three_d1/e0/seed_0/best/best.json'
best_metadata = json.loads(best.read_text()) if best.exists() else None
report = dict(checked_at_asia_shanghai=stamp, previous_poll=previous.get('checked_at_asia_shanghai'),
              protocol='four_models_60_train_300_eval', counts=counts, running=live, complete_formal_evaluations=results,
              issues=issues, resources=resources, disk_free_bytes=shutil.disk_usage(root).free,
              pause_marker_present=(root / 'jobs/PAUSED_BY_USER.json').exists(),
              dataset_manifests_ready=sorted(p.name for p in (root / 'data/manifests').glob('*.json')),
              provisional_best=best_metadata,
              checkpoint_cleanup=dict(files_deleted=len(deleted), bytes_reclaimed=sum(x['bytes'] for x in deleted)),
              note='Per-point SR and provisional best are not complete five-point or three-seed statistics.')
target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
old_ids = {x['id'] for x in previous.get('complete_formal_evaluations', [])}
new = [x for x in results if x['id'] not in old_ids]
point_text = '; '.join(f"{x['task']}/{x['method']}/seed{x['seed']}/{x['checkpoint_step']}: {x['success_count']}/{x['n_episodes']}={x['success_rate']:.0%}" for x in new)
entry = f"\n\n## 每小时巡检 {stamp}\n完整正式评测{len(results)}/300，共{sum(x['n_episodes'] for x in results)}回合；新增：{point_text or '无'}。队列{json.dumps(counts, ensure_ascii=False)}。问题：{issues or '无'}。实际进程、GPU2绑定、训练增长和评测部分回合详见experiments/ch3/monitoring_manifest.json；论文源数据由既有导出程序增量更新。\n"
with (planning / 'progress.md').open('a', encoding='utf8') as f:
    f.write(entry)
with (planning / 'task_plan.md').open('a', encoding='utf8') as f:
    f.write(f"\n\n## 巡检进度 {stamp}\n完整正式评测{len(results)}/300；新增{point_text or '无'}。全部训练评测保持原预算、控制模式与GPU2绑定。\n")
if new or issues:
    with (planning / 'findings.md').open('a', encoding='utf8') as f:
        f.write(f"\n\n## 巡检发现 {stamp}\n新增正式保存点：{point_text or '无'}。异常：{issues or '无'}。当前仅记录完整逐回合结果；未完成五点及三种子前不报告最终统计。\n")
for name in ['task_plan.md', 'findings.md', 'progress.md']:
    (root / name).write_text((planning / name).read_text(encoding='utf8'), encoding='utf8')
print(json.dumps(dict(counts=counts, new_results=new, issues=issues, running_metrics=live), ensure_ascii=False))
