# Complete Skill Catalog (`SKILL_CATALOG.md`)

This catalog indexes all **38 required software engineering lifecycle skills** in the **Reusable AI Development Skills Library**, organized across 8 lifecycle categories (`A` through `H`).

Every skill resides at `skills/<skill-name>/SKILL.md`, adheres strictly to the Agent Skills (`agentskills.io`) and Google Antigravity specifications, and remains technology-agnostic at the library level.

---

## Quick Index Table (Skills 01–38)

| ID | Skill Name (`skills/<name>/`) | Title | Category | Primary Supporting References |
| :--- | :--- | :--- | :--- | :--- |
| **01** | `project-discovery` | Project Discovery & Technology Detection | A. Core Discovery & Planning | `references/technology-stack-detection-matrix.md` |
| **02** | `requirements-analysis` | Requirements Analysis & Acceptance Criteria | A. Core Discovery & Planning | `references/deployment-readiness-quality-gate-matrix.md` |
| **03** | `adaptive-architecture` | Adaptive Architecture & Technical Planning | A. Core Discovery & Planning | `references/technology-stack-detection-matrix.md` |
| **04** | `technical-decision-records` | Documentation & Technical Decision Records | A. Core Discovery & Planning | `references/technology-stack-detection-matrix.md` |
| **05** | `ai-anti-slop` | AI Anti-Slop & Engineering Discipline | B. Core Development Quality | `skills/ai-anti-slop/references/anti-slop-rules.md`, `references/anti-slop-engineering-reference.md` |
| **06** | `adaptive-engineering` | Language and Framework Adaptive Engineering | B. Core Development Quality | `references/technology-stack-detection-matrix.md` |
| **07** | `code-quality-static-analysis` | Code Quality & Static Analysis | B. Core Development Quality | `references/technology-stack-detection-matrix.md` |
| **08** | `refactoring-legacy-safety` | Refactoring & Legacy Code Safety | B. Core Development Quality | `references/anti-slop-engineering-reference.md` |
| **09** | `dependency-supply-chain-security` | Dependency & Supply Chain Security | B. Core Development Quality | `references/owasp-asvs-top10-reference.md` |
| **10** | `application-security-owasp` | Application Security & OWASP | C. Security Engineering | `skills/application-security-owasp/references/owasp-asvs-checklist.md`, `references/owasp-asvs-top10-reference.md` |
| **11** | `api-security-webhook-reliability` | API Security & Webhook Reliability | C. Security Engineering | `references/owasp-asvs-top10-reference.md` |
| **12** | `privacy-data-protection` | Privacy & Data Protection | C. Security Engineering | `references/owasp-asvs-top10-reference.md` |
| **13** | `threat-modeling-risk-assessment` | Threat Modeling & Risk Assessment | C. Security Engineering | `references/owasp-asvs-top10-reference.md` |
| **14** | `ai-security-prompt-injection` | AI Security & Prompt Injection Defense | C. Security Engineering | `references/owasp-asvs-top10-reference.md` |
| **15** | `testing-strategy-design` | Testing Strategy & Test Design | D. Testing & QA | `references/technology-stack-detection-matrix.md` |
| **16** | `backend-testing-tdd` | Backend Testing & TDD | D. Testing & QA | `references/technology-stack-detection-matrix.md` |
| **17** | `playwright-mcp-browser-qa` | Playwright MCP Browser QA | D. Testing & QA | `skills/playwright-mcp-browser-qa/references/playwright-mcp-tools.md`, `references/playwright-mcp-reference.md` |
| **18** | `test-data-environment-isolation` | Test Data & Environment Isolation | D. Testing & QA | `references/technology-stack-detection-matrix.md` |
| **19** | `test-reporting-failure-diagnosis` | Test Reporting & Failure Diagnosis | D. Testing & QA | `references/deployment-readiness-quality-gate-matrix.md` |
| **20** | `ui-ux-design-systems` | UI/UX Engineering & Design Systems | E. Frontend & UX | `skills/ui-ux-design-systems/references/shadcn-ui-patterns.md`, `references/shadcn-ui-design-system-reference.md` |
| **21** | `accessibility-engineering` | Accessibility Engineering | E. Frontend & UX | `skills/accessibility-engineering/references/wcag22-checklist.md`, `skills/accessibility-engineering/scripts/contrast-check.py` |
| **22** | `frontend-performance` | Frontend Performance | E. Frontend & UX | `references/core-web-vitals-performance-reference.md` |
| **23** | `cross-browser-responsive-qa` | Cross-Browser and Responsive QA | E. Frontend & UX | `references/playwright-mcp-reference.md`, `references/anti-slop-engineering-reference.md` |
| **24** | `database-architecture-integrity` | Database Architecture & Integrity | F. Data & Integrations | `references/technology-stack-detection-matrix.md` |
| **25** | `query-optimization-performance` | Query Optimization & Performance | F. Data & Integrations | `references/core-web-vitals-performance-reference.md` |
| **26** | `import-export-data-processing` | Import/Export & Data Processing | F. Data & Integrations | `references/owasp-asvs-top10-reference.md` |
| **27** | `api-external-service-integration` | API and External Service Integration | F. Data & Integrations | `references/owasp-asvs-top10-reference.md` |
| **28** | `ai-provider-integration` | AI Provider Integration | F. Data & Integrations | `references/owasp-asvs-top10-reference.md` |
| **29** | `performance-profiling-optimization` | Performance Profiling & Optimization | G. Performance, Ops & Deployment | `skills/performance-profiling-optimization/references/core-web-vitals.md`, `references/core-web-vitals-performance-reference.md` |
| **30** | `caching-background-jobs` | Caching & Background Jobs | G. Performance, Ops & Deployment | `references/core-web-vitals-performance-reference.md` |
| **31** | `ci-cd-release-engineering` | CI/CD & Release Engineering | G. Performance, Ops & Deployment | `skills/ci-cd-release-engineering/references/ci-cd-security-hardening.md` |
| **32** | `environment-configuration-management` | Environment & Configuration Management | G. Performance, Ops & Deployment | `references/owasp-asvs-top10-reference.md` |
| **33** | `deployment-readiness` | Deployment Readiness & Release Safety | G. Performance, Ops & Deployment | `references/deployment-readiness-quality-gate-matrix.md` |
| **34** | `observability-incident-diagnosis` | Observability & Incident Diagnosis | G. Performance, Ops & Deployment | `references/owasp-asvs-top10-reference.md` |
| **35** | `backup-recovery-disaster-preparedness` | Backup, Recovery & Disaster Preparedness | G. Performance, Ops & Deployment | `references/deployment-readiness-quality-gate-matrix.md` |
| **36** | `seo-web-discoverability` | SEO & Web Discoverability | G. Performance, Ops & Deployment | `references/core-web-vitals-performance-reference.md` |
| **37** | `documentation-developer-handoff` | Documentation Quality & Developer Handoff | H. Final Quality & Maintenance | `references/deployment-readiness-quality-gate-matrix.md` |
| **38** | `final-quality-gate` | Final Quality Gate & Release Audit | H. Final Quality & Maintenance | `skills/final-quality-gate/references/gate-checklist.md`, `references/deployment-readiness-quality-gate-matrix.md` |

---

## Detailed Catalog by Category

### Category A — Core Discovery and Planning

#### Skill 01 — `project-discovery` (Project Discovery & Technology Detection)
- **Path**: `skills/project-discovery/SKILL.md`
- **Purpose**: Inspect and inventory an unfamiliar or evolving repository before making technical recommendations or modifying code.
- **Covers**: Repository structure, project documentation, programming languages, frameworks, runtime versions, dependency managers, entry points, routing, APIs, external integrations, database technology, data access patterns, coding conventions, test runners, linters/static analyzers, build/run/deploy workflows, security-sensitive components, verified facts vs. assumptions, and material unknowns.
- **Activate When**: Starting work in a repository for the first time, onboarding to a codebase, planning a cross-cutting feature, or encountering unfamiliar build/test tooling.
- **Do Not Use When**: The stack and target module are already verified in the current session and only a localized implementation step remains (use `adaptive-engineering`).

#### Skill 02 — `requirements-analysis` (Requirements Analysis & Acceptance Criteria)
- **Path**: `skills/requirements-analysis/SKILL.md`
- **Purpose**: Translate ambiguous or high-level feature requests and bug reports into explicit, testable functional and non-functional requirements and acceptance criteria.
- **Covers**: Functional and non-functional requirements, user workflows, Given/When/Then acceptance criteria, edge cases and failure states, security/privacy constraints, performance expectations, integration constraints, and verifiable completion criteria.
- **Activate When**: Receiving a new feature request, user story, complex bug report, or architectural change request whose acceptance criteria or edge cases are not yet explicitly specified.
- **Do Not Use When**: Executing a trivial, unambiguous fix (e.g., fixing a typo or single-line lint error) where requirements are already crystal clear.

#### Skill 03 — `adaptive-architecture` (Adaptive Architecture & Technical Planning)
- **Path**: `skills/adaptive-architecture/SKILL.md`
- **Purpose**: Evaluate existing system architecture and design incremental, maintainable technical plans that respect project boundaries without forcing unnecessary rewrites.
- **Covers**: Existing architecture evaluation, design pattern selection, architectural trade-offs, dependency boundaries, maintainability and scalability, backward-compatibility constraints, incremental implementation plans, minimizing unnecessary rewrites, and documenting architectural decisions.
- **Activate When**: Designing new modules, introducing cross-service boundaries, restructuring domain layers, or planning multi-step implementations.
- **Do Not Use When**: Performing pure discovery without planning (`project-discovery`) or recording a standalone formal ADR document (`technical-decision-records`).

#### Skill 04 — `technical-decision-records` (Documentation & Technical Decision Records)
- **Path**: `skills/technical-decision-records/SKILL.md`
- **Purpose**: Author and maintain Architecture Decision Records (ADRs), API contracts, setup/environment documentation, and operational specifications aligned with actual code.
- **Covers**: Architecture documentation, setup instructions, environment configuration docs, dependency rationales, API contracts (OpenAPI/GraphQL/schema docs), ADRs, operational documentation, and drift verification against code.
- **Activate When**: Recording a significant architectural or dependency choice, defining or updating API contracts, or documenting module boundaries during development.
- **Do Not Use When**: Performing end-of-project developer handoff and runbook consolidation across the entire system (use `documentation-developer-handoff`).

---

### Category B — Core Development Quality

#### Skill 05 — `ai-anti-slop` (AI Anti-Slop & Engineering Discipline)
- **Path**: `skills/ai-anti-slop/SKILL.md` (with `skills/ai-anti-slop/references/anti-slop-rules.md`)
- **Purpose**: Eliminate generic AI-generated code, UI, copywriting, and comment slop while enforcing intentional craftsmanship, functional completeness, and evidence-backed completion claims.
- **Covers**: Avoiding unnecessary complexity and duplicated code, avoiding generic/template UI (`R-01`..`R-40`), preserving project conventions, avoiding premature abstractions and unnecessary dependencies, banning placeholder stubs disguised as finished work, requiring evidence for completion claims (`C-1`..`C-5`), Liveliness Toolkit dials (`ENERGY`/`RHYTHM`/`MOTION`), Code Comment Hygiene (`antislop-code`), Copywriting hygiene (`antislop-copywriting`), and the 4-block Delivery Gate.
- **Activate When**: Writing or reviewing any code, UI component, landing page, dashboard, copy, or code comment, or auditing existing AI-generated output.
- **Do Not Use When**: Running purely mechanical read-only repository file discovery (`project-discovery`).

#### Skill 06 — `adaptive-engineering` (Language and Framework Adaptive Engineering)
- **Path**: `skills/adaptive-engineering/SKILL.md`
- **Purpose**: Implement features and fixes idiomatic to the repository's actual programming language, framework version, and established coding patterns.
- **Covers**: Language-specific conventions, framework-specific idioms (Laravel vs. CodeIgniter vs. Next.js vs. Django vs. FastAPI vs. Go vs. Spring Boot vs. Flutter), version compatibility, existing project patterns, appropriate tool selection, consulting official docs, and handling unknown/mixed stacks.
- **Activate When**: Writing, modifying, or reviewing application source code in any language or framework.
- **Do Not Use When**: Designing high-level system architecture before coding (`adaptive-architecture`) or running standalone static analysis gates (`code-quality-static-analysis`).

#### Skill 07 — `code-quality-static-analysis` (Code Quality & Static Analysis)
- **Path**: `skills/code-quality-static-analysis/SKILL.md`
- **Purpose**: Verify and improve code quality using the project's applicable linters, formatters, type checkers, and static analysis tools alongside structural maintainability checks.
- **Covers**: Linting, formatting, type checking, static analysis (e.g., ESLint/tsc/Biome for JS/TS, PHPStan/Pint for applicable PHP projects, Ruff/mypy for Python, `golangci-lint` for Go, `cargo clippy` for Rust), error handling, code duplication, cyclomatic/cognitive complexity, naming consistency, and validation of modified files.
- **Activate When**: After modifying code, during code review, or when diagnosing static analysis, type, or lint failures.
- **Do Not Use When**: Auditing third-party CVEs and lockfiles (use `dependency-supply-chain-security`).

#### Skill 08 — `refactoring-legacy-safety` (Refactoring & Legacy Code Safety)
- **Path**: `skills/refactoring-legacy-safety/SKILL.md`
- **Purpose**: Safely restructure existing or legacy code while preserving observable behavior, backward compatibility, and regression safety.
- **Covers**: Characterization testing and behavior verification before modification, backward compatibility preservation, incremental refactoring steps (Strangler Fig, Branch by Abstraction, Parallel Change), careful dead-code identification (checking dynamic dispatch/reflection/external callers), avoiding unnecessary rewrites, change-scope minimization, and migration risk evaluation.
- **Activate When**: Refactoring legacy modules, extracting services/helpers, modernizing syntax/framework APIs, or removing suspected dead code.
- **Do Not Use When**: Building net-new isolated greenfield features (`adaptive-engineering`).

#### Skill 09 — `dependency-supply-chain-security` (Dependency & Supply Chain Security)
- **Path**: `skills/dependency-supply-chain-security/SKILL.md`
- **Purpose**: Audit, select, update, and lock third-party packages safely while defending against supply-chain attacks, typosquatting, and vulnerable transitive dependencies.
- **Covers**: Dependency vulnerability auditing (`npm audit`, `composer audit`, `pip-audit`, `govulncheck`, `cargo audit`), direct vs. transitive dependency analysis, lockfile integrity verification, package source and maintainer verification, risk-based upgrades, breaking-change evaluation, removing redundant packages, and guarding against malicious post-install scripts.
- **Activate When**: Adding, upgrading, or removing dependencies, reviewing lockfile changes, or resolving CVE security advisories.
- **Do Not Use When**: Reviewing first-party application business logic vulnerabilities (`application-security-owasp`).

---

### Category C — Security Engineering

#### Skill 10 — `application-security-owasp` (Application Security & OWASP)
- **Path**: `skills/application-security-owasp/SKILL.md` (with `skills/application-security-owasp/references/owasp-asvs-checklist.md`)
- **Purpose**: Design, implement, and audit application security controls aligned with OWASP ASVS (L1/L2/L3) and OWASP Top 10.
- **Covers**: Authentication and authorization, least privilege, SQL/NoSQL/command injection defense, XSS and context-aware output encoding, CSRF protection, IDOR/BOLA object-level authorization, session security, input validation, file upload/download security, rate limiting, secret management, safe error handling, security audit logging, and security verification testing.
- **Activate When**: Implementing or reviewing auth, permissions, user input handling, database queries, file uploads, session handling, or conducting a security audit.
- **Do Not Use When**: Auditing only webhook retry/idempotency mechanics (`api-security-webhook-reliability`) or LLM prompt injection (`ai-security-prompt-injection`).

#### Skill 11 — `api-security-webhook-reliability` (API Security & Webhook Reliability)
- **Path**: `skills/api-security-webhook-reliability/SKILL.md`
- **Purpose**: Secure REST/GraphQL/RPC API endpoints and engineer resilient, idempotent, cryptographically verified webhook consumers and producers.
- **Covers**: API authentication/authorization (OAuth2/JWT/API keys/scopes), strict schema request validation, webhook HMAC signature and timestamp replay verification, timeouts, retries with backoff, idempotency keys, duplicate/out-of-order event handling, rate limiting (`429`), consistent error envelopes, external service failure isolation, safe logging, and integration testing.
- **Activate When**: Building or auditing API endpoints, payment/third-party webhooks (Stripe, GitHub, Slack, Midtrans, Xendit, etc.), or event-driven HTTP callbacks.
- **Do Not Use When**: Consuming general outbound third-party SDKs unrelated to API security or webhooks (also consult `api-external-service-integration`).

#### Skill 12 — `privacy-data-protection` (Privacy & Data Protection)
- **Path**: `skills/privacy-data-protection/SKILL.md`
- **Purpose**: Protect personal and sensitive data (PII, PHI, PCI, financial/auth records) across the entire data lifecycle and prevent unauthorized exposure in logs, exports, or AI prompts.
- **Covers**: Data minimization, role/tenant access restrictions, data retention schedules, field-level encryption and masking, structured log redaction, right-to-erasure / safe deletion and anonymization, privacy-aware third-party integrations, preventing PII leakage into external LLM/AI requests, and regulatory alignment (GDPR, CCPA, HIPAA, UU PDP).
- **Activate When**: Designing schemas or workflows handling user profiles, health/financial data, audit logs, analytics tracking, data exports, or AI data pipelines.
- **Do Not Use When**: Designing low-level database indexing without sensitive data implications (`query-optimization-performance`).

#### Skill 13 — `threat-modeling-risk-assessment` (Threat Modeling & Risk Assessment)
- **Path**: `skills/threat-modeling-risk-assessment/SKILL.md`
- **Purpose**: Identify assets, trust boundaries, attack surfaces, and structural threats early, and prioritize mitigations based on likelihood and business impact.
- **Covers**: Asset inventory, trust boundaries and data flow diagrams, attack surface mapping, STRIDE threat identification and abuse cases, risk scoring and prioritization, mitigation design, residual risk documentation, and security requirements for high-risk architectural changes.
- **Activate When**: Planning new architectures, payment/auth flows, multi-tenant boundaries, external integrations, or high-risk system changes.
- **Do Not Use When**: Fixing a single localized syntax or formatting issue (`code-quality-static-analysis`).

#### Skill 14 — `ai-security-prompt-injection` (AI Security & Prompt Injection Defense)
- **Path**: `skills/ai-security-prompt-injection/SKILL.md`
- **Purpose**: Secure LLM/AI-powered application features and agentic workflows against direct and indirect prompt injection, unauthorized tool execution, data exfiltration, and unsafe output rendering.
- **Covers**: Untrusted input isolation, direct/indirect prompt injection defense, strict tool-call allowlists and parameter validation, permission boundaries and sandboxing, output validation and XSS/SQL/command sanitization before execution or rendering, secret exposure prevention, RAG/retrieval content boundaries, human-in-the-loop approval for high-impact actions, and adversarial AI workflow testing.
- **Activate When**: Building or auditing LLM chat features, RAG pipelines, AI tool-calling agents, prompt templates, or automated AI workflows.
- **Do Not Use When**: Managing basic AI SDK retries, token budgets, and provider fallbacks without security threat considerations (combine with `ai-provider-integration`).

---

### Category D — Testing and Quality Assurance

#### Skill 15 — `testing-strategy-design` (Testing Strategy & Test Design)
- **Path**: `skills/testing-strategy-design/SKILL.md`
- **Purpose**: Define a risk-based, high-signal testing strategy tailored to the project's architecture and change scope—prioritizing behavioral confidence over raw test count.
- **Covers**: Unit, integration, feature, API, end-to-end, regression, acceptance, performance, and security test selection; risk-based test prioritization; test pyramid/trophy balance; and understanding coverage metric limitations.
- **Activate When**: Planning how to verify a feature, bug fix, or refactoring effort, or establishing a testing strategy for a repository.
- **Do Not Use When**: Executing specific browser clicks in Playwright MCP (`playwright-mcp-browser-qa`) or formatting a final test execution report (`test-reporting-failure-diagnosis`).

#### Skill 16 — `backend-testing-tdd` (Backend Testing & TDD)
- **Path**: `skills/backend-testing-tdd/SKILL.md`
- **Purpose**: Write and execute deterministic unit, integration, and API tests for backend services using the repository's native test framework and Red-Green-Refactor TDD principles.
- **Covers**: Domain business logic, request validation (valid/invalid/boundary payloads), authentication and authorization matrix tests, database persistence and constraints, transaction commit/rollback behavior, error handling, mocked external integrations, test isolation, and regression protection.
- **Activate When**: Implementing backend features, fixing server-side bugs, adding API endpoints, or writing unit/integration tests.
- **Do Not Use When**: Running interactive browser UI tests (`playwright-mcp-browser-qa`).

#### Skill 17 — `playwright-mcp-browser-qa` (Playwright MCP Browser QA)
- **Path**: `skills/playwright-mcp-browser-qa/SKILL.md` (with `skills/playwright-mcp-browser-qa/references/playwright-mcp-tools.md`)
- **Purpose**: Perform evidence-based functional, negative, and regression browser QA using Playwright MCP accessibility snapshots, semantic locators, console inspection, and network verification.
- **Covers**: Accessibility tree inspection (`browser_snapshot`, `browser_find`), deterministic `ref=...` element targeting, functional flow verification (`browser_click`, `browser_fill_form`, `browser_type`, `browser_select_option`, `browser_press_key`), form validation, navigation, auth/session flows, network request/response inspection (`browser_network_requests`, `browser_network_request`), console error checks (`browser_console_messages`), negative testing, and selective screenshot capture (`browser_take_screenshot`).
- **Activate When**: Verifying web UI features, forms, interactive flows, client-server integration, or reproducing frontend bugs in a live browser.
- **Do Not Use When**: Testing pure backend CLI/library code with no web UI (`backend-testing-tdd`).

#### Skill 18 — `test-data-environment-isolation` (Test Data & Environment Isolation)
- **Path**: `skills/test-data-environment-isolation/SKILL.md`
- **Purpose**: Guarantee that automated and manual tests run against isolated environments and deterministic test data without ever mutating production databases or triggering real external side effects.
- **Covers**: Dedicated test environment verification, safe test database guards (`:memory:`, test containers, dedicated `*_test` schemas), factories/fixtures/builders, deterministic seeds and frozen clocks, external HTTP/payment/email/SMS mocks, production data protection guardrails, and post-test cleanup/transaction rollback.
- **Activate When**: Setting up test suites, writing database or integration tests, seeding test environments, or testing workflows that integrate with payment gateways or notification providers.
- **Do Not Use When**: Designing production database schemas (`database-architecture-integrity`).

#### Skill 19 — `test-reporting-failure-diagnosis` (Test Reporting & Failure Diagnosis)
- **Path**: `skills/test-reporting-failure-diagnosis/SKILL.md`
- **Purpose**: Produce truthful, evidence-backed test reports that strictly classify every check as `PASS`, `FAIL`, `BLOCKED`, or `NOT TESTED`, and perform structured root-cause diagnosis on failures.
- **Covers**: Mandatory `PASS` / `FAIL` / `BLOCKED` / `NOT TESTED` classification, deterministic reproduction steps, expected vs. actual behavior, log/snapshot/network evidence attachment, root-cause analysis, regression identification, and explicit declaration of remaining uncertainty.
- **Activate When**: Reporting test execution results, diagnosing failing test suites or QA defects, or preparing verification evidence for `final-quality-gate`.
- **Do Not Use When**: Designing the initial test plan before any tests exist (`testing-strategy-design`).

---

### Category E — Frontend and User Experience

#### Skill 20 — `ui-ux-design-systems` (UI/UX Engineering & Design Systems)
- **Path**: `skills/ui-ux-design-systems/SKILL.md` (with `skills/ui-ux-design-systems/references/shadcn-ui-patterns.md`)
- **Purpose**: Build cohesive, accessible, content-driven user interfaces using the project's established design system (including `shadcn/ui` when compatible with the project stack).
- **Covers**: Reusable component architecture, design tokens (color, spacing, typography, radius, elevation), layout consistency, forms and validation UX, data tables, dialogs and navigation, responsive layouts, complete view states (loading, empty, error, success per `R-27`), existing design system preservation, and `shadcn/ui` open-code integration where compatible.
- **Activate When**: Building or updating UI components, pages, forms, tables, modals, dashboards, or theme tokens.
- **Do Not Use When**: Auditing backend database queries (`query-optimization-performance`) or forcing `shadcn/ui` into non-compatible stacks.

#### Skill 21 — `accessibility-engineering` (Accessibility Engineering)
- **Path**: `skills/accessibility-engineering/SKILL.md` (with `skills/accessibility-engineering/references/wcag22-checklist.md` and `skills/accessibility-engineering/scripts/contrast-check.py`)
- **Purpose**: Engineer and verify web and application interfaces to meet W3C WCAG 2.2 Level AA standards across keyboard, screen reader, visual contrast, and motor affordances.
- **Covers**: Semantic HTML (`<button>`, `<a href>`, landmarks, headings), full keyboard operability (`Tab`, `Enter`, `Space`, `Escape`), focus management and visible `:focus-visible` indicators (`WCAG 2.4.7`, `2.4.11`), accessible forms and error announcements (`<label for>`, `aria-invalid`, `aria-describedby`), deterministic color contrast verification (`4.5:1` normal text, `3.0:1` large text and UI components via `contrast-check.py`), screen reader live regions (`aria-live`), accessible dialogs, and `prefers-reduced-motion`.
- **Activate When**: Creating or modifying any UI component, color palette, form, modal, navigation menu, or auditing accessibility compliance.
- **Do Not Use When**: Working on headless backend services with zero user interface.

#### Skill 22 — `frontend-performance` (Frontend Performance)
- **Path**: `skills/frontend-performance/SKILL.md`
- **Purpose**: Optimize client-side asset delivery, bundle size, rendering efficiency, and Core Web Vitals mechanisms (`LCP`, `INP`, `CLS`).
- **Covers**: Image/media optimization (WebP/AVIF, `srcset`, explicit `width`/`height` or `aspect-ratio` per `R-40`), hero image prioritization (`fetchpriority="high"`, never `loading="lazy"`), JS/CSS bundle splitting and tree-shaking, React/Vue/DOM rendering optimization, network waterfall elimination, HTTP caching headers, lazy loading below-the-fold assets, non-blocking third-party scripts, and measurable before/after profiling.
- **Activate When**: Building public pages or heavy client views, optimizing slow page loads or bundle sizes, or fixing layout shifts and slow interactions.
- **Do Not Use When**: Optimizing SQL query plans or backend worker queues (`query-optimization-performance`, `caching-background-jobs`).

#### Skill 23 — `cross-browser-responsive-qa` (Cross-Browser and Responsive QA)
- **Path**: `skills/cross-browser-responsive-qa/SKILL.md`
- **Purpose**: Verify that web layouts reflow cleanly across mobile, tablet, and desktop viewports and function consistently across target browser engines (Chromium, Firefox, WebKit/Safari) and input modalities.
- **Covers**: Multi-breakpoint layout reflow (`320px` to `1440px+`, including `600px–1024px` tablet/small laptop band), horizontal overflow detection, `dvh` vs `100vh` mobile viewport handling, `44x44px` touch target sizing and spacing (`R-03`), tap equivalents for hover interactions, sticky/bottom nav clearance, CSS/JS engine compatibility, and target-browser matrix verification.
- **Activate When**: Building or modifying CSS layouts, navigation bars, tables, grids, or verifying responsive/cross-browser behavior.
- **Do Not Use When**: Testing backend-only APIs (`backend-testing-tdd`).

---

### Category F — Data and Integrations

#### Skill 24 — `database-architecture-integrity` (Database Architecture & Integrity)
- **Path**: `skills/database-architecture-integrity/SKILL.md`
- **Purpose**: Design resilient database schemas, relational constraints, transactions, concurrency controls, and backward-compatible migrations that protect data integrity.
- **Covers**: Schema design and data types, relational modeling (1:1, 1:N, M:N), database constraints (`PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`, `CHECK`), indexing fundamentals, deterministic migrations, ACID transaction boundaries, optimistic/pessimistic concurrency control (`SELECT ... FOR UPDATE`), expand-and-contract zero-downtime schema changes, and migration rollback safety.
- **Activate When**: Creating or altering database tables, columns, constraints, migrations, or transactional domain logic.
- **Do Not Use When**: Tuning slow read queries without schema changes (`query-optimization-performance`).

#### Skill 25 — `query-optimization-performance` (Query Optimization & Performance)
- **Path**: `skills/query-optimization-performance/SKILL.md`
- **Purpose**: Diagnose and eliminate slow database queries, N+1 query loops, inefficient pagination, and connection pool bottlenecks using execution plans and measurable benchmarks.
- **Covers**: Query plan analysis (`EXPLAIN ANALYZE`), composite and covering index design, N+1 detection and eager-loading remediation, keyset/cursor pagination vs. `OFFSET`, query result caching, connection pooling configuration, lock contention reduction, and measurement-driven verification.
- **Activate When**: Investigating high database CPU/latency, optimizing list/report endpoints, reviewing ORM queries, or adding indexes.
- **Do Not Use When**: Designing initial greenfield entity relationships before queries exist (`database-architecture-integrity`).

#### Skill 26 — `import-export-data-processing` (Import/Export & Data Processing)
- **Path**: `skills/import-export-data-processing/SKILL.md`
- **Purpose**: Engineer safe, memory-bounded, transactional CSV/spreadsheet/data import and export pipelines with strict validation, duplicate handling, and row-level error reporting.
- **Covers**: CSV/XLSX/JSON import and export, header and column type validation, duplicate detection and idempotent upserts, foreign-key relational integrity checks, batch/chunked streaming processing (preventing OOM on large files), transaction safety, actionable per-row error reporting, CSV formula injection neutralization (`=`, `+`, `-`, `@`), access-controlled exports, and reconciliation totals.
- **Activate When**: Building or auditing file import/export features, bulk data uploads, ETL batch jobs, or report downloads.
- **Do Not Use When**: Handling simple single-record CRUD form submissions (`ui-ux-design-systems`, `application-security-owasp`).

#### Skill 27 — `api-external-service-integration` (API and External Service Integration)
- **Path**: `skills/api-external-service-integration/SKILL.md`
- **Purpose**: Build fault-tolerant integrations with external REST, GraphQL, gRPC, or SOAP services using strict contracts, timeouts, bounded retries, rate-limit handling, and circuit breakers.
- **Covers**: API contract typing and response validation, outbound authentication and token refresh, explicit connection/read timeouts, exponential backoff with jitter, upstream pagination consumption, rate-limit handling (`429`, `Retry-After`), circuit breakers and graceful degradation, API version compatibility, and deterministic contract/mock testing.
- **Activate When**: Integrating third-party APIs (payment gateways, shipping, CRM, email/SMS, government/partner APIs) or internal microservices.
- **Do Not Use When**: Integrating LLM/generative AI providers specifically (use `ai-provider-integration` alongside this skill).

#### Skill 28 — `ai-provider-integration` (AI Provider Integration)
- **Path**: `skills/ai-provider-integration/SKILL.md`
- **Purpose**: Integrate LLM and generative AI provider APIs reliably with strict credential isolation, schema-validated outputs, token/cost budgets, rate-limit resilience, and privacy controls.
- **Covers**: Server-side API key protection, structured output schemas and response validation, token/context window budgeting and per-user cost caps, streaming and request timeouts, `429`/5xx retry and model fallback strategies, PII redaction before outbound prompts, zero-data-retention configurations, AI telemetry (latency, token counts, finish reasons), and mock vs. live integration testing.
- **Activate When**: Writing or reviewing code that calls OpenAI, Google Gemini, Anthropic, local LLMs, embedding APIs, or AI SDKs.
- **Do Not Use When**: Auditing adversarial prompt injection and tool-execution sandboxing alone (pair with `ai-security-prompt-injection`).

---

### Category G — Performance, Operations, and Deployment

#### Skill 29 — `performance-profiling-optimization` (Performance Profiling & Optimization)
- **Path**: `skills/performance-profiling-optimization/SKILL.md` (with `skills/performance-profiling-optimization/references/core-web-vitals.md`)
- **Purpose**: Conduct end-to-end performance baselining, bottleneck profiling (CPU, memory, DB, network, Core Web Vitals), targeted optimization, and post-change verification.
- **Covers**: Baseline metric capture, CPU/memory/allocation profiling, database and network latency tracing, Core Web Vitals (`LCP`, `INP`, `CLS` at p75) where applicable, hypothesis-driven optimization, before/after comparison, and performance regression monitoring.
- **Activate When**: Diagnosing slow endpoints, high memory/CPU usage, poor Web Vitals, or validating performance-critical changes.
- **Do Not Use When**: Claiming performance improvements without baseline or post-change measurements.

#### Skill 30 — `caching-background-jobs` (Caching & Background Jobs)
- **Path**: `skills/caching-background-jobs/SKILL.md`
- **Purpose**: Design consistent caching layers (Redis, Memcached, HTTP, in-memory) and reliable, idempotent asynchronous background job and scheduler pipelines.
- **Covers**: Cache invalidation and key versioning, cache-aside/write-through consistency, cache stampede protection, queue worker architecture, scheduled job overlap prevention (distributed locks), retry/backoff policies, job idempotency, concurrency limits, dead-letter queue (DLQ) and failed-job recovery, queue observability, and safe payload serialization (passing IDs, never sensitive secrets or stale ORM instances).
- **Activate When**: Implementing or debugging caching, background queues, async email/notification/report workers, or cron/scheduled tasks.
- **Do Not Use When**: Tuning synchronous SQL queries that can be fixed with an index (`query-optimization-performance`).

#### Skill 31 — `ci-cd-release-engineering` (CI/CD & Release Engineering)
- **Path**: `skills/ci-cd-release-engineering/SKILL.md` (with `skills/ci-cd-release-engineering/references/ci-cd-security-hardening.md`)
- **Purpose**: Author, harden, and maintain automated CI/CD pipelines across GitHub Actions, GitLab CI, Jenkins, CircleCI, Azure Pipelines, or Bitbucket Pipelines.
- **Covers**: Automated test and static analysis stages, deterministic build verification, dependency/container vulnerability scanning, migration dry-run checks, protected environments and manual release approvals, artifact signing/management, concurrency groups, rollback automation, failure notifications, and pipeline security hardening (least-privilege tokens, SHA-pinned actions, script-injection prevention).
- **Activate When**: Creating or modifying CI/CD workflow files (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, etc.) or release automation scripts.
- **Do Not Use When**: Performing a pre-release readiness audit of the application itself (`deployment-readiness`).

#### Skill 32 — `environment-configuration-management` (Environment & Configuration Management)
- **Path**: `skills/environment-configuration-management/SKILL.md`
- **Purpose**: Manage development, staging, test, and production configurations and secrets securely with startup validation, environment parity, and zero secret leakage.
- **Covers**: Environment separation (`dev`, `test`, `staging`, `prod`), environment variable schemas and fail-fast startup validation, secret manager integration, runtime compatibility checks, configuration drift prevention, secure production defaults (`DEBUG=false`, strict CORS/TLS), `.env.example` maintenance, and preventing secret exposure in git history, logs, or client-side bundles (`NEXT_PUBLIC_`, `VITE_`).
- **Activate When**: Adding or modifying configuration variables, `.env.example`, secret loading, feature flags, or multi-environment settings.
- **Do Not Use When**: Authoring CI/CD runner YAML syntax (`ci-cd-release-engineering`).

#### Skill 33 — `deployment-readiness` (Deployment Readiness & Release Safety)
- **Path**: `skills/deployment-readiness/SKILL.md`
- **Purpose**: Evaluate whether an application build and target environment are safe and ready for release—without executing an unauthorized deployment.
- **Covers**: Production build verification, environment/secret config checks, database migration forward/rollback safety, pre-deploy backup verification, HTTPS/TLS and filesystem/service permissions, queue worker and scheduler readiness, `/health` and `/ready` endpoints, rollback runbook verification, post-deployment smoke-test definition, release risk assessment, and explicit handoff to `final-quality-gate`.
- **Activate When**: Preparing a release, reviewing a deployment checklist, or assessing whether a branch is safe to deploy to staging or production.
- **Do Not Use When**: The user has not asked to evaluate release readiness, or when attempting to execute an actual live deployment without explicit user authorization.

#### Skill 34 — `observability-incident-diagnosis` (Observability & Incident Diagnosis)
- **Path**: `skills/observability-incident-diagnosis/SKILL.md`
- **Purpose**: Implement structured logging, metrics, distributed tracing, and health checks, and conduct systematic root-cause diagnosis during operational incidents.
- **Covers**: Structured JSON logging, correlation/request ID propagation, sensitive data redaction in logs, RED/USE metrics, OpenTelemetry distributed tracing, error tracking integration, deep health/readiness probes, symptom-based alerting, incident triage and timeline reconstruction, and blameless root-cause analysis (RCA).
- **Activate When**: Adding logging/metrics/tracing/health endpoints, configuring error monitoring, or diagnosing production/staging incidents and stack traces.
- **Do Not Use When**: Formatting routine unit test execution reports (`test-reporting-failure-diagnosis`).

#### Skill 35 — `backup-recovery-disaster-preparedness` (Backup, Recovery & Disaster Preparedness)
- **Path**: `skills/backup-recovery-disaster-preparedness/SKILL.md`
- **Purpose**: Design and verify backup strategies, retention policies, point-in-time recovery procedures, and disaster recovery runbooks for stateful systems.
- **Covers**: 3-2-1 backup architecture, automated database/storage backups and WAL/binlog archiving, retention and lifecycle policies, documented step-by-step restore procedures, periodic restore verification testing, RPO and RTO alignment, backup encryption and checksum integrity, immutable/isolated backup access controls, and recovery ownership.
- **Activate When**: Designing stateful infrastructure, preparing pre-migration backup plans, or auditing disaster recovery readiness.
- **Do Not Use When**: Working on purely stateless client-side components.

#### Skill 36 — `seo-web-discoverability` (SEO & Web Discoverability)
- **Path**: `skills/seo-web-discoverability/SKILL.md`
- **Purpose**: Optimize public-facing web pages for search engine crawlability, indexing, structured metadata, and social sharing while protecting private routes from accidental indexing.
- **Covers**: Page `<title>` and `<meta name="description">`, canonical URLs (`<link rel="canonical">`), XML sitemaps, `robots.txt` and `<meta name="robots">` / `X-Robots-Tag`, SSR/SSG indexability and HTTP status codes (`200`, `301`, `404`, `410`), crawlable `<a href>` link integrity, Open Graph / Twitter Cards, `JSON-LD` Schema.org structured data, and `hreflang`.
- **Activate When**: Building or auditing public websites, marketing/landing pages, blogs, e-commerce catalogs, or public documentation portals.
- **Do Not Use When**: Working on private authenticated dashboards, internal admin panels, or B2B back-office tools (for those, enforce `noindex, nofollow` and authentication rather than public SEO).

---

### Category H — Final Quality and Maintenance

#### Skill 37 — `documentation-developer-handoff` (Documentation Quality & Developer Handoff)
- **Path**: `skills/documentation-developer-handoff/SKILL.md`
- **Purpose**: Ensure repository documentation, setup guides, testing instructions, operational runbooks, and developer handoff materials are accurate, complete, and verified against the actual codebase.
- **Covers**: Clean-clone setup instructions, `.env.example` and configuration reference, test execution commands, architecture overview, deployment and rollback runbooks, troubleshooting guides, operational handoff checklists, maintenance schedules, and documentation-to-code verification.
- **Activate When**: Completing a feature, milestone, refactoring, or project handoff, or auditing stale repository documentation.
- **Do Not Use When**: Recording a single isolated architectural trade-off during initial design (`technical-decision-records`).

#### Skill 38 — `final-quality-gate` (Final Quality Gate & Release Audit)
- **Path**: `skills/final-quality-gate/SKILL.md` (with `skills/final-quality-gate/references/gate-checklist.md`)
- **Purpose**: Execute the authoritative 15-point release audit consolidating evidence from all applicable lifecycle skills (`SKILL-01` through `SKILL-37`) and issue a binding readiness verdict.
- **Covers**: All 15 mandatory assessment domains (Requirements, Functional Completeness, Code Quality, Automated Tests, Security Review, Dependency Vulnerabilities, Database Integrity/Migrations, API/Integration Reliability, UI/UX & Accessibility, Performance, Environment/Secrets, Backup/Rollback, Logging/Monitoring/Health Checks, Documentation, Post-Deploy Smoke Tests), strict evidence classification (`PASS`, `FAIL`, `BLOCKED`, `NOT TESTED`), justified exclusions, human risk acceptance tracking, and final verdict determination (`READY`, `READY WITH ACCEPTED RISKS`, `BLOCKED`, `INCOMPLETE`).
- **Activate When**: Before declaring any feature, milestone, pull request, or application release complete or ready for deployment.
- **Do Not Use When**: Still in initial project discovery before any work or audit has been requested (`project-discovery`).
