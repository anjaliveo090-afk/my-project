// "The Clock Tower That Lied" — narration-driven motion graphics.
// Every frame is a pure function of time t (seconds), so the same code drives
// live preview (index.html) and the offline frame renderer (render.mjs).
(function () {
  'use strict';

  const W = 1080, H = 1920, DUR = 60.66;

  // ---------- palette ----------
  const C = {
    ink: '#0a0c11', ink2: '#12151d', ink3: '#1a1e29',
    paper: '#efe6d2', dim: '#5a6070',
    brass: '#e3a04a', brassHi: '#f6c779', brassLo: '#7a5524',
    red: '#e5482f', redHi: '#ff6a4d',
    cyan: '#9fdcff', cyanLo: '#2c5b78',
    pInk: '#1c1a16', pPaper: '#ebe2cd', pRule: '#b9ad92',
  };

  // ---------- math ----------
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const lerp = (a, b, k) => a + (b - a) * k;
  const prog = (t, a, b) => clamp((t - a) / (b - a));
  const TAU = Math.PI * 2;
  const E = {
    lin: k => k,
    out: k => 1 - Math.pow(1 - k, 3),
    outQ: k => 1 - Math.pow(1 - k, 5),
    in: k => k * k * k,
    inOut: k => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2),
    inOutQ: k => (k < 0.5 ? 16 * Math.pow(k, 5) : 1 - Math.pow(-2 * k + 2, 5) / 2),
    outExpo: k => (k >= 1 ? 1 : 1 - Math.pow(2, -10 * k)),
    inExpo: k => (k <= 0 ? 0 : Math.pow(2, 10 * k - 10)),
    outBack: k => { const c = 1.9; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); },
    inBack: k => { const c = 1.7; return (c + 1) * k * k * k - c * k * k; },
  };
  // fade-in/hold/fade-out envelope
  const env = (t, a, b, fi = 0.25, fo = 0.25) => Math.min(E.out(prog(t, a, a + fi)), 1 - E.inOut(prog(t, b - fo, b)));
  function rng(seed) {
    let s = seed >>> 0;
    return () => { s = (s + 0x6D2B79F5) >>> 0; let x = s; x = Math.imul(x ^ (x >>> 15), x | 1); x ^= x + Math.imul(x ^ (x >>> 7), x | 61); return ((x ^ (x >>> 14)) >>> 0) / 4294967296; };
  }
  function mixHex(a, b, k) {
    const pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16);
    const r = Math.round(lerp(pa >> 16, pb >> 16, k)), g = Math.round(lerp((pa >> 8) & 255, (pb >> 8) & 255, k)), bl = Math.round(lerp(pa & 255, pb & 255, k));
    return `rgb(${r},${g},${bl})`;
  }

  // ---------- cue lookup from the transcript ----------
  const WORDS = window.WORDS;
  const norm = s => s.toLowerCase().replace(/[^a-z0-9']/g, '');
  function cue(word, n = 0) {
    let k = 0;
    for (const w of WORDS) if (norm(w.w) === word && k++ === n) return w.s;
    throw new Error('cue not found: ' + word + ' #' + n);
  }
  const Q = {
    clock: cue('clock'), tower: cue('tower'), lied: cue('lied'), entire: cue('entire'), city: cue('city'),
    for10: cue('for'), nobody: cue('nobody'), noticed: cue('noticed'),
    yousee: cue('you'), back: cue('back'), nobody2: cue('nobody', 1), owned: cue('owned'), watch: cue('watch'),
    bell: cue('bell'), told: cue('told'), whole: cue('whole'), when: cue('when'), start: cue('start'),
    go: cue('go'), home: cue('home'), argues: cue('argues'), nobody3: cue('nobody', 2), bell2: cue('bell', 1),
    then: cue('then', 1), young: cue('young'), moved: cue('moved'), town: cue('town'), pocket: cue('pocket'),
    never: cue('never'), lost: cue('lost'), second: cue('second'),
    sat: cue('sat'), week: cue('week'), writing: cue('writing'), rang: cue('rang'),
    dawn: cue('dawn'), ran: cue('ran'), n20: cue('20'), fast: cue('fast'),
    dusk: cue('dusk'), n25: cue('25'), slow: cue('slow'),
    which: cue('which'), every: cue('every', 1), worker: cue('worker'), handing: cue('handing'),
    nearly: cue('nearly'), hour: cue('hour'), free: cue('free'), every2: cue('every', 2), single: cue('single'), day: cue('day'),
    so: cue('so', 1), foreman: cue('foreman'), laughed: cue('laughed'), so2: cue('so', 2), hard: cue('hard'),
    dropped: cue('dropped'), sandwich: cue('sandwich'),
    clocks: cue('clocks'), dont: cue("don't"), lie: cue('lie'), kid: cue('kid'),
    workers: cue('workers'), looked: cue('looked'), insulted: cue('insulted'), mothers: cue('mothers'),
    mayor: cue('mayor'), awkward: cue('awkward'), because: cue('because'), mayor2: cue('mayor', 1), owned2: cue('owned', 1), mill2: cue('mill', 2),
    smiled: cue('smiled'), listened: cue('listened'), number: cue('number'), asked: cue('asked'), question: cue('question'),
    whose: cue('whose'), wrong: cue('wrong'), son: cue('son'), yours: cue('yours'), mine: cue('mine'),
    by: cue('by'), friday: cue('friday'), left: cue('left'), only: cue('only'), honest: cue('honest'), clock2: cue('clock', 4), pocket2: cue('pocket', 1),
    real: cue('real'), factory: cue('factory'), inspectors: cue('inspectors'), y1800: cue('1800s'), england: cue('england'),
    reported: cue('reported'), turning: cue('turning'), forward: cue('forward'), morning: cue('morning'), backN: cue('back', 1), night: cue('night'),
    inA: cue('in', 5), city3: cue('city', 3), only2: cue('only', 1), one: cue('one', 1), clock3: cue('clock', 5),
    lie2: cue('lie', 1), becomes: cue('becomes'), time: cue('time', 1),
  };

  // ---------- fonts ----------
  const F = {
    serif: px => `${px}px "Instrument Serif"`,
    serifI: px => `italic ${px}px "Instrument Serif"`,
    black: px => `900 ${px}px "InterV"`,
    bold: px => `700 ${px}px "InterV"`,
    reg: px => `400 ${px}px "InterV"`,
    mono: px => `400 ${px}px "JBMono"`,
    monoB: px => `700 ${px}px "JBMono"`,
  };

  // ---------- text helpers ----------
  function setText(ctx, font, ls = 0, align = 'center') {
    ctx.font = font; ctx.letterSpacing = ls + 'px'; ctx.textAlign = align; ctx.textBaseline = 'alphabetic';
  }
  function text(ctx, s, x, y, font, color, alpha = 1, ls = 0, align = 'center') {
    if (alpha <= 0.001) return;
    ctx.save(); setText(ctx, font, ls, align); ctx.globalAlpha *= alpha; ctx.fillStyle = color; ctx.fillText(s, x, y); ctx.restore();
  }
  // Masked rise: text slides up from under its own baseline.
  function riseText(ctx, s, x, y, font, color, k, size, opts = {}) {
    if (k <= 0) return;
    const { ls = 0, align = 'center', alpha = 1, out = 0 } = opts;
    ctx.save(); setText(ctx, font, ls, align);
    const w = ctx.measureText(s).width;
    const x0 = align === 'center' ? x - w / 2 : align === 'right' ? x - w : x;
    ctx.beginPath(); ctx.rect(x0 - 40, y - size * 1.15, w + 80, size * 1.45); ctx.clip();
    const dy = (1 - E.outQ(k)) * size * 1.2 - E.inOut(out) * size * 1.2;
    ctx.globalAlpha *= alpha; ctx.fillStyle = color; ctx.fillText(s, x, y + dy);
    ctx.restore();
  }
  // Words revealed on their own spoken onsets: [{w, t, color?}]
  function spokenLine(ctx, items, x, y, font, color, t, opts = {}) {
    const { ls = 0, gap = null, alpha = 1, rise = 26, dur = 0.32, lead = 0.05 } = opts;
    ctx.save(); setText(ctx, font, ls, 'left');
    const sp = gap ?? ctx.measureText(' ').width;
    const ws = items.map(it => ctx.measureText(it.w).width);
    const total = ws.reduce((a, b) => a + b, 0) + sp * (items.length - 1);
    let cx = x - total / 2;
    items.forEach((it, i) => {
      const k = E.out(prog(t, it.t - lead, it.t - lead + dur));
      if (k > 0) {
        ctx.globalAlpha = alpha * k; ctx.fillStyle = it.color || color;
        ctx.fillText(it.w, cx, y + (1 - k) * rise);
      }
      cx += ws[i] + sp;
    });
    ctx.restore();
  }
  // Per-letter positions for custom animation.
  function letterLayout(ctx, s, x, font, ls = 0) {
    ctx.save(); setText(ctx, font, ls, 'left');
    const total = ctx.measureText(s).width - ls;
    const out = []; let acc = x - total / 2;
    for (let i = 0; i < s.length; i++) {
      const w = ctx.measureText(s[i]).width;
      out.push({ ch: s[i], x: acc, w });
      acc += w;
    }
    ctx.restore();
    return out;
  }

  // ---------- glow helper ----------
  function glow(ctx, x, y, r, color, a) {
    if (a <= 0) return;
    const g = ctx.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, color); g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.save(); ctx.globalAlpha *= a; ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = g;
    ctx.fillRect(x - r, y - r, r * 2, r * 2); ctx.restore();
  }

  // ---------- clock dial ----------
  // minutes: minute-hand value in minutes (0..60 = one turn), hours: hour-hand value in hours.
  function dial(ctx, o) {
    const { x, y, r, col = C.brass, reveal = 1, minutes = 0, hours = 0, seconds = null,
      numerals = true, lw = 3, alpha = 1, face = C.ink2, handCol = null, trail = 0, minuteCol = null,
      dimFrom = null, hideMinute = false, roman = true, secCol = null } = o;
    if (alpha <= 0 || reveal <= 0) return;
    ctx.save(); ctx.globalAlpha *= alpha; ctx.translate(x, y);
    // face
    if (face) {
      ctx.globalAlpha *= 1; ctx.fillStyle = face;
      ctx.beginPath(); ctx.arc(0, 0, r * E.out(clamp(reveal * 1.3)), 0, TAU); ctx.fill();
      ctx.globalAlpha = alpha;
    }
    ctx.strokeStyle = col; ctx.lineCap = 'round';
    // rings, drawn on clockwise from 12
    const ra = E.inOut(clamp(reveal));
    ctx.lineWidth = lw;
    ctx.beginPath(); ctx.arc(0, 0, r, -Math.PI / 2, -Math.PI / 2 + TAU * ra); ctx.stroke();
    ctx.lineWidth = lw * 0.5;
    ctx.beginPath(); ctx.arc(0, 0, r * 0.9, -Math.PI / 2, -Math.PI / 2 + TAU * ra); ctx.stroke();
    // ticks
    for (let i = 0; i < 60; i++) {
      const tk = clamp((reveal * 1.15 - i / 60 * 0.9) * 6);
      if (tk <= 0) continue;
      const a = i / 60 * TAU - Math.PI / 2, big = i % 5 === 0;
      const r1 = r * 0.9, r2 = r1 - (big ? r * 0.1 : r * 0.04) * E.outBack(tk);
      ctx.globalAlpha = alpha * (dimFrom !== null && i >= dimFrom ? 0.25 : 1);
      ctx.lineWidth = big ? lw * 0.9 : lw * 0.45;
      ctx.beginPath(); ctx.moveTo(Math.cos(a) * r1, Math.sin(a) * r1); ctx.lineTo(Math.cos(a) * r2, Math.sin(a) * r2); ctx.stroke();
    }
    ctx.globalAlpha = alpha;
    // numerals
    if (numerals) {
      const na = clamp((reveal - 0.55) / 0.45);
      if (na > 0) {
        const R = ['XII', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI'];
        ctx.save(); setText(ctx, F.serif(r * 0.15), 0, 'center'); ctx.textBaseline = 'middle'; ctx.fillStyle = col;
        for (let i = 0; i < 12; i++) {
          const a = i / 12 * TAU - Math.PI / 2;
          ctx.globalAlpha = alpha * na * (dimFrom !== null && i * 5 >= dimFrom ? 0.25 : 1);
          ctx.fillText(roman ? R[i] : String(i === 0 ? 12 : i), Math.cos(a) * r * 0.66, Math.sin(a) * r * 0.66 + r * 0.01);
        }
        ctx.restore();
      }
    }
    // hands
    const hk = clamp((reveal - 0.7) / 0.3);
    if (hk > 0) {
      const hc = handCol || col;
      const ma = minutes / 60 * TAU - Math.PI / 2, ha = hours / 12 * TAU - Math.PI / 2;
      ctx.globalAlpha = alpha * hk;
      if (trail > 0.02 && !hideMinute) {
        // angular smear behind a fast minute hand
        const steps = 24;
        for (let i = 1; i <= steps; i++) {
          const f = i / steps;
          ctx.globalAlpha = alpha * hk * (1 - f) * 0.18;
          ctx.strokeStyle = minuteCol || hc; ctx.lineWidth = lw * 1.4;
          const aa = ma - trail * f;
          ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(aa) * r * 0.78, Math.sin(aa) * r * 0.78); ctx.stroke();
        }
        ctx.globalAlpha = alpha * hk;
      }
      ctx.strokeStyle = hc; ctx.lineWidth = lw * 2.2;
      ctx.beginPath(); ctx.moveTo(-Math.cos(ha) * r * 0.08, -Math.sin(ha) * r * 0.08); ctx.lineTo(Math.cos(ha) * r * 0.48, Math.sin(ha) * r * 0.48); ctx.stroke();
      if (!hideMinute) {
        ctx.strokeStyle = minuteCol || hc; ctx.lineWidth = lw * 1.4;
        ctx.beginPath(); ctx.moveTo(-Math.cos(ma) * r * 0.12, -Math.sin(ma) * r * 0.12); ctx.lineTo(Math.cos(ma) * r * 0.78, Math.sin(ma) * r * 0.78); ctx.stroke();
      }
      if (seconds !== null) {
        const sa = seconds / 60 * TAU - Math.PI / 2;
        ctx.strokeStyle = secCol || C.red; ctx.lineWidth = lw * 0.6;
        ctx.beginPath(); ctx.moveTo(-Math.cos(sa) * r * 0.18, -Math.sin(sa) * r * 0.18); ctx.lineTo(Math.cos(sa) * r * 0.84, Math.sin(sa) * r * 0.84); ctx.stroke();
      }
      ctx.fillStyle = hc; ctx.beginPath(); ctx.arc(0, 0, lw * 2.2, 0, TAU); ctx.fill();
    }
    ctx.restore();
  }
  function wedge(ctx, x, y, r, m0, m1, color, alpha, edge = true) {
    if (alpha <= 0 || Math.abs(m1 - m0) < 0.01) return;
    const a0 = m0 / 60 * TAU - Math.PI / 2, a1 = m1 / 60 * TAU - Math.PI / 2;
    ctx.save(); ctx.globalAlpha *= alpha;
    ctx.fillStyle = color; ctx.globalAlpha *= 0.42;
    ctx.beginPath(); ctx.moveTo(x, y); ctx.arc(x, y, r, a0, a1, m1 < m0); ctx.closePath(); ctx.fill();
    ctx.globalAlpha /= 0.42;
    if (edge) {
      ctx.strokeStyle = color; ctx.lineWidth = 6; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.arc(x, y, r, a0, a1, m1 < m0); ctx.stroke();
    }
    ctx.restore();
  }
  // Honest pocket watch: steel case, bow, crown, ticking second hand.
  function pocketWatch(ctx, x, y, r, t, alpha = 1, reveal = 1) {
    if (alpha <= 0) return;
    ctx.save(); ctx.globalAlpha *= alpha;
    // bow and crown
    ctx.strokeStyle = C.cyan; ctx.lineWidth = Math.max(2, r * 0.025);
    const bk = E.outBack(prog(reveal, 0.5, 1));
    if (bk > 0) {
      ctx.fillStyle = C.cyan;
      ctx.fillRect(x - r * 0.07, y - r - r * 0.13 * bk, r * 0.14, r * 0.14 * bk);
      ctx.beginPath(); ctx.ellipse(x, y - r - r * 0.24 * bk, r * 0.15 * bk, r * 0.12 * bk, 0, 0, TAU); ctx.stroke();
    }
    // honest seconds: one discrete tick per real second, with a small settle
    const s = Math.floor(t), f = t - s;
    const sec = (s + E.outBack(clamp(f / 0.12)) - 1) % 60 + 1;
    dial(ctx, { x, y, r, col: C.cyan, reveal, minutes: 7, hours: 5 + 7 / 60, seconds: sec * 1 + 0, lw: Math.max(1.5, r * 0.016), face: '#0b131b', secCol: C.paper, roman: false });
    ctx.restore();
  }

  // ---------- world: tower, mill, city ----------
  const TOWER = { x: 540, y: 820, r: 150 }, GROUND = 1450;
  const city = (() => {
    const R = rng(7), back = [], front = [];
    let x = -520;
    while (x < 1620) { const w = 70 + R() * 90, h = 130 + R() * 230; back.push({ x, w, h, gable: R() < 0.35 }); x += w + 6 + R() * 18; }
    x = -560;
    while (x < 1660) {
      const w = 80 + R() * 110, h = 70 + R() * 170;
      if (!(x + w > 300 && x < 960)) front.push({ x, w, h, gable: R() < 0.5 });
      x += w + 10 + R() * 30;
    }
    const wins = [];
    for (const [layer, list] of [[0, back], [1, front]]) for (const b of list) {
      const cols = Math.max(1, Math.floor((b.w - 20) / 26)), rows = Math.max(1, Math.floor((b.h - 30) / 38));
      for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) if (R() < 0.55) {
        const wx = b.x + 14 + i * ((b.w - 28) / Math.max(1, cols - 1 || 1)) - 5, wy = GROUND - b.h + 26 + j * 38;
        wins.push({ layer, x: cols === 1 ? b.x + b.w / 2 - 5 : wx, y: wy, ph: R(), d: Math.hypot(wx - TOWER.x, wy - TOWER.y) });
      }
    }
    return { back, front, wins };
  })();

  function towerShape(ctx, k = 1) {
    // housing + roof + shaft; k grows the shaft downward
    const { x, y, r } = TOWER;
    const hw = r * 1.27, top = y - r * 1.27, bot = y + r * 1.27;
    ctx.beginPath();
    ctx.moveTo(x, top - r * 1.15); ctx.lineTo(x + hw + 14, top); ctx.lineTo(x - hw - 14, top); ctx.closePath();
    ctx.rect(x - hw, top, hw * 2, bot - top);
    const sb = lerp(bot, GROUND, k);
    if (k > 0) ctx.rect(x - r * 0.82, bot, r * 1.64, sb - bot);
    return { top, bot, sb, hw };
  }
  function drawTower(ctx, col, k, alpha = 1, fill = C.ink2) {
    if (alpha <= 0) return;
    ctx.save(); ctx.globalAlpha *= alpha;
    const { x, r } = TOWER;
    const g = towerShape(ctx, k);
    ctx.fillStyle = fill; ctx.fill();
    ctx.strokeStyle = col; ctx.lineWidth = 3; ctx.lineJoin = 'miter'; ctx.stroke();
    // spire
    ctx.beginPath(); ctx.moveTo(x, g.top - r * 1.15); ctx.lineTo(x, g.top - r * 1.55); ctx.stroke();
    // shaft slits
    if (k > 0.05) {
      ctx.lineWidth = 2;
      for (let i = 0; i < 4; i++) {
        const sy = g.bot + 50 + i * 95; if (sy + 50 > g.sb) break;
        ctx.strokeRect(x - 12, sy, 24, 50);
      }
      // cornice
      ctx.beginPath(); ctx.moveTo(x - r * 0.95, g.bot + 14); ctx.lineTo(x + r * 0.95, g.bot + 14); ctx.stroke();
    }
    ctx.restore();
  }
  function drawMill(ctx, col, alpha, rise = 1) {
    if (alpha <= 0) return;
    ctx.save(); ctx.globalAlpha *= alpha; ctx.translate(0, (1 - rise) * 260);
    ctx.fillStyle = C.ink2; ctx.strokeStyle = col; ctx.lineWidth = 2.5;
    // saw-tooth roof mill, right of the tower
    const x0 = 700, x1 = 1010, top = GROUND - 170;
    ctx.beginPath(); ctx.moveTo(x0, GROUND); ctx.lineTo(x0, top);
    for (let i = 0; i < 5; i++) { const a = x0 + i * 62; ctx.lineTo(a + 50, top - 42); ctx.lineTo(a + 62, top); }
    ctx.lineTo(x1, GROUND); ctx.closePath(); ctx.fill(); ctx.stroke();
    // chimney
    ctx.beginPath(); ctx.rect(940, GROUND - 400, 38, 230); ctx.fill(); ctx.stroke();
    ctx.restore();
  }
  function drawCity(ctx, t, o) {
    const { col = C.brass, alpha = 1, rise = 1, lit = null, winCol = C.brass, layerAlpha = [0.5, 1] } = o;
    if (alpha <= 0) return;
    ctx.save(); ctx.globalAlpha *= alpha;
    [city.back, city.front].forEach((list, L) => {
      list.forEach((b, i) => {
        const rk = E.outQ(clamp(rise * 1.6 - (i % 7) * 0.08 - L * 0.15));
        if (rk <= 0) return;
        const dy = (1 - rk) * (b.h + 60);
        ctx.save(); ctx.globalAlpha *= layerAlpha[L]; ctx.translate(0, dy);
        ctx.fillStyle = L ? C.ink2 : C.ink; ctx.strokeStyle = col; ctx.lineWidth = L ? 2.2 : 1.5;
        ctx.beginPath();
        if (b.gable) { ctx.moveTo(b.x, GROUND); ctx.lineTo(b.x, GROUND - b.h); ctx.lineTo(b.x + b.w / 2, GROUND - b.h - b.w * 0.35); ctx.lineTo(b.x + b.w, GROUND - b.h); ctx.lineTo(b.x + b.w, GROUND); }
        else ctx.rect(b.x, GROUND - b.h, b.w, b.h);
        ctx.fill(); ctx.stroke(); ctx.restore();
      });
    });
    // windows
    if (lit) {
      for (const w of city.wins) {
        const lk = lit(w);
        if (lk <= 0) continue;
        const b = (w.layer ? city.front : city.back);
        ctx.globalAlpha = alpha * lk * (w.layer ? 1 : 0.55) * clamp(rise * 1.6 - 0.4);
        ctx.fillStyle = winCol; ctx.fillRect(w.x, w.y, 10, 15);
      }
    }
    ctx.restore();
  }
  function ground(ctx, col, alpha) {
    ctx.save(); ctx.globalAlpha *= alpha; ctx.fillStyle = C.ink; ctx.fillRect(-2000, GROUND, 5000, 3000);
    ctx.strokeStyle = col; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(-2000, GROUND); ctx.lineTo(3000, GROUND); ctx.stroke(); ctx.restore();
  }

  // ---------- camera ----------
  // keys: [t, wx, wy, scale, sx, sy, ease]
  function camAt(keys, t) {
    if (t <= keys[0][0]) return keys[0];
    for (let i = 1; i < keys.length; i++) {
      if (t <= keys[i][0]) {
        const a = keys[i - 1], b = keys[i], ez = E[b[6] || 'inOut'];
        const k = ez(prog(t, a[0], b[0]));
        // interpolate scale geometrically for natural zooms
        const s = Math.exp(lerp(Math.log(a[3]), Math.log(b[3]), k));
        return [t, lerp(a[1], b[1], k), lerp(a[2], b[2], k), s, lerp(a[4], b[4], k), lerp(a[5], b[5], k)];
      }
    }
    return keys[keys.length - 1];
  }
  function applyCam(ctx, c) { ctx.translate(c[4], c[5]); ctx.scale(c[3], c[3]); ctx.translate(-c[1], -c[2]); }

  // world camera for the opening (0–13.4) and the pocket-watch approach (13.4–15.5)
  const camA = [
    [0, 540, 820, 1.75, 540, 960],
    [Q.tower + 0.2, 540, 860, 1.25, 540, 900, 'inOut'],
    [Q.city + 0.2, 540, 1000, 1.0, 540, 1080, 'inOut'],
    [Q.for10 - 0.05, 540, 1000, 1.0, 540, 1080],
    [Q.for10 + 0.6, 540, 820, 2.9, 540, 880, 'inOutQ'],
    [Q.yousee, 540, 820, 3.05, 540, 880, 'lin'],
    [Q.yousee + 1.25, 560, 1010, 0.88, 540, 1060, 'inOutQ'],
    [Q.bell2 + 0.6, 560, 1010, 0.96, 540, 1060, 'lin'],
    [Q.town - 0.2, 660, 1150, 1.05, 540, 1060, 'inOut'],
    [Q.pocket + 0.35, 790, 1430, 5.5, 540, 860, 'inQ'],
  ];
  E.inQ = k => k * k * k * k;

  // tower clock time in minutes (minute hand); hour hand follows
  function towerMinutes(t) {
    let m = 6 * 60 + 58 + t * 0.3;
    m += 20 * E.outBack(prog(t, Q.lied - 0.03, Q.lied + 0.17));
    m += 18 * 60 * E.inOutQ(prog(t, Q.for10 + 0.05, Q.noticed + 0.3));
    return m;
  }

  // ---------- scene: world (0 – 15.6) ----------
  const watches = (() => {
    const R = rng(21), out = [];
    const spots = [[150, 420], [930, 380], [250, 650], [860, 640], [120, 900], [960, 900], [330, 300], [760, 260],
      [200, 1180], [880, 1170], [420, 1240], [680, 1250], [80, 1320], [1000, 1320]];
    spots.forEach(([x, y], i) => out.push({ x, y, r: 26 + R() * 18, inT: Q.back + i * 0.04, outT: Q.nobody2 + (i / spots.length) * (Q.watch - Q.nobody2 + 0.2), m: R() * 60, h: R() * 12 }));
    return out;
  })();

  function sceneWorld(ctx, t, warm = false) {
    if (t > Q.pocket + 0.8) return;
    const cam = camAt(camA, t);
    const cool = warm ? 0 : (t >= Q.bell2 ? 1 : 0); // palette swap happens behind the iris
    const col = cool > 0 ? mixHex(C.brass, '#6fa9cf', cool) : C.brass;
    ctx.save(); applyCam(ctx, cam);

    // sky glow behind tower
    glow(ctx, TOWER.x, TOWER.y, 900, cool > 0.5 ? 'rgba(60,110,160,0.35)' : 'rgba(227,160,74,0.22)', E.out(prog(t, 0.2, 2.0)));

    const riseCity = prog(t, Q.entire - 0.15, Q.city + 0.6);
    // bell wave lights the windows
    const bellR = t2 => (t2 < Q.bell ? -1 : 1500 * E.out(prog(t2, Q.bell, Q.bell + 1.7)));
    const lit = w => {
      const base = 0.18 + 0.1 * Math.sin(w.ph * 40);
      const rr = bellR(t);
      const k = rr < 0 ? 0 : clamp((rr - w.d) / 90);
      return lerp(base, 1, k) * (1 - 0.6 * cool) + cool * 0.25;
    };
    drawCity(ctx, t, { col, rise: riseCity, lit, winCol: cool > 0.5 ? '#bfe6ff' : C.brassHi });
    drawMill(ctx, col, 1, E.outQ(prog(t, Q.entire, Q.city + 0.5)));
    // tower grows from its clock
    const tk = E.inOut(prog(t, Q.clock + 0.1, Q.lied));
    drawTower(ctx, col, tk, E.out(prog(t, Q.clock - 0.25, Q.clock + 0.3)));
    ground(ctx, col, E.out(prog(t, Q.entire - 0.1, Q.city + 0.3)));

    // the dial itself
    const m = towerMinutes(t);
    const dm = (towerMinutes(t + 0.01) - towerMinutes(t - 0.01)) / 0.02; // minutes per second
    const trail = Math.min(5.5, Math.abs(dm) / 60 * TAU * 0.05);
    const liedFlash = Math.exp(-Math.max(0, t - Q.lied) * 5) * (t >= Q.lied - 0.03 ? 1 : 0);
    dial(ctx, {
      x: TOWER.x, y: TOWER.y, r: TOWER.r, col: liedFlash > 0.05 ? mixHex(col, C.red, liedFlash) : col,
      reveal: E.inOut(prog(t, 0.0, 1.25)), minutes: m, hours: m / 60, lw: 3.2, trail,
      minuteCol: liedFlash > 0.05 ? mixHex(col, C.red, Math.min(1, liedFlash * 1.5)) : null,
    });
    glow(ctx, TOWER.x, TOWER.y, 260, 'rgba(229,72,47,0.6)', liedFlash * 0.9);

    // bell rings
    for (const [bt, n] of [[Q.bell, 3], [Q.bell2, 1]]) {
      for (let i = 0; i < n; i++) {
        const k = prog(t, bt + i * 0.22, bt + i * 0.22 + 1.8);
        if (k <= 0 || k >= 1) continue;
        ctx.save(); ctx.strokeStyle = col; ctx.globalAlpha = (1 - k) * 0.8; ctx.lineWidth = 4 * (1 - k) + 1;
        ctx.beginPath(); ctx.arc(TOWER.x, TOWER.y, TOWER.r + E.out(k) * 1400, 0, TAU); ctx.stroke(); ctx.restore();
      }
    }

    // the clock maker: a single cool point walking into town
    const mk = prog(t, Q.then - 0.1, Q.town + 0.3);
    if (t > Q.then - 0.3) {
      const mx = lerp(1300, 790, E.inOut(mk)), my = 1430 + Math.abs(Math.sin(mk * 26)) * -6 * (1 - mk);
      const ma = E.out(prog(t, Q.then - 0.3, Q.then + 0.2));
      glow(ctx, mx, my, 70, 'rgba(159,220,255,0.7)', ma);
      ctx.save(); ctx.globalAlpha = ma; ctx.fillStyle = C.cyan; ctx.beginPath(); ctx.arc(mx, my, 9, 0, TAU); ctx.fill(); ctx.restore();
    }
    ctx.restore();

    // a sky full of watches nobody owned — pop in, then out, one by one
    for (const w of watches) {
      const ki = E.outBack(prog(t, w.inT, w.inT + 0.3)), ko = E.inBack(prog(t, w.outT, w.outT + 0.22));
      const k = ki * (1 - ko);
      if (k <= 0.001) continue;
      dial(ctx, { x: w.x, y: w.y, r: w.r * k, col: C.paper, reveal: 1, minutes: w.m + t * 3, hours: w.h, numerals: false, lw: 1.6, alpha: 0.85, face: C.ink });
    }
  }
  // the tower dial's screen-space position under camA (for text placement and the iris)
  function towerScreen(t) { const c = camAt(camA, t); return { x: (TOWER.x - c[1]) * c[3] + c[4], y: (TOWER.y - c[2]) * c[3] + c[5], s: c[3] }; }

  // ---------- split-flap board ----------
  const FLAP_CH = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  function flapBoard(ctx, t, x, y, n, states, alpha) {
    if (alpha <= 0) return;
    const cw = 88, ch = 128, gap = 8, total = n * cw + (n - 1) * gap;
    ctx.save(); ctx.globalAlpha *= alpha;
    for (let i = 0; i < n; i++) {
      const cx = x - total / 2 + i * (cw + gap);
      // find current transition for this cell
      let from = ' ', to = ' ', k = 1;
      for (const st of states) {
        const t0 = st.t + i * 0.025;
        if (t >= t0) { from = to; to = st.s[i] || ' '; k = prog(t, t0, t0 + 0.16); }
      }
      cell(ctx, cx, y, cw, ch, from, to, k);
    }
    ctx.restore();
  }
  function cell(ctx, x, y, w, h, from, to, k) {
    const mid = y + h / 2;
    const drawHalf = (ch, top, scaleY = 1) => {
      ctx.save();
      ctx.beginPath(); ctx.rect(x, top ? y : mid, w, h / 2); ctx.clip();
      ctx.translate(0, mid); ctx.scale(1, scaleY); ctx.translate(0, -mid);
      ctx.fillStyle = top ? C.ink3 : '#161a24'; ctx.fillRect(x, y, w, h);
      if (ch !== ' ') { setText(ctx, F.monoB(96), 0, 'center'); ctx.textBaseline = 'middle'; ctx.fillStyle = C.brassHi; ctx.fillText(ch, x + w / 2, mid + 4); }
      if (scaleY < 1) { ctx.fillStyle = `rgba(0,0,0,${(1 - Math.abs(scaleY)) * 0.5})`; ctx.fillRect(x, y, w, h); }
      ctx.restore();
    };
    if (k >= 1 || from === to) { drawHalf(to, true); drawHalf(to, false); }
    else if (k < 0.5) { drawHalf(to, true); drawHalf(from, false); drawHalf(from, true, 1 - k * 2); }
    else { drawHalf(to, true); drawHalf(from, false); drawHalf(to, false, (k - 0.5) * 2); }
    ctx.fillStyle = C.ink; ctx.fillRect(x, mid - 1.5, w, 3);
  }

  // ---------- scene text over the world ----------
  function textWorld(ctx, t) {
    // hook
    const hookOut = E.inOut(prog(t, Q.for10 - 0.15, Q.for10 + 0.25));
    const hookA = 1 - hookOut;
    if (hookA > 0 && t < Q.for10 + 0.4) {
      spokenLine(ctx, [{ w: 'a', t: 0.94 }, { w: 'clock', t: Q.clock }, { w: 'tower', t: Q.tower }, { w: 'that', t: Q.tower + 0.36 }], 540, 150, F.serifI(70), C.paper, t, { alpha: hookA });
      const lk = prog(t, Q.lied - 0.04, Q.lied + 0.28);
      if (lk > 0) {
        const s = lerp(1.5, 1, E.outExpo(lk));
        ctx.save(); ctx.translate(540, 410 - hookOut * 40); ctx.scale(s, s);
        ctx.shadowColor = 'rgba(229,72,47,0.55)'; ctx.shadowBlur = 40 * (1 - lk * 0.6);
        text(ctx, 'LIED', 0, 0, F.black(250), C.red, Math.min(1, lk * 3) * hookA, -6);
        ctx.restore();
      }
    }
    // "nobody noticed."
    const nn = env(t, Q.nobody - 0.05, Q.yousee + 0.5, 0.3, 0.45);
    if (nn > 0) spokenLine(ctx, [{ w: 'nobody', t: Q.nobody }, { w: 'noticed.', t: Q.noticed }], 540, 1430, F.serifI(84), C.paper, t, { alpha: nn });
    // split-flap: START WORK -> GO HOME
    const fa = env(t, Q.when - 0.25, Q.argues - 0.1, 0.3, 0.35);
    if (fa > 0) {
      flapBoard(ctx, t, 540, 210 - (1 - fa) * 30, 10, [
        { t: Q.when - 0.25, s: '          ' },
        { t: Q.start - 0.08, s: 'START WORK' },
        { t: Q.go - 0.08, s: ' GO  HOME ' },
      ], fa);
    }
    const na = env(t, Q.nobody3 - 0.1, Q.bell2 + 0.75, 0.25, 0.4);
    if (na > 0) spokenLine(ctx, [{ w: 'and', t: Q.nobody3 - 0.1 }, { w: 'nobody', t: Q.nobody3 }, { w: 'argues', t: Q.argues }, { w: 'with', t: Q.argues + 0.4 }, { w: 'a', t: Q.bell2 - 0.12 }, { w: 'bell.', t: Q.bell2, color: C.brassHi }], 540, 290, F.serifI(80), C.paper, t, { alpha: na });
  }

  // ---------- scene: pocket watch + ledger (15 – 21) ----------
  function sceneWatch(ctx, t) {
    if (t < Q.pocket - 0.25 || t > Q.dawn + 0.9) return;
    // the walking point becomes the watch (match zoom)
    const k = E.inOutQ(prog(t, Q.pocket - 0.2, Q.pocket + 0.45));
    const p0 = (() => { const c = camAt(camA, Math.min(t, Q.pocket + 0.35)); return { x: (790 - c[1]) * c[3] + c[4], y: (1430 - c[2]) * c[3] + c[5], r: 9 * c[3] }; })();
    // then the watch tucks into the corner for the ledger, then returns for the reveal
    const toCorner = E.inOutQ(prog(t, Q.sat - 0.15, Q.sat + 0.5));
    const back = E.inOutQ(prog(t, Q.dawn - 0.35, Q.dawn + 0.45));
    let x = lerp(p0.x, 540, k), y = lerp(p0.y, 860, k), r = lerp(p0.r, 250, k);
    x = lerp(x, 210, toCorner); y = lerp(y, 330, toCorner); r = lerp(r, 105, toCorner);
    x = lerp(x, 540, back); y = lerp(y, 880, back); r = lerp(r, 262, back);
    const a = 1 - prog(t, Q.dawn + 0.4, Q.dawn + 0.8);
    glow(ctx, x, y, r * 2.2, 'rgba(110,190,255,0.35)', k * a);
    pocketWatch(ctx, x, y, r, t, a, clamp(0.15 + k));

    // "NEVER LOST A SECOND."
    const na = env(t, Q.never - 0.1, Q.sat + 0.2, 0.2, 0.3);
    if (na > 0) {
      spokenLine(ctx, [{ w: 'NEVER', t: Q.never }, { w: 'LOST', t: Q.lost }, { w: 'A', t: Q.second - 0.16 }, { w: 'SECOND.', t: Q.second }], 540, 1290, F.monoB(62), C.cyan, t, { alpha: na, ls: 4, rise: 0, dur: 0.08 });
    }

    // ledger: a week of bells, tallied
    const la = env(t, Q.sat, Q.dawn + 0.2, 0.3, 0.4);
    if (la > 0) {
      const days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'];
      const x0 = 150, cw = 130, y0 = 640;
      ctx.save(); ctx.globalAlpha = la;
      // rules
      ctx.strokeStyle = C.cyanLo; ctx.lineWidth = 1.5;
      const rk = E.inOut(prog(t, Q.sat, Q.week));
      ctx.beginPath(); ctx.moveTo(90, y0 + 30); ctx.lineTo(90 + 900 * rk, y0 + 30); ctx.stroke();
      for (let i = 0; i <= 7; i++) { const lx = 85 + i * cw; ctx.beginPath(); ctx.moveTo(lx, y0 - 60); ctx.lineTo(lx, y0 - 60 + 700 * rk); ctx.stroke(); }
      days.forEach((d, i) => {
        const dk = E.out(prog(t, Q.week - 0.25 + i * 0.05, Q.week + i * 0.05));
        text(ctx, d, x0 + i * cw, y0 + (1 - dk) * 20, F.mono(34), C.cyan, dk, 3);
      });
      // tally marks: 4 rings per day, the last lands on "rang"
      const N = 28, t0 = Q.writing - 0.05, t1 = Q.rang;
      for (let n = 0; n < N; n++) {
        const tt = lerp(t0, t1, n / (N - 1));
        const mk = E.out(prog(t, tt, tt + 0.1));
        if (mk <= 0) continue;
        const d = Math.floor(n / 4), j = n % 4;
        const cx = x0 + d * cw - 30 + j * 20, ty = y0 + 90;
        ctx.strokeStyle = C.paper; ctx.lineWidth = 4; ctx.lineCap = 'round';
        ctx.beginPath(); ctx.moveTo(cx, ty); ctx.lineTo(cx + (j % 2 ? 3 : -2), ty + 90 * mk); ctx.stroke();
        // each bell gets a small ring stamp under its mark
        if (j === 3) {
          const rr = E.outBack(prog(t, tt, tt + 0.25));
          ctx.strokeStyle = C.brass; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.arc(x0 + d * cw, ty + 160, 18 * rr, 0, TAU); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(x0 + d * cw, ty + 160); ctx.lineTo(x0 + d * cw, ty + 160 - 12 * rr); ctx.stroke();
        }
      }
      ctx.restore();
    }
  }

  // ---------- scene: the reveal (20.6 – 30.4) ----------
  const DX = 540, DY = 880, DR = 300;
  const workersX = [130, 230, 330, 430, 540, 650, 750, 850, 950];
  const particles = (() => {
    const R = rng(99), out = [];
    workersX.forEach((wx, wi) => {
      for (let j = 0; j < 16; j++) {
        const m = R() * 45, rr = DR * (0.25 + R() * 0.68);
        const arrive = Q.handing + 0.15 + (m / 45) * 0.85 + R() * 0.12;
        out.push({ wx, wy: 1300, m, rr, arrive, start: arrive - 0.75 - R() * 0.15, cx: lerp(wx, DX, 0.5) + (R() - 0.5) * 300, cy: 1250 - R() * 500, s: 3 + R() * 4 });
      }
    });
    return out;
  })();
  const grid = (() => { const out = []; for (let j = 0; j < 7; j++) for (let i = 0; i < 5; i++) out.push({ x: 540 + (i - 2) * 190, y: 560 + j * 158, n: j * 5 + i }); return out; })();

  function sceneReveal(ctx, t) {
    if (t < Q.dawn - 0.4 || t > Q.foreman + 0.2) return;
    const shrink = E.inOutQ(prog(t, Q.every2 - 0.2, Q.every2 + 0.3));
    const dusk = E.inOut(prog(t, Q.dusk - 0.2, Q.dusk + 0.9));
    const showA = E.out(prog(t, Q.dawn - 0.2, Q.dawn + 0.5));

    // sky: dawn -> dusk; sun rises, then sets, behind the dial
    const horizon = 1330;
    const sky = ctx.createLinearGradient(0, 300, 0, horizon);
    sky.addColorStop(0, C.ink); sky.addColorStop(1, dusk > 0 ? mixHex('#3a2a1c', '#3b1f35', dusk) : '#3a2a1c');
    ctx.save(); ctx.globalAlpha = showA * (1 - shrink); ctx.fillStyle = sky; ctx.fillRect(0, 0, W, horizon);
    const sunUp = E.inOut(prog(t, Q.dawn - 0.1, Q.ran + 0.4)), sunDown = E.inOut(prog(t, Q.dusk - 0.1, Q.n25 + 0.3));
    const sunY = lerp(horizon + 160, 420, sunUp * (1 - sunDown)) + sunDown * 0;
    const sy = sunDown > 0 ? lerp(420, horizon + 160, sunDown) : sunY;
    const sunCol = dusk > 0 ? mixHex('#ffd79a', '#ff8a5c', dusk) : '#ffd79a';
    ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, horizon); ctx.clip();
    glow(ctx, 860, sy, 380, dusk > 0.5 ? 'rgba(255,120,80,0.45)' : 'rgba(255,200,120,0.45)', 1);
    ctx.fillStyle = sunCol; ctx.beginPath(); ctx.arc(860, sy, 70, 0, TAU); ctx.fill();
    ctx.restore();
    ctx.strokeStyle = C.brassLo; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(0, horizon); ctx.lineTo(W, horizon); ctx.stroke();
    ctx.fillStyle = C.ink; ctx.fillRect(0, horizon + 1, W, H);
    ctx.restore();

    // labels for the time of day
    text(ctx, 'DAWN', 70, horizon - 24, F.mono(32), C.brass, env(t, Q.dawn, Q.dusk, 0.3, 0.3) * (1 - shrink), 6, 'left');
    text(ctx, 'DUSK', 70, horizon - 24, F.mono(32), '#ff9a7a', env(t, Q.dusk, Q.which + 0.4, 0.3, 0.3), 6, 'left');

    // dial geometry (big, then shrinks into the first calendar cell)
    const g0 = grid[0];
    const x = lerp(DX, g0.x, shrink), y = lerp(DY, g0.y, shrink), r = lerp(DR, 70, shrink);
    const out = E.inBack(prog(t, Q.so, Q.so + 0.35));

    // minute-hand offsets (tower vs truth)
    const fast = 20 * E.out(prog(t, Q.n20, Q.n20 + 0.45)) * (1 - E.inOut(prog(t, Q.dusk - 0.1, Q.dusk + 0.3)));
    const slow = -25 * E.out(prog(t, Q.n25, Q.n25 + 0.5));
    const merge = E.inOutQ(prog(t, Q.which, Q.which + 0.7));
    const towerOff = fast + slow;
    const handsA = 1 - merge;

    if (r * (1 - out) > 1) {
      const rr = r * (1 - out);
      dial(ctx, { x, y, r: rr, col: C.brass, reveal: E.inOut(prog(t, Q.dawn - 0.3, Q.dawn + 0.6)), minutes: 0, hours: 6, hideMinute: true, lw: 3 * rr / DR + 1, dimFrom: t > Q.nearly - 0.05 ? 45 : null });
      // wedges
      if (merge <= 0) {
        if (fast > 0.05) wedge(ctx, x, y, rr * 0.88, 0, fast, C.red, 1);
        if (slow < -0.05) wedge(ctx, x, y, rr * 0.88, slow, 0, C.red, 1);
      } else {
        // the morning 20 and the evening 25 join into one 45-minute bite
        const a = 1;
        wedge(ctx, x, y, rr * 0.88, 0, 20 * merge, C.red, a);
        wedge(ctx, x, y, rr * 0.88, lerp(-25, 20, merge), lerp(0, 45, merge), C.red, a);
      }
      // hands: brass = tower, cyan = truth
      if (handsA > 0) {
        ctx.save(); ctx.globalAlpha = handsA;
        const hand = (m, c, w, len) => { const a = m / 60 * TAU - Math.PI / 2; ctx.strokeStyle = c; ctx.lineWidth = w; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + Math.cos(a) * rr * len, y + Math.sin(a) * rr * len); ctx.stroke(); };
        hand(0, C.cyan, 6, 0.8);
        hand(towerOff, C.brassHi, 9, 0.78);
        ctx.fillStyle = C.brassHi; ctx.beginPath(); ctx.arc(x, y, 9, 0, TAU); ctx.fill();
        ctx.restore();
      }
      // pulse when the 45 minutes are named
      const pulse = Math.exp(-Math.max(0, t - Q.nearly) * 3) * (t > Q.nearly ? 1 : 0);
      glow(ctx, x, y, rr * 1.4, 'rgba(229,72,47,0.5)', pulse * (1 - shrink));
    }
    // offset labels
    const fl = env(t, Q.n20, Q.dusk, 0.2, 0.3);
    text(ctx, '+20 MIN', DX + 250, DY - 320, F.monoB(44), C.red, fl, 2, 'center');
    const sl = env(t, Q.n25, Q.which + 0.3, 0.2, 0.3);
    text(ctx, '−25 MIN', DX - 250, DY - 320, F.monoB(44), C.red, sl, 2, 'center');
    const ml = env(t, Q.hour - 0.1, Q.every2, 0.2, 0.25);
    text(ctx, '45 MIN', DX - 230, DY - 300, F.monoB(48), C.red, ml, 2, 'center');

    // workers along the horizon, each handing time up to the tower
    const wa = env(t, Q.every - 0.05, Q.every2 + 0.2, 0.3, 0.35);
    if (wa > 0) {
      workersX.forEach((wx, i) => {
        const k = E.outBack(prog(t, Q.every + i * 0.04, Q.every + i * 0.04 + 0.35));
        if (k <= 0) return;
        ctx.save(); ctx.globalAlpha = wa; ctx.translate(wx, 1330); ctx.scale(k, k);
        ctx.fillStyle = C.paper; ctx.beginPath(); ctx.arc(0, -78, 17, 0, TAU); ctx.fill();
        ctx.beginPath(); ctx.roundRect(-16, -56, 32, 56, [14, 14, 2, 2]); ctx.fill();
        ctx.restore();
      });
      for (const p of particles) {
        const k = prog(t, p.start, p.arrive);
        if (k <= 0 || k >= 1) continue;
        const e = E.inOut(k);
        const a = p.m / 60 * TAU - Math.PI / 2;
        const tx = DX + Math.cos(a) * p.rr, ty = DY + Math.sin(a) * p.rr;
        const sx = p.wx, sy = 1240;
        const bx = (1 - e) * (1 - e) * sx + 2 * (1 - e) * e * p.cx + e * e * tx;
        const by = (1 - e) * (1 - e) * sy + 2 * (1 - e) * e * p.cy + e * e * ty;
        ctx.save(); ctx.globalAlpha = wa * Math.sin(k * Math.PI) * 0.95 + 0.05; ctx.fillStyle = C.redHi;
        ctx.translate(bx, by); ctx.rotate(k * 6 + p.m); ctx.fillRect(-p.s, -p.s * 0.5, p.s * 2, p.s); ctx.restore();
      }
    }

    // calendar burst: every single day loses the same 45 minutes
    if (shrink > 0) {
      const ga = 1 - E.inOut(prog(t, Q.so - 0.1, Q.foreman));
      for (const c of grid) {
        if (c.n === 0) continue;
        const t0 = Q.every2 + 0.05 + c.n * 0.018;
        const k = E.outBack(prog(t, t0, t0 + 0.3));
        const off = E.inBack(prog(t, Q.so - 0.1 + (34 - c.n) * 0.008, Q.so + 0.15 + (34 - c.n) * 0.008));
        const rr = 70 * k * (1 - off);
        if (rr <= 0.5) continue;
        dial(ctx, { x: c.x, y: c.y, r: rr, col: C.brass, reveal: 1, minutes: 0, hours: 6, hideMinute: true, numerals: false, lw: 2, face: C.ink2, alpha: ga });
        wedge(ctx, c.x, c.y, rr * 0.88, 0, 45 * E.out(prog(t, t0 + 0.08, t0 + 0.4)), C.red, ga, false);
      }
    }

    // headline type
    const hy = 300;
    riseText(ctx, 'FAST.', 540, hy, F.black(170), C.red, prog(t, Q.fast - 0.06, Q.fast + 0.3), 170, { out: prog(t, Q.dusk - 0.1, Q.dusk + 0.2), ls: -4 });
    riseText(ctx, 'SLOW.', 540, hy, F.black(170), C.red, prog(t, Q.slow - 0.06, Q.slow + 0.3), 170, { out: prog(t, Q.which - 0.05, Q.which + 0.25), ls: -4 });
    riseText(ctx, 'NEARLY AN HOUR', 540, hy, F.black(100), C.paper, prog(t, Q.nearly - 0.06, Q.nearly + 0.3), 100, { out: prog(t, Q.free - 0.14, Q.free + 0.1), ls: -2 });
    riseText(ctx, 'OF FREE WORK', 540, hy, F.black(110), C.red, prog(t, Q.free - 0.1, Q.free + 0.2), 110, { out: prog(t, Q.every2 - 0.12, Q.every2 + 0.1), ls: -2 });
    const ed = env(t, Q.every2 - 0.1, Q.so + 0.25, 0.1, 0.3);
    if (ed > 0) spokenLine(ctx, [{ w: 'EVERY', t: Q.every2 }, { w: 'SINGLE', t: Q.single }, { w: 'DAY.', t: Q.day, color: C.red }], 540, 400, F.black(96), C.paper, t, { alpha: ed, rise: 40, dur: 0.2, ls: -1 });
  }

  // ---------- scenes: the three people (29.9 – 40.9) ----------
  function titleCard(ctx, t, num, name, tIn, tOut, opts = {}) {
    const a = env(t, tIn - 0.1, tOut, 0.3, 0.35);
    if (a <= 0) return;
    const k = E.outQ(prog(t, tIn - 0.1, tIn + 0.5));
    const ko = E.inOut(prog(t, tOut - 0.35, tOut));
    ctx.save(); ctx.globalAlpha = a;
    // rule
    ctx.strokeStyle = C.brass; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(110, 560); ctx.lineTo(110 + 860 * k * (1 - ko), 560); ctx.stroke();
    text(ctx, num, 110, 360, F.mono(36), C.brass, k, 6, 'left');
    ctx.restore();
    // name, with per-letter bounce (used for the laugh)
    const lay = letterLayout(ctx, name, 540, F.serif(150), 0);
    const bounce = opts.bounce || (() => 0);
    ctx.save(); setText(ctx, F.serif(150), 0, 'left'); ctx.fillStyle = C.paper;
    ctx.beginPath(); ctx.rect(0, 340, W, 200); ctx.clip();
    lay.forEach((L, i) => {
      const lk = E.outQ(prog(t, tIn - 0.1 + i * 0.025, tIn + 0.35 + i * 0.025));
      const lo = E.inOut(prog(t, tOut - 0.4 + i * 0.015, tOut - 0.1 + i * 0.015));
      ctx.globalAlpha = a;
      ctx.fillText(L.ch, L.x, 500 + (1 - lk) * 170 - lo * 170 + bounce(i));
    });
    ctx.restore();
  }

  function scenePeople(ctx, t) {
    if (t < Q.so - 0.2 || t > Q.smiled + 0.6) return;
    // 01 — the foreman laughs, the sandwich drops
    const laugh = i => {
      let y = 0;
      for (const lt of [Q.laughed, Q.so2, Q.hard]) {
        const d = t - lt - i * 0.03;
        if (d > 0) y += -26 * Math.exp(-d * 6) * Math.sin(d * 22);
      }
      return y;
    };
    titleCard(ctx, t, '01', 'The Foreman', Q.foreman - 0.25, Q.workers - 0.25, { bounce: laugh });
    // the sandwich
    const sa = env(t, Q.foreman, Q.sandwich + 0.9, 0.3, 0.1);
    if (sa > 0) {
      const fall = Math.max(0, t - Q.dropped + 0.04);
      const bob = Math.sin(t * 3) * 6 * (fall > 0 ? 0 : 1);
      const layers = [[C.brass, 34, 22], ['#7fb069', 10, 10], [C.red, 18, 6], [C.paper, 12, 0], [C.brass, 26, -12]];
      let yy = 0;
      layers.forEach(([c, h, d], i) => {
        const vy = 2600 * fall * fall * (1 + i * 0.06), rot = fall * (i % 2 ? 1.6 : -1.2) * (1 + i * 0.3);
        const sx = 540 + fall * (i - 2) * 90;
        ctx.save(); ctx.globalAlpha = sa; ctx.translate(sx, 880 + yy + vy + bob); ctx.rotate(rot);
        ctx.fillStyle = c; ctx.beginPath(); ctx.roundRect(-170, -h / 2, 340, h, i === 0 ? [80, 80, 8, 8] : i === 4 ? [8, 8, 30, 30] : 6); ctx.fill();
        ctx.restore();
        yy += h + 2;
      });
    }
    const qa = env(t, Q.clocks - 0.1, Q.workers - 0.3, 0.2, 0.3);
    if (qa > 0) {
      text(ctx, '“', 140, 1020, F.serif(220), C.brass, qa * E.out(prog(t, Q.clocks - 0.15, Q.clocks + 0.2)), 0, 'left');
      spokenLine(ctx, [{ w: 'Clocks', t: Q.clocks }, { w: "don’t", t: Q.dont }], 540, 1060, F.serifI(120), C.paper, t, { alpha: qa });
      spokenLine(ctx, [{ w: 'lie,', t: Q.lie, color: C.red }, { w: 'kid.', t: Q.kid }], 540, 1190, F.serifI(120), C.paper, t, { alpha: qa });
    }

    // 02 — the workers stare
    titleCard(ctx, t, '02', 'The Workers', Q.workers - 0.3, Q.mayor - 0.3);
    const fa = env(t, Q.workers - 0.1, Q.mayor - 0.3, 0.3, 0.35);
    if (fa > 0) {
      const R = rng(5);
      for (let j = 0; j < 4; j++) for (let i = 0; i < 5; i++) {
        const n = j * 5 + i, x = 540 + (i - 2) * 180 + (j % 2 ? 0 : 0), y = 780 + j * 175, jit = R();
        const k = E.outBack(prog(t, Q.workers + n * 0.022, Q.workers + n * 0.022 + 0.35));
        if (k <= 0) continue;
        const look = prog(t, Q.looked + jit * 0.12, Q.looked + jit * 0.12 + 0.1); // 3-frame snap
        const mad = prog(t, Q.insulted + jit * 0.1, Q.insulted + jit * 0.1 + 0.1);
        const hop = Math.max(0, Math.sin(prog(t, Q.mothers + jit * 0.05, Q.mothers + jit * 0.05 + 0.3) * Math.PI)) * 18;
        ctx.save(); ctx.globalAlpha = fa; ctx.translate(x, y - hop); ctx.scale(k, k);
        ctx.fillStyle = mad > 0 ? mixHex(C.ink3, '#3a1712', mad) : C.ink3; ctx.strokeStyle = C.paper; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.arc(0, 0, 62, 0, TAU); ctx.fill(); ctx.stroke();
        // eyes: idle (looking down/aside) -> snap to camera
        const ex = lerp((jit - 0.5) * 14, (540 - x) * 0.012, look), ey = lerp(9, -1, look);
        ctx.fillStyle = C.paper;
        for (const s of [-1, 1]) { ctx.beginPath(); ctx.arc(s * 20 + ex, -4 + ey, 7, 0, TAU); ctx.fill(); }
        // brows drop into a scowl
        if (mad > 0) {
          ctx.strokeStyle = C.red; ctx.lineWidth = 5; ctx.lineCap = 'round';
          for (const s of [-1, 1]) { ctx.beginPath(); ctx.moveTo(s * 34, -26 - 4 * mad); ctx.lineTo(s * 9, -16 + 2 * mad); ctx.stroke(); }
        }
        // mouth: flat line
        ctx.strokeStyle = C.paper; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(-14, 28); ctx.lineTo(14, 28 + mad * 0); ctx.stroke();
        ctx.restore();
      }
    }

    // 03 — the mayor = the mill owner
    titleCard(ctx, t, '03', 'The Mayor', Q.mayor - 0.3, Q.smiled + 0.2);
    const ma = env(t, Q.mayor2 - 0.1, Q.smiled + 0.25, 0.2, 0.35);
    if (ma > 0) {
      const tilt = Math.sin(prog(t, Q.awkward, Q.awkward + 0.6) * Math.PI) * 0.0;
      ctx.save(); ctx.globalAlpha = ma; ctx.rotate(tilt);
      riseText(ctx, 'MAYOR', 540, 860, F.black(150), C.paper, prog(t, Q.mayor2 - 0.08, Q.mayor2 + 0.25), 150, { ls: -3 });
      const ek = E.inOut(prog(t, Q.owned2 - 0.05, Q.owned2 + 0.3));
      ctx.fillStyle = C.brass;
      ctx.fillRect(540 - 70 * ek, 940, 140 * ek, 14); ctx.fillRect(540 - 70 * ek, 980, 140 * ek, 14);
      riseText(ctx, 'MILL OWNER', 540, 1180, F.black(140), C.brass, prog(t, Q.mill2 - 0.1, Q.mill2 + 0.25), 140, { ls: -3 });
      ctx.restore();
    }
  }

  // ---------- scene: the question (40.9 – 46.6) ----------
  function sceneQuestion(ctx, t) {
    if (t < Q.smiled - 0.3 || t > Q.by + 0.1) return;
    // a smile, drawn as a single arc
    const sk = E.inOut(prog(t, Q.smiled, Q.smiled + 0.7));
    const so = E.inOut(prog(t, Q.asked, Q.question + 0.1));
    if (sk > 0 && so < 1) {
      ctx.save(); ctx.globalAlpha = 1 - so; ctx.strokeStyle = C.brass; ctx.lineWidth = 7; ctx.lineCap = 'round';
      const a0 = Math.PI * 0.18, a1 = Math.PI * 0.82;
      ctx.beginPath(); ctx.arc(540, 620, 380, lerp((a0 + a1) / 2, a0, sk), lerp((a0 + a1) / 2, a1, sk)); ctx.stroke();
      ctx.restore();
    }
    // he listened to every number
    const nums = [['+20', 200, 1260], ['−25', 860, 1180], ['45', 330, 1450], ['×7', 760, 1430], ['+20', 120, 760], ['−25', 960, 820]];
    nums.forEach(([s, x, y], i) => {
      const t0 = Q.listened - 0.1 + i * 0.1;
      const k = prog(t, t0, t0 + 1.4);
      if (k <= 0 || k >= 1) return;
      const e = E.inOut(k);
      text(ctx, s, lerp(x, 540, e), lerp(y, 980, e), F.monoB(56), C.cyan, Math.sin(k * Math.PI) * 0.9, 2);
    });
    // "?"
    const qk = E.outBack(prog(t, Q.question - 0.1, Q.question + 0.35)), qo = E.inOut(prog(t, Q.whose - 0.15, Q.whose + 0.2));
    if (qk > 0 && qo < 1) {
      ctx.save(); ctx.translate(540, 1080); ctx.scale(qk * (1 + qo * 0.4), qk * (1 + qo * 0.4));
      text(ctx, '?', 0, 0, F.serif(520), C.brass, 1 - qo); ctx.restore();
    }
    // "Whose clock is wrong, son?"
    const wa = env(t, Q.whose - 0.1, Q.mine + 0.1, 0.2, 0.3);
    if (wa > 0) {
      spokenLine(ctx, [{ w: 'Whose', t: Q.whose }, { w: 'clock', t: Q.whose + 0.14 }, { w: 'is', t: Q.wrong - 0.16 }, { w: 'wrong,', t: Q.wrong }], 540, 300, F.serifI(100), C.paper, t, { alpha: wa });
      spokenLine(ctx, [{ w: 'son?', t: Q.son }], 540, 410, F.serifI(100), C.paper, t, { alpha: wa });
    }
    // yours (small, honest) vs mine (enormous)
    const ya = env(t, Q.yours - 0.12, Q.by + 0.4, 0.25, 0.4);
    if (ya > 0) {
      const k = E.outBack(prog(t, Q.yours - 0.12, Q.yours + 0.3));
      const push = E.inOut(prog(t, Q.mine, Q.by + 0.4));
      glow(ctx, 270, 1240, 200, 'rgba(110,190,255,0.4)', ya);
      pocketWatch(ctx, 270 - push * 120, 1240 + push * 200, 95 * k * (1 - push * 0.3), t, ya, 1);
      text(ctx, 'YOURS', 270, 1400, F.mono(32), C.cyan, ya * (1 - push), 6);
    }
  }
  // "mine": the tower dial looms in, then the camera pulls back to the city
  const camB = [
    [Q.mine - 0.1, 540, 820, 4.2, 760, 520],
    [Q.mine + 0.35, 540, 820, 2.6, 700, 620, 'outQ'],
    [Q.by + 0.15, 540, 820, 2.45, 680, 640, 'lin'],
    [Q.friday + 1.0, 600, 1050, 0.82, 540, 1080, 'inOutQ'],
    [Q.pocket2 + 0.5, 640, 1080, 0.76, 540, 1080, 'lin'],
  ];
  function sceneLeave(ctx, t) {
    if (t < Q.mine - 0.12 || t > Q.real + 0.5) return;
    const cam = camAt(camB, t);
    const a = E.out(prog(t, Q.mine - 0.12, Q.mine + 0.1));
    const pull = prog(t, Q.by, Q.friday + 1.0);
    ctx.save(); ctx.globalAlpha = a; applyCam(ctx, cam);
    glow(ctx, TOWER.x, TOWER.y, 900, 'rgba(227,160,74,0.22)', 1);
    drawCity(ctx, t, { col: C.brass, rise: 1, lit: w => 0.3 + 0.7 * (0.5 + 0.5 * Math.sin(w.ph * 50)) * (1 - 0.5 * prog(t, Q.pocket2, Q.pocket2 + 0.4)), winCol: C.brassHi });
    drawMill(ctx, C.brass, 1, 1);
    drawTower(ctx, C.brass, 1, 1);
    ground(ctx, C.brass, 1);
    dial(ctx, { x: TOWER.x, y: TOWER.y, r: TOWER.r, col: C.brass, reveal: 1, minutes: 18 + (t - Q.mine) * 2, hours: 5.3, lw: 3.2 });
    // the maker walks away with the only honest clock
    const wk = prog(t, Q.friday, Q.pocket2 + 0.45);
    if (wk > 0) {
      const mx = lerp(760, 1520, E.inOut(wk)), my = 1430 - Math.abs(Math.sin(wk * 40)) * 5;
      const hon = 1 + 1.2 * Math.sin(prog(t, Q.honest - 0.1, Q.clock2 + 0.5) * Math.PI);
      glow(ctx, mx, my, 70 * hon, 'rgba(159,220,255,0.75)', 1);
      ctx.fillStyle = C.cyan; ctx.beginPath(); ctx.arc(mx, my, 9, 0, TAU); ctx.fill();
    }
    ctx.restore();
    // copy
    text(ctx, 'BY FRIDAY', 540, 250, F.mono(40), C.brass, env(t, Q.friday - 0.1, Q.real, 0.3, 0.4) * (pull > 0 ? 1 : 0), 8);
    const ha = env(t, Q.only - 0.1, Q.real + 0.1, 0.25, 0.4);
    if (ha > 0) spokenLine(ctx, [{ w: 'the', t: Q.only - 0.16 }, { w: 'only', t: Q.only }, { w: 'honest', t: Q.honest, color: C.cyan }, { w: 'clock', t: Q.clock2 }], 540, 370, F.serifI(90), C.paper, t, { alpha: ha });
  }

  // ---------- scene: real life, on paper (51 – 58) ----------
  function scenePaper(ctx, t) {
    if (t < Q.real - 0.35 || t > Q.city3 + 0.5) return;
    // page slides up from the bottom
    const up = E.inOutQ(prog(t, Q.real - 0.35, Q.real + 0.25));
    const top = lerp(H + 40, 0, up);
    ctx.save();
    ctx.fillStyle = C.pPaper; ctx.fillRect(0, top, W, H + 40);
    ctx.strokeStyle = C.pInk; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, top); ctx.lineTo(W, top); ctx.stroke();
    ctx.beginPath(); ctx.rect(0, top, W, H); ctx.clip();
    ctx.translate(0, top);
    // ruled margin
    ctx.strokeStyle = C.pRule; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(80, 0); ctx.lineTo(80, H); ctx.stroke();
    text(ctx, 'IN REAL LIFE', 540, 250, F.mono(34), C.red, E.out(prog(t, Q.real - 0.1, Q.real + 0.3)), 10);
    riseText(ctx, 'Factory', 540, 440, F.serif(170), C.pInk, prog(t, Q.factory - 0.1, Q.factory + 0.3), 170);
    riseText(ctx, 'Inspectors', 540, 600, F.serif(170), C.pInk, prog(t, Q.inspectors - 0.1, Q.inspectors + 0.3), 170);
    spokenLine(ctx, [{ w: '1800s', t: Q.y1800 }, { w: '·', t: Q.england - 0.15 }, { w: 'ENGLAND', t: Q.england }], 540, 700, F.mono(46), C.pInk, t, { ls: 6, rise: 14 });
    // rule draws on "reported"
    const rk = E.inOut(prog(t, Q.reported - 0.05, Q.reported + 0.5));
    ctx.strokeStyle = C.pInk; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(540 - 300 * rk, 760); ctx.lineTo(540 + 300 * rk, 760); ctx.stroke();
    // engraved dial; minute hand is turned forward, then back
    const fwd = 20 * E.inOut(prog(t, Q.turning, Q.forward + 0.35));
    const bck = -45 * E.inOut(prog(t, Q.backN - 0.05, Q.night + 0.3));
    const m = fwd + bck;
    const dk = E.inOut(prog(t, Q.reported - 0.1, Q.turning));
    const cx = 540, cy = 1110, r = 270;
    dial(ctx, { x: cx, y: cy, r, col: C.pInk, reveal: dk, minutes: m, hours: 6 + m / 60, lw: 3, face: null });
    ctx.save(); ctx.strokeStyle = C.pInk; ctx.lineWidth = 1; ctx.globalAlpha = dk; ctx.beginPath(); ctx.arc(cx, cy, r + 14, 0, TAU); ctx.stroke(); ctx.restore();
    // turning arrows
    const arrow = (from, to, k, col) => {
      if (k <= 0) return;
      const a0 = from / 60 * TAU - Math.PI / 2, a1 = lerp(from, to, k) / 60 * TAU - Math.PI / 2, rr = r + 46, ccw = to < from;
      ctx.save(); ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = 7; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.arc(cx, cy, rr, a0, a1, ccw); ctx.stroke();
      const hx = cx + Math.cos(a1) * rr, hy = cy + Math.sin(a1) * rr, dir = a1 + (ccw ? -Math.PI / 2 : Math.PI / 2);
      ctx.translate(hx, hy); ctx.rotate(dir);
      ctx.beginPath(); ctx.moveTo(14, 0); ctx.lineTo(-10, -13); ctx.lineTo(-10, 13); ctx.closePath(); ctx.fill();
      ctx.restore();
    };
    const fa = 1 - E.inOut(prog(t, Q.backN - 0.2, Q.backN + 0.1));
    ctx.save(); ctx.globalAlpha = fa; arrow(0, 20, E.inOut(prog(t, Q.turning, Q.forward + 0.35)), C.red); ctx.restore();
    arrow(20, -25, E.inOut(prog(t, Q.backN - 0.05, Q.night + 0.3)), C.red);
    text(ctx, 'MORNING  →', cx + 170, cy + r + 120, F.monoB(40), C.red, env(t, Q.morning - 0.1, Q.backN, 0.2, 0.25), 3);
    text(ctx, '←  NIGHT', cx - 170, cy + r + 120, F.monoB(40), C.red, E.out(prog(t, Q.night - 0.1, Q.night + 0.2)), 3);
    ctx.restore();
  }

  // ---------- finale: the lie becomes the time (57.8 – end) ----------
  function sceneFinale(ctx, t) {
    if (t < Q.inA - 0.35) return;
    // ink floods back in from the dial
    const ir = E.inOutQ(prog(t, Q.inA - 0.35, Q.inA + 0.35)) * 1500;
    ctx.save(); ctx.beginPath(); ctx.arc(540, 1110, ir, 0, TAU); ctx.clip();
    ctx.fillStyle = C.ink; ctx.fillRect(0, 0, W, H);
    // city returns, small and dim, one tower
    ctx.save(); ctx.translate(540, 0); ctx.scale(1, 1); ctx.translate(-540, 0);
    const cityA = E.out(prog(t, Q.city3 - 0.1, Q.city3 + 0.6)) * (1 - 0.6 * prog(t, Q.only2, Q.clock3));
    ctx.save(); ctx.translate(0, 380); ctx.globalAlpha = cityA * 0.55;
    drawCity(ctx, t, { col: C.brassLo, rise: prog(t, Q.city3 - 0.2, Q.city3 + 0.8), lit: () => 0.25, winCol: C.brass, layerAlpha: [0.4, 0.8] });
    ctx.restore();
    ctx.restore();
    // the one clock
    const dk = E.inOut(prog(t, Q.inA - 0.1, Q.inA + 0.6));
    const one = Math.exp(-Math.max(0, t - Q.one) * 2.5) * (t > Q.one ? 1 : 0);
    glow(ctx, 540, 820, 600, 'rgba(227,160,74,0.3)', dk * (0.6 + one));
    const settle = E.outBack(prog(t, Q.time - 0.05, Q.time + 0.3));
    const m = lerp(-25 + 20, 0, settle);
    dial(ctx, { x: 540, y: 820, r: 270 + 20 * E.inOut(prog(t, Q.inA, Q.time + 0.5)), col: C.brass, reveal: dk, minutes: m, hours: 6 + m / 60, lw: 4 });
    ctx.restore();

    // LIE -> TIME: L flips into T, M grows into the gap, E slides over, red cools to paper
    const la = E.out(prog(t, Q.lie2 - 0.12, Q.lie2 + 0.15));
    if (la > 0) {
      const mk = E.inOutQ(prog(t, Q.becomes - 0.05, Q.time + 0.05));
      const col = mixHex(C.red, C.paper, mk);
      const y = 1400, size = 190;
      ctx.save(); setText(ctx, F.black(size), 0, 'left');
      const wT = ctx.measureText('T').width, wL = ctx.measureText('L').width, wI = ctx.measureText('I').width, wM = ctx.measureText('M').width, wE = ctx.measureText('E').width;
      const lieW = wL + wI + wE, timeW = wT + wI + wM + wE;
      const totalW = lerp(lieW, timeW, mk);
      let x = 540 - totalW / 2;
      ctx.fillStyle = col; ctx.globalAlpha = la;
      // first glyph: L squashes away as T unfolds
      const firstW = lerp(wL, wT, mk);
      const flip = mk < 0.5 ? 1 - mk * 2 : (mk - 0.5) * 2;
      ctx.save(); ctx.translate(x + firstW / 2, y - size * 0.36); ctx.scale(Math.max(0.001, flip), 1); ctx.translate(-(x + firstW / 2), -(y - size * 0.36));
      ctx.fillText(mk < 0.5 ? 'L' : 'T', x + (firstW - (mk < 0.5 ? wL : wT)) / 2, y);
      ctx.restore();
      x += firstW;
      ctx.fillText('I', x, y); x += wI;
      const mw = wM * mk;
      if (mk > 0.01) { ctx.save(); ctx.translate(x + mw / 2, y); ctx.scale(mk, mk); ctx.globalAlpha = la * mk; ctx.fillText('M', -wM / 2, 0); ctx.restore(); }
      x += mw;
      ctx.fillText('E', x, y);
      ctx.restore();
      text(ctx, 'THE', 540, 1195, F.mono(40), mixHex(C.red, C.paper, mk), la, 14);
    }
  }

  // ---------- captions ----------
  // Short phrase groups, broken on punctuation, pauses and length.
  const captionGroups = (() => {
    const gs = []; let cur = [];
    WORDS.forEach((w, i) => {
      const nx = WORDS[i + 1];
      cur.push(w);
      const punct = /[.,?!]$/.test(w.w);
      const gapNext = nx ? nx.s - w.e : 9;
      if (punct || gapNext > 0.18 || cur.length >= 3) { gs.push(cur); cur = []; }
    });
    if (cur.length) gs.push(cur);
    return gs.map((g, i) => ({ words: g, s: g[0].s - 0.05, e: Math.min(gs[i + 1] ? gs[i + 1][0].s - 0.05 : DUR, g[g.length - 1].e + 0.6) }));
  })();
  function captions(ctx, t, paperK) {
    const g = captionGroups.find(c => t >= c.s && t < c.e);
    if (!g) return;
    const a = Math.min(E.out(prog(t, g.s, g.s + 0.08)), 1 - prog(t, g.e - 0.08, g.e));
    const items = g.words.map(w => ({ w: w.w.replace(/[.,]$/, '').toUpperCase(), s: w.s }));
    ctx.save(); setText(ctx, F.black(54), 1, 'left');
    const sp = 18, ws = items.map(it => ctx.measureText(it.w).width);
    const total = ws.reduce((x, y) => x + y, 0) + sp * (items.length - 1);
    let x = 540 - total / 2; const y = 1650;
    const base = paperK > 0.5 ? C.pInk : C.paper;
    items.forEach((it, i) => {
      const on = t >= it.s - 0.03;
      ctx.globalAlpha = a * (on ? 1 : 0.4);
      if (paperK <= 0.5) { ctx.lineWidth = 10; ctx.strokeStyle = 'rgba(5,6,9,0.85)'; ctx.lineJoin = 'round'; ctx.strokeText(it.w, x, y); }
      ctx.fillStyle = base; ctx.fillText(it.w, x, y);
      x += ws[i] + sp;
    });
    ctx.restore();
  }

  // ---------- post: grain + vignette ----------
  let grainTiles = null;
  function makeGrain() {
    grainTiles = [];
    for (let n = 0; n < 6; n++) {
      const c = document.createElement('canvas'); c.width = c.height = 256;
      const g = c.getContext('2d'), img = g.createImageData(256, 256), R = rng(1000 + n);
      for (let i = 0; i < img.data.length; i += 4) { const v = 128 + (R() + R() + R() - 1.5) * 110; img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255; }
      g.putImageData(img, 0, 0); grainTiles.push(c);
    }
  }
  function post(ctx, t, frame) {
    if (!grainTiles) makeGrain();
    const R = rng(frame * 13 + 7);
    ctx.save(); ctx.globalCompositeOperation = 'overlay'; ctx.globalAlpha = 0.07;
    const tile = grainTiles[frame % grainTiles.length];
    const pat = ctx.createPattern(tile, 'repeat');
    ctx.translate(-R() * 256, -R() * 256); ctx.fillStyle = pat; ctx.fillRect(0, 0, W + 256, H + 256);
    ctx.restore();
    const v = ctx.createRadialGradient(540, 900, 500, 540, 960, 1250);
    v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,0.55)');
    ctx.fillStyle = v; ctx.fillRect(0, 0, W, H);
  }

  // ---------- master render ----------
  function render(ctx, t) {
    ctx.save();
    ctx.fillStyle = C.ink; ctx.fillRect(0, 0, W, H);

    // world (0 – 15.6), with the iris on the second bell revealing the cool palette
    if (t < Q.pocket + 0.8) {
      // tiny camera shake on "lied"
      const sh = Math.exp(-Math.max(0, t - Q.lied) * 14) * (t > Q.lied ? 1 : 0);
      ctx.save(); ctx.translate(Math.sin(t * 90) * 8 * sh, Math.cos(t * 77) * 6 * sh);
      const bellAt = Q.bell2;
      const irisK = prog(t, bellAt, bellAt + 0.75);
      if (irisK > 0 && irisK < 1) {
        // draw warm world fully, then the cool world inside an expanding ring
        sceneWorld(ctx, t, true);
        const ts = towerScreen(t), R = E.inOut(irisK) * 2400 + ts.s * TOWER.r;
        ctx.save(); ctx.beginPath(); ctx.arc(ts.x, ts.y, R, 0, TAU); ctx.clip();
        ctx.fillStyle = '#070b12'; ctx.fillRect(0, 0, W, H);
        sceneWorld(ctx, t); ctx.restore();
        ctx.save(); ctx.strokeStyle = C.brassHi; ctx.globalAlpha = 1 - irisK; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(ts.x, ts.y, R, 0, TAU); ctx.stroke(); ctx.restore();
      } else {
        if (irisK >= 1) { ctx.fillStyle = '#070b12'; ctx.fillRect(0, 0, W, H); }
        sceneWorld(ctx, t);
      }
      ctx.restore();
      // fade the world away as the watch takes over
      const wf = E.inOut(prog(t, Q.pocket - 0.3, Q.pocket + 0.15));
      if (wf > 0) { ctx.fillStyle = `rgba(7,11,18,${wf})`; ctx.fillRect(0, 0, W, H); }
      textWorld(ctx, t);
    }
    sceneWatch(ctx, t);
    sceneReveal(ctx, t);
    scenePeople(ctx, t);
    sceneLeave(ctx, t);
    sceneQuestion(ctx, t);
    scenePaper(ctx, t);
    sceneFinale(ctx, t);

    const paperK = t > Q.real && t < Q.inA ? 1 : 0;
    captions(ctx, t, paperK);

    // final cut to black on the last syllable's tail
    const endK = E.inOut(prog(t, DUR - 0.3, DUR - 0.02));
    if (endK > 0) { ctx.fillStyle = `rgba(0,0,0,${endK})`; ctx.fillRect(0, 0, W, H); }
    ctx.restore();
  }

  window.CLIP = { W, H, DUR, render, post, Q };
})();
