"""Canonical formal scope and benchmark-specific success metadata."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FORMAL_METHODS=('e0','e3','e6','m3')
SUCCESS_DEFINITIONS={'mimicgen':'success_once','maniskill':'success_at_end'}
SUCCESS_DESCRIPTIONS={
    'mimicgen':'At least one executed environment step reports official task success within the fixed rollout horizon.',
    'maniskill':'The final executed environment step reports official task success at the fixed rollout horizon.'}

def annotate_success_metadata(value,benchmark):
    result=dict(value);definition=SUCCESS_DEFINITIONS[benchmark]
    old=result.get('success_definition')
    if old and old!=definition:result.setdefault('success_definition_original',old)
    result.update(success_definition=definition,success_semantics=SUCCESS_DESCRIPTIONS[benchmark])
    return result

def validate_formal_config(cfg):
    if cfg['method'] not in FORMAL_METHODS:raise ValueError('Model outside the four-model formal protocol')
    protocol=json.loads((ROOT/'configs/protocol.json').read_text())
    task=next((t for t in protocol['tasks'] if t['task']==cfg['task']),None)
    if task is None:raise ValueError('Task outside Chapter 3 protocol')
    for key in ['benchmark','budget','progress_unit','episodes','horizon','savepoints']:
        if cfg[key]!=task[key]:raise ValueError('Formal protocol mismatch: '+key)
    if cfg['seed'] not in task['seeds']:raise ValueError('Training seed outside protocol')
    if cfg['eval_positions']!=list(range(task['interval'],task['budget']+1,task['interval'])):raise ValueError('Only five prescribed checkpoint positions are permitted')
    if cfg['reset_ids']!=task['reset_ids']:raise ValueError('Formal reset list changed')
    if task['benchmark']=='maniskill' and cfg['control_mode']!={'PegInsertionSide-v1':'pd_ee_delta_pose','StackCube-v1':'pd_ee_delta_pos'}[cfg['task']]:raise ValueError('Historical joint-position replay is not the formal EE control dataset')

def validate_complete_episode_records(records,cfg,point):
    validate_formal_config(cfg)
    if len(records)!=cfg['episodes'] or len({r['reset_id'] for r in records})!=cfg['episodes'] or {r['reset_id'] for r in records}!=set(cfg['reset_ids']):raise ValueError('Formal episode/reset set incomplete or duplicated')
    definition=SUCCESS_DEFINITIONS[cfg['benchmark']]
    for r in records:
        for key in ['task','method','seed','control_mode']:
            if r[key]!=cfg[key]:raise ValueError('Episode identity mismatch: '+key)
        if r['checkpoint_step']!=point or r['success']!=r[definition]:raise ValueError('Episode checkpoint or benchmark success definition mismatch')
