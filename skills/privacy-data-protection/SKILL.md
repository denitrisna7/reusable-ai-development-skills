---
name: privacy-data-protection
description: "Enforces data privacy, PII/PHI/PCI protection, and regulatory compliance across storage, transit, logs, integrations, and AI prompts. Activate when designing schemas or workflows handling personal data, implementing data minimization, retention schedules, right-to-erasure deletion, log redaction, or scrubbing sensitive fields before external API or LLM calls. Do not use for general network firewall setup."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-12"
  category: "Security Engineering"
---

# Privacy & Data Protection

This skill governs the engineering of privacy-by-design and data protection controls across databases, APIs, logs, third-party integrations, and AI workflows. It ensures that personal and sensitive data (PII, PHI, PCI, financial records, and confidential business data) is minimized, access-restricted, encrypted, redacted from logs and AI prompts, retained only as long as necessary, and cleanly deleted or anonymized upon request.

## 1. Activation Conditions

Activate this skill when the task involves any of the following scenarios:
- Designing or modifying database schemas, forms, or APIs that collect, store, or return Personally Identifiable Information (PII), Protected Health Information (PHI), payment data (PCI), or government/tax identifiers.
- Implementing user account deletion, Right to Erasure / Right to be Forgotten, data export (DSAR / data portability), or consent management workflows.
- Auditing or configuring application logging, error trackers (Sentry, Bugsnag, Datadog), analytics, or audit trails to prevent sensitive data leakage.
- Integrating third-party analytics, CRM, marketing, or AI/LLM providers where user data might be transmitted externally.
- Evaluating technical compliance controls for applicable regulations such as GDPR, CCPA/CPRA, HIPAA, PCI-DSS, or Indonesia UU PDP.

## 2. When Not to Use

Do not use this skill as the primary workflow for the following tasks:
- General authentication, SQLi, XSS, or CSRF hardening unrelated to personal data lifecycle: route to `application-security-owasp` (`SKILL-10`).
- Defending LLM prompts against adversarial jailbreaks or tool hijacking: route to `ai-security-prompt-injection` (`SKILL-14`).
- Designing disaster recovery and infrastructure backup snapshots (except where backup retention impacts privacy): route to `backup-recovery-disaster-preparedness` (`SKILL-35`).

## 3. Scope and Objectives

Every privacy-sensitive design, implementation, or audit must cover the following objectives:
- **Data Minimization**: Collect, store, and return only the fields strictly required for the business purpose; omit internal or sensitive attributes from default API serializers.
- **Access Restrictions and Purpose Limitation**: Restrict access to sensitive fields using role-based permissions, tenant isolation, and explicit audit logging for administrative views of personal data.
- **Sensitive Data Handling (Encryption & Masking)**: Encrypt high-risk PII/credentials at rest using authenticated encryption (`AES-256-GCM` / framework encrypted casts), use blind indexes (HMAC-SHA256 with a dedicated pepper key) when exact-match lookup on encrypted columns is required, and mask sensitive values (`****-****-****-1234`, `j***@example.com`) in UIs and exports.
- **Log Redaction and Telemetry Scrubbing**: Strip passwords, tokens, full credit card numbers, national IDs, phone numbers, email addresses, and raw request bodies containing PII from application logs, exception payloads, and tracing spans.
- **Data Retention and Automated Expiration**: Define explicit TTLs and scheduled purge jobs for ephemeral sensitive records (OTPs, password reset tokens, unverified accounts, raw webhook logs, temporary exports, session histories).
- **Data Deletion vs. Anonymization (Right to Erasure)**: Implement safe account/data deletion that removes direct PII across primary tables, caches, search indexes, and object storage while anonymizing immutable financial/accounting ledger records that must be retained by law.
- **Privacy-Aware Third-Party Integrations**: Ensure external analytics, error reporters, and webhooks receive only minimized, consented fields and respect user opt-out states.
- **Preventing Sensitive Data Leakage into AI Requests**: Redact, pseudonymize, or strip PII, secrets, and unrelated tenant records before constructing prompts, embeddings, or context windows sent to external AI/LLM APIs.
- **Applicable Regulatory Alignment**: Map technical controls to the project's relevant regulatory frameworks (GDPR, CCPA/CPRA, HIPAA, PCI-DSS, UU PDP) without fabricating legal advice.

## 4. Prerequisites and Context Requirements

Before implementing privacy controls, inspect the repository to determine:
1. **Data Inventory & Classification**: Identify which models, tables, storage buckets, and caches hold Public, Internal, Confidential (PII), or Restricted (government IDs, health data, payment data, credentials) information.
2. **External Data Sinks**: List all logging transports, APM/error reporting SDKs, analytics scripts, search engines (Elasticsearch, Meilisearch, Algolia), and AI provider integrations.
3. **Legal/Business Retention Constraints**: Identify which records must be hard-deleted immediately upon erasure request versus financial/tax invoices that require tombstone anonymization (`user_id = NULL`, PII scrubbed, transaction amounts preserved).
4. **Target Jurisdictions**: Confirm whether the application serves users subject to GDPR, UU PDP, HIPAA, CCPA, or PCI-DSS.

## 5. Step-by-Step Workflow

Follow this structured engineering workflow when handling personal or sensitive data:

### Step 1: Classify Data and Enforce Data Minimization
1. Review every field in the proposed form, API payload, or database migration:
   - Remove optional personal attributes that have no verified functional requirement.
2. Audit API serializers, DTOs, and GraphQL types:
   - Never return raw model objects (`SELECT *` serialized directly) to clients.
   - Define explicit response DTOs/Resources that expose only fields needed by the current view and caller role.
3. Set `Cache-Control: no-store, private` on HTTP responses returning personal, financial, or health data so shared proxies and browsers do not cache sensitive payloads.

### Step 2: Implement Encryption at Rest, Blind Indexing, and Masking
1. **Field-Level Encryption**: For Restricted PII (national IDs/NIK, SSN, tax IDs, passport numbers, medical notes, OAuth tokens), apply application-layer authenticated encryption before database persistence.
2. **Searchable Encrypted Fields**: When uniqueness checks or exact lookups are required on encrypted fields, compute a deterministic HMAC-SHA256 blind index (`email_bidx` / `national_id_bidx`) using a separate secret key from the encryption key.
3. **Display Masking**: Return masked representations (`+62812****789`, `****1234`) in standard API responses; require an explicit, audit-logged privileged endpoint if full unmasking is ever required by authorized staff.

### Step 3: Configure Log Redaction and Error Reporter Scrubbing
1. Configure structured logger processors/formatters to redact sensitive keys (`password`, `password_confirmation`, `token`, `authorization`, `cookie`, `secret`, `nik`, `ssn`, `credit_card`, `cvv`, `iban`, `dob`) recursively across nested payloads.
2. Configure error monitoring SDKs (e.g., Sentry `beforeSend` / `sendDefaultPii: false`) to strip request bodies, cookies, and raw user IP/email details unless explicitly sanitized.
3. Ensure URL query parameters never carry PII (emails, phone numbers, names, tokens), as URLs are recorded in web server access logs, CDN logs, and browser history.

### Step 4: Guard External Integrations and AI Prompts
1. **AI / LLM Prompt Sanitization**:
   - Before sending user records or documents to an external LLM or embedding API, strip direct PII (names, emails, phone numbers, national IDs, API keys) or replace them with reversible local placeholders (`[USER_1]`, `[EMAIL_1]`).
   - Scope retrieval (RAG) queries strictly by the authenticated `tenant_id` and `user_id` so one user's private data can never enter another user's prompt context.
2. **Third-Party Analytics & Pixels**: Load non-essential tracking scripts only after user consent when required, and pass opaque internal UUIDs rather than raw email addresses or phone numbers in URLs or events.

### Step 5: Engineer Retention Schedules and Right-to-Erasure Workflows
1. **Retention Automation**: Create idempotent scheduled jobs to purge expired tokens, old export files, stale session logs, and unverified registrations beyond their retention window.
2. **Right-to-Erasure / Account Deletion**:
   - Execute deletion inside a coordinated transaction and background cleanup pipeline:
     - Hard-delete or scrub direct PII rows (`users`, `profiles`, `addresses`, `saved_methods`).
     - Anonymize immutable financial/audit records that legally cannot be deleted (e.g., replace buyer name/email on historical ledger entries with `[REDACTED USER #hash]` while preserving financial totals).
     - Delete associated files in object storage (avatars, KYC uploads, generated PDFs) and purge search index documents and cache keys.
     - Revoke all active sessions, API keys, and OAuth tokens immediately.

## 6. Technology-Specific Adaptation Rules

- **PHP (Laravel / Symfony / CodeIgniter)**:
  - In Laravel, use `encrypted` model casts (`'national_id' => 'encrypted'`), `$hidden` model arrays + explicit `JsonResource` classes, `Log::withContext()` redaction middleware, and `MassPrunable` / `Prunable` traits (`php artisan model:prune`) for retention schedules.
- **JavaScript / TypeScript (Node.js / Next.js / React / Vue)**:
  - Configure `pino` `redact: { paths: ['req.headers.authorization', 'req.headers.cookie', '*.password', '*.token', '*.email'], censor: '[REDACTED]' }`.
  - In Next.js, ensure Server Components do not pass full database user objects containing sensitive fields into Client Component props (which serialize into the public HTML/RSC payload).
- **Python (Django / FastAPI / Flask)**:
  - In Django, use `@sensitive_variables()` and `@sensitive_post_parameters()` decorators on views handling PII/credentials, explicit DRF Serializers, and custom logging `Filter` classes to scrub PII patterns.
  - In FastAPI, define separate `UserCreate` and `UserPublic` Pydantic models so sensitive fields are never serialized in responses.
- **Go / Java (Spring Boot) / C# (.NET) / Rust**:
  - Use explicit struct/DTO tags (`json:"-"` in Go, `@JsonIgnore` in Jackson, `[JsonIgnore]` in .NET, `#[serde(skip_serializing)]` in Rust) on sensitive fields and implement custom `fmt.Stringer` / `Debug` / `ToString()` methods so structs containing PII never dump raw values to logs.
- **Mobile (Flutter / iOS / Android)**:
  - Disable OS screenshot/screen-recording capture (`FLAG_SECURE` on Android, secure text/overlay on iOS) on screens displaying highly sensitive health, financial, or secret recovery data where appropriate, and wipe local SQLite/SecureStorage caches on logout.

## 7. Security and Safety Considerations

- **Never Use Soft-Delete Alone as Erasure**: Setting `deleted_at = NOW()` while leaving plaintext PII indefinitely in the table does not satisfy data erasure requirements; either hard-delete or overwrite PII columns with anonymized values after any short grace period expires.
- **PCI-DSS Boundaries**: Never store CVV/CVC codes, PIN blocks, or full magnetic stripe data under any circumstances; delegate card tokenization to PCI-compliant gateways.
- **Backup & Log Awareness**: Because immutable backups and append-only logs cannot easily be edited retroactively, prevent raw PII from entering application logs in the first place and document backup retention TTLs clearly.

## 8. Verification Criteria

Verify all applicable checks with concrete evidence before claiming completion:
- [ ] API responses and client props are inspected to confirm no unrequested PII or hidden model fields are serialized.
- [ ] High-risk sensitive fields are encrypted at rest and masked in standard UI/API views.
- [ ] Logger and error-tracker configurations are tested to confirm passwords, tokens, and PII are redacted (`[REDACTED]`).
- [ ] Account deletion / erasure tests confirm PII is removed from database tables, caches, search indexes, and storage buckets while preserving referential integrity on financial ledgers.
- [ ] Any external AI/LLM integration is verified to strip or pseudonymize PII prior to outbound API calls.

## 9. Failure Handling and Edge Cases

- **Foreign Key Constraints Blocking User Deletion**: Never disable foreign key checks blindly. Classify child tables into (a) cascade-delete personal data (`user_profiles`, `notification_settings`) and (b) set-null / anonymized historical records (`orders`, `invoices`, `audit_logs`) with an explicit transactional erasure service.
- **Third-Party Deletion Failure During Erasure**: If deleting a file in S3/GCS or removing a record from an external CRM fails during an erasure workflow, record the deletion job in a retryable outbox/queue and mark erasure status as `PENDING_EXTERNAL_CLEANUP` until confirmed complete.
- **AI Prompt Requires Entity Disambiguation**: When an LLM must reason about multiple individuals in a text, replace real names/emails with deterministic session-scoped placeholders (`PERSON_A`, `PERSON_B`) and map them back locally only if needed by the authorized user.

## 10. Expected Outputs and Reporting Requirements

Document privacy and data protection verification using the following template:

```markdown
# Privacy & Data Protection Audit Report

## 1. Data Inventory & Regulatory Context
- **Personal / Sensitive Data Fields in Scope**: `<list fields and classification: Confidential PII / Restricted>`
- **Applicable Frameworks**: `<GDPR / UU PDP / CCPA / HIPAA / PCI-DSS / Internal Policy>`

## 2. Privacy Control Verification Matrix
| Privacy Control | Status (`PASS`/`FAIL`/`N/A`) | Verification Evidence |
| :--- | :--- | :--- |
| Data Minimization & DTO Filtering | `PASS` | `<serializer/DTO file + response test>` |
| Encryption at Rest & UI/API Masking | `PASS` | `<model cast/encryption service + test>` |
| Log & Error Telemetry Redaction | `PASS` | `<logger config + redaction test>` |
| Retention Schedule & Auto-Purge | `PASS` | `<scheduled cleanup job + test>` |
| Right to Erasure / Anonymization | `PASS` | `<erasure service + cascade/ledger test>` |
| AI / External Integration Scrubbing | `N/A` | `<prompt scrubber file or N/A reason>` |

## 3. Residual Privacy Risks & Operational Notes
- `<backup retention window, third-party DPA dependencies, or manual steps>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Receive requirements from `requirements-analysis` (`SKILL-02`) and threat boundaries from `threat-modeling-risk-assessment` (`SKILL-13`).
- **Parallel / Sibling Skills**: Coordinate with `application-security-owasp` (`SKILL-10`) for cryptographic and access controls, `ai-security-prompt-injection` (`SKILL-14`) and `ai-provider-integration` (`SKILL-28`) for safe AI data handling, and `database-architecture-integrity` (`SKILL-24`) for deletion/retention schema design.
- **Downstream Skills**: Route log redaction verification to `observability-incident-diagnosis` (`SKILL-34`), backup retention alignment to `backup-recovery-disaster-preparedness` (`SKILL-35`), and release sign-off to `final-quality-gate-release-audit` (`SKILL-38`).

## 12. Source References

- **OWASP ASVS V8 (Data Protection)**: https://owasp.org/www-project-application-security-verification-standard/
- **OWASP Top 10 Privacy Risks Project**: https://owasp.org/www-project-top-10-privacy-risks/
- **NIST Privacy Framework**: https://www.nist.gov/privacy-framework
- **Library Reference**: [../../references/owasp-asvs-top10-reference.md](../../references/owasp-asvs-top10-reference.md)
