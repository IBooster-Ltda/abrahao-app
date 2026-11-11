import json,sys,os,subprocess
src,out,fps=sys.argv[1],sys.argv[2],30
m=json.load(open(f'{src}/meta.json')); fr=m['frames']
if not fr: print('no frames'); sys.exit(1)
t0=fr[0][1]
lines=[]
for k,(i,t,_) in enumerate(fr):
    f=f'{src}/f{i:06d}.jpg'
    if not os.path.exists(f): continue
    nxt=fr[k+1][1] if k+1<len(fr) else t+0.5
    d=max(1/fps,nxt-t)
    lines.append(f"file '{f}'\nduration {d:.4f}")
lines.append(f"file '{f}'")
open(f'{src}/list.txt','w').write('\n'.join(lines)+'\n')
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{src}/list.txt','-vf',f'fps={fps},scale=1290:2796:flags=lanczos,format=yuv420p','-c:v','libx264','-preset','medium','-crf','16',out],check=True)
# marks relative to the first frame's wall clock
wall0=fr[0][2]/1000.0
marks={lab:round(t-wall0,2) for lab,t in m['marks']}
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out],capture_output=True,text=True).stdout)
json.dump({'duration':round(dur,2),'marks':marks,'frames':len(fr)},open(out.replace('.mp4','.json'),'w'))
print(os.path.basename(out),'dur',round(dur,2),'frames',len(fr),'marks',marks)
