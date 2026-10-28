---
name: final-quality-gate
description: Executes the comprehensive 15-domain Final Quality Gate and Release Audit, consolidating evidence from all engineering skills (`SKILL-01` through `SKILL-37`) and integrating with `deployment-readiness` (`SKILL-33`). Activate for final pre-release verification or project sign-off. Never fabricate evidence or execute unauthorized deployments.
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-38"
  category: "Final Quality and Maintenance"
---

# Final Quality Gate & Release Audit

This skill is the terminal verification authority of the engineering lifecycle. It consolidates empirical evidence from all applicable skills (`SKILL-01` through `SKILL-37`), integrates directly with `deployment-readiness` (`SKILL-33`), and audits the system across 15 mandatory engineering domains before any release sign-off. It enforces three non-negotiable rules: **a successful compiler build is never sufficient proof of deployment readiness**, **test results and evidence must never be fabricated**, and **auditing release readiness never authorizes executing a live deployment**.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Performing a final quality gate review, pre-release audit, or production readiness sign-off for an application or major feature delivery.
- Consolidating verification evidence across requirements, code quality, security, automated testing, database migrations, UI/UX accessibility, performance, and operations.
- Issuing a formal release readiness verdict (`READY`, `READY WITH ACCEPTED RISKS`, `BLOCKED`, or `INCOMPLETE`).
- Concluding an end-to-end engineering build where the user asks whether the system is production-ready.

## 2. When Not to Use

Do not activate this skill when the task is strictly limited to:
- Early brainstorming or initial requirements gathering before implementation exists (route to `project-discovery`, `SKILL-01`, and `requirements-analysis`, `SKILL-02`).
- Fixing a single isolated syntax error or unit test mid-development before the broader task is ready for holistic verification.
- Executing a live production deployment command (this skill only evaluates and audits; it never deploys).

## 3. Scope and Objectives

The Final Quality Gate must systematically assess all **15 mandatory areas** (detailed in `[references/gate-checklist.md](references/gate-checklist.md)`):
1. **Requirements and Acceptance Criteria**: 100% traceability from user prompt/specs and edge cases to verified implementation.
2. **Functional Completeness**: Zero dead UI controls (`R-26`), zero placeholder stubs or fake handlers disguised as working features (`SKILL-05`).
3. **Code Quality**: Clean linter, formatter, typechecker, and static analysis verification (`SKILL-07`).
4. **Automated Tests**: Executed unit, integration, and E2E regression tests passing in an isolated test environment (`SKILL-15` to `SKILL-19`).
5. **Security Review**: Verified authentication, authorization (BOLA/IDOR), injection prevention, CSRF/CORS, file upload safety, and AI prompt-injection defenses (`SKILL-10` to `SKILL-14`).
6. **Dependency Vulnerability Checks**: Verified lockfile integrity and clean vulnerability audit (`SKILL-09`).
7. **Database Integrity and Migrations**: Verified constraints, transactions, query performance, and backward-compatible expand/contract migrations (`SKILL-24` to `SKILL-26`).
8. **API and External Integration Reliability**: Verified timeouts, bounded backoff retries, webhook HMAC verification, and idempotency (`SKILL-11`, `SKILL-27`, `SKILL-28`).
9. **UI/UX and Accessibility**: Verified loading/empty/error states (`R-27`), WCAG 2.2 AA contrast (`R-25`), keyboard navigation (`R-32`), and responsive reflow (`R-03`) (`SKILL-17`, `SKILL-20` to `SKILL-23`).
10. **Performance Against Relevant Targets**: Verified latency, query counts, memory, caching, and Core Web Vitals (`LCP <= 2.5s`, `INP <= 200ms`, `CLS <= 0.1` at p75) with zero unsubstantiated claims (`SKILL-22`, `SKILL-29`, `SKILL-30`).
11. **Environment Configuration and Secret Handling**: Verified secret isolation, startup fail-fast validation, `DEBUG=false` production default, and `.env.example` parity (`SKILL-32`).
12. **Backup and Rollback Readiness**: Verified pre-deploy backup coverage and documented artifact + schema rollback procedure (`SKILL-33`, `SKILL-35`).
13. **Logging, Monitoring, and Health Checks**: Verified structured logs with secret redaction, correlation IDs, and `/health` + `/ready` endpoints (`SKILL-34`).
14. **Documentation**: Verified clean-clone setup, testing, architecture, and operations handoff docs aligned with the actual system (`SKILL-37`).
15. **Post-Deployment Smoke-Test Readiness**: Verified concrete post-release smoke-test checklist (`SKILL-31`, `SKILL-33`).

## 4. Prerequisites and Context Requirements

Before issuing a Final Quality Gate verdict, review:
1. **The Shared Quality Gate Contract**: Read `[../../references/deployment-readiness-quality-gate-matrix.md](../../references/deployment-readiness-quality-gate-matrix.md)` and `[references/gate-checklist.md](references/gate-checklist.md)`.
2. **Project Technology & Risk Profile**: Identify which of the 15 domains apply to the current stack and which (if any) are architecturally non-applicable (for example, Gate 07 on a stateless app without a database, or Gate 09 on a pure backend API).
3. **Deployment Readiness Integration (`SKILL-33`)**: Incorporate or execute the operational checks from `deployment-readiness` (`SKILL-33`) so operational release safety and code quality are evaluated together.

## 5. Step-by-Step Workflow

### Step 1: Establish Scope and Justify Any Excluded Domains
- [ ] Evaluate all 15 Gate Domains against the project's actual technology stack, requirements, and risk profile.
- [ ] Remember that Gates **01 (Requirements)**, **02 (Functional Completeness)**, **03 (Code Quality)**, **04 (Automated Tests)**, **05 (Security)**, **10 (Performance)**, **11 (Environment/Secrets)**, and **14 (Documentation)** can **never** be excluded.
- [ ] For any conditionally excludable domain (Gates 06, 07, 08, 09, 12, 13, 15), record an explicit technical justification if marked `EXCLUDED (Justified N/A)`.

### Step 2: Execute Verification Commands and Gather Real Evidence
- [ ] Run the project's actual verification suite (linter, typechecker, static analyzer, unit/integration test runner, dependency audit, migration check, and production build) whenever the environment permits.
- [ ] Never stop after `npm run build` or `cargo build` succeeds: **a passing build is only one check inside Gate 03/15 and never proves functional, security, test, or operational readiness.**
- [ ] Inspect code, configurations, migrations, and templates directly for checks that require structural review (OWASP access control, N+1 queries, secret redaction, UI states, rollback docs).

### Step 3: Classify Every Check with Strict Evidence Accounting
- [ ] Using `[references/gate-checklist.md](references/gate-checklist.md)`, classify each of the 15 domains into six explicit accounting buckets:
  1. **Checks Actually Executed**: Commands or inspections actively performed during this audit.
  2. **Checks Passed Based on Evidence**: Items verified compliant with cited command output or file:line proof.
  3. **Checks Failed**: Any defect, failing test, vulnerability, or missing mandatory safeguard discovered.
  4. **Checks Blocked by Environmental Limitations**: Applicable checks that could not run due to sandbox/credential constraints.
  5. **Checks Not Executed**: Applicable checks that were skipped or not yet run.
  6. **Risks Requiring Human Approval**: Residual non-blocking trade-offs requiring explicit sign-off by the human decision-maker.

### Step 4: Remediate Blocking Defects or Compute the Final Verdict
- [ ] If the user requested both remediation and final verification, fix any discovered `FAIL` items and re-run the affected verification gates before issuing the final report.
- [ ] Determine the single authoritative release verdict:
  - **`READY`**: All applicable mandatory checks across all 15 domains were executed and passed with recorded evidence; zero `FAIL`, zero unaccepted `BLOCKED`, zero `NOT EXECUTED` mandatory checks.
  - **`READY WITH ACCEPTED RISKS`**: All critical checks passed; remaining non-blocking risks or environmental verification gaps are documented with impact, mitigation, and explicit human approval requirements.
  - **`BLOCKED`**: One or more critical requirements failed (`FAIL`), or a mandatory security, data-integrity, test, or migration gate is blocked.
  - **`INCOMPLETE`**: Required verification checks were not executed or mandatory evidence is missing.

## 6. Technology-Specific Adaptation Rules

Adapt the 15-point verification execution to the project's actual stack. Never force PHPStan, Pint, Pest, shadcn/ui, or Playwright where inapplicable to the repository:
- **PHP (Laravel / Symfony / CodeIgniter)**: Execute `composer validate --strict`, `composer audit`, code style (`./vendor/bin/pint --test` or `php-cs-fixer` if installed), static analysis (`./vendor/bin/phpstan analyse` if configured), automated tests (`php artisan test` / `./vendor/bin/pest` / `./vendor/bin/phpunit`), migration status check, and `config:cache` / `route:cache` verification.
- **JavaScript / TypeScript (React / Next.js / Vue / Node.js)**: Execute lockfile consistency check, `npm audit` / `pnpm audit`, ESLint/Biome, `tsc --noEmit`, Vitest/Jest unit/integration suites, Playwright E2E browser verification (when web UI is in scope), and production build verification (`npm run build`).
- **Python (Django / FastAPI / Flask)**: Execute `pip-audit` / `uv` lock check, Ruff (`ruff check` & `ruff format --check`), Mypy/Pyright, `pytest`, `python manage.py check --deploy`, and `makemigrations --check --dry-run`.
- **Go**: Execute `go mod verify`, `go vet ./...`, `golangci-lint run`, `go test -race ./...`, `govulncheck ./...`, and binary compilation check.
- **Java / Spring Boot**: Execute `./mvnw verify` or `./gradlew check`, Spotless/Checkstyle, JUnit 5 + Testcontainers integration suite, Flyway/Liquibase schema validation, and OWASP dependency check.
- **Rust**: Execute `cargo fmt --all -- --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test --locked`, `cargo audit`, and `cargo build --release --locked`.
- **C# / .NET**: Execute `dotnet restore --locked-mode`, `dotnet format --verify-no-changes`, `dotnet build -warnaserror`, `dotnet test`, and `dotnet list package --vulnerable`.
- **Mobile / Flutter**: Execute `flutter analyze --fatal-infos`, `flutter test`, widget accessibility semantics inspection, and platform release build verification.
- **Unknown or Mixed Stacks**: Discover and run all configured linters, typecheckers, test suites, dependency scanners, and build targets across every service in the repository, and audit any remaining domains statically with explicit evidence notes.

## 7. Security and Safety Considerations

- **Absolute Prohibition on Fabricated Evidence**: Never invent test pass counts, coverage percentages, benchmark latencies, or vulnerability scan outputs. If a command was not run or failed to run in the current environment, state that fact transparently.
- **No Unauthorized Deployment**: Concluding with a `READY` verdict authorizes the human team that the codebase passed engineering verification; the agent must **never** trigger a live production deployment unless explicitly instructed in a dedicated deployment task.

## 8. Verification Criteria

Before delivering the Final Quality Gate & Release Audit Report, confirm:
1. **All 15 Domains Accounted For**: None of the 15 mandatory assessment areas are omitted from the audit table.
2. **Evidence Attribution**: Every `PASS` entry cites concrete evidence (command exit status, test count, or file/line reference).
3. **Six Accounting Categories Explicitly Listed**: Executed, Passed, Failed, Blocked by Environment, Not Executed, and Risks Requiring Human Approval are explicitly broken down.
4. **Single Valid Verdict**: The report concludes with exactly one of `READY`, `READY WITH ACCEPTED RISKS`, `BLOCKED`, or `INCOMPLETE`.

## 9. Failure Handling and Edge Cases

- **No Automated Test Suite Exists in Legacy Repo**: Never mark Gate 04 (`Automated Tests`) as `PASS` or `EXCLUDED`. Mark Gate 04 as `FAIL` or `BLOCKED` and set the overall verdict to `BLOCKED` or `INCOMPLETE` (or `READY WITH ACCEPTED RISKS` only if the human owner explicitly accepts shipping without automated tests).
- **Sandbox Lacks Database Daemon for Live Integration Tests**: Run all unit and static checks that do not require the daemon, inspect the database migrations and integration test code statically, record the live DB test execution under **Checks Blocked by Environmental Limitations**, and provide the exact command for the user to run prior to deployment.

## 10. Expected Outputs and Reporting Requirements

Always produce the authoritative **Final Quality Gate & Release Audit Report** using this exact structure:

```markdown
# Final Quality Gate & Release Audit Report

- **Project / Release Scope**: `<application or feature name>`
- **Final Release Verdict**: `<READY | READY WITH ACCEPTED RISKS | BLOCKED | INCOMPLETE>`
- **Deployment Readiness (`SKILL-33`) Integration**: `<Aligned | No live deployment executed>`

## 1. The 15-Domain Quality Gate Matrix
| # | Gate Domain | State (`EXECUTED-PASS` / `FAIL` / `BLOCKED` / `NOT EXECUTED` / `EXCLUDED`) | Concrete Evidence or Exclusion Justification |
| :--- | :--- | :--- | :--- |
| **01** | Requirements & Acceptance Criteria | `<State>` | `<Traceability summary>` |
| **02** | Functional Completeness (Anti-Slop) | `<State>` | `<Zero dead controls / stubs verified>` |
| **03** | Code Quality & Static Analysis | `<State>` | `<Linter, formatter, typecheck output>` |
| **04** | Automated Tests | `<State>` | `<Test suite command & pass/fail count>` |
| **05** | Security Review (OWASP) | `<State>` | `<Authz, injection, CSRF/CORS, uploads verified>` |
| **06** | Dependency Vulnerability Checks | `<State>` | `<Lockfile & audit command output>` |
| **07** | Database Integrity & Migrations | `<State>` | `<FKs, transactions, expand/contract migration check>` |
| **08** | API & External Integration Reliability | `<State>` | `<Timeouts, backoff retries, idempotency, webhooks>` |
| **09** | UI/UX & Accessibility (WCAG 2.2) | `<State>` | `<Loading/empty/error states, contrast, keyboard, responsive>` |
| **10** | Performance Against Targets | `<State>` | `<Baseline vs post-change metrics / CWV mechanisms>` |
| **11** | Environment Config & Secret Handling | `<State>` | `<Zero leaked secrets, fail-fast validation, .env.example>` |
| **12** | Backup & Rollback Readiness | `<State>` | `<Backup verification & rollback runbook>` |
| **13** | Logging, Monitoring & Health Checks | `<State>` | `<Structured logs, redaction, correlation IDs, /health & /ready>` |
| **14** | Documentation & Developer Handoff | `<State>` | `<README, setup, testing, and ops docs verified>` |
| **15** | Post-Deployment Smoke-Test Readiness | `<State>` | `<Post-deploy smoke-test checklist defined>` |

## 2. Explicit Audit Evidence Breakdown
- **Checks Actually Executed**: `<count and list>`
- **Checks Passed Based on Evidence**: `<count and list>`
- **Checks Failed**: `<count and list (0 required for READY)>`
- **Checks Blocked by Environmental Limitations**: `<count and list>`
- **Checks Not Executed**: `<count and list>`
- **Risks Requiring Human Approval**: `<list with impact, mitigation, and sign-off owner>`

## 3. Required Remediation Actions (If `BLOCKED` or `INCOMPLETE`)
1. `<Actionable fix with file path and verification command>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Consolidates evidence from all engineering skills (`SKILL-01` through `SKILL-37`), with direct operational integration from `deployment-readiness` (`SKILL-33`) and test execution evidence from `test-reporting-failure-diagnosis` (`SKILL-19`).
- **Downstream Skills**: If any gate fails, routes remediation back to the domain-specific skill (`SKILL-07` for static analysis, `SKILL-10` for OWASP security, `SKILL-16`/`SKILL-17` for tests, `SKILL-24` for migrations, or `SKILL-37` for documentation) before re-running this gate.

## 12. Source References

- **Local 15-Point Audit Worksheet**: [references/gate-checklist.md](references/gate-checklist.md)
- **Shared Deployment Readiness & Quality Gate Matrix**: [../../references/deployment-readiness-quality-gate-matrix.md](../../references/deployment-readiness-quality-gate-matrix.md)
