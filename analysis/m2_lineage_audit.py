"""Trace original Threading M2 five-point records and retained EMA bests."""
import sys,json,sqlite3,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'source/diffusion_policy')]
import torch,numpy as np
from gsc_dp.dataset import ManiSkillRGBDImageDataset
torch.set_num_threads(2)
OUT=ROOT/'docs/audit_55951414';OUT.mkdir(parents=True,exist_ok=True)
db=sqlite3.connect(ROOT/'jobs/ch3_final_queue.db');db.row_factory=sqlite3.Row
cleanup=[json.loads(s) for s in (ROOT/'experiments/ch3/checkpoint_cleanup.jsonl').read_text().splitlines()]
points=[];seeds=[]
normalizer_expected=None
for seed in [0,1,2]:
    run=ROOT/f'runs/mimicgen/threading_d2/e6/seed_{seed}'
    cfg=json.loads((run/'config_resolved.json').read_text());complete=json.loads((run/'training_complete.json').read_text())
    if normalizer_expected is None:
        dataset=ManiSkillRGBDImageDataset(cfg['zarr_path'],horizon=16,pad_before=1,pad_after=7,n_obs_steps=2,seed=0,val_ratio=0)
        normalizer_expected=dataset.get_normalizer().state_dict()
    train_records=[json.loads(s) for s in (run/'train_metrics.jsonl').read_text().splitlines()]
    for p in [50,100,150,200,250]:
        d=run/f'eval/epoch_{p:06d}';s=json.loads((d/'eval_summary.json').read_text());ep=[json.loads(x) for x in (d/'episodes.jsonl').read_text().splitlines()]
        meta=json.loads((run/f'checkpoints/epoch_{p:06d}.json').read_text())
        job=dict(db.execute("SELECT * FROM jobs WHERE kind='eval' AND task='threading_d2' AND method='e6' AND seed=? AND checkpoint_step=?",(seed,p)).fetchone())
        log=ROOT/f"logs/final_job_{job['id']}.log";log_records=[]
        for line in log.read_text(errors='replace').splitlines():
            try:log_records.append(json.loads(line))
            except ValueError:pass
        episode_logs=[x for x in log_records if 'reset_id' in x and 'episodes_completed' in x]
        summaries=[x for x in log_records if 'success_rate' in x and 'n_episodes' in x]
        n=sum(x['success_once'] for x in ep);end=sum(x['success_at_end'] for x in ep)
        source=Path(s['checkpoint_path'])
        deleted=[x for x in cleanup if x.get('action')=='deleted' and x.get('path')==str(source)]
        epoch_events=[x for x in train_records if x.get('event')=='epoch_complete' and x.get('completed_epochs')==p]
        revision=s['code_revision'];writer=subprocess.check_output(['git','show',revision+':gsc_dp/checkpoints.py'],cwd=ROOT,text=True)
        checks=dict(unique_50_episodes=len(ep)==50 and len({x['reset_id'] for x in ep})==50,exact_resets={x['reset_id'] for x in ep}==set(cfg['reset_ids']),all_episode_identity=all(x['method']=='e6' and x['seed']==seed and x['checkpoint_step']==p and x['checkpoint_path']==str(source) for x in ep),all_episode_success_matches_once=all(x['success']==x['success_once'] for x in ep),summary_count_matches=n==s['success_count'] and s['n_episodes']==50 and s['success_rate']==n/50,metadata_identity=all(s[k]==meta[k] for k in ['checkpoint_step','checkpoint_path','code_revision','method','seed']),metadata_declares_exact_ema=meta.get('snapshot_type')=='temporary_exact_fp32_ema',training_epoch_updates=bool(epoch_events) and all(x['optimizer_updates']==p*688 for x in epoch_events),episode_updates=all(x['optimizer_updates']==p*688 for x in ep),log_50_resets={x['reset_id'] for x in episode_logs}==set(cfg['reset_ids']),log_at_end_agrees=all(next(y for y in ep if y['reset_id']==x['reset_id'])['success_at_end']==x['success_at_end'] for x in episode_logs),log_summary_agrees=bool(summaries) and all(summaries[-1][k]==s[k] for k in ['success_count','n_episodes','success_rate','checkpoint_step','checkpoint_path']),queue_finished=job['status']=='finished',retention_accounted=source.exists() or bool(deleted),writer_ema_payload='ema_model' in writer and 'temporary_exact_fp32_ema' in writer)
        points.append(dict(seed=seed,epoch=p,success_once_count=n,success_at_end_count=end,n_episodes=len(ep),success_rate=s['success_rate'],optimizer_updates=p*688,training_code_revision=revision,evaluation_code_revision=s.get('evaluation_code_revision'),evaluation_code_revision_recorded=bool(s.get('evaluation_code_revision')),snapshot_type=meta.get('snapshot_type'),source_checkpoint_present=source.exists(),cleanup_record_count=len(deleted),summary=str(d/'eval_summary.json'),episode_records=str(d/'episodes.jsonl'),eval_log=str(log),checks=checks))
        points[-1]['checks']['camera_order_matches']=all(x['camera']==cfg['cameras'] for x in ep)
        points[-1]['checks']['all_episodes_exact_horizon']=all(x['horizon']==cfg['horizon'] and x['actual_steps']==cfg['horizon'] for x in ep)
    own=[x for x in points if x['seed']==seed];winner=min(own,key=lambda x:(-x['success_rate'],x['epoch']))
    bestmeta=json.loads((run/'best/best.json').read_text());best=torch.load(run/'best/best.pt',map_location='cpu',weights_only=False)
    keys=list(best['ema_model']);dtype_counts={str(x):sum(v.dtype==x for v in best['ema_model'].values()) for x in {v.dtype for v in best['ema_model'].values()}}
    actual_normalizer={k[len('normalizer.'):]:v for k,v in best['ema_model'].items() if k.startswith('normalizer.')}
    normalizer_matches=set(actual_normalizer)==set(normalizer_expected) and all(torch.equal(v,normalizer_expected[k]) for k,v in actual_normalizer.items())
    seeds.append(dict(seed=seed,training_complete=complete,expected_total_optimizer_updates=172000,winner_epoch=winner['epoch'],best_sr=winner['success_rate'],retained_best=str(run/'best/best.pt'),retained_payload_keys=list(best),ema_state_tensors=len(keys),ema_state_dtype_counts=dtype_counts,has_gsa=any('attention' in x for x in keys),has_tokenlearner=any('token_learner' in x for x in keys),has_normalizer=any('normalizer' in x for x in keys),checks=dict(total_training_budget=complete['optimizer_updates']==172000 and complete['completed_epochs']==250,earliest_best_tie=bestmeta['checkpoint_step']==winner['epoch'],best_summary_count=bestmeta['success_count']==winner['success_once_count'],best_ema_identity=best['checkpoint_step']==winner['epoch'] and best['optimizer_updates']==winner['epoch']*688 and best['config']['seed']==seed and best['config']['method']=='e6' and best['code_revision']==winner['training_code_revision'])))
    del best
    seeds[-1]['checks']['normalizer_matches_current_fixed_dataset']=normalizer_matches
all_ok=all(all(x['checks'].values()) for x in points+seeds)
result=dict(baseline='55951414',status='passed_record_and_retained_best_checks' if all_ok else 'checks_failed',points=points,seeds=seeds,mean_best_sr=float(np.mean([x['best_sr'] for x in seeds])),sample_std=float(np.std([x['best_sr'] for x in seeds],ddof=1)),limitation='All 15 original temporary checkpoints were reclaimed under the approved low-storage protocol. Metadata, creator code, training update logs, 750 episode records, evaluation logs and cleanup records are traced; only the 3 retained best EMA tensors can be directly inspected now. Deleted tensors cannot be compared byte-for-byte and no hashes are reconstructed.',invalidated_runs=[])
(OUT/'threading_m2_lineage.json').write_text(json.dumps(result,indent=2))
print(json.dumps(dict(status=result['status'],failed=[{k:x[k] for k in ['seed','checks']} for x in points+seeds if not all(x['checks'].values())],seeds=seeds,mean=result['mean_best_sr'],std=result['sample_std']),ensure_ascii=False),flush=True)
