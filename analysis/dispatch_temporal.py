"""Automatically export paired successful/failed real trajectories for E0/E1/E6."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--task',required=True);p.add_argument('--seed',type=int,required=True)
    p.add_argument('--benchmark',choices=['maniskill','mimicgen'],default='maniskill')
    p.add_argument('--step',type=int,required=True);p.add_argument('--stages-dir',type=Path)
    args=p.parse_args();methods=['e0','e3','e6'];runs={}
    for method in methods:
        tag=('epoch' if args.benchmark=='mimicgen' else 'update')+f'_{args.step:06d}'
        run=ROOT/'runs'/args.benchmark/args.task/method/f'seed_{args.seed}'
        best=json.loads((run/'best/best.json').read_text())
        cp=run/'best/best.pt'
        source_tag=('epoch' if args.benchmark=='mimicgen' else 'update')+f"_{best['checkpoint_step']:06d}"
        ep=run/'eval'/source_tag/'episodes.jsonl'
        if not cp.exists() or not ep.exists():raise FileNotFoundError(f'paired source unavailable: {cp}, {ep}')
        runs[method]=dict(run=run,checkpoint=cp,episodes={r['reset_id']:r for r in [json.loads(x) for x in ep.read_text().splitlines()]})
    common=set.intersection(*(set(r['episodes']) for r in runs.values()))
    # Fixed selection: smallest common reset for each E6 official end-outcome.
    selected=[];unavailable=[]
    for outcome in [True,False]:
        candidates=sorted(i for i in common if bool(runs['e6']['episodes'][i].get('success') if args.benchmark=='mimicgen' else runs['e6']['episodes'][i].get('success_at_end'))==outcome)
        if candidates:selected.append(dict(reset_id=candidates[0],reference_outcome=outcome))
        else:unavailable.append(dict(reference_outcome=outcome,reason='no matching E6 outcome in actual paired eval episodes'))
    dest=ROOT/'analysis/temporal_paired'/args.task/f'seed_{args.seed}'/tag
    dest.mkdir(parents=True,exist_ok=True)
    (dest/'selection_manifest.json').write_text(json.dumps(dict(selection_rule='smallest shared reset ID for E6 success and failure',
        selected=selected,unavailable=unavailable,checkpoints={m:str(r['checkpoint']) for m,r in runs.items()}),indent=2))
    for selection in selected:
        outputs=[]
        for method in methods:
            target=dest/f"reset_{selection['reset_id']}"/method;outputs.append(target)
            if (target/'temporal_manifest.json').exists():continue
            command=[sys.executable,str(ROOT/'analysis/temporal_attention.py'),'collect',
                '--checkpoint',str(runs[method]['checkpoint']),'--reset-id',str(selection['reset_id']),
                '--output',str(target),'--save-axes']
            if args.stages_dir:
                stages=args.stages_dir/f"{args.task}_reset_{selection['reset_id']}.json"
                if stages.exists():command+=['--stages',str(stages)]
            subprocess.run(command,check=True,cwd=ROOT)
        subprocess.run([sys.executable,str(ROOT/'analysis/temporal_attention.py'),'compare','--inputs',
            *map(str,outputs),'--output',str(dest/f"reset_{selection['reset_id']}"/'comparison')],check=True,cwd=ROOT)
    print('paired temporal exports',dest,flush=True)

if __name__=='__main__':main()
