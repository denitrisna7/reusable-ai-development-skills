# Reusable AI Development Skills Library for Antigravity (`v1.9.2`)

A comprehensive, modular, technology-agnostic **38-skill software engineering lifecycle library** designed for **Google Antigravity** (App, CLI, and IDE) and compatible **Agent Skills (`agentskills.io`)** environments.

---

## 📌 Riwayat Perubahan Setiap Push (Changelog & Release History)

Seluruh rincian perubahan juga tercatat lengkap di [`CHANGELOG.md`](./CHANGELOG.md):

| Versi | Commit SHA | Tanggal | Ringkasan Perubahan yang Di-Push ke GitHub |
| :--- | :---: | :---: | :--- |
| **`v1.9.2` (Terbaru)** | `HEAD` | 2026-11-03 | **Conversational User Reminder & Simplified Human-Friendly Rerun Prompt**: Mengganti teks pengingat pasca-audit berbasis perintah baris perintah teknis (*Python CLI*) menjadi percakapan alami yang jauh lebih ramah (*"Audit kode kita, bila perlu git clone ulang skill ini lalu kerjakan"* atau sejenisnya) sehingga pengguna cukup meminta di chat tanpa perlu mengetik perintah terminal. |
| **`v1.9.1`** | `b7b1a5d` | 2026-11-03 | **Deep Dynamic Crawling, Interactive Widget QA, & Error 404 Visual Alerts**: Meningkatkan *crawler* rute Playwright hingga 25 rute publik dan 20 rute dashboard admin; menambahkan deteksi visual Error 404 (Halaman Tidak Ditemukan) dengan HUD Banner bahaya merah dan pencatatan defek; serta menambahkan pengujian interaktivitas elemen (akordeon, FAQ toggle, tab) dan *smooth scroll* visual pada mode *headed*. |
| **`v1.9.0`** | `a93b1b2` | 2026-11-03 | **Foreground Single-Run Execution & Fast Revision Mode**: Memastikan seluruh pengujian (Live GUI Playwright, CRUD, CI/CD, UI/UX) berjalan di latar depan (*foreground*); menetapkan bahwa audit menyeluruh 38 skill hanya dijalankan sekali di awal (tidak diulang otomatis di setiap revisi kode kecil agar proses tetap cepat); serta mewajibkan AI menyertakan pengingat cara memanggil ulang audit di akhir tanggapan. |
| **`v1.8.0`** | `49add2e` | 2026-11-03 | **Mandatory All-38-Skill Forced Execution & Zero-Touch Project Bootstrap (`setup-project.py` & `--force-all`)**: Menambahkan aturan mutlak Anti-Cherry-Picking (`AGENTS.md`, `rules/AGENTS.md`, `BEFORE_ACTION.md`) yang melarang keras AI hanya menjalankan *"yang dibutuhkan saja"*; skrip `setup-project.py` otomatis menginjeksi aturan ke `<target>/AGENTS.md`, `<target>/.gemini/rules/AGENTS.md`, dan `.agents/skills.json`; memperbarui seluruh 38 deskripsi `SKILL.md` agar bebas dari klausul eksklusi negatif (`Do not use for...`); menambahkan opsi `--force-all` di `run-audit.py` untuk mengevaluasi dan mencetak rincian aktif seluruh 38 skill (`38/38 skills verified`). |
| **`v1.7.0`** | `36d5ecd` | 2026-10-31 | **Live GUI Playwright Browser on Screen by Default (`run-browser-audit.mjs` & `run-audit.py`)**: Playwright secara otomatis mendeteksi display desktop (`$DISPLAY` / `$WAYLAND_DISPLAY`) dan membuka jendela Google Chrome nyata di layar monitor pengguna (`headless: false`, slowMo 250ms, Floating HUD Banner, glowing highlights, auto-accept dialogs, 3s visual hold), dengan fallback otomatis ke headless mode di server CI/CD atau opsi `--headless`; opsi CLI `--headed`, `--headless`, `--slowmo`, `--hold`. |
| **`v1.6.0`** | `2618956` | 2026-10-30 | **Deep Audit Architecture (`rules/AGENTS.md`, Pinpoint DOM Overflow/Contrast Selector, & Zero False-Positive 38-Skill Engine)**: Menambahkan `rules/AGENTS.md` & `AGENTS.md` agar Antigravity otomatis memuat aturan eksekusi ke dalam `<user_rules>` di setiap sesi; memperbarui `run-browser-audit.mjs` untuk mendeteksi URL rute penuh (`{{ route(...) }}`), mengabaikan *drawer* mobile yang tertutup (`-translate-x-full`), serta mencetak *class selector* pasti pada `CONTRAST FAIL` dan `OVERFLOW CULPRIT`; menghilangkan *false positive* regex (`SKILL-12`, `SKILL-14`, `SKILL-27`, `SKILL-28`) dan mengganti 12 jebakan `REVIEW` statis menjadi verifikasi otomatis deterministik di `run-audit.py`. |
| **`v1.5.2`** | `a1a4b34` | 2026-10-30 | **Registrasi Otomatis `.agents/skills.json` & Evaluasi 38 Skill Berbasis Bukti Nyata (0 Hardcoded `PASS`)**: Mengatasi batas *scan* 1 level direktori `.agents/skills/` di Antigravity dengan mendaftarkan `.agents/skills.json` (`{"entries":[{"path":".agents/skills/ai-skills/skills"}]}`) secara otomatis; mengganti 19 status `PASS` statis di `scripts/run-audit.py` menjadi pemindaian kode/runtime nyata (`PASS` / `FAIL` / `WARN` / `N/A` / `REVIEW`) di seluruh 38 skill (`SKILL-01` s/d `SKILL-38`); serta membersihkan variabel `ANTIGRAVITY_AGENT` agar `php artisan test` tidak terpotong menjadi 1 baris JSON. |
| **`v1.5.1`** | `01fb565` | 2026-10-30 | **Universal Multi-Stack Audit & Server Auto-Boot**: Menambahkan auto-boot ephemeral server untuk Next.js (`npx next dev -p 18124`), Vite (`npx vite --port 18124`), Django (`manage.py runserver`), FastAPI/Flask, native PHP (`php -S`), dan Static HTML (`python3 -m http.server`); memperluas deteksi arsitektur/komponen lintas framework (Node/React/Vue/Python/Go/Flutter); menstandarkan `CI=true npm test` agar kompatibel dengan Node test runner, Jest, Vitest, dan Mocha. |
| **`v1.5.0`** | `86cff59` | 2026-10-30 | **Full 38-Skill Code Audit & Context-Budget Optimization**: Memadatkan `description` frontmatter di 38 `SKILL.md` (`-53.3%` ukuran karakter) & menghapus duplikat `sources/anti-slop/skills/*/SKILL.md` agar tidak ada skill yang terpotong oleh *context budget* Antigravity; `run-audit.py` kini otomatis menginstal `.agents/` dan mencetak **Matriks Verifikasi 38 Skill (`SKILL-01` s/d `SKILL-38`)** + **15-Domain Final Quality Gate**; menambahkan `slopcheck.py`/`slopcheck.sh`, scan repo penuh di `contrast-check.py`, serta dukungan warna `oklab()`/`oklch()` Tailwind v4 di `run-browser-audit.mjs`. |
| **`v1.4.0`** | `2668aea` / `16c6450` | 2026-10-30 | **Auto-Heal `PATH` & Zero-Reload Playwright**: `run-audit.py` otomatis menyambungkan binary `node`, `npm`, `npx`, `composer`, `flutter`, `dart` (mencegah `Exit Code 127`), otomatis menyalakan server lokal sementara jika belum aktif, auto-login dashboard, dan melarang AI berhenti meminta *Reload MCP / Sesi Baru*. |
| **`v1.3.0`** | `bf56a63` | 2026-10-30 | **Real Headless Chromium Runner (`run-browser-audit.mjs`) & 15-Domain Gate**: Menambahkan eksekutor Playwright Chromium langsung via CLI (audit Desktop `1440x900` & Mobile `375x812`, kontras DOM asli `>= 4.5:1`, deteksi teks bertindih, console/network error), bypass ringkasan 1-baris JSON Laravel 12 dengan `--testdox`, serta mewajibkan tabel penuh **15 Domain Quality Gate**. |
| **`v1.2.1`** | `a8b0ae5` | 2026-10-29 | **Workflow Mapping & Live Progress Streaming**: Mewajibkan analisa dan pemetaan alur kerja aplikasi nyata di Fase 1 sebelum menjalankan unit test serta menampilkan progres pengujian secara bertahap di chat. |
| **`v1.2.0`** | `d8ae779` | 2026-10-29 | **Master Protocol (`BEFORE_ACTION.md`) & `run-audit.py`**: Menambahkan protokol eksekusi satu perintah dan skrip diagnosa otomatis *pre-flight*. |
| **`v1.1.0`** | `1153c2f` | 2026-10-29 | **Anti-Hallucination Hardening**: Mengunci aturan larangan mengarang status `PASS` tanpa bukti output terminal nyata pada `SKILL-16`, `SKILL-17`, dan `SKILL-38`. |
| **`v1.0.1`** | `2ec7df2` | 2026-10-29 | **Quick Start & Chat Prompts**: Menambahkan panduan `git clone` cepat dan contoh perintah chat bahasa Indonesia/Inggris di halaman utama GitHub. |
| **`v1.0.0`** | `9c4ded2` | 2026-10-29 | **Initial Release**: Rilis perdana 38 modul AI Agent Skills (`SKILL-01` s.d. `SKILL-38`), 8 dokumen referensi bersama, `contrast-check.py`, dan `validate-skills.py`. |

---

## 1. Purpose of the Library

Modern AI coding agents frequently fail in predictable ways when working across diverse repositories: assuming a preferred framework, generating generic "AI slop" UI and code comments, skipping edge-case analysis, introducing subtle OWASP vulnerabilities, claiming tests passed without running them, or equating a passing build with production deployment readiness.

This library solves those problems by providing **38 focused, self-contained, and interoperable engineering skills** that guide an AI agent from initial repository discovery and requirements analysis through architecture, implementation, security hardening, automated and browser QA, accessibility, database/API/AI integration, performance profiling, CI/CD, and a binding **15-point Final Quality Gate**.

### Key Design Principles
- **Technology-Agnostic by Default**: Never forces Laravel Pint, PHPStan, Pest, `shadcn/ui`, Playwright, or GitHub Actions onto projects where they do not belong. Every skill inspects the actual repository first.
- **Progressive Disclosure**: Every `SKILL.md` is concise (`< 500` lines) with clear trigger descriptions, offloading deep reference matrices and scripts to `references/` and `scripts/` so token context stays lean.
- **Evidence Over Claims**: Enforces strict separation between verified facts and assumptions, and classifies all test and release checks into `PASS`, `FAIL`, `BLOCKED`, or `NOT TESTED`.
- **Zero Unauthorized Deployment**: Evaluates deployment readiness thoroughly while prohibiting unauthorized production deployments or destructive actions.

---

## 2. Quick Start: How to Use in Any Project (Tata Cara Penggunaan)

You can use this skill library in any project immediately so that Google Antigravity automatically detects all 38 skills and guides your workflow from requirements to pre-deployment release checks.

### Option 1 — Project-Specific via Git Clone (Rekomendasi per Proyek)
In the root directory of any new project (Laravel, React, Vue, Next.js, Django, Flutter, etc.):
```bash
# Clone into .agents/skills/ai-skills and run zero-touch bootstrap:
git clone https://github.com/denitrisna7/reusable-ai-development-skills.git .agents/skills/ai-skills && \
python3 .agents/skills/ai-skills/scripts/setup-project.py .
```
*Running `setup-project.py` (or `setup.sh`) automatically auto-injects `AGENTS.md` into `<target>/AGENTS.md`, `<target>/.gemini/rules/AGENTS.md`, and `<target>/.agents/rules/AGENTS.md`, registers `.agents/skills.json`, heals the PATH environment, and triggers the forced 38-skill audit.*

### Master Single-Command Trigger (Perintah 1 Kalimat Langsung Beres)
You can simply give this exact prompt to Antigravity:
> **Prompt**: *"git clone kan skill ini kemudian kerjakan sesuai skill tersebut: https://github.com/denitrisna7/reusable-ai-development-skills.git"*

Whenever Antigravity sees this command, it is bound by **[`BEFORE_ACTION.md`](./BEFORE_ACTION.md)** and **[`AGENTS.md`](./AGENTS.md)** to execute the forced 38-skill protocol strictly in order without cherry-picking or skipping:
1. **Aturan Mutlak Anti-Cherry-Picking**: AI dilarang keras hanya menjalankan *"yang dibutuhkan saja"*. Seluruh 38 skill (`SKILL-01` s/d `SKILL-38`) adalah satu paket wajib yang harus dievaluasi dan diverifikasi berurutan dengan bukti empiris terminal.
2. **Phase 0 (Before Action & Forced 38-Skill Audit)**: Menjalankan `python3 .agents/skills/ai-skills/scripts/run-audit.py . --force-all` untuk mengaudit seluruh 38 skill dan mencetak bukti nyata terminal di chat (`38/38 skills verified`).
3. **Phase 1 (Workflow & Architecture Map)**: Memeriksa rute, kontroler, role, dan mencetak peta alur kerja aplikasi nyata.
4. **Phase 2 (Verbose Unit & CRUD Tests)**: Menjalankan `./vendor/bin/phpunit --testdox --colors=never` (atau `npm test` / `pytest -v`) sehingga setiap kasus uji `✔` tercetak nyata di chat.
5. **Phase 3 (Live GUI / Chromium Playwright Browser QA on Screen)**: Menjalankan Playwright di layar monitor secara visual (Desktop `1440x900` & Mobile `375x812`), menguji kontras DOM WCAG AA (`>= 4.5:1`), floating HUD banner, glowing highlight elemen, zero overflow, dan zero error console.
6. **Phase 4 (Complete 15-Domain Final Quality Gate)**: Menampilkan tabel lengkap 15 Domain Quality Gate (mencakup `SKILL-01` s/d `SKILL-38`) beserta status `READY` atau `BLOCKED`.
7. **Siklus Sekali Jalan & Cepat Saat Revisi**: Audit menyeluruh latar depan ini dijalankan **sekali saja** di awal (atau saat diminta eksplisit). Untuk setiap revisi kode berikutnya, AI hanya menjalankan pengujian terarah (*targeted test*) yang relevan agar proses tetap cepat, serta selalu mengingatkan perintah untuk memanggil ulang audit jika diperlukan.

### Option 2 — Global Install Across All Projects (Pasang 1 Kali untuk Selamanya)
Install once to your machine's Antigravity global plugin directory to make all 38 skills available across all current and future projects on your computer:
```bash
git clone https://github.com/denitrisna7/reusable-ai-development-skills.git ~/.gemini/config/plugins/reusable-ai-development-skills
```
*(Or create a symlink if you already have the repository cloned locally):*
```bash
ln -s /home/denitrisna7/Documents/Apps/Deni/Skill/reusable-ai-development-skills ~/.gemini/config/plugins/reusable-ai-development-skills
```

---

### How to Prompt Antigravity in Chat (Contoh Perintah Chat)

Once installed, talk to Antigravity naturally in English or Indonesian. The library routes your requests to the appropriate skills automatically:

#### A. Sebelum Deployment ke Server / Hosting (Pre-Deployment Release Gate)
> **Prompt**: *"Tolong jalankan audit kesiapan rilis (pre-deployment check) sebelum saya deploy proyek ini ke server/hosting."*  
> *(English: "Run a pre-deployment readiness check and final quality gate audit before deploying to production.")*

**What Antigravity executes:**
- **Credentials & Secret Audit** (`SKILL-32` & `SKILL-10`): Scans `.env`, verifies production configuration schemas, ensures zero API keys or secrets leak into client bundles, and verifies debug mode is disabled.
- **Responsive Layout & Mobile Audit** (`SKILL-23`): Tests viewports (`320px` to `1440px`), ensures minimum `44x44px` touch targets, eliminates horizontal scroll leaks, and checks mobile viewport behavior.
- **Database & Migration Safety** (`SKILL-24`): Checks that all migrations are reversible, foreign keys are guarded, and transactions are ACID-safe.
- **Binding Release Verdict** (`SKILL-38` & `SKILL-33`): Issues a formal verdict:
  - **`READY`**: Safe to proceed with production deployment.
  - **`BLOCKED`**: Critical security or architectural defect identified; deployment blocked until resolved.

#### B. Pengujian Siklus CRUD & Verifikasi Browser
> **Prompt**: *"Buatkan fitur manajemen user lengkap dengan pengujian siklus CRUD-nya sampai ke tampilan browser."*  
> *(English: "Implement the user management feature with complete CRUD testing and browser verification.")*

**What Antigravity executes:**
- Anti-slop clean architecture without boilerplate or placeholders (`SKILL-05` & `SKILL-06`).
- Full lifecycle automated backend tests: *Create -> Read -> Update -> Delete -> Post-delete 404* (`SKILL-16`).
- Real browser flow and form verification with Playwright MCP snapshots (`SKILL-17`).

#### C. Audit Frontend, UI/UX, & Aksesibilitas Mobile
> **Prompt**: *"Audit tampilan halaman ini, pastikan responsif di mobile dan aksesibilitasnya memenuhi standar WCAG AA."*  
> *(English: "Audit this page for responsive mobile layout, WCAG 2.2 AA contrast, and semantic landmarks.")*

**What Antigravity executes:**
- Semantic HTML, focus trap in modals, and keyboard navigation (`SKILL-21`).
- Exact color contrast calculation via `contrast-check.py` (`SKILL-21`).
- Core Web Vitals profiling (`LCP <= 2.5s`, `INP <= 200ms`, `CLS <= 0.1`) (`SKILL-22` & `SKILL-29`).

#### D. Tips Penting: Mencegah AI Memotong Kompas / Mengarang Status PASS
Jika Anda mendapati AI "loncat" langsung ke kesimpulan PASS tanpa mengeksekusi terminal atau Playwright:
1. **Periksa Ketersediaan Playwright MCP**: Pastikan plugin atau server `@playwright/mcp` sudah terkonfigurasi di sesi Antigravity Anda. Tanpa MCP browser, AI tidak memiliki alat untuk membuka browser dan wajib melaporkan status `BLOCKED`.
2. **Pastikan Server Lokal / Dev Server Menyala**: AI tidak bisa menguji web jika `npm run dev`, `php artisan serve`, atau server lokal belum berjalan.
3. **Gunakan Perintah Berbasis Bukti Nyata (Evidence-Based Prompt)**:
   > *"Jalankan perintah unit test di terminal sekarang dan tampilkan log output aslinya. Buka web di browser via Playwright MCP dan periksa console error. Jika tool Playwright MCP tidak tersedia atau server belum menyala, laporkan statusnya BLOCKED secara jujur dan jangan mengarang status PASS."*

---

## 3. Directory Structure

```text
reusable-ai-development-skills/
├── README.md                                  # Master library documentation & installation guide
├── plugin.json                                # Native Antigravity plugin manifest for bundle installation
├── SKILL_CATALOG.md                           # Complete catalog of all 38 skills & activation criteria
├── SKILL_ROUTING.md                           # Lifecycle workflow, routing matrix, & interoperability guide
├── SOURCES.md                                 # Primary research manifest, licenses, & maintenance guide
├── COMPLETENESS_AUDIT.md                      # 38-skill coverage verification & validation audit report
├── scripts/
│   └── validate-skills.py                     # Zero-dependency Python 3 validator for all 38 skills
├── references/                                # Shared cross-skill technical reference manuals
│   ├── anti-slop-engineering-reference.md
│   ├── core-web-vitals-performance-reference.md
│   ├── deployment-readiness-quality-gate-matrix.md
│   ├── owasp-asvs-top10-reference.md
│   ├── playwright-mcp-reference.md
│   ├── shadcn-ui-design-system-reference.md
│   ├── technology-stack-detection-matrix.md
│   └── wcag22-accessibility-reference.md
├── sources/                                   # Isolated primary upstream research repositories & snapshots
│   ├── README.md                              # Inventory and untrusted-input handling rules for sources/
│   ├── agentskills/                           # Cloned agentskills.io specification & skills-ref validator
│   ├── anti-slop/                             # Cloned miqdadbadjuber/anti-slop repository (MIT)
│   ├── playwright-mcp/                        # Cloned microsoft/playwright-mcp repository (Apache-2.0)
│   └── web-docs/                              # HTML snapshots of OWASP, WCAG 2.2, shadcn/ui, Web Vitals, etc.
└── skills/                                    # The 38 reusable Agent Skills (SKILL-01 through SKILL-38)
    ├── project-discovery/SKILL.md
    ├── requirements-analysis/SKILL.md
    ├── adaptive-architecture/SKILL.md
    ├── technical-decision-records/SKILL.md
    ├── ai-anti-slop/
    │   ├── SKILL.md
    │   └── references/anti-slop-rules.md
    ├── adaptive-engineering/SKILL.md
    ├── code-quality-static-analysis/SKILL.md
    ├── refactoring-legacy-safety/SKILL.md
    ├── dependency-supply-chain-security/SKILL.md
    ├── application-security-owasp/
    │   ├── SKILL.md
    │   └── references/owasp-asvs-checklist.md
    ├── api-security-webhook-reliability/SKILL.md
    ├── privacy-data-protection/SKILL.md
    ├── threat-modeling-risk-assessment/SKILL.md
    ├── ai-security-prompt-injection/SKILL.md
    ├── testing-strategy-design/SKILL.md
    ├── backend-testing-tdd/SKILL.md
    ├── playwright-mcp-browser-qa/
    │   ├── SKILL.md
    │   └── references/playwright-mcp-tools.md
    ├── test-data-environment-isolation/SKILL.md
    ├── test-reporting-failure-diagnosis/SKILL.md
    ├── ui-ux-design-systems/
    │   ├── SKILL.md
    │   └── references/shadcn-ui-patterns.md
    ├── accessibility-engineering/
    │   ├── SKILL.md
    │   ├── references/wcag22-checklist.md
    │   └── scripts/contrast-check.py
    ├── frontend-performance/SKILL.md
    ├── cross-browser-responsive-qa/SKILL.md
    ├── database-architecture-integrity/SKILL.md
    ├── query-optimization-performance/SKILL.md
    ├── import-export-data-processing/SKILL.md
    ├── api-external-service-integration/SKILL.md
    ├── ai-provider-integration/SKILL.md
    ├── performance-profiling-optimization/
    │   ├── SKILL.md
    │   └── references/core-web-vitals.md
    ├── caching-background-jobs/SKILL.md
    ├── ci-cd-release-engineering/
    │   ├── SKILL.md
    │   └── references/ci-cd-security-hardening.md
    ├── environment-configuration-management/SKILL.md
    ├── deployment-readiness/SKILL.md
    ├── observability-incident-diagnosis/SKILL.md
    ├── backup-recovery-disaster-preparedness/SKILL.md
    ├── seo-web-discoverability/SKILL.md
    ├── documentation-developer-handoff/SKILL.md
    └── final-quality-gate/
        ├── SKILL.md
        └── references/gate-checklist.md
```

---

## 4. Role of Every Skill (01–38)

### A. Core Discovery and Planning
1. **`project-discovery` (`SKILL-01`)**: Inspects repository structure, languages, frameworks, runtimes, package managers, entry points, databases, test tools, and security-sensitive modules—separating verified facts from assumptions.
2. **`requirements-analysis` (`SKILL-02`)**: Translates ambiguous prompts into explicit functional/non-functional requirements, user workflows, edge cases, failure states, and Given/When/Then acceptance criteria.
3. **`adaptive-architecture` (`SKILL-03`)**: Evaluates existing architecture, dependency boundaries, and trade-offs to plan incremental changes without unnecessary rewrites.
4. **`technical-decision-records` (`SKILL-04`)**: Authors and maintains Architecture Decision Records (ADRs), API contracts, setup guides, and dependency documentation aligned with actual code.

### B. Core Development Quality
5. **`ai-anti-slop` (`SKILL-05`)**: Enforces the Craftsmanship Standard (`C-1`..`C-5`), the 40 Anti-Slop rules (`R-01`..`R-40`), Liveliness Toolkit dials, code comment hygiene, copywriting discipline, and the 4-block Delivery Gate.
6. **`adaptive-engineering` (`SKILL-06`)**: Adapts implementation code to the project's actual language, framework version, idioms, and conventions.
7. **`code-quality-static-analysis` (`SKILL-07`)**: Runs and interprets stack-appropriate linters, formatters, type checkers, and static analyzers while checking complexity, duplication, and error handling.
8. **`refactoring-legacy-safety` (`SKILL-08`)**: Guides behavior-preserving incremental refactoring, characterization testing, dead-code verification, and backward compatibility.
9. **`dependency-supply-chain-security` (`SKILL-09`)**: Audits direct and transitive dependencies, lockfiles, CVEs, package provenance, and post-install script risks.

### C. Security Engineering
10. **`application-security-owasp` (`SKILL-10`)**: Enforces OWASP ASVS (L1/L2/L3) and OWASP Top 10 controls across authn/authz, SQLi, XSS, CSRF, IDOR, sessions, file uploads, rate limiting, and secrets.
11. **`api-security-webhook-reliability` (`SKILL-11`)**: Secures API endpoints and webhook consumers/producers with HMAC signature verification, replay protection, timeouts, retries, and idempotency keys.
12. **`privacy-data-protection` (`SKILL-12`)**: Enforces data minimization, PII encryption/masking, log redaction, right-to-erasure deletion, AI prompt PII filtering, and regulatory compliance.
13. **`threat-modeling-risk-assessment` (`SKILL-13`)**: Maps assets, trust boundaries, attack surfaces, and STRIDE threats to prioritize mitigations and document residual risks.
14. **`ai-security-prompt-injection` (`SKILL-14`)**: Defends AI/LLM workflows against direct/indirect prompt injection, unsafe tool execution, RAG poisoning, and unvalidated output rendering.

### D. Testing and Quality Assurance
15. **`testing-strategy-design` (`SKILL-15`)**: Selects the right mix of unit, integration, API, E2E, regression, performance, and security tests based on risk rather than raw test count.
16. **`backend-testing-tdd` (`SKILL-16`)**: Guides Red-Green-Refactor TDD and backend testing across domain logic, validation, auth matrix, database transactions, and external service mocks.
17. **`playwright-mcp-browser-qa` (`SKILL-17`)**: Conducts evidence-based browser QA using Playwright MCP accessibility snapshots (`browser_snapshot`, `browser_find`), console logs, and network inspection.
18. **`test-data-environment-isolation` (`SKILL-18`)**: Protects production data and prevents real payments/messages during tests using isolated test databases, deterministic fixtures, and mocks.
19. **`test-reporting-failure-diagnosis` (`SKILL-19`)**: Classifies every test result strictly as `PASS`, `FAIL`, `BLOCKED`, or `NOT TESTED` with reproduction steps, logs, and root-cause analysis.

### E. Frontend and User Experience
20. **`ui-ux-design-systems` (`SKILL-20`)**: Builds accessible, token-driven UI components, forms, tables, dialogs, and empty/loading/error/success states—integrating `shadcn/ui` when compatible with the project.
21. **`accessibility-engineering` (`SKILL-21`)**: Implements and audits WCAG 2.2 Level AA compliance, including semantic HTML, keyboard focus order, ARIA patterns, and deterministic contrast checking (`scripts/contrast-check.py`).
22. **`frontend-performance` (`SKILL-22`)**: Optimizes asset sizing, hero image `fetchpriority="high"`, JS/CSS bundles, rendering efficiency, caching, and Core Web Vitals mechanisms.
23. **`cross-browser-responsive-qa` (`SKILL-23`)**: Verifies multi-breakpoint layout reflow (`320px`–`1440px+`), `44x44px` touch targets, sticky nav clearance, and cross-browser compatibility.

### F. Data and Integrations
24. **`database-architecture-integrity` (`SKILL-24`)**: Designs normalized schemas, foreign key constraints, indexes, ACID transactions, concurrency locks, and zero-downtime expand-and-contract migrations.
25. **`query-optimization-performance` (`SKILL-25`)**: Eliminates N+1 queries, tunes composite/covering indexes, replaces deep `OFFSET` with keyset pagination, and verifies gains via `EXPLAIN ANALYZE`.
26. **`import-export-data-processing` (`SKILL-26`)**: Builds streaming, chunked, transactional CSV/spreadsheet imports and exports with header/type validation, formula-injection defense, and per-row error reporting.
27. **`api-external-service-integration` (`SKILL-27`)**: Engineers resilient outbound API clients with strict contracts, timeouts, exponential backoff + jitter, rate-limit handling, and circuit breakers.
28. **`ai-provider-integration` (`SKILL-28`)**: Integrates LLM/AI APIs with server-side key protection, structured schema outputs, token/cost caps, model fallbacks, and telemetry.

### G. Performance, Operations, and Deployment
29. **`performance-profiling-optimization` (`SKILL-29`)**: Establishes baseline metrics, profiles CPU/memory/DB/network and Core Web Vitals (`LCP`, `INP`, `CLS`), and verifies measurable improvements.
30. **`caching-background-jobs` (`SKILL-30`)**: Designs cache invalidation, stampede protection, idempotent queue workers, overlap-safe scheduled jobs, and dead-letter recovery.
31. **`ci-cd-release-engineering` (`SKILL-31`)**: Configures and hardens automated CI/CD pipelines, build/test gates, environment approvals, concurrency controls, and rollback workflows.
32. **`environment-configuration-management` (`SKILL-32`)**: Separates dev/staging/prod configurations, validates environment variables at startup, secures secrets, and prevents client-bundle secret leaks.
33. **`deployment-readiness` (`SKILL-33`)**: Audits build artifacts, config parity, migration safety, backups, HTTPS/permissions, queues, health checks, and rollback procedures prior to release.
34. **`observability-incident-diagnosis` (`SKILL-34`)**: Implements structured redacted logging, correlation IDs, metrics, tracing, health probes, and incident root-cause analysis.
35. **`backup-recovery-disaster-preparedness` (`SKILL-35`)**: Establishes 3-2-1 backup strategies, retention schedules, encrypted immutable backups, RPO/RTO alignment, and verified restore testing.
36. **`seo-web-discoverability` (`SKILL-36`)**: Optimizes public pages for metadata, canonicals, sitemaps, `robots.txt`, structured data, and crawlability while keeping private dashboards `noindex`.

### H. Final Quality and Maintenance
37. **`documentation-developer-handoff` (`SKILL-37`)**: Verifies that setup instructions, `.env.example`, test commands, architecture docs, and operational runbooks match the actual system.
38. **`final-quality-gate` (`SKILL-38`)**: Consolidates evidence across all 15 release domains and issues a binding release verdict: **`READY`**, **`READY WITH ACCEPTED RISKS`**, **`BLOCKED`**, or **`INCOMPLETE`**.

---

## 5. Recommended Usage Workflow & Skill Routing

See [`SKILL_ROUTING.md`](./SKILL_ROUTING.md) and [`SKILL_CATALOG.md`](./SKILL_CATALOG.md) for the complete routing decision matrix. In every project:
1. Run **`project-discovery`** first to establish the verified technology stack.
2. Run **`requirements-analysis`** to clarify scope, edge cases, and acceptance criteria.
3. Activate only the **relevant domain skills** for the task (e.g., UI skills for frontend tasks, database skills for schema changes).
4. Apply **`ai-anti-slop`** and **`application-security-owasp`** during implementation and review.
5. Verify changes with **`code-quality-static-analysis`**, **`backend-testing-tdd`**, and/or **`playwright-mcp-browser-qa`**, recording truthful results via **`test-reporting-failure-diagnosis`**.
6. Before declaring a release ready, evaluate **`deployment-readiness`** and execute **`final-quality-gate`**.

---

## 6. Advanced Global & Workspace Installation Options

> **Important Status Note**: By default, this library resides inside the workspace at `/home/denitrisna7/Documents/Apps/Deni/Skill/reusable-ai-development-skills/` (with a workspace `.agents/skills.json` pointer for the current workspace). It has **not** modified or overwritten your global `~/.gemini/config/` files.

To make these 38 skills available across **all future projects** in Google Antigravity, choose one of the three verified mechanisms supported by Antigravity:

### Option A — Global Declarative `skills.json` (Recommended, Zero Duplication)
Keep the library in a single canonical folder and register its `skills/` path in `~/.gemini/config/skills.json`. Antigravity scans each `entries` path one level deep for `<skill-name>/SKILL.md`:

```json
{
  "entries": [
    {
      "path": "/home/denitrisna7/Documents/Apps/Deni/Skill/reusable-ai-development-skills/skills"
    }
  ]
}
```
*(If `~/.gemini/config/skills.json` already exists, append the object to its `"entries"` array rather than overwriting existing entries.)*

### Option B — Install as a Global Antigravity Plugin Bundle
Because `reusable-ai-development-skills/` includes a valid `plugin.json` manifest and `skills/<skill-name>/SKILL.md` layout, you can install or symlink it as a single toggleable plugin:

```bash
# Via Antigravity CLI:
agy plugin install /home/denitrisna7/Documents/Apps/Deni/Skill/reusable-ai-development-skills

# Or copy/symlink into the global plugins directory and restart Antigravity:
ln -s /home/denitrisna7/Documents/Apps/Deni/Skill/reusable-ai-development-skills ~/.gemini/config/plugins/reusable-ai-development-skills
```

### Option C — Copy Individual or All Skills to Global or Workspace `.agents/skills/`
- **Global (All Workspaces — Antigravity App & IDE)**:
  ```bash
  mkdir -p ~/.gemini/config/skills
  cp -r /home/denitrisna7/Documents/Apps/Deni/Skill/reusable-ai-development-skills/skills/* ~/.gemini/config/skills/
  ```
- **Project-Specific (Team Sharing via Git)**:
  Add `.agents/skills.json` to your project repository pointing to the shared skills path, or copy selected skill folders into `<project-root>/.agents/skills/`.

---

## 7. Validation Procedures

Run the bundled validation script at any time to verify directory structure, `agentskills.io` frontmatter rules, required sections, line-count limits, and relative file links:

```bash
python3 reusable-ai-development-skills/scripts/validate-skills.py
```

For contrast checking during UI/Accessibility work (`SKILL-21`):
```bash
python3 reusable-ai-development-skills/skills/accessibility-engineering/scripts/contrast-check.py "#FFFFFF" "#777777"
```

---

## 8. Source Attribution, Licensing, and Maintenance

- All primary sources, upstream commit SHAs, licenses (`MIT`, `Apache-2.0`, `CC-BY-4.0`, `CC-BY-SA-4.0`, `W3C`), adaptations, and maintenance workflows are documented in [`SOURCES.md`](./SOURCES.md) and [`sources/README.md`](./sources/README.md).
- Original upstream repositories (`anti-slop`, `playwright-mcp`, `agentskills`) and HTML documentation snapshots are preserved separately in `sources/` and are never mixed into individual skill directories.

---

## 9. Known Limitations

1. **Session Restart on Initial Global Registration**: When adding a new plugin directory or global `skills.json` entry in Antigravity, start a new session or restart the Antigravity window so the skill index refreshes at startup.
2. **Runtime Tool Dependencies**: Skills such as `playwright-mcp-browser-qa` (`SKILL-17`) require the Playwright MCP server (`@playwright/mcp`) to be configured in the host agent's `mcp_config.json` when executing live browser tests; when unavailable, checks must be reported as `BLOCKED` or `NOT TESTED`.
3. **Human Sign-Off for Risk Acceptance**: The `final-quality-gate` (`SKILL-38`) status `READY WITH ACCEPTED RISKS` requires explicit human authorization and cannot be self-approved by an autonomous agent.
