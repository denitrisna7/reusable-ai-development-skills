---
name: backend-testing-tdd
description: "Mandatory lifecycle skill (SKILL-16). Writes and executes deterministic backend unit, integration, API, RBAC, and DB tests with verbose output. Part of the 38-skill quality suite."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-16"
  category: "Testing and Quality Assurance"
---

# Backend Testing & Test-Driven Development (TDD)

This skill governs the implementation and execution of automated backend tests using the target project's native testing framework and a disciplined Red-Green-Refactor workflow. It ensures thorough, deterministic verification of business logic, request validation, authentication, authorization, database persistence, transactions, error handling, and external integrations.

## 1. Activation Conditions

Activate this skill when the task involves any of the following scenarios:
- Implementing a new backend feature, domain service, API endpoint, CLI command, or background job where automated tests are required.
- Fixing a backend bug by first writing a failing regression test that reproduces the defect (`Red`), applying the minimal fix (`Green`), and cleaning up (`Refactor`).
- Writing or expanding automated tests for request validation, RBAC/ABAC policies, multi-tenant IDOR protection, database constraints, or transactional rollbacks.
- Testing external service integrations, webhook handlers, queues, or scheduled tasks using deterministic fakes, stubs, or HTTP recording/mocking.

## 2. When Not to Use

Do not use this skill as the primary workflow for the following tasks:
- High-level test planning across the entire project before writing test code: start with `testing-strategy-design` (`SKILL-15`).
- Interactive browser UI testing, DOM accessibility tree verification, or visual layout inspection: route to `playwright-mcp-browser-qa` (`SKILL-17`).
- Designing sandboxed test databases, factory architecture, or preventing live third-party side effects at the environment level: coordinate with `test-data-environment-isolation` (`SKILL-18`).

## 3. Scope and Objectives

Every backend test suite created or updated with this skill must cover the following engineering areas where applicable:
- **Red-Green-Refactor TDD Discipline**: Write or update a test that fails for the expected reason before (or alongside) implementing production changes, verify it passes after implementation, and refactor while keeping tests green.
- **Core Business Logic & Domain Rules**: Verify calculations, state transitions, invariant enforcement, boundary values, and domain exceptions.
- **Request Validation & Schema Boundaries**: Verify that missing required fields, wrong data types, out-of-range values, invalid enums, and oversized payloads are rejected with accurate status codes (`400`/`422`) and field-level error keys.
- **Authentication & Authorization (RBAC / IDOR)**: Verify unauthenticated rejection (`401`), unauthorized role rejection (`403`), and cross-user/cross-tenant object access prevention (`403`/`404`).
- **Database Behavior, Constraints & Transactions**: Verify that records are created, updated, or deleted accurately, unique/foreign-key constraints are honored, and multi-step failures trigger a complete transaction rollback with zero orphaned records.
- **Error Handling & Resilience**: Verify that domain failures, not-found states, and unexpected exceptions return consistent, safe error structures without leaking stack traces or sensitive data.
- **External Integrations**: Verify outbound API clients, webhook receivers, queues, and mailers using transport-layer fakes or HTTP stubs (`Http::fake()`, `msw`, `respx`, `httptest.Server`), asserting both the outbound request contract and local handling of `4xx`/`5xx`/timeout responses.
- **Test Isolation & Determinism**: Ensure every test runs independently in any order (`--random` / `--shuffle`) without leaking database rows, static state, environment variables, or time assumptions.
- **Regression Protection**: Lock in every resolved bug with a permanent automated regression test.

## 4. Prerequisites and Context Requirements

Before writing or running backend tests, inspect the project to confirm:
1. **Native Test Runner & Conventions**: Check `composer.json`, `package.json`, `pyproject.toml`, `go.mod`, `pom.xml`, `Cargo.toml`, or `.csproj` to identify the exact test framework, assertion style, and file naming convention (`*Test.php`, `*.test.ts`, `test_*.py`, `*_test.go`).
2. **Test Configuration & Database Safety**: Inspect `phpunit.xml`, `.env.testing`, `vitest.config.*`, or `conftest.py` to confirm tests point to an isolated test database (e.g., SQLite `:memory:` or dedicated `*_test` database), **never** the development or production database (`SKILL-18`).
3. **Existing Factories & Helpers**: Locate existing model factories, builders, auth helpers, and test traits so new tests match established repository conventions.

## 5. Step-by-Step Workflow

Follow this numbered TDD and backend verification workflow:

### Step 1: Inspect the Target Module and Run Actual Test Suite
1. Run the existing test file or module suite via actual CLI command execution (`run_command`) to verify the baseline environment is healthy and runnable. On Laravel 12+ projects, run `./vendor/bin/phpunit --testdox --colors=never` (rather than plain `php artisan test` which collapses output into a single JSON line in AI environments) so every individual test case (`✔`) is printed visibly in the chat response. The agent is strictly forbidden from assuming or hallucinating test passes without real terminal execution evidence. If the test runner fails to execute, report `BLOCKED: Test execution failed to run`.
2. Identify the public contract of the unit, service, or endpoint under test (inputs, return payload, database side effects, dispatched jobs/events, and error conditions).

### Step 2: Write Failing Tests First (The `Red` Phase)
Structure each test clearly using the **Arrange - Act - Assert (AAA)** or **Given - When - Then** pattern:
1. **Arrange**:
   - Create only the minimal required test entities using factories/builders with explicit overrides for the attributes relevant to the test.
   - Freeze or control time (`Carbon::setTestNow()`, `vi.setSystemTime()`, `freezegun`) if timestamps, expiration windows, or billing periods affect the assertion.
   - Stub external network/mail/queue boundaries if the code under test triggers external I/O.
2. **Act**:
   - Invoke the single method, command, or HTTP endpoint under test.
3. **Assert**:
   - Assert the response status code and payload structure.
   - Assert the actual persisted database state (`assertDatabaseHas`, `assertDatabaseMissing`, or direct repository query).
   - Assert dispatched jobs, emitted events, or outbound HTTP request payloads.
4. Run the test and confirm it **fails for the expected reason** (not due to a syntax error or misconfigured test environment).

### Step 3: Implement Minimal Production Code (The `Green` Phase)
1. Write clean, idiomatic production code that satisfies the test requirements without hardcoding test inputs or introducing speculative abstractions (`SKILL-05`).
2. Re-run the test suite to confirm the new test transitions from `FAIL` to `PASS`.

### Step 4: Expand to Boundary, Security, Transaction, and Failure Cases
Before considering the feature tested, add focused tests for:
1. **Validation Matrix**: Invalid payloads assert `400`/`422` and verify that the database row count remains unchanged.
2. **Authorization & IDOR Matrix**:
   - Guest / unauthenticated call -> `401 Unauthorized`.
   - Authenticated user without permission -> `403 Forbidden`.
   - Authenticated user from Tenant A accessing/mutating Tenant B's resource ID -> `403`/`404` and Tenant B's database record remains unmodified.
3. **Transaction Rollback & Concurrency**:
   - Simulate a failure on step 2 of a multi-step database transaction and assert that step 1's database write was completely rolled back.
4. **External Dependency Failure**:
   - Simulate an upstream `503 Service Unavailable`, `429 Too Many Requests`, or timeout from an external API and assert graceful error handling or retry queuing.

### Step 5: Refactor and Verify Suite Isolation (The `Refactor` Phase)
1. Clean up duplication in both production code and test setup helpers while keeping test bodies readable and self-contained.
2. Run the full affected test file and related test suite (including random order execution where supported) to confirm zero state leakage or regressions.

## 6. Technology-Specific Adaptation Rules

Always use the testing framework and idioms native to the repository:
- **PHP (Laravel / Symfony / CodeIgniter)**:
  - Use **Pest** (`it('...', function () { ... })`) or **PHPUnit** (`public function test_...(): void`) matching the project's existing tests. Never force Pest into a PHPUnit-only project or vice versa.
  - In Laravel, use `RefreshDatabase` or `DatabaseTransactions`, Model Factories (`User::factory()->create()`), `Http::fake()`, `Queue::fake()`, `Mail::fake()`, `Event::fake()`, and `$this->actingAs($user)->postJson(...)`.
- **JavaScript / TypeScript (Node.js / Express / Fastify / NestJS / Next.js)**:
  - Use **Vitest**, **Jest**, or Node's built-in `node:test` as configured in `package.json`.
  - Test HTTP handlers with `supertest`, Fastify `.inject()`, or direct Request/Response invocation; mock external HTTP calls at the network layer with `msw` (Mock Service Worker) or `undici` `MockAgent` rather than patching internal modules excessively.
- **Python (pytest / Django / FastAPI / Flask)**:
  - Use **pytest** (`pytest -q`) or `python manage.py test`.
  - Use `factory_boy` or pytest fixtures in `conftest.py`, transactional DB rollback fixtures (`@pytest.mark.django_db`), `httpx.AsyncClient` / `TestClient` for FastAPI, and `respx` or `responses` to mock outbound HTTP calls.
- **Go**:
  - Use standard `testing` (`go test -v -race ./...`) with table-driven subtests (`t.Run(tc.name, func(t *testing.T) { ... })`), `httptest.NewServer` for external HTTP mocks, and `httptest.NewRecorder` for handler verification.
- **Java / Kotlin (Spring Boot)**:
  - Use **JUnit 5**, **AssertJ**, `@DataJpaTest` / `@WebMvcTest` / `@SpringBootTest`, **WireMock** or `MockRestServiceServer` for external HTTP integrations, and `@Transactional` rollback isolation.
- **C# (.NET) & Rust**:
  - In .NET, use **xUnit** / **NUnit**, `WebApplicationFactory<Program>`, and EF Core isolated test databases. In Rust, use `cargo test`, `#[sqlx::test]` for automatic isolated database provisioning, and `wiremock` for HTTP stubbing.

## 7. Security and Safety Considerations

- **Verify Test Database Before Running**: Before running any test that executes migrations, truncations, or `RefreshDatabase`, verify that the test runner is configured to use a dedicated test database (`DB_DATABASE=*_test` or `:memory:`). Never run destructive test suites against a shared or production database.
- **Never Hit Real External Paid/Notification APIs**: Always verify that payment gateways, SMS/WhatsApp senders, email transports, and external webhooks are faked or routed to local sandboxes during test runs.
- **No Disabled Assertions**: Never comment out failing assertions, add `@todo`/`skip` to hide broken behavior without reporting it, or weaken status code checks (`assertTrue(true)`) to manufacture a green test run.

## 8. Verification Criteria

Do not claim backend testing is complete until all of the following are verified with actual command execution evidence:
- [ ] All new and updated backend tests have been executed via the native test runner and passed (`0` failures, `0` errors).
- [ ] Happy path, validation boundaries (`400`/`422`), authentication/authorization (`401`/`403`/IDOR), database persistence, and error/rollback paths are covered.
- [ ] Tests assert concrete observable state (database rows, response payloads, emitted jobs/events) rather than trivial mock return values.
- [ ] Running the test file alongside sibling suites passes cleanly without order-dependent flakiness.

## 9. Failure Handling and Edge Cases

- **Test Fails Due to Missing Local Database Extension or Container**: Do not fake a `PASS` result. Report the exact missing prerequisite (e.g., `pdo_sqlite` missing or local Postgres container stopped), mark database-dependent tests as `BLOCKED` (`SKILL-19`), and run any pure unit tests that can execute in memory.
- **Flaky Time-Dependent or Async Tests**: If a test intermittently fails around midnight, month boundaries, or sub-second timestamps, replace `now()` assumptions with explicit frozen clocks (`2026-03-15 10:00:00 UTC`) and replace arbitrary `sleep()` calls with deterministic queue/promise flushing.
- **Database Transaction Isolation Caveats**: Remember that explicit `DB::commit()` or DDL statements (`TRUNCATE`, `ALTER TABLE` in MySQL) implicitly commit open transactions and break transaction-rollback test wrappers; use explicit cleanup or isolated per-test schemas when testing raw DDL/commit behavior.

## 10. Expected Outputs and Reporting Requirements

Report backend TDD and test execution results using the following template (aligned with `SKILL-19`):

```markdown
# Backend Testing & TDD Verification Report

## 1. Test Command & Environment
- **Framework & Command Executed**: `<e.g., vendor/bin/pest tests/Feature/OrderCreationTest.php>`
- **Database / Isolation Mode**: `<SQLite :memory: / Dedicated Postgres test DB with transaction rollback>`

## 2. Test Coverage & Status Breakdown
| Test Case / Method | Category (`Logic`/`Validation`/`Auth`/`DB`/`Integration`) | Status (`PASS`/`FAIL`/`BLOCKED`/`NOT TESTED`) | Verified Assertions |
| :--- | :--- | :--- | :--- |
| `creates order and deducts inventory atomically` | `Logic + DB` | `PASS` | `201`, `orders` row created, `inventory.stock` decremented. |
| `rolls back order when payment gateway times out` | `Transaction + Integration` | `PASS` | `502`, `orders` count `0`, `inventory.stock` unchanged. |
| `rejects cross-tenant order access (IDOR)` | `Auth / Security` | `PASS` | `404`/`403`, Tenant B order untouched. |
| `rejects negative quantity and missing item_id` | `Validation` | `PASS` | `422`, validation errors on `quantity` and `item_id`. |

## 3. Execution Summary & Diagnostics
- **Total**: `<X passed, Y failed, Z blocked, W not tested>` (`<duration>`)
- **Remaining Risks / Untested Paths**: `<none or explicit explanation>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Receive the test plan from `testing-strategy-design` (`SKILL-15`) and security test requirements from `application-security-owasp` (`SKILL-10`) and `api-security-webhook-reliability` (`SKILL-11`).
- **Parallel / Sibling Skills**: Enforce database and mock safety using `test-data-environment-isolation` (`SKILL-18`), and complement backend tests with browser E2E verification via `playwright-mcp-browser-qa` (`SKILL-17`).
- **Downstream Skills**: Format failure root-cause analysis and execution status using `test-reporting-failure-diagnosis` (`SKILL-19`), and provide test evidence to `ci-cd-release-engineering` (`SKILL-31`) and `final-quality-gate-release-audit` (`SKILL-38`).

## 12. Source References

- **Kent Beck: Test-Driven Development: By Example** (Red-Green-Refactor methodology)
- **PHPUnit / Pest Documentation**: https://docs.phpunit.de/ / https://pestphp.com/docs
- **Vitest / pytest / Go Testing Documentation**: https://vitest.dev/ / https://docs.pytest.org/ / https://pkg.go.dev/testing
