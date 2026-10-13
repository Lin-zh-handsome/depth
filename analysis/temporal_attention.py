"""Independent real closed-loop temporal attention collection and paper export.

No hooks run inside the formal success-rate evaluation worker. This module
reuses the encoder's existing capture interface and records one observation
and its actual spatial weights per policy replanning event.
"""
import argparse
from collections import deque
from contextlib import contextmanager
import json
import os
import subprocess
import time
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'source/diffusion_policy'))
import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw
import torch
from gsc_dp.policy_factory import create

def numpy(t):
    return t.detach().float().cpu().numpy() if isinstance(t,torch.Tensor) else np.asarray(t)

def query_attention(width,height,y,x):
    """Actual width→height attention propagation for a chosen output query.

    width[B,row,head,query_x,key_x], height[B,column,head,query_y,key_y].
    Effective weight(head,y,x)=Ah(query_y,y at query_x)*Aw(query_x,x at y).
    This excludes residual/LEPE; it is a derived axial propagation weight,
    not a claimed full-GSA matrix or feature-response heatmap.
    """
    w=numpy(width)[-1];h=numpy(height)[-1]
    weights=h[x,:,y,:]
    result=weights[:,:,None]*w[:,: ,x,:].transpose(1,0,2)
    return result.mean(0)

def colored_heatmap(a):
    # Fixed [0,1] display normalized by the per-map maximum, recorded in metadata.
    a=np.nan_to_num(np.asarray(a,dtype='f4'))
    normalized=np.clip(a/max(float(a.max()),1e-12),0,1)
    r=np.clip(1.5-np.abs(4*normalized-3),0,1)
    g=np.clip(1.5-np.abs(4*normalized-2),0,1)
    b=np.clip(1.5-np.abs(4*normalized-1),0,1)
    return (np.stack([r,g,b],-1)*255).astype('u1')

def rgb8(rgb):return np.clip(np.moveaxis(rgb,0,-1)*255,0,255).astype('u1')

def overlay(rgb,heat,origin=(0,0),crop_size=None):
    base=Image.fromarray(rgb8(rgb));w,h=base.size
    origin=tuple(map(int,origin));cw,ch=crop_size or (w,h)
    color=Image.fromarray(colored_heatmap(heat)).resize((cw,ch),Image.Resampling.BILINEAR)
    tile=base.crop((origin[0],origin[1],origin[0]+cw,origin[1]+ch))
    base.paste(Image.blend(tile,color,.45),origin)
    return base

def panel(image,label,size=256):
    out=Image.new('RGB',(size,size+32),'white')
    out.paste(image.resize((size,size),Image.Resampling.NEAREST),(0,32))
    ImageDraw.Draw(out).text((7,9),label,fill='black')
    return out

def stage_at(annotation,step):
    selected=[x for x in annotation if x['start_step']<=step<=x['end_step']]
    if len(selected)>1:raise ValueError('overlapping offline stage intervals')
    return selected[0] if selected else None

def environment_stage(task_id,info,step):
    # Only direct official evaluation predicates receive a stage/event label.
    # No approach/carry/alignment phase is guessed from elapsed time or heatmaps.
    if task_id=='StackCube-v1':
        mapping=[('is_cubeA_on_cubeB','placement_event'),('is_cubeA_grasped','grasp_event')]
        source='mani_skill/envs/tasks/tabletop/stack_cube.py::evaluate'
    elif task_id=='PegInsertionSide-v1':
        mapping=[('success','insertion_success_event')]
        source='mani_skill/envs/tasks/tabletop/peg_insertion_side.py::evaluate'
    else:
        mapping=[('success','official_task_success_event')]
        source='MimicGen official task::_check_success'
    for key,name in mapping:
        if key in info:
            value=numpy(info[key])
            if value.size==1 and bool(value.reshape(-1)[0]):
                return dict(name=name,source_kind='environment_event',source=source,
                    predicate=key,start_step=step,end_step=step)
    return None

@contextmanager
def capture_encoder(policy):
    encoder=policy.obs_encoder;original=encoder.forward;captured={}
    if hasattr(encoder,'views'):
        def forward(obs,*args,**kwargs):
            vector,artifacts=original(obs,capture=True)
            captured.clear();captured.update(artifacts)
            return vector
        encoder.forward=forward
    try:yield captured
    finally:encoder.forward=original

def denoiser_saliency(policy,obs,timestep=50):
    """Input-gradient saliency of one deterministic denoising prediction.

    Target: mean squared epsilon output, t=50, zero normalized noisy actions.
    It describes sensitivity of this denoiser probe; it is not GSA attention,
    object segmentation, or proof of the actual sampled action's causality.
    """
    gradients={}
    with torch.enable_grad():
        inp={k:v.detach().clone().requires_grad_(k.endswith('_image')) for k,v in obs.items()}
        nobs=policy.normalizer.normalize(inp)
        flat_obs={k:v[:,:2].reshape(-1,*v.shape[2:]) for k,v in nobs.items()}
        cond=policy.obs_encoder(flat_obs).reshape(1,-1)
        action=torch.zeros(1,policy.horizon,policy.action_dim,device=policy.device)
        out=policy.model(action,torch.tensor([timestep],device=policy.device),global_cond=cond)
        target=out.square().mean()
        keys=[k for k in inp if k.endswith('_image')]
        values=torch.autograd.grad(target,[inp[k] for k in keys])
        for k,v in zip(keys,values):gradients[k]=numpy(v[0,-1].abs().mean(0))
    return gradients

def collect(args):
    from gsc_dp.analysis_env import create_analysis_env
    if os.environ.get('CUDA_VISIBLE_DEVICES')!='GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9':
        raise RuntimeError('analysis must bind the same selected physical GPU2')
    payload=torch.load(args.checkpoint,map_location='cpu',weights_only=False);cfg=payload['config']
    policy=create(cfg);policy.load_state_dict(payload['ema_model']);policy.to('cuda:0').eval().requires_grad_(False)
    output=args.output or ROOT/'analysis/temporal'/cfg['task']/cfg['method']/f"seed_{cfg['seed']}"/args.checkpoint.stem/f'reset_{args.reset_id}'
    output=output.resolve()
    if (output/'episode.json').exists():
        saved=json.loads((output/'episode.json').read_text())
        if saved['checkpoint_path']!=str(args.checkpoint) or saved['reset_id']!=args.reset_id:
            raise ValueError('completed output belongs to a different checkpoint/reset')
        export(output,args.camera,saved['control_hz']);return
    if (output/'replans.jsonl').exists():
        output.rename(output.with_name(output.name+f'.partial_{time.time_ns()}'))
    output.mkdir(parents=True,exist_ok=True);(output/'raw').mkdir(exist_ok=True)
    annotation=json.loads(args.stages.read_text())['events'] if args.stages else []
    for item in annotation:
        if item.get('source_kind') not in ['environment_event','offline_annotation'] or not item.get('source'):
            raise ValueError('each stage requires explicit source_kind and source')
    env=create_analysis_env(cfg)
    actual_hz=float(env.control_freq)
    if args.control_hz is not None and args.control_hz!=actual_hz:
        raise ValueError('requested control_hz differs from actual environment control frequency')
    args.control_hz=actual_hz
    render_device=env.render_device
    analysis_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    rows=[];step=0;once=False;last=False
    try:
        torch.manual_seed(args.reset_id);torch.cuda.manual_seed_all(args.reset_id)
        frame,info=env.reset(seed=args.reset_id);policy.reset()
        history=deque([frame]*2,maxlen=2)
        with (output/'replans.jsonl').open('a',buffering=1) as log:
            while step<cfg['horizon']:
                obs={k:torch.from_numpy(np.stack([f[k] for f in history]))[None].to('cuda:0') for k in frame}
                with capture_encoder(policy) as artifacts:
                    with torch.no_grad():result=policy.predict_action(obs)
                # Move just the captured observation and spatial maps to CPU.
                arrays={k:numpy(v[0,-1]) for k,v in obs.items()}
                summaries={}
                for camera in cfg['cameras']:
                    key=camera+'_image';art=artifacts.get(key,{})
                    H,W=arrays[key].shape[-2:]
                    if 'input_rgb' in art:
                        crop_h,crop_w=art['input_rgb'].shape[-2:]
                    else:crop_h,crop_w=H,W
                    origin=((W-crop_w)//2,(H-crop_h)//2)
                    query_full=(args.query[0]*(W-1),args.query[1]*(H-1))
                    data=dict(kind='unavailable',query_original_xy=query_full,crop_origin_xy=origin,
                        crop_size_wh=[crop_w,crop_h])
                    if 'attention_width' in art:
                        h,w=art['feature_after'].shape[-2:]
                        x=int(np.clip((query_full[0]-origin[0])/crop_w*w,0,w-1))
                        y=int(np.clip((query_full[1]-origin[1])/crop_h*h,0,h-1))
                        if not (origin[0]<=query_full[0]<origin[0]+crop_w and origin[1]<=query_full[1]<origin[1]+crop_h):
                            raise ValueError('query lies outside the encoder crop')
                        arrays[camera+'_gsa_query']=query_attention(art['attention_width'],art['attention_height'],y,x)
                        data.update(kind='derived_axial_gsa_attention',query_grid_yx=[y,x],
                            formula='mean_heads(Ah[query_x,head,query_y,key_y]*Aw[key_y,head,query_x,key_x])',
                            excludes='residual and LEPE; not a full attention matrix')
                        if args.save_axes:
                            arrays[camera+'_gsa_width']=numpy(art['attention_width'][-1])
                            arrays[camera+'_gsa_height']=numpy(art['attention_height'][-1])
                    if 'token_weights' in art:
                        arrays[camera+'_token_weights']=numpy(art['token_weights'][-1])
                        for field in ['u','v','depth_m','rho']:
                            arrays[camera+'_token_'+field]=numpy(art['token_'+field][-1])
                        data['token_count']=int(arrays[camera+'_token_weights'].shape[0])
                    summaries[camera]=data
                if cfg['method'] in ['e0','e1']:
                    saliency=denoiser_saliency(policy,obs)
                    for key,value in saliency.items():
                        camera=key[:-6];arrays[camera+'_saliency']=value
                        summaries[camera]['kind']='input_gradient_saliency'
                        summaries[camera]['saliency_target']='mean square denoiser epsilon at t=50; zero normalized noisy action'
                        summaries[camera]['saliency_caveat']='sensitivity probe, not attention or sampled-action causal attribution'
                planned=numpy(result['action'][0]);arrays['planned_action_chunk']=planned
                file=output/'raw'/f'plan_{len(rows):04d}_step_{step:04d}.npz'
                np.savez_compressed(file,**arrays)
                record=dict(episode_id=f"{cfg['task']}/reset_{args.reset_id}",reset_id=args.reset_id,
                    plan_id=len(rows),env_step=step,time_seconds=step/args.control_hz,method=cfg['method'],seed=cfg['seed'],
                    checkpoint_path=str(args.checkpoint),checkpoint_step=payload.get('checkpoint_step',payload['optimizer_updates']),
                    code_revision=payload['code_revision'],analysis_revision=analysis_revision,
                    cameras=summaries,raw_path=str(file),
                    robot_state={k:numpy(obs[k][0,-1]).tolist() for k,v in cfg['shape_meta']['obs'].items() if v.get('type')=='low_dim'},offline_gt=env.gt(),
                    planned_actions=planned.tolist(),executed_actions=[],
                    stage=stage_at(annotation,step) or environment_stage(cfg['task'],info,step),
                    collection_mode='independent_analysis_rollout',control_hz=args.control_hz)
                for action in planned:
                    frame,_,terminated,truncated,info=env.step(action);step+=1
                    last=bool(numpy(info.get('success',False)).reshape(-1)[0]);once|=last
                    record['executed_actions'].append(dict(step=step,action=action.tolist(),success=last,
                        environment_event=environment_stage(cfg['task'],info,step)))
                    history.append(frame)
                    if step>=cfg['horizon'] or terminated or truncated:break
                log.write(json.dumps(record)+'\n');rows.append(record)
                print('recorded',record['episode_id'],'plan',record['plan_id'],'step',step,flush=True)
                if step>=cfg['horizon'] or terminated or truncated:break
    finally:env.close()
    summary=dict(task=cfg['task'],method=cfg['method'],seed=cfg['seed'],reset_id=args.reset_id,
        checkpoint_path=str(args.checkpoint),code_revision=payload['code_revision'],analysis_revision=analysis_revision,
        policy_noise_seed=args.reset_id,success_at_end=last,success_once=once,
        success=once if cfg['benchmark']=='mimicgen' else last,
        steps=step,replans=len(rows),stage_annotation_path=str(args.stages) if args.stages else None,
        stage_policy='names only from explicit environment events or offline annotations; otherwise neutral timepoints',
        control_hz=args.control_hz,primary_metric_status='analysis only; not added to formal success-rate results',
        gpu_uuid=os.environ['CUDA_VISIBLE_DEVICES'],render_device=render_device)
    (output/'episode.json').write_text(json.dumps(summary,indent=2))
    export(output,args.camera,args.control_hz)

def render_row(row,camera):
    with np.load(row['raw_path']) as a:
        rgb=a[camera+'_image'];data=row['cameras'][camera]
        images=[panel(Image.fromarray(rgb8(rgb)),'RGB')]
        if camera+'_gsa_query' in a:
            img=overlay(rgb,a[camera+'_gsa_query'],data['crop_origin_xy'],data['crop_size_wh'])
            draw=ImageDraw.Draw(img);x,y=data['query_original_xy'];draw.ellipse((x-2,y-2,x+2,y+2),fill='white')
            images.append(panel(img,'GSA: derived axial attention'))
        elif camera+'_saliency' in a:
            images.append(panel(overlay(rgb,a[camera+'_saliency']),'Input-gradient saliency (not attention)'))
        else:images.append(panel(Image.fromarray(rgb8(rgb)),'Attention unavailable'))
        if camera+'_token_weights' in a:
            masks=a[camera+'_token_weights'];K=len(masks)
            tokens=Image.new('RGB',(256,256),'white');columns=4;rows=int(np.ceil(K/columns))
            tile_w,tile_h=256//columns,256//rows
            for k,mask in enumerate(masks):
                tile=overlay(rgb,mask,data['crop_origin_xy'],data['crop_size_wh']).resize((tile_w,tile_h))
                u=float(a[camera+'_token_u'][k]);v=float(a[camera+'_token_v'][k])
                d=float(a[camera+'_token_depth_m'][k].reshape(-1)[0]);rho=float(a[camera+'_token_rho'][k].reshape(-1)[0])
                draw=ImageDraw.Draw(tile);draw.rectangle((0,0,tile_w,25),fill='white')
                draw.text((2,1),f'{k}:d={d:.2f}',fill='black');draw.text((2,13),f'rho={rho:.2f}',fill='black')
                full_h,full_w=rgb.shape[-2:];ox,oy=data['crop_origin_xy'];cw,ch=data['crop_size_wh']
                cx=(ox+u*cw)/full_w*tile_w;cy=(oy+v*ch)/full_h*tile_h
                draw.ellipse((cx-2,cy-2,cx+2,cy+2),outline='white')
                tokens.paste(tile,((k%columns)*tile_w,(k//columns)*tile_h))
            images.append(panel(tokens,f'TokenLearner K={K}, depth in m'))
        else:images.append(panel(Image.new('RGB',(256,256),'white'),'Token weights: not present'))
        depth=a[camera+'_depth'][0]
        images.append(panel(Image.fromarray(colored_heatmap(depth)),'Depth (m, display scaled)'))
        canvas=Image.new('RGB',(sum(x.width for x in images),images[0].height+28),'white')
        cursor=0
        for image in images:canvas.paste(image,(cursor,28));cursor+=image.width
        label=row['stage']['name'] if row.get('stage') else 'timepoint (stage unannotated)'
        ImageDraw.Draw(canvas).text((8,8),f"plan {row['plan_id']}, step {row['env_step']}, {row['time_seconds']:.2f}s | {label}",fill='black')
        return canvas

def key_indices(rows):
    stages={}
    for i,row in enumerate(rows):
        if row.get('stage'):stages.setdefault(row['stage']['name'],i)
    indices=list(stages.values())[:6]
    for i in np.linspace(0,len(rows)-1,min(6,len(rows)),dtype=int).tolist():
        if len(indices)>=6:break
        if i not in indices:indices.append(i)
    return sorted(indices)

def export(output,camera=None,hz=None):
    rows=[json.loads(x) for x in (output/'replans.jsonl').read_text().splitlines()]
    if not rows:raise ValueError('no actual replanning data')
    camera=camera or next(iter(rows[0]['cameras']));hz=hz or rows[0]['control_hz']
    frames=output/'frames';frames.mkdir(exist_ok=True)
    keys=key_indices(rows);paths=[]
    video=output/f'{camera}_temporal_attention.mp4'
    with imageio.get_writer(video,fps=hz,codec='libx264',macro_block_size=1) as writer:
        for i,row in enumerate(rows):
            picture=render_row(row,camera)
            # Repeat a planning observation for the actions it actually controlled;
            # never pretend it is newly measured attention at intermediate steps.
            for _ in row['executed_actions']:writer.append_data(np.asarray(picture))
            if i in keys:
                path=frames/f"key_{i:04d}_step_{row['env_step']:04d}.png";picture.save(path);paths.append(path)
    panels=[Image.open(p) for p in paths]
    grid=Image.new('RGB',(panels[0].width,panels[0].height*len(panels)),'white')
    for i,p in enumerate(panels):grid.paste(p,(0,i*p.height))
    figure=output/f'{camera}_spatial_attention_evolution.png';grid.save(figure)
    metadata=dict(figure_id='Fig 3-15',title='Spatial attention evolution during closed-loop robot execution',
        title_zh='机器人执行过程中的空间关注演化分析',
        raw_rows=str(output/'replans.jsonl'),episode=str(output/'episode.json'),video=str(video),
        figure=str(figure),key_frames=[dict(path=str(p),plan_id=rows[i]['plan_id'],env_step=rows[i]['env_step'],
            stage=rows[i].get('stage')) for p,i in zip(paths,keys)],camera=camera,
        gsa_definition='derived actual width-to-height axial propagation; excludes residual/LEPE',
        token_definition='actual learned softmax spatial weights, not segmentation',
        saliency_definition='input gradient sensitivity of t50 epsilon probe, not attention',
        display_normalization='each map divided by its recorded per-map maximum; raw values kept in NPZ',
        video_timing='planning observation held for executed action count; source control_hz recorded',
        key_selection='first occurrence of explicit named stages; fill 4–6 with neutral uniformly spaced timepoints',
        success_failure_rule='outcome from actual official environment at episode end; preserve both outcomes')
    (output/'temporal_manifest.json').write_text(json.dumps(metadata,indent=2))
    print('exported',video,figure,flush=True)

def compare(outputs,dest,camera=None):
    episodes=[json.loads((p/'episode.json').read_text()) for p in outputs]
    if len({(e['task'],e['reset_id']) for e in episodes})!=1:raise ValueError('comparison requires identical task/reset ID')
    if len({e['method'] for e in episodes})!=len(episodes):raise ValueError('duplicate method in comparison')
    dest.mkdir(parents=True,exist_ok=True)
    all_rows=[[json.loads(x) for x in (p/'replans.jsonl').read_text().splitlines()] for p in outputs]
    camera=camera or next(iter(all_rows[0][0]['cameras']))
    end=max(e['steps'] for e in episodes);times=np.linspace(0,end-1,6,dtype=int)
    rendered=[];sources=[]
    for step in times:
        selected=[]
        for rows in all_rows:
            selected.append(min(rows,key=lambda r:abs(r['env_step']-step)))
        pictures=[render_row(row,camera) for row in selected]
        grid=Image.new('RGB',(pictures[0].width,len(pictures)*pictures[0].height),'white')
        for i,picture in enumerate(pictures):
            grid.paste(picture,(0,i*picture.height))
            ImageDraw.Draw(grid).text((8,i*picture.height+8),f"{episodes[i]['method']} actual step {selected[i]['env_step']} | success={episodes[i]['success_at_end']}",fill='black')
        path=dest/f'paired_step_{step:04d}.png';grid.save(path);rendered.append(path)
        sources.append(dict(requested_step=int(step),actual_steps=[r['env_step'] for r in selected],
            source_npz=[r['raw_path'] for r in selected]))
    # A synchronized comparison video at actual environment step coordinates.
    with imageio.get_writer(dest/'paired_temporal_comparison.mp4',fps=episodes[0]['control_hz'],codec='libx264',macro_block_size=1) as writer:
        for step in range(end):
            selected=[max((r for r in rows if r['env_step']<=step),key=lambda r:r['env_step']) for rows in all_rows]
            pictures=[render_row(r,camera) for r in selected]
            frame=Image.new('RGB',(pictures[0].width,len(pictures)*pictures[0].height),'white')
            for i,picture in enumerate(pictures):frame.paste(picture,(0,i*picture.height))
            writer.append_data(np.asarray(frame))
    (dest/'comparison.json').write_text(json.dumps(dict(episodes=episodes,sources=sources,
        output_png=[str(p) for p in rendered],comparison_rule='same reset, absolute environment-step alignment',
        note='successful/failed outcomes preserved; no stage correspondence inferred from elapsed time'),indent=2))

def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='mode',required=True)
    c=sub.add_parser('collect');c.add_argument('--checkpoint',type=Path,required=True)
    c.add_argument('--reset-id',type=int,required=True);c.add_argument('--query',nargs=2,type=float,default=[.5,.5])
    c.add_argument('--camera');c.add_argument('--output',type=Path);c.add_argument('--stages',type=Path)
    c.add_argument('--control-hz',type=float);c.add_argument('--save-axes',action='store_true')
    e=sub.add_parser('export');e.add_argument('--input',type=Path,required=True);e.add_argument('--camera')
    m=sub.add_parser('compare');m.add_argument('--inputs',nargs='+',type=Path,required=True);m.add_argument('--output',type=Path,required=True);m.add_argument('--camera')
    a=p.parse_args()
    if a.mode=='collect':
        a.checkpoint=a.checkpoint.resolve()
        if any(x<0 or x>1 for x in a.query):p.error('query is normalized original-image x/y in [0,1]')
        collect(a)
    elif a.mode=='export':export(a.input.resolve(),a.camera)
    else:compare([x.resolve() for x in a.inputs],a.output.resolve(),a.camera)

if __name__=='__main__':main()
