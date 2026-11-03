---
name: test-data-environment-isolation
description: "Mandatory lifecycle skill (SKILL-18). Enforces test environment and database isolation (:memory:/test DBs) with deterministic seeders and mocks. Part of the 38-skill quality suite."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-18"
  category: "Testing and Quality Assurance"
---

# Test Data & Environment Isolation

This skill establishes strict engineering safeguards to ensure that automated test suites and QA sessions execute in isolated, deterministic environments without ever modifying production data, corrupting local development databases, or triggering real external payments, emails, SMS messages, or webhooks.

## 1. Activation Conditions

Activate this skill when the task involves any of the following scenarios:
- Setting up or verifying the test environment before running backend unit/integration tests (`SKILL-16`) or browser QA (`SKILL-17`).
- Designing or refactoring model factories, database seeders, test fixtures, or builder patterns.
- Preventing live outbound HTTP calls, payment charges, email/SMS/push notifications, cloud storage writes, or third-party webhooks during test execution.
- Diagnosing and fixing flaky tests caused by shared mutable database state, parallel worker collisions, unseeded randomness, or wall-clock time dependencies.
- Configuring CI or local test runners (`phpunit.xml`, `.env.testing`, `vitest.config.ts`, `pytest.ini`, Docker Compose test profiles) to enforce safety guardrails.

## 2. When Not to Use

Do not use this skill as the primary workflow for the following tasks:
- Managing production, staging, or live cloud secret stores and runtime `.env` drift: route to `environment-configuration-management` (`SKILL-32`).
- Writing business-logic assertions in a TDD loop once isolation is already verified: route to `backend-testing-tdd` (`SKILL-16`).
- Anonymizing or scrubbing PII in live databases for privacy compliance: route to `privacy-data-protection` (`SKILL-12`).

## 3. Scope and Objectives

Every test environment and test data setup governed by this skill must address and verify:
- **Dedicated Test Environments**: Separate test configuration (`APP_ENV=testing`, `NODE_ENV=test`) strictly from development and production environments.
- **Safe Test Databases**: Route all test runs to a dedicated ephemeral or test-only database (`*_test`, SQLite `:memory:`, or isolated Testcontainers instance) and enforce hard programmatic guards that abort immediately if a non-test database host or name is detected.
- **Preventing Production Data Modification**: Guarantee zero possibility that running a test command can truncate, drop, or mutate production or shared staging tables.
- **Preventing Real Payments, Messages, or External Side Effects**: Block stray outbound network traffic by default in tests and replace payment gateways, email mailers, SMS/WhatsApp providers, push notification services, and webhook dispatchers with local fakes or stubs.
- **Test Fixtures and Composable Factories**: Build minimal, composable model factories/builders with sensible defaults and explicit state traits (`->admin()`, `->expired()`, `->paid()`) rather than brittle monolithic SQL dumps.
- **Deterministic Test Data**: Control all sources of non-determinism including system clocks/timezones, random number generators/UUIDs, and sort order (`ORDER BY`).
- **External Service Mocks & Contract Fidelity**: Ensure HTTP stubs and service fakes accurately mirror the real provider's status codes, headers, payload shapes, and error responses.
- **Cleanup and Per-Test Isolation**: Isolate every test case via database transaction rollbacks, per-worker database schemas, local storage temp directories, and cache/queue flushing so tests pass in any execution order.

## 4. Prerequisites and Context Requirements

Before executing or modifying test suites, inspect the repository to determine:
1. **Environment Resolution Order**: Check how the framework loads test configuration (e.g., `phpunit.xml` `<env>` overrides vs `.env.testing` vs process environment variables) and verify whether OS/container environment variables have `force="true"` precedence.
2. **Database Engine Requirements**: Determine whether tests rely on engine-specific features (e.g., PostgreSQL JSONB/arrays/RLS, MySQL full-text indexes, PostGIS) that require a real containerized database engine rather than SQLite `:memory:`.
3. **External Side-Effect Transports**: Inventory all configured mailers, queues, filesystem disks, cache stores, broadcasting drivers, and third-party API clients.

## 5. Step-by-Step Workflow

Follow this numbered procedure to enforce test data and environment isolation:

### Step 1: Audit and Lock Down Test Environment Configuration
1. **Inspect Test Config Files Before Running Any Test**:
   - Verify that `APP_ENV` / `NODE_ENV` / `FASTAPI_ENV` is forced to `testing` / `test`.
   - Verify that `DB_DATABASE` / `DATABASE_URL` points to `:memory:` or an explicit `*_test` database on `localhost` / `127.0.0.1` / test container host.
   - Check that config caching (e.g., Laravel `bootstrap/cache/config.php`) is cleared or bypassed during test runs so cached development `.env` credentials are never used by mistake!
2. **Add a Hard Startup Guard**:
   - In the global test bootstrap (`TestCase::setUp`, `conftest.py`, `vitest.setup.ts`), assert that the active database name ends with `_test` (or equals `:memory:`) and that the host is not a remote production/cloud RDS endpoint. Abort the test runner immediately if the assertion fails.

### Step 2: Neutralize All External Side Effects by Default
Configure the test environment and global test setup so external transports are inert by default:
1. **Mail / SMS / Push Notifications**: Set drivers to `array` / `log` / `locmem` / in-memory fake (`Mail::fake()`, `Notification::fake()`, Django `locmem.EmailBackend`).
2. **Outbound HTTP & Payment Gateways**:
   - Block unmocked external HTTP requests (`Http::preventStrayRequests()`, `msw` `onUnhandledRequest: 'error'`, `pytest-socket` `--disable-socket` or `respx` strict mode).
   - Provide explicit fixtures/stubs for expected payment, OAuth, or webhook calls using test-only dummy keys (`sk_test_mock_0000`, never live keys).
3. **Object Storage & File Systems**: Route file upload/download tests to ephemeral temporary directories (`Storage::fake('s3')`, `tmp_path` fixture, `os.MkdirTemp`) cleaned up automatically after each test.
4. **Queues & Caches**: Use synchronous or in-memory array drivers (`QUEUE_CONNECTION=sync`, `CACHE_STORE=array`) unless specifically testing Redis/database queue locking against an isolated test Redis DB index.

### Step 3: Implement Per-Test State Isolation and Cleanup
1. **Database Isolation**:
   - Prefer **Transactional Rollback per Test** (`DatabaseTransactions`, `@pytest.mark.django_db`, SQLx test transactions, Spring `@Transactional`) for fast reset.
   - When testing code that commits its own transactions or runs across processes (e.g., browser E2E), use fast table truncation (`TRUNCATE ... RESTART IDENTITY CASCADE`) or per-worker database clones (`test_db_1`, `test_db_2`).
2. **In-Memory & Global State Reset**:
   - Reset singleton instances, static caches, rate-limiter counters, auth sessions, and mocked environment variables in `afterEach` / `tearDown`.

### Step 4: Design Deterministic Factories, Fixtures, and Clocks
1. **Composable Factories**:
   - Define factories that generate valid minimal entities with unique sequence counters (`user-${seq}@example.test`) rather than random small-range numbers that occasionally collide (`faker.numberBetween(1, 10)`).
   - Use reserved non-routable domains (`@example.com`, `@example.test`, `.invalid` per RFC 2606) for all test emails and webhook URLs so accidental delivery is impossible.
2. **Deterministic Time & Randomness**:
   - Freeze the clock (`2026-06-15T12:00:00Z`) whenever testing token expiry, billing cycles, age calculations, or scheduled jobs, and always unfreeze (`useRealTimers` / `setTestNow()`) in `afterEach` / `tearDown`.
   - Always specify explicit `ORDER BY` clauses in queries asserted by tests; never rely on implicit database insertion order.

## 6. Technology-Specific Adaptation Rules

- **PHP (Laravel / Symfony / CodeIgniter)**:
  - In `phpunit.xml`, set `<env name="DB_CONNECTION" value="sqlite" force="true"/>` (or dedicated `*_test` DB) and check `bootstrap/cache/config.php` does not override test env vars (`php artisan config:clear`).
  - Call `Http::preventStrayRequests()` in `TestCase::setUp()` so any unmocked external HTTP call fails loudly instead of hitting the internet.
- **JavaScript / TypeScript (Vitest / Jest / Playwright)**:
  - Use `msw` (`setupServer`) with `server.listen({ onUnhandledRequest: 'error' })` in `beforeAll`, `server.resetHandlers()` in `afterEach`, and `server.close()` in `afterAll`.
  - Call `vi.restoreAllMocks()` and `vi.useRealTimers()` in `afterEach`.
- **Python (pytest / Django / FastAPI)**:
  - In Django, pytest-django automatically creates a `test_*` database and wraps tests in transactions; ensure `EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'`.
  - In FastAPI, override dependencies via `app.dependency_overrides[get_db] = override_get_db` wired to a rollback-only test transaction, and clear `app.dependency_overrides.clear()` in fixture teardown.
- **Go / Rust / Java (Spring Boot) / C# (.NET)**:
  - Use `t.TempDir()` and `t.Cleanup(func() { ... })` in Go; `#[sqlx::test]` in Rust; `@DynamicPropertySource` + Testcontainers or H2/test profile in Spring Boot; and `Respawn` or per-test transactions in .NET.
- **Mobile (Flutter / iOS / Android)**:
  - Inject fake repositories, in-memory SQLite/Hive boxes, and mocked HTTP clients into widget and integration tests so device tests never hit live backend APIs or persist state across runs.
- **Unknown or Mixed Stacks**:
  - Inspect how database connections, environment variables, and HTTP clients are initialized at startup, and enforce test-only connection strings and network interceptors before executing any test command.

## 7. Security and Safety Considerations

- **Never Use Real Production Data Dumps in Tests**: Never import production database dumps containing real customer emails, phone numbers, passwords, or payment tokens into local or CI test databases. If production traffic shapes are needed, synthesize them with factories.
- **RFC 2606 Safe Domains Only**: Never use real company domains or random real-world domains (`@gmail.com`, `@yahoo.com`) in test fixtures; always use `@example.com`, `@example.org`, or `@example.test`.
- **Guard Against `force="true"` Omission**: In PHPUnit and similar runners, omitting `force="true"` on XML environment variables can allow a developer's shell export or `.env` file to point `RefreshDatabase` at a live development or staging database.
- **Dummy Credentials Only**: Use obvious non-functional placeholder tokens (`sk_test_dummy_0000`, `test-webhook-secret`) in `.env.testing` and test fixtures so secret scanners and developers never confuse test fixtures with live keys.

## 8. Verification Criteria

Before declaring test environment and data isolation complete, verify:
- [ ] Test configuration explicitly targets a dedicated test database (`:memory:` or `*_test`) and aborts if pointed at a non-test database.
- [ ] Unmocked external HTTP calls, live emails, SMS messages, and payment gateway calls are blocked or routed to in-memory fakes.
- [ ] All test emails and URLs use reserved RFC 2606 domains (`example.com` / `example.test`).
- [ ] Running the test suite twice in a row and in randomized order (`--random-order` / `--shuffle`) produces identical green results with zero leftover records or temp files.

## 9. Failure Handling and Edge Cases

- **Cached Config Overriding Test `.env`**: If a framework loads cached production/dev configuration during tests, clear the configuration cache (`php artisan config:clear`) and add a check in the test bootstrap that throws an exception if `config('app.env') !== 'testing'`.
- **Parallel Test Workers Colliding on Shared Database or Redis**: Configure per-worker database suffixes (`DB_DATABASE=app_test_${TEST_TOKEN}`) and per-worker Redis prefixes/databases so parallel processes never truncate each other's rows.
- **Engine Mismatch Between SQLite and Production Postgres/MySQL**: If production migrations or queries use Postgres/MySQL-specific syntax (`JSONB`, `ILIKE`, window functions, enum alterations), use a dedicated local Postgres/MySQL `*_test` database rather than forcing incompatible SQLite workarounds into production code.

## 10. Expected Outputs and Reporting Requirements

Document test data and environment isolation verification using the following template:

```markdown
# Test Data & Environment Isolation Audit

## 1. Environment & Database Isolation
- **Test Configuration Source**: `<phpunit.xml / .env.testing / vitest.config.ts / conftest.py>`
- **Active Test Database**: `<sqlite :memory: / postgres app_test on 127.0.0.1>`
- **Non-Test DB Abort Guard**: `Verified active in <file:line>`
- **State Reset Mechanism**: `<Per-test transaction rollback / TRUNCATE / per-worker schema>`

## 2. External Side-Effect Isolation Matrix
| External Boundary | Test Isolation Mechanism | Stray Call Protection | Status (`PASS`/`FAIL`/`N/A`) |
| :--- | :--- | :--- | :--- |
| Outbound HTTP / Payment APIs | `<Http::fake() / MSW / respx>` | `<preventStrayRequests / onUnhandledRequest: error>` | `PASS` |
| Email / SMS / Notifications | `<array / locmem / Mail::fake()>` | `<RFC 2606 @example.test domains enforced>` | `PASS` |
| Object Storage / File Uploads | `<Storage::fake() / tmp_path>` | `<Auto-cleaned on teardown>` | `PASS` |
| Clocks / Randomness | `<Frozen clock + sequence factories>` | `<Restored in afterEach/tearDown>` | `PASS` |

## 3. Determinism Verification
- **Randomized Order Execution**: `<Command run + PASS result>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Receive test architecture requirements from `testing-strategy-design` (`SKILL-15`) and privacy rules from `privacy-data-protection` (`SKILL-12`).
- **Parallel / Sibling Skills**: Serve as the mandatory safety foundation for `backend-testing-tdd` (`SKILL-16`) and `playwright-mcp-browser-qa` (`SKILL-17`).
- **Downstream Skills**: Provide deterministic execution guarantees to `ci-cd-release-engineering` (`SKILL-31`) and `test-reporting-failure-diagnosis` (`SKILL-19`).

## 12. Source References

- **RFC 2606 (Reserved Top Level DNS Names for Testing: `.test`, `.example`, `.invalid`, `.localhost`)**: https://www.rfc-editor.org/rfc/rfc2606
- **Martin Fowler: Eradicating Non-Determinism in Tests**: https://martinfowler.com/articles/nonDeterminism.html
- **Mock Service Worker (MSW) Documentation**: https://mswjs.io/docs/
