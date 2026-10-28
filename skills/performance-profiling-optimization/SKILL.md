---
name: performance-profiling-optimization
description: Establishes baseline performance metrics, profiles CPU, memory, database, and network bottlenecks, and applies verified optimizations including Core Web Vitals (LCP, INP, CLS). Activate when diagnosing slow endpoints, memory leaks, high latency, or frontend rendering bottlenecks. Do not use for purely SQL index design without broader profiling or initial UI layout styling.
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-29"
  category: "Performance, Operations, and Deployment"
---

# Performance Profiling & Optimization

This skill governs end-to-end performance engineering across frontend, backend, database, and network layers. It enforces strict measurement discipline: establishing empirical baselines, isolating bottlenecks through profiling, applying targeted optimizations, and verifying improvements against quantitative targets including Core Web Vitals (`LCP <= 2.5s`, `INP <= 200ms`, `CLS <= 0.1` at p75). It strictly prohibits claiming performance gains without supporting measurements.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Investigating slow API endpoints, sluggish page loads, high server CPU utilization, or elevated memory consumption.
- Auditing or optimizing Core Web Vitals (Largest Contentful Paint, Interaction to Next Paint, Cumulative Layout Shift) for web applications.
- Running or interpreting CPU flamegraphs, heap snapshots, allocation profiles, or request waterfalls.
- Eliminating N+1 query bottlenecks, excessive payload serialization, memory leaks, or synchronous I/O blocking in request paths.
- Establishing performance baselines and automated regression budgets prior to production release.

## 2. When Not to Use

Do not activate this skill when the task is strictly limited to:
- Designing or normalizing relational database schemas without a performance bottleneck (route to `database-architecture-integrity`, `SKILL-24`).
- Deep SQL query plan rewriting and index creation in isolation (route to `query-optimization-performance`, `SKILL-25`, or use alongside this skill).
- Implementing queue workers, cron jobs, or distributed cache invalidation architecture (route to `caching-background-jobs`, `SKILL-30`).
- Visual UI styling, typography, or layout design unrelated to rendering speed or layout shifts (route to `ui-ux-design-systems`, `SKILL-20`).

## 3. Scope and Objectives

Every performance investigation and optimization executed under this skill must cover:
- **Baseline Measurement**: Capturing reproducible pre-change metrics (latency percentiles p50/p95/p99, throughput, memory RSS/heap, query count, bundle size, or lab Web Vitals) before altering code.
- **Systematic Profiling**: Using stack-appropriate profilers and tracing tools to identify where execution time or memory is actually spent rather than guessing.
- **Bottleneck Identification**: Pinpointing the exact constraining resource (CPU computation, heap allocation, database lock/scan, network RTT, or main-thread rendering).
- **CPU and Memory Optimization**: Eliminating redundant loops, quadratic algorithms ($O(N^2)$), unbounded in-memory buffering, unclosed streams, and retained object references.
- **Database Latency Reduction**: Resolving N+1 queries, over-fetching columns/rows, missing composite indexes, and unbatched write loops.
- **Network Performance**: Minimizing payload sizes, enabling compression (`Brotli`/`Gzip`), reusing HTTP keep-alive connections, eliminating waterfall chains, and configuring caching headers.
- **Core Web Vitals Compliance**: Enforcing `LCP <= 2.5s`, `INP <= 200ms`, and `CLS <= 0.1` at the 75th percentile (p75) for web interfaces, backed by structural HTML/CSS/JS optimizations.
- **Measurable Improvements**: Comparing post-change measurements against the initial baseline under identical workload and hardware conditions.
- **Regression Monitoring**: Defining performance budgets, CI size/latency checks, or APM alerts so resolved bottlenecks do not silently return.

## 4. Prerequisites and Context Requirements

Before applying performance optimizations, gather and confirm:
1. **Target Workload & SLA**: Which route, job, query, or user interaction is slow, and what are the target latency, throughput, or memory thresholds?
2. **Execution Environment Access**: Determine whether a live runtime, local dev server, benchmark harness, or database engine is available to run measurements, or if analysis is restricted to static code inspection.
3. **Dataset Scale**: Confirm realistic data volumes (row counts, payload sizes, concurrent users), because optimizations that behave well on 10 rows often fail on 1,000,000 rows.

## 5. Step-by-Step Workflow

### Step 1: Establish the Baseline Measurement
- [ ] Record the exact command, endpoint, test dataset size, and environment conditions before modifying any code.
- [ ] Capture quantitative baseline metrics:
  - **Backend/API**: Request duration (p50, p95, p99), SQL query count per request, total DB time, peak memory allocation, and response byte size.
  - **Frontend/Web**: TTFB, FCP, LCP, INP/TBT, CLS, total JS/CSS transfer size, and DOM node count (see `[references/core-web-vitals.md](references/core-web-vitals.md)`).
- [ ] If the environment prevents code execution, explicitly record Baseline Status as `"Not measured (static code inspection only)"` and document the structural complexity instead (e.g., $O(N)$ queries inside a loop).

### Step 2: Profile and Isolate the Primary Bottleneck
- [ ] Profile the hot path to separate symptoms from root causes:
  - **Database Layer**: Inspect slow query logs and run `EXPLAIN (ANALYZE, BUFFERS)` or `EXPLAIN FORMAT=JSON` to detect full table scans, filesorts, or N+1 query loops.
  - **CPU & Application Logic**: Capture a CPU profile or timing breakdown to spot heavy serialization, regex backtracking, synchronous crypto/hashing in loops, or repeated parsing.
  - **Memory & Garbage Collection**: Inspect heap snapshots or memory allocation traces to identify large in-memory collections, unchunked file/query loads, or event listener leaks.
  - **Network & Frontend Waterfall**: Inspect network request waterfalls and main-thread flamecharts for render-blocking scripts, late-discovered LCP images, or synchronous long tasks (`> 50 ms`).
- [ ] Rank identified bottlenecks by total percentage of execution time or memory consumed. Optimize the top bottleneck first.

### Step 3: Apply Targeted Optimizations
- [ ] **Database & Data Access**:
  - Replace lazy-loaded loop queries with eager loading (`with()`, `select_related()`, `prefetch_related()`, `JOIN`) or batch queries.
  - Select only required columns instead of `SELECT *` when tables contain large text/JSON blobs.
  - Replace deep `OFFSET` pagination with keyset/cursor pagination and process batch jobs using chunked cursors/streams.
- [ ] **CPU & Memory**:
  - Replace nested $O(N^2)$ array scans with hash map / `Set` lookups ($O(1)$ per lookup).
  - Stream large CSV/JSON/file exports rather than materializing entire datasets in RAM.
  - Bound in-memory caches with explicit maximum entry counts and LRU eviction.
- [ ] **Network & I/O**:
  - Reuse persistent HTTP client connection pools (`Keep-Alive`) instead of instantiating new clients per call.
  - Execute independent external API or database reads concurrently (`Promise.all`, `asyncio.gather`, `errgroup`, concurrent futures) with bounded concurrency.
- [ ] **Frontend & Core Web Vitals** (when a web UI is in scope):
  - **LCP (`<= 2.5s`)**: Ensure the hero image is in initial HTML with `fetchpriority="high"`, never `loading="lazy"`, and keep TTFB `< 800 ms`.
  - **INP (`<= 200ms`)**: Break up long tasks (`> 50 ms`), debounce rapid input handlers, virtualize long lists, and avoid forced synchronous layout thrashing.
  - **CLS (`<= 0.1`)**: Set explicit `width` and `height` or CSS `aspect-ratio` on all images, videos, embeds, and dynamic skeleton containers.

### Step 4: Re-Measure and Verify Against Baseline
- [ ] Run the exact same benchmark, profiler, or test harness used in Step 1 under identical parameters.
- [ ] Calculate the absolute and percentage delta (e.g., query count reduced from `102` to `3`, p95 latency from `840 ms` to `95 ms`).
- [ ] Run the existing automated test suite to verify that the optimization preserved exact functional behavior and edge-case semantics.

### Step 5: Configure Regression Guards
- [ ] Add automated guards where supported:
  - Database query-count assertions in integration tests (e.g., `assertQueryCount`, `assertNumQueries`).
  - Frontend JavaScript/CSS bundle-size budgets in CI builds.
  - Benchmark latency thresholds or APM p95 regression alerts.
  - Automated Lighthouse / Core Web Vitals checks on key public and authenticated templates.

## 6. Technology-Specific Adaptation Rules

Adapt profiling and optimization tooling to the actual project stack. Never force PHPStan, Pint, Pest, shadcn/ui, or Playwright where inapplicable to the repository:
- **PHP (Laravel / Symfony / CodeIgniter)**: Use `DB::enableQueryLog()`, `DB::listen()`, Laravel Telescope/Debugbar, or Blackfire/Xdebug profiling. Use `with()` eager loading, `select()` column projection, and `lazyById()` / `chunkById()` for large datasets. In CodeIgniter 4, inspect queries via `Toolbar` / `$db->getLastQuery()` and batch inserts with `insertBatch()`.
- **JavaScript / TypeScript (React / Next.js / Vue / Node.js)**: Use Chrome DevTools Performance/Memory tabs, Lighthouse, `clinic.js`, or Node `--prof` / `--cpu-prof`. Apply route/component code splitting (`React.lazy`, dynamic `import()`), optimize Next.js/Nuxt image components with `priority` / `fetchpriority="high"` on the hero asset, and avoid blocking the Node event loop with synchronous crypto, compression, or huge `JSON.parse` payloads.
- **Python (Django / FastAPI / Flask)**: Use `cProfile`, `py-spy`, `memray`, `tracemalloc`, or Django Debug Toolbar. Use `select_related()` / `prefetch_related()`, `.only()` / `.defer()`, and `.iterator(chunk_size=2000)` on QuerySets. Never run synchronous blocking I/O or CPU-bound loops directly inside `async def` FastAPI routes without offloading to a thread/process pool.
- **Go**: Use built-in `runtime/pprof`, `net/http/pprof`, `go test -bench . -benchmem`, and `go tool trace`. Preallocate slices (`make([]T, 0, cap)`), inspect escape analysis (`go build -gcflags="-m"`), reuse buffers via `sync.Pool` where benchmarked, and bound goroutine concurrency with `errgroup.SetLimit()`.
- **Java / Kotlin (Spring Boot)**: Use Java Flight Recorder (JFR), Async-profiler, or VisualVM. Prevent Hibernate/JPA N+1 queries via `@EntityGraph`, `JOIN FETCH`, or batch fetching, and use read-only transactions (`@Transactional(readOnly = true)`) on query endpoints to skip dirty-checking overhead.
- **Rust**: Use `cargo bench`, `criterion`, `cargo flamegraph`, or `dhat-rs`. Avoid unnecessary `.clone()` heap allocations on hot paths, use `Cow<str>` where appropriate, and wrap file/network reads and writes in `BufReader`/`BufWriter`.
- **C# / .NET**: Use `dotnet-trace`, `dotnet-counters`, PerfView, and BenchmarkDotNet. In Entity Framework Core, apply `.AsNoTracking()` on read-only queries, `.Include()` / `.AsSplitQuery()` to avoid N+1 or Cartesian explosions, and `IAsyncEnumerable<T>` for streaming responses.
- **Mobile / Flutter**: Use Flutter DevTools Performance, CPU Profiler, and Memory views in `--profile` mode (never benchmark in debug mode). Keep `build()` methods pure and lightweight, use `const` widget constructors, isolate repaints with `RepaintBoundary`, and render long lists lazily with `ListView.builder` / `SliverList.builder`.
- **Unknown or Mixed Stacks**: Rely on OS/process timers (`/usr/bin/time -v`), database `EXPLAIN` plans, HTTP response timing headers (`Server-Timing`), network waterfalls, and algorithmic time/space complexity analysis.

## 7. Security and Safety Considerations

- **No Cross-Tenant Cache Bleed**: When caching expensive computations or responses to improve speed, ensure cache keys scope strictly by tenant ID, user ID, and authorization role where data is not public.
- **Disable Debug Profilers in Production**: Never leave verbose debug toolbars (`APP_DEBUG=true`, publicly exposed `/debug/pprof`, Xdebug, or Django Debug Toolbar) accessible on public production endpoints.
- **Prevent Denial of Service via Unbounded Concurrency**: When parallelizing slow I/O calls, always enforce a semaphore or worker pool limit so a traffic spike does not exhaust database connections or file descriptors.
- **Timing Side-Channel Awareness**: Do not optimize cryptographic signature or password hash comparisons with early-exit string equality; always preserve constant-time comparison (`hash_equals`, `crypto.timingSafeEqual`, `hmac.compare_digest`).

## 8. Verification Criteria

Before marking performance optimization work complete, verify:
1. **No Unsubstantiated Claims**: Every reported speedup or metric improvement is paired with before/after measurements or explicitly labeled as an unmeasured static structural improvement.
2. **Functional Equivalence**: All unit and integration tests pass, confirming that caching, batching, or query rewrites did not alter business logic, pagination stability, or sort order.
3. **Core Web Vitals Mechanisms Verified**: For frontend tasks, `<img>` dimensions (`width`/`height` or `aspect-ratio`), `fetchpriority="high"` on LCP elements, and absence of layout-shifting styles are verified in the markup or browser.
4. **Memory Stability**: Batch processing or export endpoints use bounded chunking/streaming rather than loading unbounded row sets into RAM.

## 9. Failure Handling and Edge Cases

- **Optimization Degrades Readability with Negligible Gain**: If a micro-optimization yields `< 2%` improvement while complicating maintenance, revert it and focus on macro bottlenecks (I/O, queries, algorithmic complexity).
- **Lab vs. Production Mismatch**: If local benchmarks are fast because the local DB has 50 rows while production has 50 million, seed synthetic volume or inspect query execution plans (`Seq Scan` vs. `Index Scan`) rather than trusting local wall-clock time.
- **Cannot Run Profiler in Sandbox**: Clearly report the environmental limitation, provide the exact profiling command for the user to run, and document the static complexity reduction ($O(N)$ to $O(1)$ queries).
- **Cold Cache vs. Warm Cache Bias**: Always record both cold-cache and warm-cache latency numbers so a caching change does not hide a catastrophic cold-start timeout.

## 10. Expected Outputs and Reporting Requirements

Always deliver a structured **Performance Optimization Report** using the template below:

```markdown
# Performance Profiling & Optimization Report

## 1. Scope & Measurement Environment
- **Target Component / Endpoint**: `<route, function, or page>`
- **Measurement Mode**: `<Live Benchmark | Synthetic Lab | Static Code Inspection Only>`
- **Workload / Dataset Context**: `<row count, concurrency, throttling profile>`

## 2. Baseline vs. Post-Optimization Metrics
| Metric | Baseline (Before) | Post-Change (After) | Delta / Improvement | Target Threshold |
| :--- | :--- | :--- | :--- | :--- |
| `<e.g., Endpoint p95 Latency>` | `<820 ms>` | `<110 ms>` | `<-86.6%>` | `< 200 ms` |
| `<e.g., SQL Queries per Request>` | `<54>` | `<2>` | `<-52 queries>` | `< 5` |
| `<e.g., LCP / INP / CLS>` | `<3.4s / 280ms / 0.18>` | `<1.8s / 95ms / 0.02>` | `<Pass>` | `<=2.5s / <=200ms / <=0.1` |

## 3. Root-Cause Bottlenecks & Applied Fixes
1. **Bottleneck**: `<description and location in code>`
   - **Fix Applied**: `<concrete code/query/markup change>`
   - **Regression Guard**: `<test assertion or budget added>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Receives slow query findings from `query-optimization-performance` (`SKILL-25`) and UI rendering defects from `frontend-performance` (`SKILL-22`) or `playwright-mcp-browser-qa` (`SKILL-17`).
- **Downstream Skills**: Routes asynchronous offloading and distributed cache patterns to `caching-background-jobs` (`SKILL-30`), and feeds verified performance evidence into `deployment-readiness` (`SKILL-33`) and `final-quality-gate` (`SKILL-38`).

## 12. Source References

- **Google Web Vitals (Official Guide)**: https://web.dev/articles/vitals
- **Local Core Web Vitals Diagnostic Reference**: [references/core-web-vitals.md](references/core-web-vitals.md)
- **Shared Library Performance Reference**: [../../references/core-web-vitals-performance-reference.md](../../references/core-web-vitals-performance-reference.md)
