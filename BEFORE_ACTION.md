# Master Execution & Evidence-Streaming Protocol (`BEFORE_ACTION.md`)

> **CRITICAL BINDING DIRECTIVE FOR AI CODING AGENTS (ANTIGRAVITY / CLAUDE / CHATGPT / AGENT SKILLS)**  
> When the user prompts:  
> **"git clone kan skill ini kemudian kerjakan sesuai skill tersebut"**  
> *(or any variation such as "audit aplikasi kita dengan skill ini", "kerjakan sesuai skill", or "jalankan testing dan audit menyeluruh")*  
> 
> **THE "NO SHORTCUTS & NO BLACK-BOX" RULE**:  
> You are strictly prohibited from acting as a "black-box" that jumps directly to the final summary table. You must NOT be lazy or seek the path of least resistance. Every single step of analysis, terminal testing, and browser interaction MUST be printed progressively in the chat so the user can verify real progress in real time.
> 
> **YOU MUST EXECUTE THE FOLLOWING 5-PHASE PROTOCOL IN EXACT ORDER:**

---

## Phase 0: Ground-Truth Pre-Flight Diagnostic

Before doing anything else, execute the bundled diagnostic script to establish empirical facts about the project:

```bash
python3 .agents/skills/ai-skills/scripts/run-audit.py .
# (or python3 reusable-ai-development-skills/scripts/run-audit.py . if in root)
```

**Required Chat Output:**  
Print the raw pre-flight report in chat, detailing:
- Verified Technology Stack (Laravel, Node/React/Next, Django, FastAPI, Go, etc.).
- Environment and Secret Health (`.env` vs `.env.example`, `APP_DEBUG` status, sensitive token leaks).
- Active Local Ports (`3000`, `5173`, `8000`, `8080`).
- Configured Test Runner availability.

---

## Phase 1: Real Application Workflow Analysis (Anti-Hallucination Grounding)

Before writing or running tests, you must inspect the actual codebase to understand the real user workflows so tests are grounded in real routes and logic rather than hallucinated assumptions:

1. **Map Real Application Endpoints and Data Contracts**:
   - Inspect router definitions (`routes/web.php`, `routes/api.php`, `src/app/**/route.ts`, `urls.py`, etc.).
   - Inspect controllers, form requests, and database schema migrations (`SKILL-24`).
2. **Output the Workflow Map in Chat**:
   Print the concrete application workflow map in chat before testing:
   ```text
   [ALUR KERJA APLIKASI TERDETEKSI]:
   1. Autentikasi: POST /login -> Verifikasi session & CSRF token.
   2. Halaman Utama: GET /dashboard -> Render tabel data.
   3. Operasi CRUD:
      - Create: GET /items/create (Form) -> POST /items (Simpan data)
      - Read: GET /items (Tabel data) & GET /items/{id} (Detail)
      - Update: GET /items/{id}/edit -> PUT/PATCH /items/{id}
      - Delete: DELETE /items/{id} -> Status 200/204
   ```

---

## Phase 2: Live Backend & CRUD Unit Testing (Real Terminal Output)

You MUST execute the project's native test runner via `run_command` in the terminal and **display the actual test progress and output directly in chat**:

1. **Execute Native Test Suite**:
   - Node / React / Vue: `npm test` or `npm test -- --run`
   - PHP / Laravel: `php artisan test` or `./vendor/bin/pest`
   - Python: `pytest -v`
   - Go: `go test -v ./...`
2. **Strict Transparency Rule**:
   - **Do NOT** simply state "All tests passed".
   - You MUST output the actual terminal stdout showing each test case, assertions, execution time, and exit code.
   - If any test fails with a 500, 404, or 403 error, fix the root-cause in the code (`SKILL-34`, `SKILL-16`), re-run the test command, and show the passing re-run in chat.

---

## Phase 3: Step-by-Step Browser QA with Playwright MCP (Live Progress Stream)

When web/frontend views are in scope, you must execute interactive browser verification. **Every single step must be reported in chat as it happens**:

### 1. Check Pre-requisites:
- Confirm local dev server is running (e.g. `http://localhost:3000` or `http://127.0.0.1:8000`).
- Check if Playwright MCP tools (`browser_navigate`, `browser_snapshot`, `browser_click`, `browser_resize`) are active.

### 2. If Playwright MCP is AVAILABLE, Output Each Step Live in Chat:
```text
🌐 [Step 1: Navigasi Browser]
   -> Membuka URL: http://localhost:<port>/<route> via browser_navigate
   -> Status: HTTP 200 OK, Page Title: "<title>"

📸 [Step 2: Inspeksi DOM & Kontras]
   -> Memanggil browser_snapshot(boxes=true)
   -> Elemen terdeteksi: Form input, tombol submit [ref=...], tabel data
   -> Rasio kontras teks: PASS (>= 4.5:1, tidak ada teks putih di kolom putih)

🖱️ [Step 3: Interaksi CRUD Nyata]
   -> Mengisi form via browser_fill_form & klik tombol submit via browser_click
   -> Hasil: Data baru berhasil disimpan dan muncul di tabel data

📱 [Step 4: Audit Tampilan Mobile View (375x812)]
   -> Mengubah ukuran viewport via browser_resize (width: 375, height: 812)
   -> Memeriksa bounding boxes: Target sentuh >= 44x44px, tidak ada teks bertindih, horizontal scroll: 0px (PASS)

🛡️ [Step 5: Audit Console & Network Runtime]
   -> Memeriksa browser_console_messages: 0 error merah, 0 uncaught exception
   -> Memeriksa browser_network_requests: Semua request API mengembalikan status 200/201/204
```

### 3. If Playwright MCP is NOT Available or Server is Inactive:
- You are **STRICTLY FORBIDDEN** from simulating or pretending browser testing passed.
- You MUST report honestly in chat:
  ```text
  ⛔ [BROWSER TESTING BLOCKED]:
  Tool Playwright MCP tidak terdaftar di sesi ini atau server lokal belum menyala.
  Sesuai aturan SKILL-17, pengujian browser nyata tidak dapat dijalankan secara fiktif.
  Status Browser QA: BLOCKED.
  ```

---

## Phase 4: Final Quality Gate Sign-Off (`SKILL-38`)

Only after Phases 0, 1, 2, and 3 have been executed and displayed in chat, assemble the final release table:

| Domain Audit | Status | Bukti Nyata yang Ditampilkan di Chat |
| :--- | :---: | :--- |
| **1. Analisa Alur & Prasyarat** | `PASS` | Alur kerja aplikasi terpetakan di Phase 1 |
| **2. Lingkungan & Secret** | `PASS` / `FAIL` | Output dari `run-audit.py` (.env check) |
| **3. Automated Tests & CRUD** | `PASS` / `FAIL` | Log terminal asli dari Phase 2 (exit code 0) |
| **4. Browser QA & Mobile View** | `PASS` / `BLOCKED` | Log Playwright MCP dari Phase 3 (atau BLOCKED) |
| **5. Build & Keamanan OWASP** | `PASS` / `FAIL` | Output build & verifikasi CSRF/Auth |

### Official Release Verdict Rules:
- **`READY`**: Diberikan HANYA JIKA seluruh Phase 0 sampai Phase 3 dieksekusi nyata dan lulus dengan bukti log terminal/browser di chat.
- **`BLOCKED`**: Diberikan jika ada tes yang gagal, Playwright MCP tidak aktif, server mati, atau ada phase yang dilewati.
