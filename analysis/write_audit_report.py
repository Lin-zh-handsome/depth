"""Assemble the requested review from real measurements and current monitoring."""
import json,datetime,csv
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'docs/audit_55951414'
read=lambda name:json.loads((O/name).read_text())
p=read('mimicgen_saved_state_parity.json');peg=read('peg_100_source_replay_cache.json');b=read('window_update_budgets.json');m=read('threading_m2_lineage.json');a=read('controlled_model_architecture.json');h=read('historical_summary_exclusion.json')
status=json.loads((R/'experiments/ch3/monitoring_manifest.json').read_text());stamp=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='seconds')
crop=dict(official_source='source/diffusion_policy/diffusion_policy/model/vision/crop_randomizer.py:268-278',custom_source='gsc_dp/encoder.py:_prepare',mimicgen_official_offsets=[0,7],mimicgen_custom_offsets=[0,8],maniskill_official_offsets=[0,15],maniskill_custom_offsets=[0,16],evaluation_center_crop_equal=True,m2_m3_crop_implementation_equal=True,existing_runs_modified=False)
(O/'crop_initialization_disclosure.json').write_text(json.dumps(dict(crop=crop,camera_initialization=a['controlled_exceptions'][1],interpretation='An existing implementation difference, not an invalid budget or corrupted experiment. Report it; do not silently alter augmentation distributions of existing runs or add unrequested retraining.'),indent=2))
def location(name,needle):
    lines=(R/name).read_text().splitlines();line=next((i for i,s in enumerate(lines,1) if needle in s),1)
    return f'`{name}:{line}`'
budget_table='\n'.join(f"|{x['task']}|{x['steps']}|{x['true_window_count']}|{x['optimizer_updates_per_complete_epoch']}|{x['last_batch_size']}|{x['total_optimizer_updates']}|" for x in b)
m2_table='\n'.join(f"|{seed}|"+' / '.join(f"{x['success_once_count']}/50" for x in m['points'] if x['seed']==seed)+f"|{m['seeds'][seed]['winner_epoch']}|{m['seeds'][seed]['best_sr']:.0%}|" for seed in [0,1,2])
live_table='\n'.join(f"|{x['id']}|{x['kind']}|{x['method']}|{x['seed']}|"+(f"{x.get('episodes_completed',0)}/50 episodes（回合），第{x['checkpoint_step']}轮" if x['kind']=='eval' else f"{x['latest_metric'].get('completed_epochs',x['latest_metric'].get('data_epoch',0))}/250轮，{x['latest_metric'].get('optimizer_updates')}次更新"+('；等待其正式评测，正常回压' if x.get('waiting_for_eval') else ''))+'|' for x in status['running'])
text=f'''# 第三章针对性审查与修订

审查基准：main提交`55951414`。核对时间（北京时间）：{stamp}。代码修复提交：`23e5472`；后续报告/结果更新提交见Git历史。
范围保持四模型、五任务、三个训练种子、60训练/300正式评测。没有新增实验组、额外训练或正式评测，没有更换数据子集、batch size（批大小）、预算、控制模式、reset（重置）列表或保存点；没有暂停/重启已有训练、评测或调度器。仅使用GPU2，GPU5未操作。

## 问题位置、证据与处理

| 项目 | 位置及证据 | 结论与修正 | 受影响run |
| --- | --- | --- | --- |
| MimicGen离线/在线一致性 | {location('prepare_mimicgen.py','image=obs')}; {location('gsc_dp/analysis_env.py','def format')}; `mimicgen_saved_state_parity.json` | 3任务×2示范×3真实状态=18状态、36组双相机比较。RGB最大差0、米制Depth最大差0、本体状态最大差0。相机读取/编码顺序一致。六次相同真实动作的单步仿真状态差0；7维相对OSC_POSE（操作空间位姿增量控制）不改变。无需修正转换或重跑。 | 全部36个MimicGen run；没有INVALID |
| Peg成功/失败示范来源 | {location('prepare_maniskill_ch3.py','--save-traj')}; `peg_100_source_replay_cache.json` | 原始前100条官方运动规划轨迹全部success=True；官方joint→EE（关节→末端控制）转换后90成功、10失败。全部100条动作及本体状态逐条与训练缓存完全相同，图像/深度抽样相符。数据说明及manifest补充来源标记，不筛选、不重训。 | Peg全部12个run，当前尚未开始训练 |
| 真实窗口/更新预算 | {location('train.py','total_updates=')}; `window_update_budgets.json`及`experiments/ch3/dataset_budget_metadata.json` | 直接实例化正式SequenceSampler（序列采样器），读取真实索引数，非步数近似；既有run预算元数据一致。论文协议表自动携带窗口、每完整epoch更新数和总更新数。 | 全部60个run；训练总量不改 |
| 主成功率口径及失败原因 | {location('evaluate.py','success_at_end=at_end')}; {location('jobs/export_ch3.py','definition=SUCCESS_DEFINITIONS')}; `result_metadata_before_annotation.json` | MimicGen明确为success_once（执行中至少一次成功）；ManiSkill明确为success_at_end（末步成功）。原标签保存在success_definition_original，数值不改。新增逐回合及汇总口径、EMA（指数滑动平均）来源和评测代码提交字段；修正MimicGen曾成功但末步失败时的failure_reason（失败原因）误标。旧逐回合原文保留。 | 所有正式评测；已完成33点仅补充元数据，不重评 |
| 模型结构与控制变量 | {location('gsc_dp/policy_factory.py','def create')}; `controlled_configs.json`及`controlled_model_architecture.json` | 60份配置除method/seed完全相同（任务内），同一数据、归一化、ResNet18/GN（组归一化）结构和扩散网络。M0无Depth为预定差异。M2/M3共享同一TokenLearner类、8个Token、u/v/d/rho与投影残差融合；M2训练权重在审查副本隔离GSA后，真实输入上的特征和Token权重差均为0。原始模型没有被改写。 | 全部60个run；M2/M3结构核对通过 |
| M0既存初始化/裁剪实现差异 | `crop_initialization_disclosure.json`; {location('gsc_dp/encoder.py','ys = torch.randint')} | M0将一个随机初始化ResNet18复制给两相机，改进模型分别初始化相机主干。随机裁剪支持集存在一个端点差异（下详）；已披露，不宣称四模型初始张量/增强抽样完全相同。中途改动会改变既有实验，因此未悄悄切换实现，未据此擅自新增训练或标INVALID。 | 所有M0与改进模型对比；M2/M3无此差异 |
| Threading M2真实证据链 | `threading_m2_lineage.json` | 15点评测各50完整唯一reset，共750回合；每点EMA元数据、epoch×688更新、训练日志、评测日志、success_once计算、清理记录及保留best均相符。三份实际best EMA均含GSA/TokenLearner与归一化状态；归一化张量与当前固定缓存拟合值逐项相等。 | Threading M2种子0/1/2；结果有效保留 |
| 正式队列/历史隔离 | `queue_scope.json`; `formal_config_enforcement.json`; `historical_summary_exclusion.json`; {location('gsc_dp/protocol.py','def validate_formal_config')} | 实际DB恰好60训练/300评测，仅e0/e3/e6/m3。17个其他保存点摘要不进入正式统计。正式模型创建、下次调度代码和导出增加范围检查；旧方法、旧评测位置及pd_joint_pos（关节位置控制）被拒绝。当前控制器不重启；新worker会加载有效的模型创建检查，现有队列全部合规。 | 全部队列；旧ID/运行状态不变 |

## 真实状态核对细节

输入包括真实原始HDF5中的model XML（仿真场景模型）、states（仿真状态）和actions（动作），官方离线RGB-D HDF5、实际Zarr训练缓存以及正式MimicGenAnalysisEnv（在线环境适配器）。恢复保存状态后调用相同在线format（观测格式化）路径；不是仅比对代码文本。
每任务检查demo_0、demo_199各自首帧/中帧/末帧。直接正确方向差0；人为垂直反转对照有明显差值，详见逐样本JSON。Depth由MuJoCo近/远平面换算为米，与离线米制深度逐像素相等，不是把归一化深度当米。原始action转float32（单精度）后的最大舍入差为{max(x['cache_action_max_abs'] for x in p['samples']):.3g}，未发生语义缩放；HDF5保留原始动作的差为0。

Peg转换失败的源轨迹编号：`{peg['failed_replay_source_ids']}`。训练实际包含源ID0..99对应的全部100条转换轨迹，共15450个动作；每条轨迹的源ID、转换ID、原始/转换成功标记、动作形状及训练缓存区间在JSON逐条列出。不能称为“100条成功的末端控制示范”。

## 真实训练窗口与固定总量

均为batch size=64（批大小64）、sequence length=16（序列长度16）、pad_before=1/pad_after=7（前/后补齐）、drop_last=False（保留不足64条的末批）、无梯度累积、无验证示范划分。

|任务|真实数据步数|真实窗口数|每完整epoch更新数|末批条数|每run总更新数|
|---|---:|---:|---:|---:|---:|
{budget_table}

三个MimicGen任务各250个完整epoch（数据轮次），窗口数不同因而总更新数不同。ManiSkill按100000次真实optimizer.step（优化器更新）停止，最后一个数据epoch可为部分轮次，不能把它写成固定数量的完整epoch。

## M2三种子五点评测

下表为MimicGen的success_once，不能写成末步成功率。

|种子|50 / 100 / 150 / 200 / 250轮成功回合数|最早最佳轮次|Best-of-5（五次取最佳）|
|---|---|---:|---:|
{m2_table}

三种子最高成功率的均值为{m['mean_best_sr']:.2%}，样本标准差为{m['sample_std']*100:.2f}个百分点，ddof=1（样本自由度）。seed2在200/250轮同为22%，保留最早200轮。三种子实际训练均为172000次更新、250完整轮次。

追溯限制必须保留：15个原始临时checkpoint均已按既定低存储协议回收，当前可直接读取的是3份best EMA权重；其余只能据原子写入元数据、训练/评测日志、原始回合和逐文件清理记录追溯，不能再逐位比较已删除张量。历史runner（评测程序）只写入训练代码提交，未单独记录评测程序提交；无法事后无依据补写。新增runner开始明确记录evaluation_code_revision。上述证据缺口没有发现数值矛盾，不等同于已确认评测无效。

## M0的实现差异与当前处理

M0保留官方实现；M1/M2/M3使用同一自定义对齐裁剪。MimicGen 84→76时，M0随机起点为0..7，改进模型为0..8；ManiSkill128→112时，分别为0..15和0..16。评测中心裁剪位置相同，裁剪形状相同，M2/M3使用完全相同的裁剪代码。相机初始化策略也不同，不能宣称初始参数逐位匹配。
这不满足“除预定模块外所有实现细节完全相同”的严格表述，因此已修正文稿，不掩盖该差异。原协议未锁定这些抽样端点/逐相机初始张量，不据此判作预算违规或损坏实验；未经另行约定，不改变已经执行的增强分布或重新训练。

## 实际进度与影响范围

快照时间：{status['checked_at_asia_shanghai']}。训练完成4/60、运行6、排队50；正式评测完成33/300、运行2、排队265，共1650个已完成正式回合。
训练完成的是Threading M0种子0和M2三个种子。其他任务等待当前Threading的12训练/60评测完成后再调度，历史Stack Three的4个合规保存点评测保留。未创建新run或eval ID。

|Job ID|类型|方法|种子|真实进度|
|---:|---|---|---:|---|
{live_table}

INVALID列表为空；需重跑训练0项、需重跑正式评测0项。M0的实现差异作为明确保留的限制披露。既有模型权重、训练恢复状态与原始数据未改；旧结果保留，摘要修改前版本见result_metadata_before_annotation.json。修复不改变已运行worker的数值路径；新评测worker加载元数据/范围修正，已运行评测完成后由导出程序补全口径标签。

审查脚本的一次宽泛文件扫描曾把历史保存点混入元数据核查范围，已改为只按正式队列ID索引；这不是正式汇总程序混入历史数据。此前远程读取不存在envs.py/geometry.py/ch3_protocol.json的请求已按实际analysis_env.py/独立几何模块/protocol.json更正，没有修改错误路径或假造检查结果。
'''
(O/'REPORT.md').write_text(text,encoding='utf8')
summary=dict(baseline='55951414',fix_commit='23e5472',audit_time_beijing=stamp,invalidated_runs=[],training_reruns=0,evaluation_reruns=0,budgets=b,real_state_parity_samples=18,camera_comparisons=36,peg_replay_failure_ids=peg['failed_replay_source_ids'],m2_mean=m['mean_best_sr'],m2_sample_std=m['sample_std'],controlled_exceptions=crop,progress=status['counts'],report='docs/audit_55951414/REPORT.md')
(O/'audit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
for name in ['task_plan.md','findings.md','progress.md']:
    plan=R.parent/'.planning/protocol_v1'/name
    with plan.open('a',encoding='utf8') as f:f.write(f'\n\n## 55951414针对性修正完成 {stamp}\n真实状态核对18状态/36双相机对比，RGB/米制Depth/本体一致、六次相同动作转移差0；Peg原始100成功、控制转换后90成功10失败且全部进入训练；五任务窗口及固定预算已写元数据。M2的15点750回合、三个best EMA及归一化证据核对通过，17.33%±4.16个百分点明确为success_once。修复提交23e5472：口径标签、未来评测代码提交/EMA来源、失败原因、四模型正式配置拒绝旧组/旧位置/旧控制模式、论文/数据说明。已披露M0相机初始化及裁剪端点差异，不宣称完全一致，不改已有训练。临时历史张量及旧评测代码提交缺少直接证据，明确保留限制，不伪造补齐。INVALID为空、重训/重评0；全部现有合规训练评测保持原PID继续执行。详见docs/audit_55951414/REPORT.md。\n')
    (R/name).write_text(plan.read_text(encoding='utf8'),encoding='utf8')
print('REPORT_READY',str(O/'REPORT.md'),stamp)
