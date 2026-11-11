#!/bin/bash
# Render both light-trail cuts, then two-pass loudnorm to -14 LUFS / -1 dBTP (video copied).
cd "$(dirname "$0")/.."
mkdir -p deliver renders
for F in 1080x1920 1920x1080; do
  cp builds/trail-$F.html index.html
  npx -y hyperframes@0.9.26 render -o renders/trail-$F-raw.mp4 --json > renders/trail-$F.log 2>&1 || { echo "RENDER FAIL $F"; tail -c 600 renders/trail-$F.log; continue; }
  J=$(ffmpeg -v info -i renders/trail-$F-raw.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  set -- $(echo "$J" | python3 -I -c "import json,sys;d=json.load(sys.stdin);print(d['input_i'],d['input_tp'],d['input_lra'],d['input_thresh'],d['target_offset'])")
  ffmpeg -v error -y -i renders/trail-$F-raw.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$1:measured_TP=$2:measured_LRA=$3:measured_thresh=$4:offset=$5:linear=true" -c:a aac -b:a 192k -movflags +faststart deliver/trail-$F.mp4
  echo "DONE $F $(ffprobe -v error -show_entries format=duration -of csv=p=0 deliver/trail-$F.mp4)"
done
cp builds/trail-1080x1920.html index.html
echo ALLRENDERED
