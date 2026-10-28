---
name: application-security-owasp
description: "Implements and verifies application security controls aligned with OWASP ASVS (Levels 1-3) and OWASP Top 10. Activate when designing, implementing, or auditing authentication, authorization, input validation, session management, CSRF/XSS/SQLi defenses, file handling, rate limiting, secrets, error handling, or audit logging. Do not use for third-party supply chain audits or LLM prompt injection."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-10"
  category: "Security Engineering"
---

# Application Security & OWASP Verification

This skill establishes a rigorous, risk-calibrated engineering workflow for designing, implementing, and auditing application security controls based on the OWASP Application Security Verification Standard (ASVS) and the OWASP Top 10. It ensures that authentication, authorization, input validation, cryptography, session security, file handling, and audit logging are verified with concrete evidence rather than assumed safe.

## 1. Activation Conditions

Activate this skill when the task involves any of the following scenarios:
- Implementing or modifying user authentication, login, registration, MFA, password reset, or session management flows.
- Designing or auditing role-based access control (RBAC), attribute-based access control (ABAC), multi-tenant isolation, or object-level ownership checks.
- Reviewing or hardening code against SQL injection, Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), Server-Side Request Forgery (SSRF), or Insecure Direct Object References (IDOR / BOLA).
- Building file upload, file processing, or file download endpoints.
- Configuring rate limiting, HTTP security headers, CORS policies, secret handling, safe error responses, or security audit logging.
- Conducting a pre-release application security review mapped to OWASP ASVS Level 1, Level 2, or Level 3.

## 2. When Not to Use

Do not use this skill as the primary workflow for the following specialized tasks:
- Auditing third-party package lockfiles, CVEs, or supply chain risks: route to `dependency-supply-chain-security` (`SKILL-09`).
- Designing webhook signature verification, idempotency keys, and retry backoff protocols: route to `api-security-webhook-reliability` (`SKILL-11`).
- Designing PII retention schedules, GDPR/CCPA erasure workflows, or regulatory data mapping: route to `privacy-data-protection` (`SKILL-12`).
- Performing architectural STRIDE threat modeling before code exists: route to `threat-modeling-risk-assessment` (`SKILL-13`).
- Defending LLM features against direct/indirect prompt injection or unsafe tool calls: route to `ai-security-prompt-injection` (`SKILL-14`).

## 3. Scope and Objectives

Every engagement using this skill must address and verify the following security domains where applicable to the change scope:
- **Risk-Calibrated OWASP ASVS Selection**: Select ASVS Level 1 (Baseline), Level 2 (Standard Defense-in-Depth), or Level 3 (High-Assurance) based on the application's actual risk profile.
- **Authentication and Session Security**: Enforce strong password hashing (Argon2id/bcrypt), brute-force throttling, CSPRNG session tokens, session ID regeneration on login/privilege change, `HttpOnly`/`Secure`/`SameSite` cookies, and server-side revocation on logout or password reset.
- **Authorization and Least Privilege**: Enforce server-side access checks on every route and action, default-deny policies, strict mass-assignment allowlists, and least-privilege service/database accounts.
- **IDOR and Broken Object-Level Authorization (BOLA) Prevention**: Scope every data query and mutation by the authenticated principal's ownership or tenant context (`tenant_id` / `user_id`).
- **Injection Defense (SQLi, NoSQLi, Command Injection)**: Use parameterized queries/prepared statements exclusively, validate dynamic sort/column identifiers against strict allowlists, and avoid shell execution with user input.
- **Cross-Site Scripting (XSS) and CSRF Protection**: Apply context-aware output encoding, restrict dangerous HTML sinks, enforce anti-CSRF tokens on cookie-authenticated state-changing requests, and lock down CORS origins.
- **Input Validation and Mass Assignment**: Validate types, lengths, ranges, enums, and schemas at all trust boundaries before business logic executes.
- **File Upload and Download Security**: Validate file size, extension allowlists, and MIME/magic bytes; store uploads outside the public webroot or in isolated object storage with randomized filenames; serve untrusted downloads with `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff`.
- **Rate Limiting and Anti-Automation**: Apply per-IP and per-account rate limits on login, registration, OTP, password reset, exports, and expensive mutations.
- **Secret Management and Safe Error Handling**: Keep secrets out of source code and client bundles, use constant-time secret comparisons, return generic client error messages on unexpected faults, and never leak stack traces in production.
- **Audit Logging and Security Testing**: Log authentication, authorization failures, and sensitive state changes with correlation IDs and secret redaction, and verify controls with automated negative security tests.

## 4. Prerequisites and Context Requirements

Before proposing or modifying security controls, gather the following context:
1. **Technology Stack & Framework**: Identify the backend framework, ORM/query builder, template engine, authentication library, and deployment architecture (monolith, SPA + API, microservices).
2. **Application Risk Profile**: Determine the data sensitivity (public data, internal business data, PII/financial/healthcare data) to select the target OWASP ASVS level.
3. **Authentication & Session Topology**: Identify whether the application uses stateful server sessions (cookies), stateless tokens (JWT/PASETO), OAuth2/OIDC, or API keys.
4. **Trust Boundaries**: Locate all entry points accepting external input (HTTP controllers, GraphQL resolvers, CLI arguments, file uploads, query parameters, headers).

## 5. Step-by-Step Workflow

Follow this numbered engineering procedure when implementing or auditing application security:

### Step 1: Select Target OWASP ASVS Level
1. Classify the target application using `[references/owasp-asvs-checklist.md](references/owasp-asvs-checklist.md)`:
   - **ASVS Level 1**: Low-risk applications or baseline hardening.
   - **ASVS Level 2**: Default target for production applications handling user accounts, multi-tenant data, PII, or business transactions.
   - **ASVS Level 3**: High-assurance financial, medical, or critical infrastructure systems.
2. Document the selected ASVS level and the specific chapters (`V1` through `V14`) impacted by the current task.

### Step 2: Audit Entry Points, Authentication, and Session Handling
1. Inspect authentication handlers:
   - Verify password hashing uses Argon2id or bcrypt (cost >= 12).
   - Verify secret comparisons use constant-time functions (`hash_equals`, `crypto.timingSafeEqual`, `hmac.compare_digest`, `subtle.ConstantTimeCompare`).
   - Verify login, MFA, and password reset endpoints enforce rate limiting and do not leak account existence when enumeration is a risk.
2. Inspect session lifecycle:
   - Ensure session IDs are regenerated upon authentication and privilege changes.
   - Ensure cookies set `HttpOnly`, `Secure`, and `SameSite=Lax` (or `Strict`).
   - Ensure logout and password reset invalidate active server-side sessions or refresh tokens.

### Step 3: Verify Authorization, Least Privilege, and IDOR Controls
1. Trace every route, controller action, and mutation in scope:
   - Confirm middleware/guards enforce authentication before handler execution.
   - Confirm policy/gate checks enforce role and permission rules server-side.
   - Confirm database queries for single records (`GET /orders/:id`, `PATCH /users/:id`, `DELETE /documents/:id`) scope lookups by authenticated `user_id` or `tenant_id` to prevent IDOR.
2. Inspect request binding and ORM models to verify mass assignment is restricted via explicit DTOs, form requests, or `$fillable` allowlists.

### Step 4: Harden Input Validation, Queries, Rendering, and File Handling
1. **Input Validation**: Enforce strict server-side schema validation (types, string lengths, numeric bounds, strict enums) on all request bodies, query params, and headers.
2. **Database Queries**: Replace any string-interpolated SQL or raw ORM clauses with bound parameters; validate dynamic sort columns (`sort_by`, `order`) against a static allowlist.
3. **XSS & CSRF**: Audit template rendering for unescaped outputs; verify CSRF middleware is active on all state-changing cookie-authenticated endpoints.
4. **File Uploads & Downloads**:
   - Reject files exceeding size limits or lacking an allowlisted extension and verified content magic bytes.
   - Generate server-side UUID/random storage keys; never use client-supplied `filename` paths directly.
   - Store uploaded files outside the public webroot or in private bucket paths; serve downloads with `X-Content-Type-Options: nosniff` and `Content-Disposition: attachment`.

### Step 5: Verify Error Handling, Secrets, Headers, and Audit Logging
1. Ensure production configurations disable debug stack traces (`APP_DEBUG=false`, `DEBUG=False`, `NODE_ENV=production`) and return safe, structured error payloads.
2. Confirm no secrets, API keys, or private credentials are hardcoded in source files, client env variables (`NEXT_PUBLIC_*`, `VITE_*`), or committed `.env` files.
3. Verify security audit logs record actor ID, action, target resource ID, IP address, and outcome for sensitive events while redacting passwords and tokens.

### Step 6: Execute Security Verification Tests
1. Write and run automated negative security tests covering unauthenticated access (`401`), cross-user/cross-tenant IDOR attempts (`403`/`404`), invalid/malicious payloads (`422`/`400`), CSRF token omission (`419`/`403`), and rate-limit exhaustion (`429`).

## 6. Technology-Specific Adaptation Rules

Adapt security implementations to the actual project stack without forcing mismatched tools:
- **PHP (Laravel / Symfony / CodeIgniter)**:
  - In Laravel, use `FormRequest` validation, Policies/Gates (`$this->authorize()`), scoped Eloquent relationships (`$user->orders()->findOrFail($id)`), `Hash::make()`, `RateLimiter::for()`, and Blade `{{ }}` auto-escaping (avoid `{!! !!}` on untrusted data).
  - In CodeIgniter, enable `$CSRFProtection = true`, use Query Builder bound parameters or `$db->query($sql, [$binds])`, and escape views with `esc($value, 'html')`.
- **JavaScript / TypeScript (Node.js / Express / Fastify / Next.js / React / Vue)**:
  - Validate inputs with `zod`, `valibot`, or `ajv` at API/Server Action boundaries; remember that Next.js `"use server"` actions are public HTTP endpoints requiring explicit auth, authorization, and schema checks inside every action.
  - Avoid `dangerouslySetInnerHTML` (React) and `v-html` (Vue) on untrusted strings; use `helmet` for HTTP headers and parameterized queries in Prisma/Drizzle/pg.
- **Python (Django / FastAPI / Flask)**:
  - In Django, keep `CSRFViewMiddleware` enabled, avoid `.raw()` / `.extra()` with f-strings, avoid `mark_safe` on user data, and filter querysets by `request.user`.
  - In FastAPI, enforce Pydantic `Field(max_length=..., ge=..., le=...)` validation, inject authorization dependencies (`Depends(get_current_active_user)`), and use SQLAlchemy bound parameters.
- **Go**:
  - Use `database/sql` or `pgx` parameterized placeholders (`$1`, `?`), `html/template` (never `text/template` for HTML), `crypto/rand` (never `math/rand` for secrets), and `http.MaxBytesReader` on request bodies.
- **Java / Kotlin (Spring Boot) & C# (.NET)**:
  - Use Spring Security `@PreAuthorize` / method security or ASP.NET Core Policy-based authorization, Bean Validation (`@Valid`) / FluentValidation, and JPA/EF Core parameterized queries.
- **Rust**:
  - Use `sqlx` compile-time or bound queries (`sqlx::query!`), `argon2` crate for password hashing, `subtle::ConstantTimeEq`, and tower/axum body limit and rate-limit layers.
- **Mobile (Flutter / iOS / Android)**:
  - Store tokens in hardware-backed secure storage (`flutter_secure_storage`, Keychain, EncryptedSharedPreferences), never in plaintext `SharedPreferences`, and never rely on client-side checks for authorization.
- **Unknown or Mixed Stacks**:
  - Inspect existing authentication middleware, database drivers, and error handlers first; apply universal OWASP controls using the stack's native primitives.

## 7. Security and Safety Considerations

- **Never Exploit Production**: Perform security verification and negative payload testing only against local, test, or explicitly authorized staging environments.
- **No Security by Obscurity**: UUIDs, unguessable URLs, or hidden UI elements do not replace server-side authentication and authorization checks.
- **Fail Closed**: Authorization guards, rate limiters (on critical auth flows), and file validators must fail closed when required context or claims are missing.
- **Secret Hygiene in Reports**: Never output real production keys, passwords, or live session tokens in audit reports or test logs; mask sensitive values (`sk_live_...REDACTED`).

## 8. Verification Criteria

Do not declare an application security task complete until the following evidence is verified:
- [ ] Target OWASP ASVS level (L1, L2, or L3) is explicitly documented with justification.
- [ ] Every modified or audited endpoint enforces server-side authentication and object-level/role-level authorization.
- [ ] All database queries use parameterized bindings and dynamic sort/filter identifiers are allowlisted.
- [ ] Automated security tests verify both positive access (`200`/`201`) and negative access (`401` unauthenticated, `403`/`404` IDOR/unauthorized, `422` invalid input).
- [ ] Sensitive secrets, stack traces, and PII are confirmed absent from client error responses and logs.

## 9. Failure Handling and Edge Cases

- **Legacy Endpoints Using Raw SQL or Weak Hashes**: If immediate full migration breaks compatibility, wrap legacy password hashes with transparent upgrade-on-login (`password_needs_rehash` -> Argon2id/bcrypt) and parameterize raw SQL bindings immediately without altering response schemas.
- **Third-Party Library Blocks Strict CSP (`unsafe-inline`)**: Use cryptographic nonces or hashes for scripts where supported, isolate legacy pages if necessary, and document the exact residual CSP constraint rather than disabling CSP globally.
- **Stateless JWT Revocation Limitations**: When short-lived JWTs cannot be revoked instantly, enforce short access token TTLs (e.g., 5-15 minutes), rotate refresh tokens in persistent storage with reuse detection, or maintain a fast deny-list (`jti` / user `tokens_valid_after` timestamp) for password resets and bans.

## 10. Expected Outputs and Reporting Requirements

Provide a structured security verification report using the following template:

```markdown
# Application Security & OWASP Audit Report

## 1. Scope & Target ASVS Level
- **Components Audited**: `<routes, controllers, services, models>`
- **Target OWASP ASVS Level**: `Level 1 / Level 2 / Level 3` (`<justification>`)

## 2. OWASP Control Verification Matrix
| Control Area | OWASP Ref | Status (`PASS`/`FAIL`/`N/A`) | Verification Evidence |
| :--- | :--- | :--- | :--- |
| Authentication & Session Security | ASVS V2, V3 / A07 | `PASS` | `<file:line + test name>` |
| Access Control & IDOR Defense | ASVS V4 / A01 | `PASS` | `<file:line + test name>` |
| Input Validation & Injection Defense | ASVS V5 / A03 | `PASS` | `<file:line + test name>` |
| File Upload / Download Hardening | ASVS V12 / A01, A04 | `N/A` | `<reason or evidence>` |
| Rate Limiting & Abuse Protection | ASVS V2, V11, V13 / A04 | `PASS` | `<route limiter config + test>` |
| Secrets, Errors & Audit Logging | ASVS V6, V7 / A02, A05, A09 | `PASS` | `<config + log redaction check>` |

## 3. Remediations Implemented
- `<file path>`: `<summary of security control added or fixed>`

## 4. Residual Risks & Follow-Up Actions
- `<any remaining environment/infrastructure requirements or accepted risks>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Receive architectural context from `project-discovery` (`SKILL-01`) and threat priorities from `threat-modeling-risk-assessment` (`SKILL-13`).
- **Parallel / Sibling Skills**: Coordinate with `api-security-webhook-reliability` (`SKILL-11`) for webhook/API hardening, `privacy-data-protection` (`SKILL-12`) for PII handling, `ai-security-prompt-injection` (`SKILL-14`) for LLM endpoints, and `dependency-supply-chain-security` (`SKILL-09`) for package CVE audits.
- **Downstream Skills**: Hand off test implementation to `backend-testing-tdd` (`SKILL-16`) and `playwright-mcp-browser-qa` (`SKILL-17`), and provide security evidence to `deployment-readiness-release-safety` (`SKILL-33`) and `final-quality-gate-release-audit` (`SKILL-38`).

## 12. Source References

- **OWASP Application Security Verification Standard (ASVS)**: https://owasp.org/www-project-application-security-verification-standard/
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **OWASP Cheat Sheet Series**: https://cheatsheetseries.owasp.org/
- **Local Skill Checklist**: [references/owasp-asvs-checklist.md](references/owasp-asvs-checklist.md)
- **Library Reference**: [../../references/owasp-asvs-top10-reference.md](../../references/owasp-asvs-top10-reference.md)
