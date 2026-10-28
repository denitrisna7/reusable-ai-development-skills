# Core Web Vitals Field vs. Lab Diagnostics Reference

> Primary Source: https://web.dev/articles/vitals

This reference provides deep diagnostic breakdowns for Largest Contentful Paint (LCP), Interaction to Next Paint (INP), and Cumulative Layout Shift (CLS), distinguishing between Real User Monitoring (RUM / Field data) and synthetic Lab benchmarks.

---

## 1. Field Data vs. Lab Data Discipline

| Dimension | Field Data (RUM / CrUX) | Lab Data (Lighthouse / Playwright / DevTools) |
| :--- | :--- | :--- |
| **Environment** | Real end-user devices, varied CPU/network conditions, live user interactions. | Controlled, repeatable synthetic environment with fixed throttling profiles. |
| **Evaluation Target** | **75th percentile (p75)** across all page loads or interactions. | Single run or median of 3-5 synthetic runs under simulated throttling. |
| **Primary Strengths** | Captures actual user experience, real INP across full page lifetime, post-hydration shifts. | Reproduces cold-load regressions before deployment; provides flamecharts and network waterfalls. |
| **Blind Spots** | Lagging indicator; requires production traffic volume. | Misses post-scroll CLS and real user click/keyboard patterns unless scripted. |

**Mandatory Engineering Rule**: Never claim that a local unthrottled browser load proves p75 production Core Web Vitals compliance. Always specify the environment, throttling settings, and sample count when reporting lab metrics.

---

## 2. Largest Contentful Paint (LCP) Sub-Part Breakdown

Target at p75: **`LCP <= 2.5 seconds`** (Needs Improvement: `2.5s - 4.0s`, Poor: `> 4.0s`).

To optimize LCP systematically, decompose total LCP time into four sequential sub-parts that must sum to `<= 2.5s`:

1. **Time to First Byte (TTFB) (~40% budget, target `< 800 ms`)**:
   - **Causes of delay**: Slow database queries, uncached SSR responses, multiple redirect hops, cold serverless functions, missing CDN edge caching.
   - **Fixes**: Optimize backend queries (`EXPLAIN ANALYZE`), cache rendered HTML or expensive data payloads, minimize redirects, enable HTTP/2 or HTTP/3, and use `103 Early Hints` where supported.
2. **Resource Load Delay (< 10% budget)**:
   - **Causes of delay**: The LCP image URL is hidden inside an external CSS `background-image`, injected late by client-side JavaScript, or deprioritized behind other assets.
   - **Fixes**: Render the LCP image directly in initial SSR/static HTML using `<img src="..." fetchpriority="high">`. If the image must come from CSS or responsive sources, inject `<link rel="preload" as="image" href="..." fetchpriority="high">` in `<head>`.
3. **Resource Load Duration (~40% budget)**:
   - **Causes of delay**: Uncompressed PNG/JPEG hero assets, missing responsive `srcset` serving desktop-sized images to mobile viewports, no CDN compression.
   - **Fixes**: Convert images to modern formats (`AVIF`, `WebP`), define accurate `srcset` and `sizes` attributes, compress assets, and serve from an edge CDN sharing the primary origin connection (or `<link rel="preconnect">`).
4. **Element Render Delay (< 10% budget)**:
   - **Causes of delay**: Render-blocking synchronous `<script>` or large unsplit `<link rel="stylesheet">` tags in `<head>`, or heavy client hydration blocking paint after the image bytes arrive.
   - **Fixes**: Inline critical CSS, defer non-critical scripts (`defer` or `async`), remove `loading="lazy"` from the hero/LCP element, and reduce synchronous main-thread work during initial bootstrap.

---

## 3. Interaction to Next Paint (INP) Sub-Part Breakdown

Target at p75: **`INP <= 200 milliseconds`** (Needs Improvement: `200ms - 500ms`, Poor: `> 500ms`).

INP measures the worst (or 98th percentile on high-interaction pages) latency of any `click`, `tap`, or `keydown` interaction across the entire page lifecycle. Each interaction consists of three phases:

1. **Input Delay**:
   - Time between the hardware input event and the start of the event handler execution.
   - **Causes**: Long tasks (`> 50 ms`) already occupying the main thread (hydration, third-party analytics/ads scripts, large bundle evaluation, excessive timer callbacks).
   - **Fixes**: Break up initialization bundles via code-splitting, defer third-party scripts until idle, and yield to the main thread (`scheduler.yield()` or `setTimeout(0)`).
2. **Processing Duration**:
   - Time spent executing all synchronous callbacks bound to the interaction event.
   - **Causes**: Re-rendering huge component trees on every keystroke, synchronous JSON parsing/sorting in event handlers, unthrottled state mutations.
   - **Fixes**: Update minimal UI state immediately to show visual acknowledgment, offload heavy filtering/sorting to Web Workers or debounced async tasks, and avoid forced synchronous layouts (`offsetWidth`, `getBoundingClientRect` immediately after DOM writes).
3. **Presentation Delay**:
   - Time from when event callbacks finish until the browser paints the next frame on screen.
   - **Causes**: Excessive DOM size (`> 1,500` nodes in active view), complex CSS selectors, expensive `box-shadow`/`filter: blur()` repaints across large surfaces.
   - **Fixes**: Virtualize long lists and tables, use `content-visibility: auto` for off-screen sections, and keep DOM depth shallow.

---

## 4. Cumulative Layout Shift (CLS) Diagnostic Checklist

Target at p75: **`CLS <= 0.1`** (Needs Improvement: `0.1 - 0.25`, Poor: `> 0.25`).

CLS is the product of the *impact fraction* and *distance fraction* of unexpected layout shifts (shifts that do not occur within `500 ms` of direct user input).

- **Media without dimensions**: Always specify explicit `width` and `height` HTML attributes or CSS `aspect-ratio` on every `<img>`, `<video>`, `<iframe>`, and `<canvas>`.
- **Late-injected dynamic content**: Reserve fixed or `min-height` slots for cookie banners, promo bars, notification toasts, and async embeds so they do not push existing content down.
- **Web font swap shifts (FOIT/FOUT)**: Pair `font-display: swap` or `font-display: optional` with metric-compatible fallback fonts (`size-adjust`, `ascent-override`, `descent-override`) or preload critical primary WOFF2 fonts.
- **Non-composited animations**: Never animate layout properties (`top`, `left`, `width`, `height`, `margin`). Animate only compositor-friendly properties (`transform: translate3d(...)`, `scale(...)`, `opacity`).
