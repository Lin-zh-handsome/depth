set -e
CONDA=/home/linzhenghong/miniconda3/bin/conda
C=/home/linzhenghong/project/gsc_dp_chapter3/campaign_v1
if [ ! -x /home/linzhenghong/miniconda3/envs/gsc-thesis-eval/bin/python ]; then
  "$CONDA" create -y --name gsc-thesis-eval --clone gsc-robodiff
fi
PY=/home/linzhenghong/miniconda3/envs/gsc-thesis-eval/bin/python
"$PY" -m pip install mani_skill==3.0.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
echo environment_ready
