---
name: documentation-developer-handoff
description: "Mandatory lifecycle skill (SKILL-37). Audits clean-clone setup guides, .env references, test commands, architecture docs, and handoff runbooks. Part of the 38-skill quality suite."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-37"
  category: "Final Quality and Maintenance"
---

# Documentation Quality & Developer Handoff

This skill governs the creation, verification, and maintenance of technical documentation, developer onboarding guides, operational runbooks, and engineering handoff artifacts. It ensures that a new engineer or operator can clone the repository, configure the environment, run the test suite, understand the architecture, deploy safely, and troubleshoot common operational failures without relying on unwritten tribal knowledge. Every command and file path documented must be verified against the actual codebase.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Writing, updating, or auditing `README.md`, `CONTRIBUTING.md`, `OPERATIONS.md`, or developer onboarding guides.
- Documenting step-by-step local setup instructions from a fresh Git clone, including environment variables and backing services.
- Preparing a developer or operational handoff package at the conclusion of a feature, sprint, or full-project build.
- Synchronizing outdated documentation after architectural changes, command renames, dependency upgrades, or schema migrations.
- Writing troubleshooting runbooks and maintenance procedures (certificate renewal, secret rotation, queue recovery, dependency updates).

## 2. When Not to Use

Do not activate this skill when the task is strictly limited to:
- Authoring standalone Architecture Decision Records during initial system design before code exists (route to `technical-decision-records`, `SKILL-04`, and reference those ADRs from this skill).
- Generating formal OpenAPI / Swagger / GraphQL schema contracts in isolation (route to `system-architecture-design`, `SKILL-03`, or `api-external-service-integration`, `SKILL-27`).
- Executing the final 15-point release quality gate audit (route to `final-quality-gate`, `SKILL-38`, which consumes the documentation produced by this skill).

## 3. Scope and Objectives

Every documentation and developer handoff package produced under this skill must cover:
- **Setup Documentation (Clean-Clone Bootstrap)**: Listing exact runtime/OS prerequisites (language version, package manager, Docker/database engines) and sequential copy-pasteable commands from `git clone` to a running local application.
- **Environment Configuration Guide**: Explaining how to copy `.env.example` to `.env` and documenting every required and optional environment variable, expected format, and how to obtain local/sandbox credentials.
- **Testing Instructions**: Documenting exact commands to run unit tests, integration tests, browser/E2E tests, linters, typecheckers, and code coverage reports, including any required test database setup.
- **Architecture References**: Providing a clear high-level system overview, directory structure map, core domain data flow, key third-party integrations, and links to Architecture Decision Records (ADRs).
- **Deployment Procedures**: Documenting the exact build, migration, asset compilation, worker restart, and verification steps for staging and production releases (`SKILL-31` and `SKILL-33`).
- **Troubleshooting & Common Failures**: Providing symptom-to-solution runbooks for frequent local and production issues (port conflicts, migration lock errors, stale caches, missing env keys, queue worker stalls).
- **Operational Handoff**: Summarizing health check endpoints, log locations, monitoring dashboards, alert runbooks, and backup/restore commands (`SKILL-34` and `SKILL-35`).
- **Maintenance Procedures**: Documenting recurring engineering maintenance tasks (dependency vulnerability audits, secret rotation, database vacuum/pruning, expired token cleanup jobs).
- **Keeping Documentation Aligned with Reality**: Auditing every documented script name, CLI flag, port number, and file path against `package.json`, `composer.json`, `Makefile`, `Dockerfile`, and actual repository files.

## 4. Prerequisites and Context Requirements

Before writing or updating documentation, inspect the repository to establish ground truth:
1. **Manifests & Task Runners**: Read `package.json`, `composer.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `Justfile`, and `docker-compose.yml` to extract the real commands and version constraints.
2. **Environment Contract**: Read `.env.example` and central `config/` files (`SKILL-32`) so no environment variable is undocumented or misspelled.
3. **CI Pipeline Parity**: Read `.github/workflows/` or `.gitlab-ci.yml` (`SKILL-31`) so the local verification commands taught to developers match the exact gates enforced by CI.

## 5. Step-by-Step Workflow

### Step 1: Audit Existing Documentation Against Codebase Reality
- [ ] Compare existing `README.md` and `docs/` files against the current directory structure and scripts.
- [ ] Flag and remove any phantom commands (e.g., documenting `npm run test:e2e` when `package.json` only defines `npm run e2e`), dead links, obsolete architecture diagrams, or deprecated environment variables.

### Step 2: Author the Clean-Clone Local Setup & Environment Guide
- [ ] List exact **Prerequisites** with version numbers verified from config files (e.g., `PHP >= 8.3`, `Node.js 22 LTS`, `PostgreSQL 16`, `Redis 7`).
- [ ] Write a numbered **Quickstart / Bootstrap** sequence that works sequentially without hidden steps:
  1. Clone repository and install dependencies (`npm ci`, `composer install`, `uv sync`).
  2. Copy environment file (`cp .env.example .env`) and generate app keys (`php artisan key:generate`, `openssl rand -base64 32`).
  3. Start backing services (`docker compose up -d` or local DB/Redis).
  4. Run database migrations and seed development data (`migrate --seed`).
  5. Start the development server and background queue worker (`composer run dev`, `npm run dev`).
- [ ] Include an **Environment Variables Reference Table** explaining all critical keys in `.env.example`.

### Step 3: Document Testing, Linting, and Static Analysis Commands
- [ ] Provide a concise command table covering:
  - Full verification suite (single command to run all checks before opening a PR).
  - Unit and integration test commands (including how to run a single test file or filter by name).
  - End-to-end / browser test commands and prerequisite browser installation (`npx playwright install`).
  - Linter, formatter, and static analyzer commands.

### Step 4: Document Architecture Overview & Directory Map
- [ ] Include a concise **Directory Structure** tree explaining where controllers/routes, domain services, models/migrations, background jobs, configuration, and tests live.
- [ ] Summarize key architectural boundaries, state management patterns, external service integrations (payment gateways, email providers, AI providers), and link to relevant ADRs (`docs/adr/`).

### Step 5: Document Deployment, Operations, Troubleshooting, and Maintenance
- [ ] **Deployment & Rollback**: Detail build verification, zero-downtime migration execution, cache warming, worker restarts, post-deploy smoke tests, and exact rollback commands (`SKILL-31`, `SKILL-33`).
- [ ] **Operational Handoff**:
  - List liveness (`/health`) and readiness (`/ready`) endpoints and expected HTTP response codes (`SKILL-34`).
  - Document structured log streams, correlation ID headers (`X-Request-ID`), error tracking dashboards, and key alerts.
  - Document scheduled cron jobs, queue worker topologies, and Dead-Letter Queue replay commands (`SKILL-30`).
  - Link or embed the database backup verification and disaster recovery restore runbook (`SKILL-35`).
- [ ] **Troubleshooting Runbook**: Document at least 3-5 concrete failure scenarios specific to the stack (Symptom -> Root Cause -> Exact Diagnostic & Fix Commands).
- [ ] **Routine Maintenance Procedures**:
  - Dependency security auditing and safe lockfile upgrade workflow (`SKILL-09`).
  - Zero-downtime secret and API key rotation steps (`SKILL-32`).
  - Database maintenance, failed-job table pruning, and temporary file cleanup tasks.

### Step 6: Verify Documentation Accuracy Against the Live Repository
- [ ] Cross-check every file path, environment variable name, port number, and CLI script in the documentation against the repository files before completing the task.

## 6. Technology-Specific Adaptation Rules

Adapt documentation commands and structure to the project's actual stack and lockfiles. Never document or force PHPStan, Pint, Pest, shadcn/ui, or Playwright where inapplicable to the repository:
- **PHP (Laravel / Symfony / CodeIgniter)**: Document `composer install`, `.env` setup, `php artisan key:generate`, `php artisan migrate --seed`, `php artisan storage:link`, queue worker execution (`php artisan queue:listen`), scheduler (`schedule:work`), and testing/quality commands (`php artisan test`, `./vendor/bin/pint --test`, `./vendor/bin/phpstan analyse`) only when those tools exist in `composer.json`. For CodeIgniter 4, document `php spark serve`, `php spark migrate`, and `vendor/bin/phpunit`.
- **JavaScript / TypeScript (Next.js / React / Vue / Node.js)**: Identify the exact package manager from the committed lockfile (`package-lock.json` -> `npm`, `pnpm-lock.yaml` -> `pnpm`, `yarn.lock` -> `yarn`, `bun.lockb` -> `bun`) and use it consistently throughout all documented commands. Document exact script names from `package.json` (`dev`, `build`, `start`, `test`, `lint`, `typecheck`).
- **Python (Django / FastAPI / Flask)**: Document virtual environment creation (`uv sync`, `poetry install`, or `python -m venv .venv && source .venv/bin/activate`), migration execution (`python manage.py migrate` or `alembic upgrade head`), ASGI/WSGI server launch (`uvicorn`, `gunicorn`, or `manage.py runserver`), and `pytest` / `ruff` / `mypy` commands.
- **Go**: Document Go version from `go.mod`, binary build (`go build ./cmd/...`), database migration CLI (`migrate` / `goose` / `atlas`), test execution (`go test -race ./...`), and linter (`golangci-lint run`).
- **Java / Spring Boot**: Document JDK version (`17` / `21`), wrapper usage (`./mvnw spring-boot:run`, `./mvnw verify`, or `./gradlew bootRun`, `./gradlew check`), active Spring profiles (`SPRING_PROFILES_ACTIVE=local`), and Docker Compose backing services.
- **Rust**: Document toolchain from `rust-toolchain.toml`, required system libraries (`pkg-config`, `libssl-dev`), `cargo run`, `cargo test --locked`, `cargo clippy`, and `sqlx-cli` setup if used.
- **C# / .NET**: Document .NET SDK version from `global.json`, `dotnet restore`, `dotnet ef database update`, `dotnet run --project ...`, `dotnet test`, and `dotnet user-secrets` configuration.
- **Mobile / Flutter**: Document SDK versions (`Flutter`, `Dart`, `Xcode`, `Android Studio`), platform dependency installation (`flutter pub get`, `cd ios && pod install`), code generation (`dart run build_runner build --delete-conflicting-outputs`), and device/emulator launch commands (`flutter run`).
- **Unknown or Mixed Stacks**: Inspect `Makefile`, `Justfile`, `docker-compose.yml`, and CI workflow files to extract the authoritative build, run, and test commands.

## 7. Security and Safety Considerations

- **Zero Real Secrets in Documentation**: Never paste real API keys, production database URLs, internal private IP addresses, customer emails, or valid JWTs into `README.md`, code examples, or troubleshooting guides. Use clearly marked placeholders (`<YOUR_API_KEY>`, `sk_test_placeholder`).
- **Warn Around Destructive Development Commands**: Whenever documenting commands that wipe data (such as `migrate:fresh`, `prisma migrate reset`, `docker compose down -v`, or `db:wipe`), attach an explicit `[!CAUTION]` or `WARNING:` note stating that the command destroys all data and must never be run in staging or production.
- **Do Not Expose Internal Security Bypass Mechanics**: Document how authentication and RBAC work architecturally, but never document backdoor credentials or encourage disabling TLS/CSRF protections as a troubleshooting workaround.

## 8. Verification Criteria

Before marking documentation and handoff work complete, verify:
1. **100% Command & Path Accuracy**: Every npm/composer/make script, CLI flag, and relative file link mentioned in the documentation exists in the repository.
2. **Clean-Clone Completeness**: Following the setup instructions in exact top-to-bottom order leaves no missing steps (such as forgetting database creation, migrations, or background workers).
3. **Lockfile-Matched Package Manager**: Documentation does not tell users to run `yarn` in an `npm` or `pnpm` repository.
4. **Environment Variable Parity**: Every variable in `.env.example` is accounted for in the configuration documentation.

## 9. Failure Handling and Edge Cases

- **Missing `.env.example`**: If the repository lacks an `.env.example` file, create one immediately by scanning all configuration files for environment variable references (`SKILL-32`) and populate safe defaults before finishing the setup guide.
- **Multi-Service / Monorepo Projects**: Clearly document the startup order across workspaces/services (e.g., shared packages build -> database & Redis -> backend API -> frontend app) or provide a unified root command (`docker compose up` or `pnpm dev`).
- **OS-Specific Differences (Linux / macOS / Windows WSL2)**: Note platform-specific prerequisites (such as WSL2 file-watching or Docker volume mount paths on Windows, or Homebrew vs. `apt` package names) when relevant to developer setup.

## 10. Expected Outputs and Reporting Requirements

Deliver the updated documentation files (`README.md`, `docs/*.md`, `.env.example`) and provide a **Documentation & Developer Handoff Verification Summary**:

```markdown
# Documentation & Developer Handoff Report

## 1. Documentation Artifacts Updated
- **Primary Files**: `<e.g., README.md, .env.example, docs/OPERATIONS.md>`
- **Package Manager & Runtime Verified**: `<e.g., pnpm 9.x, Node 22.x, PostgreSQL 16>`

## 2. Handoff Coverage Checklist
| Handoff Section | Status | Verification Evidence |
| :--- | :--- | :--- |
| **1. Clean-Clone Setup & Prerequisites** | `<Verified>` | `<All bootstrap commands verified against manifests>` |
| **2. Environment Configuration Guide** | `<Verified>` | `<All .env.example variables documented with safe defaults>` |
| **3. Testing & Static Analysis Guide** | `<Verified>` | `<Unit, integration, E2E, and lint commands verified>` |
| **4. Architecture & Directory Map** | `<Verified>` | `<Matches actual repository tree and ADRs>` |
| **5. Deployment, Rollback & Operations** | `<Verified>` | `<Health endpoints, migrations, workers, backups documented>` |
| **6. Troubleshooting & Maintenance** | `<Verified>` | `<Common failure fixes and maintenance runbooks included>` |
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Synthesizes architectural decisions from `technical-decision-records` (`SKILL-04`), configuration contracts from `environment-configuration-management` (`SKILL-32`), CI commands from `ci-cd-release-engineering` (`SKILL-31`), health/logging details from `observability-incident-diagnosis` (`SKILL-34`), and DR runbooks from `backup-recovery-disaster-preparedness` (`SKILL-35`).
- **Downstream Skills**: Directly satisfies Gate Domain 14 (`Documentation & Handoff`) in `final-quality-gate` (`SKILL-38`).

## 12. Source References

- **Write the Docs (Software Documentation Best Practices)**: https://www.writethedocs.org/guide/
- **Google Developer Documentation Style Guide**: https://developers.google.com/style
- **Shared Deployment Readiness & Quality Gate Matrix**: [../../references/deployment-readiness-quality-gate-matrix.md](../../references/deployment-readiness-quality-gate-matrix.md)
