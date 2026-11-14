# Panduan Lengkap: Fungsi dan Kegunaan 38 Skill (`PANDUAN_FUNGSI_SKILL.md`)

Dokumen ini menjelaskan secara terperinci seluruh **38 Software Engineering Lifecycle Skills** yang ada di dalam pustaka **`reusable-ai-development-skills`**, fungsi spesifik masing-masing skill, dan skenario nyata kegunaannya.

Pustaka ini dirancang agar AI Coding Assistant (**Google Antigravity**, Claude, Cursor, Copilot) bekerja dengan standar rekayasa perangkat lunak profesional: **berbasis bukti empiris nyata, bebas halusinasi, dan tidak mengambil jalan pintas**.

---

## 📑 Daftar Isi Kategori

1. [Kategori A: Penemuan Proyek & Perencanaan Arsitektur (Skill 01–04)](#kategori-a-penemuan-proyek--perencanaan-arsitektur-skill-0104)
2. [Kategori B: Standar Kualitas Kode & Anti-Slop AI (Skill 05–09)](#kategori-b-standar-kualitas-kode--anti-slop-ai-skill-0509)
3. [Kategori C: Keamanan Aplikasi, OWASP & Proteksi AI (Skill 10–14)](#kategori-c-keamanan-aplikasi-owasp--proteksi-ai-skill-1014)
4. [Kategori D: Strategi Pengujian, TDD & Browser QA (Skill 15–19)](#kategori-d-strategi-pengujian-tdd--browser-qa-skill-1519)
5. [Kategori E: Desain UI/UX, Aksesibilitas & Responsif (Skill 20–23)](#kategori-e-desain-uiux-aksesibilitas--responsif-skill-2023)
6. [Kategori F: Database, Pemrosesan Data & Integrasi API (Skill 24–28)](#kategori-f-database-pemrosesan-data--integrasi-api-skill-2428)
7. [Kategori G: Optimasi Performa, CI/CD, DevOps & SEO (Skill 29–36)](#kategori-g-optimasi-performa-cicd-devops--seo-skill-2936)
8. [Kategori H: Dokumentasi Pengembang & Gerbang Rilis Final (Skill 37–38)](#kategori-h-dokumentasi-pengembang--gerbang-rilis-final-skill-3738)

---

## Kategori A: Penemuan Proyek & Perencanaan Arsitektur (Skill 01–04)

### `SKILL-01: project-discovery`
* **Fungsi Utama:** Melakukan inspeksi otomatis terhadap manifest dependensi (`composer.json`, `package.json`, `requirements.txt`, `pubspec.yaml`), mendeteksi stack teknologi, framework, entrypoint aplikasi, struktur direktori, dan skrip pembangunan yang ada.
* **Kegunaan / Kapan Dipakai:** Dijalankan pertama kali saat AI membuka repositori baru. Mencegah AI salah menebak framework (misal mengira Express padahal NestJS, atau mengira Laravel padahal native PHP).
* **Hasil Nyata:** Ringkasan stack teknologi terverifikasi, letak route, dan skrip pengujian yang valid.

### `SKILL-02: requirements-analysis`
* **Fungsi Utama:** Menerjemahkan instruksi pengguna yang samar atau informal menjadi kebutuhan fungsional (*functional requirements*), kebutuhan non-fungsional, dan kriteria penerimaan (*acceptance criteria*) berbasis skenario *Given-When-Then*.
* **Kegunaan / Kapan Dipakai:** Digunakan sebelum fitur baru mulai dikoding. Menghindari kesalahpahaman antara apa yang diminta pengguna dengan apa yang diimplementasikan oleh AI.
* **Hasil Nyata:** Daftar alur kerja pengguna (*user workflows*) dan batasan sistem yang jelas.

### `SKILL-03: adaptive-architecture`
* **Fungsi Utama:** Menganalisis batas-batas modul (*module boundaries*), pemisahan layer (Controller-Service-Repository), serta pola arsitektur yang sudah ada di proyek tanpa melakukan penulisan ulang (*rewrite*) yang tidak perlu.
* **Kegunaan / Kapan Dipakai:** Digunakan ketika ingin menambah modul baru atau merestrukturisasi fitur agar selaras dengan arsitektur bawaan proyek.
* **Hasil Nyata:** Rencana integrasi teknis yang menghormati arsitektur eksisting.

### `SKILL-04: technical-decision-records`
* **Fungsi Utama:** Mendokumentasikan keputusan arsitektur penting ke dalam format ADR (*Architecture Decision Record*) yang mencakup konteks masalah, opsi yang dipertimbangkan, keputusan yang diambil, dan konsekuensinya.
* **Kegunaan / Kapan Dipakai:** Digunakan saat ada perubahan arsitektur signifikan (misal ganti database, migrasi library auth, atau ganti state management).
* **Hasil Nyata:** Berkas `docs/adr/XXXX-nama-keputusan.md` yang tersinkronisasi dengan kode.

---

## Kategori B: Standar Kualitas Kode & Anti-Slop AI (Skill 05–09)

### `SKILL-05: ai-anti-slop`
* **Fungsi Utama:** Mendeteksi dan menghapus "AI Slop" — kebiasaan buruk AI seperti membuat tombol mati yang tidak ada fungsinya, teks placeholder klise (*Lorem ipsum*, deskripsi hiasan), komentar kode berlebihan yang mubazir, dan ikon palsu.
* **Kegunaan / Kapan Dipakai:** Menjamin kode dan antarmuka yang dihasilkan AI tampak profesional, nyata, dan memiliki fungsi bisnis konkret tanpa ornamen palsu.
* **Hasil Nyata:** Laporan audit eliminasi elemen palsu, tombol mati, dan teks placeholder.

### `SKILL-06: adaptive-engineering`
* **Fungsi Utama:** Menyelaraskan gaya koding AI dengan konvensi bahasa, idiom framework, versi runtime, dan *code style* yang sudah berlaku di dalam repositori.
* **Kegunaan / Kapan Dipakai:** Mencegah AI menulis kode JavaScript modern di proyek PHP legacy, atau menulis kodingan gaya Python 2 di proyek Python 3.12.
* **Hasil Nyata:** Kode bersih yang tampak ditulis oleh tim internal proyek tersebut.

### `SKILL-07: code-quality-static-analysis`
* **Fungsi Utama:** Menjalankan linter, formatters, type checker, dan analisis kompleksitas bawaan stack (misal `eslint`, `phpstan`, `mypy`, `dart analyze`).
* **Kegunaan / Kapan Dipakai:** Memastikan tidak ada error sintaks, kesalahan tipe data, atau pelanggaran gaya kode sebelum kode di-commit.
* **Hasil Nyata:** Output terminal linter dengan status lolos (*Exit Code 0*).

### `SKILL-08: refactoring-legacy-safety`
* **Fungsi Utama:** Memandu refaktor kode legacy secara aman dan bertahap (*incremental*) dengan memanfaatkan *regression harness* sehingga fungsionalitas lama tidak rusak.
* **Kegunaan / Kapan Dipakai:** Digunakan saat membersihkan *technical debt*, memecah file monolitik, atau mengganti fungsi usang (*deprecated*).
* **Hasil Nyata:** Kode lebih rapi dan bersih dengan bukti uji regresi bahwa fungsi tetap berjalan sama.

### `SKILL-09: dependency-supply-chain-security`
* **Fungsi Utama:** Memeriksa integritas berkas lockfile (`package-lock.json`, `composer.lock`, `poetry.lock`), memindai kerentanan dependensi (CVEs), serta mencegah *dependency confusion* atau injeksi paket berbahaya.
* **Kegunaan / Kapan Dipakai:** Digunakan saat menginstal pustaka baru atau melakukan audit rutin paket pihak ketiga.
* **Hasil Nyata:** Laporan `npm audit`, `composer audit`, atau `pip-audit` yang bersih dari kerentanan tinggi/kritis.

---

## Kategori C: Keamanan Aplikasi, OWASP & Proteksi AI (Skill 10–14)

### `SKILL-10: application-security-owasp`
* **Fungsi Utama:** Mengaudit aplikasi terhadap OWASP Top 10 dan standar ASVS: perlindungan dari SQL Injection, Cross-Site Scripting (XSS), CSRF, manipulasi sesi, otorisasi IDOR (*Insecure Direct Object References*), dan keamanan unggah berkas.
* **Kegunaan / Kapan Dipakai:** Wajib digunakan pada setiap fitur yang menerima input pengguna, sistem autentikasi, dan manipulasi data sensitif.
* **Hasil Nyata:** Validasi input ketat, penggunaan query berparameter (*prepared statements*), token CSRF, dan sanitasi output.

### `SKILL-11: api-security-webhook-reliability`
* **Fungsi Utama:** Mengamankan endpoint REST/GraphQL API dan merancang penanganan webhook yang aman dengan verifikasi tanda tangan kriptografis (*HMAC signature*), perlindungan *replay attack* (timestamp check), serta idempotensi.
* **Kegunaan / Kapan Dipakai:** Digunakan saat membuat atau mengintegrasikan webhook pembayaran (Midtrans, Stripe, Xendit) atau sinkronisasi data antar-server.
* **Hasil Nyata:** Webhook yang tidak bisa dipalsukan oleh penyerang dan aman dari eksekusi ganda.

### `SKILL-12: privacy-data-protection`
* **Fungsi Utama:** Melindungi data pribadi (*Personally Identifiable Information / PII*) melalui enkripsi data saat istirahat (*at rest*) dan saat transit (*in transit*), masking data pada log aplikasi, serta kepatuhan UU PDP / GDPR.
* **Kegunaan / Kapan Dipakai:** Digunakan pada fitur yang menangani nomor HP, NIK, rekam medis, alamat email, atau kata sandi.
* **Hasil Nyata:** Log sistem bersih dari kebocoran data rahasia dan database tersimpan aman.

### `SKILL-13: threat-modeling-risk-assessment`
* **Fungsi Utama:** Melakukan pemodelan ancaman (*threat modeling*) menggunakan kerangka kerja STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).
* **Kegunaan / Kapan Dipakai:** Digunakan pada fase perancangan fitur berisiko tinggi (misal transaksi keuangan, transfer hak akses admin, atau otentikasi multi-faktor).
* **Hasil Nyata:** Matriks risiko dan mitigasi keamanan yang diprioritaskan sebelum kode ditulis.

### `SKILL-14: ai-security-prompt-injection`
* **Fungsi Utama:** Melindungi fitur berbasis LLM/AI dari serangan *direct/indirect prompt injection*, manipulasi pemanggilan fungsi (*insecure tool calls*), dan kebocoran sistem prompt.
* **Kegunaan / Kapan Dipakai:** Digunakan jika aplikasi Anda memiliki fitur chatbot, asisten AI terintegrasi, atau pemrosesan dokumen berbasis AI.
* **Hasil Nyata:** Isolasi konteks input pengguna, pemisahan instruksi sistem, dan validasi skema sebelum fungsi dieksekusi.

---

## Kategori D: Strategi Pengujian, TDD & Browser QA (Skill 15–19)

### `SKILL-15: testing-strategy-design`
* **Fungsi Utama:** Merancang piramida pengujian (*test pyramid*) yang seimbang: proporsi unit test, integration test, dan end-to-end (E2E) test yang realistis untuk aplikasi.
* **Kegunaan / Kapan Dipakai:** Menentukan ruang lingkup pengujian sebelum mulai menulis kode tes otomatis.
* **Hasil Nyata:** Dokumen rencana pengujian dan penentuan skenario kritis yang wajib diuji.

### `SKILL-16: backend-testing-tdd`
* **Fungsi Utama:** Menulis dan mengeksekusi pengujian backend secara mendalam dengan format verbose (misal `./vendor/bin/phpunit --testdox`), menguji logika bisnis, model, controller, dan otorisasi peran.
* **Kegunaan / Kapan Dipakai:** Menjamin setiap baris kode backend berfungsi benar dan tidak regresi saat ada pembaruan di masa mendatang.
* **Hasil Nyata:** Laporan hasil pengujian baris demi baris (`✔ ...`) yang membuktikan fungsi Create, Read, Update, Delete (CRUD) berjalan sukses.

### `SKILL-17: playwright-mcp-browser-qa`
* **Fungsi Utama:** Menguji aplikasi web secara visual di peramban Chromium nyata di latar depan (*Live GUI on screen*) dengan kecepatan interaksi yang nyaman dilihat (*SlowMo*), Floating HUD Banner, efek sorotan bercahaya (*glowing outlines*), auto-login via `.env`, dan auto-accept dialog pop-up.
* **Kegunaan / Kapan Dipakai:** Memverifikasi alur nyata pengguna di browser: login admin, klik menu, pengisian form, pembukaan modal dialog, dan transisi halaman tanpa menggunakan screenshot statis yang sembunyi di background.
* **Hasil Nyata:** Jendela Chrome terbuka di layar monitor Anda, menguji seluruh alur secara nyata di depan mata Anda.

### `SKILL-18: test-data-environment-isolation`
* **Fungsi Utama:** Menjamin lingkungan pengujian terisolasi total dari database produksi, menggunakan database in-memory (`:memory:`), database khusus test (`_test`), dan seeder data dummy deterministik.
* **Kegunaan / Kapan Dipakai:** Mencegah terjadinya kecelakaan fatal di mana pengujian otomatis menghapus atau mengubah data asli pelanggan di server produksi.
* **Hasil Nyata:** Konfigurasi `.env.testing` yang aman dan seeder data simulasi.

### `SKILL-19: test-reporting-failure-diagnosis`
* **Fungsi Utama:** Mengumpulkan seluruh hasil pengujian dan menyajikan laporan komprehensif, mendiagnosa kegagalan secara spesifik (*root cause analysis*), dan memberikan langkah perbaikan yang tepat.
* **Kegunaan / Kapan Dipakai:** Digunakan ketika ada tes yang gagal agar developer tahu persis di baris dan logika mana kesalahannya terjadi.
* **Hasil Nyata:** Laporan PASS/FAIL berbasis bukti tanpa rekayasa.

---

## Kategori E: Desain UI/UX, Aksesibilitas & Responsif (Skill 20–23)

### `SKILL-20: ui-ux-design-systems`
* **Fungsi Utama:** Membangun antarmuka pengguna yang konsisten dan elegan berbasis design system modern (komponen Shadcn/UI, Tailwind CSS, Material Design, atau INA Digital Design System).
* **Kegunaan / Kapan Dipakai:** Menjamin tampilan antarmuka memiliki tipografi yang rapi, *spacing* konsisten, dan memiliki 4 status wajib: *ideal state*, *loading state*, *empty state*, dan *error state*.
* **Hasil Nyata:** Komponen antarmuka yang siap pakai, tidak kaku, dan ramah pengguna.

### `SKILL-21: accessibility-engineering`
* **Fungsi Utama:** Mengaudit dan menerapkan kepatuhan aksesibilitas web **WCAG 2.2 Level AA**, termasuk rasio kontras warna minimal `4.5:1` untuk teks normal, navigasi keyboard penuh, tag semantik HTML5, dan atribut ARIA yang valid.
* **Kegunaan / Kapan Dipakai:** Memastikan website dapat diakses dengan nyaman oleh semua orang, termasuk penyandang disabilitas dan lansia yang menggunakan *screen reader*.
* **Hasil Nyata:** Laporan verifikasi kontras DOM nyata dan navigasi ramah pembaca layar.

### `SKILL-22: frontend-performance`
* **Fungsi Utama:** Mengaudit dan mengoptimalkan metrik **Core Web Vitals**: Largest Contentful Paint (LCP < 2.5s), Interaction to Next Paint (INP < 200ms), dan Cumulative Layout Shift (CLS < 0.1).
* **Kegunaan / Kapan Dipakai:** Digunakan untuk mempercepat waktu muat halaman, optimasi ukuran bundle CSS/JS, dan lazy loading gambar.
* **Hasil Nyata:** Halaman web yang cepat dimuat dan tidak mengalami loncatan tampilan (*layout shift*).

### `SKILL-23: cross-browser-responsive-qa`
* **Fungsi Utama:** Menguji tata letak responsif dari layar ponsel terkecil (`320px`, `375px`), tablet (`768px`), hingga monitor desktop (`1440px`), serta memastikan **0px kebocoran horizontal (*horizontal overflow leak*)**.
* **Kegunaan / Kapan Dipakai:** Mencegah teks terpotong, elemen bertumpuk (*collision overlaps*), atau halaman yang bisa digeser ke kanan secara tidak wajar di HP.
* **Hasil Nyata:** Tata letak yang mulus di berbagai resolusi layar dengan pembuktian bounding box DOM.

---

## Kategori F: Database, Pemrosesan Data & Integrasi API (Skill 24–28)

### `SKILL-24: database-architecture-integrity`
* **Fungsi Utama:** Merancang skema database relasional yang kuat: kunci asing (*foreign keys*), integritas referensial (*ON DELETE RESTRICT/CASCADE*), transaksi ACID, dan migrasi skema yang dapat dibatalkan (*reversible migrations*).
* **Kegunaan / Kapan Dipakai:** Digunakan saat merancang tabel database baru agar data tidak rusak (*corrupt*) atau menjadi yatim (*orphan data*).
* **Hasil Nyata:** File migrasi bersih dengan metode `up()` dan `down()`.

### `SKILL-25: query-optimization-performance`
* **Fungsi Utama:** Menganalisis *execution plan* database (EXPLAIN), mendeteksi dan melenyapkan masalah kueri **N+1**, menambahkan indeks komposit yang tepat, dan mengoptimalkan paginasi data besar.
* **Kegunaan / Kapan Dipakai:** Digunakan saat aplikasi mulai lambat ketika menampilkan tabel berisi ribuan atau jutaan data.
* **Hasil Nyata:** Kueri database yang cepat dan efisien tanpa membebani RAM server.

### `SKILL-26: import-export-data-processing`
* **Fungsi Utama:** Merancang pipa pemrosesan impor/ekspor data (Excel, CSV, JSON) yang hemat memori menggunakan streaming/chunking, validasi baris per baris, dan pertahanan dari *Formula Injection* (CSV injection).
* **Kegunaan / Kapan Dipakai:** Digunakan pada fitur impor/ekspor data pegawai, laporan keuangan, atau data nakes tanpa risiko *Out of Memory (OOM)*.
* **Hasil Nyata:** Proses upload dan download file besar yang stabil dan aman dari serangan formula jahat.

### `SKILL-27: api-external-service-integration`
* **Fungsi Utama:** Mengintegrasikan API pihak ketiga dengan kontrak data ketat, batas waktu respons (*timeouts*), mekanisme coba lagi otomatis (*exponential backoff retries*), dan penanganan kegagalan (*circuit breaker*).
* **Kegunaan / Kapan Dipakai:** Digunakan saat menghubungi layanan luar seperti payment gateway, Google Sheets API, SatuSehat, atau layanan kirim pesan WhatsApp/Email.
* **Hasil Nyata:** Aplikasi tetap hidup dan tidak macet meskipun server API luar sedang lambat atau down.

### `SKILL-28: ai-provider-integration`
* **Fungsi Utama:** Mengintegrasikan SDK model kecerdasan buatan (Gemini API, OpenAI, Claude SDK) dengan isolasi kunci API di sisi server (*server-side key isolation*), validasi skema keluaran terstruktur (*structured output*), dan anggaran token (*token budgets*).
* **Kegunaan / Kapan Dipakai:** Digunakan pada aplikasi yang memiliki integrasi AI agar kunci API tidak bocor ke frontend dan biaya pemakaian token tetap terkendali.
* **Hasil Nyata:** Integrasi AI yang aman dengan validasi JSON yang ketat.

---

## Kategori G: Optimasi Performa, CI/CD, DevOps & SEO (Skill 29–36)

### `SKILL-29: performance-profiling-optimization`
* **Fungsi Utama:** Melakukan pemetaan kemacetan (*bottleneck profiling*) pada CPU, memori, I/O database, dan jaringan dengan membandingkan tolok ukur sebelum dan sesudah optimasi (*before/after benchmarks*).
* **Kegunaan / Kapan Dipakai:** Digunakan saat merespons laporan aplikasi lambat atau konsumsi server melonjak tinggi.
* **Hasil Nyata:** Pengurangan latensi terukur berbasis data nyata.

### `SKILL-30: caching-background-jobs`
* **Fungsi Utama:** Merancang strategi cache yang tepat (Redis, Memcached, File Cache) dengan aturan invalidasi yang jelas, serta mengelola antrean pekerjaan latar belakang (*background job queue*) yang idempoten.
* **Kegunaan / Kapan Dipakai:** Digunakan untuk tugas berat yang tidak boleh menahan respon pengguna (misal kirim email massal, proses laporan bulanan, atau kalkulasi angka besar).
* **Hasil Nyata:** Respon web instan karena proses berat dipindahkan ke worker latar belakang.

### `SKILL-31: ci-cd-release-engineering`
* **Fungsi Utama:** Mengonfigurasi dan mengamankan pipa otomatisasi CI/CD (GitHub Actions, GitLab CI) dengan gerbang kualitas otomatis (*quality gates*), pemindaian keamanan rahasia (*secret scanning*), dan alur rilis tanpa *downtime*.
* **Kegunaan / Kapan Dipakai:** Menjamin setiap kali ada commit atau Pull Request baru, seluruh tes dan linter dijalankan otomatis di server sebelum digabungkan ke cabang utama.
* **Hasil Nyata:** Berkas `.github/workflows/ci.yml` yang teruji dan siap rilis.

### `SKILL-32: environment-configuration-management`
* **Fungsi Utama:** Mengaudit keselarasan konfigurasi antar-lingkungan (*dev, staging, prod*), memvalidasi kelengkapan berkas `.env` terhadap `.env.example`, mengisolasi data rahasia (*secrets*), dan memastikan `APP_DEBUG=false` di lingkungan produksi.
* **Kegunaan / Kapan Dipakai:** Mencegah terjadinya kebocoran database credential atau error fatal saat aplikasi dipindahkan dari laptop developer ke server hosting.
* **Hasil Nyata:** Laporan verifikasi variabel `.env` yang lengkap dan aman.

### `SKILL-33: deployment-readiness`
* **Fungsi Utama:** Mengaudit kesiapan rilis produksi: kompilasi aset produksi (minified CSS/JS), verifikasi migrasi database, izin folder write, kesiapan cadangan (*backup*), dan prosedur pembatalan (*rollback runbook*).
* **Kegunaan / Kapan Dipakai:** Dijalankan tepat sebelum aplikasi dideploy ke server live.
* **Hasil Nyata:** Daftar periksa rilis (*pre-flight release checklist*) yang menjamin proses deployment berjalan mulus.

### `SKILL-34: observability-incident-diagnosis`
* **Fungsi Utama:** Memastikan aplikasi memiliki pencatatan log terstruktur (*structured logging*), pelacakan error (*error monitoring*), dan probe kesehatan sistem (`/health`, `/up`) untuk memudahkan penanganan insiden.
* **Kegunaan / Kapan Dipakai:** Memudahkan tim developer mendeteksi dan menyelesaikan error di server tanpa harus menebak-nebak.
* **Hasil Nyata:** Endpoint monitoring aktif dan format log yang mudah dipantau.

### `SKILL-35: backup-recovery-disaster-preparedness`
* **Fungsi Utama:** Merancang arsitektur pencadangan data berbasis prinsip 3-2-1, menguji prosedur pemulihan data (*restore testing*), serta menetapkan target RPO (*Recovery Point Objective*) dan RTO (*Recovery Time Objective*).
* **Kegunaan / Kapan Dipakai:** Menjamin bisnis tetap selamat jika sewaktu-waktu server hosting rusak, kebakaran, atau terkena ransomware.
* **Hasil Nyata:** Skrip backup otomatis dan panduan langkah pemulihan database (*disaster recovery plan*).

### `SKILL-36: seo-web-discoverability`
* **Fungsi Utama:** Mengaudit dan menerapkan standar SEO teknis: tag judul unik, deskripsi meta, URL kanonikal, berkas `robots.txt`, XML sitemap, Open Graph untuk pratinjau media sosial, serta metadata JSON-LD Schema.org.
* **Kegunaan / Kapan Dipakai:** Digunakan pada halaman publik agar website mudah ditemukan di mesin pencari Google dan tampil menarik saat link dibagikan di WhatsApp/Facebook.
* **Hasil Nyata:** Skor SEO tinggi dan pratinjau tautan media sosial yang rapi.

---

## Kategori H: Dokumentasi Pengembang & Gerbang Rilis Final (Skill 37–38)

### `SKILL-37: documentation-developer-handoff`
* **Fungsi Utama:** Mengaudit dan menulis dokumentasi serah-terima pengembang (*developer handoff*): panduan instalasi dari nol (*clean clone guide*), daftar akun default, dokumentasi API, dan petunjuk operasional.
* **Kegunaan / Kapan Dipakai:** Menjamin developer baru atau klien dapat menjalankan dan memelihara aplikasi tersebut dengan mudah tanpa harus bertanya berulang-ulang ke pembuat awal.
* **Hasil Nyata:** File `README.md` atau `PANDUAN-OPERATOR.md` yang lengkap dan dapat langsung dipraktikkan.

### `SKILL-38: final-quality-gate`
* **Fungsi Utama:** Menjalankan **15-Domain Final Quality Gate** yang mengonsolidasikan seluruh bukti pengujian dari `SKILL-01` hingga `SKILL-37` menjadi satu tabel keputusan resmi apakah aplikasi berstatus **`READY`** (siap rilis) atau **`BLOCKED`** (harus diperbaiki).
* **Kegunaan / Kapan Dipakai:** Sebagai gerbang penentu akhir sebelum aplikasi diserahkan kepada pengguna atau diluncurkan ke publik. Dilarang memberikan status `READY` jika masih ada pengujian yang gagal atau terlewat.
* **Hasil Nyata:** Tabel Keputusan Kualitas 15-Gerbang dengan bukti nomor baris kode dan hasil terminal nyata.

---

## 🚀 Ringkasan Cara Menggunakan di Proyek Mana Saja

Karena repositori ini sudah bersifat **Publik**, Anda cukup meng-clone repositori ini ke proyek mana pun yang ingin diaudit:

```bash
# 1. Masuk ke folder proyek Anda
cd /path/ke/proyek-anda

# 2. Clone repositori ini ke folder .agents/skills/ai-skills
git clone https://github.com/denitrisna7/reusable-ai-development-skills.git .agents/skills/ai-skills

# 3. Jalankan inisialisasi otomatis
python3 .agents/skills/ai-skills/scripts/setup-project.py .
```

Atau cukup berikan instruksi langsung ke AI di proyek target Anda:
> *"Tolong git clone `https://github.com/denitrisna7/reusable-ai-development-skills` ke proyek ini, lalu audit kode kita."*
