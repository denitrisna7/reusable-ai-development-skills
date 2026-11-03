---
name: code-quality-static-analysis
description: "Mandatory lifecycle skill (SKILL-07). Runs stack-native linting, formatting, type checking, complexity bounds, and duplication checks. Part of the 38-skill quality suite."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-07"
  category: "Core Development Quality"
---

# Code Quality & Static Analysis

This skill enforces verifiable code quality across modified and newly authored source files through stack-appropriate linting, formatting, static type checking, error-handling verification, complexity management, and duplication reduction. It adapts strictly to the tools configured in the target repository (for example, using PHPStan and Laravel Pint in applicable PHP/Laravel projects, ESLint/TypeScript/Biome in JS/TS projects, Ruff/mypy/Pyright in Python, or `golangci-lint` in Go) and never forces foreign or unconfigured tools onto a codebase.

## 1. Activation Conditions

Activate this skill under any of the following scenarios:
- Immediately after writing, modifying, or refactoring source code in any programming language to validate formatting, types, and static analysis rules before claiming task completion.
- Performing a dedicated code quality audit, pull request review, or static analysis remediation pass.
- Diagnosing and fixing compiler warnings, type mismatches, unhandled error paths, high cyclomatic complexity, or duplicated code blocks.
- Verifying that code modifications adhere to the repository's configured CI quality gates (`.github/workflows/`, `Makefile`, `composer.json` scripts, `package.json` scripts).

## 2. When Not to Use

Do not use this skill in the following situations:
- The repository's stack and configured quality tools have not yet been identified; inspect manifests first using [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`).
- Designing test suites or running end-to-end browser QA; route to `testing-strategy-design` (`SKILL-15`), `backend-testing-tdd` (`SKILL-16`), or `playwright-mcp-browser-qa` (`SKILL-17`).
- Re-formatting an entire untouched legacy repository in the middle of a small bug fix, which pollutes git diffs and obscures functional changes (`SKILL-08`).
- Auditing third-party CVE advisories and package lockfiles; route to [`dependency-supply-chain-security`](../dependency-supply-chain-security/SKILL.md) (`SKILL-09`).

## 3. Scope and Objectives

Every code quality and static analysis pass must explicitly cover the following ten dimensions:
- **Linting**: Identifying syntax hazards, unused variables/imports, unreachable code, unsafe patterns, and rule violations using the repository's linter.
- **Formatting**: Ensuring consistent indentation, line lengths, import ordering, and brace style aligned with the project's formatter configuration (scoped to modified files unless a repo-wide format is requested).
- **Type checking**: Enforcing explicit parameter, return, and property/variable types, eliminating unsafe `any`/`mixed` escapes where concrete types or generics apply, and verifying null/undefined safety.
- **Static analysis**: Running configured static analyzers at the project's declared strictness level to catch dead branches, invalid method calls, contract violations, and resource leaks before runtime.
- **Error handling**: Verifying that every fallible operation (I/O, network, parsing, database queries, type assertions) is explicitly handled, logged with safe context, or propagated with domain meaning, and never silently swallowed via empty `catch {}` blocks.
- **Maintainability**: Ensuring functions, classes, and modules have clear single responsibilities, descriptive identifiers, and low cognitive load.
- **Code duplication**: Detecting and consolidating copy-pasted validation logic, query filters, transformation helpers, and UI markup within the modified domain scope.
- **Complexity**: Keeping cyclomatic and cognitive complexity bounded by using guard clauses (early returns), decomposing deeply nested conditionals, and extracting focused helper functions.
- **Consistency**: Ensuring modified code matches the surrounding codebase's naming casing, visibility modifiers, strict-types declarations, and module conventions.
- **Validation of modified code**: Executing the actual static analysis, type-check, and syntax-check commands on all touched files and recording concrete command output as evidence.

> **Important Tooling Rule**: Tools such as **PHPStan** (`phpstan` / `larastan`) and **Laravel Pint** (`pint`) are examples for applicable PHP/Laravel projects where they are installed or appropriate. They are **not** universal requirements and must never be forced onto non-PHP projects or PHP projects using another configured standard (such as `PHP-CS-Fixer`, `PHP_CodeSniffer`, or `Psalm`).

## 4. Prerequisites and Context Requirements

- Inspection of the repository's manifest scripts and tool configuration files via the [Technology Stack Detection Matrix](../../references/technology-stack-detection-matrix.md).
- List of modified or newly created files (`git status`, `git diff --name-only`) so quality checks can be targeted accurately.
- Awareness of CI workflow commands (`.github/workflows/*.yml`, `.gitlab-ci.yml`) so local checks match what CI enforces.

## 5. Step-by-Step Workflow

Execute this five-step workflow whenever validating or improving code quality:

### Step 1: Detect the Project's Configured Quality Toolchain
1. Inspect manifest scripts (`package.json`, `composer.json`, `pyproject.toml`, `Makefile`, `Justfile`) and root configuration files (`phpstan.neon*`, `pint.json`, `.php-cs-fixer*`, `phpcs.xml*`, `psalm.xml`, `tsconfig.json`, `eslint.config.*`, `.eslintrc*`, `biome.json`, `.prettierrc*`, `ruff.toml`, `mypy.ini`, `.golangci.yml`, `rustfmt.toml`, `.editorconfig`).
2. Identify the exact commands that CI runs for linting, formatting, and static analysis.
3. If no third-party linter or static analyzer is installed, identify the runtime's native syntax/type verification command (`php -l`, `tsc --noEmit`, `python -m py_compile`, `go vet ./...`, `cargo check`, `dotnet build`). Never install unrequested global tools.

### Step 2: Audit Modified Code for Structural & Maintainability Quality
1. **Type Safety & Null Handling**:
   - Check that all new/modified function signatures declare explicit input and return types where supported by the language.
   - Verify that nullable values, optional properties, and array lookups are guarded before dereferencing.
2. **Error Handling Discipline**:
   - Eliminate silent failures (`catch (Exception $e) {}`, `except Exception: pass`, `_ = err` on critical writes, unhandled Promise rejections).
   - Ensure errors preserve root cause context when wrapped and return safe, actionable messages to callers.
3. **Complexity & Guard Clauses**:
   - Replace arrow-code (3+ levels of nested `if/else` or `try/catch` blocks) with early guard clauses and focused private helpers.
4. **Duplication & Dead Code**:
   - Remove unused imports, commented-out code blocks, debug statements (`dd()`, `dump()`, `var_dump()`, `console.log()` debug traces, `print()`, `dbg!()`), and duplicated logic introduced during editing.
5. **Comment Hygiene**: Apply [`ai-anti-slop`](../ai-anti-slop/SKILL.md) (`SKILL-05`) comment rules: strip decorative banners and obvious restatements; keep concise comments that explain non-obvious invariants.

### Step 3: Run Scoped Formatting and Linting Checks
1. Run the project's formatter and linter against the **modified files first** (e.g., `./vendor/bin/pint <paths>`, `npx eslint <paths>`, `ruff check <paths>`) to avoid creating massive unrelated formatting diffs across untouched files.
2. Fix all reported lint and style violations in the modified files by editing the code cleanly.

### Step 4: Run Static Analysis and Type Checking
1. Execute the project's type checker or static analyzer at its configured level (`./vendor/bin/phpstan analyse`, `pnpm tsc --noEmit`, `mypy`, `pyright`, `golangci-lint run`, `cargo clippy`).
2. Resolve every error and warning located in or caused by the modified code.
3. **Never Bypass Quality Gates Dishonestly**: Do not litter code with `@phpstan-ignore-next-line`, `// @ts-ignore`, `// eslint-disable-next-line`, `# type: ignore`, or `#[allow(dead_code)]` to hide genuine defects. A suppression directive is permissible only for a verified upstream library type defect, and must include a concise 1-line explanation comment.

### Step 5: Verify Clean Diff and Record Evidence
1. Run `git diff` on the modified files to confirm that only intentional functional changes and clean formatting remain, with zero stray debug statements or unintended file mutations.
2. Record the exact commands executed and their exit statuses for the completion report.

### Code Quality & Static Analysis Checklist
- [ ] Active project linters, formatters, and static analyzers identified from repo configs.
- [ ] All debug print/dump statements and commented-out dead code removed.
- [ ] Explicit types and null/undefined guards verified on modified functions and components.
- [ ] All error paths handled explicitly with zero empty catch blocks.
- [ ] Deep nesting flattened with guard clauses and duplicated logic consolidated.
- [ ] No unjustified `@ts-ignore`, `@phpstan-ignore`, or linter-disable suppressions added.
- [ ] Formatter, linter, and static analyzer executed with passing output recorded.

## 6. Technology-Specific Adaptation Rules

Use the tools that match the actual repository ecosystem:
- **PHP (Laravel / CodeIgniter / Symfony / Generic PHP)**:
  - Always run `php -l <file.php>` as the baseline syntax check if no analyzer is installed.
  - When `phpstan/phpstan` or `larastan/larastan` is present in `composer.json`, run `./vendor/bin/phpstan analyse <paths>` respecting `phpstan.neon` level.
  - When `laravel/pint` is present, run `./vendor/bin/pint --test <paths>` (or `./vendor/bin/pint <paths>`). When `friendsofphp/php-cs-fixer` or `squizlabs/php_codesniffer` is present instead (common in CodeIgniter and Symfony), use `./vendor/bin/php-cs-fixer` or `./vendor/bin/phpcs`, and never force Pint or PHPStan where not installed.
  - Respect `declare(strict_types=1);` if established in the repository's PHP files.
- **JavaScript / TypeScript (React / Next.js / Vue / Node)**:
  - Run the configured type checker (`tsc --noEmit`, `vue-tsc --noEmit`, or `astro check`) and linter/formatter (`eslint`, `biome check`, `oxlint`, `prettier --check`) via the lockfile-matched package manager.
  - Avoid `any`, unsafe `as unknown as T` casts, non-null assertions (`!`) without prior bounds checks, and missing React Hook dependency array entries (`exhaustive-deps`).
- **Python (Django / FastAPI / Flask)**:
  - Run `ruff check` / `ruff format --check`, `flake8`, `black --check`, and `mypy` or `pyright` when configured in `pyproject.toml` or `requirements*.txt`.
  - Avoid mutable default arguments (`def fn(items=[]):`), bare `except:` clauses, and untyped public interfaces in typed codebases.
- **Go**:
  - Run `gofmt -s -w <paths>`, `go vet ./...`, and `staticcheck` or `golangci-lint run` if configured. Check that all returned `error` values are inspected and HTTP response bodies are closed (`defer resp.Body.Close()`).
- **Rust**:
  - Run `cargo fmt --check`, `cargo check`, and `cargo clippy --all-targets`. Replace panicking `.unwrap()` calls in production paths with `?` or explicit error handling.
- **Java / Kotlin (Spring Boot / JVM) & C# (.NET)**:
  - Run `./gradlew check` (Checkstyle, SpotBugs, Detekt, Ktlint) or `./mvnw verify`, and `dotnet build -warnaserror` / `dotnet format --verify-no-changes`.
- **Mobile (Flutter / Dart)**:
  - Run `dart format --output=none --set-exit-if-changed <paths>` and `dart analyze` / `flutter analyze`.

## 7. Security and Safety Considerations

- **Static Security Rules**: Pay special attention to static analysis warnings flagging tainted SQL strings, unescaped HTML output, insecure randomness (`Math.random()` / `rand()` used for security tokens instead of `crypto.randomBytes()` / `random_bytes()`), weak hashes (`md5`, `sha1`), or path traversal risks.
- **Safe Autofix Execution**: Always inspect the `git diff` produced by automated fixers (`eslint --fix`, `pint`, `ruff --fix`, `php-cs-fixer fix`) to ensure risky rules did not alter runtime semantics or strict comparisons (`==` vs `===`).

## 8. Verification Criteria

Code quality validation is complete only when:
1. Every modified file passes syntax validation and the repository's configured formatter, linter, and static type checker with zero errors.
2. Zero debug artifacts (`console.log`, `dd`, `var_dump`, `pdb.set_trace`, `dbg!`) or commented-out code blocks remain in the diff.
3. No unapproved linter/type-checker ignore annotations were introduced to mask failures.
4. The exact CLI commands and their passing outputs are documented in the final report (`C-5`, `R-35`).

## 9. Failure Handling and Edge Cases

- **Pre-Existing Static Analysis Errors in Untouched Files**: If running a full-project static analysis command reports hundreds of legacy errors in files outside your task scope, run the analyzer scoped to your modified files (or compare baseline vs. post-change output) so you verify **zero new errors** in touched files and **zero regressions** in callers, and clearly report the pre-existing baseline count to the user.
- **No Linter or Type Checker Installed in Repository**: Do not install new devDependencies without user permission. Run the language runtime's built-in syntax/compile check (`php -l`, `node --check`, `python -m py_compile`, `go vet`) and perform a manual structured review against the ten quality dimensions in Section 3.
- **Conflicting Formatter and Linter Rules**: If a repository's Prettier and ESLint (or Pint and PHPCS) configurations conflict on a line, prioritize the tool enforced in the repository's CI pipeline (`.github/workflows/`) and note the configuration conflict for the user.

## 10. Expected Outputs and Reporting Requirements

Provide a concise **Code Quality & Static Analysis Report** whenever completing code changes or quality reviews:

```markdown
## Code Quality & Static Analysis Report

### 1. Executed Quality Gates
| Check Type | Command Executed | Scope | Status | Summary / Findings |
| :--- | :--- | :--- | :--- | :--- |
| Syntax / Compile | `<e.g., php -l / tsc --noEmit>` | `<Modified files>` | `PASS` | 0 syntax/type errors |
| Linter / Static Analysis | `<e.g., phpstan / eslint / ruff>` | `<Modified files>` | `PASS` | Level/rules verified |
| Formatter | `<e.g., pint --test / prettier>` | `<Modified files>` | `PASS` | Matches project style |

### 2. Engineering Quality Review
- **Error Handling & Null Safety**: <Confirmed explicit handling and type guards>
- **Complexity & Duplication**: <Confirmed guard clauses and shared helper reuse>
- **Diff Hygiene**: <Confirmed zero debug statements, dead code, or silent suppressions>
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - Follows stack detection from [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`) and implementation from [`adaptive-engineering`](../adaptive-engineering/SKILL.md) (`SKILL-06`) or [`refactoring-legacy-safety`](../refactoring-legacy-safety/SKILL.md) (`SKILL-08`).
- **Companion & Downstream Skills**:
  - Enforces comment and craftsmanship rules alongside [`ai-anti-slop`](../ai-anti-slop/SKILL.md) (`SKILL-05`).
  - Precedes automated test execution in `backend-testing-tdd` (`SKILL-16`), `playwright-mcp-browser-qa` (`SKILL-17`), and `test-reporting-diagnosis` (`SKILL-19`).

## 12. Source References

- Library Reference: [Technology Stack Detection & Adaptation Matrix](../../references/technology-stack-detection-matrix.md)
- Library Reference: [AI Anti-Slop & Engineering Craftsmanship Reference](../../references/anti-slop-engineering-reference.md)
- Tool Documentation: [PHPStan](https://phpstan.org/user-guide/getting-started), [TypeScript Compiler Options](https://www.typescriptlang.org/tsconfig/), [ESLint](https://eslint.org/docs/latest/), [Ruff](https://docs.astral.sh/ruff/), [golangci-lint](https://golangci-lint.run/)
