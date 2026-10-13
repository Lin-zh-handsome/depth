"""Use the clean official CNN-DP action model without editing its source."""
import copy
from diffusers.schedulers.scheduling_ddpm import DDPMScheduler
from diffusion_policy.policy.diffusion_unet_image_policy import DiffusionUnetImagePolicy
from diffusion_policy.model.vision.multi_image_obs_encoder import MultiImageObsEncoder
from diffusion_policy.model.vision.model_getter import get_resnet
from gsc_dp.encoder import RGBDGeometryObsEncoder

def create(config):
    shape = config['shape_meta']
    if config['method']=='e0':
        rgb_shape=copy.deepcopy(shape)
        rgb_shape['obs']={k:v for k,v in rgb_shape['obs'].items() if v.get('type')!='depth'}
        encoder=MultiImageObsEncoder(rgb_shape,get_resnet('resnet18',weights=None),
            crop_shape=config['crop_shape'],random_crop=True,use_group_norm=True,
            share_rgb_model=False,imagenet_norm=True)
    else:
        encoder=RGBDGeometryObsEncoder(shape,method=config['method'],
            crop_shape=config['crop_shape'],**config.get('encoder_options',{}))
    scheduler=DDPMScheduler(num_train_timesteps=100,beta_start=0.0001,beta_end=0.02,
        beta_schedule='squaredcos_cap_v2',variance_type='fixed_small',clip_sample=True,prediction_type='epsilon')
    return DiffusionUnetImagePolicy(shape,scheduler,encoder,horizon=16,n_action_steps=8,
        n_obs_steps=2,num_inference_steps=100,obs_as_global_cond=True,
        diffusion_step_embed_dim=128,down_dims=[512,1024,2048],kernel_size=5,n_groups=8,cond_predict_scale=True)
