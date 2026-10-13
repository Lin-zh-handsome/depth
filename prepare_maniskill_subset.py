"""Select fixed 100 official replay episodes without changing action semantics."""
import json
import os
from pathlib import Path
import numpy as np
import zarr
from numcodecs import Blosc, blosc
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'diffusion_policy/data/maniskill/datasets'
blosc.set_nthreads(2)
for task in ['StackCube-v1','PegInsertionSide-v1']:
    target=ROOT/'data/processed'/task/'subset100.zarr'
    manifest=ROOT/'data/manifests'/f'{task}_100.json'
    if manifest.exists() and target.exists(): continue
    source=OLD/task/'trajectory.zarr'
    r=zarr.open(str(source),'r')
    ends=r['meta/episode_ends'][:100]
    assert len(ends)==100
    n=int(ends[-1])
    tmp=target.with_name(target.name+'.partial')
    tmp.parent.mkdir(parents=True,exist_ok=True)
    out=zarr.open(str(tmp),'a')
    data=out.require_group('data'); meta=out.require_group('meta')
    for key in r['data'].array_keys():
        a=r['data'][key]
        b=data.require_dataset(key,shape=(n,*a.shape[1:]),dtype=a.dtype,chunks=a.chunks,
            compressor=Blosc(cname='zstd',clevel=3,shuffle=Blosc.BITSHUFFLE))
        for start in range(0,n,256): b[start:start+256]=a[start:min(start+256,n)]
        print(task,key,n,flush=True)
    meta.array('episode_ends',ends,overwrite=True)
    old=json.loads((OLD/task/'conversion_manifest.json').read_text())
    replay_meta=Path(old['source']).with_suffix('.json')
    episodes=json.loads(replay_meta.read_text())['episodes'][:100]
    ids=[e['episode_id'] for e in episodes]
    if len(set(ids))!=100: raise ValueError('nonunique official trajectory ids')
    old.update(n_episodes=100,n_steps=n,subset_ids=ids,subset_rule='first100 in the existing official replay order',
        processed_path=str(target),raw_replay_metadata=str(replay_meta),
        control_mode='pd_joint_pos',policy_information='RGB-D and proprioception only',
        offline_gt='not present in processed policy data')
    os.replace(tmp,target)
    manifest.parent.mkdir(parents=True,exist_ok=True)
    manifest.write_text(json.dumps(old,indent=2))
    print('ready',task,flush=True)
