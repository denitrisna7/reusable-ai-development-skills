# 15-Point Final Quality Gate & Release Audit Worksheet

> Shared Contract Reference: [../../../references/deployment-readiness-quality-gate-matrix.md](../../../references/deployment-readiness-quality-gate-matrix.md)

Use this detailed audit worksheet when executing **Skill 38 (`final-quality-gate`)** in conjunction with **Skill 33 (`deployment-readiness`)**.

---

## 1. Evidence Classification Rules (Zero Fabrication Policy)

Every single check item across all 15 domains must be assigned one of the following states based on empirical evidence:

- **`EXECUTED - PASS`**: Check was actively run or directly verified in code/config during this audit, and passed all criteria. Record the exact command output, test summary, or file/line reference.
- **`EXECUTED - FAIL`**: Check was actively run or inspected and failed one or more criteria. Automatically forces the overall release verdict to **`BLOCKED`** if the item is critical/mandatory.
- **`BLOCKED (Environmental)`**: Check is applicable and required, but could not be executed due to missing sandbox binaries, unprovisioned external services, or missing credentials. Forces the overall verdict to **`BLOCKED`** or **`INCOMPLETE`** unless explicitly waived by human sign-off under `READY WITH ACCEPTED RISKS`.
- **`NOT EXECUTED`**: Applicable check that has not yet been run. Forces the overall verdict to **`INCOMPLETE`**.
- **`EXCLUDED (Justified N/A)`**: Check does not apply to the project's architecture, stack, or scope (for example, UI/UX Accessibility on a headless CLI tool, or Database Migrations on a stateless calculator). **Requires an explicit written justification.**

---

## 2. Detailed 15-Domain Audit Checklist

### Gate 01: Requirements & Acceptance Criteria (`SKILL-01`, `SKILL-02`)
- [ ] Every explicit functional and non-functional requirement from the user prompt or specification is mapped in a traceability table.
- [ ] Implicit domain edge cases (empty inputs, boundary values, permission denials, concurrent submissions) are handled.
- [ ] Zero requested features were silently dropped or simplified without user approval.

### Gate 02: Functional Completeness & Anti-Slop (`SKILL-05`, `SKILL-06`)
- [ ] Zero `TODO`, `FIXME`, `"Coming soon"`, or mock placeholder stubs disguised as completed production logic.
- [ ] Every interactive button, link, form, filter, and menu item is wired to working logic (`R-26` zero dead controls).
- [ ] Primary happy paths and negative error-handling paths work end to end.

### Gate 03: Code Quality & Static Analysis (`SKILL-07`, `SKILL-08`)
- [ ] Code formatter and linter checks pass with zero errors.
- [ ] Static type checker / analyzer (`tsc --noEmit`, PHPStan, Mypy/Pyright, `cargo clippy`, `golangci-lint`) passes at the project's strictness level.
- [ ] Dead code, commented-out blocks, and leftover debugging statements (`console.log`, `dd()`, `var_dump()`, `print()`) are removed.

### Gate 04: Automated Tests (`SKILL-15`, `SKILL-16`, `SKILL-18`, `SKILL-19`)
- [ ] Unit and integration tests exist for all new/modified business logic and bug fixes.
- [ ] Automated test suite was executed in an isolated test environment (never touching development/production databases) and passed 100%.
- [ ] Negative assertions verify validation failures, unauthorized access (`401`/`403`), and not-found (`404`) paths.

### Gate 05: Security Review (OWASP) (`SKILL-10`, `SKILL-12`, `SKILL-13`, `SKILL-14`)
- [ ] Authentication and route/object-level authorization (IDOR/BOLA prevention) are enforced server-side on every protected endpoint.
- [ ] All SQL/NoSQL queries use parameterized bindings; all HTML output is context-escaped (XSS prevention); shell commands avoid raw string interpolation.
- [ ] CSRF protection, strict CORS policies, rate limiting on auth/public mutations, and safe file upload validation are verified.
- [ ] If AI/LLM integrations exist, untrusted prompts are isolated and LLM output is validated before triggering tools or rendering HTML.

### Gate 06: Dependency & Supply Chain Security (`SKILL-09`)
- [ ] Dependency lockfile is committed and in sync with the package manifest.
- [ ] Dependency vulnerability audit (`npm audit`, `composer audit`, `pip-audit`, `cargo audit`, `govulncheck`) was executed or inspected with zero unresolved critical/high vulnerabilities on reachable code paths.
- [ ] No hallucinated, deprecated, or typosquatted packages were introduced.

### Gate 07: Database Integrity & Migrations (`SKILL-24`, `SKILL-25`, `SKILL-26`)
- [ ] Schema changes include foreign key constraints, appropriate `ON DELETE` rules, and non-null/check constraints where appropriate.
- [ ] Multi-step writes are wrapped in atomic database transactions (`DB::transaction`, `BEGIN...COMMIT`).
- [ ] Migrations are backward-compatible (expand/contract safe) and include tested `up`/`down` paths.
- [ ] Queries on list/detail endpoints are free of N+1 query loops and missing composite indexes.

### Gate 08: API & External Integration Reliability (`SKILL-11`, `SKILL-27`, `SKILL-28`)
- [ ] Outbound HTTP/SDK calls enforce explicit connection and read timeouts (never infinite default waits).
- [ ] Transient upstream errors (`429`, `502`, `503`, `504`) use bounded retries with exponential backoff and jitter.
- [ ] Incoming webhooks verify cryptographic HMAC signatures with constant-time comparison and enforce replay protection / idempotency.

### Gate 09: UI/UX & Accessibility (`SKILL-17`, `SKILL-20`, `SKILL-21`, `SKILL-23`)
- [ ] Every data-driven view implements explicit **Loading**, **Empty**, **Error**, and **Populated** states (`R-27`).
- [ ] WCAG 2.2 AA contrast ratios (`4.5:1` normal text, `3:1` large text/UI components), visible `:focus-visible` rings, semantic landmarks, and full keyboard navigation (`Tab`, `Enter`, `Escape`) are verified.
- [ ] Responsive layout works cleanly from `320px` mobile viewports to desktop (`1440px+`) without horizontal overflow (`R-03`).

### Gate 10: Performance Against Relevant Targets (`SKILL-22`, `SKILL-25`, `SKILL-29`, `SKILL-30`)
- [ ] Baseline vs. post-change measurements (or verified structural complexity fixes when runtime is unavailable) are recorded without fabrication.
- [ ] Web interfaces enforce Core Web Vitals mechanisms (`LCP <= 2.5s` hero `fetchpriority="high"`, `INP <= 200ms` non-blocking handlers, `CLS <= 0.1` explicit media dimensions `R-40`).
- [ ] Heavy tasks (emails, exports, webhooks) are offloaded to idempotent background jobs with safe payload serialization.

### Gate 11: Environment Configuration & Secret Handling (`SKILL-32`)
- [ ] Zero hardcoded secrets, API keys, or private tokens exist in source code, Git history, or client-side bundles (`NEXT_PUBLIC_`, `VITE_`).
- [ ] `.gitignore` excludes `.env` files, and `.env.example` documents all required variables with safe placeholder values.
- [ ] Startup configuration validation fails fast on missing keys, and production defaults enforce `DEBUG=false`.

### Gate 12: Backup & Rollback Readiness (`SKILL-33`, `SKILL-35`)
- [ ] Pre-deployment database/state backup procedure is verified and restorable.
- [ ] Step-by-step application artifact and database migration rollback runbook is documented and verified.

### Gate 13: Logging, Monitoring & Health Checks (`SKILL-34`)
- [ ] Structured logging includes correlation IDs (`X-Request-ID`) and automatically redacts passwords, tokens, and PII.
- [ ] Liveness (`/health`) and readiness (`/ready`) endpoints exist and accurately verify downstream dependencies.

### Gate 14: Documentation & Developer Handoff (`SKILL-04`, `SKILL-37`)
- [ ] `README.md` and operational docs match the actual codebase commands, directory tree, environment variables, and testing procedures.

### Gate 15: Post-Deployment Smoke-Test Readiness (`SKILL-31`, `SKILL-33`)
- [ ] A concrete post-deployment smoke-test checklist is defined covering `/health` & `/ready` status, authentication, critical user workflows, and background queue heartbeats.

---

## 3. Verdict Decision Tree

1. Are any mandatory applicable checks in state **`EXECUTED - FAIL`**? -> Verdict MUST be **`BLOCKED`**.
2. Are any mandatory applicable checks in state **`BLOCKED (Environmental)`** without explicit human risk acceptance? -> Verdict MUST be **`BLOCKED`** or **`INCOMPLETE`**.
3. Are any mandatory applicable checks in state **`NOT EXECUTED`**? -> Verdict MUST be **`INCOMPLETE`**.
4. Did all mandatory checks pass except for documented non-critical residual risks that have an explicit mitigation plan and human sign-off? -> Verdict is **`READY WITH ACCEPTED RISKS`**.
5. Did all applicable mandatory checks pass with recorded empirical evidence and valid justifications for any excluded N/A domains? -> Verdict is **`READY`**.
