"""Recoverable official state→RGB-D conversion of fixed 200-demo Core subsets."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import h5py
import numpy as np
import zarr
from numcodecs import Blosc,blosc
ROOT=Path(__file__).resolve().parent
blosc.set_nthreads(2)

def main():
    import robomimic
    official=Path(robomimic.__file__).parent/'scripts/dataset_states_to_obs.py'
    for task in ['stack_three_d1','threading_d2','coffee_d2']:
        raw=ROOT/'data/raw/mimicgen'/f'{task}.hdf5'
        directory=ROOT/'data/processed'/task;directory.mkdir(parents=True,exist_ok=True)
        subset=directory/'states_200.hdf5';rgbd=directory/'rgbd_200.hdf5'
        target=directory/'subset200.zarr';manifest=ROOT/'data/manifests'/f'{task}_200.json'
        if manifest.exists():continue
        with h5py.File(raw,'r') as src:
            ids=sorted(src['data'],key=lambda x:int(x.split('_')[-1]))[:200]
            if len(ids)!=200:raise ValueError('official Core dataset has fewer than 200 demos')
            meta=json.loads(src['data'].attrs['env_args'])
            if not subset.exists():
                tmp=subset.with_suffix('.partial')
                with h5py.File(tmp,'w') as dst:
                    data=dst.create_group('data')
                    for k,v in src['data'].attrs.items():data.attrs[k]=v
                    for key in ids:src.copy(src['data'][key],data,name=key)
                    data.attrs['total']=sum(src['data'][key]['actions'].shape[0] for key in ids)
                os.replace(tmp,subset)
        (directory/'subset_200.json').write_text(json.dumps(dict(task=task,source=str(raw),ids=ids),indent=2))
        (directory/'subset_100.json').write_text(json.dumps(dict(task=task,source=str(raw),ids=ids[:100]),indent=2))
        # The official converter creates a new output; never change action semantics.
        if not rgbd.exists():
            part=directory/'rgbd_200.partial.hdf5'
            if part.exists():part.rename(part.with_name(part.name+f'.incomplete_{time.time_ns()}'))
            command=[sys.executable,str(ROOT/'official_rgbd_convert.py'),'--dataset',str(subset),'--output_name',part.name,
                '--camera_names','agentview','robot0_eye_in_hand','--camera_height','84','--camera_width','84','--depth']
            print('official RGB-D conversion',task,command,flush=True)
            # Official rendering may probe all GPUs unless explicitly pinned.
            # The raw dataset's renderer id is metadata only; set its *subset*
            # metadata to the selected device before invoking the official tool.
            with h5py.File(subset,'r+') as f:
                rendering=json.loads(f['data'].attrs['env_args'])
                rendering['env_kwargs']['render_gpu_device_id']=2
                f['data'].attrs['env_args']=json.dumps(rendering)
            subprocess.run(command,check=True)
            os.replace(part,rgbd)
        with h5py.File(rgbd,'r') as src:
            lengths=[len(src['data'][key]['actions']) for key in ids]
            ends=np.cumsum(lengths);n=int(ends[-1])
            out=zarr.open(str(target.with_name(target.name+'.partial')),'a')
            data=out.require_group('data');m=out.require_group('meta')
            first=src['data'][ids[0]]
            specs={}
            for cam in ['agentview','robot0_eye_in_hand']:
                specs[cam+'_image']=((84,84,3),'u1')
                specs[cam+'_depth']=((84,84,1),'f4')
            specs['agent_pos']=((9,),'f4');specs['action']=((first['actions'].shape[-1],),'f4')
            for key,(shape,dtype) in specs.items():
                data.require_dataset(key,shape=(n,*shape),dtype=dtype,
                    chunks=(1,*shape) if len(shape)>1 else (min(1024,n),*shape),
                    compressor=Blosc(cname='zstd',clevel=3,shuffle=Blosc.BITSHUFFLE))
            done_path=directory/'zarr_conversion_progress.json'
            done=json.loads(done_path.read_text())['completed_ids'] if done_path.exists() else []
            offset=0
            for key,length in zip(ids,lengths):
                if key not in done:
                    traj=src['data'][key];obs=traj['obs']
                    for cam in ['agentview','robot0_eye_in_hand']:
                        image=obs[cam+'_image'][:];depth=obs[cam+'_depth'][:].astype('f4')
                        if depth.ndim==3:depth=depth[...,None]
                        if image.shape!=(length,84,84,3) or depth.shape!=(length,84,84,1):
                            raise ValueError((key,cam,image.shape,depth.shape))
                        if image.dtype!=np.uint8:raise ValueError('official converter RGB must be uint8 HWC')
                        if not np.isfinite(depth).all():raise ValueError('nonfinite metric depth')
                        data[cam+'_image'][offset:offset+length]=image
                        data[cam+'_depth'][offset:offset+length]=np.where(depth>0,depth,0)
                    state=np.concatenate([obs[k][:] for k in ['robot0_eef_pos','robot0_eef_quat','robot0_gripper_qpos']],-1).astype('f4')
                    data['agent_pos'][offset:offset+length]=state
                    data['action'][offset:offset+length]=traj['actions'][:].astype('f4')
                    done.append(key);tmp=done_path.with_suffix('.tmp');tmp.write_text(json.dumps(dict(completed_ids=done)));os.replace(tmp,done_path)
                offset+=length
                if len(done)%20==0:print('converted',task,len(done),'/200',flush=True)
            m.array('episode_ends',ends,overwrite=True)
        os.replace(target.with_name(target.name+'.partial'),target)
        value=dict(task=task,n_episodes=200,n_steps=n,source=str(raw),processed_path=str(target),
            official_rgbd_path=str(rgbd),subset_ids=ids,env_meta=meta,
            cameras=['agentview','robot0_eye_in_hand'],resolution=[84,84],
            depth_model_unit='meter',rgb_depth_vertical_flip='official EnvRobosuite observation processing',
            conversion_script=str(official),action_semantics='unaltered relative OSC_POSE from official metadata',
            offline_analysis_adapter='gsc_dp/analysis_env.py; same cameras, metric depth and vertical orientation')
        manifest.write_text(json.dumps(value,indent=2));print('ready formal MimicGen data',task,flush=True)

if __name__=='__main__':main()
