---
name: caching-background-jobs
description: Designs and audits caching layers, cache invalidation strategies, asynchronous job queues, scheduled tasks, idempotency controls, and dead-letter recovery. Activate when implementing or troubleshooting Redis/Memcached caching, background workers, cron jobs, retry backoff, or queue concurrency. Do not use for synchronous HTTP API client retries or pure SQL query tuning.
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-30"
  category: "Performance, Operations, and Deployment"
---

# Caching & Background Jobs

This skill governs the design, implementation, and operational hardening of application caching layers, asynchronous job queues, and scheduled background tasks. It ensures cache consistency without stale-data leaks or stampedes, and guarantees that background jobs are idempotent, safely serialized, resilient to transient failures via exponential backoff, and recoverable when poison messages occur.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Implementing or debugging in-memory or distributed caching (Redis, Valkey, Memcached, CDN edge caches, or database-backed caches).
- Designing cache key namespaces, Time-to-Live (TTL) policies, cache-aside/write-through flows, or cache invalidation hooks.
- Preventing cache stampedes (thundering herd) on high-traffic keys using locking or stale-while-revalidate strategies.
- Moving slow synchronous operations (emails, webhooks, PDF/report generation, media transcoding, bulk imports) into asynchronous background queues.
- Configuring scheduled/cron tasks, overlap locks, retry policies, idempotency keys, worker concurrency, or Dead-Letter Queues (DLQ).

## 2. When Not to Use

Do not activate this skill when the task is strictly limited to:
- Fixing slow SQL queries that should be solved with proper indexing or eager loading before adding a cache (route to `query-optimization-performance`, `SKILL-25`).
- General CPU/memory profiling or frontend Core Web Vitals optimization (route to `performance-profiling-optimization`, `SKILL-29`).
- Outbound synchronous third-party HTTP client configuration without background queues (route to `api-external-service-integration`, `SKILL-27`).
- Streaming large CSV/Excel file parsing logic in isolation (route to `import-export-data-processing`, `SKILL-26`, or pair with this skill for async job orchestration).

## 3. Scope and Objectives

Every caching or background processing implementation under this skill must cover:
- **Cache Invalidation & TTL Strategies**: Defining explicit event-driven invalidation or versioned keys paired with bounded TTLs and jitter so no key lives forever by accident.
- **Cache Consistency & Stampede Prevention**: Enforcing consistent read/write patterns (cache-aside, write-through) and protecting expensive recomputations with distributed locks (`SET NX` / atomic locks) or early probabilistic recomputation.
- **Queue Processing Architecture**: Separating queues by priority and workload profile (e.g., `critical`, `default`, `bulk-exports`) so slow batch jobs never starve urgent user notifications.
- **Scheduled Jobs (Cron Safety)**: Enforcing single-server execution and overlap prevention (`withoutOverlapping` / distributed mutex) on recurring tasks.
- **Retries & Exponential Backoff**: Configuring bounded retry counts (`maxRetries` / `$tries`), job timeouts, and exponential backoff with random jitter.
- **Idempotency**: Ensuring that running any background job or scheduled command twice with the same payload produces the exact same side effects without duplicate charges, duplicate emails, or corrupted counters.
- **Concurrency & Worker Sizing**: Bounding worker process/thread counts and database connection consumption so background workers do not exhaust database pools needed by web traffic.
- **Failed Job Recovery**: Capturing terminal failures in a failed-job table or Dead-Letter Queue (DLQ) with actionable error context, replay tooling, and pruning policies.
- **Observability**: Instrumenting cache hit/miss ratios, queue depth, oldest job age (queue lag), job processing duration, and failure rates.
- **Safe Background Processing**: Serializing lightweight identifiers (primary keys + tenant context) into job payloads rather than full stale ORM entities or plaintext secrets.

## 4. Prerequisites and Context Requirements

Before implementing caching or background jobs, verify:
1. **Infrastructure Backing Store**: Identify the configured cache and queue driver (Redis, RabbitMQ, SQS, PostgreSQL/MySQL database queue, or in-memory local store) and whether the application runs on a single node or horizontally scaled instances.
2. **Staleness Tolerance**: Determine whether the cached domain data can tolerate seconds/minutes of eventual consistency or requires immediate invalidation upon mutation.
3. **Side-Effect Criticality**: Classify whether the background job triggers external billing/emails/webhooks (requiring strict idempotency keys and transactional outbox patterns) or purely internal recomputation.

## 5. Step-by-Step Workflow

### Step 1: Audit Necessity and Data Access First
- [ ] Verify that caching is not being used to mask an unindexed query or N+1 bug that can be fixed directly in the database layer.
- [ ] Identify operations exceeding interactive request budgets (`> 200-500 ms` or involving external network side effects) that belong in an asynchronous job queue.

### Step 2: Design the Caching Strategy and Key Contract
- [ ] **Namespace & Tenant Isolation**: Construct structured, deterministic cache keys containing environment/version, tenant ID, resource type, identifier, and query parameters (e.g., `v1:tenant:{tenant_id}:user:{id}:permissions`).
- [ ] **TTL & Jitter**: Assign an explicit TTL to every cached item. Add small random jitter (e.g., `±10%`) to bulk-populated keys to prevent simultaneous mass expiration.
- [ ] **Invalidation & Transaction Safety**:
  - Invalidate or update cache entries *after* the database transaction commits (`afterCommit`), never inside an uncommitted transaction that might roll back.
  - Prefer explicit key deletion (`FORGET`/`DEL`) over wildcard `KEYS *` scans (which block Redis in production).
- [ ] **Stampede Protection**: Wrap expensive cache rebuilds (`> 100 ms` under high concurrency) in an atomic lock or stale-while-revalidate pattern so only one worker recomputes the value.

### Step 3: Engineer Resilient & Safe Background Jobs
- [ ] **Lightweight, Safe Payload Serialization**:
  - Pass only immutable primitive identifiers (`entity_id`, `tenant_id`, `idempotency_key`, `actor_id`) in the job payload.
  - Re-fetch the fresh record from the database at job execution time and handle the case where the record was deleted or modified while the job waited in the queue.
  - Dispatch jobs *after* the enclosing database transaction commits so workers never query uncommitted rows (`RecordNotFound` race condition).
- [ ] **Idempotency Enforcement**:
  - Design every job handler as a state machine or upsert operation: check whether the target state transition or external idempotency log has already completed before executing side effects.
  - When calling external APIs (Stripe, email providers, webhooks), pass a deterministic idempotency key derived from the business event ID.
- [ ] **Timeouts, Retries, and Backoff**:
  - Define an explicit execution timeout (`timeout`) shorter than the queue visibility timeout (`retry_after` / `VisibilityTimeout`) to prevent duplicate concurrent execution.
  - Configure bounded retries (e.g., `3-5` attempts) with exponential backoff (e.g., `10s, 60s, 300s`).
  - Distinguish between **transient errors** (network timeout, HTTP `429`/`503` -> retry) and **permanent errors** (validation failure, HTTP `400`/`404` -> fail immediately without wasting retries).

### Step 4: Harden Scheduled Tasks and Worker Concurrency
- [ ] Add distributed overlap locks (`withoutOverlapping()`, `pg_try_advisory_lock`, or Redis mutex with expiry) to every scheduled cron job.
- [ ] Ensure multi-instance deployments run scheduled tasks on a single coordinator (`onOneServer()` or dedicated scheduler instance).
- [ ] Configure graceful shutdown (`SIGTERM` handling) so workers finish their in-flight job before container termination.

### Step 5: Configure Failed Job Recovery & Observability
- [ ] Route exhausted jobs to a persistent failed-job store or Dead-Letter Queue (DLQ) and implement a `failed()` hook to record diagnostic metadata and update domain status (e.g., marking an export record as `FAILED` so the UI stops spinning).
- [ ] Configure automated retention and pruning for completed and failed job records so queue tracking tables do not grow without bound.
- [ ] Expose metrics or health checks for cache hit/miss ratios, queue lag (age of oldest pending job in seconds), active worker count, and failed job rate.

## 6. Technology-Specific Adaptation Rules

Adapt caching and queue patterns to the actual project stack. Never force PHPStan, Pint, Pest, shadcn/ui, or Playwright where inapplicable to the repository:
- **PHP (Laravel / Symfony / CodeIgniter)**: In Laravel, use `Cache::remember()` or `Cache::flexible()` (stale-while-revalidate) and `Cache::lock()` for stampede protection. Implement `ShouldQueue` and `ShouldBeUnique` where appropriate, set `$afterCommit = true`, define `$tries`, `$maxExceptions`, `$timeout`, and `backoff()`, and use `->withoutOverlapping()->onOneServer()` in the scheduler. In CodeIgniter 4, use `cache()->remember()` and `codeigniter4/tasks` or CLI worker queues with database locks.
- **JavaScript / TypeScript (Node.js / BullMQ / NestJS / Next.js / Vue)**: With BullMQ, set `attempts`, `backoff: { type: 'exponential', delay: 2000 }`, `removeOnComplete: { count: 1000 }`, and `removeOnFail: { age: 604800 }`; pass deterministic `jobId` for deduplication. In Next.js, use `revalidateTag` / `revalidatePath` accurately and never cache user-private responses in shared CDN or Full Route caches.
- **Python (Django / FastAPI / Celery / Dramatiq / RQ)**: In Celery, enable `acks_late=True`, `reject_on_worker_lost=True`, `autoretry_for=(TransientError,)`, `retry_backoff=True`, `retry_jitter=True`, and `soft_time_limit` / `time_limit`. Always dispatch jobs inside `transaction.on_commit(lambda: task.delay(obj.id))` in Django or after `await session.commit()` in SQLAlchemy/FastAPI.
- **Go**: Use `singleflight.Group` (`golang.org/x/sync/singleflight`) to prevent in-process cache stampedes, and libraries like `asynq` or `river` (PostgreSQL transactional queue) for background jobs. Propagate `context.WithTimeout` into worker handlers and respect `ctx.Done()` during graceful `SIGTERM` shutdown.
- **Java / Spring Boot**: Use Spring `@Cacheable` with Redis/Caffeine, `@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)` or the Transactional Outbox pattern with RabbitMQ/Kafka, and configure Dead-Letter Exchanges (DLX) with bounded retry headers.
- **Rust**: Use `moka` (bounded concurrent cache with TTL and size weigher) or Redis via `deadpool-redis` / `fred`. For background workers (`apalis`, `fang`, or Tokio channels), use `tokio_util::sync::CancellationToken` and `TaskTracker` for graceful shutdown.
- **C# / .NET**: Use `HybridCache` (built-in stampede protection in .NET 9+) or `IMemoryCache` / `IDistributedCache`. For background work, use `Hangfire`, `Quartz.NET`, or `BackgroundService` with `Channel<T>`, ensuring scoped `DbContext` instances are created per job via `IServiceScopeFactory`.
- **Mobile / Flutter**: Bound local offline disk caches (`Hive`, `Drift`, `sqflite`, `cached_network_image`) with explicit maximum size/age eviction policies, and schedule deferred background sync tasks via platform `WorkManager` / `BGTaskScheduler` with network and battery constraints.
- **Unknown or Mixed Stacks**: Enforce the universal primitives: atomic lock on cache rebuild, versioned tenant-scoped cache keys, after-commit dispatch, ID-only job payloads, exponential backoff with jitter, and idempotency keys stored in the primary database.

## 7. Security and Safety Considerations

- **Cross-Tenant & Cross-User Cache Poisoning**: Never cache personalized or permission-filtered responses under a global cache key (e.g., `/api/dashboard` without user/tenant scope). Verify `Vary: Authorization, Cookie` headers when using HTTP/CDN caching.
- **No Plaintext Secrets in Queue Payloads**: Queue payloads stored in Redis, SQS, or database tables are visible to operators and monitoring tools. Never serialize raw API keys, passwords, or full credit card numbers into job arguments.
- **Insecure Deserialization**: Use safe data formats (`JSON`) for cached values and queue messages whenever interoperability or untrusted inputs are involved, avoiding arbitrary object deserialization (`pickle`, unguarded PHP `unserialize`) on untrusted payloads.
- **Re-Verify Authorization at Job Execution Time**: A user's role or subscription may be revoked between the time a delayed job is enqueued and the time it runs. Re-check critical tenant/account status inside the worker before executing privileged actions.

## 8. Verification Criteria

Before completing any caching or background job task, verify:
1. **Transaction Commit Ordering**: Jobs are dispatched and caches are invalidated *after* database transactions commit.
2. **Idempotency Proof**: Re-running the job handler twice in a test produces identical database state and only one external side effect.
3. **Timeout Hierarchy**: Worker job timeout is strictly less than the queue broker's retry/visibility timeout (`timeout < retry_after`).
4. **Failure State Visibility**: When a job permanently exhausts retries, any user-facing status record transitions cleanly to a failure state rather than remaining stuck in `PENDING`/`PROCESSING`.
5. **Tenant Cache Isolation**: Tests confirm that Tenant A's cached query result is never returned to Tenant B.

## 9. Failure Handling and Edge Cases

- **Cache Store Outage**: Decide explicitly whether cache connectivity failures should fail open (fallback to database with circuit breaking/rate limiting) or fail closed (for security rate-limit counters or atomic financial locks).
- **Deleted Entities Before Job Runs**: If a user creates and immediately deletes a record before the queued job executes, the job must handle the missing record gracefully (log and exit cleanly) instead of crashing repeatedly.
- **Poison Pill Jobs**: If a malformed payload causes an unhandled fatal crash (OOM or segfault), ensure max-receive counts move the message to a DLQ so workers do not loop infinitely.
- **Clock Skew on Scheduled Locks**: Ensure distributed scheduler mutex TTLs account for NTP clock drift across worker nodes, or use single-coordinator DB advisory locks.

## 10. Expected Outputs and Reporting Requirements

Provide a structured **Caching & Background Processing Report**:

```markdown
# Caching & Background Jobs Implementation Report

## 1. Caching Architecture
- **Cache Store & Key Pattern**: `<e.g., Redis | v1:tenant:{id}:resource:{id}>`
- **TTL & Invalidation Trigger**: `<e.g., 15m TTL with ±10% jitter; invalidated afterCommit on update/delete>`
- **Stampede & Isolation Controls**: `<atomic lock / tenant key scoping>`

## 2. Background Jobs & Scheduled Tasks
| Job / Task Name | Queue | Timeout / Visibility | Retries & Backoff | Idempotency Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| `<SendInvoiceJob>` | `<critical>` | `<60s / 90s>` | `<3 tries, exp 10s/60s/300s>` | `<Unique invoice_id + sent_at check>` |

## 3. Recovery & Verification
- **Dead-Letter / Failed Job Handling**: `<failed() hook updates status + DLQ retention>`
- **Verification Evidence**: `<unit/integration test outputs proving idempotency and cache invalidation>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Receives latency offloading candidates from `performance-profiling-optimization` (`SKILL-29`) and bulk file processing jobs from `import-export-data-processing` (`SKILL-26`).
- **Downstream Skills**: Connects to `observability-incident-diagnosis` (`SKILL-34`) for queue lag metrics and structured job logging, and `deployment-readiness` (`SKILL-33`) for verifying worker daemon restarts and queue readiness during releases.

## 12. Source References

- **AWS Builders' Library (Timeouts, Retries, and Backoff with Jitter)**: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
- **AWS Builders' Library (Making Retries Safe with Idempotent APIs)**: https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
- **Redis Official Documentation (Caching & Locks)**: https://redis.io/docs/latest/develop/use/patterns/
- **Shared Library Performance Reference**: [../../references/core-web-vitals-performance-reference.md](../../references/core-web-vitals-performance-reference.md)
