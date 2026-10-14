"""Incremental matrix status and thesis statistics from complete real rollout logs."""
import csv,json,os,subprocess
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import numpy as np
from registry import ROOT,connect

METHODS={'e0':'M0','e3':'M1','e6':'M2'}
def write_csv(path,rows,fields=None):
    path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix('.tmp')
    with tmp.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
    os.replace(tmp,path)

def main():
    db=connect();jobs=[dict(x) for x in db.execute('SELECT * FROM jobs')]
    lookup={(r['kind'],r['benchmark'],r['task'],r['method'],r['seed'],r['checkpoint_step']):r for r in jobs}
    def job(row,kind):
        bm='maniskill' if row['benchmark']=='maniskill3' else row['benchmark']
        method={v:k for k,v in METHODS.items()}[row['method']]
        return lookup[(kind,bm,row['task'],method,int(row['seed']),int(row['checkpoint_progress']) if kind=='eval' else -1)]
    counts={kind:dict(Counter(r['status'] for r in jobs if r['kind']==kind)) for kind in ('train','eval','analysis')}
    protocols=json.loads((ROOT/'configs/protocol.json').read_text())['tasks']
    root=ROOT/'experiments/ch3';out=ROOT/'thesis/chapter3';out.mkdir(parents=True,exist_ok=True)
    points=[];episodes=0;checkpoint_count=0
    for filename,kind in [('run_manifest.csv','train'),('eval_manifest.csv','eval')]:
        rows=list(csv.DictReader((root/filename).open()))
        for row in rows:
            r=job(row,kind);state=r['status'];row['status']={'finished':'DONE','running':'RUNNING','queued':'PENDING','failed':'FAILED'}.get(state,state.upper())
            row['notes']=r['error'] or r['prerequisite'] or 'real config/demo IDs/git revision/atomic metadata; hashing omitted by user instruction'
            run=ROOT/'runs'/r['benchmark']/r['task']/r['method']/f"seed_{r['seed']}"
            if kind=='train':
                row['best_inference_path']=str(run/'best/best.pt') if (run/'best/best.pt').exists() else '';row['latest_resume_path']=str(run/'checkpoints/recovery.pt') if (run/'checkpoints/recovery.pt').exists() else '';row['log_path']=str(ROOT/'logs'/f"final_job_{r['id']}.log")
                frozen=run/'gpu_job.json'
                row['git_sha']=json.loads(frozen.read_text())['code_revision'] if frozen.exists() else ''
            else:
                resets=root/'eval_resets'/f"{r['task']}.json";row['eval_reset_manifest']=str(resets)
                tag='epoch' if r['benchmark']=='mimicgen' else 'update'
                summary=run/'eval'/f"{tag}_{r['checkpoint_step']:06d}"/'eval_summary.json'
                row['result_path']=str(summary) if summary.exists() else '';row['eval_snapshot_path']=r['checkpoint_path'] or '';row['snapshot_artifact_state']='PRESENT' if r['checkpoint_path'] and Path(r['checkpoint_path']).exists() else 'RECLAIMED' if state=='finished' else 'NOT_CREATED'
                if r['checkpoint_path'] and Path(r['checkpoint_path']).exists():checkpoint_count+=1
                if state=='finished':
                    s=json.loads(summary.read_text());episodes+=s['n_episodes']
                    points.append(dict(task=r['task'],method=METHODS[r['method']],seed=r['seed'],progress=r['checkpoint_step'],
                        sr=s['success_rate'],episodes=s['n_episodes'],successes=s['success_count'],checkpoint_path=r['checkpoint_path'],
                        eval_manifest=str(root/'eval_manifest.csv'),episodes_path=s['episodes_path']))
        write_csv(root/filename,rows)
    now=datetime.now(timezone.utc).isoformat();live=[r for r in jobs if r['status']=='running']
    status=dict(timestamp=now,counts=counts,scheduled_checkpoint_files=checkpoint_count,complete_rollout_episodes=episodes,
        running=live,gpu='physical GPU2 only',remaining_gpu_hours='UNKNOWN: no stable per-task throughput estimate',
        resume_command='cd '+str(ROOT)+' && PYTHONNOUSERSITE=1 nohup /home/linzhenghong/miniconda3/envs/gsc-robodiff/bin/python jobs/scheduler.py > logs/final_scheduler.log 2>&1 &')
    previous=json.loads((root/'STATUS.json').read_text()) if (root/'STATUS.json').exists() else {}
    if previous.get('counts')!=counts:
        for plan in [ROOT,ROOT.parent/'.planning/protocol_v1']:
            summary='\n\n## 实际运行状态（自动更新）\n'+now+'\n45训练、225正式评测。'+json.dumps(counts)+'；完整回合 '+str(episodes)+'。全部工作只用物理GPU2。队列入队不等于实验完成。\n'
            for name in ['task_plan.md','findings.md']:
                path=plan/name
                original=path.read_text(encoding='utf-8')
                marker='\n\n## 实际运行状态（自动更新）'
                start=original.find(marker)
                if start<0:
                    updated=original+summary
                else:
                    end=original.find('\n## ',start+len(marker))
                    updated=original[:start]+summary+(original[end:] if end>=0 else '')
                path.write_text(updated,encoding='utf-8')
            with (plan/'progress.md').open('a',encoding='utf-8') as f:f.write(summary)
    (root/'STATUS.json').write_text(json.dumps(status,indent=2))
    (root/'STATUS.md').write_text('# 第三章实际状态\n\n'+now+'\n\n'+json.dumps(counts)+'\n\n完整回合 '+str(episodes)+'；已保存规定检查点 '+str(checkpoint_count)+'。剩余GPU小时 UNKNOWN。\n\n恢复：\n```bash\n'+status['resume_command']+'\n```\n\n磁盘不足时资源门槛会暂停新作业；每个run保留best，临时权重评测完成后按引用清单回收。\n')
    protocol_rows=[]
    for t in protocols:
        protocol_rows.append({k:t[k] for k in ['benchmark','task','demos','budget','progress_unit','interval','episodes','horizon','control_mode']})
        reset_dir=root/'eval_resets';reset_dir.mkdir(exist_ok=True)
        (reset_dir/f"{t['task']}.json").write_text(json.dumps(dict(task=t['task'],reset_ids=t['reset_ids'],episodes=t['episodes'],horizon=t['horizon'])))
    write_csv(out/'tables/table3_1.csv',protocol_rows)
    (out/'tables/table3_1.json').write_text(json.dumps(dict(protocol=str(ROOT/'configs/protocol.json'),dataset_manifests=str(ROOT/'data/manifests')),indent=2))
    write_csv(out/'source_data/checkpoint_sr.csv',points,['task','method','seed','progress','sr','episodes','successes','checkpoint_path','eval_manifest','episodes_path'])
    grouped=defaultdict(list)
    for p in points:grouped[(p['task'],p['method'],p['seed'])].append(p)
    stats=[];delta=[]
    for t in protocols:
        for m in METHODS.values():
            best=[]
            for seed in t['seeds']:
                values=sorted(grouped[(t['task'],m,seed)],key=lambda p:p['progress'])
                if len(values)==t['savepoints']:
                    sr=[p['sr'] for p in values];best.append(max(sr))
            stats.append(dict(task=t['task'],method=m,complete_seeds=len(best),best_mean=float(np.mean(best)) if len(best)==3 else '',
                best_std=float(np.std(best,ddof=1)) if len(best)==3 else '',status='DONE' if len(best)==3 else 'TODO'))
    write_csv(out/'tables/table3_2_best.csv',stats)
    write_csv(root/'final_results.csv',stats)
    seed_stats=[]
    for key,values in grouped.items():
        if len(values)==5:
            winner=min(values,key=lambda p:(-p['sr'],p['progress']))
            seed_stats.append(dict(task=key[0],method=key[1],seed=key[2],best_sr=winner['sr'],best_checkpoint_progress=winner['progress'],best_checkpoint_path=str(ROOT/'runs'/('mimicgen' if key[0] in ['stack_three_d1','threading_d2','coffee_d2'] else 'maniskill')/key[0]/{v:k for k,v in METHODS.items()}[key[1]]/f'seed_{key[2]}'/'best/best.pt'),status='DONE'))
    write_csv(root/'best_per_seed.csv',seed_stats,['task','method','seed','best_sr','best_checkpoint_progress','best_checkpoint_path','status'])
    write_csv(root/'eval_results.csv',points,['task','method','seed','progress','sr','episodes','successes','checkpoint_path','eval_manifest','episodes_path'])
    for t in protocols:
        s={r['method']:r for r in stats if r['task']==t['task']}
        for metric in ['best']:
            ready=all(r['status']=='DONE' for r in s.values())
            delta.append(dict(task=t['task'],metric=metric,gsa_pp=100*(s['M1'][metric+'_mean']-s['M0'][metric+'_mean']) if ready else '',
                token_given_gsa_pp=100*(s['M2'][metric+'_mean']-s['M1'][metric+'_mean']) if ready else '',
                full_pp=100*(s['M2'][metric+'_mean']-s['M0'][metric+'_mean']) if ready else '',status='DONE' if ready else 'TODO'))
    write_csv(out/'tables/module_deltas.csv',delta)
    for name in ['table3_2_best','module_deltas']:
        (out/'tables'/f'{name}.json').write_text(json.dumps(dict(source=str(root/'eval_manifest.csv'),raw_episode_source=str(out/'source_data/checkpoint_sr.csv'),statistics='Best-of-5, three independent seeds, sample std ddof=1, earliest tie'),indent=2))
    marker=out/'source_data/exported_eval_count.json'
    changed=not marker.exists() or json.loads(marker.read_text())!=len(points)
    if changed and points:
        import matplotlib;matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        for t in protocols:
            fig,ax=plt.subplots(figsize=(6,3.8))
            for m in METHODS.values():
                per_point=defaultdict(list)
                for seed in t['seeds']:
                    v=sorted(grouped[(t['task'],m,seed)],key=lambda p:p['progress'])
                    if v:ax.plot([p['progress'] for p in v],[100*p['sr'] for p in v],label=f'{m}, seed {seed}')
                    for p in v:per_point[p['progress']].append(p['sr']*100)
                complete=sorted(k for k,v in per_point.items() if len(v)==3)
                if complete:
                    mean=np.array([np.mean(per_point[k]) for k in complete]);std=np.array([np.std(per_point[k],ddof=1) for k in complete])
                    line=ax.plot(complete,mean,label=m+' mean (3 seeds)',linewidth=2.5)[0]
                    ax.fill_between(complete,mean-std,mean+std,color=line.get_color(),alpha=.15)
            ax.set(xlabel='Dataset epochs' if t['benchmark']=='mimicgen' else 'Optimizer updates',ylabel='Success rate (%)',ylim=(0,100),title=t['task']+' (available real checkpoints)')
            if ax.lines:ax.legend(fontsize=7)
            fig.tight_layout();directory=out/'figures';directory.mkdir(exist_ok=True)
            for ext in ['png','pdf']:fig.savefig(directory/f"sr_{t['task']}.{ext}",dpi=200)
            (directory/f"sr_{t['task']}.json").write_text(json.dumps(dict(source=str(out/'source_data/checkpoint_sr.csv'),task=t['task'],missing_points='not imputed',three_seed_summary='pending until all three seeds have matching points')))
            plt.close(fig)
            fig,ax=plt.subplots(figsize=(6,3.8));loss_rows=[]
            for method,name in METHODS.items():
                for seed in t['seeds']:
                    log=ROOT/'runs'/t['benchmark']/t['task']/method/f'seed_{seed}'/'train_metrics.jsonl'
                    if not log.exists():continue
                    vals=[json.loads(x) for x in log.read_text().splitlines() if x.strip()]
                    vals=[x for x in vals if 'train_loss' in x]
                    if vals:ax.plot([x['optimizer_updates'] for x in vals],[x['train_loss'] for x in vals],label=f'{name}, seed {seed}',alpha=.7)
                    loss_rows.extend(dict(method=name,seed=seed,optimizer_updates=x['optimizer_updates'],train_loss=x['train_loss'],log_path=str(log)) for x in vals)
            ax.set(xlabel='Optimizer updates',ylabel='Diffusion training loss',title=t['task'])
            if ax.lines:ax.legend(fontsize=7)
            fig.tight_layout()
            for ext in ['png','pdf']:fig.savefig(directory/f"loss_{t['task']}.{ext}",dpi=200)
            write_csv(out/'source_data'/f"loss_{t['task']}.csv",loss_rows,['method','seed','optimizer_updates','train_loss','log_path'])
            (directory/f"loss_{t['task']}.json").write_text(json.dumps(dict(source=str(out/'source_data'/f"loss_{t['task']}.csv"))))
            plt.close(fig)
        marker.write_text(json.dumps(len(points)))
    md=out/'experiments_3_6.md'
    if not md.exists():md.write_text('''# 第三章 3.6 实验结果
## 3.6.1 实验平台和评价指标
两个Benchmark、五任务、三方法、三种子；固定预算见table3_1.csv。Best为周期评测最大值，具有择优偏差；Best-of-5限定五个预注册位置，并列选最早；跨种子样本标准差ddof=1。
## 3.6.2 五任务成功率比较
TODO：45-run矩阵完整数据到齐后引用table3_2_best.csv。
## 3.6.3 GSA与TokenLearner递进式效果分析
TODO：module_deltas.csv。M0→M1包含Depth和GSA；M1→M2保持相同Depth/GSA。
## 3.6.4 空间注意力与时序关注可视化
TODO：独立checkpoint真实闭环轨迹、轴向GSA Query传播权重、8个Token空间权重；阶段名称来自环境事件或明确标注。
## 3.6.5 典型操作过程与失败案例
TODO：相同reset的M0/M1/M2成功和失败轨迹；正式成功率评测不采集完整注意力张量。
''')
if __name__=='__main__':main()
