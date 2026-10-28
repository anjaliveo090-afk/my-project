// Offline renderer: drives index.html in headless Chromium frame by frame, then muxes
// the frames with the narration via ffmpeg.
//
//   node render.mjs                       # full video -> out/clock-tower.mp4
//   node render.mjs --stills 1.9,22.5     # PNG-ish stills at given seconds -> out/stills/
//   node render.mjs --from 20 --to 30     # render only a time range (preview cut)
//   options: --workers 4  --sub 3 (motion-blur sub-frames)  --fps 30  --out out
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

// Uses a local or globally installed Playwright (CommonJS resolution honours NODE_PATH).
const { chromium } = createRequire(import.meta.url)('playwright');

const root = path.dirname(fileURLToPath(import.meta.url));
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, all) => {
  if (v.startsWith('--')) a.push([v.slice(2), all[i + 1] && !all[i + 1].startsWith('--') ? all[i + 1] : true]);
  return a;
}, []));
const FPS = Number(args.fps || 30), DUR = 60.66;
const SUB = Number(args.sub || 3), WORKERS = Number(args.workers || 4);
const OUT = path.resolve(root, args.out || 'out');

const types = { '.html': 'text/html', '.js': 'text/javascript', '.woff2': 'font/woff2', '.mp3': 'audio/mpeg' };
const server = http.createServer((req, res) => {
  const p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': types[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const url = `http://127.0.0.1:${server.address().port}/index.html?render=1`;

const browser = await chromium.launch();
async function page() {
  const p = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.error('page error:', e.message));
  await p.goto(url);
  await p.waitForFunction(() => typeof window.renderFrame === 'function');
  return p;
}
const save = (file, dataUrl) => fs.writeFileSync(file, Buffer.from(dataUrl.split(',')[1], 'base64'));

if (args.stills) {
  const dir = path.join(OUT, 'stills'); fs.mkdirSync(dir, { recursive: true });
  const p = await page();
  for (const s of String(args.stills).split(',')) {
    const f = Math.round(Number(s) * FPS);
    save(path.join(dir, `t${Number(s).toFixed(2)}.jpg`), await p.evaluate(([f, sub]) => window.renderFrame(f, sub, 0.92), [f, SUB]));
  }
  console.log('stills ->', dir);
} else {
  const f0 = Math.round(Number(args.from || 0) * FPS), f1 = Math.min(Math.ceil(DUR * FPS), Math.round(Number(args.to || DUR) * FPS));
  const dir = path.join(OUT, 'frames'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  let done = 0; const t0 = Date.now();
  await Promise.all(Array.from({ length: WORKERS }, async (_, w) => {
    const p = await page();
    for (let f = f0 + w; f < f1; f += WORKERS) {
      save(path.join(dir, `f${String(f - f0).padStart(5, '0')}.jpg`), await p.evaluate(([f, sub]) => window.renderFrame(f, sub, 0.96), [f, SUB]));
      if (++done % 100 === 0) console.log(`${done}/${f1 - f0} frames, ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
  }));
  const name = args.from || args.to ? `clock-tower_${f0 / FPS}-${f1 / FPS}.mp4` : 'clock-tower.mp4';
  const mp4 = path.join(OUT, name);
  const r = spawnSync('ffmpeg', ['-y', '-v', 'error', '-framerate', String(FPS), '-i', path.join(dir, 'f%05d.jpg'),
    '-ss', String(f0 / FPS), '-t', String((f1 - f0) / FPS), '-i', path.join(root, 'assets/narration.mp3'),
    '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
    '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '192k', '-shortest', mp4], { stdio: 'inherit' });
  if (r.status !== 0) throw new Error('ffmpeg failed');
  console.log('video ->', mp4);
}
await browser.close(); server.close();
