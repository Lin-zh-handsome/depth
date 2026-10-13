"""Benchmark adapters for independent temporal analysis, sharing policy inputs."""
import json
from pathlib import Path
import numpy as np

class MimicGenAnalysisEnv:
    """Direct official robosuite/MimicGen environment with metric RGB-D."""
    def __init__(self,cfg):
        import mimicgen  # registers the official task classes
        import robosuite
        from robosuite.utils.camera_utils import get_real_depth_map
        self.get_real_depth_map=get_real_depth_map
        meta=cfg.get('env_meta')
        if meta is None:
            manifest=json.loads(Path(cfg['dataset_manifest']).read_text())
            meta=manifest['env_meta']
        kwargs=dict(meta['env_kwargs'])
        kwargs.update(camera_names=cfg['cameras'],camera_heights=84,camera_widths=84,
            camera_depths=True,use_camera_obs=True,has_renderer=False,
            has_offscreen_renderer=True,render_gpu_device_id=2,ignore_done=True)
        self.env=robosuite.make(meta['env_name'],**kwargs)
        self.cfg=cfg;self.control_freq=self.env.control_freq
        self.render_device='MuJoCo EGL physical GPU2'

    def format(self,raw):
        out={}
        for camera in self.cfg['cameras']:
            out[camera+'_image']=np.moveaxis(raw[camera+'_image'][::-1].copy(),-1,0).astype('f4')/255
            d=self.get_real_depth_map(self.env.sim,raw[camera+'_depth'])[::-1].copy()
            if d.ndim==2:d=d[...,None]
            out[camera+'_depth']=np.moveaxis(np.where(np.isfinite(d)&(d>0),d,0),-1,0).astype('f4')
        # Only robot proprioception enters the policy. All object GT stays in gt().
        out['agent_pos']=np.concatenate([raw['robot0_eef_pos'],raw['robot0_eef_quat'],raw['robot0_gripper_qpos']]).astype('f4')
        for key,attr in self.cfg['shape_meta']['obs'].items():
            if attr.get('type')=='low_dim' and key.startswith('robot0_') and key in raw:
                out[key]=np.asarray(raw[key],dtype='f4')
        return {k:out[k] for k in self.cfg['shape_meta']['obs']}

    def reset(self,seed):
        np.random.seed(seed)
        raw=self.env.reset();self.steps=0
        return self.format(raw),{'success':bool(self.env._check_success())}

    def step(self,action):
        raw,reward,_,info=self.env.step(action);self.steps+=1
        info=dict(info,success=bool(self.env._check_success()))
        return self.format(raw),reward,False,self.steps>=self.cfg['horizon'],info

    def gt(self):
        sim=self.env.sim
        poses={}
        for i in range(sim.model.nbody):
            name=sim.model.body_id2name(i)
            if name:poses[name]=dict(position_m=sim.data.body_xpos[i].tolist(),quaternion=sim.data.body_xquat[i].tolist())
        return dict(body_poses_offline=poses,source='official simulator body state; never policy input')

    def close(self):self.env.close()

class ManiSkillAnalysisEnv:
    def __init__(self,cfg):
        import gymnasium as gym
        import mani_skill.envs
        from mani_skill.utils.wrappers import CPUGymWrapper
        from evaluate import flat,gt
        self.format=flat;self.get_gt=gt
        self.env=CPUGymWrapper(gym.make(cfg['task'],obs_mode='rgbd',control_mode=cfg['control_mode'],
            sim_backend='physx_cpu',render_backend='sapien_cuda:0',reconfiguration_freq=1,
            max_episode_steps=cfg['horizon'],render_mode='rgb_array'),ignore_terminations=True,record_metrics=True)
        self.control_freq=self.env.unwrapped.control_freq
        self.render_device=str(self.env.unwrapped.backend.render_device)
    def reset(self,seed):
        raw,info=self.env.reset(seed=seed);return self.format(raw),info
    def step(self,action):
        raw,r,t,tr,info=self.env.step(action);return self.format(raw),r,t,tr,info
    def gt(self):return self.get_gt(self.env.unwrapped)
    def close(self):self.env.close()

def create_analysis_env(cfg):
    return MimicGenAnalysisEnv(cfg) if cfg['benchmark']=='mimicgen' else ManiSkillAnalysisEnv(cfg)
