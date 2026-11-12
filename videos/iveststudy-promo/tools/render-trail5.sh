#!/bin/bash
# Render the Ana Alice cut in both formats: delivery quality, light unsharp, -14 LUFS / <= -1.2 dBTP.
cd "$(dirname "$0")/.."
mkdir -p deliver renders
for F in 1080x1920 1920x1080; do
  cp builds/trail5-$F.html index.html
  npx -y hyperframes@0.9.26 render -o renders/trail5-$F-raw.mp4 --quality delivery --crf 10 --json > renders/trail5-$F.log 2>&1 || { echo "RENDER FAIL $F"; tail -c 600 renders/trail5-$F.log; continue; }
  ffmpeg -v error -y -i renders/trail5-$F-raw.mp4 -vf "unsharp=5:5:0.55:5:5:0.0" -c:v libx264 -preset slow -crf 14 -profile:v high -pix_fmt yuv420p -tune animation -x264-params "aq-mode=3" \
    -af "alimiter=limit=0.79:attack=3:release=60:level=disabled,loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -movflags +faststart deliver/trail5-$F.mp4
  echo "DONE $F $(ffprobe -v error -show_entries format=duration -of csv=p=0 deliver/trail5-$F.mp4)"
done
cp builds/trail5-1080x1920.html index.html
echo ALLRENDERED
