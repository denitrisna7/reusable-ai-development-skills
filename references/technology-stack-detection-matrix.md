# Technology Stack Detection & Adaptation Matrix

This reference provides a deterministic lookup table for inspecting an existing repository before recommending tools, patterns, or commands. **Never assume a default stack.** Always verify the presence of manifest files, lockfiles, configuration files, and directory structures first.

---

## 1. Language, Framework, and Tooling Matrix

| Ecosystem | Manifest & Lockfiles | Framework Indicators | Static Analysis & Formatting | Testing Tools | Database & ORM Indicators |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PHP (Laravel)** | `composer.json`, `composer.lock` | `artisan`, `bootstrap/app.php`, `config/app.php`, `laravel/framework` | PHPStan / Larastan (`phpstan.neon`), Laravel Pint (`pint.json`), PHP_CodeSniffer (`phpcs.xml`), Psalm | Pest (`pestphp/pest`), PHPUnit (`phpunit.xml`), Laravel Dusk | Eloquent (`app/Models/`), `database/migrations/`, `config/database.php` |
| **PHP (CodeIgniter)** | `composer.json`, `composer.lock` | `spark` (CI4), `app/Config/Paths.php` (CI4), `system/core/CodeIgniter.php` (CI3) | PHPStan (`phpstan.neon`), PHP-CS-Fixer (`.php-cs-fixer.dist.php`), PHP_CodeSniffer | PHPUnit (`phpunit.xml.dist`, `tests/`) | CI4 Models (`app/Models/`), Query Builder (`$db->table()`), `app/Database/Migrations/` |
| **PHP (Symfony)** | `composer.json`, `composer.lock`, `symfony.lock` | `bin/console`, `config/bundles.php`, `symfony/framework-bundle` | PHPStan, Psalm, PHP-CS-Fixer, TwigCS | PHPUnit (`bin/phpunit`), Behat, Panther | Doctrine ORM (`config/packages/doctrine.yaml`, `migrations/`) |
| **JavaScript / TypeScript (React / Next.js)** | `package.json`, `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `bun.lockb` | `next.config.{js,mjs,ts}`, `app/` or `pages/`, `react`, `react-dom` | TypeScript (`tsconfig.json`), ESLint (`eslint.config.mjs`), Biome (`biome.json`), Prettier | Vitest, Jest, React Testing Library, Playwright (`playwright.config.ts`), Cypress | Prisma (`prisma/schema.prisma`), Drizzle (`drizzle.config.ts`), TypeORM, Mongoose |
| **JavaScript / TypeScript (Vue / Nuxt / Vite)** | `package.json` + lockfile | `nuxt.config.ts`, `vite.config.ts`, `vue`, `*.vue` components | `vue-tsc`, ESLint, Oxlint, Prettier | Vitest, `@vue/test-utils`, Playwright | Prisma, Drizzle, Pinia / Vuex state stores |
| **JavaScript / TypeScript (Backend: Node / NestJS / Express)** | `package.json` + lockfile | `nest-cli.json`, `@nestjs/core`, `express`, `fastify`, `hono` | `tsc --noEmit`, ESLint, Biome | Jest, Vitest, Supertest | Prisma, Drizzle, TypeORM, Sequelize, Knex, `pg`, `mysql2` |
| **Python (Django / FastAPI / Flask)** | `pyproject.toml`, `uv.lock`, `poetry.lock`, `Pipfile.lock`, `requirements.txt` | `manage.py` (Django), `fastapi`, `flask`, `asgi.py`, `wsgi.py` | Ruff (`ruff.toml`), Flake8, Black, mypy (`mypy.ini`), Pyright | pytest (`pytest.ini`, `conftest.py`), `unittest`, Hypothesis | Django ORM (`models.py`, `migrations/`), SQLAlchemy + Alembic (`alembic.ini`), Tortoise ORM |
| **Go** | `go.mod`, `go.sum`, `go.work` | `cmd/`, `internal/`, `pkg/`, `gin`, `echo`, `fiber`, `chi`, `net/http` | `go vet`, `staticcheck`, `golangci-lint` (`.golangci.yml`), `gofmt` | `go test ./...`, testify | `sqlc` (`sqlc.yaml`), GORM, `ent`, `pgx`, `golang-migrate`, `goose` |
| **Java / Kotlin (Spring Boot / Gradle / Maven)** | `pom.xml`, `build.gradle`, `build.gradle.kts`, `gradle.properties` | `@SpringBootApplication`, `src/main/resources/application.{yml,properties}` | Checkstyle, SpotBugs, PMD, Detekt, Ktlint, ErrorProne | JUnit 5, Mockito, Spring Boot Test, Testcontainers | Spring Data JPA / Hibernate, jOOQ, MyBatis, Flyway, Liquibase |
| **Rust** | `Cargo.toml`, `Cargo.lock` | `src/main.rs`, `src/lib.rs`, `axum`, `actix-web`, `tokio`, `tauri` | `cargo check`, `cargo clippy`, `rustfmt` (`rustfmt.toml`) | `cargo test`, `cargo nextest` | SQLx (`sqlx-data.json`), Diesel (`diesel.toml`), SeaORM |
| **C# / .NET** | `*.sln`, `*.csproj`, `Directory.Build.props`, `packages.lock.json` | `Program.cs`, `appsettings.json`, ASP.NET Core | Roslyn Analyzers (`.editorconfig`), `dotnet format` | xUnit, NUnit, MSTest, WebApplicationFactory | Entity Framework Core (`Migrations/`), Dapper |
| **Ruby (Rails)** | `Gemfile`, `Gemfile.lock` | `config/application.rb`, `bin/rails`, `app/controllers/` | RuboCop (`.rubocop.yml`), Brakeman (security), Sorbet | RSpec (`spec/`), Minitest (`test/`), Capybara | ActiveRecord (`db/schema.rb`, `db/migrate/`) |
| **Mobile & Cross-Platform (Flutter / Android / iOS)** | `pubspec.yaml` (Flutter), `build.gradle.kts` (Android), `Package.swift` / `*.xcodeproj` (iOS) | `lib/main.dart`, `AndroidManifest.xml`, `Info.plist` | `dart analyze`, Android Lint, SwiftLint | `flutter test`, Espresso, XCTest | Drift / sqflite (Flutter), Room (Android), CoreData / SwiftData (iOS) |

---

## 2. UI & Styling System Detection

Before proposing UI components or styling modifications, inspect the repository for existing UI systems:

| Indicator | Detected UI / Styling System | Adaptation Rule |
| :--- | :--- | :--- |
| `components.json` + `@radix-ui/*` or `@base-ui-components/*` + Tailwind CSS | **shadcn/ui** | Follow existing `components/ui/` open-code structure, CSS variable tokens in globals CSS, and `cn()` utility conventions. |
| `tailwind.config.{js,ts,cjs}` or `@import "tailwindcss"` without `components.json` | **Tailwind CSS (Custom or Headless UI)** | Use the project's existing Tailwind theme tokens and utility patterns; do not install shadcn/ui unless requested. |
| `@mui/material` in `package.json` | **Material UI (MUI)** | Use MUI `ThemeProvider`, `sx` prop, and MUI components. Do not mix Tailwind or shadcn/ui. |
| `@chakra-ui/react` or `@mantine/core` or `antd` | **Chakra / Mantine / Ant Design** | Use the active component library's primitives, theme tokens, and form wrappers. |
| `resources/views/**/*.blade.php` + Livewire / Alpine / Filament / Bootstrap | **Laravel Blade / Livewire / Filament** | Follow Blade component conventions (`<x-...>`), Livewire wire directives, or Filament schemas. |
| `app/Views/**/*.php` in CodeIgniter | **CodeIgniter Views** | Follow existing PHP view templates, layout sections, and CSS framework (Bootstrap, Tailwind, or custom CSS) already loaded. |

---

## 3. CI/CD and Infrastructure Detection

| Path / File | Platform |
| :--- | :--- |
| `.github/workflows/*.{yml,yaml}` | GitHub Actions |
| `.gitlab-ci.yml` | GitLab CI/CD |
| `Jenkinsfile` | Jenkins |
| `.circleci/config.yml` | CircleCI |
| `azure-pipelines.yml` | Azure DevOps Pipelines |
| `bitbucket-pipelines.yml` | Bitbucket Pipelines |
| `Dockerfile`, `docker-compose.yml`, `compose.yaml` | Docker / Containerized Runtime |
| `k8s/`, `helm/`, `Chart.yaml` | Kubernetes / Helm |
| `terraform/`, `*.tf`, `pulumi/` | Infrastructure as Code (Terraform / Pulumi) |

---

## 4. Handling Unknown or Mixed Technology Stacks

When a repository contains an unfamiliar framework, custom internal tooling, or a polyglot monorepo:
1. **Inspect Entrypoints and Scripts**: Read `Makefile`, `justfile`, `Taskfile.yml`, `package.json` scripts, `composer.json` scripts, and CI workflow steps to see how the project is actually built, linted, and tested.
2. **Distinguish Verified Facts from Assumptions**: Explicitly list what was confirmed from files versus what remains unknown.
3. **Never Force Foreign Tooling**: Do not introduce tools from another ecosystem (e.g., do not run npm linters in a pure Go project, or force Laravel Pint onto a legacy CodeIgniter 3 codebase).
