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
                row['checkpoint_root']=str(run/'checkpoints');row['log_path']=str(ROOT/'logs'/f"ch3_job_{r['id']}.log")
                frozen=run/'gpu_job.json'
                row['git_sha']=json.loads(frozen.read_text())['code_revision'] if frozen.exists() else ''
            else:
                resets=root/'eval_resets'/f"{r['task']}.json";row['eval_reset_manifest']=str(resets)
                tag='epoch' if r['benchmark']=='mimicgen' else 'update'
                summary=run/'eval'/f"{tag}_{r['checkpoint_step']:06d}"/'eval_summary.json'
                row['result_path']=str(summary) if summary.exists() else ''
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
        resume_command='cd '+str(ROOT)+' && PYTHONNOUSERSITE=1 nohup /home/linzhenghong/miniconda3/envs/gsc-robodiff/bin/python jobs/scheduler.py > logs/ch3_scheduler.log 2>&1 &')
    (root/'STATUS.json').write_text(json.dumps(status,indent=2))
    (root/'STATUS.md').write_text('# 第三章实际状态\n\n'+now+'\n\n'+json.dumps(counts)+'\n\n完整回合 '+str(episodes)+'；已保存规定检查点 '+str(checkpoint_count)+'。剩余GPU小时 UNKNOWN。\n\n恢复：\n```bash\n'+status['resume_command']+'\n```\n\n磁盘不足时资源门槛会暂停新作业；不删除真实权重。\n')
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
            best=[];last=[]
            for seed in t['seeds']:
                values=sorted(grouped[(t['task'],m,seed)],key=lambda p:p['progress'])
                if len(values)==t['savepoints']:
                    sr=[p['sr'] for p in values];best.append(max(sr));last.append(float(np.mean(sr[-10:])))
            stats.append(dict(task=t['task'],method=m,complete_seeds=len(best),best_mean=float(np.mean(best)) if len(best)==3 else '',
                best_std=float(np.std(best,ddof=1)) if len(best)==3 else '',last10_mean=float(np.mean(last)) if len(last)==3 else '',
                last10_std=float(np.std(last,ddof=1)) if len(last)==3 else '',status='DONE' if len(best)==3 else 'TODO'))
    write_csv(out/'tables/table3_2_best.csv',[{k:v for k,v in r.items() if not k.startswith('last10')} for r in stats])
    write_csv(out/'tables/table3_3_last10.csv',[{k:v for k,v in r.items() if not k.startswith('best')} for r in stats])
    for t in protocols:
        s={r['method']:r for r in stats if r['task']==t['task']}
        for metric in ['best','last10']:
            ready=all(r['status']=='DONE' for r in s.values())
            delta.append(dict(task=t['task'],metric=metric,gsa_pp=100*(s['M1'][metric+'_mean']-s['M0'][metric+'_mean']) if ready else '',
                token_given_gsa_pp=100*(s['M2'][metric+'_mean']-s['M1'][metric+'_mean']) if ready else '',
                full_pp=100*(s['M2'][metric+'_mean']-s['M0'][metric+'_mean']) if ready else '',status='DONE' if ready else 'TODO'))
    write_csv(out/'tables/module_deltas.csv',delta)
    marker=out/'source_data/exported_eval_count.json'
    changed=not marker.exists() or json.loads(marker.read_text())!=len(points)
    if changed and points:
        import matplotlib;matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        for t in protocols:
            fig,ax=plt.subplots(figsize=(6,3.8))
            for m in METHODS.values():
                for seed in t['seeds']:
                    v=sorted(grouped[(t['task'],m,seed)],key=lambda p:p['progress'])
                    if v:ax.plot([p['progress'] for p in v],[100*p['sr'] for p in v],label=f'{m}, seed {seed}')
            ax.set(xlabel='Dataset epochs' if t['benchmark']=='mimicgen' else 'Optimizer updates',ylabel='Success rate (%)',ylim=(0,100),title=t['task']+' (available real checkpoints)')
            if ax.lines:ax.legend(fontsize=7)
            fig.tight_layout();directory=out/'figures';directory.mkdir(exist_ok=True)
            for ext in ['png','pdf']:fig.savefig(directory/f"sr_{t['task']}.{ext}",dpi=200)
            (directory/f"sr_{t['task']}.json").write_text(json.dumps(dict(source=str(out/'source_data/checkpoint_sr.csv'),task=t['task'],missing_points='not imputed',three_seed_summary='pending until all three seeds have matching points')))
            plt.close(fig)
        marker.write_text(json.dumps(len(points)))
    md=out/'experiments_3_6.md'
    if not md.exists():md.write_text('''# 第三章 3.6 实验结果
## 3.6.1 实验平台和评价指标
两个Benchmark、五任务、三方法、三种子；固定预算见table3_1.csv。Best为周期评测最大值，具有择优偏差；Last10按时间取最终10保存点；跨种子样本标准差ddof=1。
## 3.6.2 五任务成功率比较
TODO：45-run矩阵完整数据到齐后引用table3_2_best.csv和table3_3_last10.csv。
## 3.6.3 GSA与TokenLearner递进式效果分析
TODO：module_deltas.csv。M0→M1包含Depth和GSA；M1→M2保持相同Depth/GSA。
## 3.6.4 空间注意力与时序关注可视化
TODO：独立checkpoint真实闭环轨迹、轴向GSA Query传播权重、8个Token空间权重；阶段名称来自环境事件或明确标注。
## 3.6.5 典型操作过程与失败案例
TODO：相同reset的M0/M1/M2成功和失败轨迹；正式成功率评测不采集完整注意力张量。
''')
if __name__=='__main__':main()
