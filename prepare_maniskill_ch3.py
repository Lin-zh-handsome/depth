"""Official 100-demo control conversion and metric RGB-D cache, no synthetic data."""
import json,os,subprocess,sys
from pathlib import Path
import h5py,numpy as np,zarr
from numcodecs import Blosc,blosc
ROOT=Path(__file__).resolve().parent
blosc.set_nthreads(2)

def prepare(task,control,horizon):
    raw=ROOT.parent/'data/maniskill/raw'/task/'motionplanning/trajectory.h5'
    target=ROOT/'data/raw/maniskill_ch3'/task
    target.mkdir(parents=True,exist_ok=True)
    subset=target/'trajectory.h5'
    original=json.loads(raw.with_suffix('.json').read_text());chosen=original['episodes'][:100]
    if len(chosen)!=100:raise ValueError('100 official demonstrations required')
    ids=[x['episode_id'] for x in chosen]
    if not subset.exists():
        tmp=subset.with_suffix('.partial')
        with h5py.File(raw,'r') as src,h5py.File(tmp,'w') as dst:
            for i in ids:src.copy(f'traj_{i}',dst)
        os.replace(tmp,subset)
    meta=dict(original,episodes=chosen)
    meta['env_info']=dict(original['env_info']);kwargs=dict(meta['env_info']['env_kwargs'])
    kwargs.update(render_backend='sapien_cuda:0',max_episode_steps=horizon,sensor_configs=dict(width=128,height=128,shader_pack='default'))
    meta['env_info']['env_kwargs']=kwargs
    subset.with_suffix('.json').write_text(json.dumps(meta,indent=2))
    replay=target/f'trajectory.rgbd.{control}.physx_cpu.h5'
    ready=target/'official_replay_complete.json'
    if not ready.exists():
        # Official converter controls an original joint-position environment and target EE controller.
        subprocess.run([sys.executable,'-m','mani_skill.trajectory.replay_trajectory','--traj-path',str(subset),
            '--obs-mode','rgbd','--target-control-mode',control,'--sim-backend','physx_cpu',
            '--num-envs','1','--count','100','--save-traj','--allow-failure'],check=True)
        rm=json.loads(replay.with_suffix('.json').read_text())
        if len(rm['episodes'])!=100:raise ValueError('official replay did not retain all 100 demonstrations')
        if rm['env_info']['env_kwargs']['control_mode']!=control:raise ValueError('converted control mismatch')
        ready.write_text(json.dumps(dict(source=str(raw),source_ids=ids,output=str(replay))))
    processed=ROOT/'data/processed'/task/f'subset100_{control}.zarr'
    manifest=ROOT/'data/manifests'/f'{task}_100.json'
    if manifest.exists() and json.loads(manifest.read_text()).get('control_mode')==control and processed.exists():return
    output=zarr.open(str(processed.with_name(processed.name+'.partial')),'w');data=output.require_group('data')
    chunks={};ends=[];total=0
    with h5py.File(replay,'r') as src:
        rm=json.loads(replay.with_suffix('.json').read_text())
        for episode in rm['episodes']:
            tr=src[f"traj_{episode['episode_id']}"];a=tr['actions'][:].astype('f4');n=len(a)
            if a.shape[1]!=(4 if control=='pd_ee_delta_pos' else 7):raise ValueError('EE action dimension mismatch')
            arrays={'action':a}
            obs=tr['obs']
            arrays['agent_pos']=np.concatenate([obs['agent/qpos'][:n],obs['agent/qvel'][:n],obs['extra/tcp_pose'][:n]],axis=-1).astype('f4')
            for cam in ['base_camera','hand_camera']:
                arrays[cam+'_image']=obs[f'sensor_data/{cam}/rgb'][:n]
                depth=obs[f'sensor_data/{cam}/depth'][:n].astype('f4')*.001
                arrays[cam+'_depth']=np.where(np.isfinite(depth)&(depth>0),depth,0)
            for key,x in arrays.items():
                if key not in data:
                    data.create_dataset(key,shape=(0,*x.shape[1:]),chunks=(min(n,64),*x.shape[1:]),dtype=x.dtype,
                        compressor=Blosc(cname='zstd',clevel=3,shuffle=Blosc.BITSHUFFLE))
                data[key].append(x)
            total+=n;ends.append(total)
            print(task,'cached',len(ends),'/100',flush=True)
    output.require_group('meta').array('episode_ends',np.asarray(ends,dtype='i8'))
    os.replace(processed.with_name(processed.name+'.partial'),processed)
    manifest.write_text(json.dumps(dict(task=task,source=str(raw),n_episodes=100,n_steps=total,
        control_mode=control,source_control_mode='pd_joint_pos',subset_ids=ids,
        replay_episode_ids=[x['episode_id'] for x in rm['episodes']],processed_path=str(processed),
        raw_replay_metadata=str(replay.with_suffix('.json')),cameras=['base_camera','hand_camera'],resolution=[128,128],
        depth_source_unit='millimeter',depth_model_unit='meter',
        replay_success_flags=[x.get('success') for x in rm['episodes']],
        source_success_flags=[x.get('success') for x in chosen],
        source_success_count=sum(x.get('success') is True for x in chosen),
        replay_success_count=sum(x.get('success') is True for x in rm['episodes']),
        replay_failure_count=sum(x.get('success') is False for x in rm['episodes']),
        training_retains_failed_controller_replays=True,
        subset_rule='fixed first 100 official motionplanning demos; official controller conversion; failures retained and labeled'),indent=2))
    print('READY',task,control,flush=True)

if __name__=='__main__':
    prepare('PegInsertionSide-v1','pd_ee_delta_pose',300)
    prepare('StackCube-v1','pd_ee_delta_pos',200)
