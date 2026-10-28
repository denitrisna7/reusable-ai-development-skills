# Mandatory Deployment Readiness & Final Quality Gate Matrix

This reference defines the shared verification contract between **Skill 33 (`deployment-readiness`)**, **Skill 19 (`test-reporting-failure-diagnosis`)**, and **Skill 38 (`final-quality-gate`)**.

---

## 1. Mandatory Policy Guardrails

1. **Assessment Only — No Unauthorized Deployment**: Evaluating deployment readiness or running the Final Quality Gate **never** authorizes executing a live production deployment unless the user's current task explicitly requests and authorizes deployment.
2. **Build Success != Deployment Readiness**: A passing compiler build or green linter check is only one input and is never sufficient on its own to declare an application ready for release.
3. **Zero Fabricated Evidence**: Every check must be classified using one of four evidence states:
   - **`PASS`**: Executed and verified with concrete evidence (command output, test log, snapshot, or verified config line).
   - **`FAIL`**: Executed or inspected and found defective or non-compliant.
   - **`BLOCKED`**: Could not be executed due to an environmental, credential, or runtime limitation outside the agent's control.
   - **`NOT TESTED`**: Not executed (must include an explicit applicability justification if excluded, or mark the audit `INCOMPLETE` if required).

---

## 2. The Four Final Release Audit Verdicts

Every execution of `deployment-readiness` and `final-quality-gate` must conclude with exactly one of these four statuses:

| Verdict | Strict Definition | Required Conditions |
| :--- | :--- | :--- |
| **`READY`** | All applicable mandatory checks have been executed and passed with recorded evidence. | Zero `FAIL` items, zero `BLOCKED` mandatory items, zero unexecuted mandatory checks, and all excluded checks have valid stack/scope justifications. |
| **`READY WITH ACCEPTED RISKS`** | All critical/mandatory checks passed, and remaining non-blocking risks are documented and explicitly accepted by the human decision-maker. | Zero critical security or data-loss `FAIL` items; every residual risk has a documented impact, mitigation plan, and explicit human sign-off. |
| **`BLOCKED`** | One or more critical requirements failed, or a mandatory check is blocked by an unresolved defect or environment failure. | Any `FAIL` on security, data integrity, broken core workflow, failing test suite, or unverified destructive migration. |
| **`INCOMPLETE`** | Required verification checks have not yet been executed or sufficient evidence is missing. | Default status whenever code was written or reviewed without running required verification checks or when mandatory evidence is absent. |

---

## 3. The 15-Point Final Quality Gate Assessment Matrix

| # | Gate Domain | Primary Contributing Skills | Key Verification Evidence Required | Exclusion Allowed Only When |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **Requirements & Acceptance Criteria** | `01-project-discovery`, `02-requirements-analysis` | Traceability matrix mapping every requested requirement and edge case to verified implementation. | Never excluded. |
| **02** | **Functional Completeness** | `05-ai-anti-slop`, `06-adaptive-engineering` | Zero dead controls (`R-26`), zero placeholder stubs disguised as finished code, all user workflows functional. | Never excluded. |
| **03** | **Code Quality & Static Analysis** | `07-code-quality-static-analysis`, `08-refactoring-legacy-safety` | Linter, formatter, type checker, and static analyzer outputs showing zero new errors. | Never excluded. |
| **04** | **Automated Tests** | `15-testing-strategy-design`, `16-backend-testing-tdd`, `18-test-data-environment-isolation`, `19-test-reporting-failure-diagnosis` | Execution output of unit, integration, and regression tests in isolated test environment. | Never excluded (if no test runner exists, document as risk/blocker). |
| **05** | **Security Review (OWASP)** | `10-application-security-owasp`, `12-privacy-data-protection`, `13-threat-modeling-risk-assessment`, `14-ai-security-prompt-injection` | Verification of authn/authz, injection defenses, CSRF/CORS, file upload safety, and PII protection. | Never excluded. |
| **06** | **Dependency & Supply Chain Security** | `09-dependency-supply-chain-security` | Lockfile integrity verified and dependency vulnerability audit output recorded. | Project has zero external dependencies. |
| **07** | **Database Integrity & Migrations** | `24-database-architecture-integrity`, `25-query-optimization-performance`, `26-import-export-data-processing` | Forward/backward migration safety, foreign keys/constraints, transaction safety, and N+1 check. | Stateless application with no database or persistent storage. |
| **08** | **API & External Integration Reliability** | `11-api-security-webhook-reliability`, `27-api-external-service-integration`, `28-ai-provider-integration` | Timeouts, retries with backoff, idempotency keys, webhook signature verification, fallback handling. | Application has no API endpoints or external service integrations. |
| **09** | **UI/UX & Accessibility (WCAG 2.2)** | `17-playwright-mcp-browser-qa`, `20-ui-ux-design-systems`, `21-accessibility-engineering`, `23-cross-browser-responsive-qa` | Contrast (`R-25`), keyboard navigation (`R-32`), empty/loading/error states (`R-27`), mobile reflow (`R-03`). | Pure headless backend API, CLI utility, or background worker with no UI. |
| **10** | **Performance Against Targets** | `22-frontend-performance`, `25-query-optimization-performance`, `29-performance-profiling-optimization`, `30-caching-background-jobs` | Baseline vs. post-change latency/memory/bundle measurements, or Core Web Vitals mecanismos (`R-40`). | Never excluded (adapt to backend/CLI vs. frontend targets). |
| **11** | **Environment Config & Secret Handling** | `32-environment-configuration-management` | Zero hardcoded secrets in VCS/client bundles; `.env.example` updated; production debug flags off. | Never excluded. |
| **12** | **Backup & Rollback Readiness** | `33-deployment-readiness`, `35-backup-recovery-disaster-preparedness` | Documented rollback procedure, non-destructive migration strategy, and backup verification prior to release. | Stateless preview/dev build with no persistent state. |
| **13** | **Logging, Monitoring & Health Checks** | `34-observability-incident-diagnosis` | Structured logging with secret redaction, correlation IDs, error tracking, and `/health` or `/ready` checks. | Single-run local CLI script. |
| **14** | **Documentation & Handoff** | `04-technical-decision-records`, `37-documentation-developer-handoff` | Updated `README`, setup/env docs, API contracts, ADRs, and operational runbooks aligned with code. | Never excluded. |
| **15** | **Post-Deployment Smoke-Test Readiness** | `31-ci-cd-release-engineering`, `33-deployment-readiness` | Defined post-deploy smoke-test checklist covering critical paths, health endpoints, and queue workers. | Library-only or non-deployed artifact (justify explicitly). |
