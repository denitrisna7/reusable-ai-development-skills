---
name: query-optimization-performance
description: "Eliminates N+1 query loops, tunes EXPLAIN plans, adds composite indexes, and optimizes pagination and connection pools. Use for DB performance. Do not use for initial schema design."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-25"
  category: "Data and Integrations"
---

# Query Optimization & Database Performance

This skill governs SQL and document query analysis, composite and covering index design, N+1 query detection and elimination, cursor/keyset pagination, `EXPLAIN ANALYZE` execution plan interpretation, caching strategies, and database connection management. It enforces measurement-based optimization (`C-5`, `R-36`), ensuring every index or query rewrite is backed by query count metrics or execution plan evidence.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Diagnosing slow API endpoints, dashboard queries, reports, or background jobs caused by database latency.
- Eliminating N+1 query loops in ORM relationships, GraphQL resolvers, or API serializers.
- Designing or tuning composite, partial, covering, or full-text indexes based on `WHERE`, `JOIN`, `ORDER BY`, and `GROUP BY` clauses.
- Replacing slow deep `LIMIT / OFFSET` pagination with keyset/cursor pagination or optimizing database connection pool usage.

## 2. When Not to Use

Do not use this skill as the primary workflow for:
- Initial domain entity modeling, foreign key `ON DELETE` rules, or zero-downtime column renames: route to `database-architecture-integrity` (`SKILL-24`).
- Frontend bundle splitting, image optimization, or Core Web Vitals (CLS/INP): route to `frontend-performance` (`SKILL-22`).
- Bulk CSV/Excel file ingestion and row validation: route to `import-export-data-processing` (`SKILL-26`).

## 3. Scope and Objectives

Every query optimization task or audit must cover:
- **Query Analysis & Projection Discipline**: Select only required columns (`SELECT id, name, status` rather than `SELECT *`), avoid fetching large `TEXT`/`JSONB`/`BLOB` columns in list views, and push filtering and aggregation (`COUNT`, `SUM`, `AVG`) into the database rather than loading thousands of rows into application memory.
- **Indexing Strategy (Left-Prefix, Selectivity, & Covering Indexes)**:
  - Design composite B-tree indexes following the **ESR (Equality, Sort, Range)** rule: place equality filter columns first (`WHERE tenant_id = ? AND status = ?`), followed by sort columns (`ORDER BY created_at DESC`), and range filter columns (`WHERE amount > ?`).
  - Use covering indexes (`INCLUDE (...)` in PostgreSQL/SQL Server or composite trailing columns) for hot read paths to enable Index-Only Scans.
  - Use partial/filtered indexes (`WHERE deleted_at IS NULL` or `WHERE status = 'pending'`) to shrink index size and speed up hot subset queries.
  - Avoid over-indexing write-heavy tables; every redundant index adds write amplification on `INSERT`, `UPDATE`, and `DELETE`.
- **N+1 Query Detection & Elimination**: Detect queries executed inside loops (`for item in items: item.related`) and replace them with eager loading (`with()`, `select_related()`, `prefetch_related()`, `include`), explicit SQL `JOIN`s, batch `WHERE id IN (...)` queries, or GraphQL `DataLoader` batching.
- **Scalable Pagination**: Understand that `OFFSET 100000 LIMIT 20` forces the database to scan and discard `100,000` rows. Use keyset/cursor pagination (`WHERE (created_at, id) < (?, ?) ORDER BY created_at DESC, id DESC LIMIT 20`) for infinite scroll, feeds, and large tables, or deferred join pagination when page numbers are mandatory.
- **Query Plan Interpretation (`EXPLAIN ANALYZE`)**: Inspect actual execution plans for sequential scans (`Seq Scan` / `ALL`) on large tables, high-cost nested loops, disk sort spills (`external merge Disk`), index scan vs. bitmap heap scan behavior, and shared buffer reads/hits.
- **Caching Strategy**: Apply query/result caching (Redis, Memcached, in-memory LRU, or materialized views) only after optimizing the underlying query and indexes. Define explicit TTLs, cache keys scoped by tenant/user permissions, and deterministic cache invalidation on writes.
- **Connection Pooling & Usage**: Release connections promptly, size connection pools appropriately (using PgBouncer, ProxySQL, HikariCP, SQLAlchemy pool, or Prisma pool limits), and avoid holding idle connections open during slow external HTTP calls.
- **Profiling & Measurement-Based Optimization (`C-5`)**: Record query count and execution time (or `EXPLAIN` plan cost/rows) before and after optimization.

## 4. Prerequisites and Context Requirements

Before tuning queries or adding indexes, inspect:
1. **Database Engine & Schema**: Table definitions, existing indexes (`\d tablename` or `SHOW INDEX FROM tablename`), approximate row counts, and data distribution.
2. **ORM / Query Builder Code**: Repository/controller methods, serializers/resources (where lazy-loading N+1 queries often hide), and pagination helpers.
3. **Performance Reference**: Read [../../references/core-web-vitals-performance-reference.md](../../references/core-web-vitals-performance-reference.md).

## 5. Step-by-Step Workflow

### Step 1: Profile and Capture the Baseline (`C-5`)
- [ ] Enable query logging in the test or local environment to count the exact number of SQL queries executed per request and identify the slowest statements.
- [ ] For slow SQL statements, run `EXPLAIN (ANALYZE, BUFFERS)` (PostgreSQL), `EXPLAIN ANALYZE` (MySQL 8.0.18+), or `EXPLAIN QUERY PLAN` (SQLite) on a non-production/test instance.
- [ ] If no live database is accessible, perform static code analysis of the ORM/SQL queries against the migration schema and explicitly record `"Runtime EXPLAIN: NOT TESTED (static query & index analysis only)"`.

### Step 2: Eliminate N+1 Queries and In-Memory Filtering
- [ ] Trace the full request lifecycle including view templates and API response serializers (`JsonResource`, DRF `Serializer`, GraphQL field resolvers).
- [ ] Replace lazy relationship access inside loops with eager loading or a single batch query.
- [ ] Enable strict lazy-loading prevention in development/test modes where supported (e.g., `Model::preventLazyLoading(!app()->isProduction())` in Laravel, `lazy="raise"` in SQLAlchemy).
- [ ] Replace application-side collection filtering/counting (`Model::all()->count()`, `len(Model.objects.all())`) with database `COUNT(*)` / `EXISTS` queries.

### Step 3: Optimize Index Usage and SARGability
- [ ] Verify queries are **SARGable** (Search Argument Able) so the planner can use B-tree indexes:
  - Replace `WHERE YEAR(created_at) = 2026` or `WHERE DATE(created_at) = '2026-10-28'` with range predicates: `WHERE created_at >= '2026-10-28 00:00:00' AND created_at < '2026-10-29 00:00:00'`.
  - Replace `WHERE LOWER(email) = ?` with an expression index `CREATE INDEX ON users (LOWER(email))` or case-insensitive collation (`CITEXT`).
  - Avoid leading wildcards (`WHERE name LIKE '%term%'`) on huge B-tree indexes; use trigram indexes (`pg_trgm` GIN/GiST) or full-text search (`tsvector` / `FULLTEXT`) when substring search is required.
- [ ] Design composite indexes ordered by **Equality -> Sort -> Range** matching the query's `WHERE` and `ORDER BY` clauses.

### Step 4: Optimize Pagination, Aggregations, and Connection Usage
- [ ] Convert deep list endpoints and background batch iterators from `OFFSET` pagination to cursor/keyset pagination (`WHERE id > last_seen_id ORDER BY id ASC LIMIT N`).
- [ ] On large tables where exact total counts (`COUNT(*)`) are slow on every page load, consider caching the count, using approximate counts where acceptable, or using simple "Next / Previous" pagination without `COUNT(*)`.
- [ ] Verify database connections are pooled, bounded by statement timeouts (`statement_timeout` / `max_execution_time`), and never held across external network calls.

### Step 5: Verify Post-Change Query Plans and Regression Tests
- [ ] Re-run the endpoint or test with query counting assertions (e.g., asserting query count drops from `1 + N` to `2` regardless of list size) and compare `EXPLAIN` output.

## 6. Technology-Specific Adaptation Rules

| Stack / Ecosystem | Query & N+1 Optimization Idioms | Profiling & Verification Tools |
| :--- | :--- | :--- |
| **PHP (Laravel Eloquent / CodeIgniter)** | Use `with(['relation:id,name'])`, `withCount()`, `loadMissing()`, `cursorPaginate()`, and `chunkById()` / `lazyById()`. Enable `Model::preventLazyLoading()`. | `DB::getQueryLog()`, `$this->expectsDatabaseQueryCount(n)` in Pest/PHPUnit, Laravel Telescope/Debugbar. |
| **JS / TS (Prisma / Drizzle / TypeORM / Knex)** | Use `select` (instead of fetching all columns) or targeted `include`, cursor pagination (`cursor: { id }, take, skip: 1`), and `dataloader` for GraphQL resolvers. | Prisma query event listener (`$on('query')`), `EXPLAIN` via `$queryRaw`. |
| **Python (Django ORM / SQLAlchemy)** | Use `select_related()` for `1:1`/`N:1` joins, `prefetch_related()` / `Prefetch()` for `1:N`/`M:N`, `.only()` / `.defer()`, and `.iterator(chunk_size=1000)`. In SQLAlchemy, use `selectinload()` / `joinedload()`. | `django.test.utils.CaptureQueriesContext`, `assertNumQueries()`, Django Debug Toolbar, SQLAlchemy `echo=True`. |
| **Go (`sqlx`, `pgx`, `sqlc`, `GORM`)** | Prefer explicit `JOIN` or `WHERE id = ANY($1)` batch queries in `sqlc`/`pgx`; in GORM use `Preload()` / `Joins()` and `Select()` specific columns. Configure `db.SetMaxOpenConns`, `SetMaxIdleConns`, and `SetConnMaxLifetime`. | `pg_stat_statements`, `EXPLAIN (ANALYZE, BUFFERS)`, Go benchmark tests. |
| **Java / Spring Data JPA / Hibernate** | Avoid default lazy N+1 traps via `@EntityGraph`, `JOIN FETCH` JPQL queries, or DTO projections. Configure HikariCP pool bounds and set `spring.jpa.open-in-view=false` to prevent holding DB connections during view rendering. | Hibernate statistics (`generate_statistics`), `datasource-proxy` query count assertions in JUnit. |
| **C# / .NET (EF Core) & Rust (`sqlx` / `diesel`)** | In EF Core, use `.AsNoTracking()` for read-only queries, `.Include()`, `.Select()` DTO projections, and `.AsSplitQuery()` to avoid cartesian explosion on multiple collection includes. | EF Core `ToQueryString()`, `LogTo()`, `sqlx` query logging. |
| **Mobile / Local SQLite (`Drift`, `sqflite`, `Room`)** | Create indexes on foreign keys and sort columns in local SQLite schemas, run heavy queries on background isolates/coroutines, and paginate large local tables via `LIMIT` + keyset cursor. | `EXPLAIN QUERY PLAN` in SQLite tests. |

### Keyset / Cursor Pagination Pattern vs. Offset Pagination

- **Why `OFFSET` Degrades**:
  - `SELECT id, title, created_at FROM posts WHERE tenant_id = $1 ORDER BY created_at DESC, id DESC LIMIT 20 OFFSET 50000;`
  - The database must scan and sort `50,020` index/table entries, discard the first `50,000`, and return `20` ($O(\text{offset} + \text{limit})$ cost).
- **Deterministic Keyset / Seek Replacement**:
  - `SELECT id, title, created_at FROM posts WHERE tenant_id = $1 AND (created_at, id) < ($2, $3) ORDER BY created_at DESC, id DESC LIMIT 20;`
  - Backed by a composite index `CREATE INDEX idx_posts_tenant_created_id ON posts (tenant_id, created_at DESC, id DESC);`, the database jumps directly to the cursor position in $O(\log N + \text{limit})$ time regardless of page depth.

### Index & Execution Plan Quick-Reference

| Symptom in Query / `EXPLAIN` Plan | Root Cause | Remediation |
| :--- | :--- | :--- |
| Query count scales linearly with rows ($1 + N$ queries) | Lazy loading inside loop / serializer | Add eager loading (`with`, `select_related`, `JOIN FETCH`, `DataLoader`) and add a test asserting constant $O(1)$ query count. |
| `Seq Scan` on large table despite index existing | Non-SARGable predicate (`FUNCTION(col) = val`), type mismatch (`varchar_col = 123`), or leading wildcard `LIKE '%x'`. | Rewrite predicate to bare column range, match parameter types, or add functional/trigram index. |
| `Sort Method: external merge Disk` | `ORDER BY` cannot use index and exceeds `work_mem` / `sort_buffer_size`. | Extend composite index so trailing columns match `ORDER BY` direction (`ASC`/`DESC`). |
| Cartesian product explosion on multiple `LEFT JOIN`s | Joining multiple `1:N` child tables in a single flat query (`10 x 20 = 200` duplicate parent rows). | Fetch child collections via separate `WHERE parent_id IN (...)` queries (`prefetch_related`, `selectinload`, `AsSplitQuery`). |

## 7. Security and Safety Considerations

- **Parameterized Queries Only**: When rewriting ORM queries into raw SQL or custom `JOIN` / cursor expressions for performance, **always** bind parameters (`?`, `$1`, `:param`). Never interpolate user input into `WHERE`, `ORDER BY`, or `LIMIT` strings (`application-security-owasp`, `SKILL-10`). Allowlist sort column names and sort directions (`ASC` / `DESC`).
- **Tenant-Scoped Cache Keys**: When caching query results, always prefix cache keys with `tenant_id` / `user_id` or visibility scope so one user never receives cached data belonging to another tenant.
- **Unbounded Query Protection**: Enforce a maximum page size (`MAX_LIMIT = 100`) on all list endpoints so clients cannot request `limit=1000000` and trigger denial-of-service memory exhaustion.

## 8. Verification Criteria

Before declaring query optimization complete:
1. **Query Count Evidence**: For N+1 fixes, demonstrate via test assertion or query log that fetching a list of $N$ records executes a constant number of queries ($O(1)$, e.g., 1-2 queries) rather than $O(N)$ queries.
2. **Index & Execution Plan Evidence**: Show the exact composite/partial index definition added and explain how it satisfies the query's `WHERE` + `ORDER BY` clauses (with `EXPLAIN` output when a database is running).
3. **Behavioral Equivalence**: Automated tests confirm the optimized query returns identical domain results, sorting, and tenant filtering as the original query.

## 9. Failure Handling and Edge Cases

- **Unstable Cursor Pagination on Non-Unique Timestamps**: Using `WHERE created_at < ? ORDER BY created_at DESC` alone skips rows when multiple records share the exact same timestamp. Always include a unique tie-breaker column in both the cursor predicate and sort order: `WHERE (created_at, id) < (?, ?) ORDER BY created_at DESC, id DESC`.
- **Small Table Sequential Scans**: On very small tables (e.g., `< 100` rows in local seed data), the query planner will intentionally choose a `Seq Scan` because reading a single heap page is faster than reading an index page + heap page. Test `EXPLAIN` plans with realistic row counts or `SET enable_seqscan = off` (in local PostgreSQL testing only) to verify index eligibility.
- **Write Amplification from Unused Indexes**: Before adding a new composite index `(a, b, c)`, check if an existing single-column index `(a)` or `(a, b)` is now redundant and can be safely replaced.

## 10. Expected Outputs and Reporting Requirements

Report query optimization work using this template:

```markdown
## Query Optimization & Database Performance Report

### 1. Bottleneck & Baseline Analysis
- **Target Endpoint / Job / Query**: [File path and function/method name]
- **Measurement Mode**: [Live DB + `EXPLAIN ANALYZE` / Automated Query Count Test / Static Schema & Query Analysis]
| Metric | Baseline | Post-Change | Delta | Status |
| :--- | :--- | :--- | :--- | :--- |
| Queries per Request ($N=50$ rows) | [e.g., `52` queries] | [e.g., `2` queries] | `-50 queries` | PASS |
| Execution Plan / Scan Type | [e.g., `Seq Scan + Disk Sort`] | [e.g., `Index Scan on idx_orders_tenant_created`] | Structural Fix | PASS |
| Execution Latency | [Value or Not Measured] | [Value or Not Measured] | [Delta] | [Status] |

### 2. Optimizations Implemented
- **N+1 / Eager Loading Fixes**: [Details of relationship loading or batching]
- **Index Additions / Adjustments**: [Exact index DDL or migration added]
- **Pagination / Projection / Caching Changes**: [Details]

### 3. Verification & Regression Safety
- **Automated Tests Run**: [Command & output, including query count assertions]
- **Security Check**: [Sort allowlisting, parameterized bindings, and tenant scoping verified]
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - `database-architecture-integrity` (`SKILL-24`): Governs migration creation and `CREATE INDEX CONCURRENTLY` rollout safety when adding new indexes.
- **Downstream / Co-Activated Skills**:
  - `backend-testing-tdd` (`SKILL-16`): Adds regression tests asserting query count ceilings (`assertNumQueries` / `expectsDatabaseQueryCount`).
  - `performance-profiling-optimization` (`SKILL-29`): Coordinates broader end-to-end API latency and memory profiling.

## 12. Source References

- **Use The Index, Luke (SQL Indexing & Tuning Guide)**: https://use-the-index-luke.com/
- **PostgreSQL Official Documentation (Using EXPLAIN & Indexes)**: https://www.postgresql.org/docs/current/using-explain.html
- **Shared Library Reference (Core Web Vitals & Backend Profiling)**: [../../references/core-web-vitals-performance-reference.md](../../references/core-web-vitals-performance-reference.md)
