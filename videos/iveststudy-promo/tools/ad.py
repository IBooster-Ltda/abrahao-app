# iVest Study performance ads — narration-driven, phone-recorded, beat-cut. Writes index-*.html + .srt
import json, os, sys, math, subprocess, datetime
P='/home/user/abrahao-app/videos/iveststudy-promo'; os.chdir(P)
S='tools'
VOT=json.load(open('assets/audio/vo30/timing.json'))
M={n:json.load(open(f'assets/app/m3/{n}.json'))['marks'] for n in ['estudo','redacao','simulados','flashcards','mentor','quiz','home','signup','en-estudo','en-simulados','en-home']}
HK=json.load(open(f'{S}/m/hookA.json'))
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
RED_RESULT=31.0   # measured: the 480/1000 card appears here in assets/app/m3/redacao.mp4
ENEM_DATE=datetime.date(2026,11,15)   # INEP: 8 and 15 Nov 2026 (Edital nº 64/2026). Update before publishing.
TODAY=datetime.date.today()

class Film:
    def __init__(s, name, W, H, lang='pt'):
        s.name,s.W,s.H,s.lang=name,W,H,lang; s.els=[]; s.js=[]; s.audio=[]; s.sfx=[]; s.cues=[]; s.n=0; s.T=0
        # layout
        if (W,H)==(1080,1920):
            s.PW=600; s.PX=240; s.PY=470; s.TY=255; s.TW=W-120; s.TX=60; s.CAPY=1400; s.TS=84; s.WMY=1512; s.SUBS=44
        elif (W,H)==(1920,1080):
            s.PW=400; s.PX=1280; s.PY=104; s.TY=300; s.TW=1040; s.TX=120; s.CAPY=940; s.TS=84; s.WMY=40; s.SUBS=40
        else: # 1080x1080
            s.PW=400; s.PX=620; s.PY=104; s.TY=250; s.TW=520; s.TX=50; s.CAPY=980; s.TS=64; s.WMY=36; s.SUBS=36
        s.PH=round(s.PW*2796/1290); s.base=s.PW/1290
    def uid(s,p='e'): s.n+=1; return f'{p}{s.n}'
    # ── camera inside the phone (source coords 1290x2796)
    def cam(s, sc, fx, fy):
        Sx=s.base*sc; x=s.PW/2-fx*Sx; y=s.PH/2-fy*Sx
        x=min(0,max(s.PW-1290*Sx,x)); y=min(0,max(s.PH-2796*Sx,y))
        return f'{{ scale: {Sx:.5f}, x: {x:.1f}, y: {y:.1f} }}'
    def phone(s, src, start, d, mstart, rate=1.0, cams=None, zidx=2, inner=''):
        """cams: list of (t_rel, sc, fx, fy, move_dur, ease). First entry is the initial framing."""
        pid=s.uid('ph'); cid=f'{pid}c'; vid=f'{pid}v'
        s.els.append(f'''<div id="{pid}" class="ph" style="z-index:{zidx};visibility:hidden;opacity:0"><div class="island"></div><div id="{cid}" class="cam"><video id="{vid}" class="clip" src="{src}" data-start="{start}" data-duration="{d}" data-media-start="{mstart:.2f}"{f' data-playback-rate="{rate}"' if rate!=1 else ''} muted playsinline data-track-index="2"></video>{inner}</div></div>''')
        cams=cams or [(0,1.0,645,1398,0,'none')]
        t0,sc,fx,fy,_,_=cams[0]
        s.js.append(f'tl.set("#{cid}", {s.cam(sc,fx,fy)}, {start+t0:.3f});')
        for (t,sc,fx,fy,md,ease) in cams[1:]:
            s.js.append(f'tl.to("#{cid}", {{ ...{s.cam(sc,fx,fy)}, duration: {md}, ease: "{ease}" }}, {start+t-md:.3f});')
        s.js.append(f'tl.set("#{pid}", {{ autoAlpha: 1 }}, {start:.3f}); tl.fromTo("#{pid}", {{ scale: 0.97 }}, {{ scale: 1, duration: 0.3, ease: "power3.out", immediateRender: false }}, {start:.3f}); tl.set("#{pid}", {{ autoAlpha: 0 }}, {start+d-0.001:.3f});')
        return pid,cid
    def ovl(s, cid_html_target, html):
        pass
    # ── text
    def words(s, text, acc=()):
        out=[]
        for w in text.split(' '):
            a=' acc' if w.strip('.,:!?') in acc or w in acc else ''
            out.append(f'<span class="w{a}">{w}</span>')
        return ' '.join(out)
    def title(s, lines, start, d, y=None, size=None, acc=(), align=None, x=None, w=None, cls=''):
        tid=s.uid('t'); y=s.TY if y is None else y; size=size or s.TS; x=s.TX if x is None else x; w=s.TW if w is None else w
        align=align or ('center' if s.W==1080 else 'left')
        html=''.join(f'<div class="ln">{s.words(l,acc)}</div>' for l in lines)
        s.els.append(f'<div id="{tid}" class="ttl {cls} clip" data-start="{start}" data-duration="{d}" style="left:{x}px;top:{y}px;width:{w}px;font-size:{size}px;text-align:{align}" data-layout-allow-overflow>{html}</div>')
        s.js.append(f'document.querySelectorAll("#{tid} .w").forEach((w,i)=>tl.fromTo(w,{{opacity:0,y:28,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.32,ease:"power3.out"}},{start:.3f}+i*0.045));')
        s.js.append(f'tl.to("#{tid}", {{ opacity: 0, y: -16, filter: "blur(6px)", duration: 0.22, ease: "power2.in" }}, {start+d-0.24:.3f});')
        return tid
    def sub(s, text, start, d, y, size=None, align=None):
        tid=s.uid('s'); size=size or s.SUBS; align=align or ('center' if s.W==1080 else 'left')
        s.els.append(f'<div id="{tid}" class="subt clip" data-start="{start}" data-duration="{d}" style="left:{s.TX}px;top:{y}px;width:{s.TW}px;font-size:{size}px;text-align:{align}" data-layout-allow-overflow>{text}</div>')
        s.js.append(f'tl.fromTo("#{tid}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{start+0.1:.3f}); tl.to("#{tid}",{{opacity:0,duration:0.2}},{start+d-0.22:.3f});')
    def chip(s, text, start, d, x, y, kind='ok', w=None):
        cid=s.uid('ch'); icon='✓' if kind=='ok' else '✗'
        s.els.append(f'<div id="{cid}" class="chip {kind} clip" data-start="{start}" data-duration="{d}" style="left:{x}px;top:{y}px;{f"width:{w}px;" if w else ""}" data-layout-allow-overflow><span class="ic">{icon}</span><span>{text}</span></div>')
        s.js.append(f'tl.fromTo("#{cid}",{{opacity:0,scale:0.7,x:-20}},{{opacity:1,scale:1,x:0,duration:0.35,ease:"back.out(2)",transformOrigin:"0% 50%"}},{start:.3f}); tl.to("#{cid}",{{opacity:0,duration:0.2}},{start+d-0.22:.3f});')
    def photo(s, src, start, d, sc0=1.04, sc1=1.12, dark=0.45, ox=0, oy=0):
        pid=s.uid('im')
        s.els.append(f'<div id="{pid}" class="photo clip" data-start="{start}" data-duration="{d}"><img src="{src}" alt="" /><div class="shade" style="opacity:{dark}"></div></div>')
        s.js.append(f'tl.fromTo("#{pid} img",{{scale:{sc0},x:{ox},y:{oy}}},{{scale:{sc1},x:0,y:0,duration:{d},ease:"none"}},{start:.3f});')
        return pid
    def bg(s, start, d, kind='navy'):
        bid=s.uid('bg'); s.els.append(f'<div id="{bid}" class="bgc {kind} clip" data-start="{start}" data-duration="{d}"></div>'); return bid
    def watermark(s, start, d):
        s.els.append(f'<div class="wm clip" data-start="{start}" data-duration="{d}" style="top:{s.WMY}px">iveststudy.com</div>')
    # ── audio
    def vo(s, key, at, vol=1.0):
        f=f'assets/audio/vo30/{key}.wav'; d=VOT[key]['dur']
        s.audio.append(f'<audio class="clip" src="{f}" data-start="{at:.2f}" data-duration="{d:.2f}" data-volume="{vol}" data-track-index="7"></audio>')
        # caption cues
        ws=[list(w) for w in VOT[key]['words']]
        for w in ws:
            if w[0].lower().startswith('aivest'): w[0]='iVest'
        merged=[]; i=0
        while i<len(ws):
            seq=[x[0].lower().strip('.,') for x in ws[i:i+4]]
            if seq[:4]==['ivest','study','ponto','com'] or seq[:3]==['iveststudy','dot','com']:
                n=4 if seq[:4]==['ivest','study','ponto','com'] else 3
                merged.append(['iveststudy.com',ws[i][1],ws[i+n-1][2]]); i+=n
            else: merged.append(ws[i]); i+=1
        ws=merged; cur=[]; t0=None
        def flush():
            nonlocal cur,t0
            if not cur: return
            txt=' '.join(w for w,_,_ in cur); a=at+cur[0][1]; b=at+cur[-1][2]+0.12
            s.cues.append((round(a,2),round(b,2),txt)); cur=[]
        for w,a,b in ws:
            if cur and (len(cur)>=4 or (b-cur[0][1])>1.9 or cur[-1][0].endswith(('.',',','!','?','…'))): flush()
            cur.append((w,a,b))
        flush()
        return at+d
    def music(s, src, start, d, mstart=0.0, vol=0.42, fin=0.0, fout=0.0, auto=None):
        a=f" data-automation='{json.dumps(auto)}'" if auto else ''
        s.audio.append(f'<audio class="clip" src="{src}" data-start="{start:.2f}" data-duration="{d:.2f}" data-media-start="{mstart:.2f}" data-volume="{vol}" data-fade-in="{fin}" data-fade-out="{fout}" data-track-index="3"{a}></audio>')
    def fx(s, name, at, vol=0.5): s.sfx.append((name,round(at,3),vol))
    # ── build
    def build(s, total):
        s.T=total
        # captions
        capw=min(920,s.W-120)
        s.cues.sort(key=lambda c:c[0])
        s.cues=[(a,min(b,s.cues[i+1][0]-0.04) if i+1<len(s.cues) else b,txt) for i,(a,b,txt) in enumerate(s.cues)]
        s.cues=[(a,min(b,total-0.05),txt) for (a,b,txt) in s.cues if a<total-0.3]
        for i,(a,b,txt) in enumerate(s.cues):
            s.els.append(f'<div class="cap clip" data-start="{a}" data-duration="{max(0.4,round(b-a,2))}" style="top:{s.CAPY}px;max-width:{capw}px">{txt}</div>')
        # sfx lanes
        lanes=[8,9,10,11,12,13,14,15]; free={l:0.0 for l in lanes}; out=[]
        for (n,t,v) in sorted(s.sfx,key=lambda x:x[1]):
            dd=min(dur(f'assets/sfx/{n}.mp3'),4.0); dd=min(dd,max(0.25,total-t))
            lane=next((l for l in lanes if free[l]<=t),None) or min(lanes,key=lambda l:free[l]); free[lane]=t+dd+0.02
            out.append(f'<audio class="clip" src="assets/sfx/{n}.mp3" data-start="{t}" data-duration="{dd:.2f}" data-volume="{v}" data-track-index="{lane}"></audio>')
        css=f'''
      :root {{ --blue:#2563eb; --blue2:#60a5fa; --ok:#22c55e; --miss:#f87171; }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{s.W}px; height:{s.H}px; overflow:hidden; background:#070b14; font-family:"Inter",sans-serif; }}
      #root {{ position:relative; width:{s.W}px; height:{s.H}px; overflow:hidden; background:#070b14; color:#fff; }}
      .bgc {{ position:absolute; inset:0; }}
      .bgc.navy {{ background: radial-gradient(120% 80% at 50% 30%, #152a5c 0%, #0b1220 55%, #070b14 100%); }}
      .bgc.blue {{ background:#2563eb; }}
      .photo {{ position:absolute; inset:0; overflow:hidden; }} .photo img {{ position:absolute; left:0; top:0; width:100%; height:100%; object-fit:cover; transform-origin:50% 50%; }}
      .photo .shade {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(5,8,16,.75) 0%, rgba(5,8,16,.35) 45%, rgba(5,8,16,.85) 100%); }}
      .ph {{ position:absolute; left:{s.PX}px; top:{s.PY}px; width:{s.PW}px; height:{s.PH}px; border-radius:{int(s.PW*0.085)}px; overflow:hidden; background:#000; border:{max(6,int(s.PW*0.014))}px solid #1a2030; box-shadow:0 40px 90px rgba(0,0,0,.6), 0 0 0 2px rgba(255,255,255,.06); transform-origin:50% 50%; }}
      .ph .island {{ position:absolute; left:50%; top:{int(s.PW*0.03)}px; width:{int(s.PW*0.28)}px; height:{int(s.PW*0.07)}px; margin-left:-{int(s.PW*0.14)}px; border-radius:999px; background:#000; z-index:5; }}
      .ph .cam {{ position:absolute; left:0; top:0; width:1290px; height:2796px; transform-origin:0 0; }}
      .ph .cam video {{ position:absolute; left:0; top:0; width:1290px; height:2796px; display:block; }}
      .ttl {{ position:absolute; font-weight:800; line-height:1.08; letter-spacing:-0.035em; color:#fff; text-shadow:0 2px 24px rgba(0,0,0,.6); z-index:6; }}
      .ttl .ln {{ display:block; }} .ttl .w {{ display:inline-block; margin-right:.22em; }} .ttl .acc {{ color:var(--blue2); }} .ttl.ok .acc {{ color:var(--ok); }} .ttl.miss .acc {{ color:var(--miss); }}
      .ttl.big {{ font-size:{int(s.TS*1.45)}px; }}
      .subt {{ position:absolute; font-weight:600; line-height:1.25; color:#e6ebf5; text-shadow:0 2px 16px rgba(0,0,0,.6); z-index:6; }}
      .chip {{ position:absolute; display:flex; align-items:center; gap:14px; padding:16px 24px; border-radius:18px; font-size:{int(s.SUBS*0.95)}px; font-weight:700; color:#fff; background:rgba(8,12,22,.92); border:2px solid; box-shadow:0 14px 40px rgba(0,0,0,.5); z-index:7; max-width:{s.W-80}px; line-height:1.2; }}
      .chip .ic {{ width:46px; height:46px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:30px; flex:0 0 46px; color:#06101c; }}
      .chip.ok {{ border-color:var(--ok); }} .chip.ok .ic {{ background:var(--ok); }} .chip.miss {{ border-color:var(--miss); }} .chip.miss .ic {{ background:var(--miss); }}
      .cap {{ position:absolute; left:50%; transform:translateX(-50%); padding:12px 26px; border-radius:16px; background:rgba(5,8,16,.74); color:#fff; font-size:{s.SUBS+2}px; font-weight:700; line-height:1.25; text-align:center; z-index:9; white-space:nowrap; }}
      .wm {{ position:absolute; right:{s.TX}px; font-size:{int(s.SUBS*0.8)}px; font-weight:700; color:#fff; opacity:.92; letter-spacing:-0.01em; z-index:8; padding:8px 14px; border-radius:10px; background:rgba(5,8,16,.5); }}
      .ring {{ position:absolute; border:6px solid var(--miss); border-radius:18px; box-shadow:0 0 30px rgba(248,113,113,.9); }}
      .quote {{ position:absolute; z-index:7; background:rgba(8,12,22,.94); border:2px solid rgba(255,255,255,.12); border-radius:26px; padding:28px 32px; line-height:1.3; font-weight:600; color:#e6ebf5; box-shadow:0 20px 60px rgba(0,0,0,.55); }}
      .quote .lab {{ font-size:28px; font-weight:700; letter-spacing:.14em; text-transform:uppercase; color:#9db5ff; margin-bottom:.5em; }}
      .quote b {{ font-weight:800; }}
      .num {{ position:absolute; font-weight:800; color:#fff; letter-spacing:-0.04em; line-height:1; }}
      .logo {{ position:absolute; display:flex; align-items:center; justify-content:center; gap:.26em; font-weight:800; letter-spacing:-0.04em; color:#fff; z-index:6; }}
      .logo .st {{ font-weight:500; color:#fff; }} .logo.onblue .i {{ color:#fff; }} .logo .i {{ color:var(--blue2); }}
      .logo svg {{ width:1em; height:1em; border-radius:.24em; }}
      .btn {{ position:absolute; left:50%; transform:translateX(-50%); background:var(--blue); color:#fff; font-weight:700; border-radius:22px; padding:26px 54px; box-shadow:0 0 50px rgba(37,99,235,.55); z-index:6; white-space:nowrap; }}
      .url {{ position:absolute; left:0; width:100%; text-align:center; font-weight:800; color:#fff; letter-spacing:-0.03em; z-index:6; }}
      .badge {{ position:absolute; display:flex; align-items:center; justify-content:center; font-weight:800; color:#fff; background:rgba(255,255,255,.08); border:2px solid rgba(255,255,255,.18); border-radius:22px; z-index:6; }}
      .step {{ position:absolute; display:flex; align-items:center; gap:22px; z-index:6; }} .step .n {{ width:72px; height:72px; border-radius:50%; background:var(--blue); display:flex; align-items:center; justify-content:center; font-weight:800; font-size:36px; flex:0 0 72px; box-shadow:0 0 30px rgba(37,99,235,.6); }}
      .step .tx {{ font-weight:700; font-size:{s.SUBS+6}px; line-height:1.15; }}
'''
        html=f'''<!doctype html>
<html lang="{ 'pt-BR' if s.lang=='pt' else 'en' }">
<head><meta charset="UTF-8" /><meta name="viewport" content="width={s.W}, height={s.H}" /><script src="assets/vendor/gsap.min.js"></script>
<style>{css}</style></head>
<body>
<div id="root" data-composition-id="{s.name}" data-start="0" data-duration="{total}" data-width="{s.W}" data-height="{s.H}" data-fps="30">
{chr(10).join(s.els)}
{chr(10).join(s.audio)}
{chr(10).join(out)}
</div>
<script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join(s.js)}
  window.__timelines["{s.name}"] = tl;
</script>
</body></html>
'''
        import re
        k=[0]
        def addid(m):
            k[0]+=1; return m.group(1)+f' id="auto{k[0]}"'+m.group(2)
        html=re.sub(r'(<(?:div|audio|video|p|span))((?![^>]*\bid=)[^>]*class="[^"]*\bclip\b[^>]*>)', addid, html)
        os.makedirs('builds',exist_ok=True); open(f'builds/{s.name}.html','w',encoding='utf-8').write(html)
        # srt
        def ts(t): h=int(t//3600); m=int(t%3600//60); sec=t%60; return f'{h:02d}:{m:02d}:{sec:06.3f}'.replace('.',',')
        srt=''.join(f'{i+1}\n{ts(a)} --> {ts(b)}\n{txt}\n\n' for i,(a,b,txt) in enumerate(s.cues))
        os.makedirs('deliver',exist_ok=True); open(f'deliver/{s.name}.srt','w',encoding='utf-8').write(srt)
        print('wrote', f'builds/{s.name}.html', 'cues', len(s.cues), 'sfx', len(out))

BRAND_SVG=open('assets/brand/icons/brand.svg',encoding='utf-8').read().replace('width="36" height="36"','')
def logo_html(f, size, y, x=None, w=None, study=True, inv=False):
    x=0 if x is None else x; w=f.W if w is None else w
    svg=BRAND_SVG if not inv else open('assets/brand/icons/brand-inv.svg',encoding='utf-8').read().replace('width="36" height="36"','')
    return f'<div class="logo{" onblue" if inv else ""}" style="left:{x}px;width:{w}px;top:{y}px;font-size:{size}px">{svg}<span><span class="i">i</span>Vest{" <span class=st>Study</span>" if study else ""}</span></div>'

# ─────────────────────────────────────────── scene blocks (times absolute)
def hook_A(f, t0):
    # the real essay result: digits count 0→480 over the real UI, then the real frame; C2 80/200 flagged
    bx=HK['bbox']; bgc='rgb(%d,%d,%d)'%tuple(HK['bg'])
    x0,y0,x1,y1=bx; h=y1-y0
    cnt=f'<div id="cnt" class="num clip" data-start="{t0}" data-duration="1.15" style="left:{x0-14}px;top:{y0-22}px;width:{x1-x0+22}px;height:{h+44}px;background:{bgc};font-size:{int(h/0.72)}px;text-align:right;padding-right:0;line-height:{h+44}px"><span class="v">0</span></div><div id="ring1" class="ring clip" data-start="{t0+1.1:.2f}" data-duration="0.9" style="left:1030px;top:1560px;width:190px;height:110px;opacity:0"></div>'
    f.bg(t0,2.0,'navy')
    f.phone('assets/app/m3/redacao.mp4', t0, 2.0, RED_RESULT+0.3, 1.0, cams=[(0,1.3,760,1100,0,'none'),(2.0,1.36,760,1150,2.0,'none')], inner=cnt)
    f.js.append(f'{{ const el=document.querySelector("#cnt .v"); const st={{v:0}}; tl.fromTo(st,{{v:0}},{{v:480,duration:0.85,ease:"power2.out",onUpdate:()=>{{el.textContent=String(Math.round(st.v));}}}},{t0+0.15:.3f}); }}')
    f.js.append(f'tl.fromTo("#ring1",{{opacity:0,scale:1.25}},{{opacity:1,scale:1,duration:0.18,ease:"power3.out",transformOrigin:"50% 50%",immediateRender:false}},{t0+1.1:.3f}); tl.to("#ring1",{{opacity:0.35,duration:0.18,yoyo:true,repeat:3}},{t0+1.3:.3f});')
    f.title(['Redação corrigida:','480 de 1000.'] if f.lang=='pt' else ['Essay graded:','480 out of 1000.'], t0, 2.0, acc=('480',))
    f.fx('ding-correct',t0+1.0,0.6); f.fx('error-blip',t0+1.15,0.55); f.fx('whoosh-short',t0+0.05,0.35)
def hook_B(f, t0):
    f.photo('assets/gen/m/student-frustrated-2.png',t0,2.0,1.06,1.16,0.35)
    f.title(['Errei e não sei','por quê.'], t0+0.1, 1.9, y=f.TY+40, size=int(f.TS*1.15))
    f.fx('whoosh-short',t0+0.05,0.35); f.fx('error-blip',t0+0.6,0.5)
def hook_C(f, t0):
    n=(ENEM_DATE-TODAY).days
    f.bg(t0,2.0,'navy')
    f.els.append(f'<div id="cd" class="num clip" data-start="{t0}" data-duration="2.0" style="left:0;width:{f.W}px;top:{f.TY+150}px;text-align:center;font-size:{int(f.TS*3.6)}px"><span class="v">0</span></div>')
    f.js.append(f'{{ const el=document.querySelector("#cd .v"); const st={{v:0}}; tl.fromTo(st,{{v:{n+30}}},{{v:{n},duration:0.9,ease:"power3.out",onUpdate:()=>{{el.textContent=String(Math.round(st.v));}}}},{t0+0.1:.3f}); }}')
    f.title(['Faltam'] , t0, 2.0, y=f.TY+40)
    f.title(['dias para o ENEM.','Você sabe o que está errando?'], t0+0.5, 1.5, y=f.TY+150+int(f.TS*3.6)+30, size=int(f.TS*0.72), acc=('errando?',))
    f.fx('click-soft',t0+0.1,0.4); f.fx('click-soft',t0+0.4,0.4); f.fx('click-soft',t0+0.7,0.4); f.fx('impact-bass-2',t0+1.0,0.5)

def dor(f, t0):   # 4.5 s: three statements, photos then brand field
    L=f.lang=='pt'
    f.photo('assets/gen/m/desk-night-1.png',t0,1.5,1.05,1.12,0.4)
    f.title(['Faz simulado e não sabe','por que errou.'] if L else ['You take practice tests','and never know why.'], t0, 1.5, y=f.TY+120, acc=('errou.',) if L else ('why.',))
    f.photo('assets/gen/m/student-frustrated-1.png',t0+1.5,1.5,1.12,1.04,0.35)
    f.title(['Lê a teoria,','mas na prova trava.'] if L else ['You read the theory,','then freeze on test day.'], t0+1.5, 1.5, y=f.TY+120, acc=('trava.',) if L else ('freeze',))
    f.bg(t0+3.0,1.5,'navy')
    f.title(['O problema não é estudar.','É estudar sem feedback.'] if L else ["The problem isn't studying.","It's studying without feedback."], t0+3.0, 1.5, y=f.TY+160, acc=('sem','feedback.') if L else ('without','feedback.'))
    for k in (0,1.5,3.0): f.fx('whoosh-short',t0+k,0.4)

def demo(f, t0, fast=False, clip='estudo', resfy=1150):
    """Modo Estudo on the phone. fast=False: 10.5 s (6.5→17). fast=True: 8 s (15 s cut)."""
    E=M[clip]; src=f'assets/app/m3/{clip}.mp4'; L=f.lang=='pt'
    if not fast:
        q, ty, tap, res, ev, end = t0, t0+1.5, t0+5.5, t0+6.5, t0+8.0, t0+10.5
    else:
        q, ty, tap, res, ev, end = t0, t0+1.0, t0+3.5, t0+4.0, t0+5.5, t0+8.0
    f.bg(t0,end-t0,'navy')
    # a) question
    f.phone(src, q, ty-q, E['question']+0.2, 1.0, cams=[(0,1.35,645,520,0,'none'),(ty-q,1.42,645,560,ty-q,'none')])
    f.title(['Pergunta de História.'] if L else ['A question in English.'], q, ty-q, size=int(f.TS*0.9))
    # b) typing (ends exactly at typing-end), timer running
    tyd=tap-ty; rate=1.6 if not fast else 2.2
    f.phone(src, ty, tyd, E['typing-end']-tyd*rate, rate, cams=[(0,1.28,645,1500,0,'none'),(tyd,1.34,645,1560,tyd,'none')])
    f.title(['Você responde.','O cronômetro corre.'] if L else ['You answer.','The clock is running.'], ty, tyd, size=int(f.TS*0.9))
    for k in range(int(tyd/1.5)+1): f.fx('typing', ty+k*1.5, 0.45)
    # c) tap → "Avaliando…" (music goes silent for 0.5 s before the grade)
    f.phone(src, tap, res-tap, E['tap-send']-0.25, 1.0, cams=[(0,1.45,645,2330,0,'none')])
    f.fx('send-tap', tap+0.25, 0.7)
    # d) result: the cut reveals the real 4/10 (scrolled into view in the recording)
    f.phone(src, res, ev-res, E['scroll-2']+1.95, 1.0, cams=[(0,1.9,880,resfy,0,'none'),(ev-res,2.0,900,resfy+20,ev-res,'none')])
    f.title(['Nota na hora.'] if L else ['Graded instantly.'], res, ev-res, size=int(f.TS*0.9), acc=('hora.',) if L else ('instantly.',))
    f.fx('ding-correct', res, 0.8); f.fx('impact-bass-2', res, 0.55); f.fx('sparkle', res+0.1, 0.4)
    # e) evaluation text + green/red chips built from the real AI comment
    f.phone(src, ev, end-ev, E['scroll-2']+1.95+(ev-res), 1.0, cams=[(0,1.3,645,1900,0,'none'),(end-ev,1.34,645,1950,end-ev,'none')])
    f.title(['O que acertou. O que faltou.'] if L else ['What was right. What was missing.'], ev, end-ev, size=int(f.TS*0.78))
    # the AI's real comment, large enough to read on a phone; the colours tell the story
    q=f.uid('q')
    if L:
        qh='Acertou <b class="g">o núcleo da proporcionalidade</b> (punição igual ao crime), mas cometeu <b class="r">dois erros</b>: chamou o talião de <b class="r">"justiça de vingança"</b> e disse que as leis valiam <b class="r">"para todo mundo"</b>.'
        lab='Avaliação da IA · resposta real'
    else:
        qh='<b class="g">Correctly identifies the core distinction</b>: will for opinion, going to for evidence. However, the explanation <b class="r">lacks precision</b>: it says <b class="r">"more certain"</b> instead of <b class="r">"present evidence"</b>.'
        lab='Real AI feedback'
    if f.H==1920: qx,qy,qw,qs=60,520,960,40
    elif f.W==1920: qx,qy,qw,qs=120,470,1040,36
    else: qx,qy,qw,qs=40,470,540,30
    f.els.append(f'<div id="{q}" class="quote clip" data-start="{ev+0.25:.2f}" data-duration="{end-ev-0.25:.2f}" style="left:{qx}px;top:{qy}px;width:{qw}px;font-size:{qs}px"><div class="lab">{lab}</div>{qh}</div>')
    f.js.append(f'tl.fromTo("#{q}",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.4,ease:"power3.out",transformOrigin:"50% 50%"}},{ev+0.25:.3f});')
    f.js.append(f'tl.set("#{q} b", {{ color: "#e6ebf5", textDecorationColor: "transparent" }}, {ev+0.25:.3f}); const bs=document.querySelectorAll("#{q} b"); bs.forEach((b,i)=>{{ tl.to(b, {{ color: b.classList.contains("g") ? "#4ade80" : "#f87171", duration: 0.25, ease: "power2.out" }}, {ev+0.9:.3f}+i*0.45); }});')
    for i,k in enumerate(['ok','miss','miss','miss']): f.fx('ding-correct' if k=='ok' else 'error-blip', ev+0.9+i*0.45, 0.5)
    return end

def montage(f, t0, per=1.5, items=None):
    L=f.lang=='pt'; R=M['redacao']; Sm=M['simulados']; Fl=M['flashcards']; Mn=M['mentor']
    items=items or [
        ('assets/app/m3/redacao.mp4', RED_RESULT+1.2, 1.0, (1.18,645,1500), (1.22,645,1700), ['Redação'] if L else ['Essays'], 'Nota de 0 a 1000' if L else 'Scored 0 to 1000'),
        ('assets/app/m3/simulados.mp4', Sm['exam']+0.3, 1.0, (1.15,645,900), (1.2,645,1050), ['Simulados'] if L else ['Practice tests'], 'Formato de cada banca' if L else 'Official exam format'),
        ('assets/app/m3/flashcards.mp4', Fl['flip']-0.6, 1.0, (1.18,645,1250), (1.22,645,1300), ['Flashcards'], 'Revisão espaçada' if L else 'Spaced repetition'),
        ('assets/app/m3/mentor.mp4', Mn['send']+0.2, 1.0, (1.18,645,900), (1.22,645,1150), ['Mentor IA'] if L else ['AI Mentor'], 'Tira suas dúvidas' if L else 'Answers your questions'),
    ]
    f.bg(t0, per*len(items), 'navy')
    for i,(src,ms,rate,c0,c1,ttl,sb) in enumerate(items):
        a=t0+i*per
        f.phone(src, a, per, ms, rate, cams=[(0,)+c0+(0,'none'),(per,)+c1+(per,'none')])
        f.title(ttl, a, per, size=int(f.TS*1.25), cls='')
        f.sub(sb, a, per, f.TY+int(f.TS*1.25)*len(ttl)+26)
        f.fx('whoosh-short', a, 0.4)
    return t0+per*len(items)

def steps_block(f, t0, d=8.0):
    L=f.lang=='pt'; G=M['signup']
    f.bg(t0,d,'navy')
    f.phone('assets/app/m3/signup.mp4', t0, d, G['form']+0.2, 1.0, cams=[(0,1.15,645,1000,0,'none'),(d,1.2,645,1100,d,'none')])
    f.title(['Em 3 passos:'] if L else ['3 steps:'], t0, d, size=int(f.TS*0.95))
    st=[('Crie a conta grátis' if L else 'Create your free account'),('Escolha a prova e a matéria' if L else 'Pick your exam and subject'),('Responda e receba a correção' if L else 'Answer and get graded')]
    x=f.TX; y0=f.TY+int(f.TS*0.95)+40
    for i,tx in enumerate(st):
        at=t0+0.6+i*2.2; sid=f.uid('st')
        f.els.append(f'<div id="{sid}" class="step clip" data-start="{at:.2f}" data-duration="{t0+d-at:.2f}" style="left:{x}px;top:{y0+i*110}px"><div class="n">{i+1}</div><div class="tx">{tx}</div></div>')
        f.js.append(f'tl.fromTo("#{sid}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},{at:.3f});')
        f.fx('ping', at, 0.45)
    return t0+d

def badges_block(f, t0, d=5.0):
    L=f.lang=='pt'
    f.bg(t0,d,'navy')
    f.title(['As provas que decidem sua vaga.'] if L else ['The exams that matter.'], t0, d, size=int(f.TS*0.9))
    names=['ENEM','FUVEST','UNICAMP','PAES','SAT']
    if f.W==1080 and f.H==1920:
        bw,bh=440,150; cols=2; x0=100; y0=f.TY+int(f.TS*0.9)*2+60; gap=40
    elif f.W==1920: bw,bh=300,120; cols=5; x0=120; y0=f.TY+200; gap=30
    else: bw,bh=300,110; cols=3; x0=50; y0=f.TY+180; gap=24
    for i,nm in enumerate(names):
        c,r=i%cols,i//cols; at=t0+0.3+i*0.5; bid=f.uid('bd')
        x=x0+c*(bw+gap); y=y0+r*(bh+gap)
        if cols==2 and i==4: x=x0+(bw+gap)//2
        f.els.append(f'<div id="{bid}" class="badge clip" data-start="{at:.2f}" data-duration="{t0+d-at:.2f}" style="left:{x}px;top:{y}px;width:{bw}px;height:{bh}px;font-size:{int(bh*0.38)}px">{nm}</div>')
        f.js.append(f'tl.fromTo("#{bid}",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(1.8)"}},{at:.3f});')
        f.fx('pop', at, 0.45)
    return t0+d

def offer(f, t0, d_lines=3.0, d_close=4.0):
    L=f.lang=='pt'; G=M['signup']
    f.bg(t0,d_lines,'navy')
    f.phone('assets/app/m3/signup.mp4', t0, d_lines, G['form']+0.4, 1.0, cams=[(0,1.2,645,950,0,'none'),(d_lines,1.26,645,1000,d_lines,'none')])
    lines=[('Grátis para sempre.' if L else 'Free forever.'),('3 dias de Pro ao criar sua conta.' if L else '3 days of Pro when you sign up.'),('Sem cartão.' if L else 'No card needed.')]
    step=d_lines/3.0
    for i,tx in enumerate(lines):
        at=t0+i*step; f.title([tx], at, step, y=f.TY, size=int(f.TS*0.95))
        f.fx('pop', at, 0.5)
    # close: brand, url big and fixed, button
    c=t0+d_lines; f.bg(c,d_close,'blue')
    ly=(f.H//2-330) if f.H==1920 else (f.TY-120 if f.W==1920 else f.TY-40)
    lg=f.uid('lg'); f.els.append(f'<div id="{lg}" class="clip" data-start="{c:.2f}" data-duration="{d_close}" style="position:absolute;inset:0;z-index:6">{logo_html(f, int(f.TS*1.5), ly, inv=True)}</div>')
    uy=ly+int(f.TS*1.5)+70
    f.els.append(f'<div class="url clip" data-start="{c:.2f}" data-duration="{d_close}" style="top:{uy}px;font-size:{int(f.TS*1.1)}px">iveststudy.com</div>')
    f.els.append(f'<div class="btn clip" data-start="{c+0.4:.2f}" data-duration="{d_close-0.4:.2f}" style="top:{uy+int(f.TS*1.1)+60}px;font-size:{int(f.TS*0.6)}px;background:#fff;color:#1d4ed8;box-shadow:0 20px 60px rgba(0,0,0,.25)">{"Criar conta grátis →" if L else "Create free account →"}</div>')
    f.els.append(f'<div class="subt clip" data-start="{c+0.6:.2f}" data-duration="{d_close-0.6:.2f}" style="left:0;width:{f.W}px;top:{uy+int(f.TS*1.1)+60+int(f.TS*0.6)+90}px;text-align:center;font-size:{f.SUBS}px;color:#e0ecff">{"Grátis para sempre · 3 dias de Pro · Sem cartão" if L else "Free forever · 3 days of Pro · No card"}</div>')
    f.js.append(f'tl.fromTo("#{lg} .logo",{{scale:2.2,opacity:0,filter:"blur(14px)"}},{{scale:1,opacity:1,filter:"blur(0px)",duration:0.3,ease:"power4.out",transformOrigin:"50% 50%",immediateRender:false}},{c+0.02:.3f});')
    f.js.append(f'tl.fromTo(".url",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35,ease:"power3.out",immediateRender:false}},{c+0.15:.3f});')
    f.js.append(f'tl.fromTo(".btn",{{opacity:0,y:30,scale:0.94}},{{opacity:1,y:0,scale:1,duration:0.4,ease:"power4.out",immediateRender:false}},{c+0.4:.3f}); tl.to(".btn",{{scale:0.96,duration:0.08,yoyo:true,repeat:1}},{c+1.3:.3f});')
    f.fx('impact-bass-1', c, 0.7); f.fx('whoosh-cinematic', c-0.3, 0.35); f.fx('sonic-logo', c+d_close-1.6, 0.8)
    return c+d_close

def score(f, total, hit_at, close_at, music_src='assets/audio/music30.mp3'):
    """t2.mp3 (120 bpm): hit at 13.06. Place the hit on `hit_at`; the track fades after 24 s, so a second instance (bars 16→22) carries the ending."""
    HIT=13.06; off=HIT-hit_at   # media time at film 0
    seg1_end=min(total, 23.5-off)
    auto={"version":1,"lanes":[{"target":"volume","points":[{"t":0,"v":1},{"t":round(hit_at-0.52,2),"v":1},{"t":round(hit_at-0.5,2),"v":0},{"t":round(hit_at-0.02,2),"v":0},{"t":hit_at,"v":1},{"t":round(seg1_end,2),"v":1}]}]}
    if off>=0:
        f.music(music_src, 0, seg1_end, off, 0.42, 0.0, 0.35, auto)
    else:
        f.music(music_src, -off, seg1_end+off, 0, 0.42, 0.0, 0.35, auto)
    t=seg1_end
    while t<total-0.2:
        d=min(6.0,total-t); f.music(music_src, t, d, 16.0, 0.42, 0.3, 0.6 if t+d>=total-0.2 else 0.0); t+=d

# ─────────────────────────────────────────── films
def film30(variant='A', W=1080, H=1920, lang='pt'):
    f=Film(f'ad30{variant.lower()}' if (W,H)==(1080,1920) else f'ad30{variant.lower()}-{W}x{H}', W, H, lang)
    {'A':hook_A,'B':hook_B,'C':hook_C}[variant](f,0)
    dor(f,2.0); demo(f,6.5); montage(f,17.0); offer(f,23.0,3.0,4.0)
    f.watermark(6.5, 16.5)
    f.vo('pt1',0.3); f.vo('pt2',6.6); f.vo('pt3',13.1); f.vo('pt4',17.0); f.vo('pt5',22.55); f.vo('pt6',26.6)
    score(f,30.0,13.0,26.0); f.build(30.0)
def film15():
    f=Film('ad15',1080,1920); hook_A(f,0); demo(f,2.0,fast=True); offer(f,10.0,2.0,3.0)
    f.watermark(2.0,8.0); f.vo('pt2',2.1); f.vo('pt3',6.1); f.vo('pt9',10.3)
    score(f,15.0,6.0,12.0); f.build(15.0)
def film6():
    f=Film('ad06',1080,1920); E=M['estudo']
    f.bg(0,2.6,'navy'); f.phone('assets/app/m3/estudo.mp4',0,2.6,E['scroll-2']+1.95,1.0,cams=[(0,1.9,880,1150,0,'none'),(2.6,2.0,900,1170,2.6,'none')])
    f.title(['Correção por IA','em cada resposta.'],0.1,2.5,acc=('IA',)); f.fx('ding-correct',0.6,0.8); f.fx('impact-bass-2',0.6,0.5)
    c=2.6; f.bg(c,3.4,'blue'); lg=f.uid('lg')
    f.els.append(f'<div id="{lg}" class="clip" data-start="{c}" data-duration="3.4" style="position:absolute;inset:0;z-index:6">{logo_html(f,int(f.TS*1.5),f.TY+40,inv=True)}</div>')
    f.els.append(f'<div class="url clip" data-start="{c}" data-duration="3.4" style="top:{f.TY+40+int(f.TS*1.5)+70}px;font-size:{int(f.TS*1.1)}px">iveststudy.com</div>')
    f.title(['Grátis.'],c+0.3,3.1,y=f.TY+40+int(f.TS*1.5)+70+int(f.TS*1.1)+50,size=int(f.TS*1.1))
    f.js.append(f'tl.fromTo("#{lg} .logo",{{scale:2.2,opacity:0,filter:"blur(14px)"}},{{scale:1,opacity:1,filter:"blur(0px)",duration:0.3,ease:"power4.out",transformOrigin:"50% 50%",immediateRender:false}},{c+0.02});')
    f.js.append(f'tl.fromTo(".url",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35,ease:"power3.out",immediateRender:false}},{c+0.15});')
    f.fx('impact-bass-1',c,0.7); f.fx('sonic-logo',4.4,0.8); f.vo('pt9',0.2)
    f.music('assets/audio/music30.mp3',0,6.0,16.0,0.4,0.0,0.8); f.build(6.0)
def film45(W,H):
    f=Film(f'ad45-{W}x{H}',W,H); hook_A(f,0); dor(f,2.0); demo(f,6.5); montage(f,17.0); steps_block(f,23.0,8.0); badges_block(f,31.0,5.0); offer(f,36.0,3.0,6.0)
    f.watermark(6.5,29.5)
    f.vo('pt1',0.3); f.vo('pt2',6.6); f.vo('pt3',13.1); f.vo('pt4',17.0); f.vo('pt7',23.2); f.vo('pt8',31.1); f.vo('pt5',36.0); f.vo('pt6',40.3)
    score(f,45.0,13.0,39.0); f.build(45.0)

def film_sat():
    f=Film('ad-sat-en',1080,1920,'en'); X=M['en-simulados']
    f.bg(0,2.0,'navy'); f.phone('assets/app/m3/en-simulados.mp4',0,2.0,X['exam']+0.4,1.0,cams=[(0,1.35,645,700,0,'none'),(2.0,1.42,645,760,2.0,'none')])
    f.title(['SAT practice,','graded by AI.'],0,2.0,acc=('AI.',)); f.fx('whoosh-short',0.05,0.35); f.fx('ding-correct',0.9,0.5)
    dor(f,2.0); demo(f,6.5,clip='en-estudo',resfy=950)
    items=[('assets/app/m3/en-simulados.mp4', X['sat-card']+0.2, 1.0, (1.18,645,1300), (1.24,645,1400), ['SAT mock exams'], 'Official format, timed'),
           ('assets/app/m3/en-home.mp4', 1.4, 1.0, (1.15,645,700), (1.2,645,900), ['3 languages'], 'English · Portuguese · Spanish'),
           ('assets/app/m3/en-estudo.mp4', M['en-estudo']['scroll-2']+2.2, 1.0, (1.3,645,1900), (1.34,645,2000), ['AI feedback'], 'On every answer')]
    montage(f,17.0,2.0,items); offer(f,23.0,3.0,5.0)
    f.watermark(6.5,16.5); f.vo('en1',0.3); f.vo('en2',6.6); f.vo('en3',13.1); f.vo('en4',17.0); f.vo('en6',26.4)
    score(f,31.0,13.0,26.0); f.build(31.0)

if __name__=='__main__':
    which=sys.argv[1:] or ['30a']
    for w in which:
        if w=='30a': film30('A')
        elif w=='30b': film30('B')
        elif w=='30c': film30('C')
        elif w=='15': film15()
        elif w=='6': film6()
        elif w=='45w': film45(1920,1080)
        elif w=='45s': film45(1080,1080)
        elif w=='sat': film_sat()
