set -e
export PYTHONNOUSERSITE=1 OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
C=/home/linzhenghong/project/gsc_dp_chapter3/campaign_v1
CONDA=/home/linzhenghong/miniconda3/bin/conda
if [ ! -x /home/linzhenghong/miniconda3/envs/gsc-thesis-mimic/bin/python ]; then
  "$CONDA" create -y --name gsc-thesis-mimic --clone gsc-robodiff
fi
PY=/home/linzhenghong/miniconda3/envs/gsc-thesis-mimic/bin/python
"$PY" -m pip install robosuite==1.4.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
# robomimic 0.3 does not expose the required depth observation/conversion API.
# Reuse the existing official 0.4 source while preserving robosuite 1.4.1.
"$PY" -m pip install --no-deps -e /home/linzhenghong/project/gsc_dp_chapter3/third_party/robomimic_v0_4 \
  -i https://pypi.tuna.tsinghua.edu.cn/simple
"$PY" -m pip install --no-deps -e "$C/source/mimicgen" -i https://pypi.tuna.tsinghua.edu.cn/simple
touch "$C/logs/mimic_env.ready"
