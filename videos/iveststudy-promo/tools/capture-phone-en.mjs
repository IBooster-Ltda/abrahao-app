import { createRequire } from 'module'; const require = createRequire(import.meta.url); const { chromium, devices } = require('playwright'); const fs = require('fs');
const OUT = process.argv[2], ST = process.argv[3], STILL = process.argv[4], HAND = process.argv[5];
const browser = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--no-sandbox'] });
const prep = () => { try { localStorage.setItem('ivest_theme','dark'); } catch (e) {} setInterval(() => { document.querySelectorAll('a,button').forEach(e => { if (e.innerText && e.innerText.trim() === 'Admin') e.style.display = 'none'; }); }, 150); };
const sleep = ms => new Promise(r => setTimeout(r, ms)); const now = () => Date.now();
async function ask(key, text) { fs.writeFileSync(`${HAND}/${key}.question.txt`, text); console.log('WAITING', key); const f = `${HAND}/${key}.answer.txt`; for (let i = 0; i < 2400; i++) { if (fs.existsSync(f)) { const a = fs.readFileSync(f, 'utf8'); if (a.trim()) return a; } await sleep(500); } throw new Error('no answer ' + key); }
async function recorder(page, name) { const dir = `${OUT}/${name}`; fs.mkdirSync(dir, { recursive: true }); const client = await page.context().newCDPSession(page); let n = 0; const meta = []; const t0 = now(); const marks = [];
  client.on('Page.screencastFrame', (ev) => { const i = n++; fs.writeFile(`${dir}/f${String(i).padStart(6, '0')}.jpg`, Buffer.from(ev.data, 'base64'), () => {}); meta.push([i, ev.metadata.timestamp, now() - t0]); client.send('Page.screencastFrameAck', { sessionId: ev.sessionId }).catch(() => {}); });
  await client.send('Page.startScreencast', { format: 'jpeg', quality: 92, maxWidth: 1290, maxHeight: 2796, everyNthFrame: 1 });
  const mark = (label) => { const t = (now() - t0) / 1000; marks.push([label, t]); console.log(`T ${name} ${label} ${t.toFixed(2)}`); };
  const stop = async () => { await client.send('Page.stopScreencast').catch(() => {}); await sleep(800); fs.writeFileSync(`${dir}/meta.json`, JSON.stringify({ frames: meta, marks })); console.log(`REC ${name} frames ${n}`); };
  return { mark, stop }; }
async function flow(name, fn) { const ctx = await browser.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true, locale: 'en-US', userAgent: devices['iPhone 14 Pro Max'].userAgent, storageState: `${ST}/state.json` });
  await ctx.addInitScript(prep); const page = await ctx.newPage(); page.on('dialog', d => d.accept()); let rec = null; page.rec = async () => { rec = await recorder(page, name); return rec; };
  try { await fn(page); } catch (e) { console.log(name, 'ERR', e.message.slice(0, 300)); await page.screenshot({ path: `${STILL}/${name}-error.png` }).catch(()=>{}); }
  if (rec) await rec.stop(); await ctx.storageState({ path: `${ST}/state.json` }); await ctx.close(); console.log('done', name); }
const txt = async (page) => (await page.evaluate(() => document.body.innerText));
const still = (page, n) => page.screenshot({ path: `${STILL}/${n}.png` });
async function smoothScroll(page, px, ms) { await page.evaluate(([px, ms]) => new Promise(r => { const y0 = window.scrollY; const t0 = performance.now(); const step = (t) => { const k = Math.min(1, (t - t0) / ms); const e = k < .5 ? 2*k*k : -1+(4-2*k)*k; window.scrollTo(0, y0 + px * e); if (k < 1) requestAnimationFrame(step); else r(); }; requestAnimationFrame(step); }), [px, ms]); }
async function toEN(page) { const b = page.getByRole('button', { name: 'EN', exact: true }).first(); if (await b.count()) { await b.click(); await page.waitForTimeout(1200); } const s = page.getByText(/Skip guide|Pular guia/).first(); if (await s.count()) { await s.click().catch(()=>{}); await page.waitForTimeout(400); } }
async function typeHuman(page, loc, text) { await loc.click(); for (const ch of text) { await page.keyboard.type(ch); await sleep(ch === ' ' ? 60 + Math.random() * 90 : 28 + Math.random() * 50); if (ch === ',' || ch === '.') await sleep(250 + Math.random() * 300); } }
await flow('en-home', async (page) => { await page.goto('https://www.iveststudy.com/app', { waitUntil: 'networkidle' }); await page.waitForTimeout(1200); await toEN(page); await still(page, 'en-home'); console.log('EN HOME:', (await txt(page)).slice(0, 400).replace(/\n+/g,' | '));
  const rec = await page.rec(); await page.waitForTimeout(1200); rec.mark('top'); await smoothScroll(page, 1200, 3000); await page.waitForTimeout(1200); });
await flow('en-simulados', async (page) => { await page.goto('https://www.iveststudy.com/app', { waitUntil: 'networkidle' }); await page.waitForTimeout(1000); await toEN(page); await page.goto('https://www.iveststudy.com/simulados', { waitUntil: 'networkidle' }); await page.waitForTimeout(1500); console.log('EN SIM:', (await txt(page)).slice(0, 300).replace(/\n+/g,' | '));
  const rec = await page.rec(); await page.waitForTimeout(1000); rec.mark('list');
  const sat = page.locator('button').filter({ hasText: /SAT/ }).first(); await sat.scrollIntoViewIfNeeded(); await page.waitForTimeout(1500); rec.mark('sat-card'); await still(page, 'en-sat-card');
  await sat.click(); await page.waitForTimeout(3000); rec.mark('exam'); await still(page, 'en-sat-exam'); console.log('SAT EXAM:', (await txt(page)).slice(0, 600).replace(/\n+/g,' | ')); await smoothScroll(page, 600, 2000); await page.waitForTimeout(1500); });
await flow('en-estudo', async (page) => { await page.goto('https://www.iveststudy.com/app', { waitUntil: 'networkidle' }); await page.waitForTimeout(1200); await toEN(page);
  const tabb = page.locator('a,button').filter({ hasText: /^\s*(Study|Estudo)\s*$/ }).last(); await tabb.click({ force: true }); await page.waitForTimeout(1300); console.log('EN ESTUDO:', (await txt(page)).slice(0, 500).replace(/\n+/g,' | '));
  const row = page.locator('button').filter({ hasText: /Inglês|English/ }).filter({ hasText: /Select|Selecionar/ }).first(); await row.scrollIntoViewIfNeeded(); await row.click(); await page.waitForTimeout(900);
  const chips = await page.evaluate(() => { const bs = [...document.querySelectorAll('button')]; const i = bs.findIndex(b => /Inglês|English/.test(b.innerText) && /Select|Selecionar/.test(b.innerText)); const out = []; for (let k = i + 1; k < bs.length; k++) { const t = bs[k].innerText.trim(); if (!t || t.length > 40 || /Start|Iniciar|Select|Cancel|Core|Hard|Easy|Básico|Basic|Hardcore|^\d+$|All|Tudo/i.test(t)) continue; out.push(t); if (out.length >= 3) break; } return out; });
  for (const c of chips) { await page.getByRole('button', { name: c, exact: true }).first().click().catch(()=>{}); await page.waitForTimeout(250); }
  await page.locator('button', { hasText: /^\s*Core\s*$/ }).first().click().catch(()=>{}); await page.locator('button', { hasText: /^\s*10\s*$/ }).first().click().catch(()=>{});
  await page.locator('button', { hasText: /^\s*(Start|Iniciar)\s*$/ }).first().click(); await page.waitForTimeout(2500); await still(page, 'en-estudo-q');
  const answer = await ask('en-estudo', (await txt(page)).slice(0, 3000));
  const rec = await page.rec(); await page.waitForTimeout(2500); rec.mark('question');
  const ta = page.locator('textarea').first(); await ta.scrollIntoViewIfNeeded(); await page.waitForTimeout(800); rec.mark('typing-start'); await typeHuman(page, ta, answer.trim()); rec.mark('typing-end'); await page.waitForTimeout(900);
  const btn = page.getByText(/Evaluate answer|Avaliar resposta/).first(); await btn.scrollIntoViewIfNeeded(); await page.waitForTimeout(600); rec.mark('tap-send'); await btn.click();
  for (let i = 0; i < 120; i++) { await sleep(200); const t = await txt(page); if (/\d\/10\b/.test(t) && !/Avaliando|Evaluating|Grading/i.test(t)) break; }
  rec.mark('result'); await page.waitForTimeout(2500); await still(page, 'en-estudo-graded');
  rec.mark('scroll-start'); await smoothScroll(page, 700, 1800); await page.waitForTimeout(2500); rec.mark('scroll-2'); await smoothScroll(page, 700, 1800); await page.waitForTimeout(2500); await smoothScroll(page, 700, 1800); await page.waitForTimeout(2000);
  console.log('EN GRADED:', (await txt(page)).slice(0, 1600).replace(/\n+/g,' | ')); });
await browser.close(); console.log('ALL DONE 4');
