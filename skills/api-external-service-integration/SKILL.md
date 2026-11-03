---
name: api-external-service-integration
description: "Mandatory lifecycle skill (SKILL-27). Audits third-party REST/GraphQL APIs for strict contracts, timeouts, backoff retries, and rate limits. Part of the 38-skill quality suite."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-27"
  category: "Data and Integrations"
---

# API and External Service Integration

This skill governs outbound communication with third-party APIs, payment gateways, messaging providers, identity services, and internal microservices (REST, GraphQL, gRPC, SOAP). It ensures that every external network boundary enforces typed contracts, strict response validation, explicit timeouts, bounded retries with jitter, rate-limit compliance, idempotency, failure isolation, and deterministic integration testing.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Integrating a third-party REST, GraphQL, gRPC, or SOAP API or wrapping an external vendor SDK.
- Implementing OAuth2 token exchange/refresh flows, API key signing, mTLS, or HMAC outbound requests.
- Adding resilience mechanisms (timeouts, exponential backoff retries, rate-limit handling, circuit breakers, or fallback paths) to HTTP clients.
- Consuming paginated upstream APIs or writing contract/mock tests for external integrations.

## 2. When Not to Use

Do not use this skill as the primary workflow for:
- Generative AI / LLM provider integrations requiring token budgeting, prompt privacy, and streaming model fallbacks: route to `ai-provider-integration` (`SKILL-28`) (or co-activate both).
- Securing *inbound* API endpoints and verifying incoming webhooks exposed by your own server: route to `api-security-webhook-reliability` (`SKILL-11`).
- Internal database query tuning: route to `query-optimization-performance` (`SKILL-25`).

## 3. Scope and Objectives

Every outbound API or external service integration must cover:
- **Typed API Contracts & Anti-Corruption Layer**: Encapsulate external vendor specifics behind a clean, domain-focused service interface or adapter (`Adaptive Architecture`, `SKILL-03`). Never leak raw third-party DTO shapes or vendor SDK exceptions across the rest of the application.
- **Authentication & Credential Hygiene**: Load API keys, OAuth2 client secrets, and private certificates exclusively from environment/secret storage (`environment-configuration-management`, `SKILL-32`). Implement thread/process-safe OAuth2 access token caching and proactive refresh before expiry, plus automatic single-retry on unexpected `401 Unauthorized` token expiration.
- **Strict Outbound & Inbound Validation**: Validate outbound request parameters before sending, and treat **all** external API responses as untrusted input: validate response status codes, `Content-Type`, and JSON payload schemas before using data.
- **Explicit Connection & Read Timeouts**: Never execute an outbound HTTP/RPC request using an HTTP client with infinite default timeouts. Configure explicit `connect_timeout` (e.g., `2-5s`) and `read/total_timeout` (e.g., `5-15s`) on every client instance.
- **Bounded Retries with Exponential Backoff, Jitter, & Idempotency**:
  - Retry only transient failures: network timeouts, DNS/socket resets, `408 Request Timeout`, `429 Too Many Requests`, and `502 / 503 / 504` gateway errors.
  - Never blindly retry `400`, `401` (unless refreshing an expired token once), `403`, `404`, or `422` client validation errors.
  - For non-idempotent mutations (`POST` payments, orders, transfers, messages), require and pass a deterministic **Idempotency-Key** header so retries never duplicate side effects.
  - Cap retries (e.g., max `3` attempts) using exponential backoff with full jitter:
    $$t_{\text{sleep}} = \text{random}\left(0, \min\left(T_{\text{cap}}, T_{\text{base}} \cdot 2^{\text{attempt}}\right)\right)$$
- **Rate Limit Compliance (`429`)**: Honor upstream `Retry-After` (seconds or HTTP-date), `X-RateLimit-Remaining`, and `X-RateLimit-Reset` headers. Apply client-side rate limiting (token bucket / concurrency limiter) during bulk synchronization.
- **Upstream Pagination Handling**: Consume paginated upstream endpoints (`next_cursor`, `Link: <...>; rel="next"`, `page`/`per_page`) in bounded loops with a hard safety ceiling (`max_pages`) to prevent infinite loops if an upstream API returns a stuck cursor.
- **Version Compatibility & Deprecation**: Pin explicit API version headers or URL paths (e.g., `Stripe-Version`, `X-GitHub-Api-Version`), tolerate unknown fields in responses (`ignoreUnknownProperties`), and monitor `Deprecation` / `Sunset` response headers.
- **Failure Isolation & Graceful Degradation**: Keep external calls strictly outside database transactions (`SKILL-24`), apply circuit breakers or bulkheads so a slow upstream vendor cannot exhaust application worker threads, and provide clear fallback behavior when non-critical services fail.
- **Integration Testing with Deterministic Mocks**: Test success, malformed JSON, `429` rate limit, `503` retry recovery, and timeout paths using deterministic HTTP mocks (`WireMock`, `MSW`, `nock`, `responses`, `respx`, `httptest.Server`, `Http::fake()`) without hitting live third-party endpoints in unit/CI suites (`SKILL-18`).

## 4. Prerequisites and Context Requirements

Before implementing or modifying an external integration, inspect:
1. **Upstream API Specification**: Official OpenAPI/Swagger spec, GraphQL schema, authentication mechanism, rate limits, idempotency support, and error payload format.
2. **Existing HTTP Client & Resilience Stack**: Project HTTP client (`Guzzle`/`Http` facade, `fetch`/`undici`/`axios`/`ky`, `httpx`/`requests`/`aiohttp`, Go `net/http`, Spring `RestClient`/`WebClient`, .NET `IHttpClientFactory`, Rust `reqwest`), connection pool config, and existing adapter directory structure.
3. **Failure Criticality**: Whether the external call is on a synchronous user-facing path (requiring fast fail/fallback) or can be decoupled via a background queue / outbox (`SKILL-30`).

## 5. Step-by-Step Workflow

### Step 1: Define the Domain Adapter Contract and DTO Schema
- [ ] Create a dedicated client/adapter module for the external provider with explicit input and output types/DTOs.
- [ ] Configure schema parsing (`zod`, `Pydantic`, `serde`, Jackson/DataTransferObject) to validate required response fields while ignoring unrecognized extra fields added by upstream minor updates.
- [ ] Map upstream HTTP status codes and vendor error codes into structured domain exceptions (`ExternalServiceTransientError`, `ExternalServiceRateLimitError`, `ExternalServiceValidationError`, `ExternalServiceAuthError`).

### Step 2: Configure the HTTP Client, Connection Pool, and Timeouts
- [ ] Reuse a shared HTTP client / connection pool (`Keep-Alive`) rather than instantiating a fresh TCP/TLS pool per request.
- [ ] Set explicit `connect_timeout` and `timeout` values on the client.
- [ ] Configure TLS verification (`verify: true` / strict CA validation; never disable TLS certificate verification in production code) and SSRF protections if any part of the URL is dynamic.

### Step 3: Implement Idempotency, Retry Policy, and Rate-Limit Handling
- [ ] Attach a deterministic `Idempotency-Key` (derived from the domain entity ID + operation type, never a fresh random UUID per retry attempt!) to all state-changing `POST`/`PATCH` requests.
- [ ] Configure retry middleware limited to `max_attempts = 3` for transient network/5xx/429 errors:
  - If a `429` or `503` response includes a `Retry-After` header, parse it: if the requested wait is short (`<= max_sync_wait`, e.g., `5s`), sleep and retry; if longer, fail fast on synchronous web requests or schedule a delayed background job retry.
  - Otherwise, apply exponential backoff with random jitter.

### Step 4: Harden Upstream Pagination and Transaction Isolation
- [ ] For paginated endpoints, iterate via a generator/stream with a `max_pages` guard and ensure the cursor/offset actually advances on every page.
- [ ] Verify that **no** database transaction (`BEGIN ... COMMIT`) wraps the outbound network call: read/lock state -> commit -> call external API -> record result in a new short transaction.

### Step 5: Write Contract & Failure-Mode Integration Tests
- [ ] Using the stack's HTTP mocking tool, write tests for:
  1. `200 OK` valid contract parsing (and tolerance of extra unknown JSON keys).
  2. `429 Too Many Requests` with `Retry-After` header handling.
  3. Transient `503 Service Unavailable` followed by `200 OK` retry recovery (verifying the same `Idempotency-Key` is sent on both attempts).
  4. Non-retryable `400 / 422` error failing immediately after `1` attempt.
  5. Network read timeout handling.

## 6. Technology-Specific Adaptation Rules

| Stack / Ecosystem | HTTP Client & Resilience Idioms | HTTP Mocking & Testing Tools |
| :--- | :--- | :--- |
| **PHP (Laravel / CodeIgniter / Symfony)** | Use Laravel `Http::baseUrl(...)->timeout(10)->connectTimeout(3)->retry(3, 200, when: ...)` or Guzzle `HandlerStack` with retry middleware. | `Http::fake([...])` + `Http::assertSent(...)`, Guzzle `MockHandler`. |
| **JS / TS (Node.js / Next.js / NestJS)** | Use `fetch` with `AbortSignal.timeout(10_000)` or `undici` / `ky` / `axios-retry`. Validate responses with `zod.safeParse()`. | `msw` (Mock Service Worker), `undici` `MockAgent`, `nock`. |
| **Python (Django / FastAPI / Services)** | Use `httpx.Client` / `AsyncClient(timeout=httpx.Timeout(10.0, connect=3.0))` with `tenacity` (`@retry(stop=stop_after_attempt(3), wait=wait_random_exponential())`) and `Pydantic` response models. | `respx` (for `httpx`), `responses` (for `requests`), `pytest`. |
| **Go** | Never use `http.DefaultClient` (which has `Timeout: 0`). Instantiate `&http.Client{Timeout: 10 * time.Second, Transport: ...}` and pass `context.WithTimeout(ctx, ...)`. Always `defer resp.Body.Close()` and drain/limit body via `io.LimitReader`. | `net/http/httptest.NewServer(...)`. |
| **Java / Spring Boot & C# / .NET** | In Java, use Spring `RestClient` / `WebClient` with `Resilience4j` (`@Retry`, `@CircuitBreaker`, `@RateLimiter`, `@Bulkhead`). In .NET, use `IHttpClientFactory` + `Microsoft.Extensions.Http.Resilience` (Polly v8). | `WireMock`, `MockRestServiceServer` (Spring), custom `HttpMessageHandler` (.NET). |
| **Rust** | Reuse a shared `reqwest::Client::builder().connect_timeout(...).timeout(...).build()?` with `reqwest-middleware` + `reqwest-retry` and `serde::Deserialize`. | `wiremock` crate or `mockito`. |
| **Mobile (Flutter / iOS / Android)** | Use `dio` or `http.Client` with explicit `connectTimeout` / `receiveTimeout`, certificate pinning where required, and token refresh interceptors that queue concurrent `401` requests during refresh. | `http_mock_adapter` / `MockClient` in `flutter test`. |

### HTTP Status Code Retry & Error Mapping Matrix

| Upstream Status / Condition | Retryable? | Required Client Action |
| :--- | :--- | :--- |
| `200 / 201 / 202 / 204` | No | Validate response schema (and check GraphQL/SOAP body-level `errors` array) before returning. |
| `400 / 404 / 409 / 422` | **Never** | Fail immediately (`1` attempt); map to domain validation/conflict/not-found exception and log sanitized error context. |
| `401 Unauthorized` | **At most once** | If using expiring OAuth2/JWT tokens, refresh the cached token under a mutex lock and retry once; otherwise fail and alert. |
| `403 Forbidden` | **Never** | Fail immediately; indicates missing scope, permission, or IP/WAF block. |
| `408 Request Timeout` / Socket Timeout | **Yes (Bounded)** | Retry up to `max_attempts` with exponential backoff + jitter and identical `Idempotency-Key`. |
| `429 Too Many Requests` | **Yes (Bounded)** | Parse `Retry-After` header; wait if within sync budget or reschedule via background job queue (`SKILL-30`). |
| `500` Internal Server Error | **Conditional** | Retry only for idempotent reads (`GET`/`HEAD`) or mutations carrying a verified upstream `Idempotency-Key`. |
| `502 / 503 / 504` Gateway Errors | **Yes (Bounded)** | Retry with exponential backoff + jitter; increment circuit-breaker failure counter. |

## 7. Security and Safety Considerations

- **Server-Side Request Forgery (SSRF) Defense**: If an integration URL, webhook callback, or domain is user-configurable, validate the scheme (`https` only), parse the hostname, resolve DNS, and block private/loopback/link-local/cloud-metadata IP ranges (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.169.254`, `::1`, `fc00::/7`) before connecting (`SKILL-10`).
- **Secret Redaction in Logs & Exceptions**: Never log `Authorization: Bearer ...`, `X-API-Key`, client secrets, or raw PII payloads when logging failed HTTP requests or raising exceptions (`SKILL-12`, `SKILL-34`).
- **Bounded Response Body Reads**: Protect memory against rogue or compromised upstream servers returning multi-gigabyte response streams by capping response body reads (e.g., `io.LimitReader(resp.Body, 10<<20)` or `maxContentLength`).

## 8. Verification Criteria

Before declaring an external integration complete:
1. **Timeout & Retry Evidence**: Code inspection confirms explicit connect/read timeouts, bounded retry count, exponential backoff with jitter, and idempotency keys on mutations.
2. **Contract & Error Mapping Evidence**: Responses are schema-validated before consumption, and upstream errors map cleanly to domain exceptions without leaking raw credentials or crashing callers.
3. **Mocked Integration Test Evidence**: Automated tests verify happy-path parsing, retry on transient `503`/`429`, immediate fail on `4xx`, and timeout handling without calling live production APIs.

## 9. Failure Handling and Edge Cases

- **HTTP `200 OK` With Application-Level Error Payload**: Legacy SOAP, GraphQL (`{ "data": null, "errors": [...] }`), and some REST APIs return HTTP `200 OK` even when the operation failed. Always inspect both HTTP status and payload-level error fields.
- **Retry Storms (Thundering Herd)**: When an upstream provider recovers from a brief outage, synchronized retries across hundreds of workers can immediately knock it down again. Always include random jitter in backoff delays and enforce a circuit breaker or retry budget.
- **Clock Skew on OAuth2 / Signed Requests**: Treat OAuth2 tokens as expired `30-60 seconds` before their advertised `expires_in` timestamp to prevent in-flight expiration due to clock drift.

## 10. Expected Outputs and Reporting Requirements

Report external service integration work using this template:

```markdown
## External Service Integration Report

### 1. Integration Overview
- **Upstream Provider & Protocol**: [e.g., Stripe REST API v2024-06-20 / GraphQL / gRPC]
- **Adapter / Client Location**: [File paths]
- **Authentication Method**: [e.g., OAuth2 Client Credentials with cached token refresh / Bearer API Key]

### 2. Resilience & Security Configuration
| Control | Configured Value / Policy | Status |
| :--- | :--- | :--- |
| Connect / Read Timeout | [e.g., `3s` connect / `10s` read] | [Verified] |
| Retry Policy & Jitter | [e.g., Max 3 attempts on 429/502/503/504 with exponential backoff + jitter] | [Verified] |
| Idempotency Strategy | [e.g., Deterministic `Idempotency-Key: order_{id}_capture`] | [Verified] |
| Response Validation & Error Mapping | [e.g., Zod / Pydantic schema + typed domain exceptions] | [Verified] |
| DB Transaction Isolation & Log Redaction | [External call outside DB tx; auth headers redacted] | [Verified] |

### 3. Integration Test Evidence
- **Test Suite Executed**: [Command & output covering 200 OK, 429 Retry-After, 503 retry, 4xx no-retry, timeout]
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - `adaptive-architecture-planning` (`SKILL-03`): Defines the adapter/port boundary for external services.
  - `environment-configuration-management` (`SKILL-32`): Manages API keys, base URLs, and timeouts via validated config.
- **Downstream / Co-Activated Skills**:
  - `api-security-webhook-reliability` (`SKILL-11`): Handles the inverse flow when the external service sends asynchronous webhooks back to the application.
  - `test-data-environment-isolation` (`SKILL-18`): Ensures test suites use deterministic mocks and never trigger live charges or external messages.
  - `ai-provider-integration` (`SKILL-28`): Specializes these resilience patterns for LLM/generative AI providers.

## 12. Source References

- **AWS Builders' Library (Timeouts, Retries, and Backoff with Jitter)**: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
- **RFC 9110 (HTTP Semantics - Idempotent Methods & Retry-After)**: https://datatracker.ietf.org/doc/html/rfc9110
- **Shared Library Reference (OWASP ASVS Outbound & API Security)**: [../../references/owasp-asvs-top10-reference.md](../../references/owasp-asvs-top10-reference.md)
