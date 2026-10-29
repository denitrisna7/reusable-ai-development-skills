---
name: api-security-webhook-reliability
description: "Secures REST/GraphQL APIs and builds idempotent, HMAC-verified webhooks with rate limiting and retries. Use for APIs and webhooks. Do not use for general outbound SDK calls."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-11"
  category: "Security Engineering"
---

# API Security & Webhook Reliability

This skill defines the engineering standards for building secure, fault-tolerant APIs and reliable webhook integrations. It ensures that every API endpoint and webhook boundary enforces strict authentication, payload validation, cryptographic signature verification, replay protection, idempotency, bounded timeouts, jittered retries, and safe failure handling.

## 1. Activation Conditions

Activate this skill when the task involves any of the following scenarios:
- Designing, implementing, or auditing REST, GraphQL, gRPC, or JSON-RPC API endpoints exposed to clients or partner services.
- Building incoming webhook receivers (e.g., Stripe, GitHub, Midtrans, Xendit, Twilio, Slack, Shopify, or custom partner webhooks).
- Building outgoing webhook dispatchers that deliver signed event notifications to subscriber URLs.
- Implementing API authentication (Bearer tokens, OAuth2 scopes, HMAC signatures, mTLS, API keys), rate limiting, or consistent error envelopes.
- Resolving duplicate webhook processing, race conditions in payment/order callbacks, hanging HTTP requests, or retry storms.

## 2. When Not to Use

Do not use this skill as the primary workflow for the following tasks:
- General web session authentication, HTML XSS protection, or file upload hardening unrelated to APIs/webhooks: route to `application-security-owasp` (`SKILL-10`).
- Consuming third-party SDKs or REST client pagination/data-mapping logic where the focus is client consumption rather than API security and webhook reliability: route to `api-external-service-integration` (`SKILL-27`).
- Managing general background worker queues and cache invalidation unrelated to API/webhook transport: route to `caching-background-jobs` (`SKILL-30`).

## 3. Scope and Objectives

Every API or webhook implementation covered by this skill must address and verify the following core requirements:
- **API Authentication and Scoped Authorization**: Authenticate every non-public API request using scoped tokens or credentials, and enforce resource-level and scope-level authorization per route.
- **Strict Request Validation**: Validate `Content-Type`, payload size limits, query pagination bounds (`limit` / `per_page` caps), and request schemas before executing business logic.
- **Webhook Signature Verification and Replay Protection**: Verify cryptographic signatures (HMAC-SHA256 or asymmetric signatures) against the raw, unparsed request body using constant-time comparison, and reject stale timestamps outside an allowed tolerance window (e.g., 5 minutes).
- **Idempotency and Duplicate Event Handling**: Enforce idempotency keys on state-changing API mutations (`Idempotency-Key` header) and deduplicate incoming webhook events by unique provider `event_id` using atomic database constraints or locks.
- **Explicit Timeouts**: Configure explicit connection, read, and total request timeouts on all outbound HTTP calls and bound inbound webhook processing time by acknowledging quickly (`2xx`) and offloading heavy work when appropriate.
- **Retries with Exponential Backoff and Jitter**: Retry transient network/upstream failures (`408`, `429`, `502`, `503`, `504`) using bounded attempts, exponential backoff, full jitter, and `Retry-After` header compliance; never blindly retry `400`, `401`, `403`, or `422` errors.
- **Rate Limiting and Throttling**: Protect APIs with tiered rate limits (per IP, per API key, per tenant) and return standard rate-limit headers (`Retry-After`, `X-RateLimit-*` or `RateLimit-*`).
- **Consistent Error Responses**: Return deterministic, machine-readable error envelopes (e.g., RFC 9457 Problem Details or project standard JSON error schema) with accurate HTTP status codes and correlation IDs.
- **External Service Failure Handling and Safe Logging**: Isolate upstream outages with circuit breaking or graceful degradation, log delivery/verification diagnostics with request IDs, and redact secrets, signatures, and sensitive payloads.
- **Integration Testing**: Verify valid signatures, tampered signatures, expired timestamps, duplicate event deliveries, timeout handling, and rate-limit enforcement through automated tests.

## 4. Prerequisites and Context Requirements

Before modifying API or webhook handlers, inspect the codebase to establish:
1. **Existing API Conventions**: Check how existing endpoints format responses, validation errors, pagination metadata, and authentication middleware.
2. **Webhook Provider Specifications**: Identify the exact signature header format (e.g., `Stripe-Signature`, `X-Hub-Signature-256`, custom `X-Signature` + `X-Timestamp`), hashing algorithm, raw body parsing rules, and retry schedule.
3. **Persistence & Locking Layer**: Identify the database or cache store (PostgreSQL, MySQL, Redis) used to record processed webhook event IDs and idempotency keys.
4. **Queue Infrastructure**: Determine whether synchronous processing or asynchronous job queuing is used after webhook signature verification.

## 5. Step-by-Step Workflow

Follow this numbered procedure when engineering or auditing APIs and webhooks:

### Step 1: Secure API Authentication, Scopes, and Rate Limits
1. Require authentication middleware on all protected API routes; reject tokens passed in URL query strings (to prevent leakage in access logs and `Referer` headers).
2. Enforce granular token scopes or permissions (e.g., `orders:read` vs `orders:write`) and verify tenant/resource ownership on every request.
3. Configure per-key and per-IP rate limiting on API routes, with stricter limits on authentication, mutation, and search/export endpoints.

### Step 2: Enforce Request Schema, Payload Size, and Pagination Bounds
1. Validate incoming `Content-Type` (e.g., require `application/json`) and enforce a strict request body size limit (e.g., `1MB` default for JSON APIs).
2. Validate request bodies, path parameters, and query strings against strict schemas (rejecting unknown fields on sensitive mutations where appropriate).
3. Cap pagination parameters (`limit = min(requested_limit, MAX_LIMIT)`, e.g., max 100 items per page) to prevent unbounded memory/database exhaustion.

### Step 3: Implement Cryptographic Webhook Signature & Replay Verification
1. **Preserve Raw Request Body**: Access the exact raw byte payload (`req.rawBody`, `$request->getContent()`, `await request.body()`) before any JSON parser re-serializes or mutates whitespace/key order.
2. **Validate Timestamp Freshness**: Extract the event timestamp, verify it is a valid integer/ISO time within the allowed window (default `<= 300` seconds from current UTC time), and reject stale or far-future timestamps.
3. **Compute and Compare HMAC**: Reconstruct the signed payload (typically `${timestamp}.${rawBody}`), compute the HMAC-SHA256 using the webhook signing secret, and compare against the provided signature using a constant-time comparison function.
4. Return `401 Unauthorized` or `400 Bad Request` immediately if the signature or timestamp is invalid, without revealing the expected signature in error messages or logs.

### Step 4: Guarantee Idempotency and Duplicate Event Suppression
1. **Incoming Webhooks**:
   - Create a dedicated `webhook_events` (or `processed_events`) table with a `UNIQUE` index on `(provider, external_event_id)`.
   - Perform an atomic insert (`INSERT ... ON CONFLICT DO NOTHING` or unique constraint catch) inside the transaction or lock before applying side effects.
   - If the event has already been processed (`status = completed`), return `200 OK` immediately so the provider stops retrying without re-executing business logic.
   - Verify out-of-order delivery safety (e.g., `order.paid` arriving before `order.created`, or an older timestamp overwriting a newer state) by checking entity state transitions or upstream sequence versions.
2. **State-Changing API Mutations**:
   - Support an `Idempotency-Key` header on `POST`/`PATCH` endpoints that create payments, orders, or transfers.
   - Hash the request parameters alongside the key; if the same key is reused with different parameters, return `422 Unprocessable Entity` / `409 Conflict`. If reused with identical parameters, return the stored response or status.

### Step 5: Configure Timeouts, Retries, and Outbound Webhook Safety
1. **Timeouts**: Configure explicit connect timeout (e.g., `2-5s`) and response timeout (e.g., `5-15s`) on all HTTP clients. Never leave default infinite timeouts in production code.
2. **Retry Policy**: Wrap transient outbound requests or webhook dispatch jobs with exponential backoff + jitter (e.g., `base * 2^attempt + random_jitter`), honoring upstream `Retry-After` headers and routing permanently failed events to a Dead-Letter Queue (DLQ) or failed-event log.
3. **Outbound Webhook SSRF Protection**: If users can register custom webhook callback URLs, validate `https://` scheme and block private/loopback/link-local IP ranges (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.169.254`, `::1`) at DNS resolution time.

### Step 6: Standardize Error Envelopes and Write Integration Tests
1. Ensure all API errors return a consistent JSON structure (`code`, `message`, `details`/`errors`, `request_id`) without exposing internal database errors or stack traces.
2. Write automated integration tests covering valid payloads, invalid/missing signatures, expired timestamps, duplicate concurrent webhook deliveries, rate-limit `429` responses, and upstream timeout handling.

## 6. Technology-Specific Adaptation Rules

- **PHP (Laravel / Symfony / CodeIgniter)**:
  - Use `$request->getContent()` for raw webhook payloads and `hash_equals(hash_hmac('sha256', $signedPayload, $secret), $signature)` for verification.
  - Use Laravel `Cache::lock()` or database unique constraints with `DB::transaction()` for idempotency, and `Http::timeout(10)->connectTimeout(3)->retry(3, 200, throw: false)` for outbound calls.
- **JavaScript / TypeScript (Node.js / Express / Fastify / Next.js)**:
  - In Express/Fastify, capture raw bytes via `express.raw({ type: 'application/json' })` or a `verify` callback before `express.json()`; in Next.js App Router, use `await request.text()` before `JSON.parse()`.
  - Compare buffers of equal length using `crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b))`. Use `AbortSignal.timeout(ms)` on `fetch()`.
- **Python (FastAPI / Django / Flask)**:
  - Read raw bytes via `await request.body()` (FastAPI) or `request.body` (Django) and verify with `hmac.compare_digest(expected, received)`.
  - Always pass `timeout=httpx.Timeout(10.0, connect=3.0)` or `requests.post(..., timeout=(3.05, 10))` on outbound HTTP calls.
- **Go**:
  - Wrap `r.Body` with `http.MaxBytesReader(w, r.Body, maxBytes)`, read bytes with `io.ReadAll`, and verify with `hmac.Equal(expectedMAC, actualMAC)`.
  - Configure `&http.Client{Timeout: 10 * time.Second}` and pass `context.WithTimeout` per request.
- **Java (Spring Boot) / C# (.NET) / Rust**:
  - Use `MessageDigest.isEqual` (Java), `CryptographicOperations.FixedTimeEquals` (.NET), or `ring::constant_time` / `hmac::Mac::verify_slice` (Rust) on the raw request byte stream.
- **Unknown or Mixed Stacks**:
  - Inspect how the HTTP server buffers request bodies and how database transactions are managed before implementing webhook verification or idempotency middleware.

## 7. Security and Safety Considerations

- **Never Parse Before Verifying**: Parsing complex JSON, XML, or multipart bodies before verifying the webhook signature exposes the server to parser DoS and deserialization attacks.
- **Secret Rotation Support**: Support dual-secret verification (`PRIMARY_SECRET` and `PREVIOUS_SECRET`) during webhook signing secret rotation windows so zero legitimate events are dropped.
- **Safe Logging**: Log webhook `event_id`, `event_type`, verification status, and `request_id`, but never log the signing secret, raw `Authorization` headers, or unredacted PII/card data from payloads.
- **Test Isolation**: Never send test webhooks to live customer URLs or hit live payment gateways during automated tests.

## 8. Verification Criteria

Before marking an API or webhook task complete, verify the following evidence:
- [ ] Raw body HMAC/signature verification uses constant-time comparison and enforces a timestamp replay window.
- [ ] Replaying the exact same webhook `event_id` (or `Idempotency-Key`) twice results in exactly one state mutation and a safe `2xx` idempotent response.
- [ ] Outbound HTTP calls define explicit connect and read timeouts and bounded retry logic.
- [ ] Pagination endpoints enforce a strict maximum page size (`max_limit`), and error responses follow a consistent schema with no stack traces.
- [ ] Automated integration tests pass for valid, tampered, expired, and duplicate webhook/API requests.

## 9. Failure Handling and Edge Cases

- **Downstream Database or Queue Temporarily Unavailable During Webhook Receipt**: If the webhook receiver cannot persist the event to the database or queue, return `500`/`503` (not `200 OK`) so the webhook provider retries delivery later according to its backoff schedule.
- **Permanent Business Validation Failure in Webhook Payload**: If the signature is valid but the payload references a non-existent or permanently invalid business state that retries will never fix, log the anomaly with full correlation context and return `200`/`202` (or route to an internal dead-letter table) to prevent infinite provider retry loops.
- **Out-of-Order Webhook Arrival**: Design handlers to inspect state transitions (e.g., never transition an order from `COMPLETED` back to `PENDING` if a delayed `order.pending` event arrives late) or fetch the authoritative resource state from the provider API when sequence ambiguity occurs.

## 10. Expected Outputs and Reporting Requirements

Report API and webhook engineering work using the following structured format:

```markdown
# API Security & Webhook Reliability Report

## 1. Endpoints & Webhooks Covered
- **Routes / Handlers**: `<list of endpoints, methods, and handler files>`
- **Authentication / Signature Scheme**: `<Bearer OAuth2 / HMAC-SHA256 + Timestamp / API Key>`

## 2. Reliability & Security Controls Matrix
| Control | Status (`PASS`/`FAIL`/`N/A`) | Implementation & Test Evidence |
| :--- | :--- | :--- |
| Auth & Object/Scope Authorization | `PASS` | `<middleware/policy file + test>` |
| Raw Body Signature & Replay Window | `PASS` | `<verifier file:line + tamper/expiry test>` |
| Idempotency & Duplicate Suppression | `PASS` | `<unique constraint/lock + duplicate replay test>` |
| Timeouts & Exponential Backoff Retries | `PASS` | `<client config file:line + timeout test>` |
| Rate Limiting & Pagination Bounds | `PASS` | `<limiter config + max_limit check>` |
| Consistent Error Envelope & Safe Logs | `PASS` | `<exception handler + log redaction verification>` |

## 3. Residual Risks & Operational Notes
- `<secret rotation instructions, DLQ monitoring notes, or provider timeout limits>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Receive security baseline requirements from `application-security-owasp` (`SKILL-10`) and architectural contracts from `adaptive-architecture` (`SKILL-03`).
- **Parallel / Sibling Skills**: Coordinate with `api-external-service-integration` (`SKILL-27`) for external client contracts, `caching-background-jobs` (`SKILL-30`) for async queue workers, and `database-architecture-integrity` (`SKILL-24`) for idempotency table constraints.
- **Downstream Skills**: Route test execution to `backend-testing-tdd` (`SKILL-16`) and `test-data-environment-isolation` (`SKILL-18`), and feed operational readiness into `observability-incident-diagnosis` (`SKILL-34`) and `final-quality-gate-release-audit` (`SKILL-38`).

## 12. Source References

- **OWASP API Security Top 10**: https://owasp.org/API-Security/
- **OWASP ASVS V13 (API and Web Service)**: https://owasp.org/www-project-application-security-verification-standard/
- **RFC 9457 (Problem Details for HTTP APIs)**: https://www.rfc-editor.org/rfc/rfc9457
- **IETF Idempotency-Key HTTP Header Field Draft**: https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/
- **Library Reference**: [../../references/owasp-asvs-top10-reference.md](../../references/owasp-asvs-top10-reference.md)
