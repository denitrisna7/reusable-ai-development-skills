---
name: frontend-performance
description: "Profiles and optimizes frontend web and client rendering performance across Core Web Vitals (LCP, INP, CLS), asset compression, JavaScript and CSS bundle size, network request waterfalls, caching, lazy loading, and resource prioritization. Activate when diagnosing slow page loads, layout shifts, sluggish interactions, or oversized bundles. Do not use for backend SQL query tuning (use query-optimization-performance)."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-22"
  category: "Frontend and User Experience"
---

# Frontend Performance Engineering

This skill governs frontend asset delivery, Core Web Vitals (LCP, INP, CLS), rendering efficiency, JavaScript and CSS bundle minimization, network request waterfalls, browser caching, lazy loading, and resource prioritization. It enforces measurement-based optimization (`C-5`, `R-36`, `R-40`), requiring baseline and post-change evidence rather than unverified speed claims.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Diagnosing or improving Core Web Vitals: Largest Contentful Paint (**LCP <= 2.5s**), Interaction to Next Paint (**INP <= 200ms**), or Cumulative Layout Shift (**CLS <= 0.1**).
- Auditing or reducing JavaScript/CSS bundle sizes, implementing route or component code splitting, or removing heavy client dependencies.
- Optimizing images, fonts, SVGs, videos, or third-party scripts (`fetchpriority`, `loading="lazy"`, `srcset`, `preload`, `defer`/`async`).
- Eliminating client-side render waterfalls, excessive component re-renders, or main-thread jank on large lists and interactive views.

## 2. When Not to Use

Do not use this skill as the primary workflow for:
- Database SQL query plans, N+1 ORM queries, or index tuning: route to `query-optimization-performance` (`SKILL-25`).
- Server-side CPU profiling, worker memory leaks, or infrastructure autoscaling: route to `performance-profiling-optimization` (`SKILL-29`).
- Visual design token architecture or component state structure unrelated to performance: route to `ui-ux-design-systems` (`SKILL-20`).

## 3. Scope and Objectives

Every frontend performance audit or optimization must cover:
- **Asset Optimization (`R-40`)**: Serve modern image formats (`AVIF`, `WebP`) with responsive `srcset` and `sizes`, compress SVGs, subset web fonts (`woff2`, `font-display: swap` or `optional`), and declare explicit `width` and `height` (or CSS `aspect-ratio`) on every `<img>`, `<video>`, `<iframe>`, and `<canvas>` to prevent layout shift (`CLS`).
- **Lazy Loading & Hero Priority (`R-40`)**: Never apply `loading="lazy"` to the above-the-fold LCP/hero image; explicitly mark the hero image with `fetchpriority="high"` and ensure its URL is discoverable in the initial HTML document. Apply `loading="lazy"` and `decoding="async"` to below-the-fold media and heavy offscreen components.
- **Resource Prioritization**: Use `<link rel="preconnect">` sparingly (only for 1-2 critical cross-origin asset domains), `<link rel="preload">` only for critical late-discovered LCP assets or fonts, and `defer` or `async` on all third-party scripts in `<head>` so they never block first paint.
- **JavaScript & CSS Bundle Size**: Enforce route-level and heavy-widget code splitting (`React.lazy`, dynamic `import()`), tree-shake icon and utility libraries (never import entire barrel modules when build tooling cannot tree-shake them), purge unused CSS, and inline or prioritize critical CSS where appropriate.
- **Rendering Efficiency & Main-Thread Responsiveness (`INP`)**: Avoid unnecessary component re-renders, keep input/click handlers under `50ms` on the main thread, virtualize long lists/tables (`> 100` complex rows), and debounce/throttle expensive filter or resize computations.
- **Network Requests & Waterfall Elimination**: Replace sequential client-side `fetch` chains (`Component A mounts -> fetches -> mounts Child B -> fetches`) with parallel data loading, server-side data fetching, or prefetching on intent. Enable Brotli (`br`) or Gzip compression on text assets.
- **Caching Strategy**: Configure long-lived immutable caching (`Cache-Control: public, max-age=31536000, immutable`) for content-hashed static bundles (`app.[hash].js`), paired with short-lived or revalidated caching (`no-cache` or `stale-while-revalidate`) for HTML entrypoints.
- **Profiling & Measurable Improvements (`C-5`, `R-36`)**: Measure bundle sizes, network waterfalls, or Web Vitals before and after changes. Never invent Lighthouse scores or percentage improvements without real execution output.

## 4. Prerequisites and Context Requirements

Before applying frontend performance changes, inspect:
1. **Build & Bundler Configuration**: `vite.config.*`, `next.config.*`, `webpack.config.*`, `nuxt.config.*`, `angular.json`, `composer.json` / `package.json`, and production build output directories (`dist/`, `.next/`, `public/build/`).
2. **Entrypoint HTML & Layout Templates**: Root `<head>` tags, font declarations, third-party analytics/tag scripts, and hero section markup.
3. **Data Fetching & State Layer**: How pages fetch initial data (SSR, SSG, RSC, client-side `useEffect`, TanStack Query, SWR, Livewire, HTMX).

## 5. Step-by-Step Workflow

### Step 1: Establish a Verifiable Baseline (`C-5`)
- [ ] Run the production build (`npm run build`, `pnpm build`, `flutter build web`, etc.) to capture exact baseline chunk sizes (`kB` raw and gzipped/brotli).
- [ ] If a live server and browser are available, inspect network requests (`browser_network_requests`) and console diagnostics via `playwright-mcp-browser-qa` (`SKILL-17`) or Chrome DevTools / Lighthouse.
- [ ] If the app cannot be run live in the current environment, record static baseline evidence (bundle sizes from build output or static code defects such as missing image dimensions or render-blocking scripts) and label runtime metrics as `"not measured (static inspection only)"`.

### Step 2: Optimize LCP, Media Assets, and Resource Prioritization (`R-40`)
- [ ] Locate the primary above-the-fold hero element on each target route:
  - Ensure hero `<img>` tags have `fetchpriority="high"`, explicit `width` and `height`, and **no** `loading="lazy"`.
  - Avoid hiding the LCP image inside a client-only JS bundle or CSS `background-image` that waits for JS execution.
- [ ] Audit all below-the-fold `<img>` and `<iframe>` elements: add `loading="lazy"`, `decoding="async"`, explicit `width`/`height` (or `aspect-ratio`), and responsive `srcset`/`sizes` or modern formats (`AVIF`/`WebP`).
- [ ] Inspect `<head>` for render-blocking `<script>` tags and external stylesheets: add `defer` or `async` to non-critical scripts, and remove unused `<link rel="preconnect">` or `<link rel="preload">` tags.

### Step 3: Reduce Bundle Size and Network Waterfalls
- [ ] Analyze the largest JS/CSS chunks from the build output:
  - Split heavy route-specific libraries (charting engines, rich text editors, PDF viewers, map SDKs, date-manipulation libraries) behind dynamic `import()`.
  - Replace full-library imports with specific submodules or lightweight native browser APIs (`Intl.DateTimeFormat`, `Intl.NumberFormat`, `structuredClone`, `URLSearchParams`).
- [ ] Inspect data-fetching hooks and route loaders to eliminate sequential request waterfalls: initiate independent requests in parallel (`Promise.all`) or lift fetching to the route/server loader.

### Step 4: Optimize CLS and INP (Rendering & Interactivity)
- [ ] Verify every dynamic slot (skeleton loaders, async banners, third-party embeds, web fonts) reserves its exact layout height (`min-h-[...]`, `aspect-ratio`) so content below never jumps after load (`CLS <= 0.1`).
- [ ] Audit slow event handlers (`onClick`, `onInput`, `onChange`): keep synchronous UI state updates fast, defer heavy filtering (`useDeferredValue` / `startTransition` or requestAnimationFrame/debounce), and apply windowing/virtualization to tables or lists rendering hundreds of complex DOM nodes.
- [ ] Replace layout-thrashing CSS animations (`top`, `left`, `width`, `height`) with compositor-friendly properties (`transform`, `opacity`).

### Step 5: Verify Build Output and Post-Change Metrics
- [ ] Re-run the production build and compare chunk sizes against Step 1.
- [ ] Verify that code-split components include loading fallback boundaries (`<Suspense>` or skeleton placeholders) and that no console or runtime hydration errors were introduced.

## 6. Technology-Specific Adaptation Rules

| Stack / Ecosystem | Frontend Performance Adaptation | Verification & Tooling |
| :--- | :--- | :--- |
| **Next.js / React / Remix / Vite** | Use framework `<Image priority>` (for LCP) or standard `<img fetchpriority="high" width height>`, React Server Components or route `loader`s to eliminate client waterfalls, `dynamic()` / `React.lazy()` for heavy modals/charts, and `useTransition` for expensive UI filtering. | `next build` route size table, `vite-bundle-visualizer` / `rollup-plugin-visualizer`, Lighthouse / Web Vitals. |
| **Vue / Nuxt / SvelteKit / Angular** | Use `defineAsyncComponent` (Vue), `<NuxtImg preload>`, SvelteKit `load` functions, or Angular `@defer (on viewport)` blocks for below-the-fold heavy components. | `nuxt analyze`, `vite build`, Angular build budgets in `angular.json`. |
| **Laravel (Blade / Livewire / Inertia) & CodeIgniter** | Use Vite (`@vite`) with hashed assets, Livewire `#[Lazy]` components for heavy dashboard widgets, Inertia partial reloads (`only: [...]`), and native `<img width height loading="lazy">` in templates. | `npm run build` Vite manifest output, browser network waterfall inspection. |
| **Python (Django / FastAPI / Jinja2) / Go / Rails** | Enable `ManifestStaticFilesStorage` / WhiteNoise (Django) or hashed asset pipelines with Brotli/Gzip and `Cache-Control: immutable`; use HTMX partial swaps instead of full-page reloads where appropriate. | Static asset manifest verification, HTTP response header checks. |
| **Java / Spring, C# / .NET, Rust Web Apps** | Enable versioned static resource resolvers (`ResourceUrlEncodingFilter`, `asp-append-version="true"`), HTTP response compression (Brotli/Gzip), and precompressed static assets. | Build artifact size inspection and response header verification. |
| **Flutter (Mobile & Web)** | Use `ListView.builder` / `SliverList.builder` for lazy viewport rendering, `const` constructors to prevent widget rebuilds, `RepaintBoundary` around animations, and `precacheImage` for critical visuals. | `flutter build web --analyze-size`, Flutter DevTools Performance overlay. |

### Core Web Vitals Engineering Checklist

1. **Largest Contentful Paint (`LCP <= 2.5s`)**:
   - Server TTFB is `< 800ms`.
   - Hero image is in initial HTML with `fetchpriority="high"` and without `loading="lazy"`.
   - Critical CSS is small and non-critical `<script>` tags use `defer` or `async`.
   - Web fonts use `woff2` with `font-display: swap` or `optional` and preconnect/preload only for the primary body/heading font.
2. **Interaction to Next Paint (`INP <= 200ms`)**:
   - Event callbacks (`click`, `keydown`, `input`) yield to the browser main thread within `50ms`.
   - Heavy list filtering, sorting, or chart re-computation is debounced, virtualized, or wrapped in non-blocking transitions.
   - Hydration does not freeze the main thread via oversized client state payloads.
3. **Cumulative Layout Shift (`CLS <= 0.1`)**:
   - Every `<img>`, `<video>`, `<iframe>`, and ad/embed container reserves explicit `width`/`height` or `aspect-ratio`.
   - Dynamic alerts, banners, and skeleton placeholders match the dimensions of the final rendered content.
   - Animations only mutate `transform` and `opacity`, never layout geometry (`top`, `left`, `height`, `margin`).

## 7. Security and Safety Considerations

- **Cache Poisoning & Private Data Safety**: Never set `Cache-Control: public` on HTML responses, API endpoints, or SSR payloads that contain authenticated user data, CSRF tokens, or session state. Use `Cache-Control: private, no-store` for sensitive authenticated responses, and reserve `public, max-age=31536000, immutable` strictly for content-hashed static files (`.js`, `.css`, `.woff2`, public images).
- **Subresource Integrity (SRI) & Third-Party Scripts**: When loading scripts from external CDNs, include `integrity="sha384-..."` and `crossorigin="anonymous"`, and audit third-party tags so performance optimizations do not introduce untrusted script execution.
- **Font & Asset Privacy**: Prefer self-hosted fonts (`woff2`) over third-party font CDNs when privacy policies or GDPR requirements restrict leaking visitor IPs to external origins.

## 8. Verification Criteria

Before claiming a frontend performance improvement:
1. **Measured Evidence (`C-5`, `R-36`)**: Report exact before/after bundle sizes (in `kB`) from the build tool or measured timing/Web Vitals metrics from an actual run. If runtime measurement was not possible, state `"not measured (static inspection only)"` and list the exact structural fixes applied.
2. **Hero & Media Compliance (`R-40`)**: The LCP hero image uses `fetchpriority="high"` and is not lazy-loaded; all `<img>`, `<video>`, and `<iframe>` tags declare explicit dimensions (`width`/`height` or `aspect-ratio`).
3. **Zero Regression**: Production build succeeds and interactive flows work without hydration mismatches, broken dynamic imports, or console errors.

## 9. Failure Handling and Edge Cases

- **Code Splitting Hydration or Chunk Load Errors**: When deploying new hashed chunks, long-lived open browser tabs may request an outdated chunk URL during navigation. Configure the router/error boundary to catch `ChunkLoadError` and trigger a clean full-page navigation to the target URL.
- **Over-Preloading**: Preloading too many fonts or images competes with the critical HTML/CSS path and degrades LCP on mobile networks. Restrict `<link rel="preload">` to at most 1-2 critical resources discovered late by the browser parser.
- **Virtualization vs. Accessibility / Ctrl+F**: Only virtualize lists when DOM node counts genuinely cause measurable main-thread lag (`> 100-200` complex rows), and ensure keyboard navigation and pagination alternatives remain accessible.

## 10. Expected Outputs and Reporting Requirements

Report frontend performance work using the following template:

```markdown
## Frontend Performance Report

### 1. Baseline vs. Post-Change Measurements
- **Measurement Mode**: [Live Browser + Production Build / Production Build Only / Static Code Inspection Only]
| Metric / Asset | Baseline | Post-Change | Delta | Status |
| :--- | :--- | :--- | :--- | :--- |
| [e.g., Main JS Bundle (gzip)] | `248.4 kB` | `142.1 kB` | `-106.3 kB (-42.8%)` | PASS |
| [e.g., Hero LCP Image Attributes] | `loading="lazy"`, no size | `fetchpriority="high"`, `1200x630` | Structural Fix | PASS |
| [e.g., LCP / INP / CLS] | [Value or Not Measured] | [Value or Not Measured] | [Delta] | [Status] |

### 2. Optimizations Applied
- **Asset & LCP Prioritization (`R-40`)**: [Summary of image, font, and script priority changes]
- **Bundle & Waterfall Reduction**: [Summary of code splitting, tree shaking, and parallel fetching]
- **Rendering & CLS Stability**: [Summary of dimension reservation, memoization, or virtualization]
- **Caching & Compression**: [Summary of Cache-Control headers or static asset hashing]

### 3. Verification & Residual Risks
- **Production Build Check**: [Command run & exit status]
- **Unmeasured / Environment Limitations**: [Explicitly list any metrics that require staging/field telemetry]
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - `ui-ux-design-systems` (`SKILL-20`): Supplies the component architecture and loading skeleton states (`R-27`).
- **Downstream / Co-Activated Skills**:
  - `cross-browser-responsive-qa` (`SKILL-23`) and `playwright-mcp-browser-qa` (`SKILL-17`): Verifies that lazy-loaded images, responsive `srcset` attributes, and code-split routes render properly across viewports.
  - `query-optimization-performance` (`SKILL-25`) and `performance-profiling-optimization` (`SKILL-29`): Route here when slow page loads originate from high server TTFB (`> 800ms`) or slow API endpoints.

## 12. Source References

- **Google Web Vitals (LCP, INP, CLS)**: https://web.dev/articles/vitals
- **Optimize Largest Contentful Paint (web.dev)**: https://web.dev/articles/optimize-lcp
- **Optimize Interaction to Next Paint (web.dev)**: https://web.dev/articles/optimize-inp
- **Optimize Cumulative Layout Shift (web.dev)**: https://web.dev/articles/optimize-cls
- **Shared Library Reference (Core Web Vitals & Performance)**: [../../references/core-web-vitals-performance-reference.md](../../references/core-web-vitals-performance-reference.md)
- **Shared Library Reference (Anti-Slop Engineering `R-36`, `R-40`)**: [../../references/anti-slop-engineering-reference.md](../../references/anti-slop-engineering-reference.md)
