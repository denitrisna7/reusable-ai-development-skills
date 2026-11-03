---
name: deployment-readiness
description: "Mandatory lifecycle skill (SKILL-33). Audits production builds, config safety, migrations, backups, health checks, and rollback runbooks. Part of the 38-skill quality suite."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-33"
  category: "Performance, Operations, and Deployment"
---

# Deployment Readiness & Release Safety

This skill evaluates whether an application and its operational environment are ready for a safe production release. It audits build integrity, production configuration, database migration safety, backup verification, HTTPS and service permissions, queue/scheduler readiness, health endpoints, rollback procedures, and post-deployment smoke tests. It operates strictly under the Mandatory Deployment Readiness Policy: **this skill evaluates readiness and must never execute an actual deployment unless the user's task explicitly authorizes that action.**

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Assessing whether a feature, release branch, or application is ready to deploy to staging or production.
- Preparing a pre-deployment checklist, release risk assessment, rollback runbook, or post-deployment smoke-test plan.
- Auditing operational release safety (database migration backward compatibility, queue worker restart procedures, HTTPS/TLS enforcement, file/process permissions, and `/health` or `/ready` endpoints).
- Supplying operational readiness evidence to `final-quality-gate` (`SKILL-38`).

## 2. When Not to Use

Do not activate this skill when the task is strictly limited to:
- Authoring CI/CD pipeline YAML syntax or build runner scripts (route to `ci-cd-release-engineering`, `SKILL-31`).
- Designing long-term disaster recovery architecture and 3-2-1 backup storage infrastructure from scratch (route to `backup-recovery-disaster-preparedness`, `SKILL-35`, which supplies backup evidence to this skill).
- Executing the full 15-domain holistic code, UX, security, and requirements audit (pair with `final-quality-gate`, `SKILL-38`).

## 3. Scope and Objectives

Every deployment readiness evaluation conducted under this skill must cover:
- **Build Verification**: Confirming that the production build compiles cleanly without errors, missing assets, or broken lockfiles, while recognizing that **a successful build alone is never proof of deployment readiness**.
- **Configuration Checks**: Verifying that production environment variables, secrets, debug flags (`DEBUG=false`), and allowed hosts/CORS origins are properly configured and validated.
- **Database Migration Safety**: Auditing pending database migrations for destructive operations (`DROP COLUMN`, `DROP TABLE`, table-locking rewrites on large tables, non-nullable additions without defaults) and verifying expand/contract compatibility with running application instances.
- **Backup Verification**: Confirming that an automated or pre-release database/state backup is active, verified, and restorable before running production migrations.
- **HTTPS & Permissions**: Verifying TLS termination, HSTS/HTTPS redirects, secure cookie flags, least-privilege OS/container user execution (non-root container user), and writable storage/cache directory permissions.
- **Queue & Scheduler Readiness**: Ensuring background worker daemons, supervisor configs, and cron schedulers are configured to restart gracefully (`SIGTERM` / `queue:restart`) so workers do not continue running stale code in memory.
- **Health Checks**: Verifying that liveness (`/health` or `/healthz`) and readiness (`/ready` or `/readyz`) endpoints exist and accurately reflect downstream dependency readiness.
- **Rollback Procedures**: Documenting and verifying exact, step-by-step rollback commands for both application artifacts and database schema changes.
- **Post-Deployment Smoke Tests**: Defining concrete, non-destructive verification checks to execute immediately after release.
- **Release Risk Assessment**: Grading the release blast radius, downtime requirements, and data mutation risks.
- **Deployment Documentation**: Recording exact pre-deploy, deploy, verification, and rollback steps for operators.

## 4. Prerequisites and Context Requirements

Before issuing a deployment readiness verdict, gather:
1. **Release Diff & Migration List**: Inspect all code changes, dependency updates, new environment variables, and pending database migrations included in the release candidate.
2. **Target Topology**: Identify whether the deployment uses rolling updates, blue/green switching, serverless functions, or single-server maintenance windows.
3. **Explicit Integration Contract with `final-quality-gate` (`SKILL-38`)**: Review `[../../references/deployment-readiness-quality-gate-matrix.md](../../references/deployment-readiness-quality-gate-matrix.md)` to ensure evidence states (`PASS`, `FAIL`, `BLOCKED`, `NOT TESTED`) and final verdicts (`READY`, `READY WITH ACCEPTED RISKS`, `BLOCKED`, `INCOMPLETE`) are strictly enforced.

## 5. Step-by-Step Workflow

### Step 1: Verify Production Build and Dependency Lock Integrity
- [ ] Run the production build and static verification commands in clean/locked mode (or inspect CI artifacts if sandboxed).
- [ ] Confirm lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `composer.lock`, `uv.lock`, `Cargo.lock`, `go.sum`) are committed and synchronized with manifests.
- [ ] Verify that production asset compilation (`npm run build`, `vite build`, binary build) produces expected outputs with zero fatal errors.

### Step 2: Audit Environment Configuration, HTTPS, and Runtime Permissions
- [ ] Cross-check all new or modified environment variables in the release against `.env.example` and deployment manifests (`SKILL-32`).
- [ ] Confirm production security settings: `DEBUG=false`, HTTPS enforcement enabled, trusted proxy headers configured, and no development/debug routes exposed.
- [ ] Check container/filesystem permissions: containers run as a non-root user where applicable, and runtime writable directories (`storage/`, `bootstrap/cache/`, `tmp/`) have explicit ownership without insecure `chmod 777`.

### Step 3: Evaluate Database Migration & Backup Safety
- [ ] Inspect every pending migration file line by line:
  - Does it drop or rename a column/table still queried by the currently running application version during a zero-downtime rolling deploy? If yes, mark **`BLOCKED`** until refactored into an expand/contract migration.
  - Does it add an index or alter a massive table without `CONCURRENTLY` / online DDL where supported? Flag lock duration risk.
  - Does it include a valid `down()` / rollback path or a documented forward-fix strategy?
- [ ] Confirm pre-deployment backup status: verify that a recent snapshot/backup procedure is in place and verified (`SKILL-35`) before any schema or data migration runs.

### Step 4: Verify Health Checks, Queues, and Graceful Restart Readiness
- [ ] Verify `/health` (liveness) and `/ready` (readiness) endpoints exist and return HTTP `200` when healthy and `503` when critical dependencies (database, Redis) are unreachable.
- [ ] Verify the deployment script signals background queue workers to finish current jobs and reload new code (e.g., `php artisan queue:restart`, `SIGTERM` to Celery/BullMQ/Go workers).

### Step 5: Define Rollback Plan and Post-Deployment Smoke Tests
- [ ] Write the exact rollback procedure:
  1. How to revert the application container/artifact to the previous commit SHA.
  2. Whether database migrations can be rolled back safely or require expand-phase tolerance.
  3. How to flush/warm caches if cache serialization formats changed.
- [ ] Write a concrete Post-Deployment Smoke-Test Checklist covering health endpoints, authentication, primary core user workflow, and background job heartbeats.

### Step 6: Assign the Mandatory Readiness Verdict
- [ ] Classify every check as `PASS`, `FAIL`, `BLOCKED`, or `NOT TESTED` (with stack/scope justification if excluded).
- [ ] Assign one of the four mandatory verdicts shared with `final-quality-gate` (`SKILL-38`):
  - **`READY`**: All applicable mandatory checks executed and passed with recorded evidence.
  - **`READY WITH ACCEPTED RISKS`**: All critical checks passed; non-blocking residual risks are documented with mitigation plans and require explicit human sign-off.
  - **`BLOCKED`**: One or more critical checks failed (broken build/tests, destructive unguarded migration, exposed secret, missing rollback path).
  - **`INCOMPLETE`**: Required checks have not yet been executed or evidence is missing.

## 6. Technology-Specific Adaptation Rules

Adapt deployment readiness checks to the project's actual stack and deployment target. Never force PHPStan, Pint, Pest, shadcn/ui, or Playwright where inapplicable:
- **PHP (Laravel / Symfony / CodeIgniter)**: Verify `composer install --no-dev --optimize-autoloader --classmap-authoritative`, `php artisan config:cache`, `route:cache`, `view:cache`, `migrate --force` safety, `storage:link`, and `queue:restart` in the deploy runbook; confirm `APP_DEBUG=false` and `APP_ENV=production`. In CodeIgniter 4, verify `CI_ENVIRONMENT=production`, writable `writable/` permissions, and `php spark migrate` safety.
- **JavaScript / TypeScript (Next.js / React / Vue / Node.js)**: Verify production build output (`next build`, `vite build`, `nuxt build`), standalone server or asset bundle integrity, PM2/container graceful shutdown (`SIGINT`/`SIGTERM` handling with `server.close()`), and static asset CDN/cache-control headers.
- **Python (Django / FastAPI / Flask)**: Run `python manage.py check --deploy` in Django (verifying `SECURE_HSTS_SECONDS`, `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `STATIC_ROOT` via `collectstatic --noinput`). Verify Gunicorn/Uvicorn worker counts, timeouts, and graceful shutdown flags (`--graceful-timeout`).
- **Go**: Verify reproducible binary compilation (`CGO_ENABLED=0` where appropriate), embedded static migrations/assets (`embed.FS`), TLS root certificate availability (`ca-certificates` in distroless/scratch images), and `SIGTERM` context cancellation via `http.Server.Shutdown(ctx)`.
- **Java / Spring Boot**: Verify executable JAR/container layer build, Flyway/Liquibase migration validation, Spring Boot Actuator `/actuator/health/liveness` and `/actuator/health/readiness` (ensuring sensitive actuator endpoints like `/actuator/env` and `/actuator/heapdump` are NOT publicly exposed), and `server.shutdown=graceful`.
- **Rust**: Verify `cargo build --release --locked`, SQLx offline query metadata check (`SQLX_OFFLINE=true`), graceful Tokio signal handling (`axum::serve(...).with_graceful_shutdown(...)`), and minimal runtime container dependencies.
- **C# / .NET**: Verify `dotnet publish -c Release`, EF Core migration bundle or idempotent SQL script generation (`dotnet ef migrations script --idempotent`), ASP.NET Core `MapHealthChecks`, and production HTTPS/HSTS middleware.
- **Mobile / Flutter**: Verify release build compilation (`flutter build appbundle --release` / `flutter build ipa --release`), version and build number increments in `pubspec.yaml`, signing keystore/provisioning configuration, ProGuard/R8 rules, and production HTTPS API endpoints.
- **Unknown or Mixed Stacks**: Audit artifact compilation, lockfile consistency, environment variable completeness, schema migration compatibility, non-root execution permissions, health endpoints, and rollback scripts.

## 7. Security and Safety Considerations

- **No Unauthorized Deployment Execution**: Never run `fly deploy`, `vercel --prod`, `kubectl apply`, `helm upgrade`, `terraform apply`, `git push production`, or SSH production deployment commands during a readiness evaluation unless the user explicitly instructs and authorizes executing the live deployment.
- **Protect Diagnostic Endpoints**: Ensure health check endpoints do not leak internal stack traces, database credentials, version numbers, or environment variables in public HTTP responses.
- **Database Migration Blast-Radius Protection**: Never approve running unbacked-up destructive DDL (`DROP TABLE`, `TRUNCATE`, `ALTER COLUMN` with lossy type cast) in a production deployment pipeline.

## 8. Verification Criteria

Before completing a deployment readiness assessment, confirm:
1. **Build != Ready Enforced**: The report never declares `READY` solely because `build` succeeded; migration safety, config, backups, permissions, queues, health checks, rollback, and smoke tests are all evaluated.
2. **Zero Fabricated Evidence**: Any check that could not be executed locally (e.g., production backup snapshot check) is honestly marked `BLOCKED` or `NOT TESTED` with exact instructions for the operator.
3. **Verdict Consistency**: The issued verdict (`READY`, `READY WITH ACCEPTED RISKS`, `BLOCKED`, `INCOMPLETE`) strictly matches the rules in `[../../references/deployment-readiness-quality-gate-matrix.md](../../references/deployment-readiness-quality-gate-matrix.md)`.
4. **Actionable Runbook**: Both the forward deployment sequence and the inverse rollback sequence are explicitly documented.

## 9. Failure Handling and Edge Cases

- **Destructive Migration Required**: If dropping or renaming an active column is required, mark the single-step release `BLOCKED` and instruct the team to split it into a two-phase expand/contract release: Release 1 stops reading/writing the old column in code; Release 2 drops the column after Release 1 is verified stable in production.
- **Stateless or Static Applications**: If an application has no database or background queues, mark Database Migration Safety, Backup Verification, and Queue Readiness as `NOT APPLICABLE (Excluded)` with an explicit architectural justification.
- **Long-Running Data Backfills**: Separate schema DDL migrations from heavy data backfills so the deployment step completes in seconds rather than timing out the orchestrator.

## 10. Expected Outputs and Reporting Requirements

Always output a structured **Deployment Readiness & Release Safety Report**:

```markdown
# Deployment Readiness & Release Safety Report

- **Release Target / Version**: `<branch / commit SHA / version>`
- **Deployment Readiness Verdict**: `<READY | READY WITH ACCEPTED RISKS | BLOCKED | INCOMPLETE>`
- **Deployment Executed?**: `NO (Readiness evaluation only per mandatory safety policy)`

## 1. Readiness Verification Matrix
| Check Domain | Status (`PASS`/`FAIL`/`BLOCKED`/`NOT TESTED`) | Evidence / Justification |
| :--- | :--- | :--- |
| **1. Production Build & Lockfile** | `<Status>` | `<Build command output & lockfile check>` |
| **2. Environment & Secret Config** | `<Status>` | `<.env.example diff, DEBUG=false verified>` |
| **3. Database Migration Safety** | `<Status>` | `<Pending migrations audited; backward compatibility>` |
| **4. Backup Verification** | `<Status>` | `<Pre-deploy snapshot mechanism verified>` |
| **5. HTTPS, TLS & Permissions** | `<Status>` | `<TLS redirect, cookies, non-root permissions>` |
| **6. Queue & Scheduler Readiness** | `<Status>` | `<Graceful worker restart & overlap locks>` |
| **7. Health & Readiness Checks** | `<Status>` | `</health and /ready endpoints verified>` |
| **8. Rollback Procedure** | `<Status>` | `<Artifact + schema rollback steps documented>` |
| **9. Post-Deploy Smoke Test Plan** | `<Status>` | `<Critical path smoke checks defined>` |

## 2. Release Risk Assessment & Rollback Runbook
- **Risk Level**: `<Low | Medium | High>`
- **Pre-Deploy Steps**: `<1. Verify backup... 2. Apply config...>`
- **Rollback Steps**: `<Exact commands to revert artifact and migrations>`
- **Post-Deploy Smoke Tests**: `<1. GET /health -> 200... 2. Verify login...>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Consumes pipeline verification from `ci-cd-release-engineering` (`SKILL-31`), config validation from `environment-configuration-management` (`SKILL-32`), health/logging checks from `observability-incident-diagnosis` (`SKILL-34`), and backup readiness from `backup-recovery-disaster-preparedness` (`SKILL-35`).
- **Downstream Skills**: Directly integrates with and supplies the operational readiness assessment to `final-quality-gate` (`SKILL-38`).

## 12. Source References

- **Shared Deployment Readiness & Quality Gate Matrix**: [../../references/deployment-readiness-quality-gate-matrix.md](../../references/deployment-readiness-quality-gate-matrix.md)
- **Google SRE Book (Release Engineering & Reliable Launches)**: https://sre.google/sre-book/release-engineering/
