import { createRequire } from 'module'; const require = createRequire(import.meta.url); const { chromium, devices } = require('playwright'); const fs = require('fs');
const OUT = process.argv[2], ST = process.argv[3], STILL = process.argv[4], HAND = process.argv[5]; const ONLY = (process.argv[6] || '').split(',').filter(Boolean);
const browser = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--no-sandbox'] });
const prep = () => { try { localStorage.setItem('ivest_theme','dark'); } catch (e) {} setInterval(() => { document.querySelectorAll('a,button').forEach(e => { if (e.innerText && e.innerText.trim() === 'Admin') e.style.display = 'none'; }); }, 150); };
const sleep = ms => new Promise(r => setTimeout(r, ms)); const now = () => Date.now();
async function ask(key, text) { fs.writeFileSync(`${HAND}/${key}.question.txt`, text); console.log('WAITING', key); const f = `${HAND}/${key}.answer.txt`; for (let i = 0; i < 2400; i++) { if (fs.existsSync(f)) { const a = fs.readFileSync(f, 'utf8'); if (a.trim()) return a; } await sleep(500); } throw new Error('no answer ' + key); }
// 3x screencast recorder: frames at device pixels, timestamps kept
async function recorder(page, name) {
  const dir = `${OUT}/${name}`; fs.mkdirSync(dir, { recursive: true });
  const client = await page.context().newCDPSession(page); let n = 0; const meta = []; const t0 = now(); const marks = [];
  client.on('Page.screencastFrame', (ev) => { const i = n++; fs.writeFile(`${dir}/f${String(i).padStart(6, '0')}.jpg`, Buffer.from(ev.data, 'base64'), () => {}); meta.push([i, ev.metadata.timestamp, now() - t0]); client.send('Page.screencastFrameAck', { sessionId: ev.sessionId }).catch(() => {}); });
  await client.send('Page.startScreencast', { format: 'jpeg', quality: 92, maxWidth: 1290, maxHeight: 2796, everyNthFrame: 1 });
  const mark = (label) => { const t = (now() - t0) / 1000; marks.push([label, t]); console.log(`T ${name} ${label} ${t.toFixed(2)}`); };
  const stop = async () => { await client.send('Page.stopScreencast').catch(() => {}); await sleep(800); fs.writeFileSync(`${dir}/meta.json`, JSON.stringify({ frames: meta, marks })); console.log(`REC ${name} frames ${n}`); };
  return { mark, stop };
}
async function flow(name, fn, opts = {}) {
  if (ONLY.length && !ONLY.includes(name)) return;
  const ctx = await browser.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true, locale: 'pt-BR', userAgent: devices['iPhone 14 Pro Max'].userAgent, ...(opts.anon ? {} : { storageState: `${ST}/state.json` }) });
  await ctx.addInitScript(prep); const page = await ctx.newPage(); page.on('dialog', d => d.accept());
  let rec = null; page.rec = async () => { rec = await recorder(page, name); return rec; };
  try { await fn(page); } catch (e) { console.log(name, 'ERR', e.message.slice(0, 300)); await page.screenshot({ path: `${STILL}/${name}-error.png` }).catch(()=>{}); }
  if (rec) await rec.stop();
  if (!opts.anon) await ctx.storageState({ path: `${ST}/state.json` }); await ctx.close(); console.log('done', name);
}
const skipGuide = async (page) => { const s = page.getByText('Pular guia'); if (await s.count()) { await s.first().click(); await page.waitForTimeout(500); } };
const tab = (page, t) => page.locator('a,button').filter({ hasText: new RegExp('^\\s*' + t + '\\s*$') }).last();
const still = (page, n) => page.screenshot({ path: `${STILL}/${n}.png` });
const txt = async (page) => (await page.evaluate(() => document.body.innerText));
async function pickSubject(page, subj, nChips = 3) {
  const row = page.locator('button').filter({ hasText: subj }).filter({ hasText: 'Selecionar' }).first(); await row.scrollIntoViewIfNeeded(); await row.click(); await page.waitForTimeout(900);
  const chips = await page.evaluate((subj) => { const bs = [...document.querySelectorAll('button')]; const i = bs.findIndex(b => b.innerText.includes(subj) && b.innerText.includes('Selecionar')); const out = []; for (let k = i + 1; k < bs.length; k++) { const t = bs[k].innerText.trim(); if (!t || t.length > 40 || /Iniciar|Selecionar|Cancelar|Core|Difícil|Fácil|Médio|Básico|Hardcore|^\d+$|Tudo/i.test(t)) continue; out.push(t); if (out.length >= 3) break; } return out; }, subj);
  for (const c of chips.slice(0, nChips)) { await page.getByRole('button', { name: c, exact: true }).first().click().catch(()=>{}); await page.waitForTimeout(250); }
}
const diff = (page, name) => page.locator('button', { hasText: new RegExp('^' + name + '$') }).first();
async function typeHuman(page, loc, text) { await loc.click(); for (const ch of text) { await page.keyboard.type(ch); await sleep(ch === ' ' ? 60 + Math.random() * 90 : 28 + Math.random() * 50); if (ch === ',' || ch === '.') await sleep(250 + Math.random() * 300); } }
async function slowScroll(page, steps, px = 300, pause = 1300) { for (let i = 0; i < steps; i++) { await page.mouse.wheel(0, px); await page.waitForTimeout(pause); } }
async function smoothScroll(page, px, ms) { await page.evaluate(([px, ms]) => new Promise(r => { const y0 = window.scrollY; const t0 = performance.now(); const step = (t) => { const k = Math.min(1, (t - t0) / ms); const e = k < .5 ? 2*k*k : -1+(4-2*k)*k; window.scrollTo(0, y0 + px * e); if (k < 1) requestAnimationFrame(step); else r(); }; requestAnimationFrame(step); }), [px, ms]); }
const imgInfo = (page) => page.evaluate(() => [...document.querySelectorAll('main img, article img, section img')].map(i => ({ alt: i.alt, ok: i.complete && i.naturalWidth > 0 })));

await flow('estudo', async (page) => {
  await page.goto('https://www.iveststudy.com/app', { waitUntil: 'networkidle' }); await page.waitForTimeout(1200); await skipGuide(page);
  await tab(page, 'Estudo').click({ force: true }); await page.waitForTimeout(1300);
  await pickSubject(page, 'História'); await diff(page, 'Core').click(); await page.waitForTimeout(250); await diff(page, '10').click().catch(()=>{}); await page.waitForTimeout(250);
  await page.locator('button', { hasText: /^\s*Iniciar\s*$/ }).first().click(); await page.waitForTimeout(2500);
  for (let k = 0; k < 6; k++) { const imgs = await imgInfo(page); const t = await txt(page); const hasPic = imgs.length > 0 || /Retrato d|\[imagem\]|Figura/i.test(t); if (!hasPic) break; const sk = page.getByText(/Pular/).first(); if (await sk.count()) { await sk.click(); await page.waitForTimeout(2200); } else break; }
  await page.waitForTimeout(600); await still(page, 'estudo-q');
  const answer = await ask('estudo', (await txt(page)).slice(0, 3000));
  const rec = await page.rec(); await page.waitForTimeout(2500); rec.mark('question');
  const ta = page.locator('textarea').first(); await ta.scrollIntoViewIfNeeded(); await page.waitForTimeout(800); rec.mark('typing-start');
  await typeHuman(page, ta, answer.trim()); rec.mark('typing-end'); await page.waitForTimeout(900);
  const btn = page.getByText('Avaliar resposta →').first(); await btn.scrollIntoViewIfNeeded(); await page.waitForTimeout(600); rec.mark('tap-send'); await btn.click();
  for (let i = 0; i < 90; i++) { await sleep(200); const t = await txt(page); if (/\/10/.test(t) && !/Avaliando|Analisando|Corrigindo/i.test(t)) break; }
  rec.mark('result'); await page.waitForTimeout(2500); await still(page, 'estudo-graded');
  rec.mark('scroll-start'); await smoothScroll(page, 700, 1800); await page.waitForTimeout(2500); rec.mark('scroll-2'); await smoothScroll(page, 700, 1800); await page.waitForTimeout(2500); await smoothScroll(page, 700, 1800); await page.waitForTimeout(2000);
  await page.screenshot({ path: `${STILL}/estudo-graded-full.png`, fullPage: true });
  console.log('GRADED:', (await txt(page)).slice(0, 1800).replace(/\n+/g,' | '));
});
await flow('redacao', async (page) => {
  await page.goto('https://www.iveststudy.com/redacao', { waitUntil: 'networkidle' }); await page.waitForTimeout(1500);
  await page.getByText('A valorização da saúde mental na sociedade contemporânea').last().click(); await page.waitForTimeout(1500);
  const essay = fs.readFileSync(`${HAND}/redacao-m2.txt`, 'utf8'); const ta = page.locator('textarea').first(); await ta.waitFor({ timeout: 15000 });
  const rec = await page.rec(); await page.waitForTimeout(1200); rec.mark('editor');
  await ta.click(); await page.keyboard.type(essay.slice(0, 160), { delay: 30 }); rec.mark('typed-sample'); await ta.fill(essay); await page.waitForTimeout(1200); rec.mark('filled');
  const btn = page.getByText(/Avaliar redação/).first(); await btn.scrollIntoViewIfNeeded(); await page.waitForTimeout(600); rec.mark('tap-send'); await btn.click();
  for (let i = 0; i < 240; i++) { await sleep(200); const t = await txt(page); if (/\/1000/.test(t) && !/Avaliando|Analisando|Corrigindo/i.test(t)) break; }
  rec.mark('result'); await page.waitForTimeout(3000); await still(page, 'redacao-result');
  rec.mark('scroll-start'); await smoothScroll(page, 900, 2200); await page.waitForTimeout(2200); await smoothScroll(page, 900, 2200); await page.waitForTimeout(2200);
  await page.screenshot({ path: `${STILL}/redacao-result-full.png`, fullPage: true });
  console.log('REDACAO:', (await txt(page)).slice(0, 1200).replace(/\n+/g,' | '));
});
await flow('simulados', async (page) => {
  await page.goto('https://www.iveststudy.com/simulados', { waitUntil: 'networkidle' }); await page.waitForTimeout(1500);
  const rec = await page.rec(); await page.waitForTimeout(1500); rec.mark('list');
  await smoothScroll(page, 1500, 2600); await page.waitForTimeout(1500); rec.mark('scrolled'); await smoothScroll(page, -1500, 1200); await page.waitForTimeout(1000);
  const b = page.getByText(/Iniciar simulado ENEM/).first(); await b.scrollIntoViewIfNeeded(); await page.waitForTimeout(600); rec.mark('tap'); await b.click(); await page.waitForTimeout(3000); rec.mark('exam'); await still(page, 'simulado-enem'); await smoothScroll(page, 600, 2000); await page.waitForTimeout(1500);
});
await flow('flashcards', async (page) => {
  await page.goto('https://www.iveststudy.com/app', { waitUntil: 'networkidle' }); await page.waitForTimeout(1200); await skipGuide(page);
  await tab(page, 'Flashcards').click({ force: true }); await page.waitForTimeout(1300);
  await pickSubject(page, 'Biologia'); await diff(page, 'Core').click().catch(()=>{}); await page.waitForTimeout(300);
  await page.getByText(/Iniciar flashcards/).first().click(); await page.waitForTimeout(2500);
  const rec = await page.rec(); await page.waitForTimeout(1500); rec.mark('front');
  await page.getByText('toque para ver a resposta').first().click(); rec.mark('flip'); await page.waitForTimeout(2200); await still(page, 'flashcard-back');
  await page.getByText('Sabia!').first().click(); rec.mark('sabia'); await page.waitForTimeout(2200);
  await page.getByText('toque para ver a resposta').first().click().catch(()=>{}); rec.mark('flip2'); await page.waitForTimeout(2000); await page.getByText('Quase lá').first().click().catch(()=>{}); await page.waitForTimeout(1800);
});
await flow('mentor', async (page) => {
  await page.goto('https://www.iveststudy.com/mentor', { waitUntil: 'networkidle' }); await page.waitForTimeout(1500);
  const rec = await page.rec(); await page.waitForTimeout(1200); rec.mark('empty');
  const inp = page.locator('textarea, input[type=text]').last(); await inp.click(); await page.keyboard.type('Qual a diferença entre Romantismo e Realismo?', { delay: 45 }); await page.waitForTimeout(500);
  const send = page.locator('button').filter({ hasText: /Enviar|Perguntar/ }).first(); rec.mark('send'); if (await send.count()) await send.click(); else await page.keyboard.press('Enter');
  for (let i = 0; i < 90; i++) { await sleep(300); const t = await txt(page); if (/Realismo/.test(t) && t.length > 1200) break; } rec.mark('answer');
  await page.waitForTimeout(3000); await still(page, 'mentor-answer'); await smoothScroll(page, 900, 2500); await page.waitForTimeout(1500);
});
await flow('quiz', async (page) => {
  await page.goto('https://www.iveststudy.com/app', { waitUntil: 'networkidle' }); await page.waitForTimeout(1200); await skipGuide(page);
  await tab(page, 'Quiz').click({ force: true }); await page.waitForTimeout(1300);
  await pickSubject(page, 'Geografia'); await diff(page, 'Fácil').click().catch(()=>{}); await page.waitForTimeout(300);
  await page.locator('button', { hasText: /^\s*Iniciar( →)?\s*$/ }).first().click(); await page.waitForTimeout(2500); await still(page, 'quiz-q');
  const snippet = (await ask('quiz', (await txt(page)).slice(0, 3000))).trim();
  const rec = await page.rec(); await page.waitForTimeout(1500); rec.mark('question');
  await page.getByText(snippet, { exact: false }).first().click(); rec.mark('tap'); await page.waitForTimeout(3000); await still(page, 'quiz-result'); await smoothScroll(page, 500, 1500); await page.waitForTimeout(1500);
});
await flow('home', async (page) => {
  await page.goto('https://www.iveststudy.com/app', { waitUntil: 'networkidle' }); await page.waitForTimeout(1500); await skipGuide(page);
  const rec = await page.rec(); await page.waitForTimeout(1200); rec.mark('top'); await smoothScroll(page, 1400, 3500); await page.waitForTimeout(1500);
});
await flow('signup', async (page) => {
  await page.goto('https://www.iveststudy.com/', { waitUntil: 'networkidle' }); await page.waitForTimeout(1500);
  const rec = await page.rec(); await page.waitForTimeout(1200); rec.mark('landing'); await smoothScroll(page, 500, 1800); await page.waitForTimeout(800);
  const cta = page.getByText(/Criar conta grátis/).first(); await cta.scrollIntoViewIfNeeded(); await page.waitForTimeout(500); rec.mark('tap'); await cta.click(); await page.waitForTimeout(2500); rec.mark('form'); await still(page, 'signup'); await page.waitForTimeout(1500);
}, { anon: true });
await browser.close(); console.log('ALL DONE 3');
