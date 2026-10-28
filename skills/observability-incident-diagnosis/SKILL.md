---
name: observability-incident-diagnosis
description: Implements structured logging, RED/USE metrics, distributed tracing, health and readiness endpoints, correlation IDs, sensitive log redaction, and incident root-cause analysis. Activate when adding telemetry, designing alerts, or diagnosing production outages and errors. Do not use for CPU/memory optimization without incident telemetry.
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-34"
  category: "Performance, Operations, and Deployment"
---

# Observability & Incident Diagnosis

This skill governs application telemetry, operational monitoring, and systematic incident diagnosis. It enforces structured context-rich logging with strict secret/PII redaction, RED and USE metric instrumentation, correlation ID propagation across service and queue boundaries, accurate liveness/readiness health endpoints, symptom-based alerting, and blameless Root Cause Analysis (RCA).

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Implementing or refactoring application logging into structured JSON/key-value logs with request correlation IDs.
- Instrumenting application metrics (Prometheus, OpenTelemetry, StatsD, CloudWatch) or distributed tracing spans.
- Integrating error tracking and crash monitoring (Sentry, Bugsnag, Rollbar, Datadog, OpenTelemetry collectors).
- Building `/health` (liveness) and `/ready` (readiness) endpoints that verify downstream dependencies safely.
- Diagnosing live or simulated production incidents, reconstructing failure timelines, and writing postmortems / Root Cause Analyses (RCA).
- Auditing logs to redact leaked passwords, bearer tokens, API keys, payment data, or Personal Identifiable Information (PII).

## 2. When Not to Use

Do not activate this skill when the task is strictly limited to:
- Diagnosing failing unit or integration test assertions in local development or CI (route to `test-reporting-failure-diagnosis`, `SKILL-19`).
- Micro-benchmarking CPU/memory hotspots or optimizing SQL queries once the bottleneck is already known (route to `performance-profiling-optimization`, `SKILL-29`, or `query-optimization-performance`, `SKILL-25`).
- Designing database backup archives and disaster recovery storage (route to `backup-recovery-disaster-preparedness`, `SKILL-35`).

## 3. Scope and Objectives

Every observability or incident diagnosis engagement under this skill must cover:
- **Structured Logging**: Emitting machine-parseable logs (JSON in production, readable formatted logs in local dev) enriched with timestamp (`ISO-8601 UTC`), severity level, service name, environment, `request_id`/`trace_id`, `user_id`/`tenant_id` (when authenticated), and event code.
- **Metrics (RED & USE Methods)**:
  - **RED (Request-driven services)**: Request **R**ate, **E**rror rate (HTTP `5xx` vs `4xx`), and **D**uration histograms (p50, p95, p99).
  - **USE (Resources/Infrastructure)**: **U**tilization, **S**aturation (queue depth, connection pool wait count), and **E**rrors.
- **Distributed Tracing**: Propagating W3C Trace Context (`traceparent`, `tracestate`) across HTTP calls, gRPC requests, and background queue messages when multi-service or async workflows exist.
- **Error Monitoring**: Capturing unhandled exceptions with stack traces, release version tags (`release_sha`), breadcrumbs, and user/tenant impact counts.
- **Health & Readiness Checks**: Distinguishing lightweight process liveness (`/healthz`) from dependency readiness (`/readyz` checking DB, cache, and migrations with bounded timeouts).
- **Actionable Alerting**: Designing symptom-based alerts tied to user pain (high error rate, high p95 latency, queue stall) with runbook links rather than noisy threshold spam.
- **Correlation Identifiers**: Generating or accepting a validated `X-Request-ID` / `X-Correlation-ID` at the ingress edge, propagating it through all logs and downstream calls, and returning it in HTTP responses and error payloads.
- **Sensitive Log Redaction**: Automatically scrubbing credentials (`password`, `secret`, `token`, `authorization`, `cookie`, `api_key`, `credit_card`, `ssn`, `cvv`) before logs leave the process.
- **Incident Diagnosis & Root Cause Analysis**: Executing a structured triage workflow (Mitigate -> Isolate -> Diagnose -> Remediate -> Prevent) and producing a 5-Whys RCA with corrective action items.

## 4. Prerequisites and Context Requirements

Before implementing telemetry or diagnosing an incident, determine:
1. **Runtime & Log Sink**: Does the application log to `stdout`/`stderr` (12-Factor container standard) or rotating files, and what collector/APM ingests the stream?
2. **Compliance & Privacy Constraints**: Which fields constitute regulated data (GDPR PII, HIPAA PHI, PCI cardholder data) requiring masking or hashing in logs?
3. **Incident Context (during outages)**: What changed recently (deployments, config flips, migrations, upstream API outages, traffic spikes), when did symptoms start, and what is the user blast radius?

## 5. Step-by-Step Workflow

### Step 1: Implement Correlation ID Middleware & Context Propagation
- [ ] At the HTTP/API entrypoint, read incoming `X-Request-ID` (validate length/charset to prevent log injection) or generate a fresh UUIDv4/ULID if absent.
- [ ] Bind `request_id`, `trace_id`, `route`, `method`, and authenticated `actor_id` / `tenant_id` into request-scoped logging context (`AsyncLocalStorage` in Node, `contextvars` in Python, `Context` in Go, `Log::shareContext` in Laravel, MDC in Java).
- [ ] Attach `X-Request-ID` to the outgoing HTTP response headers and include it in structured API error responses so users can report exact failing request IDs.
- [ ] Pass `correlation_id` into dispatched background job payloads so worker logs link directly back to the originating HTTP request.

### Step 2: Configure Structured Logging & Automated Secret Redaction
- [ ] Replace ad-hoc `console.log`, `print()`, `var_dump()`, or `fmt.Println()` debugging statements with a leveled structured logger (`debug`, `info`, `warn`, `error`, `fatal`).
- [ ] Configure a centralized redaction processor/formatter that recursively masks sensitive keys (`password`, `password_confirmation`, `token`, `access_token`, `refresh_token`, `secret`, `api_key`, `authorization`, `cookie`, `set-cookie`, `card_number`, `cvv`, `ssn`) with `"[REDACTED]"`.
- [ ] Standardize core log fields across services:
  - `timestamp` (UTC ISO-8601)
  - `level` (`debug` | `info` | `warn` | `error` | `fatal`)
  - `service` and `environment`
  - `request_id` / `trace_id` / `span_id`
  - `event` (machine-readable slug, e.g., `payment.webhook.failed`)
  - `duration_ms` and `http_status` (for request/operation completion logs)
- [ ] Ensure HTTP `4xx` client validation errors log at `info` or `warn` (never `error`/`fatal`), reserving `error` for genuine system failures (`5xx`, unhandled exceptions, dependency timeouts).

### Step 3: Instrument Health Endpoints, Metrics, and Tracing
- [ ] Create two distinct operational endpoints:
  - **Liveness (`GET /health` or `/healthz`)**: Fast (`< 10 ms`) check confirming the application process and event loop are responsive. Never fail liveness due to a temporary downstream database hiccup (which would cause Kubernetes/orchestrators to restart healthy app containers in a cascading loop).
  - **Readiness (`GET /ready` or `/readyz`)**: Verifies database connectivity (`SELECT 1` with a strict `1-2s` timeout) and critical cache/broker availability. Returns `200 OK` when ready to receive traffic and `503 Service Unavailable` when dependencies are down.
- [ ] Expose RED metrics (request count by route/status, latency histogram buckets) and USE saturation metrics (DB connection pool active/idle/waiting counts, memory usage, queue depth).
- [ ] Propagate W3C `traceparent` headers across outbound HTTP requests and message broker headers so distributed traces connect across services.

### Step 4: Incident Diagnosis & Root Cause Analysis Workflow
When diagnosing an active bug or production incident:
1. **Stabilize First**: Assess blast radius and check whether an immediate rollback, feature flag disable, or traffic rate limit is needed to stop user impact.
2. **Correlate Timeline with Changes**: Compare the exact timestamp of error/latency onset against recent deployments, config changes, database migration locks, expired TLS certificates, or third-party provider outages.
3. **Trace by Correlation ID**: Filter structured logs and distributed traces by failing `request_id` or exception class to locate the exact failing line, SQL query, or upstream timeout.
4. **Formulate & Falsify Hypotheses**: Test one hypothesis at a time against log/metric evidence rather than applying speculative code patches blindly.
5. **Conduct 5-Whys Root Cause Analysis**: Look beyond the proximate trigger ("null pointer in handler") to the systemic gap ("missing schema validation and missing integration test for empty webhook payload").
6. **Implement Regression Test & Alert**: Write an automated test reproducing the exact failure condition and add a telemetry guard.

### Step 5: Configure Actionable Alerting and Incident Runbooks
- [ ] Define symptom-based alerts tied directly to user experience and SLO burn rates:
  - High HTTP `5xx` error rate (`> 1%` over 5 minutes).
  - Elevated endpoint latency (p95 exceeding SLA threshold over 10 minutes).
  - Queue saturation (oldest pending job age exceeding threshold or Dead-Letter Queue non-empty).
  - Readiness probe failures across multiple instances.
- [ ] Link every alert rule to a concrete diagnostic runbook entry.

## 6. Technology-Specific Adaptation Rules

Adapt logging, metrics, tracing, and health check implementations to the project's actual stack. Never force PHPStan, Pint, Pest, shadcn/ui, or Playwright where inapplicable:
- **PHP (Laravel / Symfony / CodeIgniter)**: Use Monolog JSON formatters in production (`LOG_STACK` / `stderr` channel), `Log::shareContext(['request_id' => ...])`, Laravel `/up` health route or custom `/ready` check, and Telescope/Sentry/Nightwatch with sensitive header/input scrubbing configured in `bootstrap/app.php`. In CodeIgniter 4, extend `CodeIgniter\Log\Logger` or custom filters to inject `X-Request-ID` and redact sensitive POST fields.
- **JavaScript / TypeScript (Node.js / Next.js / React / Vue / NestJS)**: Use `pino` or `winston` with built-in redaction (`redact: ['req.headers.authorization', 'req.headers.cookie', '*.password', '*.token', '*.secret']`). Use Node `AsyncLocalStorage` for automatic request ID propagation across async calls and OpenTelemetry SDK (`@opentelemetry/sdk-node`) for distributed tracing.
- **Python (Django / FastAPI / Flask)**: Use `structlog` or `python-json-logger` paired with `contextvars` (`structlog.contextvars.bind_contextvars(request_id=...)`) for correlation IDs. Configure a redaction processor in the logging pipeline that scrubs sensitive keys before JSON serialization.
- **Go**: Use standard library `log/slog` (`slog.NewJSONHandler(os.Stdout, nil)`), propagate request metadata via `context.Context`, and implement `slog.LogValuer` on structs containing credentials so sensitive fields automatically render as `[REDACTED]`.
- **Java / Spring Boot**: Use SLF4J + Logback (`logstash-logback-encoder` for JSON), populate `MDC.put("requestId", ...)` in a `OncePerRequestFilter` (clearing `MDC.clear()` in `finally`), and configure Spring Boot Actuator `/actuator/health/liveness` and `/actuator/health/readiness` with Micrometer + OpenTelemetry.
- **Rust**: Use the `tracing` and `tracing-subscriber` crates (`fmt().json()`, `#[tracing::instrument(skip(password, token, secret))]`) with `tower_http::trace::TraceLayer` and `secrecy::SecretString` to prevent accidental `Debug`/`Display` printing of secrets.
- **C# / .NET**: Use `ILogger<T>` with structured message templates (`_logger.LogInformation("Order {OrderId} processed", orderId)`), `Serilog` or OpenTelemetry logging with destructuring redaction policies, and ASP.NET Core `MapHealthChecks` separating `"live"` and `"ready"` tags.
- **Mobile / Flutter**: Use `PlatformDispatcher.instance.onError` and `FlutterError.onError` wired to Crashlytics/Sentry with PII scrubbing enabled, breadcrumb logging for navigation/network events, and correlation headers (`X-Request-ID`) attached to outbound API client requests.
- **Unknown or Mixed Stacks**: Emit single-line JSON logs to `stdout`/`stderr` containing `timestamp`, `level`, `request_id`, `message`, and redacted `context`, and expose `/health` and `/ready` HTTP routes.

## 7. Security and Safety Considerations

- **Prevent Log Injection (CRLF / ANSI Escape Injection)**: Sanitize or JSON-encode all user-controlled strings before logging so attackers cannot forge fake log lines via newline characters (`\r\n`) or terminal escape sequences.
- **Never Expose Stack Traces or Internal Versions on Public `/health`**: Public health responses should return minimal status (`{"status":"ok"}`); detailed component diagnostics belong behind internal cluster networks or authenticated operator tokens.
- **Bound Log Volume on Hot Loops**: Rate-limit or sample repetitive error logs inside high-throughput loops so a downstream outage does not fill disk volumes (`ENOSPC`) or exhaust log ingestion quotas.
- **GDPR / Privacy Compliance in Telemetry**: Avoid logging raw user email addresses, phone numbers, IP addresses, or full request bodies unless explicitly required for security audit trails with defined retention limits (`SKILL-12`).

## 8. Verification Criteria

Before completing observability or incident diagnosis work, verify:
1. **Redaction Tested**: Attempting to log an object containing `password`, `authorization`, `cookie`, `secret`, or `token` produces `[REDACTED]` in the output stream.
2. **Correlation ID End-to-End**: A request sent with `X-Request-ID: test-corr-123` echoes `X-Request-ID: test-corr-123` in the response header and includes `"request_id":"test-corr-123"` in emitted log lines.
3. **Liveness vs. Readiness Separation**: `/health` stays `200` when the process is alive, while `/ready` returns `503` if a required database connection fails.
4. **RCA Completeness**: For incident diagnosis tasks, the root cause is traced to code/config level and paired with a regression test.

## 9. Failure Handling and Edge Cases

- **Telemetry Sink Outage**: Logging and metric exporters must never block or crash the main application thread if the external log/APM collector becomes unreachable (use non-blocking buffered queues with drop-on-full backpressure).
- **Circular References in Logged Objects**: Configure JSON log serializers to handle circular object references and `BigInt` values safely without throwing serialization exceptions inside `catch` blocks.
- **Health Check Cascading Load**: Cache expensive downstream readiness checks for `1-3 seconds` or keep readiness queries ultra-light (`SELECT 1`) so aggressive load-balancer polling does not overload the database.

## 10. Expected Outputs and Reporting Requirements

Deliver a structured **Observability & Incident Diagnosis Report**:

```markdown
# Observability & Incident Diagnosis Report

## 1. Telemetry & Health Architecture
- **Structured Logger & Redaction**: `<Logger library, JSON schema, redacted field patterns>`
- **Correlation ID Propagation**: `<Header name, middleware path, async job propagation>`
- **Health Endpoints**:
  - `Liveness (/healthz)`: `<Behavior & response code>`
  - `Readiness (/readyz)`: `<Checked dependencies & timeout>`
- **Key Metrics & Alerts (RED/USE)**: `<Instrumented counters, histograms, and alert thresholds>`

## 2. Incident Root Cause Analysis (When Diagnosing an Incident)
- **Incident Summary & Impact**: `<Symptom, start/end time, affected routes/users>`
- **Root Cause (5 Whys)**: `<Chain from symptom to underlying systemic cause>`
- **Remediation & Prevention**: `<Code fix, regression test added, alert/monitor updated>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Receives background worker telemetry hooks from `caching-background-jobs` (`SKILL-30`) and external API error events from `api-external-service-integration` (`SKILL-27`).
- **Downstream Skills**: Supplies `/health` and `/ready` verification and monitoring evidence to `deployment-readiness` (`SKILL-33`) and `final-quality-gate` (`SKILL-38`), and operational runbooks to `documentation-developer-handoff` (`SKILL-37`).

## 12. Source References

- **OpenTelemetry Official Specification**: https://opentelemetry.io/docs/specs/otel/
- **OWASP Logging Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- **Google SRE Book (Monitoring Distributed Systems & Postmortem Culture)**: https://sre.google/sre-book/monitoring-distributed-systems/
