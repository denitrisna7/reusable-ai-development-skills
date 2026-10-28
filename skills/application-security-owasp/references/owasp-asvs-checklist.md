# OWASP ASVS (V1-V14) & OWASP Top 10 (A01-A10) Verification Checklist

> **Primary Sources**:
> - OWASP Application Security Verification Standard (ASVS): https://owasp.org/www-project-application-security-verification-standard/
> - OWASP Top 10: https://owasp.org/www-project-top-ten/

Use this verification checklist during design, implementation, and security review to scale controls to the application's actual risk level.

---

## 1. Risk-Based ASVS Level Selection Matrix

| ASVS Level | Risk Profile & Target Systems | Mandatory Verification Depth |
| :--- | :--- | :--- |
| **Level 1 (L1: Opportunistic Baseline)** | All web applications, low-risk internal utilities, public informational apps, and MVPs preparing for initial launch. | Protects against easily discoverable and common vulnerabilities (SQLi, XSS, CSRF, broken authentication, exposed debug configs). Verifiable via automated security testing, configuration inspection, and targeted code checks. |
| **Level 2 (L2: Standard Defense-in-Depth)** | Applications processing PII, B2B multi-tenant SaaS, payment/billing workflows, administrative portals, and healthcare/enterprise data systems. | Protects against motivated attackers. Requires explicit object-level authorization checks, defense-in-depth input validation, hardened session management, cryptographic key hygiene, structured security logging, and threat-driven test cases. |
| **Level 3 (L3: High-Assurance Critical)** | Critical infrastructure, core banking/settlement engines, medical life-safety systems, defense systems, and high-value regulated platforms. | Protects against advanced persistent threats and insider abuse. Requires strict architectural isolation, hardware-backed cryptography (HSM/KMS), zero-trust service authentication, formal threat modeling, and continuous audit verification. |

---

## 2. OWASP Top 10 (A01-A10) Engineering & Verification Checklist

### A01: Broken Access Control
- [ ] **Default-Deny Enforcement**: Every private route, controller, GraphQL resolver, and RPC handler enforces authentication and authorization server-side before executing business logic.
- [ ] **IDOR / BOLA Prevention**: Every query fetching, updating, or deleting a record by ID scopes the query to the authenticated principal's ownership or tenant context (`WHERE id = ? AND tenant_id = ?`).
- [ ] **Function-Level Authorization**: Administrative, billing, and role-management actions verify explicit role/permission claims server-side; hidden UI buttons or client-side router guards are never trusted as security controls.
- [ ] **Mass Assignment Protection**: Request payloads are filtered through strict allowlists/DTOs so attackers cannot overwrite `role`, `is_admin`, `tenant_id`, `balance`, or `verified_at`.
- [ ] **CSRF Defense**: Cookie-authenticated state-changing endpoints (`POST`, `PUT`, `PATCH`, `DELETE`) enforce anti-CSRF tokens and `SameSite=Lax` or `SameSite=Strict` cookies.
- [ ] **CORS Lockdown**: `Access-Control-Allow-Origin` uses an explicit origin allowlist; `Access-Control-Allow-Credentials: true` is never paired with a wildcard (`*`) or reflected arbitrary `Origin` header.

### A02: Cryptographic Failures
- [ ] **Password Hashing**: Passwords and secret recovery codes are hashed with Argon2id (preferred), bcrypt (cost >= 12), or PBKDF2-HMAC-SHA256 (iterations >= 600,000); MD5, SHA-1, and unsalted hashes are forbidden.
- [ ] **Encryption in Transit**: TLS 1.2+ (prefer TLS 1.3) is enforced for all external traffic and sensitive internal connections, accompanied by `Strict-Transport-Security` (HSTS).
- [ ] **Encryption at Rest**: Sensitive fields (API tokens, tax IDs, bank details, health records) use authenticated encryption (`AES-256-GCM` or `ChaCha20-Poly1305`) with keys managed outside source code.
- [ ] **Cryptographic Randomness**: Session IDs, password reset tokens, CSRF tokens, and API keys are generated exclusively using the platform CSPRNG (`crypto.randomBytes`, `random_bytes`, `secrets.token_urlsafe`, `crypto/rand`).

### A03: Injection
- [ ] **SQL & ORM Parameterization**: All database queries use prepared statements or bound parameters; string interpolation or concatenation of user input into SQL, HQL, or raw ORM expressions (`whereRaw`, `extra`, `fmt.Sprintf`) is prohibited.
- [ ] **Dynamic Identifier Allowlisting**: Dynamic table names, column names, and `ORDER BY` directions are validated against a strict hardcoded allowlist before query construction.
- [ ] **XSS & Output Encoding**: User-supplied content rendered in HTML, attributes, URLs (`javascript:` / `data:` blocked), or CSS is context-encoded; dangerous sinks (`dangerouslySetInnerHTML`, `v-html`, `{!! !!}`, `mark_safe`, `innerHTML`) are avoided or sanitized with a strict allowlist sanitizer (e.g., DOMPurify).
- [ ] **OS Command & Template Injection**: User input is never passed to shell interpreters (`sh -c`, `exec`, `system`, `subprocess.Popen(..., shell=True)`) or evaluated inside server-side templates (`eval`, `Twig` string templates, `Jinja2` `from_string`).

### A04: Insecure Design
- [ ] **Business Logic Concurrency**: Financial transfers, coupon redemptions, seat reservations, and quota deductions use atomic database operations or pessimistic/optimistic locking (`SELECT ... FOR UPDATE`) to prevent race conditions (TOCTOU).
- [ ] **Workflow State Integrity**: Multi-step wizards, checkout flows, and approval pipelines verify prerequisite state transitions server-side on every step.
- [ ] **Anti-Automation & Abuse Limits**: High-cost and sensitive operations (registration, login, OTP verification, password reset, exports, AI generation) enforce per-IP and per-account rate limits.

### A05: Security Misconfiguration
- [ ] **Production Debug Lockdown**: Debug error pages, stack trace exposure, development profilers (Telescope, Debugbar, Werkzeug debugger, pprof public endpoints), and directory listings are disabled in production.
- [ ] **HTTP Security Headers**: Responses set `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `X-Frame-Options: DENY` (or CSP `frame-ancestors`), and `Permissions-Policy`.
- [ ] **Cloud & Storage Permissions**: Object storage buckets (S3, GCS, Azure Blob) block public ACLs by default unless explicitly designated for public static assets.

### A06: Vulnerable and Outdated Components
- [ ] **Dependency Hygiene**: Lockfiles are committed, transitive dependencies are audited for known CVEs, and unused packages or risky post-install scripts are removed.

### A07: Identification and Authentication Failures
- [ ] **Session Fixation & Rotation**: Session identifiers are regenerated immediately upon login, privilege elevation, and password change.
- [ ] **Session Cookie Hardening**: Session cookies set `HttpOnly`, `Secure`, `SameSite`, and an appropriate path/expiration (`Max-Age` / `Expires`).
- [ ] **Credential Recovery Safety**: Password reset and magic-link tokens are high-entropy (>= 128 bits), single-use, time-limited (e.g., <= 15-60 minutes), stored hashed in the database, and never leaked via `Referer` headers or generic responses that enable user enumeration.
- [ ] **Session Revocation**: Logging out or resetting a password invalidates the server-side session or revokes active refresh tokens.

### A08: Software and Data Integrity Failures
- [ ] **Safe Deserialization**: Untrusted data is parsed using safe data-only parsers (`JSON.parse`, `json_decode`, `yaml.safe_load`); native object deserialization (`unserialize`, `pickle.loads`, `ObjectInputStream`, `BinaryFormatter`) is never used on untrusted input.
- [ ] **Webhook & Artifact Integrity**: Incoming webhooks verify cryptographic HMAC signatures and replay timestamps before processing payloads.

### A09: Security Logging and Monitoring Failures
- [ ] **Security Event Audit Trail**: Authentication successes/failures, authorization denials, role changes, password resets, API key creation, and data exports are logged with actor ID, timestamp, IP, and request correlation ID.
- [ ] **Secret & PII Redaction**: Passwords, session cookies, bearer tokens, payment card numbers, and raw secret keys are stripped before logs are emitted.
- [ ] **Log Injection Prevention**: User-controlled strings written to logs are structured (JSON) or sanitized against CR/LF newline and terminal escape sequence injection.

### A10: Server-Side Request Forgery (SSRF)
- [ ] **Outbound URL Validation**: Server-side HTTP clients fetching user-influenced URLs validate the scheme (`https` only) and hostname against an allowlist where possible.
- [ ] **Internal Network Blocking**: DNS resolution is checked prior to connection to block loopback (`127.0.0.0/8`, `::1`), private RFC 1918 ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), and cloud metadata endpoints (`169.254.169.254`, `fd00:ec2::254`), and HTTP redirects are not followed blindly.

---

## 3. OWASP ASVS V1-V14 Domain Verification Summary

| ASVS Chapter | Core Verification Requirement | Minimum Level |
| :--- | :--- | :--- |
| **V1 Architecture & Design** | Document trust boundaries, enforce tenant separation at the data layer, and apply least privilege across services. | L1 / L2 |
| **V2 Authentication** | Enforce strong password policies, constant-time secret comparison, MFA support where required, and brute-force throttling. | L1 |
| **V3 Session Management** | Use CSPRNG tokens, rotate session IDs on auth state change, enforce idle/absolute timeouts, and support revocation. | L1 |
| **V4 Access Control** | Enforce server-side policy checks for every route, action, and object reference (`IDOR` protection). | L1 |
| **V5 Validation & Encoding** | Validate input syntax, types, bounds, and schemas at trust boundaries; apply context-specific output encoding. | L1 |
| **V6 Stored Cryptography** | Use vetted standard algorithms, separate keys from code/data, and support key rotation without downtime. | L2 |
| **V7 Error Handling & Logging** | Return generic client error messages on unexpected faults; log security events with correlation IDs and secret redaction. | L1 |
| **V8 Data Protection** | Classify sensitive data, disable client caching on private responses (`Cache-Control: no-store`), and minimize stored PII. | L2 |
| **V9 Communications** | Enforce TLS 1.2/1.3, HSTS, and authenticated internal service communication. | L1 |
| **V10 Malicious Code** | Ensure no debug backdoors, unauthorized telemetry, or unreviewed dynamic code execution exists. | L1 |
| **V11 Business Logic** | Enforce sequential step order, concurrency locks, and anti-automation rate limits on critical business flows. | L1 / L2 |
| **V12 Files & Resources** | Validate file size, extension allowlist, and magic bytes; store outside webroot with random names; set `nosniff` and `attachment` on downloads. | L1 |
| **V13 API & Web Service** | Enforce `Content-Type` checks, bounded pagination limits, strict schema validation, and per-client rate limiting. | L1 |
| **V14 Configuration** | Strip debug utilities in production, set security headers, and lock down CORS and cloud storage permissions. | L1 |
