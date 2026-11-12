#!/bin/bash
# Render the narrated light-trail cut in both formats at delivery quality,
# then a light unsharp pass, two-pass loudnorm (-14 LUFS / -1 dBTP) and a high-bitrate H.264 master.
cd "$(dirname "$0")/.."
mkdir -p deliver renders
for F in 1080x1920 1920x1080; do
  cp builds/trail4-$F.html index.html
  npx -y hyperframes@0.9.26 render -o renders/trail4-$F-raw.mp4 --quality delivery --crf 10 --json > renders/trail4-$F.log 2>&1 || { echo "RENDER FAIL $F"; tail -c 600 renders/trail4-$F.log; continue; }
  J=$(ffmpeg -v info -i renders/trail4-$F-raw.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  set -- $(echo "$J" | python3 -I -c "import json,sys;d=json.load(sys.stdin);print(d['input_i'],d['input_tp'],d['input_lra'],d['input_thresh'],d['target_offset'])")
  ffmpeg -v error -y -i renders/trail4-$F-raw.mp4 -vf "unsharp=5:5:0.55:5:5:0.0" -c:v libx264 -preset slow -crf 14 -profile:v high -pix_fmt yuv420p -tune animation -x264-params "aq-mode=3" \
    -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$1:measured_TP=$2:measured_LRA=$3:measured_thresh=$4:offset=$5:linear=true" -c:a aac -b:a 192k -movflags +faststart deliver/trail4-$F.mp4
  echo "DONE $F $(ffprobe -v error -show_entries format=duration:stream=bit_rate -select_streams v -of csv=p=0 deliver/trail4-$F.mp4 | tr '\n' ' ')"
done
cp builds/trail4-1080x1920.html index.html
echo ALLRENDERED
