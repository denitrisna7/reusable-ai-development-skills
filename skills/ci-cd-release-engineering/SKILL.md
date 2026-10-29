---
name: ci-cd-release-engineering
description: "Authors and hardens CI/CD pipelines, quality gates, migration checks, and rollback workflows across GitHub Actions/GitLab CI. Use for pipelines. Do not use for manual release sign-off."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-31"
  category: "Performance, Operations, and Deployment"
---

# CI/CD & Release Engineering

This skill governs the design, implementation, and security hardening of Continuous Integration and Continuous Delivery (CI/CD) pipelines and release workflows. It ensures every code change passes deterministic automated quality gates (linting, static analysis, automated tests, dependency audits, build verification, and migration checks) and that releases enforce environment protection, concurrency serialization, provenance, and rapid rollback capability. GitHub Actions is used as a primary reference example, and all workflows must be adapted to the project's actual CI/CD platform.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Creating, modifying, or debugging CI/CD pipeline configuration files (`.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/config.yml`, `azure-pipelines.yml`, `bitbucket-pipelines.yml`).
- Automating build verification, test suite execution, static analysis, or dependency vulnerability scanning on pull/merge requests.
- Designing staged deployment pipelines (staging -> smoke test -> approval -> production) with concurrency locks and rollback triggers.
- Hardening CI/CD workflows against script injection, over-privileged tokens, unpinned third-party actions, or secret leaks.
- Configuring artifact versioning, container image tagging by immutable commit SHA, and release notes generation.

## 2. When Not to Use

Do not activate this skill when the task is strictly limited to:
- Performing a pre-release audit or issuing a final go/no-go release verdict without modifying pipeline automation (route to `deployment-readiness`, `SKILL-33`, and `final-quality-gate`, `SKILL-38`).
- Writing unit, integration, or browser tests themselves rather than wiring them into CI (route to `testing-strategy-design`, `SKILL-15`, `backend-testing-tdd`, `SKILL-16`, or `playwright-mcp-browser-qa`, `SKILL-17`).
- Managing application runtime `.env` schemas and secret stores outside of pipeline orchestration (route to `environment-configuration-management`, `SKILL-32`).

## 3. Scope and Objectives

Every CI/CD pipeline designed or audited under this skill must cover:
- **Automated Tests in Pipeline**: Running unit, integration, and critical E2E tests automatically in clean, isolated environments with deterministic service containers (databases, caches).
- **Linting & Static Analysis Gates**: Enforcing code formatting, linter rules, and strict type/static analysis before merging.
- **Build Verification**: Compiling binaries, bundling frontend assets, or building container images with zero warnings/errors treated as silent passes.
- **Dependency Security Checks**: Auditing lockfiles (`npm ci`, `composer install --locked`, `pip-audit`, `cargo audit`, `govulncheck`) and blocking builds on critical known vulnerabilities.
- **Database Migration Checks**: Validating that pending migrations apply cleanly from scratch, roll back or pass expand/contract linting, and match ORM models/schema definitions.
- **Release Approvals & Protected Environments**: Requiring explicit human approval and branch/tag restrictions before promoting artifacts to production.
- **Artifact Management & Provenance**: Building once, tagging artifacts with immutable commit SHAs/digests, setting retention policies, and promoting identical artifacts across environments.
- **Environment Protection & Concurrency Controls**: Canceling superseded PR check runs while strictly serializing production deployment runs (`cancel-in-progress: false`).
- **Rollback Strategy**: Providing an automated or one-command rollback workflow that restores the previous known-good artifact tag and verifies health endpoints.
- **Failure Reporting**: Surfacing actionable test reports, JUnit/SARIF annotations, and build logs so failures are immediately diagnosable.

## 4. Prerequisites and Context Requirements

Before authoring or modifying CI/CD pipelines, inspect the repository to determine:
1. **Active CI/CD Platform**: Check for `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`, `azure-pipelines.yml`, or `bitbucket-pipelines.yml`. GitHub Actions is only an example; always target the platform actually used by the repository.
2. **Exact Local Commands & Lockfiles**: Inspect `package.json`, `composer.json`, `Makefile`, `pyproject.toml`, `Cargo.toml`, or `go.mod` so the pipeline runs the exact scripts used by developers and enforces lockfile integrity.
3. **Runtime Version Matrix**: Match the language runtime, database engine, and OS versions in CI to the production runtime specification.

## 5. Step-by-Step Workflow

### Step 1: Structure Pipeline Stages for Fast Feedback
- [ ] Organize pipelines into logical stages ordered by execution speed and failure probability:
  1. **Fast Static Checks (`< 2 min`)**: Lockfile verification, formatting check, linter, typechecker/static analyzer, and secret scanning.
  2. **Automated Test Suite**: Unit tests and service-containerized integration tests with coverage/JUnit artifact upload.
  3. **Migration & Build Verification**: Database migration dry-run (apply up, verify schema drift, test rollback where supported) and production artifact/image build.
  4. **Staging Deployment & Smoke Test**: Deploy immutable artifact to staging and run automated health/smoke assertions.
  5. **Production Release (Protected)**: Require environment approval, serialize execution via concurrency lock, deploy, run post-deploy smoke checks, and trigger rollback on failure.

### Step 2: Enforce Deterministic Installs and Caching
- [ ] Always use immutable lockfile installation commands:
  - Node.js: `npm ci`, `pnpm install --frozen-lockfile`, or `yarn install --immutable`
  - PHP: `composer install --no-interaction --prefer-dist --no-progress`
  - Python: `uv sync --frozen`, `poetry install --no-interaction`, or `pip install --require-hashes`
  - Rust / Go: `cargo test --locked` / `go mod verify`
- [ ] Cache dependency download directories keyed by the exact hash of the lockfile (`hashFiles('**/package-lock.json')`), never by mutable branch name alone.

### Step 3: Add Database Migration Safety Checks in CI
- [ ] Spin up an ephemeral database service container matching the production engine and version.
- [ ] Run all migrations from an empty database to verify clean forward execution.
- [ ] Verify there is no unmigrated schema drift between ORM models and migration files (e.g., `makemigrations --check --dry-run` in Django, `prisma migrate status`, or schema diff check).

### Step 4: Harden Pipeline Security & Concurrency
- [ ] Apply all controls detailed in `[references/ci-cd-security-hardening.md](references/ci-cd-security-hardening.md)`:
  - Set least-privilege `permissions` (`contents: read` by default).
  - Pin external actions/plugins to full commit SHAs or immutable digests.
  - Pass untrusted event strings (`pull_request.title`, `head_ref`, commit messages) through `env:` variables rather than inline `${{ ... }}` shell interpolation.
  - Set `cancel-in-progress: true` on PR verification workflows and `cancel-in-progress: false` on deployment workflows.
  - Set explicit job `timeout-minutes` (e.g., `15` minutes) so hung processes do not burn runner quotas.

### Step 5: Wire Release Promotion, Smoke Verification, and Rollback
- [ ] Tag built artifacts/images with both the immutable Git commit SHA (`sha-<commit>`) and semantic release version.
- [ ] Add an automated post-deployment verification step that polls `/health` or `/ready` and executes critical smoke checks.
- [ ] Provide a documented, parameterized rollback workflow (`workflow_dispatch` or manual pipeline stage) accepting a target `release_sha` or tag to redeploy the prior artifact immediately.

## 6. Technology-Specific Adaptation Rules

GitHub Actions is an example. Adapt syntax and tooling to the project's actual CI/CD platform and stack, and never force PHPStan, Pint, Pest, shadcn/ui, or Playwright where inapplicable:
- **CI/CD Platform Adaptation**:
  - **GitHub Actions**: `.github/workflows/*.yml`, `concurrency`, `environment`, `permissions`, `actions/cache`, `upload-artifact`.
  - **GitLab CI**: `.gitlab-ci.yml`, `stages`, `interruptible: true` (for CI jobs), `resource_group: production` (for serialized deploys), `rules`, `artifacts:reports:junit`.
  - **Jenkins**: Declarative `Jenkinsfile`, `options { disableConcurrentBuilds(abortPrevious: true); timeout(time: 15, unit: 'MINUTES') }`, `post { always { junit ... } }`.
  - **CircleCI / Azure Pipelines / Bitbucket Pipelines**: Use platform-native caching keyed by lockfile checksums, manual approval gates, and deployment concurrency locks.
- **Technology Stack Adaptation**:
  - **PHP (Laravel / Symfony / CodeIgniter)**: Run `composer validate --strict`, `composer audit`, code style check (`./vendor/bin/pint --test` or `php-cs-fixer` if installed), static analysis (`./vendor/bin/phpstan analyse` if configured), and Pest/PHPUnit with MySQL/PostgreSQL service containers.
  - **JavaScript / TypeScript (React / Next.js / Vue / Node.js)**: Run lockfile install (`npm ci` / `pnpm install --frozen-lockfile`), linter (`eslint` / `biome`), typecheck (`tsc --noEmit`), unit/integration tests (`vitest` / `jest`), E2E browser tests (`playwright test` if present, uploading trace artifacts on failure), and production build check (`npm run build`).
  - **Python (Django / FastAPI / Flask)**: Run `uv sync --frozen` or `pip install -r requirements.txt`, `ruff check`, `ruff format --check`, `mypy` / `pyright`, `pytest`, `pip-audit`, and `python manage.py makemigrations --check --dry-run` (for Django).
  - **Go**: Run `go mod verify`, `golangci-lint run`, `go test -race -v ./...`, `govulncheck ./...`, and cross-compile binary verification.
  - **Java / Spring Boot**: Run `./mvnw -B verify` or `./gradlew check` with Gradle/Maven wrapper verification, Spotless/Checkstyle, JUnit 5 + Testcontainers, and OWASP dependency check.
  - **Rust**: Run `cargo fmt --all -- --check`, `cargo clippy --all-targets --all-features -- -D warnings`, `cargo test --locked`, and `cargo audit`.
  - **C# / .NET**: Run `dotnet restore --locked-mode`, `dotnet format --verify-no-changes`, `dotnet build --no-restore -warnaserror`, `dotnet test --no-build`, and `dotnet list package --vulnerable`.
  - **Mobile / Flutter**: Run `flutter pub get --enforce-lockfile`, `flutter analyze --fatal-infos`, `flutter test`, and platform build verification (`flutter build apk --debug` or signed release builds).
  - **Unknown or Mixed Stacks**: Discover build/test entrypoints from `Makefile`, `Justfile`, `Taskfile.yml`, or `Dockerfile` multi-stage targets and wire each stage into a fail-closed CI pipeline.

## 7. Security and Safety Considerations

- **Never Echo or Artifact Secrets**: Never run `env`, `printenv`, or `set -x` around steps handling credentials, and never upload `.env` files or unredacted debug logs as downloadable build artifacts.
- **Fork Pull Request Isolation**: Ensure workflows triggered by external forks do not have access to deployment secrets, internal package registries with write tokens, or production environments.
- **No Unreviewed Force Deploys**: Do not configure pipelines to auto-deploy directly to production on unreviewed branch pushes; require passing CI status checks and protected branch/environment gates.
- **Supply Chain Integrity**: Verify checksums of downloaded CLI tools (such as custom linters or cloud CLIs installed via `curl`) inside pipeline scripts rather than piping unverified remote scripts to `bash`.

## 8. Verification Criteria

Before declaring CI/CD engineering work complete, verify:
1. **Valid Pipeline Syntax**: YAML/Groovy syntax is valid, all job dependencies (`needs` / `stages`) form a valid DAG, and referenced npm/composer/Makefile commands actually exist in the repository.
2. **Hardening Applied**: Explicit token permissions, job timeouts, concurrency blocks, action SHA pinning, and safe variable quoting are present (see `[references/ci-cd-security-hardening.md](references/ci-cd-security-hardening.md)`).
3. **Fail-Closed Gates**: No linter, static analysis, or test step uses `|| true` or `continue-on-error: true` unless explicitly justified as an informational non-blocking report.
4. **Build-Once Promotion**: Deploy jobs promote the verified build artifact or commit SHA rather than rebuilding untested code during deployment.

## 9. Failure Handling and Edge Cases

- **Flaky Tests Blocking Pipeline**: Do not mask flaky tests with global `continue-on-error: true`. Isolate the root cause (shared state, timing race, unmocked clock/network), upload failure artifacts/traces on retry, and route to `test-reporting-failure-diagnosis` (`SKILL-19`).
- **Missing CI Platform in Repo**: If no CI configuration exists yet, inspect repository remotes (`github.com`, `gitlab.com`, `bitbucket.org`) or default cleanly to the matching platform conventions.
- **Irreversible Database Migrations During Rollback**: Document clearly in the pipeline that code rollback is only instant when paired with backward-compatible expand/contract database migrations.
- **Monorepo Partial Builds**: In monorepos, use path filters or workspace graph runners (`turbo`, `nx`) for fast PR feedback, while ensuring changes to shared core packages trigger downstream dependent test suites.

## 10. Expected Outputs and Reporting Requirements

Deliver the pipeline configuration file(s) along with a **CI/CD & Release Pipeline Summary**:

```markdown
# CI/CD & Release Engineering Report

## 1. Pipeline Overview
- **CI/CD Platform & Config Path**: `<e.g., GitHub Actions | .github/workflows/ci.yml>`
- **Triggers & Concurrency Policy**: `<push/PR on main; cancel-in-progress on PRs, serialized on production>`

## 2. Quality Gates & Stages Configured
| Stage / Job | Executed Command(s) | Blocking Gate? | Timeout |
| :--- | :--- | :--- | :--- |
| `<Lint & Typecheck>` | `<npm ci && npm run lint && npx tsc --noEmit>` | `Yes` | `10m` |
| `<Unit & Integration Tests>` | `<npm test -- --ci>` | `Yes` | `15m` |
| `<Dependency Audit>` | `<npm audit --audit-level=high>` | `Yes` | `5m` |
| `<Build & Migration Check>` | `<npx prisma migrate deploy && npm run build>` | `Yes` | `15m` |

## 3. Security Hardening & Rollback Controls
- **Token Permissions & Pinning**: `<permissions: contents: read; SHA-pinned actions>`
- **Rollback Procedure**: `<How to trigger automated rollback to previous SHA>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Automates the checks defined by `code-quality-static-analysis` (`SKILL-07`), `dependency-supply-chain-security` (`SKILL-09`), `backend-testing-tdd` (`SKILL-16`), and `playwright-mcp-browser-qa` (`SKILL-17`).
- **Downstream Skills**: Feeds build, test, and migration artifacts into `deployment-readiness` (`SKILL-33`) and `final-quality-gate` (`SKILL-38`), and aligns environment variables with `environment-configuration-management` (`SKILL-32`).

## 12. Source References

- **GitHub Actions Official Documentation**: https://docs.github.com/en/actions
- **Local CI/CD Security Hardening Reference**: [references/ci-cd-security-hardening.md](references/ci-cd-security-hardening.md)
- **OWASP CI/CD Security Risks**: https://owasp.org/www-project-top-10-ci-cd-security-risks/
