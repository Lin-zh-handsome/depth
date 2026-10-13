set -e
C=/home/linzhenghong/project/gsc_dp_chapter3/campaign_v1
target="$C/data/raw/mimicgen/stack_three_d1.hdf5"
[ -s "$target" ] && exit 0
# Resume the exact partial official dataset; retry truncated transfers too.
if curl -fL -C - --retry 3 --retry-all-errors --retry-delay 5 --connect-timeout 20 --max-time 1800 \
    "https://hf-mirror.com/datasets/amandlek/mimicgen_datasets/resolve/main/core/stack_three_d1.hdf5?download=true&resume=20261013" \
    -o "$target.part"; then
  mv "$target.part" "$target"
else
  echo 'Domestic mirror resumed transfer failed; use the user-provided Clash proxy for the same official dataset.'
  export http_proxy=http://127.0.0.1:7890 https_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7891
  curl -fL -C - --retry 3 --retry-all-errors --connect-timeout 20 --max-time 1800 \
    'https://huggingface.co/datasets/amandlek/mimicgen_datasets/resolve/main/core/stack_three_d1.hdf5?download=true' \
    -o "$target.part"
  mv "$target.part" "$target"
fi
