# iVest Study · "rastro de luz" — one neon comet travels through the product and lights each part.
# Usage: python3 -I tools/style.py 1920x1080 1080x1920   → builds/trail-WxH.html
import json, os, sys, math, re, subprocess
P=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(P)
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
ICON={n:re.sub(r'\s(width|height|class)="[^"]*"','',open(f'assets/brand/icons/{n}.svg',encoding='utf-8').read()) for n in ['brand','estudo','quiz','flashcards','simulados','redacao','mentor']}
BEAT=0.4915; LOOP=8*BEAT  # music-trail.mp3: 8-beat drop at media 7.91–11.84
M0=1.2                     # film time of the first impact
B=[round(M0+i*LOOP,2) for i in range(4)]   # 1.2, 5.13, 9.06, 12.99 — every loop starts on the drop hit
T=16.0
RISER_MS=1.75   # riser.mp3 climbs from -32 dB at 1.7 s to its peak at 2.9 s
BLUE='#3b82f6'; LIGHT='#93c5fd'; CORE='#eff6ff'

def build(W,H):
    V=H>W; cx=W/2; cy=H/2 if not V else 900
    els=[]; js=[]; trails=[]; heads=[]; sfx=[]; n=[0]
    def uid(p): n[0]+=1; return f'{p}{n[0]}'
    def fx(name,at,vol=0.5,ms=0.0,d=None): sfx.append((name,round(at,3),vol,ms,d))
    # ── light trail: three strokes (glow, body, core) + a comet head
    def trail(d, at, du, tail=0, ease='power1.inOut', persist_to=None, width=1.0, color=BLUE, head=True):
        g=uid('tr'); hid=g+'h' if head else None
        trails.append(f'<g id="{g}" class="trail" style="opacity:0"><path d="{d}" stroke="{color}" stroke-width="{26*width:.1f}" filter="url(#glowB)" opacity=".55"/><path d="{d}" stroke="{LIGHT}" stroke-width="{9*width:.1f}" filter="url(#glowA)"/><path d="{d}" stroke="{CORE}" stroke-width="{3.2*width:.1f}"/></g>')
        if head: heads.append(f'<div id="{hid}" class="head" style="opacity:0"></div>')
        js.append(f'trail("{g}", {at:.3f}, {du:.3f}, {tail}, "{ease}", {json.dumps(hid)}, {persist_to if persist_to is not None else "null"});')
        return g
    def at_clip(id,start,d,html,style='',cls=''):
        els.append(f'<div id="{id}" class="clip {cls}" data-start="{start:.2f}" data-duration="{d:.2f}" style="{style}">{html}</div>')
    def glowpulse(sel,at,col=BLUE,big=1.0):
        js.append(f'tl.fromTo("{sel}",{{boxShadow:"0 0 0px rgba(59,130,246,0)"}},{{boxShadow:"0 0 {int(70*big)}px {col}",duration:0.18,ease:"power3.out",immediateRender:false}},{at:.3f}); tl.to("{sel}",{{boxShadow:"0 0 {int(26*big)}px {col}55",duration:0.7,ease:"power2.out"}},{at+0.18:.3f});')
    k=1.0 if not V else 1.0
    # ═══ 1 · LOGO written by light (0 → 1.95)
    lw=980; lx=cx-lw/2; ly=cy-90
    logo=f'<div class="logo" style="left:{lx:.0f}px;top:{ly:.0f}px;width:{lw}px;font-size:{150 if not V else 132}px"><span class="cap">{ICON["brand"]}</span><span><span class="i">i</span>Vest <span class="st">Study</span></span></div>'
    at_clip('s1',0,1.95,logo+'<div id="s1flash" class="flash"></div>')
    p1=(f'M {-120} {H*0.86:.0f} C {cx-700:.0f} {H*0.86:.0f}, {cx-760:.0f} {ly+215:.0f}, {cx-470:.0f} {ly+205:.0f}' if not V else f'M {cx-260:.0f} {ly+620:.0f} C {cx-620:.0f} {ly+560:.0f}, {cx-640:.0f} {ly+225:.0f}, {cx-470:.0f} {ly+205:.0f}')+f' L {cx+470:.0f} {ly+205:.0f} C {cx+640:.0f} {ly+200:.0f}, {cx+700:.0f} {ly+120:.0f}, {cx+720:.0f} {ly-40:.0f}'
    trail(p1,0.05,1.1,0,'power2.inOut',persist_to=1.75)
    js.append(f'tl.fromTo("#s1 .logo",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.62,ease:"none"}},0.42);')
    js.append(f'tl.fromTo("#s1 .logo",{{scale:1}},{{scale:1.06,duration:0.12,ease:"power3.out",yoyo:true,repeat:1,transformOrigin:"50% 50%"}},{M0:.3f}); tl.fromTo("#s1flash",{{opacity:0}},{{opacity:0.9,duration:0.08}},{M0:.3f}); tl.to("#s1flash",{{opacity:0,duration:0.5}},{M0+0.08:.3f});')
    js.append(f'tl.to("#s1 .logo",{{scale:0.55,opacity:0,filter:"blur(14px)",duration:0.4,ease:"power3.in",transformOrigin:"50% 50%"}},1.55);')
    fx('riser',0.0,0.6,RISER_MS,1.2); fx('whoosh-cinematic',0.05,0.4); fx('impact-bass-2',M0,0.9); fx('sparkle',M0+0.05,0.5)
    # ═══ 2 · answer chips the comet bounces through (1.6 → 2.45), receding in depth
    chips=['A','B','C','D']; cp=[]
    for i,c in enumerate(chips):
        sc=1.0-0.17*i; x=cx-460+i*300 if not V else cx-270+i*180; y=cy+170-i*120 if not V else cy+330-i*190
        cid=f'chip{i}'; cp.append((x,y,sc))
        at_clip(cid,1.55,1.0,f'<div class="chip" data-layout-ignore style="transform:scale({sc:.2f})">{c}</div>',f'position:absolute;left:{x-60:.0f}px;top:{y-60:.0f}px;width:120px;height:120px;filter:blur({i*1.2:.1f}px)')
    pts=' '.join(f'L {x:.0f} {y:.0f}' for x,y,_ in cp)
    p2=f'M {cx+720:.0f} {ly-40:.0f} C {cx+400:.0f} {cy+420:.0f}, {cp[0][0]-200:.0f} {cp[0][1]+160:.0f}, {cp[0][0]:.0f} {cp[0][1]:.0f} ' + ' '.join(f'Q {(cp[i][0]+cp[i+1][0])/2:.0f} {min(cp[i][1],cp[i+1][1])-130:.0f} {cp[i+1][0]:.0f} {cp[i+1][1]:.0f}' for i in range(3)) + f' L {cx:.0f} {cy-60:.0f}'
    trail(p2,1.55,0.95,420,'power1.in')
    for i in range(4):
        t=1.55+0.95*(0.42+0.15*i)
        js.append(f'tl.fromTo("#chip{i} .chip",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.25,ease:"power3.out",immediateRender:false}},{1.55+0.05*i:.3f}); tl.to("#chip{i} .chip",{{backgroundColor:"#2563eb",borderColor:"#bfdbfe",color:"#fff",boxShadow:"0 0 50px #3b82f6",duration:0.12}},{t:.3f}); tl.to("#chip{i}",{{opacity:0,scale:1.3,duration:0.25}},{t+0.25:.3f});')
        fx('pop',t,0.4)
    # ═══ 3 · phone: Modo Estudo, real flow (2.2 → B1+0.05)
    pw,ph=(540,960) if not V else (600,1120); px=cx-pw/2; py=cy-ph/2
    ph_html=f'''<div class="phone" style="width:{pw}px;height:{ph}px">
      <div class="isl"></div>
      <div class="pscroll"><div class="pbar"><span class="pb-ic">{ICON["estudo"]}</span><span>Modo Estudo</span><span class="pb-r">História</span></div>
      <div class="prog"><i></i></div>
      <div class="q">O que o princípio “olho por olho, dente por dente” revela sobre a justiça babilônica?</div>
      <div class="timer"><span class="tl">CRONÔMETRO</span><span id="tm" class="tv">1:00</span></div>
      <div class="ans"><span id="ty"></span><span class="caret"></span></div>
      <div id="pbtn" class="pbtn">Avaliar resposta →</div>
      <div id="pres" class="pres"><div class="score"><b id="sc">4</b><span>/10</span></div>
        <div id="fb1" class="fb ok"><i>✓</i>Proporcionalidade: acertou</div>
        <div id="fb2" class="fb miss"><i>✗</i>Leis iguais para todos: errou</div></div></div>
    </div>'''
    at_clip('s3',2.2,B[1]+0.1-2.2,ph_html,f'position:absolute;left:{px:.0f}px;top:{py:.0f}px;width:{pw}px;height:{ph}px;perspective:1600px')
    r=56; x0,y0,x1,y1=px-14,py-14,px+pw+14,py+ph+14
    p3=f'M {cx:.0f} {cy-60:.0f} C {cx-160:.0f} {y0-140:.0f}, {x0+60:.0f} {y0-40:.0f}, {x0+r:.0f} {y0:.0f} L {x1-r:.0f} {y0:.0f} Q {x1:.0f} {y0:.0f} {x1:.0f} {y0+r:.0f} L {x1:.0f} {y1-r:.0f} Q {x1:.0f} {y1:.0f} {x1-r:.0f} {y1:.0f} L {x0+r:.0f} {y1:.0f} Q {x0:.0f} {y1:.0f} {x0:.0f} {y1-r:.0f} L {x0:.0f} {y0+r:.0f} Q {x0:.0f} {y0:.0f} {x0+r:.0f} {y0:.0f}'
    trail(p3,2.3,0.9,0,'power2.inOut',persist_to=B[1]-0.2,width=0.7)
    js.append(f'tl.fromTo("#s3 .phone",{{rotationY:-38,rotationX:16,scale:0.78,opacity:0,filter:"blur(10px)"}},{{rotationY:-10,rotationX:5,scale:0.96,opacity:1,filter:"blur(0px)",duration:0.6,ease:"power3.out",immediateRender:false}},2.2); tl.to("#s3 .phone",{{rotationY:8,rotationX:2,duration:{B[1]-0.3-2.8:.2f},ease:"none"}},2.8);')
    ans='A punição tinha que ser igual ao crime. E as leis valiam para todo mundo.'
    js.append(f'typeTo("#ty", {json.dumps(ans)}, 2.75, 0.85);')
    js.append(f'countDown("#tm", 60, 45, 2.4, {B[1]-2.4:.2f});')
    tap=3.72; js.append(f'tl.to("#pbtn",{{scale:0.94,backgroundColor:"#1d4ed8",duration:0.08,yoyo:true,repeat:1}},{tap:.3f}); tl.set("#pbtn",{{textContent:"Avaliando…"}},{tap+0.05:.3f}); ')
    res=4.0
    js.append(f'tl.to("#s3 .pscroll",{{y:{-330 if not V else -250},duration:0.4,ease:"power3.inOut"}},{res-0.2:.3f}); tl.set("#pbtn",{{display:"none"}},{res-0.2:.3f});')
    js.append(f'tl.fromTo("#pres",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3,ease:"power3.out",immediateRender:false}},{res:.3f}); tl.fromTo("#pres .score",{{scale:1.6}},{{scale:1,duration:0.35,ease:"back.out(2.2)",transformOrigin:"0% 50%",immediateRender:false}},{res:.3f});')
    js.append(f'tl.fromTo("#fb1",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.25,immediateRender:false}},{res+0.18:.3f}); tl.fromTo("#fb2",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.25,immediateRender:false}},{res+0.36:.3f});')
    js.append(f'tl.to("#s3 .phone",{{rotationY:42,rotationX:-6,scale:0.78,opacity:0,filter:"blur(12px)",duration:0.35,ease:"power3.in"}},{B[1]-0.3:.3f});')
    # tap comet into the button
    bx=cx; byy=py+ph*0.70
    trail(f'M {x1:.0f} {y0+200:.0f} C {x1+180:.0f} {byy-200:.0f}, {bx+260:.0f} {byy+40:.0f}, {bx:.0f} {byy:.0f}',tap-0.35,0.35,220,'power2.in',width=0.6)
    fx('whoosh-short',2.25,0.4); fx('typing',2.75,0.5,0,0.9); fx('send-tap',tap,0.7); fx('ding-correct',res,0.75); fx('ding-correct',res+0.18,0.4); fx('error-blip',res+0.36,0.55)
    # ═══ 4 · essay gauge 0 → 920, competencies light (B1 → 7.05)
    gr=255 if not V else 270; gcx,gcy=cx,(cy-60 if not V else cy-120)
    circ=f'M {gcx:.1f} {gcy-gr:.1f} A {gr} {gr} 0 1 1 {gcx-0.01:.2f} {gcy-gr:.1f}'
    a=2*math.pi*0.92; ex=gcx+gr*math.sin(a); ey=gcy-gr*math.cos(a)
    arc=f'M {gcx:.1f} {gcy-gr:.1f} A {gr} {gr} 0 1 1 {ex:.1f} {ey:.1f}'
    comps=[('C1',200),('C2',200),('C3',160),('C4',200),('C5',160)]
    pill_w=150 if not V else 170; gap=20; pw5=5*pill_w+4*gap; pyy=gcy+gr+(46 if not V else 80)
    pills=''.join(f'<div id="cp{i}" class="pill" style="left:{gcx-pw5/2+i*(pill_w+gap)-gcx+W/2:.0f}px;top:{pyy:.0f}px;width:{pill_w}px"><b>{c}</b><span>{v}</span></div>' for i,(c,v) in enumerate(comps))
    g_html=f'''<svg class="ring" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><path d="{circ}" stroke="rgba(148,163,184,.16)" stroke-width="22" fill="none"/></svg>
      <div class="eyb" style="left:0;width:{W}px;top:{gcy-gr-(70 if not V else 100):.0f}px">{ICON["redacao"]}<span>REDAÇÃO</span></div>
      <div class="gnum" style="left:0;width:{W}px;top:{gcy-95:.0f}px"><b id="gv">0</b><span>/1000</span></div>
      <div class="glab" style="left:0;width:{W}px;top:{gcy+95:.0f}px">nota por competência</div>
      {pills}'''
    at_clip('s4',B[1],7.1-B[1],g_html,'position:absolute;left:0;top:0;width:100%;height:100%')
    trail(arc,B[1],1.05,0,'power2.out',persist_to=6.85,width=1.2)
    js.append(f'countUp("#gv", 0, 920, {B[1]:.3f}, 1.05);')
    for i in range(5):
        t=B[1]+0.35+i*0.2; js.append(f'tl.fromTo("#cp{i}",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.22,ease:"back.out(2)",immediateRender:false}},{t:.3f}); tl.to("#cp{i}",{{borderColor:"#22c55e",color:"#bbf7d0",boxShadow:"0 0 30px rgba(34,197,94,.55)",duration:0.15}},{t+0.1:.3f});'); fx('click-soft',t,0.45)
    js.append(f'/*gnum*/tl.fromTo("#s4 .gnum",{{scale:0.8,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2)",transformOrigin:"50% 50%",immediateRender:false}},{B[1]:.3f}); tl.fromTo("#s4 .eyb, #s4 .glab",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.3,immediateRender:false}},{B[1]+0.1:.3f});')
    # burst
    for i in range(14):
        ang=i/14*2*math.pi; sid=f'sp{i}'; els.append(f'<div id="{sid}" class="spark clip" data-start="6.6" data-duration="0.6" style="left:{gcx-6:.0f}px;top:{gcy-6:.0f}px"></div>')
        js.append(f'tl.fromTo("#{sid}",{{x:{gr*math.cos(ang)*0.95:.0f},y:{gr*math.sin(ang)*0.95:.0f},opacity:1,scale:1}},{{x:{gr*math.cos(ang)*1.9:.0f},y:{gr*math.sin(ang)*1.9:.0f},opacity:0,scale:0.3,duration:0.5,ease:"power3.out",immediateRender:false}},6.62);')
    js.append('tl.to("#s4 > *",{opacity:0,filter:"blur(10px)",scale:1.1,duration:0.35,ease:"power3.in",transformOrigin:"50% 50%"},6.7);')
    fx('impact-bass-2',B[1],0.8); fx('whoosh-short',6.6,0.4); fx('sparkle',6.62,0.5)
    # ═══ 5 · ranks Bronze → Elite (7.05 → B2)
    ranks=[('Bronze','#d97706'),('Prata','#94a3b8'),('Ouro','#f59e0b'),('Platina','#14b8a6'),('Diamante','#38bdf8'),('Mestre','#a855f7'),('Elite','#ef4444')]
    cw,chh=(1400,520) if not V else (1000,760); rx,ryy=cx-cw/2,cy-chh/2
    bw=128 if not V else 150
    slots=[]
    if not V:
        bg_=(cw-140-7*bw)/6; slots=[(70+i*(bw+bg_), chh-260) for i in range(7)]
    else:
        g4=(cw-140-4*bw)/3; slots=[(70+i*(bw+g4), 250) for i in range(4)]+[(70+(bw+g4)/2+i*(bw+g4), 500) for i in range(3)]
    badges=''
    for i,(nm,col) in enumerate(ranks):
        bxx,byy_=slots[i]; badges+=f'<div id="rk{i}" class="rk" style="left:{bxx:.0f}px;top:{byy_:.0f}px;width:{bw}px;--c:{col}"><div class="hex"></div><span>{nm}</span></div>'
    r_html=f'<div class="card rcard" style="width:{cw}px;height:{chh}px"><div class="ct">Progressão de Ranks</div><div class="cs">Suba de Bronze até Elite.</div>{badges}</div>'
    at_clip('s5',7.05,B[2]+0.1-7.05,r_html,f'position:absolute;left:{rx:.0f}px;top:{ryy:.0f}px;width:{cw}px;height:{chh}px;perspective:1800px')
    js.append(f'tl.fromTo("#s5 .rcard",{{rotationX:58,y:120,opacity:0,filter:"blur(8px)"}},{{rotationX:0,y:0,opacity:1,filter:"blur(0px)",duration:0.55,ease:"power3.out",transformOrigin:"50% 100%",immediateRender:false}},7.05);')
    cen=[(rx+x+bw/2, ryy+y+bw*1.08+46) for (x,y) in slots]   # just under each badge label
    if not V:
        p5=f'M {cx:.0f} {cy-260:.0f} C {rx-120:.0f} {cy-200:.0f}, {rx-60:.0f} {cen[0][1]+80:.0f}, {rx+40:.0f} {cen[0][1]+30:.0f} L {rx+cw-40:.0f} {cen[0][1]+30:.0f}'
    else:
        y1_,y2_=cen[0][1]+24,cen[4][1]+24
        p5=f'M {cx:.0f} {ryy-200:.0f} C {rx-140:.0f} {ryy:.0f}, {rx-40:.0f} {y1_:.0f}, {rx+40:.0f} {y1_:.0f} L {rx+cw-60:.0f} {y1_:.0f} C {rx+cw+60:.0f} {y1_:.0f}, {rx+cw+60:.0f} {y2_:.0f}, {rx+cw-60:.0f} {y2_:.0f} L {rx+80:.0f} {y2_:.0f}'
    trail(p5,7.25,1.25,0,'power1.inOut',persist_to=B[2]-0.25,width=0.8)
    order=list(range(7)) if not V else [0,1,2,3,6,5,4]
    for k_,i in enumerate(order):
        t=7.25+1.25*(0.36+0.62*k_/6); js.append(f'tl.to("#rk{i}",{{scale:1.18,duration:0.12,ease:"power3.out",yoyo:true,repeat:1}},{t:.3f}); tl.to("#rk{i} .hex",{{opacity:1,boxShadow:"0 0 46px var(--c)",duration:0.15}},{t:.3f}); tl.to("#rk{i} span",{{color:"#fff",duration:0.15}},{t:.3f});'); fx('pop',t,0.32+0.03*i)
    js.append(f'tl.to("#rk6",{{scale:1.32,duration:0.25,ease:"back.out(2)"}},8.78); tl.to("#s5 .rcard",{{rotationY:-30,scale:0.85,opacity:0,filter:"blur(12px)",duration:0.35,ease:"power3.in"}},{B[2]-0.3:.3f});')
    fx('sparkle',8.55,0.55); fx('whoosh-short',7.05,0.35)
    # ═══ 6 · Mentor (B2 → 10.95)
    mw,mh=(1180,600) if not V else (960,940); mx,my=cx-mw/2,cy-mh/2
    m_html=f'''<div class="card mcard" style="width:{mw}px;height:{mh}px">
      <div class="mt"><i class="dot"></i>Mentor iVest<span class="ms">qualquer matéria do vestibular</span></div>
      <div class="ava" style="{'left:80px;top:170px' if not V else f'left:{mw/2-110:.0f}px;top:130px'}">{ICON["brand"]}</div>
      <div id="u1" class="bub me" style="{'left:430px;top:150px;width:670px' if not V else 'left:110px;top:410px;width:780px'}"><span id="uq"></span></div>
      <div id="m1" class="bub bot" style="{'left:430px;top:330px;width:670px' if not V else 'left:70px;top:600px;width:820px'}">Romantismo idealiza. Realismo mostra a vida como ela é.</div></div>'''
    at_clip('s6',B[2],11.05-B[2],m_html,f'position:absolute;left:{mx:.0f}px;top:{my:.0f}px;width:{mw}px;height:{mh}px;perspective:1600px')
    x0,y0,x1,y1=mx-12,my-12,mx+mw+12,my+mh+12; r=40
    p6=f'M {x0+r:.0f} {y0:.0f} L {x1-r:.0f} {y0:.0f} Q {x1:.0f} {y0:.0f} {x1:.0f} {y0+r:.0f} L {x1:.0f} {y1-r:.0f} Q {x1:.0f} {y1:.0f} {x1-r:.0f} {y1:.0f} L {x0+r:.0f} {y1:.0f} Q {x0:.0f} {y1:.0f} {x0:.0f} {y1-r:.0f} L {x0:.0f} {y0+r:.0f} Q {x0:.0f} {y0:.0f} {x0+r:.0f} {y0:.0f}'
    trail(p6,B[2]+0.02,0.7,0,'power2.inOut',persist_to=10.75,width=0.7)
    js.append(f'tl.fromTo("#s6 .mcard",{{scale:0.9,opacity:0,rotationY:18}},{{scale:1,opacity:1,rotationY:0,duration:0.45,ease:"power3.out",immediateRender:false}},{B[2]:.3f}); tl.fromTo("#s6 .ava",{{scale:0.4,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:"back.out(2)",immediateRender:false}},{B[2]+0.2:.3f}); tl.to("#s6 .ava",{{y:-14,duration:0.5,ease:"sine.inOut",yoyo:true,repeat:3}},{B[2]+0.6:.3f});')
    js.append(f'tl.fromTo("#u1",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.25,immediateRender:false}},{B[2]+0.35:.3f}); typeTo("#uq", "Qual a diferença entre Romantismo e Realismo?", {B[2]+0.3:.3f}, 0.5);')
    js.append(f'tl.fromTo("#m1",{{opacity:0,y:24,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(1.8)",immediateRender:false}},{B[2]+0.85:.3f}); tl.to("#s6 .mcard",{{scale:0.86,opacity:0,filter:"blur(12px)",rotationY:-24,duration:0.3,ease:"power3.in"}},10.72);')
    fx('impact-bass-2',B[2],0.7); fx('typing',B[2]+0.3,0.45,0,0.5); fx('notification',B[2]+0.85,0.5)
    # ═══ 7 · feature graph (10.95 → B3)
    feats=[('redacao','Redação','#f97316'),('simulados','Simulados','#c2410c'),('flashcards','Flashcards','#ec4899'),('quiz','Quiz','#ef4444'),('mentor','Mentor IA','#a855f7')]
    if not V:
        hub=(cx-560,cy+60); nodes=[(cx-180+i*215,cy-150+(abs(i-2)*-40)+ (0 if i%2==0 else 70)) for i in range(5)]
        nodes=[(cx-160,cy-170),(cx+60,cy-40),(cx+260,cy-200),(cx+460,cy-60),(cx+650,cy-210)]
    else:
        hub=(cx,cy-430); nodes=[(cx-360,cy-40),(cx-180,cy+230),(cx,cy-20),(cx+180,cy+230),(cx+360,cy-40)]
    hubh=f'<div class="hub" style="left:{hub[0]-90:.0f}px;top:{hub[1]-90:.0f}px">{ICON["brand"]}</div><div class="hlab" style="left:{hub[0]-200:.0f}px;top:{hub[1]+205:.0f}px">PT · EN · ES</div>'
    langs=''.join(f'<div id="lg{i}" class="lang" style="left:{hub[0]-38+150*math.cos(a_):.0f}px;top:{hub[1]-38+150*math.sin(a_):.0f}px">{t}</div>' for i,(t,a_) in enumerate([('PT',-2.3),('EN',-0.85),('ES',2.4)]))
    nd=''.join(f'<div id="nd{i}" class="node" style="left:{x-70:.0f}px;top:{y-70:.0f}px;--c:{c}"><div class="nc">{ICON[ic]}</div><span>{lab}</span></div>' for i,((ic,lab,c),(x,y)) in enumerate(zip(feats,nodes)))
    at_clip('s7',10.95,B[3]+0.1-10.95,hubh+langs+nd,'position:absolute;left:0;top:0;width:100%;height:100%')
    js.append(f'tl.fromTo("#s7 .hub",{{scale:0.3,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:"back.out(2)",immediateRender:false}},10.95); tl.fromTo("#s7 .hlab",{{opacity:0}},{{opacity:1,duration:0.3,immediateRender:false}},11.15);')
    for i in range(3): js.append(f'tl.fromTo("#lg{i}",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.4)",immediateRender:false}},{11.1+0.08*i:.3f}); tl.to("#lg{i}",{{rotation:360,duration:2.2,ease:"none",transformOrigin:"{38-150*math.cos([-2.3,-0.85,2.4][i]):.0f}px {38-150*math.sin([-2.3,-0.85,2.4][i]):.0f}px"}},11.1);')
    for i,(x,y) in enumerate(nodes):
        t=11.2+i*0.28; mxp=(hub[0]+x)/2; myp=min(hub[1],y)-(140 if not V else 80)
        trail(f'M {hub[0]:.0f} {hub[1]:.0f} Q {mxp:.0f} {myp:.0f} {x:.0f} {y:.0f}',t,0.38,0,'power2.out',persist_to=B[3]-0.15,width=0.55)
        js.append(f'tl.fromTo("#nd{i}",{{opacity:0.25,scale:0.8}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(2.4)",immediateRender:false}},{t+0.34:.3f}); tl.to("#nd{i} .nc",{{backgroundColor:"var(--c)",borderColor:"#fff",color:"#fff",boxShadow:"0 0 60px var(--c)",duration:0.15}},{t+0.34:.3f}); tl.to("#nd{i} span",{{color:"#fff",duration:0.15}},{t+0.34:.3f});')
        js.append(f'tl.set("#nd{i}",{{opacity:0.25}},10.95);'); fx('pop',t+0.34,0.45)
    js.append(f'tl.to("#s7 .hub, #s7 .hlab, #s7 .lang, #s7 .node",{{opacity:0,scale:0.6,filter:"blur(10px)",duration:0.3,ease:"power3.in",stagger:0.02}},{B[3]-0.35:.3f});')
    fx('whoosh-short',10.95,0.4)
    # ═══ 8 · end: comet writes the logo, URL fixed (B3 → T)
    ey_=cy-170 if not V else cy-200
    end=f'''<div class="logo" style="left:{cx-lw/2:.0f}px;top:{ey_:.0f}px;width:{lw}px;font-size:{140 if not V else 124}px"><span class="cap">{ICON["brand"]}</span><span><span class="i">i</span>Vest <span class="st">Study</span></span></div>
      <div class="url" style="left:0;width:{W}px;top:{ey_+215:.0f}px">iveststudy.com</div>
      <div class="cta" style="left:{cx-330:.0f}px;top:{ey_+340:.0f}px;width:660px">Comece grátis · 3 dias de Pro</div><div id="s8flash" class="flash"></div>'''
    at_clip('s8',B[3],T-B[3],end,'position:absolute;left:0;top:0;width:100%;height:100%')
    p8=f'M {-100} {ey_+460:.0f} C {cx-320:.0f} {ey_+470:.0f}, {cx-560:.0f} {ey_+175:.0f}, {cx-450:.0f} {ey_+165:.0f} L {cx+450:.0f} {ey_+165:.0f}'
    trail(p8,B[3]-0.3,0.75,0,'power2.inOut',persist_to=None)
    js.append(f'tl.fromTo("#s8 .logo",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.45,ease:"none",immediateRender:false}},{B[3]-0.02:.3f}); tl.fromTo("#s8flash",{{opacity:0}},{{opacity:0.85,duration:0.08,immediateRender:false}},{B[3]+0.42:.3f}); tl.to("#s8flash",{{opacity:0,duration:0.6}},{B[3]+0.5:.3f});')
    js.append(f'tl.fromTo("#s8 .url",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.35,ease:"power3.out",immediateRender:false}},{B[3]+0.55:.3f}); tl.fromTo("#s8 .cta",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)",transformOrigin:"50% 50%",immediateRender:false}},{B[3]+0.8:.3f});')
    js.append(f'tl.to("#s8 .logo",{{scale:1.04,duration:{T-B[3]-0.6:.2f},ease:"sine.inOut",transformOrigin:"50% 50%"}},{B[3]+0.5:.3f}); tl.to("#s8 .cta",{{boxShadow:"0 0 60px rgba(59,130,246,.9)",duration:0.5,ease:"sine.inOut",yoyo:true,repeat:3}},{B[3]+1.2:.3f});')
    fx('whoosh-cinematic',B[3]-0.35,0.4); fx('impact-bass-1',B[3]+0.42,0.85); fx('sparkle',B[3]+0.45,0.5); fx('sonic-logo',T-1.75,0.8)
    # ═══ audio
    aud=[]
    t=M0; i=0
    while t<T-0.05:
        d=min(LOOP,T-t); last=t+d>=T-0.05
        aud.append(f'<audio id="mus{i}" class="clip" src="assets/audio/music-trail.mp3" data-start="{t:.3f}" data-duration="{d:.3f}" data-media-start="7.91" data-volume="0.62" data-fade-out="{0.6 if last else 0}" data-track-index="{3 if i%2==0 else 4}"></audio>'); t+=LOOP; i+=1
    lanes=list(range(8,16)); free={l:0.0 for l in lanes}
    for j,(nm,at,vol,ms,dd) in enumerate(sorted(sfx,key=lambda x:x[1])):
        dd=dd or min(dur(f'assets/sfx/{nm}.mp3'),4.0); dd=min(dd,T-at)
        lane=next((l for l in lanes if free[l]<=at),None) or min(lanes,key=lambda l:free[l]); free[lane]=at+dd+0.02
        aud.append(f'<audio id="fx{j}" class="clip" src="assets/sfx/{nm}.mp3" data-start="{at:.3f}" data-duration="{dd:.2f}" data-media-start="{ms}" data-volume="{vol}" data-track-index="{lane}"></audio>')
    css=f'''
  *{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#030817;font-family:"Inter",sans-serif}}
  #root{{position:relative;width:{W}px;height:{H}px;overflow:hidden;color:#fff;background:radial-gradient(90% 70% at 50% 45%,#0b1f4a 0%,#06112b 45%,#030817 100%)}}
  #haze{{position:absolute;left:{cx-700:.0f}px;top:{cy-700:.0f}px;width:1400px;height:1400px;border-radius:50%;background:radial-gradient(circle,rgba(37,99,235,.35) 0%,rgba(37,99,235,.12) 35%,rgba(3,8,23,0) 65%);filter:blur(40px)}}
  #grain{{position:absolute;inset:0;background:radial-gradient(120% 90% at 50% 50%,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%)}}
  svg.trails{{position:absolute;left:0;top:0;z-index:20;pointer-events:none;overflow:visible}} svg.trails path{{fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:0 1000000}}
  .head{{position:absolute;left:-46px;top:-46px;width:92px;height:92px;border-radius:50%;z-index:21;background:radial-gradient(circle,#fff 0%,#dbeafe 18%,rgba(96,165,250,.85) 34%,rgba(37,99,235,0) 70%)}}
  .clip{{position:absolute}}
  .logo{{position:absolute;display:flex;align-items:center;justify-content:center;gap:.24em;font-weight:800;letter-spacing:-.045em;line-height:1;color:#fff;white-space:nowrap;text-shadow:0 0 40px rgba(96,165,250,.55)}}
  .logo .cap svg{{width:1em;height:1em;display:block;border-radius:.24em;box-shadow:0 0 50px rgba(59,130,246,.9)}} .logo .i{{color:{LIGHT}}} .logo .st{{font-weight:500;color:#dbeafe}}
  .flash{{position:absolute;inset:0;background:radial-gradient(60% 50% at 50% 50%,rgba(191,219,254,.75),rgba(59,130,246,.15) 50%,rgba(0,0,0,0) 75%);opacity:0;pointer-events:none}}
  .chip{{width:120px;height:120px;border-radius:30px;display:flex;align-items:center;justify-content:center;font-size:56px;font-weight:800;color:#93c5fd;background:rgba(15,23,42,.9);border:3px solid rgba(147,197,253,.35);opacity:0}}
  .phone{{position:absolute;left:0;top:0;border-radius:64px;background:#0b111c;border:10px solid #1b2436;box-shadow:0 50px 120px rgba(0,0,0,.6),0 0 60px rgba(59,130,246,.25);overflow:hidden;transform-style:preserve-3d;padding:90px 34px 0}}
  .isl{{position:absolute;left:50%;top:22px;width:150px;height:40px;margin-left:-75px;border-radius:999px;background:#000}}
  .pbar{{display:flex;align-items:center;gap:14px;font-size:30px;font-weight:700}} .pb-ic svg{{width:38px;height:38px;color:#60a5fa;display:block}} .pb-r{{margin-left:auto;font-size:28px;color:#93c5fd;font-weight:600}}
  .prog{{height:10px;border-radius:5px;background:#1e293b;margin:22px 0 28px}} .prog i{{display:block;width:20%;height:100%;border-radius:5px;background:#3b82f6}}
  .q{{font-size:30px;line-height:1.28;font-weight:700;color:#f1f5f9}}
  .timer{{margin-top:26px;border:2px solid #1f2a3d;border-radius:22px;padding:16px 22px;display:flex;align-items:center;justify-content:space-between}} .tl{{font-size:28px;letter-spacing:.12em;color:#94a3b8;font-weight:700}} .tv{{font-size:48px;font-weight:800;font-variant-numeric:tabular-nums}}
  .ans{{margin-top:22px;min-height:150px;border:2px solid #1f2a3d;border-radius:22px;padding:18px 22px;font-size:30px;line-height:1.35;color:#e2e8f0}} .caret{{display:inline-block;width:3px;height:1em;background:#60a5fa;vertical-align:-.12em;margin-left:3px}}
  .pbtn{{margin-top:24px;display:inline-block;background:#2563eb;color:#fff;font-weight:700;font-size:30px;padding:18px 28px;border-radius:18px;transform-origin:0 50%}}
  .pres{{margin-top:26px;opacity:0}} .score{{font-weight:800;color:#f59e0b;line-height:1;margin-bottom:16px;display:inline-block}} .score b{{font-size:96px}} .score span{{font-size:44px;color:#fbbf24}}
  .fb{{display:flex;align-items:center;gap:14px;font-size:30px;font-weight:700;padding:12px 16px;border-radius:16px;margin-top:10px;background:rgba(15,23,42,.9);opacity:0}} .fb i{{font-style:normal;width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#04121f;font-size:26px;flex:0 0 42px}}
  .fb.ok{{border:2px solid #22c55e}} .fb.ok i{{background:#22c55e}} .fb.miss{{border:2px solid #f87171}} .fb.miss i{{background:#f87171}}
  svg.ring{{position:absolute;left:0;top:0}}
  .eyb{{position:absolute;display:flex;align-items:center;justify-content:center;gap:14px;font-size:34px;font-weight:800;letter-spacing:.18em;color:#fdba74}} .eyb svg{{width:40px;height:40px;color:#fb923c}}
  .gnum{{position:absolute;text-align:center;line-height:1;font-weight:800;letter-spacing:-.05em}} .gnum b{{font-size:{150 if not V else 170}px;font-variant-numeric:tabular-nums;text-shadow:0 0 50px rgba(96,165,250,.6)}} .gnum span{{font-size:44px;color:#94a3b8;margin-left:6px}}
  .glab{{position:absolute;text-align:center;font-size:36px;font-weight:600;color:#cbd5e1}}
  .pill{{position:absolute;height:84px;border-radius:20px;border:3px solid #334155;background:rgba(15,23,42,.9);display:flex;align-items:center;justify-content:center;gap:12px;font-size:32px;color:#94a3b8;opacity:0}} .pill b{{color:#fff}}
  .spark{{width:12px;height:12px;border-radius:50%;background:#bfdbfe;box-shadow:0 0 16px #60a5fa;opacity:0}}
  .card{{position:absolute;left:0;top:0;border-radius:36px;background:rgba(10,17,32,.92);border:2px solid rgba(148,163,184,.18);box-shadow:0 40px 100px rgba(0,0,0,.55);transform-style:preserve-3d}}
  .ct{{position:absolute;left:70px;top:56px;font-size:56px;font-weight:800;letter-spacing:-.03em}} .cs{{position:absolute;left:70px;top:132px;font-size:34px;color:#cbd5e1;font-weight:500}}
  .rk{{position:absolute;display:flex;flex-direction:column;align-items:center;gap:16px}} .rk .hex{{width:100%;aspect-ratio:1/1.08;background:var(--c);clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%);opacity:.38}} .rk span{{font-size:28px;font-weight:700;color:#94a3b8}}
  .mt{{position:absolute;left:56px;top:46px;font-size:44px;font-weight:800;display:flex;align-items:baseline;gap:18px;flex-wrap:wrap;width:85%}} .mt .dot{{width:18px;height:18px;border-radius:50%;background:#22c55e;box-shadow:0 0 16px #22c55e;align-self:center}} .ms{{font-size:30px;font-weight:500;color:#94a3b8}}
  .ava{{position:absolute;width:220px;height:220px}} .ava svg{{width:220px;height:220px;display:block;border-radius:52px;box-shadow:0 0 90px rgba(59,130,246,.9)}}
  .bub{{position:absolute;font-size:36px;line-height:1.3;font-weight:600;padding:24px 30px;border-radius:28px;opacity:0}} .bub.me{{background:#2563eb;color:#fff;border-bottom-right-radius:8px}} .bub.bot{{background:#111a2c;border:2px solid #334155;color:#e2e8f0;border-bottom-left-radius:8px}}
  .hub{{position:absolute;width:180px;height:180px}} .hub svg{{width:180px;height:180px;display:block;border-radius:44px;box-shadow:0 0 90px rgba(59,130,246,.95)}}
  .hlab{{position:absolute;width:400px;text-align:center;font-size:36px;font-weight:800;color:#dbeafe;letter-spacing:.04em}}
  .lang{{position:absolute;width:76px;height:76px;border-radius:50%;background:#0f172a;border:3px solid #60a5fa;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:800;color:#bfdbfe}}
  .node{{position:absolute;width:140px;display:flex;flex-direction:column;align-items:center;gap:16px}} .nc{{width:140px;height:140px;border-radius:50%;background:rgba(15,23,42,.95);border:3px solid #334155;color:#94a3b8;display:flex;align-items:center;justify-content:center}} .nc svg{{width:62px;height:62px}} .node span{{font-size:32px;font-weight:700;color:#94a3b8;white-space:nowrap}}
  .url{{position:absolute;text-align:center;font-size:{84 if not V else 92}px;font-weight:800;letter-spacing:-.03em;text-shadow:0 0 30px rgba(96,165,250,.6)}}
  .cta{{position:absolute;text-align:center;font-size:40px;font-weight:700;padding:22px 0;border-radius:999px;background:#2563eb;box-shadow:0 0 30px rgba(59,130,246,.6)}}
'''
    jsh='''
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });
  const trail = (gid, at, dur, tail, ease, hid, persistTo) => {
    const g = document.getElementById(gid); const ps = [...g.querySelectorAll('path')]; const L = ps[0].getTotalLength(); const h = hid ? document.getElementById(hid) : null;
    const st = { p: 0 };
    const apply = () => { const e = st.p * (L + tail); const s = tail ? Math.max(0, e - tail) : 0; const ee = Math.min(e, L);
      ps.forEach(p => { p.style.strokeDasharray = `${Math.max(0.01, ee - s)} ${L * 3}`; p.style.strokeDashoffset = `${-s}`; });
      if (h) { const pt = ps[0].getPointAtLength(ee); h.style.transform = `translate(${pt.x}px, ${pt.y}px)`; } };
    tl.set(g, { opacity: 1 }, at);
    tl.fromTo(st, { p: 0 }, { p: 1, duration: dur, ease, onUpdate: apply, immediateRender: false }, at);
    if (h) { tl.set(h, { opacity: 1 }, at); tl.to(h, { opacity: 0, duration: 0.18 }, at + dur); }
    if (persistTo !== null) tl.to(g, { opacity: 0, duration: 0.3, ease: "power2.in" }, persistTo); else if (!tail) tl.to(g, { opacity: 0, duration: 0.5 }, at + dur + 1.2);
  };
  const typeTo = (sel, text, at, dur) => { const el = document.querySelector(sel); const st = { n: 0 }; tl.fromTo(st, { n: 0 }, { n: text.length, duration: dur, ease: "none", onUpdate: () => { el.textContent = text.slice(0, Math.round(st.n)); }, immediateRender: false }, at); };
  const countUp = (sel, a, b, at, dur) => { const el = document.querySelector(sel); const st = { v: a }; tl.fromTo(st, { v: a }, { v: b, duration: dur, ease: "power2.out", onUpdate: () => { el.textContent = String(Math.round(st.v)); }, immediateRender: false }, at); };
  const countDown = (sel, a, b, at, dur) => { const el = document.querySelector(sel); const st = { v: a }; tl.fromTo(st, { v: a }, { v: b, duration: dur, ease: "none", onUpdate: () => { const s = Math.round(st.v); el.textContent = `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`; }, immediateRender: false }, at); };
  tl.fromTo("#haze", { x: -80, y: 30, scale: 0.95 }, { x: 80, y: -30, scale: 1.12, duration: __T__, ease: "sine.inOut" }, 0);
'''.replace("__T__",str(T))
    html=f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8" /><meta name="viewport" content="width={W}, height={H}" /><script src="assets/vendor/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="trail" data-start="0" data-duration="{T}" data-width="{W}" data-height="{H}" data-fps="30">
<div id="haze"></div><div id="grain"></div>
{chr(10).join(els)}
<svg class="trails" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><filter id="glowA" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter><filter id="glowB" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16"/></filter></defs>
{chr(10).join(trails)}
</svg>
{chr(10).join(heads)}
{chr(10).join(aud)}
</div>
<script>{jsh}
  {chr(10).join("  "+l for l in js)}
  window.__timelines["trail"] = tl;
</script></body></html>'''
    os.makedirs('builds',exist_ok=True); out=f'builds/trail-{W}x{H}.html'; open(out,'w',encoding='utf-8').write(html); print('wrote',out,'sfx',len(sfx),'trails',len(trails))

for a in (sys.argv[1:] or ['1920x1080']):
    w,h=map(int,a.split('x')); build(w,h)
