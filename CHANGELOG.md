# Changelog — Reusable AI Development Skills Library (`CHANGELOG.md`)

All notable updates, fixes, and protocol enhancements pushed to `denitrisna7/reusable-ai-development-skills` are documented in this file.

---

## [`v1.8.0`] — 2026-11-03
### Added & Enforced (Mandatory All-38-Skill Forced Execution & Zero-Touch Project Bootstrap)
- **Ironclad Anti-Cherry-Picking Rule (`AGENTS.md`, `rules/AGENTS.md`, & `BEFORE_ACTION.md`)**:
  - Solved the issue where AI agents only ran "what they thought was needed" ("hanya yang dibutuhkan saja") or cherry-picked 2–3 skills.
  - Added an absolute non-negotiable rule strictly prohibiting the agent from skipping skills or treating the library as an à la carte menu.
  - Forces the agent to systematically evaluate, execute, and verify ALL 38 skills (`SKILL-01` to `SKILL-38`) across the application with concrete code or terminal evidence.
- **Zero-Touch Project Bootstrap & Rule Auto-Injection (`scripts/setup-project.py` & `scripts/setup.sh`)**:
  - Automatically auto-injects `AGENTS.md` into `<project_root>/AGENTS.md`, `<project_root>/.gemini/rules/AGENTS.md`, and `<project_root>/.agents/rules/AGENTS.md` when cloned into any external repository.
  - Writes `<target>/.agents/skills.json` and syncs `.agents/scripts/` and `.agents/references/`.
  - Permanently binds Antigravity to inject the mandatory 38-skill execution rules into `<user_rules>` in that project.
- **Forced 38-Skill Active Execution Matrix & Breakdown (`scripts/run-audit.py --force-all`)**:
  - Enhanced `scripts/run-audit.py` to evaluate and verify all 38 skills with an explicit active execution matrix (`38/38 skills actively verified (0 skills skipped)`).
  - Added `--force-all` flag to print detailed per-skill execution breakdowns with evidence lines for each individual skill from `[01/38]` to `[38/38]`.
- **SKILL.md Frontmatter Router Optimization (All 38 Skills)**:
  - Eliminated restrictive negative phrasing ("Do not use for...") across all 38 `SKILL.md` frontmatters that previously tricked AI model routers into suppressing skills.
  - Replaced descriptions with positive, authoritative mandatory lifecycle statements (`Mandatory lifecycle skill (SKILL-XX)... Part of the 38-skill quality suite.`) while maintaining strict context budget compliance.

## [`v1.7.0`] — 2026-10-31
### Added & Enhanced (Live Visual GUI Playwright Browser on Screen by Default)
- **Live Visual GUI Browser Mode on Screen (`scripts/run-browser-audit.mjs` & `scripts/run-audit.py`)**:
  - Automatically detects desktop display availability (`DISPLAY`, `WAYLAND_DISPLAY`, Windows, macOS). On desktop environments, Playwright now opens a visible Google Chrome window directly on the user's screen (`headless: false`) by default instead of running silently in the background, allowing the user to watch the entire automation unfold in real time.
  - Automatically falls back to headless mode (`headless: true`) in headless servers, Docker containers, or CI/CD pipelines without a display, or when the launch fails.
  - Prioritizes Google Chrome Flatpak (`/var/lib/flatpak/app/com.google.Chrome/current/active/files/extra/chrome`) and system Chrome binaries alongside Playwright cache binaries.
- **Interactive Visual Testing UX & Floating HUD Status Banner**:
  - **Floating HUD Banner (`#playwright-live-hud`)**: Displays real-time test progress, current phase, routes, viewports, WCAG AA contrast status, and login state in a styled pill banner pinned to the top of the browser window.
  - **DOM Audit Isolation**: The HUD banner is explicitly excluded from DOM audits, visibility calculations, and overflow detection so it causes zero false positives.
  - **Glowing Element Highlights**: Automatically highlights active form input fields in amber (`#f59e0b`), valid inputs in emerald green (`#10b981`), and submit buttons in ruby red (`#ef4444`) with glowing outlines (`box-shadow`) so the user can clearly see each interaction.
  - **Paced Execution (`slowMo`)**: Runs at 250ms slowMo in headed mode so human eyes can track each click, fill, and navigation comfortably.
  - **End-of-Run Visual Hold**: Automatically holds the browser window for 3 seconds after completing tests so the user can inspect the final screen before the browser closes.
  - **Automatic Browser Dialog Handling**: Automatically detects and accepts browser `alert()` and `confirm()` dialogs (e.g. deletion confirmation dialogs) and logs them to the console.
- **Configurable CLI Flags**:
  - `--headed` or `--visual`: Force GUI window on screen.
  - `--headless`: Force headless background execution (ideal for CI/CD).
  - `--slowmo=<ms>`: Customize delay between Playwright actions (default 250ms in visual mode).
  - `--hold=<sec>`: Customize visual hold time before closing (default 3s in visual mode).
- **Timeout Extension & Forwarding (`scripts/run-audit.py`)**:
  - Extended browser audit command timeout from 90s to 180s to accommodate visual executions with `slowMo`.
  - Automatically forwards `--headed`, `--headless`, `--visual`, `--slowmo`, and `--hold` arguments to `run-browser-audit.mjs`.
- **Protocol & Documentation Updates**:
  - Updated `BEFORE_ACTION.md`, `rules/AGENTS.md`, `AGENTS.md`, `README.md`, and `skills/playwright-mcp-browser-qa/SKILL.md` to reflect Live Visual On-Screen execution and new CLI flags.

## [`v1.6.0`] — 2026-10-30
### Added, Fixed & Hardened (Deep Audit Across Real Applications)
- **Native Antigravity `<user_rules>` Auto-Injection (`rules/AGENTS.md` & `AGENTS.md`)**: Added `rules/AGENTS.md` inside the plugin root and `AGENTS.md` at the repository root (plus automatic sync to `<target>/.agents/rules/AGENTS.md`, `.agents/scripts/`, and `.agents/references/` via `scripts/run-audit.py`) so Antigravity automatically loads the 5-phase execution protocol into `<user_rules>` on every session.
- **Same-Origin Full-URL Route Discovery & Off-Canvas Drawer Filtering (`scripts/run-browser-audit.mjs`)**:
  - Parses `<a href>` via `new URL(a.href, window.location.origin)` so framework route helpers that emit absolute URLs (such as Laravel `{{ route('...') }}`) are automatically discovered and audited across Desktop (`1440x900`) and Mobile (`375x812`).
  - Filters out closed off-screen mobile drawers (`rect.right <= 0`, `x-cloak`, `aria-hidden="true"`) in `isVisible(el)` and adds a `120ms` post-navigation settle delay for Alpine.js / React / Vue hydration.
  - Prints exact CSS class selectors on `CONTRAST FAIL` (`<p.text-[11px].text-ink-2/80>`) and exact overflowing DOM elements (`❌ OVERFLOW CULPRIT: <table.w-full.min-w-[700px]> right=717px (+342px past viewport)`) whenever `horizontalOverflowPx > 4`.
- **Zero False Positives & Deterministic 38-Skill Evidence Matrix (`scripts/run-audit.py`)**:
  - Eliminated regex false positives on static English log strings (`SKILL-12`), Service Workers and config files (`SKILL-27`), and database migrations (`SKILL-14` / `SKILL-28`).
  - Replaced the 12 static `"REVIEW"` traps (`SKILL-02`, `SKILL-03`, `SKILL-06`, `SKILL-13`, `SKILL-14`, `SKILL-20`, `SKILL-25`, `SKILL-26`, `SKILL-28`, `SKILL-29`, `SKILL-30`, `SKILL-33`) with concrete code and runtime verification checks so compliant applications deterministically reach `AUTOMATED VERDICT: READY`.
- **Expanded Self-Validation Suite (`scripts/validate-skills.py`)**: Verifies all 18 required root, rule, and helper script files alongside all 38 `SKILL.md` files and 161 relative links.

---

## [`v1.5.2`] — 2026-10-30 (Commit `a1a4b34`)
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
