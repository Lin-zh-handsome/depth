"""Execute the official converter with its renderer probe pinned to GPU2."""
import runpy
from pathlib import Path
import sys
import egl_probe
import robomimic
import mimicgen  # official Core task registration before the converter runs

# robomimic may otherwise select the first probed physical EGL GPU even when
# CUDA_VISIBLE_DEVICES exposes a different device. This changes only device
# selection, not data conversion, observation processing, physics, or actions.
egl_probe.get_available_devices=lambda:[2]
official=Path(robomimic.__file__).parent/'scripts/dataset_states_to_obs.py'
sys.argv[0]=str(official)
runpy.run_path(str(official),run_name='__main__')
