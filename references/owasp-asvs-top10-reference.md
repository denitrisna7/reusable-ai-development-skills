# OWASP ASVS & OWASP Top 10 Security Reference

> Primary Sources:
> - **OWASP Application Security Verification Standard (ASVS)**: https://owasp.org/www-project-application-security-verification-standard/
> - **OWASP Top 10**: https://owasp.org/www-project-top-ten/

This reference maps OWASP Top 10 risk categories and OWASP ASVS verification domains to concrete engineering controls and verification checks.

---

## 1. Selecting the Appropriate OWASP ASVS Level

Scale security verification to the application's actual risk profile:

| ASVS Level | Target Application Profile | Verification Depth |
| :--- | :--- | :--- |
| **Level 1 (L1 — Baseline)** | All applications (public websites, low-risk internal tools, prototypes moving to production). | Mitigates opportunistic and common exploitable vulnerabilities (SQLi, XSS, broken auth, default configs). Verifiable via automated scanning, configuration review, and functional security tests. |
| **Level 2 (L2 — Standard)** | Applications handling sensitive data, PII, multi-tenant business logic, B2B SaaS, or financial/healthcare workflows. | Requires defense-in-depth, explicit threat modeling, object-level authorization checks, cryptographic verification, structured audit logging, and secure code review. |
| **Level 3 (L3 — Advanced)** | High-assurance systems: critical infrastructure, high-value financial settlement, medical safety, or regulated sovereign data. | Requires strict architectural compartmentalization, hardware-backed key management, formal threat modeling, zero-trust service boundaries, and continuous verification. |

---

## 2. OWASP Top 10 Risk Matrix & Engineering Controls

| Risk ID | Category | Primary Vulnerabilities | Mandatory Engineering Controls |
| :--- | :--- | :--- | :--- |
| **A01** | **Broken Access Control** | IDOR / BOLA, privilege escalation, missing function-level auth, CORS misconfiguration, path traversal, CSRF. | Enforce server-side authorization on every route/mutation; verify resource ownership (`user_id` / `tenant_id`) in queries; default-deny policies; signed/scoped tokens; SameSite cookies + CSRF tokens for state-changing cookie-authed requests. |
| **A02** | **Cryptographic Failures** | Plaintext secrets, weak password hashing (MD5/SHA1), missing TLS, hardcoded keys, insecure RNG. | Use Argon2id or bcrypt (cost >= 12) for passwords; TLS 1.2/1.3 in transit; AES-GCM / ChaCha20-Poly1305 at rest; OS CSPRNG (`crypto.randomBytes`, `secrets`, `random_bytes`) for tokens. |
| **A03** | **Injection** | SQL injection, NoSQL injection, OS command injection, XSS, SSTI, LDAP/ORM injection. | Use parameterized queries / prepared statements exclusively; validate/whitelist column names in dynamic `ORDER BY`; use context-aware output encoding; avoid shell execution (`exec`/`system`) with user input. |
| **A04** | **Insecure Design** | Missing rate limits on sensitive flows, race conditions (TOCTOU) in balances/coupons, missing trust boundaries. | Perform threat modeling before implementation; enforce database-level unique constraints and `SELECT ... FOR UPDATE` or atomic updates on financial/inventory state; add business-flow rate limits. |
| **A05** | **Security Misconfiguration** | Debug mode enabled in production (`APP_DEBUG=true`, `DEBUG=True`), permissive S3/GCS buckets, default credentials, missing security headers. | Disable debug traces in production; set `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, and `Permissions-Policy`; lock down cloud storage ACLs. |
| **A06** | **Vulnerable and Outdated Components** | Unpatched CVEs in direct/transitive dependencies, abandoned libraries, unpinned packages. | Commit lockfiles; run ecosystem vulnerability audits (`npm audit`, `composer audit`, `pip-audit`, `govulncheck`, `cargo audit`); remove unused dependencies. |
| **A07** | **Identification and Authentication Failures** | Brute-force login/OTP, session fixation, weak session entropy, tokens in URL query strings, missing session invalidation on logout/password reset. | Regenerate session ID upon login/privilege change; enforce rate limiting and lockout/backoff on login/MFA/password-reset; set `HttpOnly`, `Secure`, `SameSite` on session cookies; invalidate active sessions on password change. |
| **A08** | **Software and Data Integrity Failures** | Insecure deserialization (`unserialize`, `pickle`, `yaml.load`), unsigned webhooks, unverified CI/CD third-party actions, unverified scripts. | Never deserialize untrusted byte streams with unsafe deserializers; verify HMAC signatures and timestamps on all incoming webhooks; pin CI actions and third-party scripts (SRI). |
| **A09** | **Security Logging and Monitoring Failures** | Unlogged auth failures or privilege changes, sensitive PII/tokens leaked into logs, log injection. | Log authentication attempts, access control failures, and admin actions with correlation IDs; redact passwords, API keys, tokens, and PII before logging; sanitize log fields against newline/ANSI injection. |
| **A10** | **Server-Side Request Forgery (SSRF)** | Fetching user-supplied URLs (`webhook_url`, `avatar_url`, PDF generators) allowing access to `169.254.169.254` or internal RFC1918 networks. | Validate schemes (`https` only), resolve DNS and block loopback/link-local/private IP ranges (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.169.254`, `::1`), disable automatic HTTP redirects to unvalidated hosts. |

---

## 3. OWASP ASVS Domains Checklist (V1–V14)

- **V1 Architecture, Design and Threat Modeling**: Trust boundaries identified; tenant isolation enforced at data layer; least privilege across service accounts.
- **V2 Authentication**: Credential strength rules; brute-force throttling; timing-safe token comparison (`hash_equals`, `crypto.timingSafeEqual`, `hmac.compare_digest`).
- **V3 Session Management**: Cryptographically random session IDs; session regeneration on login; server-side revocation on logout.
- **V4 Access Control**: Every controller/handler checks both authentication and object-level / role-level authorization; no reliance on client-side hidden fields or disabled buttons.
- **V5 Validation, Sanitization and Encoding**: Strict schema validation (types, lengths, ranges, enums) at API/form boundaries; context-appropriate HTML/attribute/JS encoding.
- **V6 Stored Cryptography**: No custom crypto; rotation support for encryption keys; secrets loaded from environment/secret manager, never committed to VCS.
- **V7 Error Handling and Logging**: Generic, safe error responses to clients; detailed diagnostics routed only to internal structured logs with secret redaction.
- **V8 Data Protection**: Sensitive fields encrypted or masked; `Cache-Control: no-store` on sensitive responses; data retention and deletion paths defined.
- **V9 Communications Security**: HTTPS enforced everywhere; HSTS configured; internal service-to-service traffic authenticated and encrypted.
- **V10 Malicious Code**: No hidden backdoors, debug bypasses, or unverified post-install script execution.
- **V11 Business Logic**: Multi-step workflows enforce state transitions server-side; idempotency and concurrency locks prevent replay or double-spend.
- **V12 Files and Resources**: Validate file uploads by MIME/magic bytes and extension whitelist; enforce size limits; store outside public webroot or in isolated object storage with randomized filenames; serve downloads with `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff`.
- **V13 API and Web Service**: Enforce `Content-Type` validation, pagination bounds (`max_limit`), rate limiting, and schema contracts.
- **V14 Configuration**: Production builds strip development tools; dependency lockfiles verified; security headers active.
