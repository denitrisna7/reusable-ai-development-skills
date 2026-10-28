---
name: database-architecture-integrity
description: "Designs and audits relational and document database schemas, entity relations, primary and foreign key constraints, indexes, deterministic migrations, ACID transactions, concurrency locks, and zero-downtime backward-compatible schema changes. Activate when creating or modifying tables, migrations, foreign keys, or transactional workflows. Do not use for pure query execution plan tuning (use query-optimization-performance)."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-24"
  category: "Data and Integrations"
---

# Database Architecture & Data Integrity

This skill governs database schema modeling, relational and document structures, database-enforced constraints, indexing fundamentals, deterministic migrations, ACID transaction boundaries, concurrency control, backward-compatible schema evolution, and rollback safety. It ensures that data integrity is enforced at the storage engine level rather than relying solely on application-layer validation.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Designing new database tables, collections, columns, data types, or entity relationships (`1:1`, `1:N`, `M:N`).
- Authoring, reviewing, or modifying database migrations, seeders, or schema definitions.
- Implementing multi-step data mutations that require ACID transactions, idempotency keys, optimistic locking, or pessimistic row locking (`SELECT ... FOR UPDATE`).
- Planning zero-downtime schema alterations, column renames/removals, data backfills, or migration rollback procedures.

## 2. When Not to Use

Do not use this skill as the primary workflow for:
- Diagnosing slow SQL queries, `EXPLAIN ANALYZE` execution plans, or N+1 query bottlenecks without schema design changes: route to `query-optimization-performance` (`SKILL-25`).
- Bulk CSV/spreadsheet parsing and export pipelines: route to `import-export-data-processing` (`SKILL-26`).
- Full database backup scheduling and disaster recovery drills: route to `backup-recovery-dr` (`SKILL-35`).

## 3. Scope and Objectives

Every database architecture or migration task must cover:
- **Schema Design & Data Types**: Model domain entities (`C-3`) using third normal form (`3NF`) by default, introducing deliberate denormalization or JSONB/document columns only with a documented read/flexibility justification. Select precise column types:
  - Monetary values: exact fixed-point integer minor units (`BIGINT` cents) or `NUMERIC(precision, scale)` / `DECIMAL` (never `FLOAT` or `REAL`).
  - Timestamps: timezone-aware UTC timestamps (`TIMESTAMPTZ` in PostgreSQL, UTC `DATETIME(6)` / `TIMESTAMP`).
  - Identifiers: `BIGINT GENERATED ALWAYS AS IDENTITY` or `UUID` (preferring time-ordered `UUIDv7` where supported to avoid B-tree page fragmentation).
- **Relations (`1:1`, `1:N`, `M:N`)**: Model associative `M:N` relationships with explicit join tables containing composite uniqueness constraints, timestamps, and foreign keys.
- **Database-Level Constraints**: Enforce integrity in the database schema via `PRIMARY KEY`, `FOREIGN KEY` with explicit `ON DELETE` (`RESTRICT`, `CASCADE`, or `SET NULL`) and `ON UPDATE` behavior, `NOT NULL`, `UNIQUE` (including partial unique indexes where soft deletes exist), and `CHECK` constraints for invariants (e.g., `CHECK (amount >= 0)`).
- **Foundational Indexing**: Create indexes for all foreign key columns (in engines like PostgreSQL that do not auto-index foreign keys), unique business keys, and primary lookup filters.
- **Deterministic Migrations**: Write version-controlled, deterministic, and idempotent-where-possible migrations that separate schema DDL from large data backfills.
- **ACID Transactions**: Wrap multi-write business operations in atomic database transactions, while strictly keeping external network I/O (HTTP API calls, emails, webhook dispatches, file storage uploads) **outside** open database transactions to prevent connection pool starvation and lock contention.
- **Concurrency Control**: Prevent race conditions (double-spending, inventory overselling, duplicate status transitions) using pessimistic locking (`SELECT ... FOR UPDATE`), atomic conditional updates (`UPDATE ... WHERE status = 'pending'`), unique idempotency keys, or optimistic version columns (`version = version + 1`).
- **Backward-Compatible Schema Changes (Expand-and-Contract)**: Avoid breaking running application instances during deployments by splitting destructive changes (renaming/dropping columns, adding `NOT NULL` without a default on large tables) into safe multi-phase releases.
- **Migration Rollback Considerations**: Provide tested `down` / rollback migrations or documented forward-fix recovery paths, noting that destructive DDL (`DROP TABLE`, `DROP COLUMN`) cannot restore deleted data without a backup.

## 4. Prerequisites and Context Requirements

Before writing schema changes or migrations, inspect:
1. **Database Engine & Version**: PostgreSQL, MySQL/MariaDB, SQLite, SQL Server, Oracle, MongoDB, Firestore, or DynamoDB (and engine-specific DDL locking behavior).
2. **ORM / Migration Tooling**: Laravel Eloquent Migrations, CodeIgniter Migrations, Prisma, Drizzle, TypeORM, Knex, Alembic/SQLAlchemy, Django Migrations, Flyway, Liquibase, Goose/`golang-migrate`, SQLx, or EF Core.
3. **Existing Schema & Conventions**: Naming conventions (`snake_case` plural tables vs. existing repo style), primary key format, soft-delete conventions (`deleted_at`), and multi-tenant isolation keys (`tenant_id` / `organization_id`).

## 5. Step-by-Step Workflow

### Step 1: Analyze Domain Invariants and Existing Schema
- [ ] Inspect existing migrations and schema dumps (`schema.rb`, `schema.prisma`, `database/migrations/`, `models.py`) to match naming, key types, and tenant scoping conventions.
- [ ] Identify all invariants that must never be violated even if a bug exists in application code (e.g., unique email per active tenant, non-negative account balance, non-null foreign owner).

### Step 2: Design Tables, Relations, Constraints, and Indexes
- [ ] Choose accurate column types (`NUMERIC` or integer minor units for money, `TIMESTAMPTZ` for timestamps, bounded `VARCHAR` or `TEXT` with length validation).
- [ ] Define explicit `FOREIGN KEY` constraints and deliberately choose `ON DELETE RESTRICT` (for financial/audit records that must never vanish silently), `ON DELETE CASCADE` (for strictly owned child rows), or `ON DELETE SET NULL`.
- [ ] If the table uses soft deletes (`deleted_at`), replace naive `UNIQUE (email)` constraints with a partial unique index (`CREATE UNIQUE INDEX ... ON users (email) WHERE deleted_at IS NULL` in PostgreSQL/SQLite) or handle soft-deleted uniqueness explicitly.
- [ ] Add explicit indexes on all foreign key columns and frequent filter/join columns.

### Step 3: Evaluate Backward Compatibility and Locking Risk (Expand-and-Contract)
- [ ] Check whether the migration modifies an existing production table:
  - **Safe in a single release (Expand)**: Adding a nullable column, adding a new table, or adding an index concurrently (`CREATE INDEX CONCURRENTLY` in PostgreSQL).
  - **Unsafe in a single release**: Renaming a column/table, changing a column's type incompatibly, or dropping a column currently referenced by live application code.
- [ ] For breaking changes on live systems, structure an **Expand -> Migrate/Backfill -> Switch -> Contract** plan:
  1. *Expand*: Add the new nullable column; deploy code that writes to both old and new columns.
  2. *Backfill*: Backfill existing rows in small chunked batches outside a single giant transaction.
  3. *Switch*: Deploy code that reads from the new column and stops reading the old column; add `NOT NULL` constraint (using `NOT VALID` + `VALIDATE CONSTRAINT` on PostgreSQL to avoid long table locks).
  4. *Contract*: Drop the old column in a subsequent release.

### Step 4: Engineer Transactional and Concurrency Safety
- [ ] Wrap coupled writes (e.g., creating an order, decrementing stock, and recording a ledger entry) inside a single database transaction.
- [ ] Audit the transaction block to verify **zero** external HTTP requests, SMTP calls, or slow file operations occur while the transaction is open; trigger external side effects after commit (e.g., via transactional outbox or `DB::afterCommit()` / `transaction.on_commit()`).
- [ ] Protect state-check-then-mutate flows against TOCTOU race conditions using `SELECT ... FOR UPDATE`, atomic `UPDATE ... WHERE`, or optimistic version checks.

### Step 5: Verify Migration Execution and Rollback
- [ ] Run the migration forward (`up`), inspect the resulting database schema (`\d+`, `SHOW CREATE TABLE`, or schema dump), test rollback (`down`) and re-application (`up`) in an isolated local/test database, and run integration tests (`backend-testing-tdd`, `SKILL-16`).

## 6. Technology-Specific Adaptation Rules

| Stack / Ecosystem | Schema & Migration Adaptation | Concurrency & Transaction Idioms |
| :--- | :--- | :--- |
| **PHP (Laravel / CodeIgniter)** | Use `Schema::create` / `table` with `$table->foreignId(...)->constrained()->restrictOnDelete()`. Never edit already-committed production migrations; create a new migration. | Use `DB::transaction(fn () => ...)` and `DB::afterCommit(...)` or `afterCommit()` on queued jobs. Use `->lockForUpdate()` for pessimistic locks. |
| **JS / TS (Prisma / Drizzle / TypeORM / Knex)** | Define explicit `@relation(..., onDelete: Restrict)` and `@@index([foreignKey])` in Prisma (Prisma does not auto-index foreign keys on PostgreSQL). Commit generated SQL migration files. | Use `prisma.$transaction(async (tx) => ...)` with interactive timeout bounds, or raw `FOR UPDATE` / atomic `updateMany({ where: { id, version } })`. |
| **Python (Django / SQLAlchemy / Alembic)** | Use `models.ForeignKey(..., on_delete=models.PROTECT)` or `CASCADE`, `CheckConstraint`, and `UniqueConstraint`. Split schema and data migrations in Django (`RunPython`) with `atomic = False` for concurrent index creation. | Use `with transaction.atomic():`, `select_for_update()`, and `transaction.on_commit(callback)` for post-commit side effects. |
| **Go (`database/sql`, `pgx`, `sqlc`, `GORM`)** | Use `golang-migrate`, `goose`, or `atlas` SQL migrations with explicit `.up.sql` and `.down.sql` files. Note that PostgreSQL supports transactional DDL, whereas MySQL implicitly commits on DDL. | Always `defer tx.Rollback(ctx)` after `BeginTx`, pass `ctx` with timeout, and execute external calls only after `tx.Commit(ctx)` returns `nil`. |
| **Java / Spring Boot & C# / .NET** | Use Flyway (`V1__*.sql`) or Liquibase (Java) and EF Core Migrations (C#). Avoid `ddl-auto: update` in production Spring Boot configs; set `ddl-auto: validate`. | Use `@Transactional` (Spring) or `TransactionScope` / `BeginTransactionAsync` (.NET) and publish domain events via `@TransactionalEventListener(phase = AFTER_COMMIT)`. |
| **Rust (`sqlx` / `diesel`)** | Use `sqlx migrate add -r` for reversible `.up.sql` / `.down.sql` migrations and compile-time query checking (`sqlx::query!`). | Use `let mut tx = pool.begin().await?; ... tx.commit().await?;` (uncommitted `tx` rolls back automatically on drop). |
| **Mobile / Local Embedded DBs (SQLite / Drift / Room / CoreData)** | Define explicit schema versions (`schemaVersion`) and step-by-step `onUpgrade(db, oldVersion, newVersion)` migrations; enable `PRAGMA foreign_keys = ON;` on every SQLite connection opening. | Test upgrade paths across every historical `oldVersion -> currentVersion` pair in unit tests. |

### Zero-Downtime Expand-and-Contract Decision Matrix

| Schema Operation | Naive Approach (Causes Downtime / Locks / Errors) | Safe Expand-and-Contract Approach |
| :--- | :--- | :--- |
| **Rename a column** | `ALTER TABLE RENAME COLUMN a TO b` while old app pods still query `a`. | 1. Add nullable `b`. 2. Dual-write `a` & `b`, backfill `b`. 3. Switch reads to `b`. 4. Drop `a` in next release. |
| **Add `NOT NULL` column** | `ALTER TABLE ADD COLUMN c TEXT NOT NULL` without default on existing rows, or volatile default rewriting table. | 1. Add nullable `c` (or constant default in PG 11+/MySQL 8.0.12+). 2. Backfill `c` in batches. 3. Add `CHECK (c IS NOT NULL) NOT VALID`, then `VALIDATE CONSTRAINT`. |
| **Add index on huge table** | Blocking `CREATE INDEX` locks writes on PostgreSQL. | Use `CREATE INDEX CONCURRENTLY` outside a transaction block (`ALGORITHM=INPLACE, LOCK=NONE` on MySQL). |
| **Drop a column** | `ALTER TABLE DROP COLUMN a` while running code still runs `SELECT a` or `SELECT *` mapped to ORM struct. | 1. Ignore column in ORM (`@Ignore` / omit from select list) and deploy app. 2. Drop column in subsequent migration release. |

## 7. Security and Safety Considerations

- **Never Run Destructive Commands Without User Consent**: Before executing `migrate:fresh`, `migrate:reset`, `prisma migrate reset`, `DROP TABLE`, or `TRUNCATE` on any database outside an ephemeral in-memory test runner, verify the target database connection and obtain explicit user approval.
- **Multi-Tenant Data Isolation**: In multi-tenant databases, enforce `tenant_id` on every tenant-scoped table, include `tenant_id` in composite indexes and foreign keys, and consider PostgreSQL Row-Level Security (RLS) where appropriate.
- **Least-Privilege Database Roles**: Separate migration/admin credentials (DDL permissions) from runtime application credentials (DML `SELECT, INSERT, UPDATE, DELETE` only) where supported by deployment architecture.

## 8. Verification Criteria

Before declaring database architecture or migration work complete:
1. **Migration Up/Down Proof**: Migrations apply cleanly (`up`), roll back cleanly (`down`, where reversible), and re-apply cleanly on an isolated test database (or SQL syntax/ORM schema validation passes if no database server is running).
2. **Constraint & Foreign Key Proof**: All relations declare explicit `ON DELETE` rules, foreign key columns are indexed, and monetary/timestamp types avoid float and timezone-naive traps.
3. **Transaction & Lock Proof**: Multi-write mutations use transactions, external I/O occurs strictly outside transaction boundaries, and concurrent race conditions are mitigated.

## 9. Failure Handling and Edge Cases

- **MySQL Implicit Commit During Failed Migrations**: Unlike PostgreSQL, MySQL commits DDL statements (`ALTER TABLE`, `CREATE INDEX`) immediately and cannot roll back a partially failed multi-statement migration automatically. Keep MySQL migrations focused on one table/change per file so failures are easy to diagnose and recover.
- **`CREATE INDEX CONCURRENTLY` Inside Transactions**: PostgreSQL forbids `CREATE INDEX CONCURRENTLY` inside a transaction block. Disable migration transaction wrapping (`disableTransaction` / `atomic = False`) for concurrent index migrations.
- **Irreversible Data Migrations**: If a migration drops a column or consolidates data such that `down` cannot losslessly reconstruct previous values, document the migration as irreversible or raise an explicit `IrreversibleMigration` error in `down()` rather than silently creating an empty column that masks data loss.

## 10. Expected Outputs and Reporting Requirements

Provide a structured database architecture report using this template:

```markdown
## Database Architecture & Migration Report

### 1. Schema & Relation Summary
- **Database Engine & Tooling**: [e.g., PostgreSQL 16 + Prisma / MySQL 8 + Laravel Migrations]
- **Tables / Collections Modified**: [List of tables and files]
- **Constraints & Indexes Added**:
  - Primary/Foreign Keys & `ON DELETE` Policy: [Details]
  - Unique / Check Constraints: [Details]
  - Indexes: [Details]

### 2. Transaction, Concurrency & Compatibility Review
- **ACID Boundaries & External I/O Isolation**: [Verified / Details]
- **Concurrency Mechanism**: [e.g., `SELECT ... FOR UPDATE` / Optimistic version / Unique idempotency key]
- **Deployment Compatibility**: [Single-step safe expand / Multi-phase Expand-and-Contract required]
- **Rollback Strategy**: [Reversible `down` migration verified / Forward-fix + backup required]

### 3. Verification Evidence
| Check | Status (PASS / FAIL / BLOCKED / NOT TESTED) | Evidence |
| :--- | :--- | :--- |
| Schema / Migration Validation | [Status] | [Command & output] |
| Migration `up` -> `down` -> `up` Cycle | [Status] | [Command & output] |
| Constraint & Race-Condition Tests | [Status] | [Test results] |
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - `adaptive-architecture-planning` (`SKILL-03`): Defines service and data ownership boundaries.
- **Downstream / Co-Activated Skills**:
  - `query-optimization-performance` (`SKILL-25`): Evaluates composite index order, covering indexes, and query execution plans against the schema.
  - `backend-testing-tdd` (`SKILL-16`) and `test-data-environment-isolation` (`SKILL-18`): Tests constraint enforcement, rollbacks, and concurrency behaviour in isolated test databases.
  - `deployment-readiness` (`SKILL-33`) and `backup-recovery-dr` (`SKILL-35`): Coordinates pre-migration backups and release rollout order.

## 12. Source References

- **PostgreSQL Official Documentation (Constraints, Indexes, Concurrency Control)**: https://www.postgresql.org/docs/current/ddl-constraints.html
- **Prisma / Django / Laravel Official Migration Documentation**: See [../../references/technology-stack-detection-matrix.md](../../references/technology-stack-detection-matrix.md)
- **Shared Library Reference (Deployment Readiness & Migration Safety)**: [../../references/deployment-readiness-quality-gate-matrix.md](../../references/deployment-readiness-quality-gate-matrix.md)
