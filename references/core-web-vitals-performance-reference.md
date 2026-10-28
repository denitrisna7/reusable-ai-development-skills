# Performance Profiling & Core Web Vitals Reference

> Primary Source:
> - **Google Web Vitals (web.dev)**: https://web.dev/articles/vitals
> - Additional reference patterns adapted from `addyosmani/web-quality-skills` and `miqdadbadjuber/anti-slop` (MIT License).

This reference covers measurement discipline, Core Web Vitals thresholds, frontend rendering performance, and backend/database profiling.

---

## 1. The Cardinal Rule of Performance Engineering

**Never claim a performance improvement or report a metric score without a real baseline and post-change measurement.**
- If an application cannot be executed in the current environment, state `"not measured (static code inspection only)"` and report the structural optimization applied (e.g., removing an N+1 query inside a loop, adding a composite index, or adding `fetchpriority="high"` to the hero `<img>`).
- Never conflate a single local lab run with 75th-percentile (p75) production field data.

---

## 2. Core Web Vitals Thresholds (p75 Field Targets)

| Metric | Full Name | Dimension Measured | Good (Pass) | Needs Improvement | Poor (Fail) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LCP** | Largest Contentful Paint | Loading performance (when largest above-the-fold image/text renders) | **<= 2.5 s** | `2.5 s – 4.0 s` | `> 4.0 s` |
| **INP** | Interaction to Next Paint | Interactivity responsiveness across clicks, taps, and key presses | **<= 200 ms** | `200 ms – 500 ms` | `> 500 ms` |
| **CLS** | Cumulative Layout Shift | Visual stability (unexpected layout shifts during page lifecycle) | **<= 0.1** | `0.1 – 0.25` | `> 0.25` |

### High-Impact Frontend Mechanisms
1. **LCP Optimization**:
   - Keep Server Time to First Byte (**TTFB**) `< 800 ms` via query optimization, caching, and CDN/edge delivery.
   - Ensure the hero/LCP image is a standard `<img src="..." fetchpriority="high">` present in initial HTML—**never** `loading="lazy"` and not hidden inside late-executing client JS.
   - Eliminate render-blocking synchronous `<script>` tags and oversized unsplit CSS bundles in `<head>`.
2. **INP Optimization**:
   - Break up long main-thread tasks (`> 50 ms`); avoid synchronous heavy computation or large DOM re-renders inside click/input handlers.
   - Debounce/throttle rapid search or filter inputs while keeping immediate visual feedback.
   - Audit third-party scripts and defer non-essential hydration.
3. **CLS Optimization**:
   - Declare explicit `width` and `height` (or CSS `aspect-ratio`) on every `<img>`, `<video>`, `<iframe>`, and canvas element (`R-40`).
   - Reserve min-height containers for dynamic banners, async widgets, and skeleton placeholders.
   - Use `font-display: swap` or `optional` with size-adjusted fallback fonts.

---

## 3. Backend, Database, and Memory Profiling Reference

| Bottleneck Layer | Symptoms | Diagnostic Tools by Ecosystem | Remediation Patterns |
| :--- | :--- | :--- | :--- |
| **Database Queries** | High endpoint latency; linear query count growth with list size ($O(N)$ queries). | `EXPLAIN (ANALYZE, BUFFERS)` (PostgreSQL), `EXPLAIN FORMAT=JSON` (MySQL), Laravel Telescope/Debugbar, Django Debug Toolbar, Prisma query logs, `pg_stat_statements`. | Eager-load relations to eliminate N+1 queries; add targeted composite/covering indexes matching `WHERE` + `ORDER BY`; replace `OFFSET` pagination on deep tables with cursor/keyset pagination; select only needed columns. |
| **CPU & Serialization** | High CPU utilization under concurrency; slow JSON serialization or regex backtracking. | `py-spy` / `cProfile` (Python), `pprof` (Go), Node `--prof` / Chrome DevTools CPU profiler, `cargo flamegraph` (Rust), Blackfire / Xdebug profiler (PHP), JFR / Async-profiler (Java). | Stream large payloads instead of buffering in memory; precompile regexes and avoid catastrophic backtracking; move heavy report/export jobs to background queues. |
| **Memory & Leaks** | Growing RSS/heap over time; OOM kills during batch imports or long-lived workers. | Node Heap Snapshots, `tracemalloc` / `memray` (Python), `pprof` heap (Go), Eclipse MAT (JVM), chunked cursor iteration in PHP/Laravel (`lazy()` / `chunkById()`). | Process large datasets via generators/streams/cursors in bounded batches; clear event listeners/timers/closures; bound in-memory caches with LRU + max size. |
| **External I/O & Network** | Thread/worker pool exhaustion waiting on slow upstream APIs. | OpenTelemetry spans, HTTP client timing hooks, connection pool metrics. | Enforce explicit connect/read timeouts; reuse HTTP keep-alive connection pools; parallelize independent upstream calls where safe; cache idempotent upstream responses. |
