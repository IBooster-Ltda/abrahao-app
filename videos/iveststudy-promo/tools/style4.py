# iVest Study · "rastro de luz" v3 — calmer, narrated; light only where it does a job
# (writes the logo, fills the essay ring, wires the feature map, underlines the end card).
# python3 -I tools/style3.py 1080x1920 1920x1080  → builds/trail3-WxH.html + deliver/trail3-WxH.srt
import json, os, sys, math, re, subprocess
P=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(P)
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
ICON={n:re.sub(r'^<svg[^>]*>',lambda m: re.sub(r'\s(width|height|class|style)="[^"]*"','',m.group(0)),open(f'assets/brand/icons/{n}.svg',encoding='utf-8').read()) for n in ['brand','estudo','quiz','flashcards','simulados','redacao','mentor']}
CFG=dict(vo='vo-trail-f', sched='trail4-schedule', music='music-trail3', name='trail4')
CFG.update(dict(a.split('=',1) for a in sys.argv[1:] if '=' in a))   # e.g. vo=vo-trail-aa sched=trail5-schedule music=music-trail5 name=trail5
VO=json.load(open(f'tools/{CFG["vo"]}.json',encoding='utf-8'))
SCH=json.load(open(f'tools/{CFG["sched"]}.json')); SC={k:tuple(v) for k,v in SCH['sched'].items()}; T=SCH['T']
BLUE='#3b82f6'; LIGHT='#93c5fd'; CORE='#eff6ff'
IN=0.7; OUT=0.5

def build(W,H):
    V=H>W; cx=W/2; cy=H/2 if not V else 880
    els=[]; js=[]; trails=[]; heads=[]; sfx=[]; n=[0]; cues=[]
    def uid(p): n[0]+=1; return f'{p}{n[0]}'
    def fx(name,at,vol=0.5,ms=0.0,d=None): sfx.append((name,round(at,3),vol,ms,d))
    def trail(d, at, du, ease='power2.inOut', persist_to=None, width=1.0, head=True):
        g=uid('tr'); hid=g+'h'
        trails.append(f'<g id="{g}" class="trail" style="opacity:0"><path d="{d}" stroke="{BLUE}" stroke-width="{22*width:.1f}" filter="url(#glowB)" opacity=".5"/><path d="{d}" stroke="{LIGHT}" stroke-width="{8*width:.1f}" filter="url(#glowA)"/><path d="{d}" stroke="{CORE}" stroke-width="{3*width:.1f}"/></g>')
        heads.append(f'<div id="{hid}" class="head" style="opacity:0"></div>')
        js.append(f'trail("{g}", {at:.3f}, {du:.3f}, 0, "{ease}", {json.dumps(hid if head else None)}, {persist_to if persist_to is not None else "null"});')
    def clip(id,start,d,html,style=''):
        els.append(f'<div id="{id}" class="clip" data-start="{start:.3f}" data-duration="{d:.3f}" style="{style}">{html}</div>')
    def mk(k,word): s,off,_=SC[k]; return s+off+VO[k]['marks'][word]
    def vo(k):
        s,off,_=SC[k]; at=s+off
        els.append(f'<audio id="vo-{k}" class="clip" src="assets/audio/{CFG["vo"]}/{k}.wav" data-start="{at:.3f}" data-duration="{VO[k]["dur"]:.2f}" data-volume="1" data-track-index="7"></audio>')
        ws=[list(w) for w in VO[k]['words']]
        for w in ws:
            if w[0].lower().startswith('aivest'): w[0]='iVest'
        mrg=[]; i=0
        while i<len(ws):
            seq=[x[0].lower().strip('.,:?') for x in ws[i:i+4]]
            if seq[:4]==['ivest','study','ponto','com']: mrg.append(['iveststudy.com',ws[i][1],ws[i+3][2]]); i+=4
            else: mrg.append(ws[i]); i+=1
        cur=[]
        def flush():
            if cur: cues.append([round(at+cur[0][1],2),round(at+cur[-1][2]+0.25,2),' '.join(w for w,_,_ in cur)]); cur.clear()
        for w,a,b in mrg:
            if cur and (len(cur)>=6 or b-cur[0][1]>2.2 or cur[-1][0].endswith(('.',':','?','!')) or (cur[-1][0].endswith(',') and len(cur)>=3)): flush()
            cur.append((w,a,b))
        flush()
    def enter(sel,at,frm,to='{rotationY:0,rotationX:0,scale:1,opacity:1,y:0}',origin='50% 50%'):
        js.append(f'tl.fromTo("{sel}",{frm},{{...{to},duration:{IN},ease:"power3.out",transformOrigin:"{origin}",immediateRender:false}},{at:.3f});')
    def leave(sel,at,to='{scale:0.94,opacity:0,y:-20}'):
        js.append(f'tl.to("{sel}",{{...{to},duration:{OUT},ease:"power2.in"}},{at:.3f});')
    def drift(sel,a,b,frm,to):
        js.append(f'tl.fromTo("{sel}",{frm},{{...{to},duration:{b-a:.2f},ease:"sine.inOut",immediateRender:false}},{a:.3f});')

    # ═══ 1 · logo, written by one stroke of light
    s,off,d=SC['logo']
    lw=1000; ly=cy-95; fs=150 if not V else 132
    logo=lambda sid,top: f'<div class="logo" style="left:{cx-lw/2:.0f}px;top:{top:.0f}px;width:{lw}px;font-size:{fs}px"><span class="cap">{ICON["brand"]}</span><span><span class="i">i</span>Vest <span class="st">Study</span></span></div>'
    clip('s1',0,d,logo('l1',ly)+'<div id="s1flash" class="flash"></div>','position:absolute;inset:0')
    ux0,ux1,uy=cx-430,cx+430,ly+fs*1.25
    trail(f'M {ux0:.0f} {uy:.0f} L {ux1:.0f} {uy:.0f}',0.25,1.0,'power2.inOut',persist_to=d-OUT)
    js.append(f'tl.fromTo("#s1 .logo",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:1.0,ease:"power2.inOut"}},0.25);')
    js.append('tl.fromTo("#s1flash",{opacity:0},{opacity:0.7,duration:0.12,immediateRender:false},1.24); tl.to("#s1flash",{opacity:0,duration:0.9},1.36);')
    drift('#s1 .logo',1.25,d,'{scale:1}','{scale:1.04}'); leave('#s1 .logo',d-OUT,'{scale:1.08,opacity:0,filter:"blur(6px)"}')
    vo('logo'); fx('riser',0.0,0.4,1.75,1.24); fx('impact-bass-2',1.24,0.55); fx('sparkle',1.26,0.35)

    # ═══ 2 · Modo Estudo on a phone
    s,off,d=SC['estudo']
    pw,ph=(540,920) if not V else (620,1160); px=cx-pw/2; py=(50 if not V else cy-ph/2)
    PS=dict(pb=(30 if not V else 32),q=(28 if not V else 35),tv=(44 if not V else 54),ans=(28 if not V else 34),btn=(28 if not V else 34),sc=(84 if not V else 118),fb=(28 if not V else 32))
    prog='' if not V else '<div class="prog"><i></i></div>'
    ph_html=f'''<div class="pwrap" style="width:{pw}px;height:{ph}px"><div class="phone" style="width:{pw}px;height:{ph}px">
        <div class="isl"></div>
        <div class="pbar" style="font-size:{PS['pb']}px"><span class="pb-ic">{ICON["estudo"]}</span><span>Modo Estudo</span><span class="pb-r">História</span></div>{prog}
        <div class="q" style="font-size:{PS['q']}px;margin-top:{14 if not V else 0}px">O que o “olho por olho, dente por dente” revela sobre a justiça babilônica?</div>
        <div class="timer"><span class="tl">CRONÔMETRO</span><span id="tm" class="tv" style="font-size:{PS['tv']}px">1:00</span></div>
        <div class="ans" style="font-size:{PS['ans']}px"><span id="ty"></span><span id="caret" class="caret"></span></div>
        <div class="slot"><div id="pbtn" class="pbtn" style="font-size:{PS['btn']}px">Avaliar resposta →</div>
          <div id="pres" class="pres"><div class="score"><b id="sc" style="font-size:{PS['sc']}px">4</b><span>/10</span></div>
            <div id="fb1" class="fb ok" style="font-size:{PS['fb']}px"><i>✓</i>Proporcionalidade: acertou</div>
            <div id="fb2" class="fb miss" style="font-size:{PS['fb']}px"><i>✗</i>Leis iguais para todos: errou</div></div></div>
      </div></div>'''
    clip('s2',s,d,ph_html,f'position:absolute;left:{px:.0f}px;top:{py:.0f}px;width:{pw}px;height:{ph}px;perspective:1800px')
    tap=mk('estudo','corrige'); res=mk('estudo','hora'); a1=mk('estudo','acertou'); a2=mk('estudo','faltou')
    enter('#s2 .pwrap',s,'{rotationY:-24,rotationX:10,scale:0.9,opacity:0,y:40}','{rotationY:-8,rotationX:3,scale:1,opacity:1,y:0}')
    drift('#s2 .pwrap',s+IN,res,'{rotationY:-8,rotationX:3}','{rotationY:0,rotationX:0}')
    js.append(f'tl.fromTo("#s2 .phone",{{boxShadow:"0 50px 120px rgba(0,0,0,.6), 0 0 0px rgba(59,130,246,0)"}},{{boxShadow:"0 50px 120px rgba(0,0,0,.6), 0 0 70px rgba(59,130,246,.45)",duration:1.2,immediateRender:false}},{s+0.3:.3f});')
    ans='A punição era igual ao crime. E as leis valiam para todos.'
    js.append(f'typeTo("#ty", {json.dumps(ans)}, {s+0.7:.3f}, {tap-0.4-s-0.7:.3f});')
    js.append(f'countDown("#tm", 60, 51, {s:.3f}, {res-s:.3f}); tl.set("#caret",{{opacity:0}},{tap:.3f});')
    js.append(f'tl.to("#pbtn",{{scale:0.95,backgroundColor:"#1d4ed8",duration:0.1,yoyo:true,repeat:1}},{tap:.3f}); tl.set("#pbtn",{{textContent:"Avaliando…"}},{tap+0.08:.3f}); tl.to("#pbtn",{{opacity:0,duration:0.2}},{res-0.2:.3f});')
    js.append(f'tl.fromTo("#pres",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.4,ease:"power3.out",immediateRender:false}},{res:.3f}); tl.fromTo("#pres .score",{{scale:1.4}},{{scale:1,duration:0.5,ease:"back.out(2)",transformOrigin:"0% 60%",immediateRender:false}},{res:.3f});')
    js.append(f'tl.fromTo("#fb1",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.35,immediateRender:false}},{a1:.3f}); tl.fromTo("#fb2",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:0.35,immediateRender:false}},{a2:.3f});')
    drift('#s2 .pwrap',res,s+d-OUT,'{scale:1}','{scale:1.05}')
    leave('#s2 .pwrap',s+d-OUT,'{scale:0.96,opacity:0,y:-30}')
    vo('estudo'); fx('whoosh-short',s,0.3); fx('typing',s+0.7,0.4,0,tap-0.4-s-0.7); fx('send-tap',tap,0.55); fx('ding-correct',res,0.6); fx('ding-correct',a1,0.3); fx('error-blip',a2,0.45)

    # ═══ 3 · essay — the light fills the score ring
    s,off,d=SC['redacao']
    gr=255 if not V else 280; gcx,gcy=cx,(cy-70 if not V else cy-120)
    circ=f'M {gcx:.1f} {gcy-gr:.1f} A {gr} {gr} 0 1 1 {gcx-0.01:.2f} {gcy-gr:.1f}'
    aa=2*math.pi*0.92; arc=f'M {gcx:.1f} {gcy-gr:.1f} A {gr} {gr} 0 1 1 {gcx+gr*math.sin(aa):.1f} {gcy-gr*math.cos(aa):.1f}'
    comps=[('C1',200),('C2',200),('C3',160),('C4',200),('C5',160)]
    pwid=(150 if not V else 172); gap=20; tot=5*pwid+4*gap; pyy=gcy+gr+(46 if not V else 80)
    pills=''.join(f'<div id="cp{i}" class="pill" style="left:{cx-tot/2+i*(pwid+gap):.0f}px;top:{pyy:.0f}px;width:{pwid}px"><b>{c}</b><span>{v}</span></div>' for i,(c,v) in enumerate(comps))
    g_html=f'''<svg class="ring" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><path d="{circ}" stroke="rgba(148,163,184,.14)" stroke-width="20" fill="none"/></svg>
      <div class="eyb" style="left:0;width:{W}px;top:{gcy-gr-(72 if not V else 104):.0f}px">{ICON["redacao"]}<span>REDAÇÃO</span></div>
      <div class="gnum" style="left:0;width:{W}px;top:{gcy-(92 if not V else 104):.0f}px"><b id="gv" style="font-size:{150 if not V else 172}px">0</b><span>/1000</span></div>
      <div class="glab" style="left:0;width:{W}px;top:{gcy+(92 if not V else 104):.0f}px">nota por competência</div>{pills}'''
    clip('s3',s,d,g_html,'position:absolute;left:0;top:0;width:100%;height:100%')
    z=mk('redacao','zero'); cdur=z-s+0.7
    trail(arc,s+0.2,cdur,'power2.out',persist_to=s+d-OUT,width=1.1)
    js.append(f'countUp("#gv", 0, 920, {s+0.2:.3f}, {cdur:.3f});')
    enter('#s3 .gnum',s,'{scale:0.85,opacity:0}'); enter('#s3 .eyb, #s3 .glab',s+0.15,'{opacity:0,y:16}')
    p0=mk('redacao','competência')
    for i in range(5):
        tt=p0+i*0.28; js.append(f'tl.fromTo("#cp{i}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.8)",immediateRender:false}},{tt:.3f}); tl.to("#cp{i}",{{borderColor:"#22c55e",color:"#bbf7d0",boxShadow:"0 0 26px rgba(34,197,94,.45)",duration:0.25}},{tt+0.15:.3f});'); fx('click-soft',tt,0.35)
    leave('#s3 > *',s+d-OUT,'{opacity:0,scale:1.04}')
    vo('redacao'); fx('whoosh-short',s,0.25); fx('sparkle',s+0.2+cdur,0.35)

    # ═══ 4 · ranks — a plain progress bar fills under the badges
    s,off,d=SC['ranks']
    ranks=[('Bronze','#d97706'),('Prata','#94a3b8'),('Ouro','#f59e0b'),('Platina','#14b8a6'),('Diamante','#38bdf8'),('Mestre','#a855f7'),('Elite','#ef4444')]
    cw,chh=(1400,560) if not V else (1000,820); rx,ryy=cx-cw/2,cy-chh/2
    bw=128 if not V else 158
    if not V: g7=(cw-140-7*bw)/6; slots=[(70+i*(bw+g7),210) for i in range(7)]
    else: g4=(cw-140-4*bw)/3; slots=[(70+i*(bw+g4),230) for i in range(4)]+[(70+(bw+g4)/2+i*(bw+g4),500) for i in range(3)]
    badges=''.join(f'<div id="rk{i}" class="rk" style="left:{x:.0f}px;top:{y:.0f}px;width:{bw}px;--c:{c}"><div class="hex"></div><span>{nm}</span></div>' for i,((nm,c),(x,y)) in enumerate(zip(ranks,slots)))
    bar_y=chh-80
    r_html=f'''<div class="rwrap" style="width:{cw}px;height:{chh}px"><div class="card" style="width:{cw}px;height:{chh}px"><div class="ct">Progressão de Ranks</div><div class="cs">Índice de Preparo · Bronze → Elite</div>{badges}
      <div class="bar" style="left:70px;top:{bar_y}px;width:{cw-140}px"><i id="rbar"></i></div></div></div>'''
    clip('s4',s,d,r_html,f'position:absolute;left:{rx:.0f}px;top:{ryy:.0f}px;width:{cw}px;height:{chh}px;perspective:1800px')
    enter('#s4 .rwrap',s,'{rotationX:30,y:80,opacity:0,scale:0.95}','{rotationX:0,y:0,opacity:1,scale:1}','50% 100%')
    r0=mk('ranks','treino'); r1=mk('ranks','Elite')
    js.append(f'tl.fromTo("#rbar",{{scaleX:0.02}},{{scaleX:1,duration:{r1-r0:.2f},ease:"power1.inOut",transformOrigin:"0% 50%",immediateRender:false}},{r0:.3f});')
    for i in range(7):
        tt=r0+(r1-r0)*(i/6); js.append(f'tl.to("#rk{i} .hex",{{opacity:1,boxShadow:"0 0 40px var(--c)",duration:0.25}},{tt:.3f}); tl.to("#rk{i} span",{{color:"#fff",duration:0.25}},{tt:.3f}); tl.fromTo("#rk{i}",{{scale:1}},{{scale:1.1,duration:0.18,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{tt:.3f});'); fx('pop',tt,0.25+0.03*i)
    js.append(f'tl.to("#rk6",{{scale:1.22,duration:0.4,ease:"back.out(2)"}},{r1+0.4:.3f});')
    drift('#s4 .rwrap',s+IN,s+d-OUT,'{rotationY:0}','{rotationY:-4}'); leave('#s4 .rwrap',s+d-OUT)
    vo('ranks'); fx('whoosh-short',s,0.25); fx('sparkle',r1+0.4,0.4)

    # ═══ 5 · Mentor
    s,off,d=SC['mentor']
    mw,mh=(1180,560) if not V else (960,820); mx,my=cx-mw/2,cy-mh/2
    bubs=('left:420px;top:140px;width:690px','left:420px;top:318px;width:690px','left:70px;top:160px') if not V else ('left:90px;top:360px;width:800px','left:60px;top:570px;width:840px',f'left:{mw/2-100:.0f}px;top:120px')
    m_html=f'''<div class="mwrap" style="width:{mw}px;height:{mh}px"><div class="card" style="width:{mw}px;height:{mh}px">
        <div class="mt"><i class="dot"></i>Mentor iVest<span class="ms">qualquer matéria</span></div>
        <div class="ava" style="{bubs[2]}">{ICON["brand"]}</div>
        <div id="u1" class="bub me" style="{bubs[0]}"><span id="uq"></span></div>
        <div id="m1" class="bub bot" style="{bubs[1]}">Romantismo idealiza. Realismo mostra a vida como ela é.</div></div></div>'''
    clip('s5',s,d,m_html,f'position:absolute;left:{mx:.0f}px;top:{my:.0f}px;width:{mw}px;height:{mh}px;perspective:1600px')
    enter('#s5 .mwrap',s,'{rotationY:14,scale:0.94,opacity:0}','{rotationY:0,scale:1,opacity:1}')
    enter('#s5 .ava',s+0.2,'{scale:0.6,opacity:0}')
    rp=mk('mentor','responde')
    js.append(f'tl.fromTo("#u1",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.3,immediateRender:false}},{s+0.35:.3f}); typeTo("#uq", "Qual a diferença entre Romantismo e Realismo?", {s+0.4:.3f}, {rp-0.35-s-0.4:.3f});')
    js.append(f'tl.fromTo("#m1",{{opacity:0,y:20,scale:0.97}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(1.6)",immediateRender:false}},{rp:.3f});')
    drift('#s5 .mwrap',s+IN,s+d-OUT,'{scale:1}','{scale:1.03}'); leave('#s5 .mwrap',s+d-OUT)
    vo('mentor'); fx('whoosh-short',s,0.25); fx('typing',s+0.4,0.35,0,rp-0.35-s-0.4); fx('notification',rp,0.45)

    # ═══ 6 · feature map — connectors are the only lines, one per feature as it is named
    s,off,d=SC['mapa']
    feats=[('redacao','Redação','#ea580c'),('simulados','Simulados','#92573a'),('flashcards','Flashcards','#ec4899'),('quiz','Quiz','#dc2626'),('mentor','Mentor IA','#7b8694')]   # computed sidebar colours, dark mode
    if not V:
        hub=(400,470); fan=[-60,30,-30,60,0]   # one ray per node: Redação, Simulados, Flashcards, Quiz, Mentor
        nodes=[(hub[0]+1000*math.cos(math.radians(a_)),hub[1]+420*math.sin(math.radians(a_))) for a_ in fan]
    else: hub=(cx,cy-300); nodes=[(cx-360,cy+90),(cx-180,cy+370),(cx,cy+110),(cx+180,cy+370),(cx+360,cy+90)]
    NR=72; HUB=90
    langs=['PT','EN','ES']; lx=[hub[0]-150+i*150 for i in range(3)]; lyy=hub[1]+(-215 if V else 170)
    hubh=f'<div class="hub" style="left:{hub[0]-90:.0f}px;top:{hub[1]-90:.0f}px">{ICON["brand"]}</div>'+''.join(f'<div id="lg{i}" class="lang" style="left:{x-38:.0f}px;top:{lyy:.0f}px">{t_}</div>' for i,(t_,x) in enumerate(zip(langs,lx)))
    nd=''.join(f'<div id="nd{i}" class="node4" style="left:{x-NR:.0f}px;top:{y-NR:.0f}px;--c:{c}"><div class="disc">{ICON[ic]}</div><span data-layout-allow-overflow>{lab}</span></div>' for i,((ic,lab,c),(x,y)) in enumerate(zip(feats,nodes)))
    clip('s6',s,d,hubh+nd,'position:absolute;left:0;top:0;width:100%;height:100%')
    enter('#s6 .hub',s,'{scale:0.5,opacity:0}')
    js.append(f'tl.fromTo("#s6 .node4",{{opacity:0,scale:0.85}},{{opacity:0.4,scale:1,duration:0.5,stagger:0.06,immediateRender:false}},{s+0.2:.3f});')
    times=[s+0.5, mk('mapa','simulados'), mk('mapa','flashcards'), mk('mapa','quiz'), s+0.75]
    for i,((x,y),t0_) in enumerate(zip(nodes,times)):
        dx,dy=x-hub[0],y-hub[1]; L_=math.hypot(dx,dy); ux,uy_=dx/L_,dy/L_
        k_=HUB/max(abs(ux),abs(uy_)); sx,sy=hub[0]+ux*(k_+10),hub[1]+uy_*(k_+10)        # leave the hub tile at its border
        ex,ey=x-ux*(NR+10),y-uy_*(NR+10)                                                # arrive at the node ring
        trail(f'M {sx:.1f} {sy:.1f} L {ex:.1f} {ey:.1f}',t0_-0.4,0.45,'power2.out',persist_to=s+d-OUT,width=0.5)
        js.append(f'tl.to("#nd{i}",{{opacity:1,duration:0.2}},{t0_+0.05:.3f}); tl.to("#nd{i} .disc",{{borderColor:"var(--c)",boxShadow:"0 0 46px var(--c), inset 0 0 30px color-mix(in srgb, var(--c) 35%, transparent)",duration:0.3}},{t0_+0.05:.3f}); tl.to("#nd{i} span",{{color:"#fff",duration:0.25}},{t0_+0.05:.3f}); tl.fromTo("#nd{i}",{{scale:1}},{{scale:1.1,duration:0.2,yoyo:true,repeat:1,immediateRender:false}},{t0_+0.05:.3f});')
        fx('pop',t0_+0.05,0.38 if i in (1,2,3) else 0.2)
    lt0=mk('mapa','português')
    for i in range(3):
        js.append(f'tl.fromTo("#lg{i}",{{scale:0.4,opacity:0}},{{scale:1,opacity:1,duration:0.35,ease:"back.out(2.2)",immediateRender:false}},{lt0+0.5*i:.3f});'); fx('click-soft',lt0+0.5*i,0.35)
    leave('#s6 .hub, #s6 .lang, #s6 .node4',s+d-OUT,'{opacity:0,scale:0.92}')
    vo('mapa'); fx('whoosh-short',s,0.25)

    # ═══ 7 · end card — the same stroke underlines the brand
    s,off,d=SC['fim']; ey_=cy-170 if not V else cy-200
    end=f'''{logo('l2',ey_).replace('class="logo"','class="logo"')}
      <div class="url" style="left:0;width:{W}px;top:{ey_+(230 if not V else 215):.0f}px">iveststudy.com</div>
      <div class="cta" style="left:{cx-340:.0f}px;top:{ey_+(355 if not V else 340):.0f}px;width:680px">Comece grátis · 3 dias de Pro</div><div id="s7flash" class="flash"></div>'''
    clip('s7',s,d,end,'position:absolute;left:0;top:0;width:100%;height:100%')
    uy2=ey_+fs*1.25-(4 if not V else 10)
    trail(f'M {ux0:.0f} {uy2:.0f} L {ux1:.0f} {uy2:.0f}',s+0.1,0.9,'power2.inOut',persist_to=None)
    js.append(f'tl.fromTo("#s7 .logo",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.9,ease:"power2.inOut",immediateRender:false}},{s+0.1:.3f}); tl.fromTo("#s7flash",{{opacity:0}},{{opacity:0.6,duration:0.12,immediateRender:false}},{s+1.0:.3f}); tl.to("#s7flash",{{opacity:0,duration:0.9}},{s+1.12:.3f});')
    ga=mk('fim','grátis'); ua=mk('fim','aiVest')
    enter('#s7 .cta',ga,'{opacity:0,scale:0.92}'); enter('#s7 .url',ua,'{opacity:0,y:20}')
    drift('#s7 .logo',s+1.0,T,'{scale:1}','{scale:1.03}')
    js.append(f'tl.to("#s7 .cta",{{boxShadow:"0 0 60px rgba(59,130,246,.85)",duration:0.6,ease:"sine.inOut",yoyo:true,repeat:{int((T-ga-1.0)/0.6)}}},{ga+0.7:.3f});')
    vo('fim'); fx('impact-bass-1',s+1.0,0.6); fx('sparkle',s+1.02,0.35); fx('sonic-logo',T-1.75,0.65)

    # ═══ captions
    capy=1520 if V else 990
    for i,(a,b,txt) in enumerate(cues):
        b=min(b, cues[i+1][0]-0.04) if i+1<len(cues) else min(b,T-0.05)
        els.append(f'<div id="cap{i}" class="subcap clip" data-start="{a:.2f}" data-duration="{max(0.4,b-a):.2f}" style="top:{capy}px">{txt}</div>')
    # ═══ audio
    aud=[f'<audio id="music" class="clip" src="assets/audio/{CFG["music"]}.mp3" data-start="0" data-duration="{T}" data-media-start="0" data-volume="0.34" data-track-index="3"></audio>']
    lanes=list(range(8,16)); free={l:0.0 for l in lanes}
    for j,(nm,at,vol,ms,dd) in enumerate(sorted(sfx,key=lambda x:x[1])):
        dd=dd or min(dur(f'assets/sfx/{nm}.mp3'),4.0); dd=max(0.2,min(dd,T-at))
        lane=next((l for l in lanes if free[l]<=at),None) or min(lanes,key=lambda l:free[l]); free[lane]=at+dd+0.02
        aud.append(f'<audio id="fx{j}" class="clip" src="assets/sfx/{nm}.mp3" data-start="{at:.3f}" data-duration="{dd:.2f}" data-media-start="{ms}" data-volume="{vol}" data-track-index="{lane}"></audio>')
    css=open('tools/style2.css',encoding='utf-8').read().replace('__W__',str(W)).replace('__H__',str(H)).replace('__HX__',f'{cx-700:.0f}').replace('__HY__',f'{cy-700:.0f}').replace('__CAPF__','46' if V else '42')
    css+='''
  .node4{position:absolute;width:144px;height:144px;display:flex;flex-direction:column;align-items:center;gap:18px;overflow:visible}
  .node4 .disc{width:144px;height:144px;border-radius:50%;background:#0b1222;border:4px solid color-mix(in srgb, var(--c) 55%, #1e293b);color:var(--c);display:flex;align-items:center;justify-content:center;flex:0 0 144px}
  .node4 .disc svg{width:70px;height:70px;stroke-width:2.1}
  .node4 span{font-size:34px;font-weight:700;color:#cbd5e1;white-space:nowrap}
  .bar{position:absolute;height:14px;border-radius:7px;background:rgba(148,163,184,.16);overflow:hidden} .bar i{display:block;width:100%;height:100%;border-radius:7px;background:linear-gradient(90deg,#d97706,#f59e0b,#14b8a6,#38bdf8,#a855f7,#ef4444);transform:scaleX(.02);transform-origin:0 50%}
  .lang{width:76px;height:76px;font-size:28px}
'''
    jsh=open('tools/style2.js',encoding='utf-8').read().replace('__T__',str(T))
    html=f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8" /><meta name="viewport" content="width={W}, height={H}" /><script src="assets/vendor/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="{CFG['name']}" data-start="0" data-duration="{T}" data-width="{W}" data-height="{H}" data-fps="30">
<div id="haze"></div><div id="vig"></div>
{chr(10).join(els)}
<svg class="trails" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><filter id="glowA" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter><filter id="glowB" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter></defs>
{chr(10).join(trails)}
</svg>
{chr(10).join(heads)}
{chr(10).join(aud)}
</div>
<script>{jsh}
  {chr(10).join("  "+l for l in js)}
  window.__timelines["{CFG['name']}"] = tl;
</script></body></html>'''
    os.makedirs('builds',exist_ok=True); out=f'builds/{CFG["name"]}-{W}x{H}.html'; open(out,'w',encoding='utf-8').write(html)
    def f2s(t): h=int(t//3600); m=int(t%3600//60); ss=t%60; return f'{h:02d}:{m:02d}:{ss:06.3f}'.replace('.',',')
    os.makedirs('deliver',exist_ok=True); open(f'deliver/{CFG["name"]}-{W}x{H}.srt','w',encoding='utf-8').write(''.join(f'{i+1}\n{f2s(a)} --> {f2s(b)}\n{tx}\n\n' for i,(a,b,tx) in enumerate(cues)))
    print('wrote',out,'T',T,'cues',len(cues),'trails',len(trails),'sfx',len(sfx))
for a in ([x for x in sys.argv[1:] if '=' not in x] or ['1080x1920']):
    w,h=map(int,a.split('x')); build(w,h)
