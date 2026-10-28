---
name: dependency-supply-chain-security
description: "Audits direct and transitive dependencies, verifies lockfile integrity and package registries, evaluates CVEs and lifecycle install scripts, eliminates redundant packages, and plans risk-based dependency upgrades. Activate when adding, updating, removing, or auditing third-party packages across any ecosystem. Do not use for application-layer OWASP logic reviews."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-09"
  category: "Core Development Quality"
---

# Dependency & Supply Chain Security

This skill governs the selection, auditing, installation, upgrading, and removal of third-party packages across all programming ecosystems. It protects software repositories against supply-chain attacks (typosquatting, dependency confusion, malicious `postinstall` scripts, unpinned git dependencies), known vulnerabilities (CVEs/GHSAs), license incompatibilities, and dependency bloat. Every dependency change is held to strict necessity, lockfile integrity, and regression verification standards.

## 1. Activation Conditions

Activate this skill under any of the following scenarios:
- Before installing any new third-party package (`npm`/`pnpm`/`yarn`/`bun`, `composer`, `pip`/`uv`/`poetry`, `go get`, `cargo add`, `Maven`/`Gradle`, `NuGet`, `pub`) to verify necessity, package authenticity, and supply-chain safety.
- Performing a dependency security audit to identify and remediate vulnerable direct or transitive packages.
- Planning or executing minor, patch, or major version upgrades across project dependencies.
- Resolving lockfile drift, duplicate competing lockfiles, dependency version conflicts, or deprecated/abandoned libraries.
- Auditing a repository for redundant, unused, or bloated dependencies.

## 2. When Not to Use

Do not use this skill in the following situations:
- Auditing custom application authentication, authorization, SQL injection, or XSS logic written in first-party code; route to `application-security-owasp` (`SKILL-10`).
- Initial broad repository orientation before any package work is considered; run [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`) first.
- Designing internal module dependency boundaries between first-party classes; route to [`adaptive-architecture`](../adaptive-architecture/SKILL.md) (`SKILL-03`).

## 3. Scope and Objectives

Every dependency management or supply-chain audit task must cover the following nine core areas:
- **Dependency auditing**: Running ecosystem-native vulnerability scanners and inspecting advisory databases for known security flaws.
- **Direct and transitive dependencies**: Tracing whether a vulnerable or problematic package is required directly by the application or pulled in transitively via a parent package, and choosing the safest remediation path.
- **Vulnerability assessment**: Evaluating CVE/GHSA severity, actual exploitability in the application's execution context (e.g., whether the vulnerable function or CLI flag is reachable in production vs. dev-only build tools), and patch availability.
- **Lockfile integrity**: Ensuring deterministic builds via committed, synchronized lockfiles (`composer.lock`, `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `uv.lock`, `poetry.lock`, `go.sum`, `Cargo.lock`) with intact cryptographic hashes (`sha512`/`sha256`).
- **Package source verification**: Verifying exact package names and scopes against official registries to prevent typosquatting and slopsquatting (AI-hallucinated package names), and auditing custom registries or git URL dependencies.
- **Risk-based updates**: Grouping dependency updates by risk tier (zero-breaking security patches first, minor updates second, major breaking upgrades isolated per package with full migration checks).
- **Breaking changes**: Inspecting upstream changelogs, migration guides, minimum runtime requirements, and peer-dependency constraints before applying version bumps.
- **Unnecessary packages**: Rejecting trivial third-party packages when the language standard library or an already-installed package provides the capability, and removing orphaned dependencies.
- **Installation scripts and untrusted packages**: Inspecting lifecycle hooks (`preinstall`, `install`, `postinstall`, Composer plugins/scripts, `setup.py` execution) before running package installations.

## 4. Prerequisites and Context Requirements

- Access to the repository's manifest files (`package.json`, `composer.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle.kts`, `*.csproj`, `pubspec.yaml`) and their corresponding lockfiles.
- Verified runtime version constraints from [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`).
- Read access to CI/CD workflow files (`.github/workflows/`, `Dockerfile`) to verify how dependencies are installed in build environments (e.g., `npm ci`, `pnpm install --frozen-lockfile`, `composer install --no-interaction --prefer-dist`).

## 5. Step-by-Step Workflow

Follow this six-step engineering procedure for dependency additions, upgrades, and security audits:

### Step 1: Enforce the Necessity & Anti-Slop Gate Before Adding Any Package
1. **Standard Library Check**: Before proposing any new package, verify whether the language runtime already provides the functionality natively (e.g., native `fetch`, `crypto.randomUUID()`, `Intl`, `structuredClone`, or `node:test`/`node:util` in modern JS/Node; native `enum`, `array_*`, `DateTimeImmutable`, or `hash_hmac` in PHP; `pathlib`, `urllib`, `dataclasses`, `tomllib` in Python).
2. **Existing Dependency Check**: Inspect the project's manifest to see if an installed library already covers the need (e.g., do not add `axios` if a project already standardizes on `ky` or native `fetch`; do not add `moment` or `dayjs` if `date-fns` is already installed).
3. **Anti-Slopsquatting Verification**: Never guess or hallucinate a package name. Verify the exact package identifier, vendor/scope prefix, maintenance status, license compatibility, and download/repository legitimacy before adding it to a manifest.

### Step 2: Verify Package Sources, Registries, and Lockfile Integrity
1. Inspect registry configuration files (`.npmrc`, `composer.json` `repositories` block, `pip.conf`, `pyproject.toml` `[[tool.uv.index]]`, `Cargo.toml` `[source]`, `NuGet.config`):
   - Flag any unexpected third-party registries, insecure `http://` registry URLs, or unpinned git branch dependencies (`"main"` / `"master"` instead of an immutable commit SHA or signed release tag).
   - Check for **Dependency Confusion** exposure if private scoped packages are mixed with public registries without explicit scope-to-registry mapping.
2. Verify Lockfile Health:
   - Confirm that exactly **one** lockfile exists per package ecosystem in a workspace (never mix `package-lock.json` and `yarn.lock` or `pnpm-lock.yaml` in the same directory).
   - Confirm that the lockfile is in sync with the manifest and contains cryptographic integrity checksums (`integrity: sha512-...`, `go.sum` hashes, `Cargo.lock` checksums).

### Step 3: Audit Lifecycle Scripts and Untrusted Package Hooks
1. Before installing newly added or unfamiliar packages, check whether they execute arbitrary code during installation (`preinstall`, `install`, `postinstall` in npm; `post-autoload-dump` or unapproved `allow-plugins` in Composer; arbitrary `setup.py` in Python sdist packages).
2. Prefer `--ignore-scripts` (or ecosystem equivalent) when inspecting untrusted trees, and review `composer.json -> config.allow-plugins` to ensure only explicitly trusted Composer plugins are permitted to execute.

### Step 4: Execute Vulnerability Auditing (Direct & Transitive)
1. Run the ecosystem's native audit command (when available in the environment):
   - PHP: `composer audit`
   - JS/TS: `pnpm audit`, `npm audit`, or `yarn npm audit`
   - Python: `pip-audit` or `uv` / `safety` (if installed)
   - Go: `govulncheck ./...` (if installed) or inspect `go.mod` versions
   - Rust: `cargo audit` (if installed)
   - .NET: `dotnet list package --vulnerable --include-transitive`
2. For each reported vulnerability, classify:
   - **Dependency Type**: Direct (`prod` vs `dev`) or Transitive (and trace why it is installed using `composer why <pkg>`, `pnpm why <pkg>`, `npm explain <pkg>`, `go mod why -m <pkg>`, `cargo tree -i <pkg>`).
   - **Reachability & Runtime Exposure**: Determine whether the vulnerable package is shipped to production or confined to local build/test tooling, and whether the vulnerable code path is invoked by the application.

### Step 5: Plan and Execute Risk-Based Updates & Unused Package Cleanup
1. **Tier 1 (Low Risk: Security & Bugfix Patches)**: Apply compatible patch/minor updates (`semver` safe) that resolve CVEs without breaking APIs. For transitive vulnerabilities where the parent package has not yet bumped its constraint, use explicit, documented resolution overrides (`overrides` in `package.json`, `pnpm.overrides`, conflict/constraint pinning in `composer.json`, or `patch` in `Cargo.toml`) only after verifying compatibility.
2. **Tier 2 (Medium Risk: Minor Feature Updates)**: Update minor versions in logical groups and run static analysis and tests.
3. **Tier 3 (High Risk: Major Version Upgrades)**: Isolate major upgrades **one core package/framework at a time**:
   - Verify runtime compatibility (e.g., does the new major version require a newer PHP, Node, Python, or Go version than the project targets?).
   - Review breaking changes and update first-party call sites before claiming the upgrade succeeded.
4. **Unused Dependency Removal**: Before removing a package from `dependencies` or `require`, search the codebase (source files, configs, CLI scripts, dynamic loaders, build plugins, and autoloaders) to confirm zero usage.

### Step 6: Verify Deterministic Build and Regression Suite
1. Confirm the lockfile updated cleanly using the project's single active package manager.
2. Run [`code-quality-static-analysis`](../code-quality-static-analysis/SKILL.md) (`SKILL-07`) and the project's automated test suite to prove no regressions were introduced by added, updated, or removed packages.

### Dependency & Supply Chain Checklist
- [ ] Necessity verified against standard library and already-installed packages before adding dependencies.
- [ ] Package names verified against official registries (zero hallucinated / typosquatted names).
- [ ] Single canonical lockfile maintained with intact cryptographic hashes.
- [ ] Registry configs and `allow-plugins` / `postinstall` lifecycle scripts audited.
- [ ] Direct and transitive vulnerabilities traced (`why` / `explain`) and prioritized by runtime reachability.
- [ ] Breaking changes and runtime engine constraints verified before version upgrades.
- [ ] Static analysis and automated tests executed after lockfile updates.

## 6. Technology-Specific Adaptation Rules

Adapt dependency workflows to the target ecosystem:
- **PHP (Composer: Laravel / CodeIgniter / Symfony)**:
  - Use `composer audit`, `composer why <vendor/pkg>`, and `composer outdated --direct`.
  - Distinguish `require` (production runtime) from `require-dev` (testing/static analysis like `phpunit/phpunit`, `phpstan/phpstan`, `laravel/pint`). Ensure production Dockerfiles use `composer install --no-dev --prefer-dist --no-interaction --optimize-autoloader`.
  - Verify `config.allow-plugins` in `composer.json` explicitly lists only required plugins.
- **JavaScript / TypeScript (`pnpm` / `npm` / `yarn` / `bun`)**:
  - Strictly obey the repository's existing lockfile tool. In CI/Docker, ensure frozen lockfile commands (`npm ci`, `pnpm install --frozen-lockfile`, `yarn install --immutable`) are used rather than loose `npm install`.
  - Distinguish `dependencies`, `devDependencies`, and `peerDependencies`. Never place build-only linters or test runners in production `dependencies` when server bundle size or container footprint matters.
- **Python (`uv` / `poetry` / `pip-tools` / `pipenv`)**:
  - Prefer lockfiles with hashes (`uv.lock`, `poetry.lock`, `Pipfile.lock`, or `requirements.txt --generate-hashes`) over floating unpinned `requirements.txt` files.
- **Go**:
  - Run `go mod tidy` and `go mod verify` to confirm module cache hashes match `go.sum`.
- **Rust**:
  - Keep `Cargo.lock` committed for binary/application crates and use `cargo update -p <crate>` for targeted updates rather than sweeping full-tree updates when minimizing risk.
- **Java / Kotlin (Maven / Gradle) & C# (.NET)**:
  - Use BOMs (Bill of Materials, e.g., `spring-boot-dependencies`) or central package management (`Directory.Packages.props` in .NET) when already established in the repository to prevent transitive version skew.

## 7. Security and Safety Considerations

- **Never Execute Untrusted Install Scripts Blindly**: If auditing a suspicious repository or unfamiliar third-party package, inspect `package.json` `scripts` and `composer.json` `scripts` via `read_file` **before** running `npm install` or `composer install`.
- **Pin CI GitHub Actions & Container Base Images**: Supply-chain security extends to `.github/workflows/*.yml` and `Dockerfile`s; flag unpinned `uses: owner/action@main` references and `:latest` container tags during supply-chain reviews.
- **License Compliance**: Flag copyleft (`GPL`, `AGPL`, `SSPL`) or non-commercial licenses when adding dependencies to commercial or MIT/Apache-2.0 repositories.

## 8. Verification Criteria

A dependency audit, addition, or upgrade is complete only when:
1. Audit output (`composer audit`, `npm/pnpm audit`, or manifest inspection) is recorded with exact package versions and CVE/GHSA identifiers.
2. The manifest and lockfile are synchronized with zero conflicting lockfiles left in the workspace.
3. Static analysis/type checking and automated tests pass against the updated dependency tree (`R-35`).
4. Any remaining unpatched vulnerabilities (e.g., upstream fix not yet released or dev-only tool with zero production exposure) are explicitly documented as residual risks with mitigation rationale.

## 9. Failure Handling and Edge Cases

- **Offline or Restricted Network Environment**: If the execution sandbox blocks external registry calls (`composer audit` or `npm install` fails with network error), inspect the manifest and lockfile statically, report the network restriction honestly as `BLOCKED` for live registry resolution, and provide the exact commands and version constraints for the user to run.
- **Peer Dependency / Transitive Deadlock**: When upgrading package `A` requires version `X` of package `C`, while package `B` requires incompatible version `Y` of `C`, trace the dependency graph (`why`/`explain`), check whether `B` has an updated compatible release, and present the exact upgrade pair to the user rather than forcing `--force` or `--legacy-peer-deps` silently.
- **Abandoned Upstream Package**: If a vulnerable direct dependency is unmaintained and has no patched version, document the abandonment and propose either replacing it with standard library code or migrating to a maintained alternative via an adapter seam (`SKILL-03`, `SKILL-08`).

## 10. Expected Outputs and Reporting Requirements

Present a structured **Dependency & Supply Chain Security Report** using the following template:

```markdown
# Dependency & Supply Chain Security Report

## 1. Ecosystem & Lockfile Integrity Summary
- **Package Manager & Manifests**: `<e.g., pnpm (package.json + pnpm-lock.yaml)>`
- **Lockfile & Registry Status**: `<Synchronized / Single lockfile / Integrity hashes verified / Registry check>`
- **Install Script & Plugin Audit**: `<Reviewed postinstall / allow-plugins status>`

## 2. Vulnerability & Dependency Findings
| Package | Direct / Transitive (Parent) | Current Version | Issue / CVE / GHSA | Severity & Reachability | Action / Target Version |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `<pkg-name>` | `<Transitive via X>` | `1.2.3` | `CVE-XXXX-YYYY` | `High (Prod reachable)` | `Upgrade to 1.2.4` |

## 3. Risk-Based Upgrade & Cleanup Plan
- **Tier 1 (Safe Patches Applied)**: `<List>`
- **Tier 2/3 (Minor/Major Upgrades & Breaking Change Notes)**: `<List>`
- **Redundant / Unused Packages Removed**: `<List with grep verification>`

## 4. Verification & Residual Risk
- **Audit / Build / Test Verification**: `<Commands executed + PASS/BLOCKED status>`
- **Documented Residual Risks**: `<Any unpatched dev-only or upstream-blocked advisories>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - Receives initial manifest and lockfile inventory from [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`).
- **Companion & Downstream Skills**:
  - Enforces dependency minimalism alongside [`ai-anti-slop`](../ai-anti-slop/SKILL.md) (`SKILL-05`).
  - Routes breaking-change code adaptations to [`adaptive-engineering`](../adaptive-engineering/SKILL.md) (`SKILL-06`), [`code-quality-static-analysis`](../code-quality-static-analysis/SKILL.md) (`SKILL-07`), and [`refactoring-legacy-safety`](../refactoring-legacy-safety/SKILL.md) (`SKILL-08`).
  - Complements application-level security checks in `application-security-owasp` (`SKILL-10`) and CI/CD pipeline checks in `ci-cd-pipelines` (`SKILL-29`).

## 12. Source References

- Library Reference: [Technology Stack Detection & Adaptation Matrix](../../references/technology-stack-detection-matrix.md)
- Standard: [OWASP Top 10: A06:2021 Vulnerable and Outdated Components / Software Supply Chain Failures](https://owasp.org/www-project-top-ten/)
- Standard: [OWASP Software Component Verification Standard (SCVS)](https://scvs.owasp.org/)
- Reference: [SLSA (Supply-chain Levels for Software Artifacts) Specification](https://slsa.dev/)
