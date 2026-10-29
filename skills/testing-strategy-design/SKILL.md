---
name: testing-strategy-design
description: "Designs risk-based testing strategies across unit, integration, API, E2E, security, and performance levels. Use when planning test coverage. Do not use for running a single test."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-15"
  category: "Testing and Quality Assurance"
---

# Testing Strategy & Test Design

This skill establishes a disciplined, risk-driven methodology for designing an effective testing strategy tailored to a project's actual architecture, domain risks, and delivery constraints. It ensures appropriate allocation across unit, integration, feature, API, end-to-end (E2E), regression, acceptance, performance, and security tests while explicitly enforcing a core engineering principle: **never maximize test count at the expense of test quality**.

## 1. Activation Conditions

Activate this skill when the task involves any of the following scenarios:
- Designing the overall test architecture or QA plan for a new project, service, or major feature module.
- Determining which test levels (unit vs. integration vs. API vs. browser E2E) should verify a set of requirements and acceptance criteria.
- Auditing an existing test suite that suffers from slow execution, high flakiness, excessive mocking, or low defect-detection value.
- Establishing risk-based test priorities when time or environment constraints prevent exhaustive testing of every permutation.
- Defining regression, acceptance, performance, and security verification gates prior to a major refactoring or production release.

## 2. When Not to Use

Do not use this skill as the primary workflow for the following tasks:
- Writing and running concrete backend unit/integration test code in a TDD loop: route to `backend-testing-tdd` (`SKILL-16`).
- Executing interactive browser QA and accessibility snapshot verification with Playwright MCP: route to `playwright-mcp-browser-qa` (`SKILL-17`).
- Configuring test databases, factories, mocks, and sandbox isolation: route to `test-data-environment-isolation` (`SKILL-18`).
- Formatting a test execution report or diagnosing a specific test failure: route to `test-reporting-failure-diagnosis` (`SKILL-19`).

## 3. Scope and Objectives

Every testing strategy designed under this skill must evaluate and define the role of each applicable test level:
- **Project-Specific Strategy Selection**: Tailor the test pyramid or testing trophy to the application's actual architecture (e.g., domain-heavy library vs. CRUD web app vs. microservice API vs. full-stack SPA).
- **Unit Tests**: Verify pure domain logic, calculations, state machines, parsers, and edge-case branching in fast, isolated memory execution.
- **Integration Tests**: Verify real interactions across component boundaries, including database queries, ORM mappings, constraints, cache layers, and queue serialization.
- **Feature & API Tests**: Verify full HTTP/RPC request-to-response flows including routing, middleware, request validation, authentication, authorization, database side effects, and response contracts.
- **End-to-End (E2E) Browser/Client Tests**: Verify critical user journeys across the real rendered UI, client state, network boundary, and backend persistence.
- **Regression Tests**: Lock in deterministic reproductions for every fixed bug and guard high-risk legacy behavior before refactoring.
- **Acceptance Tests**: Map test cases directly to user-facing acceptance criteria (`AC-01`, `AC-02`) so every business requirement has an executable proof.
- **Performance Tests**: Define targeted load, latency, query-count (`N+1`), or bundle/Core Web Vitals benchmarks where performance is a material requirement.
- **Security Tests**: Include negative test cases for unauthenticated access (`401`), unauthorized/IDOR access (`403`/`404`), injection/XSS payloads, CSRF enforcement, and rate limits (`429`).
- **Risk-Based Test Selection**: Prioritize test depth based on business impact, failure likelihood, security exposure, and change frequency.
- **Test Coverage Limitations & Quality Enforcement**: Recognize why line coverage percentages can be misleading, avoid tautological mock-heavy tests, and prioritize behavioral assertions over raw test count.

## 4. Prerequisites and Context Requirements

Before designing a testing strategy, inspect the repository to gather:
1. **Application Architecture & Stack**: Identify the language, framework, database, frontend rendering model (SSR, SPA, mobile, API-only), and external dependencies.
2. **Existing Test Infrastructure**: Check existing test runners, directory structures (`tests/Unit`, `tests/Feature`, `e2e/`), CI pipeline stages, fixtures, and helper utilities.
3. **Requirements & Risk Profile**: Review the acceptance criteria (from `SKILL-02`) and threat register (from `SKILL-13`) to identify critical business flows and failure modes.
4. **Execution Constraints**: Identify whether a local database, container runtime, or dev server is available for integration and browser tests.

## 5. Step-by-Step Workflow

Follow this numbered procedure to design a high-signal testing strategy:

### Step 1: Audit Existing Test Capabilities and Risk Hotspots
1. Inspect existing test configs (`phpunit.xml`, `vitest.config.ts`, `pytest.ini`, `playwright.config.ts`, `go.mod`, `Cargo.toml`) to understand current test conventions.
2. Classify the modules/features in scope by **Risk Tier**:
   - **Tier 1 (Critical)**: Authentication, authorization/tenancy, payments, ledger/inventory mutations, data deletion/privacy, and core user onboarding/checkout journeys.
   - **Tier 2 (Standard)**: Standard CRUD workflows, filtering/search, notifications, import/export, and dashboard views.
   - **Tier 3 (Low Risk)**: Static presentation helpers, simple configuration wiring, and cosmetic UI adjustments.

### Step 2: Assign Verification to the Lowest Effective Test Level
Apply the **Lowest Effective Level Principle**: verify each behavior at the fastest, most deterministic layer capable of providing genuine confidence, without duplicating identical combinatorial permutations across slower layers:
1. **Combinatorial & Edge-Case Matrix -> Unit Tests**: Test 15 boundary conditions of a tax/discount calculation in fast unit tests (~milliseconds), not in 15 full-browser E2E runs (~minutes).
2. **Data Integrity, Queries, & Auth Policies -> Integration / Feature / API Tests**: Test HTTP status codes, validation rules, RBAC/IDOR scoping, database constraints, and transactions against a real test database.
3. **Critical User Journeys & Visual/DOM Wiring -> E2E / Browser QA**: Test the primary happy paths, form submission wiring, auth redirects, and critical error states in a real browser (`playwright-mcp-browser-qa`).

### Step 3: Map Requirements to Explicit Positive, Negative, and Boundary Cases
For every feature in scope, design test cases across four mandatory dimensions:
1. **Happy Path (Acceptance)**: Valid actor + valid input produces the expected return value, HTTP response, UI update, and persisted database state.
2. **Boundary & Validation Cases**: Empty inputs, missing required fields, maximum length boundaries, zero/negative numbers, invalid enums, and malformed formats return structured `400`/`422` errors with zero partial database corruption.
3. **Security & Authorization Negative Cases**: Unauthenticated callers receive `401`; unauthorized roles or cross-tenant IDOR attempts receive `403`/`404` and leave target records untouched.
4. **Failure, Concurrency & Idempotency Cases**: Duplicate submissions, concurrent race conditions, or simulated upstream API failures roll back cleanly or handle retries idempotently.

### Step 4: Enforce Test Quality Over Test Quantity
Audit every proposed test against these anti-slop quality rules:
- **No Mock-Tautology Tests**: Never mock the exact class or query under test and merely assert that the mock returned what it was configured to return. Mock only external third-party boundaries (HTTP gateways, email/SMS, clocks) when testing application flows.
- **Behavioral Assertions Over Implementation Coupling**: Assert observable outcomes (returned values, database records, emitted events, HTTP payloads, accessible DOM state) rather than fragile private method call counts.
- **Explain Coverage Limitations**: Document what line coverage does *not* prove (e.g., 100% line coverage with mocked repositories does not verify SQL syntax, foreign key constraints, or production configuration).

### Step 5: Define the Execution Plan and Quality Gates
1. Organize tests into fast local feedback loops (unit + targeted feature tests) and full pre-merge/release suites (all integration, API, security, and E2E checks).
2. Specify the exact commands and environment prerequisites required to run each suite cleanly.

## 6. Technology-Specific Adaptation Rules

Select testing layers and runners native to the detected stack; never force foreign test tools onto a project:
- **PHP (Laravel / Symfony / CodeIgniter)**:
  - Use **Pest** or **PHPUnit** (whichever the repository already uses). Leverage Feature/HTTP tests (`$this->actingAs($user)->postJson(...)`) with transactional database traits for controller/policy/validation flows, and Unit tests for isolated domain services.
- **JavaScript / TypeScript (Node.js / React / Next.js / Vue)**:
  - Use **Vitest** or **Jest** for unit/integration tests, **Testing Library** (`@testing-library/react` / `vue`) for component behavior via accessible roles, **Supertest** or native handler invocation for API routes, and **Playwright** / **Playwright MCP** for browser E2E.
- **Python (Django / FastAPI / Flask)**:
  - Use **pytest** (or Django `manage.py test`) with `httpx.AsyncClient` / `TestClient` (FastAPI) or Django `Client` for API/feature tests, and fixtures (`conftest.py`) for isolated database sessions.
- **Go**:
  - Use table-driven tests with the standard `testing` package (`go test -race ./...`), `httptest.NewServer` / `httptest.NewRecorder` for HTTP handlers, and real test databases for repository tests.
- **Java (Spring Boot) / C# (.NET) / Rust**:
  - Use **JUnit 5** + `@WebMvcTest`/`@DataJpaTest`/Testcontainers (Java), **xUnit** + `WebApplicationFactory` (.NET), or `cargo test` (`#[test]`, `#[tokio::test]` in Rust).
- **Mobile (Flutter)**:
  - Balance Flutter `test` (unit), `testWidgets` (widget tests for UI states and accessibility), and `integration_test` for full device flows.
- **Unknown or Mixed Stacks**:
  - Inspect build scripts, CI definitions, and directory conventions first to identify the native test runner; design the test allocation matrix around the actual runtime boundaries before writing new test files.

## 7. Security and Safety Considerations

- **Mandatory Security Test Allocation**: No test strategy for an authenticated or state-changing feature is complete without explicit negative authorization (`401`/`403`/IDOR) and input validation test cases.
- **Production Safety**: Ensure the test strategy specifies isolated test databases and mocked external payment/messaging transports before any test command is executed (`SKILL-18`).
- **Rate-Limit & Abuse Verification**: Include explicit test cases verifying that brute-force and high-cost endpoints enforce rate-limit thresholds (`429 Too Many Requests`).

## 8. Verification Criteria

A testing strategy and test design artifact is complete only when:
- [ ] Every requirement and acceptance criterion (`AC-XX`) is mapped to at least one concrete test level and test case.
- [ ] The strategy explicitly covers positive, boundary/validation, negative security/authorization, and failure/idempotency scenarios.
- [ ] Each test is placed at the lowest effective level (avoiding redundant slow E2E permutations while ensuring real integration boundaries are tested).
- [ ] High-value behavioral assertions are prioritized over superficial line coverage or mock-tautology test counts.
- [ ] Coverage limitations and any untestable environmental dependencies are explicitly documented.

## 9. Failure Handling and Edge Cases

- **Legacy Codebase With Zero Existing Tests**: Do not attempt to write unit tests for tightly coupled legacy classes before refactoring. Design higher-level **Characterization / Feature Tests** at the HTTP or service boundary first to lock in current observable behavior, then refactor and add unit tests incrementally (`SKILL-08`).
- **Resource-Constrained Local Environment**: If heavy performance load testing or external sandbox integration cannot run locally, define deterministic local checks (e.g., query-count assertions to catch `N+1` regressions) and document the staging load-test requirement honestly.

## 10. Expected Outputs and Reporting Requirements

Present the testing strategy and test design matrix using the following template:

```markdown
# Testing Strategy & Test Design Plan

## 1. Architecture & Risk Summary
- **Target Feature / System**: `<scope>`
- **Detected Test Stack**: `<runner, assertion library, DB isolation strategy, browser tool>`
- **High-Risk Areas (Tier 1)**: `<auth, tenancy, payments, concurrency, data integrity>`

## 2. Multi-Layer Test Allocation Matrix
| Test ID | Requirement / Risk Ref | Test Level (`Unit`/`Integration`/`API`/`E2E`/`Security`/`Perf`) | Scenario & Input | Expected Observable Outcome |
| :--- | :--- | :--- | :--- | :--- |
| `TC-01` | `AC-01` | `Unit` | Calculate tiered tax across boundary amounts (`0`, `max`, negative). | Exact decimal output or domain validation error. |
| `TC-02` | `AC-02 / SR-01` | `Feature / API` | Authenticated user submits valid order (`POST /api/orders`). | `201 Created`, DB row persisted, stock decremented atomically. |
| `TC-03` | `SR-02 (IDOR)` | `Security / API` | Tenant A user requests Tenant B order (`GET /api/orders/:b_id`). | `404 Not Found` or `403 Forbidden`; no data leaked. |
| `TC-04` | `AC-03` | `E2E Browser` | Complete checkout form and verify confirmation state via accessibility snapshot. | Confirmation heading rendered, zero console/network errors. |

## 3. Coverage Limitations & Quality Guardrails
- **Mocking Boundary**: `<Only external payment/email gateways mocked; DB and policies run for real>`
- **Known Coverage Gaps / Untested Areas**: `<Document any environment-blocked tests>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Consume acceptance criteria from `requirements-analysis` (`SKILL-02`), architectural boundaries from `adaptive-architecture` (`SKILL-03`), and threat priorities from `threat-modeling-risk-assessment` (`SKILL-13`).
- **Downstream Execution Skills**: Route backend unit/integration/API test implementation to `backend-testing-tdd` (`SKILL-16`), browser QA to `playwright-mcp-browser-qa` (`SKILL-17`), environment setup to `test-data-environment-isolation` (`SKILL-18`), and execution reporting to `test-reporting-failure-diagnosis` (`SKILL-19`).

## 12. Source References

- **Martin Fowler: The Practical Test Pyramid**: https://martinfowler.com/articles/practical-test-pyramid.html
- **OWASP Web Security Testing Guide (WSTG)**: https://owasp.org/www-project-web-security-testing-guide/
- **Google Testing Blog / Software Engineering at Google (Testing Overview)**: https://abseil.io/resources/swe-book
