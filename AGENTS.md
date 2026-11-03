# Reusable AI Development Skills — Mandatory Execution & Verification Rules

Whenever this library or plugin (`reusable-ai-development-skills`) is active in the workspace or cloned via `git clone`, you MUST follow these non-negotiable rules:

## 1. Pemisahan Mutlak Alur Kerja: Penambahan Fitur vs. Audit Penuh (Anti-Overtesting)

Sebelum mengambil tindakan apa pun, AI **WAJIB** mengidentifikasi maksud (*user intent*) dari pengguna:

### A. MODE PENAMBAHAN FITUR / REVISI KODE / PERBAIKAN BUG (DEFAULT):
- **Kondisi**: Pengguna meminta membuat fitur baru, menambah input/kolom, mengedit teks/tampilan, memperbaiki bug, mengajukan pertanyaan, atau merevisi kode.
- **ATURAN MUTLAK**:
  1. **DILARANG KERAS MENJALANKAN AUDIT 38-SKILL PENUH (`run-audit.py --force-all`)**.
  2. **DILARANG KERAS MELUNCURKAN PENGUJIAN PLAYWRIGHT BROWSER OTOMATIS**.
  3. **DILARANG KERAS MENJALANKAN FULL TEST SUITE** yang memakan waktu lama.
  4. AI **WAJIB LANGSUNG MENGERJAKAN** kode atau fitur yang diminta pengguna secara cepat, bersih, dan tepat sasaran.
  5. Jika butuh verifikasi pada kode yang baru diubah, AI **HANYA** menjalankan pengujian terarah (*targeted single test / linter*) pada berkas terkait saja, TANPA browser audit.

### B. MODE AUDIT PENUH 38-SKILL (HANYA ATAS PERMINTAAN EKSPLISIT ATAU INITIAL BOOTSTRAP):
- **Kondisi**: HANYA dijalankan saat:
  1. Proyek pertama kali diinisialisasi / di-bootstrap (`setup-project.py`) setelah `git clone`.
  2. Pengguna **SECARA EKSPLISIT MEMINTA DI CHAT** untuk mengaudit aplikasi (misal: *"Audit kode kita, bila perlu git clone ulang skill ini lalu kerjakan"* atau *"Audit aplikasi ini secara menyeluruh"*).
- **ATURAN MUTLAK**:
  1. Evaluasi seluruh 38 skill secara berurutan di latar depan (*foreground*).
  2. Setelah audit penuh selesai, sertakan pesan pengingat di akhir tanggapan, dan **JANGAN DIULANG** pada pesan/revisi/penambahan fitur berikutnya!

---

## 2. Pengujian Latar Depan (Live GUI Foreground di Layar) & Fitur Screenshot DIMATIKAN TOTAL

- **Fitur Screenshot DIMATIKAN TOTAL (Strictly Disabled & Forbidden)**:
  1. **DILARANG KERAS** menggunakan `browser_take_screenshot`, `page.screenshot()`, atau membuat file gambar screenshot (`.png`, `.jpg`) sebagai bukti pengujian!
  2. Menyuguhkan file gambar screenshot statis adalah tindakan terlarang karena menyembunyikan proses pengujian di latar belakang (RAM) dan membuang-buang token/berkas.
- **Wajib Foreground Live GUI di Layar Monitor Pengguna**:
  1. Seluruh pengujian browser (Playwright UI/UX, CRUD, navigasi rute, kontras, mobile reflow) **WAJIB berjalan di latar depan (*foreground*)**.
  2. Pada komputer dengan layar monitor desktop (`$DISPLAY` / `$WAYLAND_DISPLAY`), Playwright **WAJIB membuka jendela Google Chrome nyata langsung di depan layar pengguna (`headless: false`)**.
  3. Dilengkapi dengan **Floating HUD Status Banner**, **Glowing Highlights** pada form dan tombol, **SlowMo** (250-300ms), serta penanganan dialog otomatis (`dialog.accept()`) sehingga pengguna dapat melihat langsung jalannya pengujian (pengetikan form, klik tombol simpan/hapus, perpindahan menu) di depan mata mereka secara nyata.
  4. Seluruh pengujian unit/CRUD backend (`phpunit --testdox`, `npm test`, `pytest -v`) dan audit CI/CD wajib dicetak secara terperinci baris demi baris di chat/terminal latar depan.
  5. Bukti pengujian adalah penampakan nyata di layar monitor dan baris log terminal, **BUKAN file tangkapan layar screenshot**.

---

## 3. Absolute Rule of Forced 38-Skill Execution (Saat Mode Audit Aktif — Anti-Cherry-Picking)

Ketika Mode Audit Aktif (saat bootstrap awal atau permintaan eksplisit pengguna):
- **Zero Cherry-Picking Permitted**: You are STRICTLY FORBIDDEN from selecting only a subset of skills under the premise of *"hanya menjalankan yang dibutuhkan"*.
- **All 38 Skills Are Compulsory**: You MUST actively evaluate, execute, and verify ALL 38 skills (`SKILL-01` through `SKILL-38`) sequentially across the entire application as a unified software engineering lifecycle.
- **Active Verification for Every Skill**:
  1. For every domain existing in the project, cite concrete file and line evidence and active automated checks.
  2. For any technology or domain absent from the project, provide empirical search evidence (`0 matching files found`) and mark `N/A`.
- **Zero-Touch Bootstrap Auto-Execution**:
  When cloned or invoked, immediately ensure project rules and skills are active in the target workspace by running:
  `python3 .agents/skills/ai-skills/scripts/setup-project.py .`

---

## 4. Mandatory 5-Phase Execution Protocol (`BEFORE_ACTION.md`)

1. **Phase 0 — Ground-Truth Pre-Flight & Forced 38-Skill Auto-Audit**:
   - Run `python3 .agents/skills/ai-skills/scripts/run-audit.py . --force-all` and paste output in chat (`38/38 skills actively verified`).
2. **Phase 1 — Real Application Workflow & Architecture Map (`SKILL-01` to `SKILL-04`)**:
   - Inspect actual routes, controllers, models, roles, and print the complete workflow map.
3. **Phase 2 — Verbose Unit, CRUD, & Mobile Test Execution (`SKILL-05` to `SKILL-16`, `SKILL-18`, `SKILL-19`)**:
   - Never collapse unit tests into 1 line: run `./vendor/bin/phpunit --testdox --colors=never`, `CI=true npm test`, or `pytest -v`.
4. **Phase 3 — Real Playwright Browser QA — Live GUI on Screen (`SKILL-17`, `SKILL-20` to `SKILL-23`, `SKILL-36`)**:
   - Buka Google Chrome di layar monitor pengguna (`headless: false`, SlowMo, Floating HUD). Fitur screenshot dimatikan total.
5. **Phase 4 — Complete 38-Skill & 15-Domain Final Quality Gate (`SKILL-33` to `SKILL-38`)**:
   - Output the complete **15-Domain Final Quality Gate Table (`Gate 01` through `Gate 15`)**.

---

## 5. Kewajiban Pengingat di Akhir Tanggapan Audit

Setiap kali audit penuh 38-skill selesai dijalankan, AI **WAJIB** menyertakan pesan pengingat berikut di akhir tanggapannya:
> 💡 **Informasi Pelaksanaan Audit:**  
> Audit menyeluruh 38 skill (Live GUI Playwright, CRUD, CI/CD, dan UI/UX) telah selesai dijalankan di latar depan. Untuk mempercepat proses revisi kode berikutnya, audit penuh ini **hanya dijalankan sekali dan tidak akan diulang otomatis di setiap perubahan kecil**.  
> Jika Anda ingin menjalankan ulang audit menyeluruh ini kapan saja, Anda cukup menyampaikan di chat:  
> **"Audit kode kita, bila perlu git clone ulang skill ini lalu kerjakan"** (atau prompt sejenisnya).
