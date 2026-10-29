# Changelog — Reusable AI Development Skills Library (`CHANGELOG.md`)

All notable updates, fixes, and protocol enhancements pushed to `denitrisna7/reusable-ai-development-skills` are documented in this file.

---

## [`v1.5.2`] — 2026-10-30
### Added & Fixed (Cross-App Discovery Registration & Zero-Hardcoded-PASS 38-Skill Evaluator)
- **Automatic `.agents/skills.json` Registration (`scripts/run-audit.py`)**: Solved Antigravity's 1-level `.agents/skills/<name>/SKILL.md` scan limit when users clone the repository into `.agents/skills/ai-skills` (where skills live two levels deep at `.agents/skills/ai-skills/skills/<name>/SKILL.md`). `sync_agents_directory()` now automatically creates/updates `.agents/skills.json` (`{"entries": [{"path": ".agents/skills/ai-skills/skills"}]}`) and syncs all 38 skills into `.agents/skills/` so `git pull` stays synchronized and every skill is discovered immediately.
- **100% Evidence-Driven 38-Skill Evaluator (`scripts/run-audit.py`)**: Replaced all 19 previously hardcoded `"PASS"` strings in the 38-skill evaluation matrix with real static and runtime code checks (`PASS`, `FAIL`, `WARN`, `N/A`, `REVIEW`):
  - `SKILL-11` (`api-security-webhook-reliability`) now actively fails (`FAIL`) if webhook endpoints/controllers exist without signature/HMAC verification.
  - `SKILL-13` (`ai-security-prompt-injection`) and `SKILL-28` (`ai-provider-integration`) inspect actual AI/LLM client files for API key isolation, prompt validation, and timeout/fallback controls, or report honest `N/A` when the app has no AI integration.
  - `SKILL-24`, `SKILL-25`, `SKILL-26`, `SKILL-30`, `SKILL-31`, `SKILL-34`, `SKILL-35`, `SKILL-36`, and `SKILL-37` inspect actual migrations, eager-loading patterns, chunked imports, cache/queue jobs, SEO/meta tags (`run-browser-audit.mjs`), CI workflows, backup scripts, and README setup sections.
- **Strip `ANTIGRAVITY_AGENT` / `OPENCODE` Environment Variables (`scripts/run-audit.py`)**: Prevented Laravel 12 (`nunomaduro/collision`) from collapsing `php artisan test` output into a 1-line JSON summary when invoked inside Antigravity.

---

## [`v1.5.1`] — 2026-10-30 (Commit `01fb565`)
### Added & Improved (Universal Multi-Stack Audit & Server Auto-Boot)
- **Universal Multi-Stack Server Boot (`scripts/run-audit.py`)**: Added automatic ephemeral dev server boot support for Next.js (`npx next dev -p 18124`), Vite (`npx vite --port 18124`), Django (`python3 manage.py runserver`), FastAPI/Flask, native PHP (`php -S`), and Static HTML (`python3 -m http.server`), ensuring real Headless Chromium QA runs out-of-the-box on ANY web stack without manual configuration.
- **Universal Multi-Stack Code & Architecture Discovery (`scripts/run-audit.py`)**: Expanded discovery patterns to map controllers, routers, models, schemas, UI views/components/screens, and migrations across Node.js/Next.js/React/Vue, Python, Go, and Flutter, not just PHP/Laravel.
- **Cross-Framework `npm test` CI Runner (`scripts/run-audit.py`)**: Switched to `CI=true npm test` (removing hardcoded `-- --run`) so native Node test runner (`node --test`), Jest, Vitest, and Mocha execute deterministically in single-run mode.
- **Multi-File Seeder Credential Discovery (`scripts/run-browser-audit.mjs`)**: Searches `UserSeeder.php`, `DemoDataSeeder.php`, `prisma/seed.ts`, and `seed.py` for seeded test login accounts, skipping comments and deletion lines.

---

## [`v1.5.0`] — 2026-10-30 (Commit `86cff59`)
### Added & Improved (Full 38-Skill Code Audit & Context-Budget Optimization)
- **Context-Budget Optimization Across All 38 `SKILL.md` Frontmatters**: Compacted YAML frontmatter `description` fields across all 38 skills (`14,448` chars -> `6,750` chars, `-53.3%`) and removed duplicate upstream `sources/anti-slop/skills/*/SKILL.md` files from git tracking so Antigravity never excludes any of the 38 skills due to `<skills>` context budget limits.
- **Master 38-Skill & 15-Gate Automated Execution Engine (`scripts/run-audit.py`)**:
  - Automatically evaluates and prints the **Complete 38-Skill Verification Matrix (`SKILL-01` to `SKILL-38`)** and **15-Domain Final Quality Gate Summary (`Gate 01` to `Gate 15`)** on any target repository.
  - Automatically syncs `skills/`, `references/`, `scripts/`, and `BEFORE_ACTION.md` into `<target-project>/.agents/` so all 38 skills and all 8 shared reference manuals resolve relative links cleanly.
- **Repository-Wide WCAG 2.2 AA Contrast Scanner (`scripts/contrast-check.py` / `scripts/contrast_check.py`)**: Upgraded `contrast-check.py` to support both 2-color pair mode (`contrast-check.py "#767676" "#FFFFFF"`) and full-repository UI scan mode (`contrast-check.py .`).
- **Standalone & Integrated AI Anti-Slop Scanner (`scripts/slopcheck.py` / `scripts/slopcheck.sh`)**: Audits UI templates and source code for placeholder text (`Lorem ipsum`), dead links (`href="#"`), banned AI copywriting clichés, and leftover debug calls (`dd()`, `var_dump()`).
- **Tailwind CSS v4 `oklab()` / `oklch()` & Landmark/SEO Support in `scripts/run-browser-audit.mjs`**: Added Chromium 2D `<canvas>` color rasterization for modern CSS Color 4 (`oklab`, `oklch`, `color()`) contrast accuracy, plus DOM landmark, `img[alt]`, `<meta name="viewport">`, `<html lang>`, and route load latency (`ms`) checks.

---

## [`v1.4.0`] — 2026-10-30 (Commit `16c6450`)
### Added & Improved (Zero-Reload Playwright & Auto-Heal PATH)
- **Auto-PATH & Binary Healer (`scripts/run-audit.py`)**: Automatically injects and symlinks `~/.local/bin/{node,npm,npx,composer}` and `~/development/flutter/bin/{flutter,dart}` into `~/.gemini/antigravity/bin` and `PATH` so commands in fresh project sessions never fail with `Exit Code 127 (command not found)`.
- **Zero-Reload Playwright Execution (`BEFORE_ACTION.md` & `SKILL-17`)**: Strictly forbids the AI agent from stopping to ask the user to reload MCP servers or restart the IDE window.
- **Automatic Ephemeral Dev Server Boot (`scripts/run-audit.py`)**: Automatically starts a temporary local server (`php artisan serve` or `npm run dev`) if no dev server is currently active on ports `8000`, `3000`, `5173`, or `8080`, runs `scripts/run-browser-audit.mjs` against it, and shuts down the temporary server cleanly.
- **Auto-Discovery of Test Login Credentials (`scripts/run-browser-audit.mjs`)**: Automatically inspects `database/seeders/DatabaseSeeder.php` (when `--user` is not manually passed) to test interactive login and audit authenticated dashboard routes in Headless Chromium.

---

## [`v1.3.0`] — 2026-10-30 (Commit `bf56a63`)
### Added & Improved (Real Headless Chromium Runner & 15-Domain Gate Table)
- **Built-In Headless Chromium Playwright Auditor (`scripts/run-browser-audit.mjs`)**: Directly launches Headless Chromium (`~/.cache/ms-playwright`) via Node.js CLI to audit:
  - Desktop (`1440x900`) and Mobile (`375x812`) viewports.
  - Real DOM computed color contrast (`window.getComputedStyle`) across all visible text nodes (`WCAG 2.2 AA >= 4.5:1`), catching white-on-white or unreadable text.
  - Real DOM text-range bounding-box collisions (`Range.getBoundingClientRect`), clipped text, and horizontal overflow leaks (`scrollWidth > innerWidth`).
  - JS Console errors, uncaught page exceptions, and failed HTTP network requests (`>= 400`).
- **Bypass Laravel 12 1-Line JSON Test Truncation (`scripts/run-audit.py`)**: Strips AI environment variables (`CLAUDECODE`, `AGENT`, etc.) and executes `./vendor/bin/phpunit --testdox --colors=never` so all individual `✔` test cases are printed line-by-line instead of collapsing into `{"tool":"phpunit","result":"passed"...}`.
- **Mandatory 15-Domain Final Quality Gate Table (`BEFORE_ACTION.md`)**: Replaced the 5-row summary table with the full 15-Domain Quality Gate matrix covering all 38 skills (`SKILL-01` through `SKILL-38`).

---

## [`v1.2.1`] — 2026-10-29 (Commit `a8b0ae5`)
### Improved
- **Workflow Mapping & Progress Transparency (`BEFORE_ACTION.md`, `SKILL-16`, `SKILL-17`, `SKILL-38`)**: Enforced Phase 1 application workflow mapping (routes, controllers, roles, CRUD state machines) prior to running unit tests, and required live progress streaming in chat.

---

## [`v1.2.0`] — 2026-10-29 (Commit `d8ae779`)
### Added
- **Master Before-Action Execution Protocol (`BEFORE_ACTION.md`)**: Created the single-prompt execution protocol triggered by *"git clone kan skill ini kemudian kerjakan sesuai skill tersebut"*.
- **Automated Pre-Flight Diagnostic Runner (`scripts/run-audit.py`)**: Created zero-dependency Python pre-flight auditor for stack detection, `.env` inspection, local server detection, and test runner execution.

---

## [`v1.1.0`] — 2026-10-29 (Commit `1153c2f`)
### Fixed
- **Anti-Hallucination Hardening (`SKILL-16`, `SKILL-17`, `SKILL-38`)**: Added binding rules forbidding fabricated `PASS` claims without terminal/tool execution evidence.

---

## [`v1.0.1`] — 2026-10-29 (Commit `2ec7df2`)
### Added
- **Quick Start & Practical Chat Prompts (`README.md`)**: Added step-by-step `git clone` instructions and Indonesian/English prompt examples on the GitHub front page.

---

## [`v1.0.0`] — 2026-10-29 (Commit `9c4ded2`)
### Added
- **Initial Release**: Complete 38-skill Antigravity AI Development Skills Library (`SKILL-01` through `SKILL-38`), 8 shared reference manuals, `contrast-check.py`, `validate-skills.py`, `SKILL_CATALOG.md`, `SKILL_ROUTING.md`, `SOURCES.md`, and `COMPLETENESS_AUDIT.md`.
