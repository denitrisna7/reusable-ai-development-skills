---
name: environment-configuration-management
description: "Manages dev/staging/prod environment parity, .env validation, secret isolation, and safe production defaults (DEBUG=false). Use for config/secrets. Do not use for CI YAML syntax."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-32"
  category: "Performance, Operations, and Deployment"
---

# Environment & Configuration Management

This skill governs how applications separate, validate, store, and inject configuration and secrets across development, testing, staging, and production environments. It enforces fail-fast configuration validation at startup, strict environment parity, secure production defaults, and technical safeguards that prevent credentials from leaking into version control, logs, error pages, or client-side JavaScript bundles.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Creating, updating, or auditing `.env.example`, configuration modules, or environment variable schemas.
- Separating configuration across development, isolated test, staging, and production environments.
- Integrating secret managers (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, Doppler, encrypted credentials) or rotating secrets.
- Implementing fail-fast startup validation for required environment variables and runtime versions.
- Auditing frontend/fullstack builds (`NEXT_PUBLIC_`, `VITE_`, `PUBLIC_`, `REACT_APP_`) to prevent server secrets from leaking into browser bundles.
- Diagnosing configuration drift or missing environment variables between local and deployed environments.

## 2. When Not to Use

Do not activate this skill when the task is strictly limited to:
- Authoring CI/CD workflow YAML pipelines or runner orchestration (route to `ci-cd-release-engineering`, `SKILL-31`).
- Designing user authentication flows, password hashing, or RBAC rules (route to `application-security-owasp`, `SKILL-10`).
- Evaluating overall release go/no-go status across all 15 engineering domains (route to `deployment-readiness`, `SKILL-33`, and `final-quality-gate`, `SKILL-38`).

## 3. Scope and Objectives

Every environment and configuration implementation under this skill must cover:
- **Development, Staging, & Production Separation**: Strictly isolating credentials, databases, cache namespaces, storage buckets, and third-party API accounts (sandbox vs. live) per environment.
- **Structured Environment Variables**: Centralizing all environment variable reads into typed configuration modules rather than scattering raw `process.env`, `os.getenv`, or `env()` calls across business logic.
- **Secret Storage**: Storing sensitive credentials in dedicated secret managers, encrypted platform stores, or runtime-injected environment variables, never in source code or committed files.
- **Fail-Fast Configuration Validation**: Validating the presence, type, format (URL, port, enum, minimum key length), and cross-field constraints of all required configuration at application boot before serving traffic.
- **Runtime Compatibility**: Pinning and validating language runtime, OS/libc, and required system extension versions across local, CI, and production environments.
- **Environment Parity**: Keeping backing service engines and major versions (e.g., PostgreSQL 16, Redis 7) consistent across development, staging, and production to avoid environment-specific bugs.
- **Configuration Drift Prevention**: Maintaining `.env.example` and infrastructure/config manifests as a synchronized, tested contract so newly added variables never cause surprise production crashes.
- **Secure Defaults**: Defaulting all security-sensitive toggles (`DEBUG=false`, strict TLS verification, restrictive CORS origins, secure cookies, production error masking) to their safest posture when unset.
- **Preventing Secret Exposure**: Blocking secrets from entering Git history, build artifacts, client-side JavaScript bundles, debug stack traces, or health/diagnostic endpoints.

## 4. Prerequisites and Context Requirements

Before modifying configuration or environment handling, inspect:
1. **Existing Config Architecture**: Locate `.gitignore`, `.env.example`, `config/` directories, container manifests (`Dockerfile`, `docker-compose.yml`), and runtime pinning files (`.nvmrc`, `.python-version`, `composer.json`, `rust-toolchain.toml`).
2. **Client vs. Server Boundary**: In full-stack or frontend frameworks, identify which environment variable prefixes (`NEXT_PUBLIC_`, `VITE_`, `NUXT_PUBLIC_`, `EXPO_PUBLIC_`) are statically inlined into public client bundles.
3. **Deployment Target**: Confirm how configuration is injected at runtime (platform environment variables, Kubernetes Secrets/ConfigMaps, systemd unit files, or cloud secret manager SDKs).

## 5. Step-by-Step Workflow

### Step 1: Audit Repository for Exposed Secrets and `.gitignore` Coverage
- [ ] Verify `.gitignore` (and `.dockerignore`) explicitly excludes `.env`, `.env.*` (while allowing `!.env.example` and `!.env.test.example`), private keys (`*.pem`, `*.key`), and local credential files (`service-account*.json`).
- [ ] Scan code for hardcoded API keys, JWT secrets, database passwords, webhook signing keys, or private URLs, and move them immediately to environment variables.

### Step 2: Centralize Configuration and Eliminate Raw Env Reads
- [ ] Route all environment variable lookups through a single typed configuration layer (`config/*.php` in Laravel, `@t3-oss/env` / Zod schema in TypeScript, `pydantic-settings` in Python, typed struct in Go/Rust).
- [ ] Prohibit calling raw `env('KEY')` inside controllers, services, or views (in frameworks like Laravel where `config:cache` causes direct `env()` calls to return `null` in production).

### Step 3: Implement Fail-Fast Startup Validation & Secure Defaults
- [ ] Define a strict startup validation schema covering every required variable:
  - Validate data types (`int`, `bool`, `url`, `email`, strict `enum` for `APP_ENV` / `NODE_ENV` in `['development', 'test', 'staging', 'production']`).
  - Enforce cryptographic minimum lengths on signing keys (`APP_KEY`, `JWT_SECRET`, `SESSION_SECRET` `>= 32` high-entropy bytes).
  - Fail immediately at process startup with a clear diagnostic message listing missing or invalid keys (never print the secret values themselves).
- [ ] Configure **Secure-by-Default Fallbacks**:
  - `DEBUG` / `APP_DEBUG` defaults to `false` unless explicitly set in local development.
  - Session/auth cookies default to `Secure=true`, `HttpOnly=true`, and `SameSite=Lax` (or `Strict`).
  - CORS `Access-Control-Allow-Origin` defaults to an explicit allowlist, never `*` with credentials.

### Step 4: Enforce Client-Side Bundle Isolation
- [ ] Audit every variable prefixed with `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`, `NUXT_PUBLIC_`, or `PUBLIC_`.
- [ ] Ensure **zero** database URLs, private API keys, OpenAI/Anthropic/Gemini server keys, Stripe secret keys (`sk_...`), or webhook secrets use public prefixes or are imported by client-rendered components.
- [ ] In Next.js/Remix/SvelteKit, enforce server-only module guards (`import 'server-only'` or `$env/static/private`) on server configuration modules.

### Step 5: Synchronize `.env.example` and Verify Parity
- [ ] Update `.env.example` whenever any configuration key is added, renamed, or removed.
- [ ] Document each variable in `.env.example` with a comment explaining its purpose, expected format, whether it is required in production, and safe dummy placeholder values (e.g., `STRIPE_SECRET_KEY=sk_test_placeholder_replace_me`).
- [ ] Add an automated CI check or startup test verifying that every key in `.env.example` is recognized by the central configuration schema and vice versa (drift detection).
- [ ] Verify runtime compatibility across `composer.json` / `package.json` `engines`, `.nvmrc` / `.python-version`, `Dockerfile` base image tags, and CI runner versions.

### Step 6: Configure Secret Manager Integration & Rotation Support
- [ ] For staging and production environments, inject secrets from dedicated secret vaults (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, HashiCorp Vault, or encrypted platform secrets) rather than manually editing files on servers.
- [ ] Design authentication and webhook verification modules to accept a primary and secondary key during rotation windows so rotating a secret never drops in-flight requests.

## 6. Technology-Specific Adaptation Rules

- **PHP (Laravel / Symfony / CodeIgniter)**: Access configuration exclusively via `config('services.stripe.secret')`, never `env()` outside `config/*.php`. Ensure `APP_DEBUG=false` in production, validate required keys in `AppServiceProvider::boot()`, and test compatibility with `php artisan config:cache`.
- **JavaScript / TypeScript (Next.js / React / Vite / Node.js)**: Validate `process.env` at startup using `zod` (`@t3-oss/env-nextjs` or custom schema). Strictly separate server secrets from `NEXT_PUBLIC_*` / `VITE_*` variables, and guard server config files with `import 'server-only'`.
- **Python (Django / FastAPI / Flask)**: Use `pydantic-settings` (`BaseSettings`) or `django-environ` / `environs` with strict type validation. In Django, ensure `DEBUG = False` by default, require `SECRET_KEY` and explicit `ALLOWED_HOSTS` from the environment in production, and enable `SECURE_SSL_REDIRECT` and `SESSION_COOKIE_SECURE`.
- **Go**: Use typed config structs with `env` / `envconfig` tags and validate required fields in `main()` before binding HTTP listeners.
## 6. Technology-Specific Adaptation Rules

Adapt configuration management to the project's actual ecosystem. Never force PHPStan, Pint, Pest, shadcn/ui, or Playwright where inapplicable:
- **PHP (Laravel / Symfony / CodeIgniter)**: In Laravel, access configuration exclusively via `config('services.stripe.secret')`, never `env()` outside `config/*.php`. Ensure `APP_DEBUG=false` by default in `config/app.php`, validate required production keys in `AppServiceProvider::boot()`, and test compatibility with `php artisan config:cache`. In CodeIgniter 4, use typed `Config\*` classes extending `CodeIgniter\Config\BaseConfig` with `CI_ENVIRONMENT = production` as the safe production setting.
- **JavaScript / TypeScript (Next.js / React / Vue / Vite / Node.js)**: Validate `process.env` / `import.meta.env` at startup using `zod` (`@t3-oss/env-nextjs` or custom schema module). Strictly separate server-only secrets from `NEXT_PUBLIC_*`, `VITE_*`, or `NUXT_PUBLIC_*` variables, and guard server config files with `import 'server-only'`.
- **Python (Django / FastAPI / Flask)**: Use `pydantic-settings` (`BaseSettings` with `SettingsConfigDict`) or `django-environ` / `environs` with strict type validation. In Django, ensure `DEBUG = False` by default, require `SECRET_KEY` and explicit `ALLOWED_HOSTS` from the environment in production, and enable `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, and `CSRF_COOKIE_SECURE`.
- **Go**: Use typed config structs with `caarlos0/env` or `kelseyhightower/envconfig` struct tags (`env:"DATABASE_URL,required,notEmpty"`), and validate all required fields in `main()` before binding HTTP/gRPC listeners.
- **Java / Spring Boot**: Use `@ConfigurationProperties(prefix = "app")` combined with `@Validated` (`@NotBlank`, `@NotNull`, `@Min`) so the Spring context fails fast on boot if any required property is missing or malformed. Keep sensitive properties in environment variables or Vault/Secret Manager rather than committed `application.properties`.
- **Rust**: Deserialize environment variables into strongly typed structs using `config` or `envy` + `serde`, wrapping sensitive fields in `secrecy::SecretString` so they cannot be accidentally printed via `Debug` or `Display` traits, and fail fast in `main()`.
- **C# / .NET**: Bind configuration to strongly typed classes using `services.AddOptions<AppSettings>().BindConfiguration("App").ValidateDataAnnotations().ValidateOnStart()`. Use `dotnet user-secrets` for local development rather than placing secrets in `appsettings.Development.json`.
- **Mobile / Flutter**: Never treat `--dart-define`, `.env` asset bundles, or native `Info.plist` / `AndroidManifest.xml` entries as secret storage; any value shipped inside an APK/AAB/IPA binary is public to reverse engineering. Store only public environment endpoints (`API_BASE_URL`, public publishable keys) in build flavors, and proxy private API calls through an authenticated backend.
- **Unknown or Mixed Stacks**: Implement a dedicated startup bootstrap script or entrypoint check (`check-env.sh` or config loader) that verifies required environment variables are non-empty and properly formatted before launching the main process.

## 7. Security and Safety Considerations

- **Never Log Configuration Dumps**: When startup validation fails or debug endpoints run, log only the *names* and validation error reasons of missing or invalid environment variables, never the resolved secret values or a full dump of `process.env`.
- **Immediate Secret Rotation on Exposure**: If a real credential was ever committed to Git history or exposed in logs/bundles, deleting the line in a subsequent commit does not secure the key. Flag the credential immediately for revocation and rotation in the provider dashboard.
- **Isolate Test Environment Config**: Ensure automated test suites (`phpunit.xml`, `vitest.config.ts`, `pytest.ini`) forcibly override `APP_ENV=testing` / `NODE_ENV=test` and point to an isolated in-memory or ephemeral test database and mock mail/payment drivers so running tests can never wipe development/production databases or charge real cards.
- **Restrict File Permissions on Deployed `.env` Files**: On VM or bare-metal deployments that use `.env` files on disk, enforce `chmod 600 .env` owned by the service account and block web server access to dotfiles (`location ~ /\. { deny all; }` in Nginx).

## 8. Verification Criteria

Before marking environment and configuration work complete, verify:
1. **Zero Hardcoded Secrets**: Static scan confirms no raw API keys, passwords, or private tokens exist in source code or committed config files.
2. **Startup Fail-Fast Works**: Booting the application with a required secret unset exits immediately with a clear, non-leaky validation error.
3. **Config Caching & Bundle Safety**: Framework config caching (`config:cache` or production bundler build) succeeds without leaking server secrets into public client assets.
4. **`.env.example` Parity**: Every environment variable referenced across all config modules is documented with safe placeholders in `.env.example`.
5. **Test Isolation Confirmed**: Running the test suite does not read or mutate the local development or staging database configured in `.env`.

## 9. Failure Handling and Edge Cases

- **Multi-Stage Docker Builds Needing Build-Time Public Vars**: Distinguish between build-time public variables (`ARG NEXT_PUBLIC_API_URL`) and runtime server secrets; never bake server secrets into Docker image layers via `ENV` or `ARG` in `Dockerfile` (use runtime environment injection or BuildKit `--mount=type=secret`).
- **Boolean String Parsing Traps**: In many languages, `"false"` or `"0"` as a non-empty string evaluates to truthy (`Boolean("false") === true` in JS; `bool("False") === True` in Python). Always parse boolean environment variables explicitly (`['true', '1', 'yes'].includes(val.toLowerCase())`).
- **Secret Rotation Without Downtime**: Support dual-key verification windows (e.g., `JWT_SECRET_CURRENT` and `JWT_SECRET_PREVIOUS`, or webhook signing key arrays) when rotating cryptographic signing secrets on live systems.

## 10. Expected Outputs and Reporting Requirements

Deliver updated configuration files and `.env.example` alongside an **Environment & Configuration Audit Report**:

```markdown
# Environment & Configuration Management Report

## 1. Configuration Schema & Validation
- **Central Config Module(s)**: `<path to config schema/files>`
- **Fail-Fast Validation Mechanism**: `<e.g., Zod schema / Pydantic BaseSettings / ServiceProvider check>`
- **Runtime Version Pinning**: `<e.g., Node 22.x in package.json, .nvmrc, and Dockerfile>`

## 2. Environment Variable Inventory
| Variable Name | Scope (`Server` / `Public Client`) | Required in Prod? | Default / Fallback | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `<DATABASE_URL>` | `Server Only` | `Yes (Fail-Fast)` | `None` | `<Primary DB connection string>` |
| `<APP_DEBUG>` | `Server Only` | `No` | `false` | `<Debug mode toggle (safe default)>` |

## 3. Secret Hygiene & Parity Checks
- **`.gitignore` & `.dockerignore` Verified**: `<Pass | Details>`
- **Client Bundle Leak Audit**: `<Verified zero server secrets in NEXT_PUBLIC_/VITE_>`
- **`.env.example` Synchronization**: `<Updated and verified>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Receives security posture requirements from `application-security-owasp` (`SKILL-10`) and third-party credential needs from `api-external-service-integration` (`SKILL-27`) and `ai-provider-integration` (`SKILL-28`).
- **Downstream Skills**: Provides verified configuration contracts to `ci-cd-release-engineering` (`SKILL-31`), `deployment-readiness` (`SKILL-33`), `documentation-developer-handoff` (`SKILL-37`), and `final-quality-gate` (`SKILL-38`).

## 12. Source References

- **The Twelve-Factor App (III. Config & X. Dev/prod parity)**: https://12factor.net/config
- **OWASP Secrets Management Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- **OWASP Top 10 A05:2021 Security Misconfiguration**: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
