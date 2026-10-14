"""Runtime-only GPU2 duty-cycle governor; never alters model or experiment protocol."""
import ctypes,fcntl,json,os,signal,time
from pathlib import Path
from datetime import datetime,timezone,timedelta
ROOT=Path(__file__).resolve().parents[1]
GPU='GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9'
class Rates(ctypes.Structure):_fields_=[('gpu',ctypes.c_uint),('memory',ctypes.c_uint)]
lib=ctypes.CDLL('libnvidia-ml.so.1');handle=ctypes.c_void_p()
lib.nvmlDeviceGetHandleByUUID.argtypes=[ctypes.c_char_p,ctypes.POINTER(ctypes.c_void_p)]
if lib.nvmlInit_v2()!=0 or lib.nvmlDeviceGetHandleByUUID(GPU.encode(),ctypes.byref(handle))!=0:raise RuntimeError('NVML GPU2 unavailable')
lock=(ROOT/'jobs/gpu_load_governor.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
stop=[False];signal.signal(signal.SIGTERM,lambda *_:stop.__setitem__(0,True));signal.signal(signal.SIGINT,lambda *_:stop.__setitem__(0,True))
paused=set();duty=.80;history=[]
allowed={str(ROOT/'train.py'),str(ROOT/'evaluate.py'),str(ROOT/'analysis/temporal_attention.py')}
def eligible(pid):
 p=Path('/proc')/str(pid)
 try:
  if p.stat().st_uid!=os.getuid() or (p/'cwd').resolve()!=ROOT:return False
  args=(p/'cmdline').read_bytes().split(b'\0')
  if len(args)<2 or args[1].decode() not in allowed:return False
  env=dict(x.split('=',1) for x in (p/'environ').read_bytes().decode().split('\0') if '=' in x)
  return env.get('CUDA_VISIBLE_DEVICES')==GPU
 except OSError:return False
def workers():return [int(p.name) for p in Path('/proc').iterdir() if p.name.isdigit() and eligible(int(p.name))]
def resume():
 for pid in list(paused):
  try:
   if eligible(pid):os.kill(pid,signal.SIGCONT)
  except ProcessLookupError:pass
  paused.discard(pid)
def sample_for(seconds,values):
 end=time.monotonic()+seconds
 while not stop[0] and time.monotonic()<end:
  v=Rates()
  if lib.nvmlDeviceGetUtilizationRates(handle,ctypes.byref(v))==0:values.append(int(v.gpu))
  time.sleep(min(.5,max(0,end-time.monotonic())))
try:
 while not stop[0]:
  cfg=json.loads((ROOT/'jobs/gpu_load_target.json').read_text())
  if not cfg.get('enabled',True):resume();time.sleep(1);continue
  target=cfg.get('target_percent',70);cycle=cfg.get('cycle_seconds',6);values=[]
  resume();sample_for(cycle*duty,values)
  pids=workers()
  for pid in pids:
   try:os.kill(pid,signal.SIGSTOP);paused.add(pid)
   except ProcessLookupError:pass
  sample_for(cycle*(1-duty),values);resume()
  average=sum(values)/len(values) if values else 0;history.append(average);history=history[-10:]
  if pids and abs(average-target)>3:duty=max(.20,min(.98,duty+.25*(target-average)/100))
  state=dict(timestamp=datetime.now(timezone(timedelta(hours=8))).isoformat(),target_percent=target,cycle_mean_percent=round(average,1),recent_mean_percent=round(sum(history)/len(history),1),active_fraction=round(duty,3),controlled_pids=pids,physical_gpu=2)
  path=ROOT/'jobs/gpu_load_state.json';tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(state,indent=2));os.replace(tmp,path)
  print(json.dumps(state),flush=True)
finally:
 resume();lib.nvmlShutdown()
