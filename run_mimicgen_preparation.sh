set -e
C=/home/linzhenghong/project/gsc_dp_chapter3/campaign_v1
export PYTHONNOUSERSITE=1 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
export CUDA_VISIBLE_DEVICES=GPU-d191b5a1-ec3c-2aa9-8b29-9b6272ac74c9 GSC_GPU=2
export MUJOCO_GL=egl MUJOCO_EGL_DEVICE_ID=2
while [ ! -f "$C/logs/mimic_env.ready" ]; do
  sleep 30
done
cd "$C"
/home/linzhenghong/miniconda3/envs/gsc-thesis-mimic/bin/python prepare_mimicgen.py
