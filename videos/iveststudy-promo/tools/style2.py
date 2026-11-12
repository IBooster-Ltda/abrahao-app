# iVest Study · "rastro de luz" v2 — narrated, captioned, every beat keyed to a spoken word and a music downbeat.
# python3 -I tools/style2.py 1080x1920 1920x1080   → builds/trail2-WxH.html
import json, os, sys, math, re, subprocess
P=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(P)
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
ICON={n:re.sub(r'^<svg[^>]*>',lambda m: re.sub(r'\s(width|height|class|style)="[^"]*"','',m.group(0)),open(f'assets/brand/icons/{n}.svg',encoding='utf-8').read()) for n in ['brand','estudo','quiz','flashcards','simulados','redacao','mentor']}
VO=json.load(open('tools/vo-trail.json',encoding='utf-8'))
BEAT=0.4915; U=2*BEAT; LOOP=8*BEAT; MEDIA0=7.91   # music-trail.mp3: 8-beat drop at media 7.91 (hit on its first frame)
M0=1.2
def units(sec): return math.ceil(sec/U-1e-6)
# schedule: scene start, VO offset, length in 2-beat units (each scene starts on a downbeat with the drop hit)
SC={}; t=M0+U
SC['logo']=(0.0, M0-VO['logo']['marks']['Study'], None)
for k,off,tail in [('estudo',0.35,0.6),('redacao',0.15,0.7),('ranks',0.25,0.8),('mentor',0.2,1.2),('mapa',0.15,0.5),('fim',0.5,None)]:
    n=units(off+VO[k]['dur']+(tail if tail is not None else 1.4)); SC[k]=(round(t,3),off,round(n*U,3)); t+=n*U
T=round(t,3)
BLUE='#3b82f6'; LIGHT='#93c5fd'; CORE='#eff6ff'

def build(W,H):
    V=H>W; cx=W/2; cy=H/2 if not V else 880
    els=[]; js=[]; trails=[]; heads=[]; sfx=[]; n=[0]; cues=[]
    def uid(p): n[0]+=1; return f'{p}{n[0]}'
    def fx(name,at,vol=0.5,ms=0.0,d=None): sfx.append((name,round(at,3),vol,ms,d))
    def strokes(d,width=1.0):
        return f'<path d="{d}" stroke="{BLUE}" stroke-width="{26*width:.1f}" filter="url(#glowB)" opacity=".55"/><path d="{d}" stroke="{LIGHT}" stroke-width="{9*width:.1f}" filter="url(#glowA)"/><path d="{d}" stroke="{CORE}" stroke-width="{3.2*width:.1f}"/>'
    def trail(d, at, du, tail=0, ease='power1.inOut', persist_to=None, width=1.0, local=None):
        """local=(list_for_svg, list_for_heads): draw inside a rotating wrapper so the light stays glued to it."""
        g=uid('tr'); hid=g+'h'
        tgt_t,tgt_h=(trails,heads) if local is None else local
        tgt_t.append(f'<g id="{g}" class="trail" style="opacity:0">{strokes(d,width)}</g>')
        tgt_h.append(f'<div id="{hid}" class="head" style="opacity:0"></div>')
        js.append(f'trail("{g}", {at:.3f}, {du:.3f}, {tail}, "{ease}", "{hid}", {persist_to if persist_to is not None else "null"});')
    def clip(id,start,d,html,style=''):
        els.append(f'<div id="{id}" class="clip" data-start="{start:.3f}" data-duration="{d:.3f}" style="{style}">{html}</div>')
    def vo(k,at):
        els.append(f'<audio id="vo-{k}" class="clip" src="assets/audio/vo-trail/{k}.wav" data-start="{at:.3f}" data-duration="{VO[k]["dur"]:.2f}" data-volume="1" data-track-index="7"></audio>')
        ws=[list(w) for w in VO[k]['words']]
        for w in ws:
            if w[0].lower().startswith('aivest'): w[0]='iVest'
        mrg=[]; i=0
        while i<len(ws):
            seq=[x[0].lower().strip('.,:') for x in ws[i:i+4]]
            if seq[:4]==['ivest','study','ponto','com']: mrg.append(['iveststudy.com',ws[i][1],ws[i+3][2]]); i+=4
            else: mrg.append(ws[i]); i+=1
        cur=[]
        def flush():
            if cur: cues.append([round(at+cur[0][1],2),round(at+cur[-1][2]+0.15,2),' '.join(w for w,_,_ in cur)]); cur.clear()
        for w,a,b in mrg:
            if cur and (len(cur)>=6 or b-cur[0][1]>2.1 or cur[-1][0].endswith(('.',':','?','!')) or (cur[-1][0].endswith(',') and len(cur)>=3)): flush()
            cur.append((w,a,b))
        flush()
    def mk(k,word): s,off,_=SC[k]; return s+off+VO[k]['marks'][word]

    # ═══ 1 · LOGO written by light  (0 → estudo start)
    s,off,_=SC['logo']; P0=SC['estudo'][0]
    lw=980; ly=cy-90
    logo=f'<div class="logo" style="left:{cx-lw/2:.0f}px;top:{ly:.0f}px;width:{lw}px;font-size:{150 if not V else 132}px"><span class="cap">{ICON["brand"]}</span><span><span class="i">i</span>Vest <span class="st">Study</span></span></div>'
    clip('s1',0,P0-0.25,logo+'<div id="s1flash" class="flash"></div>','position:absolute;inset:0')
    p1=(f'M {-120} {H*0.86:.0f} C {cx-700:.0f} {H*0.86:.0f}, {cx-760:.0f} {ly+215:.0f}, {cx-470:.0f} {ly+205:.0f}' if not V else f'M {cx-260:.0f} {ly+620:.0f} C {cx-620:.0f} {ly+560:.0f}, {cx-640:.0f} {ly+225:.0f}, {cx-470:.0f} {ly+205:.0f}')+f' L {cx+470:.0f} {ly+205:.0f} C {cx+640:.0f} {ly+200:.0f}, {cx+700:.0f} {ly+120:.0f}, {cx+720:.0f} {ly-40:.0f}'
    trail(p1,0.0,1.1,0,'power2.inOut',persist_to=P0-0.5)
    js.append(f'tl.fromTo("#s1 .logo",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.62,ease:"none"}},0.4);')
    js.append(f'tl.fromTo("#s1 .logo",{{scale:1}},{{scale:1.06,duration:0.12,ease:"power3.out",yoyo:true,repeat:1,transformOrigin:"50% 50%"}},{M0:.3f}); tl.fromTo("#s1flash",{{opacity:0}},{{opacity:0.9,duration:0.08}},{M0:.3f}); tl.to("#s1flash",{{opacity:0,duration:0.5}},{M0+0.08:.3f});')
    js.append(f'tl.to("#s1 .logo",{{scale:0.55,opacity:0,filter:"blur(14px)",duration:0.35,ease:"power3.in",transformOrigin:"50% 50%"}},{P0-0.62:.3f});')
    vo('logo',s+off)
    fx('riser',0.0,0.55,1.75,M0); fx('whoosh-cinematic',0.02,0.35); fx('impact-bass-2',M0,0.85); fx('sparkle',M0+0.05,0.45)

    # ═══ 2 · phone · Modo Estudo
    s,off,d=SC['estudo']
    pw,ph=(540,920) if not V else (620,1160); px=cx-pw/2; py=(50 if not V else cy-ph/2)
    # comet: logo tail → bounces through four answer chips → lands on the phone's top-left corner
    chips=['A','B','C','D']; cp=[]
    for i,c in enumerate(chips):
        sc_=1.0-0.15*i
        x=(cx-500+i*250) if not V else (cx-300+i*170); y=(cy+260-i*110) if not V else (cy+420-i*170)
        cp.append((x,y)); clip(f'chip{i}',s-0.65,0.9,f'<div class="chip" data-layout-ignore style="transform:scale({sc_:.2f})">{c}</div>',f'position:absolute;left:{x-60:.0f}px;top:{y-60:.0f}px;width:120px;height:120px')
    land=(px-14,py+60)
    p2=f'M {cx+720:.0f} {ly-40:.0f} C {cx+420:.0f} {cy+420:.0f}, {cp[0][0]-200:.0f} {cp[0][1]+170:.0f}, {cp[0][0]:.0f} {cp[0][1]:.0f} '+' '.join(f'Q {(cp[i][0]+cp[i+1][0])/2:.0f} {min(cp[i][1],cp[i+1][1])-120:.0f} {cp[i+1][0]:.0f} {cp[i+1][1]:.0f}' for i in range(3))+f' Q {land[0]-60:.0f} {land[1]-160:.0f} {land[0]:.0f} {land[1]:.0f}'
    trail(p2,s-0.7,0.85,380,'power1.in')
    for i in range(4):
        tt=s-0.7+0.85*(0.4+0.13*i)
        js.append(f'tl.fromTo("#chip{i} .chip",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.2,ease:"power3.out",immediateRender:false}},{s-0.65+0.04*i:.3f}); tl.to("#chip{i} .chip",{{backgroundColor:"#2563eb",borderColor:"#bfdbfe",color:"#fff",boxShadow:"0 0 50px #3b82f6",duration:0.1}},{tt:.3f}); tl.to("#chip{i}",{{opacity:0,scale:1.25,duration:0.22}},{tt+0.2:.3f});'); fx('pop',tt,0.38)
    PS=dict(pb=(30 if not V else 32),q=(28 if not V else 35),tl=28,tv=(44 if not V else 54),ans=(28 if not V else 34),btn=(28 if not V else 34),sc=(84 if not V else 118),fb=(28 if not V else 32))
    ph_html=f'''<div class="pwrap" style="width:{pw}px;height:{ph}px">
      <div class="phone" style="width:{pw}px;height:{ph}px">
        <div class="isl"></div>
        <div class="pbar" style="font-size:{PS['pb']}px"><span class="pb-ic">{ICON["estudo"]}</span><span>Modo Estudo</span><span class="pb-r">História</span></div>
        {"" if not V else '<div class="prog"><i></i></div>'}
        <div class="q" style="font-size:{PS['q']}px;margin-top:{14 if not V else 0}px">O que o “olho por olho, dente por dente” revela sobre a justiça babilônica?</div>
        <div class="timer"><span class="tl">CRONÔMETRO</span><span id="tm" class="tv" style="font-size:{PS['tv']}px">1:00</span></div>
        <div class="ans" style="font-size:{PS['ans']}px"><span id="ty"></span><span id="caret" class="caret"></span></div>
        <div class="slot"><div id="pbtn" class="pbtn" style="font-size:{PS['btn']}px">Avaliar resposta →</div>
          <div id="pres" class="pres"><div class="score"><b id="sc" style="font-size:{PS['sc']}px">4</b><span>/10</span></div>
            <div id="fb1" class="fb ok" style="font-size:{PS['fb']}px"><i>✓</i>Proporcionalidade: acertou</div>
            <div id="fb2" class="fb miss" style="font-size:{PS['fb']}px"><i>✗</i>Leis iguais para todos: errou</div></div></div>
      </div>
      <svg class="ltr" width="{pw+60}" height="{ph+60}" viewBox="0 0 {pw+60} {ph+60}" style="left:-30px;top:-30px">__T__</svg>__H__
    </div>'''
    lt=[]; lh=[]
    r=74; a0,b0,a1,b1=16,16,pw+44,ph+44
    outline=f'M {a0:.0f} {b0+90:.0f} L {a0:.0f} {b0+r:.0f} Q {a0:.0f} {b0:.0f} {a0+r:.0f} {b0:.0f} L {a1-r:.0f} {b0:.0f} Q {a1:.0f} {b0:.0f} {a1:.0f} {b0+r:.0f} L {a1:.0f} {b1-r:.0f} Q {a1:.0f} {b1:.0f} {a1-r:.0f} {b1:.0f} L {a0+r:.0f} {b1:.0f} Q {a0:.0f} {b1:.0f} {a0:.0f} {b1-r:.0f} L {a0:.0f} {b0+90:.0f}'
    trail(outline,s+0.12,0.95,0,'power2.inOut',persist_to=s+d-0.35,width=0.7,local=(lt,lh))
    ph_html=ph_html.replace('__T__','\n'.join(lt)).replace('__H__','\n'.join(h.replace('class="head"','class="head" ').replace('style="opacity:0"','style="opacity:0;left:-76px;top:-76px"') for h in lh))
    clip('s3',s,d,ph_html,f'position:absolute;left:{px:.0f}px;top:{py:.0f}px;width:{pw}px;height:{ph}px;perspective:1700px')
    ty0=mk('estudo','responde'); tap=mk('estudo','corrige'); res=mk('estudo','hora')
    js.append(f'tl.fromTo("#s3 .pwrap",{{rotationY:-34,rotationX:14,scale:0.86,opacity:0,filter:"blur(8px)"}},{{rotationY:-9,rotationX:4,scale:1,opacity:1,filter:"blur(0px)",duration:0.5,ease:"power3.out",immediateRender:false}},{s:.3f}); tl.to("#s3 .pwrap",{{rotationY:7,rotationX:1,duration:{d-0.85:.2f},ease:"none"}},{s+0.5:.3f});')
    ans='A punição tinha que ser igual ao crime. E as leis valiam para todo mundo.'
    js.append(f'typeTo("#ty", {json.dumps(ans)}, {ty0:.3f}, {tap-0.25-ty0:.3f});')
    js.append(f'countDown("#tm", 60, 46, {s:.3f}, {res-s:.3f}); tl.set("#caret",{{opacity:0}},{tap:.3f});')
    js.append(f'tl.to("#pbtn",{{scale:0.94,backgroundColor:"#1d4ed8",duration:0.08,yoyo:true,repeat:1}},{tap:.3f}); tl.set("#pbtn",{{textContent:"Avaliando…"}},{tap+0.05:.3f}); tl.to("#pbtn",{{opacity:0,y:-12,duration:0.15}},{res-0.15:.3f});')
    js.append(f'tl.fromTo("#pres",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3,ease:"power3.out",immediateRender:false}},{res:.3f}); tl.fromTo("#pres .score",{{scale:1.6}},{{scale:1,duration:0.35,ease:"back.out(2.2)",transformOrigin:"0% 60%",immediateRender:false}},{res:.3f});')
    js.append(f'tl.fromTo("#fb1",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.25,immediateRender:false}},{mk("estudo","acertou"):.3f}); tl.fromTo("#fb2",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.25,immediateRender:false}},{mk("estudo","faltou"):.3f});')
    js.append(f'tl.to("#s3 .pwrap",{{rotationY:40,rotationX:-6,scale:0.8,opacity:0,filter:"blur(12px)",duration:0.32,ease:"power3.in"}},{s+d-0.34:.3f});')
    vo('estudo',s+off)
    fx('whoosh-short',s-0.7,0.38); fx('impact-bass-2',s,0.6); fx('typing',ty0,0.45,0,tap-0.25-ty0); fx('send-tap',tap,0.65); fx('ding-correct',res,0.7); fx('ding-correct',mk('estudo','acertou'),0.35); fx('error-blip',mk('estudo','faltou'),0.5)

    # ═══ 3 · essay gauge
    s,off,d=SC['redacao']
    gr=255 if not V else 280; gcx,gcy=cx,(cy-70 if not V else cy-120)
    circ=f'M {gcx:.1f} {gcy-gr:.1f} A {gr} {gr} 0 1 1 {gcx-0.01:.2f} {gcy-gr:.1f}'
    aa=2*math.pi*0.92; arc=f'M {gcx:.1f} {gcy-gr:.1f} A {gr} {gr} 0 1 1 {gcx+gr*math.sin(aa):.1f} {gcy-gr*math.cos(aa):.1f}'
    comps=[('C1',200),('C2',200),('C3',160),('C4',200),('C5',160)]
    pwid=(150 if not V else 172); gap=20; tot=5*pwid+4*gap; pyy=gcy+gr+(46 if not V else 80)
    pills=''.join(f'<div id="cp{i}" class="pill" style="left:{cx-tot/2+i*(pwid+gap):.0f}px;top:{pyy:.0f}px;width:{pwid}px"><b>{c}</b><span>{v}</span></div>' for i,(c,v) in enumerate(comps))
    g_html=f'''<svg class="ring" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><path d="{circ}" stroke="rgba(148,163,184,.16)" stroke-width="22" fill="none"/></svg>
      <div class="eyb" style="left:0;width:{W}px;top:{gcy-gr-(72 if not V else 104):.0f}px">{ICON["redacao"]}<span>REDAÇÃO</span></div>
      <div class="gnum" style="left:0;width:{W}px;top:{gcy-(92 if not V else 104):.0f}px"><b id="gv" style="font-size:{150 if not V else 172}px">0</b><span>/1000</span></div>
      <div class="glab" style="left:0;width:{W}px;top:{gcy+(92 if not V else 104):.0f}px">nota por competência</div>{pills}'''
    clip('s4',s,d,g_html,'position:absolute;left:0;top:0;width:100%;height:100%')
    c0=mk('redacao','zero')
    trail(arc,s,c0-s+0.85,0,'power2.out',persist_to=s+d-0.45,width=1.2)
    js.append(f'countUp("#gv", 0, 920, {s:.3f}, {c0-s+0.85:.3f});')
    js.append(f'tl.fromTo("#s4 .gnum",{{scale:0.8,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2)",transformOrigin:"50% 50%",immediateRender:false}},{s:.3f}); tl.fromTo("#s4 .eyb, #s4 .glab",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.3,immediateRender:false}},{s+0.1:.3f});')
    p0=mk('redacao','competência')-0.25
    for i in range(5):
        tt=p0+i*0.16; js.append(f'tl.fromTo("#cp{i}",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.22,ease:"back.out(2)",immediateRender:false}},{tt:.3f}); tl.to("#cp{i}",{{borderColor:"#22c55e",color:"#bbf7d0",boxShadow:"0 0 30px rgba(34,197,94,.55)",duration:0.15}},{tt+0.1:.3f});'); fx('click-soft',tt,0.4)
    bt=s+d-0.5
    for i in range(14):
        ang=i/14*2*math.pi; sid=f'sp{i}'; els.append(f'<div id="{sid}" class="spark clip" data-start="{bt:.3f}" data-duration="0.6" style="left:{gcx-6:.0f}px;top:{gcy-6:.0f}px"></div>')
        js.append(f'tl.fromTo("#{sid}",{{x:{gr*math.cos(ang)*0.95:.0f},y:{gr*math.sin(ang)*0.95:.0f},opacity:1,scale:1}},{{x:{gr*math.cos(ang)*1.9:.0f},y:{gr*math.sin(ang)*1.9:.0f},opacity:0,scale:0.3,duration:0.5,ease:"power3.out",immediateRender:false}},{bt+0.02:.3f});')
    js.append(f'tl.to("#s4 > *",{{opacity:0,filter:"blur(10px)",scale:1.08,duration:0.3,ease:"power3.in",transformOrigin:"50% 50%"}},{s+d-0.32:.3f});')
    vo('redacao',s+off); fx('impact-bass-2',s,0.6); fx('sparkle',bt,0.45)

    # ═══ 4 · ranks Bronze → Elite
    s,off,d=SC['ranks']
    ranks=[('Bronze','#d97706'),('Prata','#94a3b8'),('Ouro','#f59e0b'),('Platina','#14b8a6'),('Diamante','#38bdf8'),('Mestre','#a855f7'),('Elite','#ef4444')]
    cw,chh=(1400,520) if not V else (1000,800); rx,ryy=cx-cw/2,cy-chh/2
    bw=128 if not V else 158
    if not V: g7=(cw-140-7*bw)/6; slots=[(70+i*(bw+g7),chh-262) for i in range(7)]; order=list(range(7))
    else: g4=(cw-140-4*bw)/3; slots=[(70+i*(bw+g4),250) for i in range(4)]+[(70+(bw+g4)/2+i*(bw+g4),520) for i in range(3)]; order=[0,1,2,3,6,5,4]
    badges=''.join(f'<div id="rk{i}" class="rk" style="left:{x:.0f}px;top:{y:.0f}px;width:{bw}px;--c:{c}"><div class="hex"></div><span>{nm}</span></div>' for i,((nm,c),(x,y)) in enumerate(zip(ranks,slots)))
    lt=[]; lh=[]
    cen=[(x+bw/2,y+bw*1.08+52) for x,y in slots]
    if not V: rp=f'M 30 {cen[0][1]+18:.0f} L {cw-30:.0f} {cen[0][1]+18:.0f}'
    else:
        y1_,y2_=cen[0][1]+14,cen[4][1]+14
        rp=f'M 30 {y1_:.0f} L {cw-90:.0f} {y1_:.0f} C {cw+10:.0f} {y1_:.0f}, {cw+10:.0f} {y2_:.0f}, {cw-90:.0f} {y2_:.0f} L 90 {y2_:.0f}'
    r0=s+0.3; r1=mk('ranks','Elite'); trail(rp,r0,r1-r0,0,'power1.inOut',persist_to=s+d-0.35,width=0.8,local=(lt,lh))
    r_html=f'''<div class="rwrap" style="width:{cw}px;height:{chh}px"><div class="card" style="width:{cw}px;height:{chh}px"><div class="ct">Progressão de Ranks</div><div class="cs">Suba de Bronze até Elite.</div>{badges}</div>
      <svg class="ltr" width="{cw}" height="{chh}" viewBox="0 0 {cw} {chh}" style="left:0;top:0">{"".join(lt)}</svg>{"".join(h.replace('style="opacity:0"','style="opacity:0"') for h in lh)}</div>'''
    clip('s5',s,d,r_html,f'position:absolute;left:{rx:.0f}px;top:{ryy:.0f}px;width:{cw}px;height:{chh}px;perspective:1800px')
    js.append(f'tl.fromTo("#s5 .rwrap",{{rotationX:55,y:110,opacity:0,filter:"blur(8px)"}},{{rotationX:0,y:0,opacity:1,filter:"blur(0px)",duration:0.45,ease:"power3.out",transformOrigin:"50% 100%",immediateRender:false}},{s:.3f}); tl.to("#s5 .rwrap",{{rotationY:-4,duration:{d-0.8:.2f},ease:"none"}},{s+0.45:.3f});')
    for k_,i in enumerate(order):
        tt=r0+(r1-r0)*(0.08+0.92*k_/6); js.append(f'tl.to("#rk{i}",{{scale:1.16,duration:0.1,ease:"power3.out",yoyo:true,repeat:1}},{tt:.3f}); tl.to("#rk{i} .hex",{{opacity:1,boxShadow:"0 0 46px var(--c)",duration:0.12}},{tt:.3f}); tl.to("#rk{i} span",{{color:"#fff",duration:0.12}},{tt:.3f});'); fx('pop',tt,0.3+0.03*k_)
    js.append(f'tl.to("#rk6",{{scale:1.3,duration:0.22,ease:"back.out(2)"}},{r1+0.22:.3f}); tl.to("#s5 .rwrap",{{rotationY:-28,scale:0.86,opacity:0,filter:"blur(12px)",duration:0.3,ease:"power3.in"}},{s+d-0.32:.3f});')
    vo('ranks',s+off); fx('impact-bass-2',s,0.5); fx('sparkle',r1+0.2,0.5)

    # ═══ 5 · Mentor
    s,off,d=SC['mentor']
    mw,mh=(1180,560) if not V else (960,800); mx,my=cx-mw/2,cy-mh/2
    bubs=('left:420px;top:140px;width:690px','left:420px;top:318px;width:690px','left:70px;top:160px') if not V else ('left:90px;top:360px;width:800px','left:60px;top:560px;width:840px',f'left:{mw/2-100:.0f}px;top:120px')
    lt=[]; lh=[]; r=44; a0,b0,a1,b1=16,16,mw+44,mh+44
    mo=f'M {a0+r:.0f} {b0:.0f} L {a1-r:.0f} {b0:.0f} Q {a1:.0f} {b0:.0f} {a1:.0f} {b0+r:.0f} L {a1:.0f} {b1-r:.0f} Q {a1:.0f} {b1:.0f} {a1-r:.0f} {b1:.0f} L {a0+r:.0f} {b1:.0f} Q {a0:.0f} {b1:.0f} {a0:.0f} {b1-r:.0f} L {a0:.0f} {b0+r:.0f} Q {a0:.0f} {b0:.0f} {a0+r:.0f} {b0:.0f}'
    trail(mo,s+0.05,0.65,0,'power2.inOut',persist_to=s+d-0.35,width=0.7,local=(lt,lh))
    m_html=f'''<div class="mwrap" style="width:{mw}px;height:{mh}px"><div class="card" style="width:{mw}px;height:{mh}px">
        <div class="mt"><i class="dot"></i>Mentor iVest<span class="ms">qualquer matéria</span></div>
        <div class="ava" style="{bubs[2]}">{ICON["brand"]}</div>
        <div id="u1" class="bub me" style="{bubs[0]}"><span id="uq"></span></div>
        <div id="m1" class="bub bot" style="{bubs[1]}">Romantismo idealiza. Realismo mostra a vida como ela é.</div></div>
      <svg class="ltr" width="{mw+60}" height="{mh+60}" viewBox="0 0 {mw+60} {mh+60}" style="left:-30px;top:-30px">{"".join(lt)}</svg>{"".join(h.replace('style="opacity:0"','style="opacity:0;left:-76px;top:-76px"') for h in lh)}</div>'''
    clip('s6',s,d,m_html,f'position:absolute;left:{mx:.0f}px;top:{my:.0f}px;width:{mw}px;height:{mh}px;perspective:1600px')
    ma=mk('mentor','dúvida')
    js.append(f'tl.fromTo("#s6 .mwrap",{{scale:0.9,opacity:0,rotationY:16}},{{scale:1,opacity:1,rotationY:0,duration:0.4,ease:"power3.out",immediateRender:false}},{s:.3f}); tl.fromTo("#s6 .ava",{{scale:0.4,opacity:0}},{{scale:1,opacity:1,duration:0.35,ease:"back.out(2)",immediateRender:false}},{s+0.15:.3f}); tl.to("#s6 .ava",{{y:-12,duration:0.5,ease:"sine.inOut",yoyo:true,repeat:{int((d-1)/0.5)}}},{s+0.5:.3f});')
    js.append(f'tl.fromTo("#u1",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.22,immediateRender:false}},{s+0.25:.3f}); typeTo("#uq", "Qual a diferença entre Romantismo e Realismo?", {s+0.3:.3f}, {ma-0.15-s-0.3:.3f});')
    js.append(f'tl.fromTo("#m1",{{opacity:0,y:24,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(1.8)",immediateRender:false}},{ma:.3f}); tl.to("#s6 .mwrap",{{scale:0.86,opacity:0,filter:"blur(12px)",rotationY:-22,duration:0.3,ease:"power3.in"}},{s+d-0.32:.3f});')
    vo('mentor',s+off); fx('impact-bass-2',s,0.5); fx('typing',s+0.3,0.4,0,ma-0.45-s); fx('notification',ma,0.5)

    # ═══ 6 · feature map
    s,off,d=SC['mapa']
    feats=[('redacao','Redação','#f97316'),('simulados','Simulados','#c2410c'),('flashcards','Flashcards','#ec4899'),('quiz','Quiz','#ef4444'),('mentor','Mentor IA','#a855f7')]
    if not V: hub=(cx-620,cy+40); nodes=[(cx-280,cy-190),(cx-60,cy+130),(cx+160,cy-190),(cx+380,cy+130),(cx+600,cy-190)]
    else: hub=(cx,cy-430); nodes=[(cx-360,cy-30),(cx-180,cy+250),(cx,cy-10),(cx+180,cy+250),(cx+360,cy-30)]
    ang=[-2.45,-0.7,2.55]; R_=200
    hubh=f'<div class="hub" style="left:{hub[0]-90:.0f}px;top:{hub[1]-90:.0f}px">{ICON["brand"]}</div><div class="hlab" style="left:{hub[0]-220:.0f}px;top:{hub[1]+(250 if V else 230):.0f}px">PT · EN · ES</div>'
    langs=''.join(f'<div id="lg{i}" class="lang" style="left:{hub[0]-38+R_*math.cos(a_):.0f}px;top:{hub[1]-38+R_*math.sin(a_):.0f}px">{t_}</div>' for i,(t_,a_) in enumerate(zip(['PT','EN','ES'],ang)))
    nd=''.join(f'<div id="nd{i}" class="node" style="left:{x-70:.0f}px;top:{y-70:.0f}px;--c:{c}"><div class="nc">{ICON[ic]}</div><span>{lab}</span></div>' for i,((ic,lab,c),(x,y)) in enumerate(zip(feats,nodes)))
    clip('s7',s,d,hubh+langs+nd,'position:absolute;left:0;top:0;width:100%;height:100%')
    js.append(f'tl.fromTo("#s7 .hub",{{scale:0.3,opacity:0}},{{scale:1,opacity:1,duration:0.35,ease:"back.out(2)",immediateRender:false}},{s:.3f});')
    t_sim=max(mk('mapa','Simulados'),s+0.3); times=[t_sim+0.25, t_sim, mk('mapa','flashcards'), mk('mapa','quiz'), mk('mapa','quiz')+0.3]
    for i,((x,y),t0_) in enumerate(zip(nodes,times)):
        mxp=(hub[0]+x)/2; myp=min(hub[1],y)-(140 if not V else 60)
        trail(f'M {hub[0]:.0f} {hub[1]:.0f} Q {mxp:.0f} {myp:.0f} {x:.0f} {y:.0f}',t0_-0.3,0.34,0,'power2.out',persist_to=s+d-0.3,width=0.55)
        js.append(f'tl.set("#nd{i}",{{opacity:0.28}},{s:.3f}); tl.fromTo("#nd{i}",{{scale:0.8}},{{scale:1,duration:0.25,ease:"back.out(2.4)",immediateRender:false}},{t0_+0.04:.3f}); tl.to("#nd{i}",{{opacity:1,duration:0.1}},{t0_+0.04:.3f}); tl.to("#nd{i} .nc",{{backgroundColor:"var(--c)",borderColor:"#fff",color:"#fff",boxShadow:"0 0 60px var(--c)",duration:0.15}},{t0_+0.04:.3f}); tl.to("#nd{i} span",{{color:"#fff",duration:0.15}},{t0_+0.04:.3f});'); fx('pop',t0_+0.04,0.42)
    lt0=mk('mapa','português')
    for i in range(3):
        org=f'{38-R_*math.cos(ang[i]):.0f}px {38-R_*math.sin(ang[i]):.0f}px'
        js.append(f'tl.fromTo("#lg{i}",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.28,ease:"back.out(2.4)",immediateRender:false}},{lt0+0.18*i:.3f}); tl.fromTo("#lg{i}",{{rotation:0}},{{rotation:200,duration:{s+d-lt0:.2f},ease:"none",transformOrigin:"{org}",immediateRender:false}},{lt0:.3f});'); fx('click-soft',lt0+0.18*i,0.4)
    js.append(f'tl.fromTo("#s7 .hlab",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3,immediateRender:false}},{lt0:.3f});')
    js.append(f'tl.to("#s7 .hub, #s7 .hlab, #s7 .lang, #s7 .node",{{opacity:0,scale:0.6,filter:"blur(10px)",duration:0.28,ease:"power3.in",stagger:0.015}},{s+d-0.32:.3f});')
    vo('mapa',s+off); fx('impact-bass-2',s,0.5)

    # ═══ 7 · end card
    s,off,d=SC['fim']; ey_=cy-170 if not V else cy-200
    end=f'''<div class="logo" style="left:{cx-lw/2:.0f}px;top:{ey_:.0f}px;width:{lw}px;font-size:{140 if not V else 124}px"><span class="cap">{ICON["brand"]}</span><span><span class="i">i</span>Vest <span class="st">Study</span></span></div>
      <div class="url" style="left:0;width:{W}px;top:{ey_+215:.0f}px">iveststudy.com</div>
      <div class="cta" style="left:{cx-340:.0f}px;top:{ey_+340:.0f}px;width:680px">Comece grátis · 3 dias de Pro</div><div id="s8flash" class="flash"></div>'''
    clip('s8',s,d,end,'position:absolute;left:0;top:0;width:100%;height:100%')
    p8=f'M {-100} {ey_+460:.0f} C {cx-320:.0f} {ey_+470:.0f}, {cx-560:.0f} {ey_+175:.0f}, {cx-450:.0f} {ey_+165:.0f} L {cx+450:.0f} {ey_+165:.0f}'
    trail(p8,s-0.3,0.75,0,'power2.inOut',persist_to=None)
    js.append(f'tl.fromTo("#s8 .logo",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.45,ease:"none",immediateRender:false}},{s-0.02:.3f}); tl.fromTo("#s8flash",{{opacity:0}},{{opacity:0.85,duration:0.08,immediateRender:false}},{s+0.42:.3f}); tl.to("#s8flash",{{opacity:0,duration:0.6}},{s+0.5:.3f});')
    ga=mk('fim','grátis'); ua=mk('fim','aiVest')
    js.append(f'tl.fromTo("#s8 .cta",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)",transformOrigin:"50% 50%",immediateRender:false}},{ga:.3f}); tl.fromTo("#s8 .url",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.3,ease:"power3.out",immediateRender:false}},{ua:.3f});')
    js.append(f'tl.to("#s8 .logo",{{scale:1.04,duration:{d-0.6:.2f},ease:"sine.inOut",transformOrigin:"50% 50%"}},{s+0.5:.3f}); tl.to("#s8 .cta",{{boxShadow:"0 0 60px rgba(59,130,246,.9)",duration:0.5,ease:"sine.inOut",yoyo:true,repeat:{int((s+d-ga-0.6)/0.5)}}},{ga+0.4:.3f});')
    vo('fim',s+off); fx('whoosh-cinematic',s-0.35,0.35); fx('impact-bass-1',s+0.42,0.8); fx('sparkle',s+0.45,0.45); fx('sonic-logo',T-1.7,0.75)

    # ═══ captions (burned) — safe zones: 9:16 y≤1520, 16:9 bottom band
    capy=1500 if V else 986
    for i,(a,b,txt) in enumerate(cues):
        b=min(b, cues[i+1][0]-0.04) if i+1<len(cues) else min(b,T-0.05)
        els.append(f'<div id="cap{i}" class="subcap clip" data-start="{a:.2f}" data-duration="{max(0.35,b-a):.2f}" style="top:{capy}px">{txt}</div>')
    # ═══ music: every scene restarts the 8-beat drop on its first frame; ducked under the voice
    aud=[]; k=0
    starts=[M0]+[SC[x][0] for x in ['estudo','redacao','ranks','mentor','mapa','fim']]+[T]
    for a,b in zip(starts[:-1],starts[1:]):
        t_=a
        while t_<b-0.02:
            dd=min(LOOP,b-t_); last=b>=T-0.01 and t_+dd>=T-0.02
            aud.append(f'<audio id="mus{k}" class="clip" src="assets/audio/music-trail.mp3" data-start="{t_:.3f}" data-duration="{dd:.3f}" data-media-start="{MEDIA0}" data-volume="0.42" data-fade-out="{0.7 if last else 0}" data-track-index="{3+k%2}"></audio>'); t_+=dd; k+=1
    lanes=list(range(8,16)); free={l:0.0 for l in lanes}
    for j,(nm,at,vol,ms,dd) in enumerate(sorted(sfx,key=lambda x:x[1])):
        dd=dd or min(dur(f'assets/sfx/{nm}.mp3'),4.0); dd=max(0.2,min(dd,T-at))
        lane=next((l for l in lanes if free[l]<=at),None) or min(lanes,key=lambda l:free[l]); free[lane]=at+dd+0.02
        aud.append(f'<audio id="fx{j}" class="clip" src="assets/sfx/{nm}.mp3" data-start="{at:.3f}" data-duration="{dd:.2f}" data-media-start="{ms}" data-volume="{vol}" data-track-index="{lane}"></audio>')
    css=open('tools/style2.css',encoding='utf-8').read().replace('__W__',str(W)).replace('__H__',str(H)).replace('__HX__',f'{cx-700:.0f}').replace('__HY__',f'{cy-700:.0f}').replace('__CAPF__','46' if V else '42')
    jsh=open('tools/style2.js',encoding='utf-8').read().replace('__T__',str(T))
    html=f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8" /><meta name="viewport" content="width={W}, height={H}" /><script src="assets/vendor/gsap.min.js"></script><style>{css}</style></head>
<body><div id="root" data-composition-id="trail2" data-start="0" data-duration="{T}" data-width="{W}" data-height="{H}" data-fps="30">
<div id="haze"></div><div id="vig"></div>
{chr(10).join(els)}
<svg class="trails" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><filter id="glowA" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter><filter id="glowB" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16"/></filter></defs>
{chr(10).join(trails)}
</svg>
{chr(10).join(heads)}
{chr(10).join(aud)}
</div>
<script>{jsh}
  {chr(10).join("  "+l for l in js)}
  window.__timelines["trail2"] = tl;
</script></body></html>'''
    os.makedirs('builds',exist_ok=True); out=f'builds/trail2-{W}x{H}.html'; open(out,'w',encoding='utf-8').write(html)
    srt=''.join(f'{i+1}\n{f2s(a)} --> {f2s(b)}\n{tx}\n\n' for i,(a,b,tx) in enumerate(cues))
    os.makedirs('deliver',exist_ok=True); open(f'deliver/trail2-{W}x{H}.srt','w',encoding='utf-8').write(srt)
    print('wrote',out,'T',T,'cues',len(cues),'sfx',len(sfx),'scenes',SC)
def f2s(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return f'{h:02d}:{m:02d}:{s:06.3f}'.replace('.',',')
for a in (sys.argv[1:] or ['1080x1920']):
    w,h=map(int,a.split('x')); build(w,h)
