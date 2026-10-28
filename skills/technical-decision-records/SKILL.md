---
name: technical-decision-records
description: "Authors and maintains architecture documentation, Architecture Decision Records (ADRs), setup guides, environment configurations, dependency docs, API contracts, and operational runbooks aligned with actual code. Activate when recording technical decisions, updating system docs, or documenting APIs and operations. Do not use for making initial architectural choices or writing inline code comments."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-04"
  category: "Core Discovery and Planning"
---

# Documentation & Technical Decision Records

This skill governs the creation, verification, and maintenance of high-signal technical documentation across a software repository, including Architecture Decision Records (ADRs), developer setup instructions, environment variable templates, dependency rationales, API contracts, and operational runbooks. It enforces strict alignment between documentation and the actual codebase implementation, eliminating speculative claims, stale commands, and AI-generated filler prose.

## 1. Activation Conditions

Activate this skill under any of the following scenarios:
- Recording a significant architectural, database, security, or dependency decision in an Architecture Decision Record (ADR).
- Creating or updating `README.md`, developer onboarding guides, local setup instructions, or `.env.example` documentation after adding or modifying features, services, or tooling.
- Documenting HTTP/REST, GraphQL, gRPC, CLI, or webhook API contracts (including OpenAPI/Swagger specs or markdown endpoint references).
- Authoring operational runbooks covering deployment steps, health checks, background workers, backup/restore procedures, or incident rollback steps.
- Auditing existing project documentation to fix drift where documented commands, paths, or endpoints no longer match the actual code.

## 2. When Not to Use

Do not use this skill in the following situations:
- Evaluating architectural options before a decision has been analyzed; run [`adaptive-architecture`](../adaptive-architecture/SKILL.md) (`SKILL-03`) first.
- Cleaning up or writing inline source code comments (`//`, `/* */`, docstrings); route to [`ai-anti-slop`](../ai-anti-slop/SKILL.md) (`SKILL-05`, Code Comment Hygiene).
- Gathering initial product requirements and user acceptance criteria; route to [`requirements-analysis`](../requirements-analysis/SKILL.md) (`SKILL-02`).
- Creating unrequested markdown summary files after every minor code edit when the user did not ask for standalone documentation.

## 3. Scope and Objectives

Every documentation task executed under this skill must cover the applicable subset of these eight core responsibilities:
- **Architecture documentation**: Clear system topology overviews, module boundary maps, data flow summaries, and directory responsibilities grounded in real repository paths.
- **Setup instructions**: Reproducible step-by-step prerequisites, dependency installation commands, database initialization/migration steps, and local development server startup commands.
- **Environment configuration**: Complete documentation of required and optional environment variables in `.env.example` (or stack equivalent) with expected types, safe defaults, and where each variable is consumed.
- **Dependency documentation**: Rationale for non-obvious third-party libraries, system binary requirements (e.g., `ffmpeg`, `redis`, `wkhtmltopdf`, PHP extensions), and version constraints.
- **API contracts**: Accurate endpoint paths, HTTP methods, authentication headers, request parameter/body schemas, response payloads, status codes, error formats, and idempotency/rate-limit headers.
- **Technical decision records (ADRs)**: Concise, immutable or status-tracked records (`Proposed`, `Accepted`, `Deprecated`, `Superseded`) capturing context, decision drivers, considered alternatives, chosen solution, and trade-offs.
- **Operational documentation**: Production build commands, queue worker/scheduler supervision requirements, health-check endpoints, monitoring alerts, and rollback procedures.
- **Keeping documentation aligned with actual implementation**: Verifying every command, file path, config key, and endpoint against the live codebase before saving documentation.

## 4. Prerequisites and Context Requirements

- Direct read access to the repository's manifests, configuration files, route definitions, and existing `docs/` or `README.md` structure.
- Verified stack details from [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`) and architectural rationale from [`adaptive-architecture`](../adaptive-architecture/SKILL.md) (`SKILL-03`) when documenting new designs.
- Familiarity with the copywriting and evidence rules in [`ai-anti-slop`](../ai-anti-slop/SKILL.md) (`SKILL-05`): no em-dash (`—`) overuse (`R-02`), no marketing buzzwords (`R-16`), and no unverified claims (`C-5`, `R-36`).

## 5. Step-by-Step Workflow

Follow this procedure whenever authoring or updating technical documentation:

### Step 1: Audit Existing Documentation Structure and Drift
1. Inspect existing documentation (`README.md`, `docs/`, `docs/adr/`, `openapi.yaml`, `.env.example`) to match the project's established folder hierarchy and file naming convention (e.g., `docs/adr/0001-record-architecture-decisions.md`).
2. Cross-check existing documented commands and file paths against the live manifest files (`package.json`, `composer.json`, `Makefile`, `pyproject.toml`, `Cargo.toml`) to identify stale or broken instructions.

### Step 2: Verify Every Technical Fact in Source Code
1. **Commands**: Confirm that every `npm run`, `pnpm`, `composer`, `php artisan`, `php spark`, `pytest`, `go`, or `cargo` command actually exists in the project's manifest or CLI binary.
2. **Environment Variables**: Grep the codebase (`env(`, `getenv(`, `process.env.`, `os.environ`, `os.Getenv`) to ensure every new or modified configuration key is reflected in `.env.example` and configuration docs with safe placeholder values.
3. **API Endpoints**: Inspect route registrations, request validators, and response serializers/resources so documented field names, types, and status codes match the actual implementation 1:1.

### Step 3: Author or Update Architecture Decision Records (ADRs)
1. When a significant technical choice is made (e.g., selecting a database locking strategy, introducing a queue worker, changing auth token storage, or adding a core dependency), create a numbered ADR.
2. Include five mandatory ADR sections:
   - **Status & Date**: `Accepted` (or `Proposed` / `Superseded by ADR-XXXX`) and ISO date.
   - **Context & Problem Statement**: The concrete technical requirement, constraint, or failure that forced a decision.
   - **Decision Drivers**: Latency, security, maintainability, compatibility, or hosting constraints.
   - **Considered Alternatives**: At least two realistic options with honest pros and cons.
   - **Decision Outcome & Consequences**: What was chosen, positive outcomes, negative trade-offs/risks, and how compliance is verified in code.

### Step 4: Author or Update Setup, Dependency, API, and Operational Docs
1. **Setup & Environment**: Write copy-pasteable terminal commands in exact execution order (clone/install -> copy `.env.example` -> generate key/configure DB -> run migrations/seeds -> start server -> run tests).
2. **Dependencies**: Document why specialized packages or native OS libraries exist and note any license or upgrade constraints.
3. **API Contracts**: Provide concrete request/response JSON (or protocol) examples using realistic domain values (never fabricated trust claims) and document error codes (`400`, `401`, `403`, `404`, `409`, `422`, `429`, `500`).
4. **Operational Runbooks**: Document required background processes (e.g., `queue:work`, `horizon`, Celery worker, cron entries), zero-downtime deployment sequences, and safe rollback steps.

### Step 5: Run Documentation Hygiene and Accuracy Gate
1. Strip AI filler prose, decorative emoji headers (`🚀`, `💡`, `✅`), empty buzzwords (`Seamless`, `Next-Gen`), and unapproved em dashes (`R-02`, `R-16`, `R-36`).
2. Verify all relative Markdown links and file paths resolve to existing files in the repository.

### Documentation Verification Checklist
- [ ] All documented CLI commands verified against manifest scripts or tool binaries.
- [ ] All environment variables synchronized with `.env.example` using safe placeholder values.
- [ ] API request/response schemas and status codes verified against route handlers and validators.
- [ ] ADRs capture context, alternatives, chosen solution, and trade-offs concisely.
- [ ] Operational requirements (workers, crons, migrations, rollbacks) documented accurately.
- [ ] Zero secrets, real API keys, or production credentials included in any documentation file.
- [ ] Prose passes anti-slop copywriting hygiene (concise, actor-named, no emoji header spam, no em dashes).

## 6. Technology-Specific Adaptation Rules

Tailor documentation artifacts to the conventions of the detected stack:
- **PHP (Laravel / CodeIgniter / Symfony)**: Document `composer install`, `.env.example` setup, key generation (`php artisan key:generate` for Laravel), migration commands (`php artisan migrate` or `php spark migrate`), storage links, and queue/scheduler daemon setups (`Supervisor` / `cron`).
- **JavaScript / TypeScript (React / Next.js / Vue / Node)**: Use the exact package manager command (`pnpm`, `npm`, `yarn`, or `bun`) matching the lockfile. Distinguish build-time public variables (`NEXT_PUBLIC_*`, `VITE_*`) from server-only runtime secrets in environment docs.
- **Python (Django / FastAPI / Flask)**: Document virtual environment activation and the exact package manager (`uv sync`, `poetry install`, or `pip install -r requirements.txt`). Note whether FastAPI auto-generates OpenAPI docs at `/docs` and keep Pydantic field descriptions synchronized.
- **Go / Rust / Java / C# (.NET)**: Document required toolchain versions, build targets (`go build`, `cargo build --release`, `./gradlew bootJar`, `dotnet publish`), database migration CLI steps (`golang-migrate`, `sqlx`, `Flyway`, `dotnet ef`), and configuration file overrides.
- **Polyglot Monorepos**: Maintain a clear root `README.md` indexing each service/package alongside service-local documentation or a centralized `docs/` directory with valid relative links.

## 7. Security and Safety Considerations

- **Never Commit Secrets in Examples**: Always use unmistakable dummy placeholders in documentation and `.env.example` (e.g., `STRIPE_SECRET_KEY=sk_test_placeholder_replace_me`, `DB_PASSWORD=secret_local_only`). Never copy values from a developer's live `.env` file into documentation.
- **Internal Topology Discretion**: In public repositories, avoid documenting sensitive production IP addresses, internal staff email addresses, or exploitable security blind spots in public-facing markdown files.
- **Safe Operational Commands**: Operational runbooks that include destructive recovery commands (e.g., `migrate:fresh`, `DROP TABLE`, cache flushes) must include explicit `[!CAUTION]` or warning callouts stating data-loss impact.

## 8. Verification Criteria

Before declaring documentation work complete, confirm with evidence:
1. Every file path referenced in the documentation exists on disk.
2. Every script or command documented in Setup/Operations matches the exact command name in `package.json`, `composer.json`, `Makefile`, or CI workflows.
3. Every newly introduced environment variable in code is present in `.env.example` and the configuration table.
4. No fabricated benchmarks, unmeasured SLA numbers, or fake compliance badges (`SOC 2`, `ISO 27001`) appear anywhere in the documentation (`C-5`, `R-36`).

## 9. Failure Handling and Edge Cases

- **Code and Documentation Conflict**: When existing documentation contradicts the actual source code, treat the verified source code and passing tests as the source of truth for current behavior, update the documentation to match, and note the discrepancy for the user.
- **Undocumented Legacy Environment Variables**: If code reads environment variables without default values and no `.env.example` exists, create `.env.example` populated with every discovered key and safe placeholder descriptions.
- **Deprecated Decisions**: Never silently delete historical ADRs when architecture changes. Mark the old ADR status as `Superseded by ADR-XXXX` and link forward to the new ADR so historical context is preserved.

## 10. Expected Outputs and Reporting Requirements

Use the following **ADR Template** when recording architectural decisions, and provide a concise summary of all updated documentation files in your response:

```markdown
# ADR-XXXX: <Short Imperative Title of Decision>

- **Status**: <Proposed | Accepted | Deprecated | Superseded by ADR-YYYY>
- **Date**: <YYYY-MM-DD>
- **Affected Components**: `<path/to/module>`, `<path/to/config>`

## 1. Context and Problem Statement
<2-4 sentences describing the technical problem, requirement, and repository constraints.>

## 2. Decision Drivers
- <Driver 1: e.g., Must support zero-downtime rolling deployments>
- <Driver 2: e.g., Must work within existing PostgreSQL + Redis infrastructure>

## 3. Considered Options
1. **<Option 1>**: <Summary, pros, cons>
2. **<Option 2>**: <Summary, pros, cons>

## 4. Decision Outcome
Chosen option: **<Option X>**, because <concrete technical rationale>.

### Consequences
- **Positive**: <Concrete benefits>
- **Negative / Trade-offs**: <Known limitations and mitigation steps>
- **Verification**: <How this decision is enforced by tests, linters, or code boundaries>
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - Receives repository inventory from [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`).
  - Receives requirement specifications from [`requirements-analysis`](../requirements-analysis/SKILL.md) (`SKILL-02`).
  - Receives architectural trade-offs and designs from [`adaptive-architecture`](../adaptive-architecture/SKILL.md) (`SKILL-03`).
- **Downstream Skills**:
  - Applies prose and comment discipline from [`ai-anti-slop`](../ai-anti-slop/SKILL.md) (`SKILL-05`).
  - Supports release readiness and operational handoffs in `deployment-readiness-checklist` (`SKILL-30`) and `maintenance-incident-response` (`SKILL-38`).

## 12. Source References

- Library Reference: [AI Anti-Slop & Engineering Craftsmanship Reference](../../references/anti-slop-engineering-reference.md) (`C-5`, `R-02`, `R-16`, `R-36`)
- Reference: Michael Nygard, *Documenting Architecture Decisions* (`https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions`)
- Reference: [Markdown Architectural Decision Records (MADR)](https://adr.github.io/madr/)
- Specification: [OpenAPI Specification (OAS 3.1)](https://spec.openapis.org/oas/latest.html)
