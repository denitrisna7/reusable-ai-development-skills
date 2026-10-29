# Master Execution & Evidence-Streaming Protocol (`BEFORE_ACTION.md`)

> **CRITICAL BINDING DIRECTIVE FOR AI CODING AGENTS (ANTIGRAVITY / CLAUDE / CHATGPT / AGENT SKILLS)**  
> When the user prompts:  
> **"git clone kan skill ini kemudian kerjakan sesuai skill tersebut"**  
> *(or any variation such as "audit aplikasi kita dengan skill ini", "kerjakan sesuai skill", or "jalankan testing dan audit menyeluruh")*  
> 
> **THE "NO SHORTCUTS, NO 1-LINE JSON, NO IDE RELOAD STOPS, & NO FAKE BLOCKED" RULES**:  
> 1. **Always Pull Latest Skill Repo First**: If `.agents/skills/ai-skills` or `reusable-ai-development-skills` already exists in the project, run `git -C <skills-dir> pull origin main` first so you always execute the latest scripts.  
> 2. **Never Stop to Ask the User to Reload MCP or Restart the IDE Window**: Do NOT waste turns editing `mcp_config.json`, searching the plugin marketplace, or telling the user to reload MCP servers! `scripts/run-audit.py` automatically heals `PATH` (`~/.local/bin`, `~/development/flutter/bin`, `~/.gemini/antigravity/bin`), auto-starts a temporary local server if none is running, and runs `scripts/run-browser-audit.mjs` in real Headless Chromium directly via `run_command` in the current session!  
> 3. **Never Collapse Unit Tests into 1-Line JSON**: In Laravel 12+, `php artisan test` outputs a 1-line JSON summary (`{"tool":"phpunit","result":"passed"...}`) when it detects an AI environment. You MUST run `./vendor/bin/phpunit --testdox --colors=never` (or `pytest -v` / `npm test`) so every single test case (`✔ ...`) is printed visibly in the chat!  
> 4. **Never Skip Playwright with `BROWSER TESTING BLOCKED`**: Execute `node <skills-path>/scripts/run-browser-audit.mjs http://127.0.0.1:<port>` (or let `run-audit.py` run it automatically) to run real Headless Chromium browser QA across Desktop (`1440x900`) and Mobile (`375x812`) viewports, including interactive login (`--login-url=/login --user=... --pass=...`)!  
> 5. **Never Output a Partial 5-Row Final Table**: Phase 4 MUST output the complete **15-Domain Final Quality Gate Table (`Gate 01` through `Gate 15`, covering all 38 skills `SKILL-01` through `SKILL-38`)**.  
> 6. **Never Deploy When Any Gate is `FAIL` or `BLOCKED`**: Production deployment is strictly prohibited unless all applicable gates are `PASS` and the user explicitly requested deployment.

---

## Phase 0: Ground-Truth Pre-Flight Diagnostic (`SKILL-01`, `SKILL-32`)

Ensure the local application server is running (start `php artisan serve`, `npm run dev`, etc. in the background if not yet running), then execute the bundled pre-flight and browser audit script:

```bash
python3 .agents/skills/ai-skills/scripts/run-audit.py .
# (or python3 reusable-ai-development-skills/scripts/run-audit.py . if cloned in root)
```

**Required Chat Output:**  
Paste the complete output of `run-audit.py` showing:
- Verified Technology Stack & Manifests (`SKILL-01`).
- Environment & Secret Health (`.env` vs `.env.example`, `APP_DEBUG`, credential hygiene) (`SKILL-32`).
- Active Local Dev Server URL.

---

## Phase 1: Real Application Workflow & Architecture Analysis (`SKILL-01` to `SKILL-04`)

Before running or writing tests, inspect the actual codebase so tests match the real routes, controllers, roles, and state machines:

1. **Inspect Routes, Controllers, Models, and Views**:
   - Read route definitions (`routes/web.php`, `routes/api.php`, `src/app/**`, `urls.py`, etc.).
   - Read controllers, form validation rules, authorization scopes/policies, and database migrations (`SKILL-24`).
2. **Print the Complete Application Workflow Map in Chat**:
   - List all active user roles and permissions.
   - Map the full end-to-end user journeys and CRUD endpoints (Create -> Read -> Update -> Delete -> Post-Delete verification).

---

## Phase 2: Full Verbose Unit, CRUD, & Static Analysis Execution (`SKILL-05` to `SKILL-16`, `SKILL-18`, `SKILL-19`)

Execute the project's test runner and static analyzers in verbose mode and **print the real per-test checklist in chat**:

1. **Backend / Unit / CRUD Test Suite (Verbose TestDox Mandatory)**:
   - **Laravel / PHP**: Run `./vendor/bin/phpunit --testdox --colors=never` (do NOT rely solely on 1-line JSON from `php artisan test`).
   - **Node / TypeScript**: Run `npm test -- --run --reporter=verbose`.
   - **Python**: Run `pytest -v`.
   - **Flutter / Mobile (if present)**: Run `flutter analyze && flutter test --expanded`.
2. **Display Real Test Progress in Chat**:
   - Print the actual test suite groups and individual `✔` test cases in the chat response so the user can see every CRUD, RBAC, and validation test executing.
   - If any test fails (500, 404, 403), fix the root cause in the code, re-run `./vendor/bin/phpunit --testdox`, and show the passing output.

---

## Phase 3: Real Headless Chromium Playwright Browser QA (`SKILL-17`, `SKILL-20` to `SKILL-23`)

You MUST verify the live web application in a real Chromium browser across **both Desktop (`1440x900`) and Mobile (`375x812`) viewports**.

### Execution Method (Always Runnable):
Run the bundled Playwright Chromium auditor against the active local server, passing key public routes and interactive login credentials if applicable:

```bash
node .agents/skills/ai-skills/scripts/run-browser-audit.mjs http://127.0.0.1:8000 / /login --login-url=/login --user=<test-email> --pass=<test-password>
```
*(If Playwright MCP tools `browser_navigate` / `browser_snapshot` are also active in the session, you may run them in addition to `run-browser-audit.mjs`).*

### Required Live Progress Stream in Chat:
Paste the real output from `run-browser-audit.mjs` showing for **every route** at **Desktop (`1440x900`)** and **Mobile (`375x812`)**:
- **HTTP Status & Title**: Confirm `HTTP 200` (zero unexpected `404`/`403`/`500`).
- **DOM Structure**: Count of verified text nodes, forms, buttons, and tables.
- **Horizontal Overflow (`SKILL-23`)**: Confirm `0px (PASS - No horizontal leak)` on Mobile `375x812` and Desktop `1440x900`.
- **Real DOM Computed Color Contrast (`SKILL-21`)**: Confirm minimum contrast ratio `>= 4.5:1` across all visible text nodes (proving zero white-on-white or unreadable text).
- **Real DOM Bounding-Box Collisions (`SKILL-23`)**: Confirm `0 overlapping text elements (PASS)` and `0 clipped text elements (PASS)`.
- **Console & Network Diagnostics (`SKILL-17`)**: Confirm `0 JS errors` and `0 failed HTTP requests`.

---

## Phase 4: Complete 15-Domain Final Quality Gate Sign-Off (`SKILL-33` to `SKILL-38`)

After Phases 0, 1, 2, and 3 are printed in chat, output the **complete 15-Domain Final Quality Gate Table** (never truncate to 5 rows):

| Gate ID | Quality Gate Domain & Skills Covered | Status (`PASS` / `FAIL` / `BLOCKED` / `N/A`) | Concrete Evidence Cited from Phases 0–3 |
| :--- | :--- | :---: | :--- |
| **Gate 01** | **Requirements & Workflow Traceability** (`SKILL-01`, `SKILL-02`) | `PASS` | Workflow map & PRD requirements verified in Phase 1 |
| **Gate 02** | **Functional Completeness & Anti-Slop** (`SKILL-05`, `SKILL-06`) | `PASS` | Zero placeholder stubs, dead buttons, or AI slop |
| **Gate 03** | **Code Quality & Static Analysis** (`SKILL-07`, `SKILL-08`) | `PASS` | Linter / analyzer exit code 0 |
| **Gate 04** | **Automated Backend & CRUD Tests** (`SKILL-15`, `SKILL-16`, `SKILL-18`, `SKILL-19`) | `PASS` | Full `--testdox` suite output & assertion count cited |
| **Gate 05** | **Application Security & OWASP ASVS** (`SKILL-10`, `SKILL-12`, `SKILL-13`, `SKILL-14`) | `PASS` | Auth, RBAC, CSRF, SQLi/XSS defenses verified |
| **Gate 06** | **Dependency & Supply-Chain Security** (`SKILL-09`) | `PASS` | Lockfile & dependency audit clean |
| **Gate 07** | **Database Integrity & Migrations** (`SKILL-24`, `SKILL-25`, `SKILL-26`) | `PASS` | Foreign keys, ACID transactions, & seeders/migrations verified |
| **Gate 08** | **API & External Service Reliability** (`SKILL-11`, `SKILL-27`, `SKILL-28`) | `PASS` | Timeouts, webhook validation, & error handling verified |
| **Gate 09** | **Playwright Browser QA, Contrast, & Mobile View** (`SKILL-17`, `SKILL-20`, `SKILL-21`, `SKILL-23`) | `PASS` | Real Chromium `1440x900` & `375x812`: contrast `>= 4.5:1`, `0` overlaps, `0` console errors |
| **Gate 10** | **Frontend & Backend Performance** (`SKILL-22`, `SKILL-29`, `SKILL-30`) | `PASS` | Query optimization, caching, & asset build verified |
| **Gate 11** | **Environment Config & Secret Isolation** (`SKILL-32`) | `PASS` | `.env` check via `run-audit.py`; `APP_DEBUG=false` in prod |
| **Gate 12** | **Backup, Recovery, & Rollback Readiness** (`SKILL-33`, `SKILL-35`) | `PASS` | Reversibility & backup safety verified |
| **Gate 13** | **Observability, Logging, & Health Checks** (`SKILL-34`) | `PASS` | Error logs clean & health endpoints verified |
| **Gate 14** | **Documentation & Architecture Records** (`SKILL-03`, `SKILL-04`, `SKILL-37`) | `PASS` | Setup docs, credentials table, & handoff notes updated |
| **Gate 15** | **CI/CD, SEO, & Post-Deploy Smoke Readiness** (`SKILL-31`, `SKILL-33`, `SKILL-36`, `SKILL-38`) | `PASS` | Release build & smoke checks verified |

### Authoritative Release Verdict:
- **`READY`**: Issued ONLY when all applicable gates across Gates 01–15 are `PASS` with real terminal and Chromium browser logs displayed above.
- **`BLOCKED`**: Issued if any test failed, any contrast/overlap defect was found in Chromium, or any required gate was skipped.
