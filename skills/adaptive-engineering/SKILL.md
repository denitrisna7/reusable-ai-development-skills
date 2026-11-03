---
name: adaptive-engineering
description: "Mandatory lifecycle skill (SKILL-06). Enforces repository idioms, framework conventions, runtime versions, and clean code craftsmanship. Part of the 38-skill quality suite."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-06"
  category: "Core Development Quality"
---

# Language and Framework Adaptive Engineering

This skill governs how application code is written and integrated so that every change looks and behaves like a native part of the target repository. It prevents cross-stack contamination, deprecated API usage, and version-incompatible syntax by requiring engineers to match the project's verified language version, framework idioms, directory conventions, error-handling patterns, and active toolchain. When encountering unfamiliar frameworks, bleeding-edge versions, or custom internal platforms, it enforces consulting authoritative documentation and existing codebase examples before writing code.

## 1. Activation Conditions

Activate this skill under any of the following scenarios:
- Writing new features, endpoints, services, CLI commands, background jobs, or UI components in any programming language or framework.
- Modifying existing modules where adherence to local naming, dependency injection, state management, and error-handling conventions is required.
- Working in repositories pinned to specific language or framework versions (e.g., PHP 8.1 vs. 8.4, Laravel 10 vs. 11, CodeIgniter 3 vs. 4, React 18 vs. 19, Next.js Pages vs. App Router, Python 3.10 vs. 3.13, Go 1.21 vs. 1.23).
- Implementing changes in polyglot monorepos where backend, frontend, worker, and infrastructure code each follow distinct ecosystem standards.
- Working in unknown, proprietary, or legacy environments where modern framework assumptions would break the build.

## 2. When Not to Use

Do not use this skill in the following situations:
- The repository has not yet been inspected to determine its language, framework, and runtime version; run [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`) first.
- Designing high-level system boundaries or evaluating macro-architectural trade-offs before implementation; run [`adaptive-architecture`](../adaptive-architecture/SKILL.md) (`SKILL-03`) first.
- Running standalone linting, formatting, and static type-check gates after implementation; route to [`code-quality-static-analysis`](../code-quality-static-analysis/SKILL.md) (`SKILL-07`).
- Auditing third-party package vulnerabilities and lockfiles; route to [`dependency-supply-chain-security`](../dependency-supply-chain-security/SKILL.md) (`SKILL-09`).

## 3. Scope and Objectives

Every implementation task governed by this skill must explicitly address the following eight engineering areas:
- **Language-specific conventions**: Idiomatic syntax, type system usage, naming conventions (`PSR-12`/`PER-CS` for PHP, `PEP 8` for Python, `Effective Go` for Go, Rust ownership idioms), and memory/resource management (`defer`, `using`, `with`, RAII).
- **Framework-specific practices**: Using native framework lifecycle hooks, routing, dependency injection, validation, ORM scopes, middleware, and localization mechanisms instead of reinventing them.
- **Version compatibility**: Verifying that every language feature, standard library function, and framework API used is supported by the exact version constraints declared in the project's manifest and lockfiles.
- **Existing project patterns**: Matching the surrounding codebase's file placement, helper utilities, DTO/response envelopes, logging format, and configuration access patterns.
- **Appropriate tooling selection**: Invoking only the package manager, build tool, test runner, and code generator configured for the active workspace.
- **Avoiding stack assumptions**: Never importing tools, libraries, or paradigms from another ecosystem (e.g., never assuming Laravel helpers exist in CodeIgniter, or assuming `shadcn/ui` exists in a Material UI React project).
- **Consulting official documentation**: Verifying unfamiliar APIs, major version migration changes (such as Laravel 10 to 11 bootstrap changes or Next.js 15 async request APIs), and library signatures against official documentation or installed type definitions before coding.
- **Handling unknown or unsupported environments**: Inspecting local source files, internal SDK definitions, and build scripts when working with custom frameworks or niche runtimes, and stating constraints clearly when runtime tools are unavailable.

## 4. Prerequisites and Context Requirements

- Verified stack, runtime version, and lockfile inventory from [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`) and the [Technology Stack Detection Matrix](../../references/technology-stack-detection-matrix.md).
- Read access to neighboring files in the target directory to observe local coding idioms before editing.
- Access to installed package declarations (`vendor/`, `node_modules/`, lockfiles, or official docs) to confirm exact method signatures and version numbers.

## 5. Step-by-Step Workflow

Follow this five-step engineering workflow whenever writing or modifying application code:

### Step 1: Verify Runtime and Framework Version Constraints
1. Check the exact language and framework versions pinned in the repository (`composer.json` + `composer.lock`, `package.json` + lockfile, `pyproject.toml`, `go.mod`, `Cargo.toml`, `*.csproj`, `pom.xml`/`build.gradle.kts`, `pubspec.yaml`).
2. Note version-specific boundaries before writing a single line of code:
   - **PHP / Laravel / CodeIgniter / Symfony**: Do not use PHP 8.3 typed class constants or `json_validate()` if the project targets `"php": "^8.1"`. Do not use Laravel 11 `bootstrap/app.php` routing callbacks in a Laravel 9/10 project that uses `app/Http/Kernel.php` and `app/Providers/RouteServiceProvider.php`. Distinguish CodeIgniter 4 namespaced classes (`App\Controllers\BaseController`) from CodeIgniter 3 (`CI_Controller`).
   - **JavaScript / TypeScript / React / Next.js / Vue**: Check whether `next` is v13/14 or v15+ (where `params`, `searchParams`, `cookies()`, and `headers()` are asynchronous Promises) and whether routes live under `app/` or `pages/`. Check whether React is v18 (`forwardRef` required) or v19 (`ref` as a standard prop).
   - **Python / Django / FastAPI**: Check whether `pydantic` is v1 (`.dict()`, `@validator`) or v2 (`.model_dump()`, `@field_validator`, `ConfigDict`), and whether SQLAlchemy uses 1.x `session.query()` or 2.0 `select()` syntax.
   - **Go / Rust / Java / .NET**: Check `go.mod` version (e.g., whether `slices`/`maps` stdlib packages or enhanced `http.ServeMux` routing patterns in Go 1.22+ are available), Rust edition (`2021` vs `2024`), and Java/Kotlin or .NET target framework version.

### Step 2: Sample Local Neighborhood Patterns
1. Read 2 to 3 existing files in the same module or layer (e.g., two existing controllers, two existing services, two existing UI forms) before creating or editing a file.
2. Record and replicate the repository's established conventions for:
   - Imports and module organization (absolute aliases like `@/` vs. relative paths, namespace casing).
   - Input validation and error signaling (custom domain exceptions vs. result objects vs. framework validation errors).
   - Response formatting (API Resource classes, standardized `{ data, meta, error }` envelopes, or typed DTOs).
   - Shared utilities (date/time libraries, currency/money types, logger instances, translation helpers).

### Step 3: Consult Installed Types and Authoritative Documentation
1. When calling a framework method, ORM query builder, or third-party SDK whose signature or behavior is not 100% certain, inspect the installed type definitions/source in the workspace or consult official documentation.
2. Never hallucinate configuration keys, CLI flags, or method names. Verify that every imported symbol exists in the installed package version.

### Step 4: Implement Using Native Ecosystem Idioms
1. Write clean, cohesive code that leverages the framework's built-in capabilities rather than fighting them.
2. Enforce strict resource and concurrency safety:
   - Always propagate cancellation/timeout contexts (`context.Context` in Go, `AbortSignal` in JS/TS, `CancellationToken` in C#).
   - Always close or scope file handles, streams, and database transactions deterministically (`try/finally`, `with`, `using`, `defer`, `DB::transaction()`).
3. Apply [`ai-anti-slop`](../ai-anti-slop/SKILL.md) (`SKILL-05`) discipline: zero placeholder stubs, zero dead controls, and high-signal comments only.

### Step 5: Execute Ecosystem-Native Verification
1. Run the project's native compiler, type checker, linter, and targeted tests using the exact package manager or wrapper script configured in the workspace (`./gradlew`, `./mvnw`, `pnpm`, `composer`, `uv run`, `cargo`).
2. Confirm that no foreign lockfiles, untracked temp scripts, or cross-ecosystem artifacts were created.

### Adaptive Engineering Checklist
- [ ] Language version and framework major version verified from manifests/lockfiles.
- [ ] Neighboring files inspected to match local naming, structure, and error conventions.
- [ ] Framework APIs and SDK method signatures verified against installed definitions or official docs.
- [ ] Native framework mechanisms used instead of ad-hoc custom reimplementations.
- [ ] No foreign tools, unrequested UI libraries, or wrong package managers invoked.
- [ ] Code compiled/checked and verified with the project's native toolchain.

## 6. Technology-Specific Adaptation Rules

Follow these ecosystem-specific adaptation rules strictly:
- **PHP (Laravel)**: Match the project's Laravel major version (`8.x` through `12.x`). Use Eloquent relationships and scopes, FormRequests, Policies/Gates, API Resources, `DB::transaction()`, and `config()` (never call `env()` outside `config/*.php` because config caching breaks direct `env()` calls in production).
- **PHP (CodeIgniter 3 & 4)**: In CI4, use namespaces (`App\Controllers`, `App\Models`), `$this->validateData()`, `Config\Services`, and CI4 Entities/Migrations. In legacy CI3, respect `$this->load->model()`, `$this->input->post()`, `$this->form_validation`, and CI3's non-namespaced class loading. Never copy Laravel `artisan` or Eloquent syntax into CodeIgniter.
- **PHP (Symfony)**: Use constructor autowiring, Symfony Validator attributes/constraints, Voters for authorization, Doctrine repositories/migrations, and Messenger for queues.
- **JavaScript / TypeScript (React / Next.js / Vue / Node)**:
  - Use the exact package manager matching the lockfile (`pnpm`, `npm`, `yarn`, or `bun`).
  - In React/Next.js, preserve `"use client"` / `"use server"` boundaries and match the active styling system (`shadcn/ui` + Tailwind only if `components.json` exists; otherwise respect MUI, Chakra, CSS Modules, or plain Tailwind).
  - In Vue/Nuxt, match Options API vs. Composition API (`<script setup lang="ts">`) as used in the repo.
- **Python (Django / FastAPI / Flask)**: Match Pydantic v1 vs. v2 in FastAPI, sync vs. async views/ORM calls in Django, and always run commands inside the project's active virtual environment (`uv`, `poetry`, `pipenv`, or `.venv`).
- **Go**: Follow standard Go formatting (`gofmt`), explicit `if err != nil` error wrapping (`fmt.Errorf("...: %w", err)`), `context.Context` as the first parameter on I/O functions, and race-free goroutine lifecycle management.
- **Java / Kotlin (Spring Boot) & C# (.NET)**: Use constructor injection over field injection (`@Autowired`), respect nullable annotations/types, use configured database migration tools (`Flyway`/`Liquibase`/`EF Core`), and invoke `./gradlew` or `./mvnw` wrappers.
- **Rust**: Prefer idiomatic borrowing, `?` error propagation with the project's error crate (`thiserror` for libraries, `anyhow` for applications if already present), and avoid `.unwrap()` / `.expect()` on fallible runtime inputs.
- **Mobile (Flutter / Android / iOS)**: Follow the existing state management pattern (`Riverpod`, `Bloc`, `Provider`, `Jetpack ViewModel`, `SwiftUI Observable`), platform theming, and lifecycle-safe async updates (checking `mounted` in Flutter before using `BuildContext` across async gaps).
- **Unknown, Custom, or Mixed Environments**:
  - Inspect `Makefile`, `Justfile`, `Taskfile.yml`, `Dockerfile`, and `.github/workflows/` to discover how the application is compiled, linted, and started.
  - Read the application's entry file (`index.php`, `main.py`, `main.go`, `server.js`) and trace how requests, dependencies, and database connections are wired before proposing edits.
  - Never introduce npm, Composer, or Docker configurations into a repository that does not use them unless explicitly instructed by the user.

## 7. Security and Safety Considerations

- **Never Use Deprecated or Unsafe Language Functions**: Avoid `eval()`, `unserialize()` on untrusted input in PHP, `pickle.loads()` on untrusted data in Python, `innerHTML` / `dangerouslySetInnerHTML` with unsanitized strings in JS/TS, or raw string-concatenated SQL in any language.
- **Framework Configuration Caching Safety**: Respect framework production compilation rules (such as Laravel `config:cache`, Next.js static prerendering, or Spring AOT) so code does not work locally while failing in production builds.
- **Environment Isolation**: Never execute project commands that connect to remote production databases or mutate live cloud resources during development verification.

## 8. Verification Criteria

Before claiming an implementation task is complete:
1. All modified files use syntax and APIs compatible with the project's declared runtime and framework versions.
2. Code structure, naming, imports, and error handling match neighboring files in the repository.
3. No unapproved dependencies or foreign lockfiles were introduced.
4. Static analysis, type checking, and automated tests in the target ecosystem pass with zero new errors (verified via [`code-quality-static-analysis`](../code-quality-static-analysis/SKILL.md), `SKILL-07`).

## 9. Failure Handling and Edge Cases

- **Missing Local Runtime or Compiler**: If the current environment lacks the required runtime binary (e.g., a Rust or .NET project opened on a machine without `cargo` or `dotnet`, or Docker is not running), inspect the code and types statically, explicitly report that runtime execution was `BLOCKED` by the missing binary, and provide the exact command for the user to run.
- **Inconsistent Patterns Inside the Same Repository**: Many real-world codebases contain both legacy patterns and a newer target pattern. Check `README.md`, `AGENTS.md`, ADRs, or recent git commits (`git log -n 10`) to identify which pattern is the active standard, and follow the active standard for new code.
- **Unsupported or Custom Internal Framework**: Read the framework's bootstrap, router, and base classes directly in the repository to learn its request lifecycle and conventions before making edits.

## 10. Expected Outputs and Reporting Requirements

When reporting completed implementation work, summarize how the changes adapted to the project's stack:

```markdown
## Adaptive Engineering Implementation Summary

- **Detected Stack & Runtime Target**: `<Language Version + Framework Version + Package Manager>`
- **Conventions & Reference Files Matched**: `<2-3 existing repo files used as pattern templates>`
- **Implemented Changes**:
  - `<path/to/file>`: `<Concise summary of logic, patterns, and version-safe APIs used>`
- **Toolchain & Verification Status**:
  - `<Command executed>`: `<PASS / FAIL / BLOCKED with output summary>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - Consumes stack detection from [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`) and design plans from [`adaptive-architecture`](../adaptive-architecture/SKILL.md) (`SKILL-03`).
- **Companion & Downstream Skills**:
  - Enforces craftsmanship and comment/UI quality alongside [`ai-anti-slop`](../ai-anti-slop/SKILL.md) (`SKILL-05`).
  - Hands off modified files to [`code-quality-static-analysis`](../code-quality-static-analysis/SKILL.md) (`SKILL-07`) for linting, formatting, and type-checking verification.
  - Routes legacy code modifications through [`refactoring-legacy-safety`](../refactoring-legacy-safety/SKILL.md) (`SKILL-08`).

## 12. Source References

- Library Reference: [Technology Stack Detection & Adaptation Matrix](../../references/technology-stack-detection-matrix.md)
- Library Reference: [AI Anti-Slop & Engineering Craftsmanship Reference](../../references/anti-slop-engineering-reference.md)
- Standards: [PHP-FIG PER Coding Style](https://www.php-fig.org/per/coding-style/), [PEP 8 Style Guide for Python Code](https://peps.python.org/pep-0008/), [Effective Go](https://go.dev/doc/effective_go)
