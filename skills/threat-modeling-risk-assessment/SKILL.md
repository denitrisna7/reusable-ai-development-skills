---
name: threat-modeling-risk-assessment
description: "Performs structured threat modeling and security risk assessments using STRIDE, trust boundary mapping, and likelihood-impact scoring. Activate before implementing new architectures, multi-tenant flows, payment/auth systems, external integrations, or high-risk changes to identify assets, attack surfaces, mitigations, and residual risks. Do not use for routine syntax linting or UI styling."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-13"
  category: "Security Engineering"
---

# Threat Modeling & Risk Assessment

This skill provides a structured, actionable methodology for identifying security threats, analyzing trust boundaries, prioritizing risks, and defining mandatory security controls before or during high-risk engineering changes. It combines STRIDE analysis, business-logic abuse cases, and likelihood-by-impact risk scoring to focus engineering effort on threats that materially affect confidentiality, integrity, and availability.

## 1. Activation Conditions

Activate this skill when the task involves any of the following scenarios:
- Designing a new application architecture, microservice boundary, or multi-tenant isolation model.
- Planning or reviewing high-risk features such as authentication, role/permission management, billing/payments, ledger transfers, file ingestion, webhook callbacks, or AI agent tool execution.
- Introducing a new external integration, public API endpoint, administrative impersonation flow, or cross-organization sharing mechanism.
- Evaluating the security impact of an architectural migration, database tenancy change, or infrastructure topology change.
- Assessing residual security risks before release sign-off to determine whether a system is `READY`, `READY WITH ACCEPTED RISKS`, or `BLOCKED`.

## 2. When Not to Use

Do not use this skill as the primary workflow for the following tasks:
- Fixing an already-identified, isolated code vulnerability (e.g., parameterizing a single SQL query or adding a missing CSRF token): route directly to `application-security-owasp` (`SKILL-10`).
- Auditing npm/Composer/pip lockfiles for known library CVEs: route to `dependency-supply-chain-security` (`SKILL-09`).
- Performing routine code formatting, static analysis, or non-security refactoring: route to `code-quality-static-analysis` (`SKILL-07`) or `refactoring-legacy-code-safety` (`SKILL-08`).

## 3. Scope and Objectives

Every threat modeling and risk assessment engagement must explicitly cover:
- **Assets and Crown Jewels**: Identify the high-value data assets (credentials, encryption keys, PII, financial ledgers, tenant intellectual property) and operational assets (availability, compute quotas, external API credits) at stake.
- **Trust Boundaries and Data Flows**: Map how data moves across untrusted clients, public networks, API gateways, application workers, databases, object storage, and third-party providers.
- **Attack Surface Enumeration**: Catalogue all exposed entry points including HTTP routes, webhooks, GraphQL resolvers, WebSockets, file uploads, CLI jobs, and RAG/AI ingestion channels.
- **Structured Threat Identification (STRIDE + Abuse Cases)**: Systematically evaluate Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege alongside domain-specific business logic abuse cases.
- **Impact Assessment and Risk Prioritization**: Score each threat by Likelihood (`Low`, `Medium`, `High`) and Impact (`Low`, `Medium`, `High`, `Critical`) to establish a prioritized remediation order.
- **Mitigation Strategies and Security Requirements**: Translate prioritized threats into concrete, testable engineering controls (preventive, detective, and corrective) mapped to code and configuration.
- **Residual Risk Documentation**: Record any risk that cannot be fully eliminated in code, specify compensating controls, and escalate high/critical residual risks for explicit human decision-maker approval.

## 4. Prerequisites and Context Requirements

Before conducting threat modeling, gather the following context from the codebase or requirements:
1. **System Architecture & Components**: Identify the runtime services, data stores, queues, caches, and third-party integrations involved in the feature.
2. **Actor & Privilege Matrix**: List all actors (anonymous visitor, authenticated user, tenant admin, support operator, system cron/worker, external webhook sender) and their intended privilege boundaries.
3. **Data Sensitivity Classification**: Determine whether the data in scope includes Restricted credentials/keys, Confidential PII/financial data, or public content.
4. **Deployment & Network Context**: Understand whether endpoints are internet-facing, behind a WAF/VPN, or internal service-to-service.

## 5. Step-by-Step Workflow

Follow this numbered engineering procedure to execute a threat model and risk assessment:

### Step 1: Decompose the System, Assets, and Trust Boundaries
1. List the core assets created, read, updated, or deleted by the feature.
2. Identify every **Trust Boundary** crossed during execution:
   - **Boundary 1 (Browser / Mobile Client -> Public API)**: Untrusted client input enters the backend.
   - **Boundary 2 (External Partner / Webhook -> Backend)**: External party sends signed/unsigned callbacks.
   - **Boundary 3 (Tenant A -> Shared Application / Database -> Tenant B)**: Multi-tenant logical separation boundary.
   - **Boundary 4 (Application -> External Third-Party / AI API)**: Outbound transmission of internal data or reception of untrusted external responses.
   - **Boundary 5 (Application Process -> OS / File System / Database)**: Execution of queries, file operations, or subprocesses.

### Step 2: Enumerate the Attack Surface
1. For each trust boundary, list every concrete entry point:
   - URL paths, HTTP methods, headers, cookies, and query parameters.
   - Uploaded file formats, archive extractors, CSV/Excel parsers, or webhook payloads.
   - Multi-step state transitions (e.g., `cart -> checkout -> payment_callback -> fulfillment`).

### Step 3: Identify Threats Using STRIDE and Business Abuse Cases
Evaluate each entry point and data flow across all six STRIDE categories plus business logic abuse:
1. **Spoofing (`S`)**: Can an attacker forge an identity, session, webhook event, tenant header (`X-Tenant-ID`), or IP address (`X-Forwarded-For`)?
2. **Tampering (`T`)**: Can an attacker modify prices, quantities, user IDs, role flags, signed URLs, or state transitions in transit or storage?
3. **Repudiation (`R`)**: Can an actor perform a sensitive mutation (fund transfer, role grant, data deletion, admin override) without an immutable, attributable audit log?
4. **Information Disclosure (`I`)**: Can an attacker read another user's or tenant's records via IDOR, verbose error messages, timing side-channels, unencrypted storage, or shared cache keys?
5. **Denial of Service (`D`)**: Can an attacker exhaust CPU, memory, database connections, disk space, or paid third-party API quotas via unbounded pagination, regex backtracking (ReDoS), zip bombs, or unthrottled endpoints?
6. **Elevation of Privilege (`E`)**: Can a standard user invoke admin endpoints, bypass subscription quotas, self-approve a workflow, or escape a sandbox?
7. **Business Logic Abuse**: Can an attacker exploit race conditions (double-spending a coupon/balance via concurrent requests), replay a valid webhook, or abuse free-tier trials?

### Step 4: Assess Impact and Prioritize Risks
Rate each identified threat using the Likelihood x Impact matrix:
- **Critical Risk**: High/Medium Likelihood + Critical Impact (e.g., unauthenticated RCE, SQLi, cross-tenant data breach, payment bypass, authentication bypass). **Mandatory blocker: must be mitigated before implementation/release.**
- **High Risk**: High Likelihood + High Impact or Medium Likelihood + Critical Impact (e.g., stored XSS, IDOR on user records, unsigned webhook state change, missing rate limit on OTP/login). **Mandatory mitigation required before release.**
- **Medium Risk**: Low Likelihood + High Impact or Medium Likelihood + Medium Impact (e.g., CSRF on low-impact preference, missing security header with compensating control). **Mitigate in current cycle or document explicit compensating control.**
- **Low Risk**: Low Likelihood + Low Impact. **Fix opportunistically or track as hardening backlog.**

### Step 5: Define Concrete Mitigations and Security Requirements
1. For every Critical, High, and Medium threat, define an explicit, testable **Security Requirement** (`SR-01`, `SR-02`, ...):
   - Specify the exact architectural or code-level control (e.g., `SR-01: Acquire row lock via SELECT ... FOR UPDATE on wallet row before balance deduction`).
   - Specify the verification method (unit/integration negative test, static check, or runtime config check).
2. Document any **Residual Risk** that remains after code controls are applied (e.g., reliance on upstream CDN DDoS protection or manual administrative review).

## 6. Technology-Specific Adaptation Rules

Adapt threat analysis to the specific failure modes of the project's technology stack:
- **PHP (Laravel / Symfony / CodeIgniter)**:
  - Check for unguarded mass assignment (`Model::create($request->all())`), unscoped route model binding (`Route::get('/invoices/{invoice}')` without `scopeBindings()` or policy check), `unserialize()` on untrusted data, and public storage symlink exposure.
- **JavaScript / TypeScript (Node.js / Next.js / React / Vue)**:
  - Check Next.js Server Actions (`"use server"`) for missing authentication/authorization checks, accidental leakage of server secrets into Client Component props, prototype pollution in deep object merges, and event-loop blocking via synchronous crypto/regex.
- **Python (Django / FastAPI / Flask)**:
  - Check FastAPI endpoints for missing `Depends()` auth guards or Returning raw ORM models instead of filtered `response_model` schemas; check Django for `csrf_exempt` misuse, `pickle`/`yaml.load` deserialization, and `.extra()`/`RawSQL` usage.
- **Go / Rust / Java (Spring) / C# (.NET)**:
  - In Go, check goroutine leaks, race conditions on shared maps/structs (`go test -race`), and SSRF in default `http.Client`. In Java/.NET, check Jackson/BinaryFormatter polymorphic deserialization and Actuator/Swagger exposure in production.
- **Mobile (Flutter / Native)**:
  - Treat the mobile binary and local device storage as an untrusted environment; assume API keys embedded in client builds can be extracted via reverse engineering and enforce all authorization and quota controls server-side.
- **Unknown or Mixed Stacks**:
  - Map the process boundaries, network listeners, and data stores first; apply STRIDE at every boundary where data crosses between components of differing trust levels.

## 7. Security and Safety Considerations

- **Proportionate Depth**: Keep threat models focused on realistic attack vectors and concrete code controls rather than theoretical nation-state physical hardware attacks unrelated to the application's risk profile.
- **No Unapproved Risk Acceptance**: An AI agent must never unilaterally accept a Critical or High security risk on behalf of the user; surface unmitigated high-severity risks prominently and mark release readiness as `BLOCKED` until mitigated or explicitly approved by the human owner.
- **Safe Documentation**: Describe vulnerabilities and attack vectors analytically so developers can fix them; do not commit live exploit payloads targeting production URLs.

## 8. Verification Criteria

A threat modeling and risk assessment task is complete only when:
- [ ] All assets, actors, entry points, and trust boundaries for the target feature/system are explicitly mapped.
- [ ] Threats are evaluated across all STRIDE categories and domain-specific business logic abuse cases (including concurrency/race conditions).
- [ ] Every identified threat is scored by Likelihood, Impact, and overall Risk Severity (`Critical`, `High`, `Medium`, `Low`).
- [ ] Every `Critical` and `High` risk is paired with a concrete, testable security requirement (`SR-XX`) and verification test criterion.
- [ ] Residual risks and any assumptions requiring human sign-off are explicitly documented.

## 9. Failure Handling and Edge Cases

- **Incomplete Architecture Visibility**: If external infrastructure details (e.g., WAF rules, VPC firewall policies, KMS configuration) are not visible inside the repository, do not assume those infrastructure protections exist. Require application-layer defense-in-depth controls and record the infrastructure unknown as an explicit assumption to verify.
- **High-Risk Change Requested Without Security Budget/Scope**: If a user requests a quick implementation of a high-risk feature (e.g., custom file upload or payment webhook) without mentioning security, proactively embed the mandatory Critical/High mitigations (signature check, IDOR scope, path sanitization) into the implementation plan rather than shipping an insecure baseline.

## 10. Expected Outputs and Reporting Requirements

Present the threat model and risk assessment using the following Markdown template:

```markdown
# Threat Model & Security Risk Assessment

## 1. System Scope, Assets & Trust Boundaries
- **Feature / Module in Scope**: `<name and components>`
- **High-Value Assets**: `<data, credentials, financial state, availability>`
- **Trust Boundaries**:
  - `TB-01`: `<Untrusted Actor/System>` -> `<Target Component>` (`<protocol/channel>`)

## 2. Prioritized Threat & Risk Register (STRIDE + Abuse Cases)
| Threat ID | Boundary / Entry Point | Category (`STRIDE` / `Abuse`) | Threat Description | Likelihood | Impact | Risk Rating | Mitigation & Security Requirement (`SR-ID`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TM-01` | `TB-01: POST /api/checkout` | `Abuse / Tampering` | Concurrent requests redeem single-use voucher multiple times (TOCTOU). | High | High | **High** | `SR-01`: Wrap voucher check + redemption in DB transaction with `SELECT ... FOR UPDATE` and unique constraint. |
| `TM-02` | `TB-01: GET /api/invoices/:id` | `Info Disclosure` | Authenticated user enumerates other tenants' invoice IDs (IDOR). | High | Critical | **Critical** | `SR-02`: Scope query by `WHERE id = ? AND tenant_id = ?` and add cross-tenant 403/404 test. |

## 3. Mandatory Security Requirements for Implementation & QA
- [ ] `SR-01`: `<Requirement details + verification test>`
- [ ] `SR-02`: `<Requirement details + verification test>`

## 4. Residual Risks & Human Decisions Required
- `<Document any remaining accepted/infrastructure risks and required sign-offs>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Consume system context from `project-discovery` (`SKILL-01`), functional scope from `requirements-analysis` (`SKILL-02`), and design proposals from `adaptive-architecture` (`SKILL-03`).
- **Downstream Security Skills**: Route web/auth controls to `application-security-owasp` (`SKILL-10`), webhook/API controls to `api-security-webhook-reliability` (`SKILL-11`), PII controls to `privacy-data-protection` (`SKILL-12`), and LLM controls to `ai-security-prompt-injection` (`SKILL-14`).
- **Downstream QA & Release Skills**: Feed risk priorities into `testing-strategy-design` (`SKILL-15`) and `backend-testing-tdd` (`SKILL-16`), and supply the residual risk register to `deployment-readiness-release-safety` (`SKILL-33`) and `final-quality-gate-release-audit` (`SKILL-38`).

## 12. Source References

- **OWASP Threat Modeling Project**: https://owasp.org/www-community/Threat_Modeling
- **OWASP Threat Modeling Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html
- **OWASP ASVS V1 (Architecture, Design and Threat Modeling)**: https://owasp.org/www-project-application-security-verification-standard/
- **Library Reference**: [../../references/owasp-asvs-top10-reference.md](../../references/owasp-asvs-top10-reference.md)
