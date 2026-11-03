# Reusable AI Development Skills — Mandatory Execution & Verification Rules

Whenever this library or plugin (`reusable-ai-development-skills`) is active in the workspace or cloned via `git clone` (for example, when the user prompts *"git clone kan skill ini kemudian kerjakan sesuai skill tersebut"*, *"audit aplikasi ini"*, or *"kerjakan sesuai skill"*), you MUST follow these non-negotiable rules:

## 1. Absolute Rule of Forced 38-Skill Execution (Anti-Cherry-Picking / "DILARANG HANYA MENJALANKAN YANG DIBUTUHKAN SAJA")

- **Zero Cherry-Picking Permitted**: You are STRICTLY FORBIDDEN from selecting only a subset of skills (such as running only unit tests or only linting) under the premise of *"hanya menjalankan yang dibutuhkan"* or *"skill lainnya tidak relevan"*.
- **All 38 Skills Are Compulsory**: You MUST actively evaluate, execute, and verify ALL 38 skills (`SKILL-01` through `SKILL-38`) sequentially across the entire application as a unified software engineering lifecycle.
- **Active Verification for Every Skill**:
  1. For every domain existing in the project (database, authentication, APIs, UI/UX, accessibility, security, background workers, caching), you MUST actively inspect the codebase, run automated checks, and cite concrete file and line evidence.
  2. For any technology or domain absent from the project (e.g., no AI provider SDK in a pure PHP app, or no Flutter mobile code in a web-only app), you MUST provide empirical search evidence proving its absence (`0 matching files / imports found`), confirm that no shadow/unprotected implementation exists, and mark `N/A` with evidence—NEVER silently skipping the skill.
- **Zero-Touch Bootstrap Auto-Execution**:
  When cloned or invoked, immediately ensure project rules and skills are active in the target workspace by running:
  `python3 .agents/skills/ai-skills/scripts/setup-project.py .`
  (or `python3 reusable-ai-development-skills/scripts/setup-project.py .`), which automatically injects `AGENTS.md` into `<project_root>/AGENTS.md`, `<project_root>/.gemini/rules/AGENTS.md`, and `<project_root>/.agents/rules/AGENTS.md`, registers `.agents/skills.json`, and triggers the forced 38-skill audit.

## 2. Mandatory 5-Phase Execution Protocol (`BEFORE_ACTION.md`)

1. **Phase 0 — Ground-Truth Pre-Flight & Forced 38-Skill Auto-Audit**:
   - Always pull the latest skill repository first if already cloned (`git -C .agents/skills/ai-skills pull origin main`).
   - Run `python3 .agents/skills/ai-skills/scripts/run-audit.py . --force-all` and paste the real output in chat, demonstrating active verification across all 38 skills (`38/38 skills actively verified`).
2. **Phase 1 — Real Application Workflow & Architecture Map (`SKILL-01` to `SKILL-04`)**:
   - Inspect actual routes, controllers, models, roles, permissions, and state machines before writing or modifying tests.
   - Print the complete workflow and role-permission map in chat.
3. **Phase 2 — Verbose Unit, CRUD, & Mobile Test Execution (`SKILL-05` to `SKILL-16`, `SKILL-18`, `SKILL-19`)**:
   - **Never collapse unit tests into a 1-line JSON summary**: Run `./vendor/bin/phpunit --testdox --colors=never` (for Laravel/PHP), `CI=true npm test` (for Node/TS), `pytest -v` (for Python), and `flutter analyze && flutter test` (for Flutter) so every individual test case (`✔ ...`) is visible in chat.
4. **Phase 3 — Real Playwright Browser QA — Live GUI on Screen / Headless (`SKILL-17`, `SKILL-20` to `SKILL-23`, `SKILL-36`)**:
   - **Never stop to ask the user to reload MCP servers or restart the IDE window**: Even if `mcp_playwright_*` tools are not registered in the current chat turn, execute `node .agents/scripts/run-browser-audit.mjs http://127.0.0.1:<port>` directly via `run_command` (or let `run-audit.py` auto-boot an ephemeral server and run it automatically).
   - **Live GUI Window on Screen**: On desktop environments with `$DISPLAY` / `$WAYLAND_DISPLAY`, Playwright automatically opens a visible Google Chrome window directly on screen with a Floating HUD Status Banner, glowing field outlines, and auto-dialog handling so the user can watch the automation execute live. On headless servers or CI/CD pipelines, it falls back smoothly to headless mode (or via `--headless`).
   - Verify Desktop (`1440x900`) and Mobile (`375x812`) viewports for HTTP `200`, `0px` horizontal overflow, WCAG 2.2 AA computed DOM contrast (`>= 4.5:1`), `0` overlapping text elements, and `0` JS/network errors.
5. **Phase 4 — Complete 38-Skill & 15-Domain Final Quality Gate (`SKILL-33` to `SKILL-38`)**:
   - Output the complete **15-Domain Final Quality Gate Table (`Gate 01` through `Gate 15`, covering `SKILL-01` through `SKILL-38`)**. Never truncate the final table to 5 rows.
   - Fix every `FAIL` defect in code and re-run `run-audit.py` until all applicable checks pass before issuing a **`READY`** verdict.
   - Never deploy to production unless all applicable gates are `PASS` and the user explicitly requested deployment.

## 3. Foreground Visibility & Single Full Audit Lifecycle ("DIJALANKAN DI LATAR DEPAN SEKALI SAJA, JANGAN DIULANG DI SETIAP REVISI")

- **Foreground Live Visibility (Latar Depan & Nyata)**:
  1. Seluruh pengujian browser (Playwright UI/UX, kontras, overflow, mobile reflow) wajib berjalan di **latar depan (*foreground*)**. Pada komputer dengan monitor desktop, Playwright otomatis membuka jendela Google Chrome langsung di layar dengan Floating HUD Banner, glowing highlights, dan slowMo sehingga pengguna dapat melihat pengujian berjalan secara visual.
  2. Seluruh pengujian unit/CRUD backend (`phpunit --testdox`, `npm test`, `pytest -v`) dan audit CI/CD wajib dicetak secara terperinci baris demi baris di chat/terminal latar depan.
- **Single-Run on Initialization / On-Demand (Hanya Dijalankan Sekali di Awal)**:
  1. Audit menyeluruh 38 skill di latar depan (`run-audit.py . --force-all`) **HANYA dijalankan sekali saja** saat inisialisasi awal proyek (setelah `git clone`), saat *bootstrap* (`setup-project.py`), atau ketika pengguna secara eksplisit meminta audit aplikasi.
  2. **DILARANG MENGULANG AUDIT 38-SKILL PENUH DI SETIAP REVISI KODE KECIL**:
     Saat pengguna meminta perbaikan kecil, revisi teks, penambahan kolom, atau perbaikan bug sederhana pada kode:
     - AI **DILARANG KERAS** menjalankan ulang seluruh 38 skill dan browser audit yang memakan waktu lama.
     - AI **HANYA** menjalankan pengujian terarah (*targeted incremental test*) yang relevan dengan berkas yang sedang diubah (misalnya hanya menjalankan 1 file unit test terkait atau linter pada file tersebut).
- **Kewajiban Pengingat di Akhir Tanggapan**:
  Setiap kali audit penuh 38-skill selesai dijalankan, AI **WAJIB** menyertakan pesan pengingat berikut di akhir tanggapannya (menggunakan bahasa percakapan yang ramah tanpa sintaks Python/terminal):
  > 💡 **Informasi Pelaksanaan Audit:**  
  > Audit menyeluruh 38 skill (Live GUI Playwright, CRUD, CI/CD, dan UI/UX) telah selesai dijalankan di latar depan. Untuk mempercepat proses revisi kode berikutnya, audit penuh ini **hanya dijalankan sekali dan tidak akan diulang otomatis di setiap perubahan kecil**.  
  > Jika Anda ingin menjalankan ulang audit menyeluruh ini kapan saja, Anda cukup menyampaikan di chat:  
  > **"Audit kode kita, bila perlu git clone ulang skill ini lalu kerjakan"** (atau prompt sejenisnya).
