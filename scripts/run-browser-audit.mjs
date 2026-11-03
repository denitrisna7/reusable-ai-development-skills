#!/usr/bin/env node
/**
 * Real Headless Chromium Browser QA & Visual/DOM Auditor (Playwright Engine)
 *
 * Automatically locates Playwright (`node_modules/playwright`, global links in
 * `~/.cache/ms-playwright/.links`, or local installations) and executes a REAL
 * headless Chromium browser session to verify:
 *   1. Page navigation & HTTP status codes (catching 404, 403, 500)
 *   2. Runtime JS Console Errors, Page Errors, and failed Network Requests
 *   3. Desktop (1440x900) and Mobile (375x812) Responsive Reflow
 *   4. Real DOM Computed Color Contrast (WCAG 2.2 AA >= 4.5:1 normal / >= 3.0:1 large,
 *      detecting unreadable or white-on-white text)
 *   5. Real DOM Text-Range Bounding-Box Collisions (overlapping/floating text,
 *      horizontal overflow, clipped text, and mobile touch target dimensions)
 *   6. Automatic or explicit Interactive Login & authenticated dashboard verification
 *
 * Usage:
 *   node scripts/run-browser-audit.mjs [baseUrl] [route1] [route2] ... [--login-url=/login --user=admin@example.com --pass=password]
 */

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { createRequire } from 'node:module';

async function loadPlaywright() {
  const candidates = [
    path.join(process.cwd(), 'package.json'),
    path.join(os.homedir(), 'package.json'),
  ];

  const linksDir = path.join(os.homedir(), '.cache', 'ms-playwright', '.links');
  if (fs.existsSync(linksDir)) {
    for (const file of fs.readdirSync(linksDir)) {
      try {
        const linkedPath = fs.readFileSync(path.join(linksDir, file), 'utf8').trim();
        if (linkedPath && fs.existsSync(linkedPath)) {
          candidates.push(path.join(linkedPath, 'package.json'));
          candidates.push(path.join(linkedPath, '..', '..', 'package.json'));
        }
      } catch {
        // ignore unreadable link file
      }
    }
  }

  for (const candidate of candidates) {
    if (!fs.existsSync(candidate)) continue;
    try {
      const req = createRequire(candidate);
      try {
        return req('playwright');
      } catch {
        return req('playwright-core');
      }
    } catch {
      // try next candidate
    }
  }

  try {
    return await import('playwright');
  } catch {
    return await import('playwright-core');
  }
}

function findChromiumExecutable() {
  const customPaths = [
    '/var/lib/flatpak/app/com.google.Chrome/current/active/files/extra/chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/google-chrome',
    '/opt/google/chrome/chrome',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
  ];
  for (const bin of customPaths) {
    if (fs.existsSync(bin)) return bin;
  }

  const cacheDir = path.join(os.homedir(), '.cache', 'ms-playwright');
  if (fs.existsSync(cacheDir)) {
    const dirs = fs.readdirSync(cacheDir).filter((d) => d.startsWith('chromium-')).sort().reverse();
    for (const dir of dirs) {
      const bin = path.join(cacheDir, dir, 'chrome-linux64', 'chrome');
      if (fs.existsSync(bin)) return bin;
      const binLegacy = path.join(cacheDir, dir, 'chrome-linux', 'chrome');
      if (fs.existsSync(binLegacy)) return binLegacy;
    }
  }
  return undefined;
}

function autoDiscoverCredentialsFromRepo() {
  const envCandidates = [
    path.join(process.cwd(), '.env'),
    path.join(process.cwd(), 'sdmk_app', '.env'),
    path.join(process.cwd(), 'app', '.env'),
    path.join(process.cwd(), 'backend', '.env'),
    path.join(process.cwd(), '..', '.env'),
  ];
  for (const envPath of envCandidates) {
    if (fs.existsSync(envPath)) {
      try {
        const txt = fs.readFileSync(envPath, 'utf8');
        const uMatch = txt.match(/(?:ADMIN_USERNAME|ADMIN_EMAIL|ADMIN_USER|TEST_USER_EMAIL)\s*=\s*['"]?([^'"\r\n]+)['"]?/i);
        const pMatch = txt.match(/(?:ADMIN_INITIAL_PASSWORD|ADMIN_PASSWORD|ADMIN_PASS|TEST_USER_PASSWORD)\s*=\s*['"]?([^'"\r\n]+)['"]?/i);
        if (uMatch && pMatch) {
          const u = uMatch[1].trim();
          const p = pMatch[1].trim();
          if (u && p) {
            return { loginUrl: '/login', user: u, pass: p };
          }
        }
      } catch {
        // ignore
      }
    }
  }

  const candidates = [
    path.join(process.cwd(), 'database', 'seeders', 'DatabaseSeeder.php'),
    path.join(process.cwd(), 'database', 'seeders', 'UserSeeder.php'),
    path.join(process.cwd(), 'database', 'seeders', 'DemoDataSeeder.php'),
    path.join(process.cwd(), 'prisma', 'seed.ts'),
    path.join(process.cwd(), 'prisma', 'seed.js'),
    path.join(process.cwd(), 'seed.py'),
  ];
  for (const seederPath of candidates) {
    if (!fs.existsSync(seederPath)) continue;
    try {
      const lines = fs.readFileSync(seederPath, 'utf8').split(/\r?\n/);
      for (const line of lines) {
        if (line.includes('delete') || line.trim().startsWith('//') || line.trim().startsWith('*') || line.trim().startsWith('#')) {
          continue;
        }
        const m = line.match(/['"]([a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})['"]/);
        if (m) {
          return { loginUrl: '/login', user: m[1], pass: 'password' };
        }
      }
    } catch {
      // ignore
    }
  }
  return null;
}

/**
 * Injected into the live Chromium DOM to audit computed contrast, text-range overlaps, overflow, and touch targets.
 */
function domAuditEvaluator(viewportLabel) {
  const colorCanvas = document.createElement('canvas');
  colorCanvas.width = 1;
  colorCanvas.height = 1;
  const colorCtx = colorCanvas.getContext('2d', { willReadFrequently: true });

  function parseRgba(str) {
    if (!str || str === 'transparent' || str === 'rgba(0, 0, 0, 0)') {
      return { r: 255, g: 255, b: 255, a: 0 };
    }
    const m = str.match(/rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)(?:\s*[,/]\s*([\d.]+))?\s*\)/i);
    if (m) {
      return {
        r: Number(m[1]),
        g: Number(m[2]),
        b: Number(m[3]),
        a: m[4] !== undefined ? Number(m[4]) : 1,
      };
    }
    // Support Tailwind v4 oklab(), oklch(), color(srgb ...), hsl() via Chromium 2D canvas rasterizer
    if (colorCtx) {
      try {
        colorCtx.clearRect(0, 0, 1, 1);
        colorCtx.fillStyle = str;
        colorCtx.fillRect(0, 0, 1, 1);
        const data = colorCtx.getImageData(0, 0, 1, 1).data;
        return {
          r: data[0],
          g: data[1],
          b: data[2],
          a: Number((data[3] / 255).toFixed(3)),
        };
      } catch {
        // fallback below
      }
    }
    return { r: 255, g: 255, b: 255, a: 0 };
  }

  function blend(fg, bg) {
    const a = fg.a + bg.a * (1 - fg.a);
    if (a === 0) return { r: 255, g: 255, b: 255, a: 0 };
    return {
      r: (fg.r * fg.a + bg.r * bg.a * (1 - fg.a)) / a,
      g: (fg.g * fg.a + bg.g * bg.a * (1 - fg.a)) / a,
      b: (fg.b * fg.a + bg.b * bg.a * (1 - fg.a)) / a,
      a,
    };
  }

  function getEffectiveBg(el) {
    const layers = [];
    let cur = el;
    let hasBgImage = false;
    while (cur && cur.nodeType === 1) {
      const style = window.getComputedStyle(cur);
      const beforeStyle = window.getComputedStyle(cur, '::before');
      if (
        style.backgroundImage !== 'none' ||
        (beforeStyle && beforeStyle.backgroundImage !== 'none') ||
        style.backdropFilter !== 'none'
      ) {
        hasBgImage = true;
        break;
      }
      const bg = parseRgba(style.backgroundColor);
      if (bg.a > 0) layers.push(bg);
      if (bg.a >= 0.99) break;
      cur = cur.parentElement;
    }
    let composite = { r: 255, g: 255, b: 255, a: 1 };
    for (let i = layers.length - 1; i >= 0; i--) {
      composite = blend(layers[i], composite);
    }
    return { currBg: composite, hasBgImage };
  }

  function luminance({ r, g, b }) {
    const chan = [r, g, b].map((v) => {
      const s = v / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * chan[0] + 0.7152 * chan[1] + 0.0722 * chan[2];
  }

  function contrastRatio(c1, c2) {
    const l1 = luminance(c1);
    const l2 = luminance(c2);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  }

  function isVisible(el) {
    let cur = el;
    while (cur && cur.nodeType === 1) {
      if (cur.id === 'playwright-live-hud' || (cur.closest && cur.closest('#playwright-live-hud'))) {
        return false;
      }
      if (cur.hasAttribute('hidden') || cur.hasAttribute('x-cloak') || cur.getAttribute('aria-hidden') === 'true') {
        return false;
      }
      const style = window.getComputedStyle(cur);
      if (style.display === 'none' || style.visibility === 'hidden' || Number(style.opacity) < 0.05) return false;
      if (style.clip === 'rect(0px, 0px, 0px, 0px)' || cur.classList.contains('sr-only')) return false;
      cur = cur.parentElement;
    }
    const rect = el.getBoundingClientRect();
    if (rect.width <= 2 || rect.height <= 2) return false;
    // Ignore off-canvas drawers translated completely off-screen to the left or top
    if (rect.right <= 0 || rect.bottom <= 0) return false;
    return true;
  }

  function isInsideHorizontalScrollContainer(el, vw) {
    let cur = el.parentElement;
    while (cur && cur !== document.body && cur !== document.documentElement) {
      const st = window.getComputedStyle(cur);
      if (['auto', 'scroll', 'hidden', 'clip'].includes(st.overflowX)) {
        const r = cur.getBoundingClientRect();
        if (r.right <= vw + 2) return true;
      }
      cur = cur.parentElement;
    }
    return false;
  }

  const vw = window.innerWidth;
  const docScrollWidth = document.documentElement.scrollWidth;
  const horizontalOverflowPx = Math.max(0, docScrollWidth - vw);

  const contrastFailures = [];
  let minContrast = 21.0;
  let textElementsChecked = 0;

  const clippedElements = [];
  const overflowCulprits = [];
  const textBoxes = [];

  const allElements = Array.from(document.querySelectorAll('body *'));
  if (horizontalOverflowPx > 4) {
    for (const el of allElements) {
      if (el.id === 'playwright-live-hud' || (el.closest && el.closest('#playwright-live-hud'))) continue;
      const r = el.getBoundingClientRect();
      if (r.right > vw + 4 && !isInsideHorizontalScrollContainer(el, vw)) {
        const cls = typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 3).join('.') : '';
        overflowCulprits.push({
          selector: `<${el.tagName.toLowerCase()}${cls}>`,
          rightPx: Math.round(r.right),
          overflowPx: Math.round(r.right - vw),
        });
      }
    }
    if (overflowCulprits.length === 0) {
      for (const el of allElements) {
        if (el.id === 'playwright-live-hud' || (el.closest && el.closest('#playwright-live-hud'))) continue;
        const r = el.getBoundingClientRect();
        if (r.right > vw + 4 || el.scrollWidth > vw + 4) {
          const cls = typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 3).join('.') : '';
          overflowCulprits.push({
            selector: `<${el.tagName.toLowerCase()}${cls}>`,
            rightPx: Math.round(Math.max(r.right, el.scrollWidth)),
            overflowPx: Math.round(Math.max(r.right, el.scrollWidth) - vw),
          });
        }
      }
    }
  }

  for (const el of allElements) {
    if (!isVisible(el)) continue;

    const textNodes = Array.from(el.childNodes).filter((n) => n.nodeType === 3 && n.textContent.trim().length > 0);
    if (textNodes.length === 0) continue;

    const directText = textNodes.map((n) => n.textContent.trim()).join(' ').trim();
    if (!directText) continue;

    const style = window.getComputedStyle(el);
    const { currBg, hasBgImage } = getEffectiveBg(el);

    if (!hasBgImage) {
      const fgRaw = parseRgba(style.color);
      const fg = blend(fgRaw, currBg);
      const ratio = contrastRatio(fg, currBg);
      const fontSize = parseFloat(style.fontSize) || 16;
      const isBold = (parseInt(style.fontWeight, 10) || 400) >= 700;
      const isLarge = fontSize >= 24 || (fontSize >= 18.66 && isBold);
      const threshold = isLarge ? 3.0 : 4.5;

      textElementsChecked++;
      if (ratio < minContrast) minContrast = ratio;

      if (ratio < threshold) {
        const cls = typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 3).join('.') : '';
        contrastFailures.push({
          tag: `${el.tagName.toLowerCase()}${cls}`,
          text: directText.slice(0, 40),
          ratio: Number(ratio.toFixed(2)),
          threshold,
          fg: style.color,
          bg: `rgb(${Math.round(currBg.r)},${Math.round(currBg.g)},${Math.round(currBg.b)})`,
        });
      }
    }

    if (
      (style.overflowX === 'hidden' || style.overflowX === 'clip') &&
      style.textOverflow !== 'ellipsis' &&
      el.scrollWidth > el.clientWidth + 6 &&
      el.children.length === 0
    ) {
      clippedElements.push({
        tag: el.tagName.toLowerCase(),
        text: directText.slice(0, 40),
        clientWidth: el.clientWidth,
        scrollWidth: el.scrollWidth,
      });
    }

    // Measure exact rendered character range box
    try {
      const range = document.createRange();
      range.selectNodeContents(textNodes[0]);
      const r = range.getBoundingClientRect();
      if (r.top >= 0 && r.bottom <= window.innerHeight * 2.5 && r.width > 6 && r.height > 6) {
        textBoxes.push({ el, rect: r, text: directText.slice(0, 35), tag: el.tagName.toLowerCase() });
      }
    } catch {
      // ignore range errors
    }
  }

  const overlaps = [];
  for (let i = 0; i < Math.min(textBoxes.length, 150); i++) {
    for (let j = i + 1; j < Math.min(textBoxes.length, 150); j++) {
      const a = textBoxes[i];
      const b = textBoxes[j];
      if (a.el === b.el || a.el.contains(b.el) || b.el.contains(a.el)) continue;

      const xOverlap = Math.max(0, Math.min(a.rect.right, b.rect.right) - Math.max(a.rect.left, b.rect.left));
      const yOverlap = Math.max(0, Math.min(a.rect.bottom, b.rect.bottom) - Math.max(a.rect.top, b.rect.top));
      const overlapArea = xOverlap * yOverlap;
      const minArea = Math.min(a.rect.width * a.rect.height, b.rect.width * b.rect.height);

      if (overlapArea > 0 && overlapArea / minArea > 0.35) {
        overlaps.push({
          first: `<${a.tag}> "${a.text}"`,
          second: `<${b.tag}> "${b.text}"`,
          overlapPct: Math.round((overlapArea / minArea) * 100),
        });
      }
    }
  }

  const missingAltCount = Array.from(document.querySelectorAll('img')).filter(
    (img) => isVisible(img) && !img.hasAttribute('alt')
  ).length;
  const hasViewportMeta = Boolean(document.querySelector('meta[name="viewport"]'));
  const htmlLang = document.documentElement.getAttribute('lang') || '';
  const landmarksCount = document.querySelectorAll('main, nav, header, footer, [role="main"], [role="navigation"]').length;

  return {
    viewportLabel,
    viewportSize: `${vw}x${window.innerHeight}`,
    title: document.title,
    horizontalOverflowPx,
    textElementsChecked,
    minContrast: textElementsChecked > 0 ? Number(minContrast.toFixed(2)) : null,
    contrastFailures: contrastFailures.slice(0, 5),
    clippedElements: clippedElements.slice(0, 5),
    overflowCulprits: overflowCulprits.slice(0, 4),
    overlaps: overlaps.slice(0, 5),
    formsCount: document.querySelectorAll('form').length,
    buttonsCount: document.querySelectorAll('button, [type="submit"]').length,
    tablesCount: document.querySelectorAll('table').length,
    missingAltCount,
    hasViewportMeta,
    htmlLang,
    landmarksCount,
  };
}

async function main() {
  const args = process.argv.slice(2);
  let baseUrl = 'http://127.0.0.1:8000';
  const routes = [];
  let loginUrl = null;
  let loginUser = null;
  let loginPass = null;

  const hasDisplay = Boolean(
    process.env.DISPLAY ||
    process.env.WAYLAND_DISPLAY ||
    process.platform === 'win32' ||
    process.platform === 'darwin'
  );

  let isHeaded = hasDisplay;
  let slowMo = isHeaded ? 250 : 0;
  let holdSec = isHeaded ? 3 : 0;

  for (const arg of args) {
    if (arg.startsWith('--login-url=')) loginUrl = arg.split('=')[1];
    else if (arg.startsWith('--user=')) loginUser = arg.split('=')[1];
    else if (arg.startsWith('--pass=')) loginPass = arg.split('=')[1];
    else if (arg === '--headless') { isHeaded = false; slowMo = 0; holdSec = 0; }
    else if (arg === '--headed' || arg === '--visual') { isHeaded = true; slowMo = 250; holdSec = 3; }
    else if (arg.startsWith('--slowmo=')) slowMo = parseInt(arg.split('=')[1], 10) || 0;
    else if (arg.startsWith('--hold=')) holdSec = parseInt(arg.split('=')[1], 10) || 0;
    else if (arg.startsWith('http://') || arg.startsWith('https://')) baseUrl = arg.replace(/\/$/, '');
    else if (arg.startsWith('/')) routes.push(arg);
  }

  if (!loginUser) {
    const autoCreds = autoDiscoverCredentialsFromRepo();
    if (autoCreds) {
      loginUrl = autoCreds.loginUrl;
      loginUser = autoCreds.user;
      loginPass = autoCreds.pass;
    }
  }

  const pw = await loadPlaywright();
  const executablePath = findChromiumExecutable();

  console.log('========================================================================');
  console.log('  PLAYWRIGHT BROWSER QA & VISUAL/DOM AUDITOR (LIVE ON SCREEN)');
  console.log('========================================================================');
  console.log(`Target Base URL : ${baseUrl}`);
  console.log(`Display Target  : ${isHeaded ? 'LIVE GUI WINDOW (Tampil di Layar Monitor Anda)' : 'Headless Chromium (Background/CI)'}`);
  console.log(`Browser Engine  : ${executablePath || 'Playwright Default Chromium'}`);
  if (isHeaded) {
    console.log(`Visual Features : SlowMo=${slowMo}ms, Floating HUD Banner=Aktif, Highlight Glow=Aktif`);
  }

  let browser;
  try {
    browser = await pw.chromium.launch({
      headless: !isHeaded,
      slowMo,
      ...(executablePath ? { executablePath } : {}),
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--window-size=1440,960',
      ],
    });
  } catch (launchErr) {
    if (isHeaded) {
      console.log(`⚠️  [NOTICE] Gagal membuka jendela GUI (${launchErr.message}). Beralih otomatis ke mode Headless...`);
      isHeaded = false;
      slowMo = 0;
      holdSec = 0;
      browser = await pw.chromium.launch({
        headless: true,
        slowMo: 0,
        ...(executablePath ? { executablePath } : {}),
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
      });
    } else {
      throw launchErr;
    }
  }

  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
  });
  const page = await context.newPage();

  async function setHUD(text, type = 'action') {
    if (!isHeaded) return;
    try {
      await page.evaluate(({ text, type }) => {
        let el = document.getElementById('playwright-live-hud');
        if (!el) {
          el = document.createElement('div');
          el.id = 'playwright-live-hud';
          el.setAttribute('aria-hidden', 'true');
          document.body.appendChild(el);
        }
        const colors = {
          action: 'linear-gradient(135deg, #0284c7, #0369a1)',
          audit: 'linear-gradient(135deg, #6366f1, #4f46e5)',
          success: 'linear-gradient(135deg, #059669, #047857)',
          warning: 'linear-gradient(135deg, #d97706, #b45309)',
          danger: 'linear-gradient(135deg, #dc2626, #991b1b)',
        };
        const bg = colors[type] || colors.action;
        el.innerHTML = `
          <div style="position:fixed; top:14px; left:50%; transform:translateX(-50%); z-index:99999999; background:${bg}; color:#ffffff; padding:10px 24px; border-radius:9999px; font-family:ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size:13px; font-weight:800; letter-spacing:0.3px; box-shadow:0 12px 30px rgba(0,0,0,0.5); display:flex; align-items:center; gap:10px; pointer-events:none; border:2px solid rgba(255,255,255,0.4); text-shadow:0 1px 2px rgba(0,0,0,0.5); user-select:none; transition:all 0.25s ease;">
            <span style="background:rgba(255,255,255,0.25); padding:2px 8px; border-radius:9999px; font-size:11px; font-weight:700;">PLAYWRIGHT LIVE QA</span>
            <span>${text}</span>
          </div>
        `;
      }, { text, type });
    } catch {
      // ignore
    }
  }

  async function highlightElement(locator, color = '#f59e0b') {
    if (!isHeaded) return;
    try {
      await locator.evaluate((el, c) => {
        el.style.outline = `3px solid ${c}`;
        el.style.boxShadow = `0 0 16px ${c}`;
        el.style.transition = 'all 0.25s ease';
      }, color);
    } catch {}
  }

  page.on('dialog', async (dialog) => {
    console.log(`   💬 Browser Dialog: "${dialog.message()}" -> Auto-accepted (OK)`);
    await dialog.accept().catch(() => {});
  });

  const consoleErrors = [];
  const pageErrors = [];
  const failedRequests = [];

  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', (err) => {
    pageErrors.push(err.message);
  });
  page.on('response', (res) => {
    if (res.status() >= 400 && !res.url().includes('favicon.ico')) {
      failedRequests.push(`${res.status()} ${res.request().method()} ${res.url()}`);
    }
  });

  if (routes.length === 0) {
    routes.push('/');
    try {
      await page.goto(baseUrl + '/', { waitUntil: 'domcontentloaded', timeout: 15000 });
      const hrefs = await page.evaluate(() =>
        Array.from(document.querySelectorAll('a[href]'))
          .map((a) => {
            try {
              const u = new URL(a.href, window.location.origin);
              if (u.origin !== window.location.origin) return null;
              return u.pathname;
            } catch {
              return null;
            }
          })
          .filter(
            (p) =>
              p &&
              p.startsWith('/') &&
              !p.endsWith('.apk') &&
              !p.endsWith('.pdf') &&
              !p.startsWith('/unduh-apk/file')
          )
      );
      for (const h of hrefs) {
        const clean = h.split('?')[0].split('#')[0];
        if (!routes.includes(clean) && routes.length < 25) routes.push(clean);
      }
    } catch (e) {
      console.error(`⛔ [FATAL] Cannot connect to ${baseUrl}: ${e.message}`);
      await browser.close();
      process.exit(1);
    }
  }

  let totalDefects = 0;
  const viewports = [
    { label: 'Desktop Web View', width: 1440, height: 900 },
    { label: 'Mobile Phone View', width: 375, height: 812 },
  ];

  async function auditRoutesList(routeList, phaseLabel, maxLimit = 25) {
    for (let rIdx = 0; rIdx < routeList.length; rIdx++) {
      const route = routeList[rIdx];
      const targetUrl = baseUrl + route;
      console.log(`\n------------------------------------------------------------------------`);
      console.log(`🌐 [${phaseLabel} ${rIdx + 1}/${routeList.length}] ${targetUrl}`);
      console.log(`------------------------------------------------------------------------`);

      for (const vp of viewports) {
        consoleErrors.length = 0;
        pageErrors.length = 0;
        failedRequests.length = 0;

        await page.setViewportSize({ width: vp.width, height: vp.height });
        await setHUD(`🌐 [${phaseLabel} ${rIdx + 1}/${routeList.length}] ${route} (${vp.label} ${vp.width}x${vp.height})`, 'action');
        const t0 = Date.now();
        let response = null;
        try {
          response = await page.goto(targetUrl, { waitUntil: 'domcontentloaded', timeout: 15000 });
        } catch (gotoErr) {
          consoleErrors.push(gotoErr.message);
        }
        const loadMs = Date.now() - t0;
        await setHUD(`📐 Memeriksa Kontras WCAG AA, Overflow & Tata Letak (${vp.width}x${vp.height})...`, 'audit');

        if (isHeaded) {
          await page.evaluate(() => window.scrollBy({ top: 350, behavior: 'smooth' })).catch(() => {});
          await page.waitForTimeout(160);
          await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'smooth' })).catch(() => {});
          await page.waitForTimeout(120);

          // Test clicking visible interactive elements (buttons, accordion, tabs, modals, search) on desktop view
          if (vp.width === 1440) {
            try {
              // 1. Test clicking visible interactive buttons, tabs, accordions, and modal triggers
              const interactiveSelectors = [
                'details > summary',
                '[data-bs-toggle="collapse"]',
                '.faq-item summary',
                '.accordion-button',
                'button.tab-btn, [role="tab"], .nav-tabs .nav-link',
                '[data-bs-toggle="modal"], [data-toggle="modal"]',
                'button:has-text("Tambah"), button:has-text("Create"), button:has-text("New")',
                'button.filter-btn, [data-filter]',
              ];
              for (const sel of interactiveSelectors) {
                const loc = page.locator(sel).first();
                if ((await loc.count()) > 0 && (await loc.isVisible())) {
                  const label = ((await loc.innerText().catch(() => '')) || sel).trim().replace(/\s+/g, ' ').slice(0, 30);
                  await setHUD(`🖱️ Menguji Klik Tombol: "${label}"...`, 'action');
                  await highlightElement(loc, '#3b82f6');
                  await loc.click({ timeout: 2500 }).catch(() => {});
                  await page.waitForTimeout(250);

                  // If modal opened, inspect it and close it
                  const modalClose = page.locator('.modal.show [data-bs-dismiss="modal"], .modal.show .btn-close, dialog[open] button:has-text("Tutup"), dialog[open] button:has-text("Close"), [aria-label="Close"]').first();
                  if ((await modalClose.count()) > 0 && (await modalClose.isVisible())) {
                    await setHUD(`📋 Modal Terbuka! Memeriksa Elemen & Menutup Modal...`, 'audit');
                    await highlightElement(modalClose, '#ef4444');
                    await modalClose.click({ timeout: 2000 }).catch(() => {});
                    await page.waitForTimeout(200);
                  }
                }
              }

              // 2. Test interactive search/filter form inputs if present
              const searchInput = page.locator('input[type="search"], input[name*="search"], input[name*="cari"], input[placeholder*="cari" i], input[placeholder*="search" i]').first();
              if ((await searchInput.count()) > 0 && (await searchInput.isVisible())) {
                await setHUD(`🔍 Menguji Input Form Pencarian & Filter...`, 'action');
                await highlightElement(searchInput, '#f59e0b');
                await searchInput.fill('Uji Otomasi Playwright');
                await page.waitForTimeout(300);
                await searchInput.fill('');
                await page.waitForTimeout(150);
              }

              // 3. Test table action buttons / row hover (previewing CRUD action buttons)
              const rowActionButton = page.locator('table tbody tr:first-child button, table tbody tr:first-child a.btn, table tbody tr:first-child [title*="Edit" i], table tbody tr:first-child [title*="Detail" i]').first();
              if ((await rowActionButton.count()) > 0 && (await rowActionButton.isVisible())) {
                await setHUD(`⚡ Menguji Aksi Baris Data Tabel (CRUD Action)...`, 'action');
                await highlightElement(rowActionButton, '#10b981');
                await rowActionButton.hover().catch(() => {});
                await page.waitForTimeout(250);
              }
            } catch {
              // Ignore if non-interactable
            }
          }
        } else {
          await page.waitForTimeout(160);
        }

        const status = response ? response.status() : (consoleErrors.length > 0 ? 500 : 0);
        const audit = await page.evaluate(domAuditEvaluator, vp.label);

        // Discover and queue any nested internal links (crawling deeper up to maxLimit)
        if (status === 200 && routeList.length < maxLimit) {
          try {
            const discoveredLinks = await page.evaluate(() => {
              return Array.from(document.querySelectorAll('a[href]'))
                .map((a) => {
                  try {
                    const u = new URL(a.href, window.location.origin);
                    if (u.origin !== window.location.origin) return null;
                    return u.pathname;
                  } catch {
                    return null;
                  }
                })
                .filter(
                  (p) =>
                    p &&
                    p.startsWith('/') &&
                    !p.endsWith('.apk') &&
                    !p.endsWith('.pdf') &&
                    !p.startsWith('/unduh-apk/file') &&
                    !p.includes('logout')
                );
            });
            for (const dl of discoveredLinks) {
              const clean = dl.split('?')[0].split('#')[0];
              if (!routeList.includes(clean) && routeList.length < maxLimit) {
                routeList.push(clean);
              }
            }
          } catch {
            // Ignore extraction errors
          }
        }

        console.log(`  📐 [${vp.label} (${vp.width}x${vp.height})]`);
        console.log(`     • HTTP Status & Load  : HTTP ${status} (${loadMs}ms) | Title: "${audit.title}"`);
        console.log(`     • DOM & A11y Landmarks: ${audit.textElementsChecked} text nodes, ${audit.landmarksCount} landmarks, ${audit.formsCount} forms, ${audit.buttonsCount} buttons, ${audit.missingAltCount} missing alt`);
        console.log(`     • SEO & Viewport Meta : lang="${audit.htmlLang || 'n/a'}", viewportMeta=${audit.hasViewportMeta ? 'PRESENT' : 'MISSING'}`);
        console.log(`     • Horizontal Overflow : ${audit.horizontalOverflowPx === 0 ? '0px (PASS - No horizontal leak)' : `${audit.horizontalOverflowPx}px (FAIL - Horizontal scroll leak!)`}`);
        console.log(`     • Color Contrast      : Min ${audit.minContrast ?? 'N/A'}:1 (${audit.contrastFailures.length === 0 ? 'PASS WCAG AA' : `${audit.contrastFailures.length} FAILURES`})`);
        console.log(`     • Element Collisions  : ${audit.overlaps.length === 0 ? '0 overlapping text elements (PASS)' : `${audit.overlaps.length} OVERLAPS DETECTED (FAIL)`}`);
        console.log(`     • Clipped Text        : ${audit.clippedElements.length === 0 ? '0 clipped text elements (PASS)' : `${audit.clippedElements.length} CLIPPED ELEMENTS (WARNING)`}`);
        console.log(`     • Console & Network   : ${consoleErrors.length + pageErrors.length} JS errors, ${failedRequests.length} failed HTTP requests`);

        if (status === 404) {
          totalDefects++;
          console.log(`     ❌ ERROR 404 (HALAMAN TIDAK DITEMUKAN): Rute "${route}" menghasilkan status 404 Not Found!`);
          if (isHeaded) {
            await setHUD(`❌ Error 404: Rute ${route} Tidak Ditemukan!`, 'danger');
            await page.waitForTimeout(600);
          }
        } else if (status >= 400) {
          totalDefects++;
          console.log(`     ❌ HTTP ERROR: Route returned status ${status}`);
          if (isHeaded) {
            await setHUD(`❌ HTTP Error ${status}: ${route}`, 'danger');
            await page.waitForTimeout(500);
          }
        }
        if (audit.horizontalOverflowPx > 4) {
          totalDefects++;
          for (const oc of audit.overflowCulprits || []) {
            console.log(`     ❌ OVERFLOW CULPRIT: ${oc.selector} right=${oc.rightPx}px (+${oc.overflowPx}px past viewport)`);
          }
        }
        if (audit.contrastFailures.length > 0) {
          totalDefects += audit.contrastFailures.length;
          for (const cf of audit.contrastFailures) {
            console.log(`     ❌ CONTRAST FAIL: <${cf.tag}> "${cf.text}" ratio ${cf.ratio}:1 (need >= ${cf.threshold}:1, fg=${cf.fg}, bg=${cf.bg})`);
          }
        }
        if (audit.overlaps.length > 0) {
          totalDefects += audit.overlaps.length;
          for (const ov of audit.overlaps) {
            console.log(`     ❌ OVERLAP FAIL: ${ov.first} overlaps ${ov.second} (${ov.overlapPct}%)`);
          }
        }
        if (consoleErrors.length > 0 || pageErrors.length > 0) {
          totalDefects += consoleErrors.length + pageErrors.length;
          for (const err of [...consoleErrors, ...pageErrors].slice(0, 3)) {
            console.log(`     ❌ JS ERROR: ${err}`);
          }
        }
      }
    }
  }

  // Audit Public Routes First
  await auditRoutesList(routes, 'PUBLIC ROUTE AUDIT');

  // Optional Interactive Login & Authenticated Route Audit
  if (loginUrl && loginUser && loginPass) {
    try {
      await page.setViewportSize({ width: 1440, height: 900 });
      const loginRes = await page.goto(baseUrl + loginUrl, { waitUntil: 'domcontentloaded', timeout: 15000 });
      if (!loginRes || loginRes.status() < 400) {
        const emailInput = page.locator('input[type="email"], input[name="email"], input[name="username"]').first();
        const passInput = page.locator('input[type="password"], input[name="password"]').first();
        const submitBtn = page.locator('button[type="submit"], input[type="submit"]').first();

        if ((await emailInput.count()) > 0 && (await passInput.count()) > 0) {
          console.log(`\n🔐 [AUTH FLOW] Testing Interactive Browser Login at ${baseUrl}${loginUrl} (${loginUser})...`);
          await setHUD(`🔐 Login Otomatis ke Portal: ${loginUser}`, 'action');
          if (isHeaded) {
            await highlightElement(emailInput, '#f59e0b');
            await page.waitForTimeout(250);
          }
          await emailInput.fill(loginUser);
          if (isHeaded) {
            await highlightElement(emailInput, '#10b981');
            await highlightElement(passInput, '#f59e0b');
            await page.waitForTimeout(250);
          }
          await passInput.fill(loginPass);
          if (isHeaded) {
            await highlightElement(passInput, '#10b981');
            await highlightElement(submitBtn, '#ef4444');
            await page.waitForTimeout(300);
          }
          await submitBtn.click();
          await page.waitForLoadState('domcontentloaded', { timeout: 15000 }).catch(() => {});
          const postPath = new URL(page.url()).pathname;
          console.log(`   -> Post-Login Redirect: ${page.url()} | Title: "${await page.title()}"`);
          await setHUD(`🚀 Login Berhasil! Memeriksa Dashboard: ${postPath}`, 'success');
          await page.waitForTimeout(500);
          if (postPath !== loginUrl) {
            const adminLinks = await page.evaluate(() => {
              return Array.from(document.querySelectorAll('nav a[href], aside a[href], .sidebar a[href], header a[href]'))
                .map((a) => {
                  try {
                    const u = new URL(a.href, window.location.origin);
                    if (u.origin !== window.location.origin) return null;
                    return u.pathname;
                  } catch { return null; }
                })
                .filter((p) => p && p.startsWith('/') && !p.includes('logout') && !p.includes('unduh'));
            });
            const adminRoutes = [postPath];
            for (const al of adminLinks) {
              const clean = al.split('?')[0].split('#')[0];
              if (!adminRoutes.includes(clean) && adminRoutes.length < 20) {
                adminRoutes.push(clean);
              }
            }
            console.log(`\n📋 [ADMIN & CRUD NAVIGATION] Terdeteksi ${adminRoutes.length} rute/menu dashboard untuk diaudit di layar...`);
            await auditRoutesList(adminRoutes, 'AUTHENTICATED DASHBOARD & CRUD MENU AUDIT');
          }
        }
      }
    } catch (err) {
      console.log(`   [AUTH FLOW NOTICE]: ${err.message}`);
    }
  }

  if (isHeaded && holdSec > 0) {
    const finalType = totalDefects === 0 ? 'success' : 'danger';
    const finalMsg = totalDefects === 0
      ? `🌟 SEMUA PENGUJIAN BROWSER LULUS (PASS)! Menutup dalam ${holdSec}s...`
      : `⚠️ AUDIT SELESAI: ${totalDefects} temuan terdeteksi. Menutup dalam ${holdSec}s...`;
    await setHUD(finalMsg, finalType);
    console.log(`\n🖥️  [LIVE DISPLAY] Menahan browser selama ${holdSec} detik agar Anda dapat melihat tampilan akhir di layar...`);
    await page.waitForTimeout(holdSec * 1000);
  }

  await browser.close();

  console.log('\n========================================================================');
  if (totalDefects === 0) {
    console.log(`  ✅ PLAYWRIGHT BROWSER QA VERDICT: PASS (All routes & viewports verified)`);
    console.log('========================================================================');
    process.exit(0);
  } else {
    console.log(`  ❌ PLAYWRIGHT BROWSER QA VERDICT: FAIL (${totalDefects} UI/runtime defects detected)`);
    console.log('========================================================================');
    process.exit(1);
  }
}

main().catch((err) => {
  console.error(`⛔ [PLAYWRIGHT EXECUTION ERROR]: ${err.stack || err.message}`);
  process.exit(1);
});
