---
name: ai-provider-integration
description: "Integrates LLM and generative AI provider APIs with server-side API key protection, structured schema output validation, token and cost budgets, rate-limit handling, streaming timeouts, model fallbacks, PII privacy controls, and deterministic mock testing. Activate when building or reviewing AI/LLM features. Do not use for adversarial prompt injection defense alone (pair with ai-security-prompt-injection)."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-28"
  category: "Data and Integrations"
---

# AI Provider Integration Engineering

This skill governs the architecture, reliability, cost control, privacy, and verification of integrations with Large Language Models (LLMs), multimodal models, embedding services, and generative AI APIs (such as Google Gemini `google-genai` / `@google/genai`, OpenAI, Anthropic, Vertex AI, AWS Bedrock, and local/self-hosted inference servers). It ensures AI features are treated as untrusted, probabilistic, metered external dependencies with strict output validation, budget guardrails, and deterministic fallbacks.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Integrating an LLM, multimodal generation, embedding, reranking, speech-to-text, or text-to-speech API into an application.
- Implementing structured outputs (JSON Schema), function/tool calling, or server-sent event (SSE) / WebSocket streaming responses from an AI model.
- Designing token budgets, per-user/per-tenant cost limits, model routing, or fallback behavior when an AI provider fails or rate-limits requests.
- Auditing AI integrations for exposed API keys, unvalidated model outputs, PII leakage, missing timeouts, or unmocked unit tests.

## 2. When Not to Use

Do not use this skill as the primary workflow for:
- Standard non-AI third-party REST/GraphQL integrations (Stripe, Twilio, GitHub): route to `api-external-service-integration` (`SKILL-27`).
- Adversarial prompt injection, indirect RAG poisoning, and agent tool-execution authorization matrices: co-activate `ai-security-prompt-injection` (`SKILL-14`).
- General code quality or UI anti-slop discipline unrelated to AI API integration: route to `ai-anti-slop-craftsmanship` (`SKILL-05`).

## 3. Scope and Objectives

Every AI provider integration must cover:
- **API Key & Credential Protection**: Call commercial AI provider APIs exclusively from a server-side backend or authenticated edge proxy using server-only environment variables (`GEMINI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`). **Never** bundle raw provider API keys into browser JavaScript (`NEXT_PUBLIC_*`, `VITE_*`), mobile APKs/IPAs, or desktop client binaries (unless using short-lived, scope-restricted ephemeral session tokens explicitly designed for client WebSockets such as Gemini Live ephemeral tokens).
- **Current Official SDK & Model Selection**: Use current official SDKs (e.g., `@google/genai` or `google-genai` for Gemini rather than deprecated legacy packages) and pin explicit, non-deprecated model identifiers configurable via environment settings so model upgrades do not require code rewrites.
- **Structured Responses & Strict Output Validation**:
  - Whenever an AI response drives application logic, database writes, or UI rendering, enforce native **Structured Outputs** (`responseSchema` / `responseJsonSchema` + `responseMimeType: "application/json"`, `zodResponseFormat`, or strict tool schemas) where supported by the provider.
  - Validate every model output against a strict application-side schema (`Zod`, `Pydantic`, JSON Schema, `serde`) before consumption. Treat all LLM text/HTML/Markdown/JSON output as **untrusted user input** (sanitize before rendering to prevent XSS, and never pass raw model output to `eval`, shell commands, or raw SQL).
  - Inspect the model's termination status (`finishReason` / `stop_reason`): handle `MAX_TOKENS` (truncated JSON), `SAFETY` / `CONTENT_FILTER`, and `RECITATION` explicitly before attempting JSON parsing.
- **Token & Cost Controls**:
  - Enforce explicit `maxOutputTokens` / `max_tokens` ceilings on every request.
  - Bound input context length (truncating or summarizing oversized user documents/history and capping uploaded media file sizes/durations).
  - Enforce per-user and per-tenant rate limits and daily/monthly token or spend quotas so a single user or automated loop cannot exhaust the organization's billing cap.
- **Rate Limits (`429`), Timeouts, & Streaming Resilience**:
  - Set explicit connection timeouts, Time-To-First-Token (`TTFT`) timeouts, and total generation deadlines (`AbortSignal` / `context.WithTimeout`).
  - Handle `429 Resource Exhausted / Too Many Requests` and `503 Model Overloaded` using exponential backoff with jitter while respecting `Retry-After` headers.
  - For streaming (`generateContentStream` / SSE), handle client disconnects cleanly by aborting the upstream provider stream immediately so tokens are not wasted after the user closes the tab.
- **Fallback Behavior & Provider Failure Isolation**:
  - Define a clear fallback chain: e.g., retry transient failure once -> fall back to a secondary/lighter model (`pro` -> `flash`) or secondary region/provider -> degrade gracefully to a deterministic non-AI workflow or clear user-facing retry state (`R-27`).
  - Keep slow AI calls outside database transactions (`SKILL-24`) so DB connections are never held during multi-second LLM inference.
- **Privacy & Data Minimization (`SKILL-12`)**:
  - Redact or omit unnecessary PII, payment details, passwords, and secrets before constructing prompts or embedding payloads.
  - Document and configure provider data-retention and training opt-out policies (zero-data-retention endpoints or enterprise terms where required).
- **Observability Without Prompt Leakage (`SKILL-34`)**:
  - Record structured telemetry for every AI call: `model`, `provider`, `latency_ms`, `time_to_first_token_ms`, `input_tokens`, `output_tokens`, `cached_tokens`, `finish_reason`, `status_code`, and `correlation_id`.
  - Redact raw user prompts and completions in default production logs unless explicit privacy-compliant prompt auditing is enabled.
- **Testing with Deterministic Mocks & Controlled Live Tests**:
  - Run unit and CI tests against deterministic mock responses covering valid structured output, truncated `MAX_TOKENS`, safety refusal, malformed JSON, and `429`/`503` errors.
  - Gate live provider integration tests behind an explicit opt-in flag (`RUN_LIVE_AI_TESTS=true`) with tiny token limits (`maxOutputTokens: 32`) to prevent runaway CI costs.

## 4. Prerequisites and Context Requirements

Before implementing or modifying an AI integration, inspect:
1. **Provider & SDK**: Which AI provider(s) and SDK versions are installed in `package.json`, `pyproject.toml`, `composer.json`, `go.mod`, or `Cargo.toml`.
2. **Task Modality & Latency Profile**: Whether the call is synchronous (chat/structured extraction `< 5s`), streaming (SSE/WebSocket), or long-running batch/background processing (deep research, video/audio generation, bulk embeddings).
3. **Security & Privacy Boundaries**: Read [../../references/owasp-asvs-top10-reference.md](../../references/owasp-asvs-top10-reference.md) and coordinate with `ai-security-prompt-injection` (`SKILL-14`) and `privacy-data-protection` (`SKILL-12`).

## 5. Step-by-Step Workflow

### Step 1: Verify Server-Side Credential Isolation and SDK Setup
- [ ] Audit environment variable usage to ensure API keys are loaded only in server-side modules and are absent from client-side env prefixes (`NEXT_PUBLIC_`, `VITE_`, `PUBLIC_`, `REACT_APP_`).
- [ ] Centralize AI client initialization in a dedicated server-side gateway/service wrapper with configurable model names (`AI_PRIMARY_MODEL`, `AI_FALLBACK_MODEL`) and timeouts.
- [ ] If integrating Google Gemini, verify the project uses the current Google Gen AI SDK (`@google/genai` in TypeScript/JavaScript or `google-genai` in Python) and current model identifiers (`gemini-2.5-flash`, `gemini-2.5-pro`, etc.).

### Step 2: Define Input Budgets and Privacy Filters
- [ ] Validate and bound user inputs before building the prompt (e.g., max character/token count, allowed MIME types and file size limits for multimodal uploads).
- [ ] Strip or mask PII and sensitive internal fields that the model does not need to complete the task.
- [ ] Check user/tenant rate-limit and quota allowance before dispatching the upstream API call.

### Step 3: Enforce Structured Outputs, Finish-Reason Checks, and Output Validation
- [ ] Define the expected response contract using a strict schema (`Zod`, `Pydantic`, or OpenAPI/JSON Schema) and pass it to the provider's structured output configuration.
- [ ] When the response returns:
  1. Check `finishReason` / `stop_reason` first (handle safety blocks, refusals, or `MAX_TOKENS` truncation gracefully).
  2. Parse and validate the payload using the application's schema validator (`safeParse` / `model_validate_json`).
  3. If validation fails, trigger a bounded repair/fallback path or return a safe domain error rather than crashing with an unhandled `SyntaxError`.

### Step 4: Implement Timeouts, Cancellation, Retries, and Model Fallbacks
- [ ] Attach an explicit timeout and propagate request cancellation (`req.signal` / `ctx.Done()`) into the AI SDK call so aborted client requests cancel in-flight generation.
- [ ] Configure retries (`max 2-3 attempts`) with exponential backoff + jitter for `429` and `503` errors, and fall back to the configured secondary model or deterministic fallback if the primary model remains unavailable.
- [ ] Ensure all database writes happen in a short transaction *after* the AI response is received and validated.

### Step 5: Instrument Telemetry and Write Deterministic Tests
- [ ] Emit structured metrics/logs capturing token usage (`promptTokenCount`, `candidatesTokenCount`), latency, model used, and finish reason.
- [ ] Write automated unit/integration tests with mocked provider responses for:
  - Valid structured response.
  - Truncated response (`finishReason: "MAX_TOKENS"`) or invalid JSON schema violation.
  - Safety refusal (`finishReason: "SAFETY"`).
  - Provider `429` rate limit and `503` fallback to secondary model or graceful error state.

## 6. Technology-Specific Adaptation Rules

| Stack / Ecosystem | AI SDK & Structured Output Idioms | Streaming, Timeout & Testing Patterns |
| :--- | :--- | :--- |
| **TypeScript / Node.js / Next.js** | Use `@google/genai` (`GoogleGenAI`), `openai`, `@anthropic-ai/sdk`, or Vercel `ai` SDK on the server. Validate structured JSON with `zod`. | Pass `AbortSignal.timeout(ms)` or `req.signal`; stream via `ReadableStream` / SSE; mock client methods in `vitest`/`jest` or via `msw`. |
| **Python (FastAPI / Django / Workers)** | Use `google-genai` (`from google import genai`), `openai`, or `anthropic` with `pydantic.BaseModel` as the structured `response_schema`. | Use `asyncio.timeout(seconds)` for async calls; stream via `StreamingResponse`; mock SDK client or HTTP transport (`respx` / `unittest.mock.AsyncMock`) in `pytest`. |
| **PHP (Laravel / Symfony)** | Use official/community server-side HTTP clients or Laravel `Http::timeout(30)` against provider REST endpoints with JSON Schema response formatting and DTO validation. | Offload slow generation to queued jobs (`ShouldQueue`) and broadcast progress via Reverb/SSE; test with `Http::fake()`. |
| **Go / Java / C# / Rust** | Use `google.golang.org/genai` (Go), Spring AI / LangChain4j (Java), `Microsoft.Extensions.AI` (.NET), or `async-openai` / `reqwest` (Rust) with strongly typed struct deserialization. | Propagate `context.Context` / `CancellationToken` for timeouts and client disconnects; test via injected provider interface mocks. |
| **Mobile (Flutter / iOS / Android)** | Route AI requests through your own authenticated backend API (or Firebase AI Logic with App Check + per-user rate limits) rather than embedding raw provider keys in client binaries. | Handle offline/timeout states in UI (`R-27`) and cancel in-flight streams when widgets dispose. |

## 7. Security and Safety Considerations

- **Never Expose Raw Provider Keys in Client Code**: Any API key shipped in web frontend bundles or mobile app binaries can be extracted in seconds and abused to rack up thousands of dollars in API charges. Enforce a strict backend proxy boundary.
- **Untrusted Output Handling (XSS, SSRF, RCE, SQLi)**: Never render LLM-generated HTML without DOMPurify/allowlist sanitization; never execute LLM-generated SQL or shell commands directly; and require explicit human confirmation and server-side authorization checks before executing high-impact AI tool calls (`ai-security-prompt-injection`, `SKILL-14`).
- **Billing Denial-of-Wallet Defense**: Always combine authentication, per-user/IP rate limiting, input length caps, and `maxOutputTokens` on every endpoint that triggers a paid AI model call.

## 8. Verification Criteria

Before declaring an AI provider integration complete:
1. **Credential Isolation Proof**: Grep/inspection confirms zero AI provider keys exist in client-exposed source files or public env variables.
2. **Schema & Finish-Reason Proof**: Model outputs are validated against an explicit schema after checking `finishReason`, with graceful handling for refusals and truncation.
3. **Budget, Timeout & Fallback Proof**: Input size caps, `maxOutputTokens`, request timeouts, cancellation propagation, and fallback behavior are implemented and verified.
4. **Mocked Test Suite Proof**: Automated tests pass in CI without requiring live API keys or incurring real token spend.

## 9. Failure Handling and Edge Cases

- **Truncated JSON (`finishReason == "MAX_TOKENS"`)**: When a model hits `maxOutputTokens` mid-JSON, `JSON.parse()` will throw an unexpected end-of-input error. Always check `finishReason` before parsing so the error handler reports token budget truncation rather than a generic parser crash.
- **Hallucinated Entity IDs or URLs in Structured Output**: Even when JSON syntax is valid, an LLM can hallucinate a `user_id`, `product_id`, or URL. Always verify any returned IDs or URLs against the database or allowlist before acting on them (`C-5`).
- **Long-Running Multimodal / Video / Batch Tasks**: Operations taking `> 15-30s` (such as video generation or large document extraction) will time out standard HTTP gateways; use asynchronous background polling/webhook jobs (`SKILL-30`).

## 10. Expected Outputs and Reporting Requirements

Report AI provider integration work using this template:

```markdown
## AI Provider Integration Report

### 1. Architecture & Model Configuration
- **Provider & SDK**: [e.g., Google Gemini via `@google/genai` / Python `google-genai`]
- **Model Routing**: [Primary: e.g., `gemini-2.5-flash` | Fallback: Deterministic / Secondary model]
- **Credential Boundary**: [Server-side env var only; verified zero client bundle exposure]

### 2. Guardrails, Budgets & Validation
| Guardrail | Implementation Details | Status |
| :--- | :--- | :--- |
| Input / Context Budget | [Max chars / file size / rate limit per user] | [Verified] |
| Output Token Ceiling (`maxOutputTokens`) | [Configured limit] | [Verified] |
| Structured Output & Schema Validation | [JSON Schema + Zod/Pydantic validation + `finishReason` check] | [Verified] |
| Timeout, Cancellation & Retry Policy | [Connect/TTFT/Total timeout + abort propagation + 429 backoff] | [Verified] |
| Privacy & Telemetry Redaction | [PII minimization + token/latency logging without raw prompt leaks] | [Verified] |

### 3. Verification Evidence
- **Deterministic Mock Tests**: [Command & output covering valid output, MAX_TOKENS truncation, SAFETY block, and 429/503 fallback]
- **Live Integration Test Status**: [Executed with bounded tokens / Skipped in offline CI (`NOT TESTED`)]
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - `api-external-service-integration` (`SKILL-27`): Supplies base HTTP timeout, retry, and circuit-breaker primitives.
  - `environment-configuration-management` (`SKILL-32`): Secures provider API keys and model configuration variables.
- **Downstream / Co-Activated Skills**:
  - `ai-security-prompt-injection` (`SKILL-14`): Mandatory companion skill whenever untrusted user input, RAG documents, or tool/function calls are passed to the model.
  - `privacy-data-protection` (`SKILL-12`): Governs PII redaction and data-retention compliance before sending user data to external AI APIs.
  - `observability-incident-diagnosis` (`SKILL-34`): Tracks token consumption, latency percentiles, and provider error rates.

## 12. Source References

- **Google Gemini API & SDK Documentation (`google-genai` / `@google/genai`)**: https://ai.google.dev/gemini-api/docs
- **OWASP Top 10 for Large Language Model Applications**: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- **Shared Library Reference (OWASP ASVS & AI Security)**: [../../references/owasp-asvs-top10-reference.md](../../references/owasp-asvs-top10-reference.md)
