"""Real saved-state offline/cache/online parity; no policy training or formal eval."""
import os,sys,json,copy,types,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import numpy as np,h5py,zarr
import egl_probe
egl_probe.get_available_devices=lambda:[2]
import mimicgen
import robomimic.utils.env_utils as EU
from gsc_dp.analysis_env import MimicGenAnalysisEnv

out=ROOT/'docs/audit_55951414';out.mkdir(parents=True,exist_ok=True)
rows=[]
for task in ['threading_d2','stack_three_d1','coffee_d2']:
    cfg=json.loads((ROOT/f'configs/runs/mimicgen/{task}/e6/seed_0.json').read_text())
    m=json.loads(Path(cfg['dataset_manifest']).read_text());meta=copy.deepcopy(m['env_meta'])
    meta['env_kwargs']['render_gpu_device_id']=2
    online=MimicGenAnalysisEnv(cfg)
    # Same official state restoration used by dataset_states_to_obs, wrapping
    # the actual online runner's direct robosuite instance after construction.
    bridge=EU.create_env_for_data_processing(env_meta=meta,camera_names=cfg['cameras'],camera_height=84,camera_width=84,reward_shaping=False,use_depth_obs=True)
    bridge.env.close()
    bridge.env=online.env
    cache=zarr.open(cfg['zarr_path'],'r');ends=cache['meta/episode_ends'][:]
    with h5py.File(m['source'],'r') as raw,h5py.File(m['official_rgbd_path'],'r') as saved:
        for di in [0,199]:
            demo=m['subset_ids'][di];g=raw['data'][demo];sg=saved['data'][demo]
            states=g['states'];action=g['actions'];offset=int(ends[di-1]) if di else 0
            bridge.reset_to({'model':g.attrs['model_file'],'states':states[0]})
            for ti in sorted(set([0,len(action)//2,len(action)-1])):
                official=bridge.reset_to({'states':states[ti]})
                current=online.env._get_observations(force_update=True)
                formatted=online.format(current)
                row=dict(task=task,demo=demo,timestep=ti,global_cache_index=offset+ti,cameras=cfg['cameras'],encoder_camera_order=sorted(k for k,v in cfg['shape_meta']['obs'].items() if v['type']=='rgb'),fields={})
                for cam in cfg['cameras']:
                    rgb=sg['obs'][cam+'_image'][ti];depth=sg['obs'][cam+'_depth'][ti].astype('f4')
                    if depth.ndim==2:depth=depth[...,None]
                    actual=np.rint(np.moveaxis(formatted[cam+'_image'],0,-1)*255)
                    d=np.moveaxis(formatted[cam+'_depth'],0,-1)
                    row['fields'][cam]=dict(rgb_same_orientation_mae=float(np.abs(actual-rgb).mean()),rgb_vertical_reverse_mae=float(np.abs(actual-rgb[::-1]).mean()),rgb_max_abs=float(np.abs(actual-rgb).max()),depth_max_abs_m=float(np.abs(d-depth).max()),depth_mae_m=float(np.abs(d-depth).mean()),depth_range_m=[float(depth.min()),float(depth.max())],cache_rgb_exact=bool(np.array_equal(cache['data'][cam+'_image'][offset+ti],rgb)),cache_depth_exact=bool(np.array_equal(cache['data'][cam+'_depth'][offset+ti],depth)),official_vs_online_rgb_max=float(np.abs(actual-official[cam+'_image']).max()),official_vs_online_depth_max=float(np.abs(d-official[cam+'_depth']).max()))
                proprio=np.concatenate([sg['obs'][k][ti] for k in ['robot0_eef_pos','robot0_eef_quat','robot0_gripper_qpos']]).astype('f4')
                row.update(proprio_max_abs=float(np.abs(formatted['agent_pos']-proprio).max()),cache_proprio_exact=bool(np.array_equal(cache['data/agent_pos'][offset+ti],proprio)),cache_action_max_abs=float(np.abs(cache['data/action'][offset+ti]-action[ti]).max()),hdf5_action_max_abs=float(np.abs(sg['actions'][ti]-action[ti]).max()),sim_state_max_abs=float(np.abs(online.env.sim.get_state().flatten()-states[ti]).max()),action_dim=int(action.shape[-1]),controller_class=type(online.env.robots[0].controller).__name__,controller_relative=getattr(online.env.robots[0].controller,'use_delta',None),action_limits=[x.tolist() for x in online.env.action_spec])
                rows.append(row)
                # Independent transition check compares the exact offline wrapper
                # step and the exact live adapter step, with controller reset.
                if ti==0:
                    bridge.reset_to({'model':g.attrs['model_file'],'states':states[ti]})
                    bridge.step(action[ti]);first=online.env.sim.get_state().flatten().copy()
                    bridge.reset_to({'model':g.attrs['model_file'],'states':states[ti]})
                    online.steps=0;online.step(action[ti]);second=online.env.sim.get_state().flatten().copy()
                    row['same_action_transition_max_abs']=float(np.abs(first-second).max())
                print(json.dumps(row),flush=True)
                (out/'mimicgen_saved_state_parity.json').write_text(json.dumps(dict(status='in_progress',gpu_uuid=os.environ['CUDA_VISIBLE_DEVICES'],samples=rows),indent=2))
    online.close()
result=dict(status='complete',gpu_uuid=os.environ['CUDA_VISIBLE_DEVICES'],source='actual raw HDF5 states/actions/model XML; official converted HDF5; active Zarr; actual online adapter',samples=rows)
(out/'mimicgen_saved_state_parity.json').write_text(json.dumps(result,indent=2))
print('COMPLETE',len(rows),flush=True)
