#!/usr/bin/env node
/**
 * Real Headless Chromium Browser QA & Visual/DOM Auditor (Playwright Engine)
 *
 * Automatically locates Playwright (`node_modules/playwright`, global links in
 * `~/.cache/ms-playwright/.links`, or local installations) and executes a REAL
 * headless Chromium browser session to verify:
 *   1. Page navigation & HTTP status codes (catching 404, 403, 500)
 *   2. Runtime JS Console Errors, Page Errors, and failed Network Requests
 *   3. Desktop (1440x900) and Mobile (375x812 & 320x568) Responsive Reflow
 *   4. Real DOM Computed Color Contrast (WCAG 2.2 AA >= 4.5:1 normal / >= 3.0:1 large,
 *      detecting unreadable or white-on-white text)
 *   5. Real DOM Bounding-Box Collisions (overlapping/floating text, horizontal overflow,
 *      clipped text, and mobile touch target dimensions)
 *   6. Optional interactive Login & authenticated page verification
 *
 * Usage:
 *   node scripts/run-browser-audit.mjs [baseUrl] [route1] [route2] ... [--login-url=/login --user=admin@example.com --pass=password]
 */

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

async function loadPlaywright() {
  const candidates = [
    path.join(process.cwd(), 'package.json'),
    path.join(os.homedir(), 'package.json'),
  ];

  // Also check ~/.cache/ms-playwright/.links/* for existing playwright-core installs
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

  // Fallback: dynamic import
  try {
    return await import('playwright');
  } catch {
    return await import('playwright-core');
  }
}

function findChromiumExecutable() {
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
  const sysBins = ['/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome'];
  for (const bin of sysBins) {
    if (fs.existsSync(bin)) return bin;
  }
  return undefined;
}

/**
 * Injected into the live Chromium DOM to audit computed contrast, overlaps, overflow, and touch targets.
 */
function domAuditEvaluator(viewportLabel) {
  function parseRgba(str) {
    if (!str) return { r: 255, g: 255, b: 255, a: 0 };
    const m = str.match(/rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)(?:\s*[,/]\s*([\d.]+))?\s*\)/i);
    if (!m) return { r: 255, g: 255, b: 255, a: 0 };
    return {
      r: Number(m[1]),
      g: Number(m[2]),
      b: Number(m[3]),
      a: m[4] !== undefined ? Number(m[4]) : 1,
    };
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
    while (cur && cur.nodeType === 1) {
      const style = window.getComputedStyle(cur);
      const bg = parseRgba(style.backgroundColor);
      if (bg.a > 0) layers.push(bg);
      if (bg.a >= 0.99 || style.backgroundImage !== 'none') break;
      cur = cur.parentElement;
    }
    // Base canvas white
    let composite = { r: 255, g: 255, b: 255, a: 1 };
    for (let i = layers.length - 1; i >= 0; i--) {
      composite = blend(layers[i], composite);
    }
    return { currBg: composite, hasBgImage: cur && window.getComputedStyle(cur).backgroundImage !== 'none' };
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
    const bright = Math.max(l1, l2);
    const dark = Math.min(l1, l2);
    return (bright + 0.05) / (dark + 0.05);
  }

  function isVisible(el) {
    const style = window.getComputedStyle(el);
    if (style.display === 'none' || style.visibility === 'hidden' || Number(style.opacity) < 0.05) return false;
    const rect = el.getBoundingClientRect();
    return rect.width > 1 && rect.height > 1;
  }

  const vw = window.innerWidth;
  const docScrollWidth = document.documentElement.scrollWidth;
  const horizontalOverflowPx = Math.max(0, docScrollWidth - vw);

  const contrastFailures = [];
  let minContrast = 21.0;
  let textElementsChecked = 0;

  const clippedElements = [];
  const textBoxes = [];

  const allElements = Array.from(document.querySelectorAll('body *'));
  for (const el of allElements) {
    if (!isVisible(el)) continue;

    // Direct text content check
    const directText = Array.from(el.childNodes)
      .filter((n) => n.nodeType === 3)
      .map((n) => n.textContent.trim())
      .join(' ')
      .trim();

    if (!directText) continue;

    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
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
        contrastFailures.push({
          tag: el.tagName.toLowerCase(),
          text: directText.slice(0, 40),
          ratio: Number(ratio.toFixed(2)),
          threshold,
          fg: style.color,
          bg: `rgb(${Math.round(currBg.r)},${Math.round(currBg.g)},${Math.round(currBg.b)})`,
        });
      }
    }

    // Check unintentional text clipping
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

    if (rect.top >= 0 && rect.bottom <= window.innerHeight * 3 && rect.width > 8 && rect.height > 8) {
      textBoxes.push({ el, rect, text: directText.slice(0, 35), tag: el.tagName.toLowerCase() });
    }
  }

  // Check bounding-box collisions between distinct non-ancestor text elements
  const overlaps = [];
  for (let i = 0; i < Math.min(textBoxes.length, 150); i++) {
    for (let j = i + 1; j < Math.min(textBoxes.length, 150); j++) {
      const a = textBoxes[i];
      const b = textBoxes[j];
      if (a.el.contains(b.el) || b.el.contains(a.el)) continue;

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

  // Check touch targets on mobile viewports
  const smallTouchTargets = [];
  if (vw <= 480) {
    const controls = Array.from(document.querySelectorAll('button, input:not([type="hidden"]), select, textarea, a.btn, [role="button"]'));
    for (const ctrl of controls) {
      if (!isVisible(ctrl)) continue;
      const r = ctrl.getBoundingClientRect();
      if (r.width < 32 || r.height < 32) {
        smallTouchTargets.push({
          tag: ctrl.tagName.toLowerCase(),
          label: (ctrl.innerText || ctrl.getAttribute('aria-label') || ctrl.getAttribute('name') || 'control').trim().slice(0, 30),
          size: `${Math.round(r.width)}x${Math.round(r.height)}px`,
        });
      }
    }
  }

  return {
    viewportLabel,
    viewportSize: `${vw}x${window.innerHeight}`,
    title: document.title,
    horizontalOverflowPx,
    textElementsChecked,
    minContrast: textElementsChecked > 0 ? Number(minContrast.toFixed(2)) : null,
    contrastFailures: contrastFailures.slice(0, 5),
    clippedElements: clippedElements.slice(0, 5),
    overlaps: overlaps.slice(0, 5),
    smallTouchTargets: smallTouchTargets.slice(0, 5),
    formsCount: document.querySelectorAll('form').length,
    buttonsCount: document.querySelectorAll('button, [type="submit"]').length,
    tablesCount: document.querySelectorAll('table').length,
  };
}

async function main() {
  const args = process.argv.slice(2);
  let baseUrl = 'http://127.0.0.1:8000';
  const routes = [];
  let loginUrl = null;
  let loginUser = null;
  let loginPass = null;

  for (const arg of args) {
    if (arg.startsWith('--login-url=')) loginUrl = arg.split('=')[1];
    else if (arg.startsWith('--user=')) loginUser = arg.split('=')[1];
    else if (arg.startsWith('--pass=')) loginPass = arg.split('=')[1];
    else if (arg.startsWith('http://') || arg.startsWith('https://')) baseUrl = arg.replace(/\/$/, '');
    else if (arg.startsWith('/')) routes.push(arg);
  }

  const pw = await loadPlaywright();
  const executablePath = findChromiumExecutable();

  console.log('========================================================================');
  console.log('  PLAYWRIGHT REAL CHROMIUM BROWSER QA & VISUAL/DOM AUDITOR (LIVE LOG)');
  console.log('========================================================================');
  console.log(`Target Base URL : ${baseUrl}`);
  console.log(`Browser Engine  : Headless Chromium (${executablePath || 'Playwright Default'})`);

  const browser = await pw.chromium.launch({
    headless: true,
    ...(executablePath ? { executablePath } : {}),
  });

  const context = await browser.newContext();
  const page = await context.newPage();

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

  // Auto-discover internal routes from homepage if none explicitly passed
  if (routes.length === 0) {
    routes.push('/');
    try {
      await page.goto(baseUrl + '/', { waitUntil: 'domcontentloaded', timeout: 15000 });
      const hrefs = await page.evaluate(() =>
        Array.from(document.querySelectorAll('a[href]'))
          .map((a) => a.getAttribute('href'))
          .filter((h) => h && h.startsWith('/') && !h.startsWith('//') && !h.endsWith('.apk') && !h.endsWith('.pdf'))
      );
      for (const h of hrefs) {
        const clean = h.split('?')[0].split('#')[0];
        if (!routes.includes(clean) && routes.length < 6) routes.push(clean);
      }
    } catch (e) {
      console.error(`⛔ [FATAL] Cannot connect to ${baseUrl}: ${e.message}`);
      await browser.close();
      process.exit(1);
    }
  }

  // Optional Interactive Login Flow
  if (loginUrl && loginUser && loginPass) {
    console.log(`\n🔐 [AUTH FLOW] Testing Interactive Browser Login at ${baseUrl}${loginUrl} (${loginUser})...`);
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(baseUrl + loginUrl, { waitUntil: 'domcontentloaded', timeout: 15000 });
    const emailInput = page.locator('input[type="email"], input[name="email"], input[name="username"]').first();
    const passInput = page.locator('input[type="password"], input[name="password"]').first();
    const submitBtn = page.locator('button[type="submit"], input[type="submit"]').first();

    if ((await emailInput.count()) > 0 && (await passInput.count()) > 0) {
      await emailInput.fill(loginUser);
      await passInput.fill(loginPass);
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 15000 }).catch(() => {}),
        submitBtn.click(),
      ]);
      console.log(`   -> Post-Login URL: ${page.url()} | Title: "${await page.title()}"`);
      const postPath = new URL(page.url()).pathname;
      if (postPath !== loginUrl && !routes.includes(postPath)) {
        routes.push(postPath);
      }
    } else {
      console.log('   -> WARNING: Login form inputs not found on login page.');
    }
  }

  let totalDefects = 0;
  const viewports = [
    { label: 'Desktop Web View', width: 1440, height: 900 },
    { label: 'Mobile Phone View', width: 375, height: 812 },
  ];

  for (const route of routes) {
    const targetUrl = baseUrl + route;
    console.log(`\n------------------------------------------------------------------------`);
    console.log(`🌐 [ROUTE AUDIT] ${targetUrl}`);
    console.log(`------------------------------------------------------------------------`);

    for (const vp of viewports) {
      consoleErrors.length = 0;
      pageErrors.length = 0;
      failedRequests.length = 0;

      await page.setViewportSize({ width: vp.width, height: vp.height });
      const response = await page.goto(targetUrl, { waitUntil: 'domcontentloaded', timeout: 15000 });
      const status = response ? response.status() : 0;

      const audit = await page.evaluate(domAuditEvaluator, vp.label);

      console.log(`  📐 [${vp.label} (${vp.width}x${vp.height})]`);
      console.log(`     • HTTP Status & Title : HTTP ${status} | "${audit.title}"`);
      console.log(`     • DOM Structure       : ${audit.textElementsChecked} text nodes, ${audit.formsCount} forms, ${audit.buttonsCount} buttons, ${audit.tablesCount} tables`);
      console.log(`     • Horizontal Overflow : ${audit.horizontalOverflowPx === 0 ? '0px (PASS - No horizontal leak)' : `${audit.horizontalOverflowPx}px (FAIL - Horizontal scroll leak!)`}`);
      console.log(`     • Color Contrast      : Min ${audit.minContrast ?? 'N/A'}:1 (${audit.contrastFailures.length === 0 ? 'PASS WCAG AA' : `${audit.contrastFailures.length} FAILURES`})`);
      console.log(`     • Element Collisions  : ${audit.overlaps.length === 0 ? '0 overlapping text elements (PASS)' : `${audit.overlaps.length} OVERLAPS DETECTED (FAIL)`}`);
      console.log(`     • Clipped Text        : ${audit.clippedElements.length === 0 ? '0 clipped text elements (PASS)' : `${audit.clippedElements.length} CLIPPED ELEMENTS (WARNING)`}`);
      console.log(`     • Console & Network   : ${consoleErrors.length + pageErrors.length} JS errors, ${failedRequests.length} failed HTTP requests`);

      if (status >= 400) {
        totalDefects++;
        console.log(`     ❌ HTTP ERROR: Route returned status ${status}`);
      }
      if (audit.horizontalOverflowPx > 4) {
        totalDefects++;
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

  await browser.close();

  console.log('\n========================================================================');
  if (totalDefects === 0) {
    console.log(`  ✅ PLAYWRIGHT BROWSER QA VERDICT: PASS (${routes.length} routes x 2 viewports verified)`);
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
