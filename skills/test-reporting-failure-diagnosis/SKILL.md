---
name: test-reporting-failure-diagnosis
description: "Mandatory lifecycle skill (SKILL-19). Produces evidence-backed PASS/FAIL test reports with verbose failure diagnosis and reproduction steps. Part of the 38-skill quality suite."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-19"
  category: "Testing and Quality Assurance"
---

# Test Reporting & Failure Diagnosis

This skill enforces strict, evidence-backed honesty in all quality assurance reporting and provides a systematic engineering workflow for diagnosing test failures and regressions. It mandates an explicit four-state classification (`PASS`, `FAIL`, `BLOCKED`, `NOT TESTED`) for every verification check and strictly prohibits claiming a test passed if it was not actually executed and verified.

## 1. Activation Conditions

Activate this skill when the task involves any of the following scenarios:
- Reporting the outcome of any unit, integration, API, security, performance, or browser E2E test execution.
- Investigating a failing test (`FAIL`), a newly introduced regression, or an intermittent flaky test in local development or CI.
- Documenting why a verification check could not be run due to missing credentials, stopped containers, or sandbox restrictions (`BLOCKED` / `NOT TESTED`).
- Consolidating test evidence and diagnostic findings for code review, bug triage, deployment readiness (`SKILL-33`), or the final quality gate (`SKILL-38`).

## 2. When Not to Use

Do not use this skill as the primary workflow for the following tasks:
- Designing the initial test plan before running any tests: route to `testing-strategy-design` (`SKILL-15`).
- Diagnosing live production outages, APM alerts, or distributed tracing incidents outside of test verification: route to `observability-incident-diagnosis` (`SKILL-34`).
- Authoring new backend feature code and unit tests from scratch: route to `backend-testing-tdd` (`SKILL-16`) first, then use this skill to report results and diagnose failures.

## 3. Scope and Objectives

Every test report and failure diagnosis governed by this skill must fulfill the following mandatory requirements:
- **Mandatory Four-State Status Classification**: Every reported test case, suite, or acceptance check must be explicitly categorized as one of:
  - **`PASS`**: The test was actually executed in the current verification cycle, all behavioral assertions succeeded, and concrete execution output/evidence was observed.
  - **`FAIL`**: The test was executed and produced an assertion failure, unhandled exception, wrong HTTP status, console/network error, or incorrect state mutation.
  - **`BLOCKED`**: The test could not be executed due to an external or environmental blocker (e.g., missing database driver, unavailable Docker daemon, missing sandbox API key, broken upstream build).
  - **`NOT TESTED`**: The check exists or is relevant to the system, but was intentionally not executed in the current scope, time window, or task boundary.
- **Strict Anti-Fabrication Enforcement**: Never report `PASS` based on static code reading alone, never fold `BLOCKED` or `NOT TESTED` items into a blanket `"All tests passed"` claim, and never hide failing tests by deleting or skipping them without reporting.
- **Deterministic Reproduction Steps**: Document exact commands, environment variables, seed values, URLs, and input payloads required to reproduce any `FAIL` or `BLOCKED` check.
- **Expected vs. Actual Behavior**: Contrast the exact expected specification (status code, return value, database state, DOM snapshot) against the actual observed output.
- **Relevant Logs and Evidence**: Capture the specific stack trace frames, assertion diffs, SQL/network payloads, or browser console errors (with secrets redacted).
- **Root Cause Investigation**: Trace failures from the symptom back to the underlying defect in production code, configuration, migration state, or test setup.
- **Regression Identification**: Determine whether a failure is a new regression introduced by current changes (`git diff`) or a pre-existing failure on the base branch.
- **Remaining Uncertainty Disclosure**: Explicitly state any unverified paths, environmental differences between local tests and production, or residual risks.

## 4. Prerequisites and Context Requirements

Before producing a test report or diagnosing a failure, collect:
1. **Raw Execution Output**: Capture the exact terminal stdout/stderr, exit code, test count, and assertion messages from the test runner or Playwright MCP session.
2. **Recent Change Diff (`git status` / `git diff`)**: Identify which production files, migrations, configurations, or test files were modified in the current task.
3. **Application & Test Logs**: Locate framework log files (`storage/logs/laravel.log`, pytest output, container logs, browser console/network logs) corresponding to the failure timestamp.

## 5. Step-by-Step Workflow

Follow this numbered procedure when diagnosing failures and compiling test reports:

### Step 1: Execute and Classify Every Check Honestly
1. Run the targeted test commands or browser QA checks.
2. Assign each check its strict status (`PASS`, `FAIL`, `BLOCKED`, or `NOT TESTED`):
   - If a command was not run, it is **`NOT TESTED`** (or **`BLOCKED`** if an environment error prevented execution).
   - If a page loaded with `200 OK` but form submission or data persistence was not exercised, the submission flow is **`NOT TESTED`**, not `PASS`.

### Step 2: Capture Reproduction Details and Evidence for Every `FAIL` or `BLOCKED`
For each non-passing item, record:
1. **Exact Command / Action Sequence**: e.g., `vendor/bin/pest --filter=OrderRefundTest` or the exact Playwright MCP tool sequence.
2. **Expected Behavior**: The contract required by the acceptance criteria or test assertion.
3. **Actual Behavior & Evidence**: The exact error class, message, HTTP status, assertion diff, and file:line reference (`app/Services/RefundService.php:84`).

### Step 3: Perform Systematic Root Cause Analysis (Fault Tree Triage)
Classify the root cause of each `FAIL` into one of five engineering categories before attempting a fix:
1. **Category A: Production Logic Defect (True Bug / Regression)**:
   - The test accurately reflects the business requirement, and the production code returned the wrong calculation, status code, query result, or state transition.
   - *Action*: Fix the production code and re-run the test.
2. **Category B: Schema, Migration, or Configuration Drift**:
   - Missing database migration, unseeded lookup table, stale config cache, or missing `.env.testing` variable.
   - *Action*: Fix the migration/config setup and re-verify.
3. **Category C: Stale or Incorrect Test Expectation**:
   - Intentional requirement changes updated the API contract or UI copy, leaving an older test asserting obsolete behavior.
   - *Action*: Verify the new requirement against `SKILL-02`; only update the test assertion if the behavioral change was explicitly intended. Never weaken assertions to hide an unintended bug!
4. **Category D: Test Isolation or Flakiness Defect**:
   - The test passes when run alone (`--filter`) but fails when run in the full suite due to leaked database records, unreset mocks, or hardcoded timestamps.
   - *Action*: Apply `test-data-environment-isolation` (`SKILL-18`) fixes (transactional rollback, frozen clock, unique factory sequences).
5. **Category E: Environment / Sandbox Limitation (`BLOCKED`)**:
   - Missing PHP/Python/Node extension, stopped database daemon, or forbidden network socket in the execution sandbox.
   - *Action*: Document the exact blocker and remediation command if fixable; otherwise report clearly as `BLOCKED`.

### Step 4: Isolate Regressions vs. Pre-Existing Failures
1. Check whether the failing code path was touched by the current change set (`git diff`).
2. If the failure occurs in an untouched module, inspect whether a shared middleware, dependency update, database migration, or global helper change caused a cross-cutting regression, or whether the test was already broken prior to the task. Document this distinction with evidence.

### Step 5: Compile the Structured Verification Report
1. Present the complete breakdown of `PASS`, `FAIL`, `BLOCKED`, and `NOT TESTED` items alongside reproduction steps, root cause analysis, and remaining uncertainties.

## 6. Technology-Specific Adaptation Rules

Use the native diagnostic flags of the project's test runner to extract high-signal failure evidence:
- **PHP (Pest / PHPUnit)**:
  - Run single failing tests with `vendor/bin/pest --filter="test name" -v` or `vendor/bin/phpunit --filter="test_name" --stop-on-failure`.
  - In Laravel HTTP/Feature tests, use `$response->dump()`, `$response->dumpHeaders()`, or `$this->withoutExceptionHandling()` temporarily during diagnosis to reveal underlying `500` exception stack traces, then remove debug calls before finalizing.
- **JavaScript / TypeScript (Vitest / Jest / Playwright)**:
  - Run targeted tests with `npx vitest run path/to/file.test.ts -t "test name"` or `npx jest path/to/file.test.ts --runInBand`.
  - For Playwright, inspect trace/console/network output (`browser_console_messages`, `browser_network_request`) to see whether a UI failure originated from a backend `4xx`/`5xx` API response or a frontend state bug.
- **Python (pytest / Django)**:
  - Run `pytest path/to/test_file.py -k "test_name" -vv --tb=short -s` to inspect local variables and concise tracebacks without noise.
- **Go / Rust / Java / C#**:
  - Use `go test -v -race -run TestName ./pkg/...` (Go), `cargo test test_name -- --nocapture` (Rust), `mvn test -Dtest=ClassName#methodName` (Java), or `dotnet test --filter FullyQualifiedName~MethodName` (.NET).

## 7. Security and Safety Considerations

- **Never Suppress Failures Dishonestly**: Never add `.skip`, `@pytest.mark.skip`, `markTestSkipped()`, `@Disabled`, or comment out assertions simply to report `"0 failures"`.
- **Remove Temporary Diagnostic Instrumentation**: If `withoutExceptionHandling()`, `dd()`, `console.log()`, or verbose debug flags were added during root-cause investigation, remove them and re-run the test cleanly before completion.
- **Redact Secrets in Diagnostic Logs**: Strip any bearer tokens, session cookies, or connection passwords from stack traces and HTTP dumps included in reports.

## 8. Verification Criteria

A test report or failure diagnosis is complete and valid only when:
- [ ] Every test suite or check in scope is explicitly labeled `PASS`, `FAIL`, `BLOCKED`, or `NOT TESTED`.
- [ ] Zero unexecuted checks are marked `PASS`.
- [ ] Every `FAIL` or `BLOCKED` item includes exact reproduction steps, expected vs. actual behavior, relevant error logs, and root-cause classification.
- [ ] Any fixed failure has been re-executed to confirm it transitions to `PASS` without breaking sibling tests in the suite.
- [ ] Remaining uncertainties and untested boundaries are explicitly stated.

## 9. Failure Handling and Edge Cases

- **Intermittent / Non-Deterministic Failure ("Heisenbug")**: If a test fails once and passes on immediate re-run, do **not** dismiss it as a harmless glitch. Re-run the test repeatedly (e.g., 5-10 times or with `--repeat` / `--random-order`) and inspect time boundaries, async race conditions, and shared factory uniqueness (`SKILL-18`).
- **Cascading Failures From a Single Root Cause**: When 40 tests fail with the exact same stack trace (e.g., a missing migration column or broken auth middleware), group them under a single primary Root Cause Diagnosis rather than repeating 40 identical explanations, then re-run all 40 after fixing the root cause.

## 10. Expected Outputs and Reporting Requirements

Every test verification and failure diagnosis report must follow this structure:

```markdown
# Test Execution & Failure Diagnosis Report

## 1. Execution Summary
| Status | Count | Summary |
| :--- | :--- | :--- |
| **`PASS`** | `<N>` | Executed and verified with passing assertions. |
| **`FAIL`** | `<N>` | Executed and failed verification (see Root Cause Diagnosis below). |
| **`BLOCKED`** | `<N>` | Could not execute due to environment/dependency blocker. |
| **`NOT TESTED`** | `<N>` | Not executed in current verification scope. |

## 2. Detailed Test Matrix
| Check / Test ID | Suite / Command | Status (`PASS`/`FAIL`/`BLOCKED`/`NOT TESTED`) | Evidence / Output Summary |
| :--- | :--- | :--- | :--- |
| `OrderServiceTest::it_calculates_vat` | `vendor/bin/pest tests/Unit/OrderServiceTest.php` | `PASS` | `1 passed (4 assertions) in 0.12s` |
| `WebhookControllerTest::it_rejects_replay` | `vendor/bin/pest tests/Feature/WebhookControllerTest.php` | `FAIL` | Expected `401`, received `200` at line 58. |
| `Browser Checkout E2E` | `Playwright MCP` | `BLOCKED` | Local Postgres container not running (`Connection refused :5432`). |
| `Load Test (1000 RPS)` | `k6` | `NOT TESTED` | Out of scope for local unit/feature verification. |

## 3. Failure & Blocker Diagnosis (Required for Every `FAIL` / `BLOCKED`)
### `[FAIL] WebhookControllerTest::it_rejects_replay`
- **Reproduction Steps**: Run `vendor/bin/pest --filter=it_rejects_replay` with timestamp `now - 600s`.
- **Expected Behavior**: Reject webhook payloads older than `300s` with `401 Unauthorized`.
- **Actual Behavior**: Returned `200 OK` and processed event.
- **Relevant Logs & Evidence**: `VerifyWebhookSignature.php:42` compared `abs($now - $ts) > 300000` (milliseconds instead of seconds).
- **Root Cause & Regression Analysis**: **Category A (Production Logic Defect)** introduced in current diff (`VerifyWebhookSignature.php`).
- **Resolution & Re-Verification**: Corrected unit comparison to `> 300` seconds; re-ran suite -> `PASS`.

## 4. Remaining Uncertainty & Untested Risks
- `<Explicitly list any BLOCKED or NOT TESTED areas that must be verified in CI/staging before deployment>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Receive execution results from `backend-testing-tdd` (`SKILL-16`), `playwright-mcp-browser-qa` (`SKILL-17`), and `cross-browser-responsive-qa` (`SKILL-23`), and uphold the anti-slop evidence standards of `ai-anti-slop` (`SKILL-05`).
- **Parallel / Sibling Skills**: Route isolation/flakiness root causes to `test-data-environment-isolation` (`SKILL-18`) and legacy regression safety to `refactoring-legacy-code-safety` (`SKILL-08`).
- **Downstream Skills**: Supply verified `PASS` / `FAIL` / `BLOCKED` / `NOT TESTED` evidence directly to `deployment-readiness-release-safety` (`SKILL-33`) and `final-quality-gate-release-audit` (`SKILL-38`).

## 12. Source References

- **OWASP Testing Guide: Reporting**: https://owasp.org/www-project-web-security-testing-guide/
- **IEEE 829 / ISO/IEC/IEEE 29119 Software Testing Test Incident & Summary Report Standards**
- **AI Anti-Slop Verification Discipline**: [../ai-anti-slop/SKILL.md](../ai-anti-slop/SKILL.md)
