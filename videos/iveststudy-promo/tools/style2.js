
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
