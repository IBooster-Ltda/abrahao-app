#!/bin/bash
cd /home/user/abrahao-app/videos/iveststudy-promo
mkdir -p deliver renders
for n in ad30a ad15 ad06 ad30b ad30c ad-sat-en ad45-1920x1080 ad45-1080x1080; do
  cp builds/$n.html index.html
  npx -y hyperframes@0.9.26 render -o renders/$n-raw.mp4 --json > renders/$n.log 2>&1
  if [ ! -f renders/$n-raw.mp4 ]; then echo "RENDER FAIL $n"; tail -c 600 renders/$n.log; continue; fi
  # two-pass loudness normalisation to -14 LUFS integrated, -1 dBTP; video stream copied (H.264, 30 fps)
  J=$(ffmpeg -v info -i renders/$n-raw.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  II=$(echo "$J" | python3 -I -c "import json,sys;d=json.load(sys.stdin);print(d['input_i'],d['input_tp'],d['input_lra'],d['input_thresh'],d['target_offset'])")
  set -- $II
  ffmpeg -v error -y -i renders/$n-raw.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$1:measured_TP=$2:measured_LRA=$3:measured_thresh=$4:offset=$5:linear=true" -c:a aac -b:a 192k -movflags +faststart deliver/$n.mp4
  echo "DONE $n $(ffprobe -v error -show_entries format=duration -of csv=p=0 deliver/$n.mp4)"
done
cp builds/ad30a.html index.html
echo ALLRENDERED
