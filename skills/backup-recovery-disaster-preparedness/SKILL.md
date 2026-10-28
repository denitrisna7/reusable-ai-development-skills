---
name: backup-recovery-disaster-preparedness
description: Designs and audits backup architectures (3-2-1 rule, full and incremental/WAL backups), data retention policies, RPO/RTO targets, automated restore verification, encryption, and disaster recovery runbooks. Activate when planning data protection, backup automation, or disaster recovery. Do not use for routine git branching or code rollback.
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-35"
  category: "Performance, Operations, and Deployment"
---

# Backup, Recovery & Disaster Preparedness

This skill governs the design, verification, and operational hardening of data backup, point-in-time recovery (PITR), and disaster preparedness strategies. It enforces the core engineering axiom that **an untested backup is not a backup**: every backup system must couple automated encrypted snapshots with periodic restore verification, explicit Recovery Point Objective (RPO) and Recovery Time Objective (RTO) alignment, immutable access controls, and documented recovery ownership.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Designing or auditing database, object storage, or persistent volume backup schedules and scripts.
- Defining Recovery Point Objectives (RPO), Recovery Time Objectives (RTO), and data retention / lifecycle policies.
- Implementing Point-in-Time Recovery (PITR) using Write-Ahead Log (WAL) archiving or binary logs (`binlog`).
- Creating automated backup integrity checks, checksum verification, encryption-at-rest, and isolated restore drills.
- Authoring Disaster Recovery (DR) runbooks for data corruption, accidental deletion, ransomware, or regional cloud outages.

## 2. When Not to Use

Do not activate this skill when the task is strictly limited to:
- Rolling back stateless application container images or Git commits in CI/CD (route to `ci-cd-release-engineering`, `SKILL-31`).
- Designing application-level CSV/Excel user data export endpoints (route to `import-export-data-processing`, `SKILL-26`).
- Auditing GDPR user data deletion requests in application business logic without backup retention scope (route to `privacy-data-protection`, `SKILL-12`, though note how GDPR erasure interacts with backup retention windows).

## 3. Scope and Objectives

Every backup and disaster recovery strategy engineered or audited under this skill must cover:
- **Backup Strategy (3-2-1 Rule)**: Maintaining at least **3** copies of critical data across **2** distinct storage media/tiers with at least **1** copy stored off-site or in a separate cloud region/account.
- **Data Retention Policies**: Defining tiered retention schedules (e.g., continuous WAL/binlog for 7-35 days, daily snapshots for 30 days, weekly for 12 weeks, monthly for 1 year) aligned with regulatory and privacy laws.
- **Recovery Procedures**: Providing exact, copy-pasteable step-by-step commands to restore a full database, perform a Point-in-Time Recovery (PITR) to the second before an accidental `DROP`/`DELETE`, or recover object storage buckets.
- **Restore Testing**: Automating or scheduling regular restore drills into an isolated verification instance and running schema/row-count integrity queries.
- **RPO & RTO Alignment**: Explicitly mapping backup frequency and restore automation to the business's tolerable data loss window (RPO) and tolerable downtime window (RTO).
- **Disaster Recovery Planning**: Addressing multi-AZ/multi-region failover, DNS switching, infrastructure-as-code (IaC) reconstruction, and dependency order during cold starts.
- **Backup Integrity & Encryption**: Enforcing strong encryption in transit (TLS) and at rest (`AES-256` / KMS), generating cryptographic checksums (`SHA-256`), and alerting on zero-byte or failed backup runs.
- **Access Protection (Ransomware & Blast-Radius Defense)**: Isolating backup storage credentials from production application credentials and enabling Object Lock / WORM (Write-Once-Read-Many) immutability so compromised application servers cannot delete or encrypt their own backups.
- **Documented Recovery Ownership**: Defining clear operational roles (who is paged on backup failure, who authorizes production DB restore, and who signs off on quarterly restore drills).

## 4. Prerequisites and Context Requirements

Before designing or auditing backup and recovery systems, identify:
1. **Stateful Stores Inventory**: List every stateful component (primary relational DB, document store, Redis persistence if stateful, user-uploaded S3/GCS/local media files, secret vaults, and configuration state).
2. **Data Volume & Change Rate**: Determine database size and daily write volume to choose between logical dumps (`pg_dump`, `mysqldump`) and physical snapshots + continuous WAL/binlog streaming.
3. **Business RPO / RTO Requirements**: Clarify whether the system is a hobby/internal tool (e.g., RPO `24h`, RTO `4h`) or a mission-critical transactional platform (e.g., RPO `< 5 min` via PITR, RTO `< 30 min`).

## 5. Step-by-Step Workflow

### Step 1: Inventory All Stateful Assets and Classify RPO/RTO
- [ ] Map every persistent data store in the architecture and verify none are overlooked:
  - Primary relational and document databases (PostgreSQL, MySQL, MongoDB, SQLite).
  - Object storage buckets and local persistent volumes containing user-uploaded media, invoices, or exports.
  - Stateful search indices or key-value stores if they hold non-recomputable state.
  - Infrastructure state files (`terraform.tfstate`), TLS certificates, and secret vault configurations.
- [ ] Record target **RPO** (maximum acceptable age of lost data) and **RTO** (maximum acceptable time to restore service) for each asset.
- [ ] Verify that backup schedules run more frequently than the RPO target (for example, continuous WAL archiving for `RPO <= 5 minutes`, or hourly snapshots for `RPO <= 1 hour`).

### Step 2: Engineer Transactionally Consistent, Encrypted Backups
- [ ] **Relational Databases**:
  - PostgreSQL: Use `pg_dump --format=custom` (which runs in a repeatable-read snapshot transaction) for logical backups, or managed RDS/Cloud SQL automated snapshots + continuous WAL archiving (`pgBackRest` / `wal-g`) for PITR.
  - MySQL / MariaDB: Always use `mysqldump --single-transaction --routines --triggers --events` on InnoDB tables so backups are point-in-time consistent without locking tables, paired with `binlog` archiving for PITR.
  - SQLite: Never copy a live `.sqlite` file with raw `cp` while writes may occur; use `sqlite3 db.sqlite ".backup 'backup.sqlite'"` or `VACUUM INTO` or `Litestream` continuous replication.
- [ ] **File & Object Storage**:
  - Enable bucket versioning and cross-region/off-site replication on S3/GCS/R2 buckets storing user uploads or documents.
- [ ] **Encryption & Integrity Verification**:
  - Encrypt backup archives before or during upload (`AES-256-GCM` / GPG / KMS envelope encryption).
  - Verify exit codes (`set -euo pipefail` in backup scripts), validate non-zero archive size, and record a `SHA-256` checksum manifest alongside each backup artifact.

### Step 3: Enforce Blast-Radius Isolation and Retention Lifecycle
- [ ] **Pull vs. Push / Write-Only Isolation**: Ensure the production application's IAM role or server credentials can at most *append* new backups to a staging bucket, or better yet, have a dedicated backup account *pull* snapshots and store them in an immutable vault with Object Lock (Compliance/Governance mode) enabled.
- [ ] **Automated Retention Pruning**: Configure lifecycle policies to expire old backups only after the retention window elapses and only when at least $N$ recent successful backups exist (never prune the last good backup if recent backups have been failing!).

### Step 4: Implement Automated Restore Testing & Alerting
- [ ] Create an automated or scripted restore verification workflow:
  1. Fetch the latest encrypted backup artifact from off-site storage.
  2. Decrypt and restore it into an isolated, ephemeral database container or staging instance.
  3. Execute sanity queries (verify migration table version, table count, non-zero row counts on core tables, and foreign key integrity).
  4. Tear down the temporary instance and emit a verification metric/log.
- [ ] Configure dead-man's-switch alerting (alert fires if no successful backup heartbeat is recorded within the expected schedule window).

### Step 5: Document the Disaster Recovery Runbook
- [ ] Write a clear, high-stress-friendly DR Runbook containing:
  - Designated Recovery Owner, backup operator, and escalation contacts.
  - Severity classification criteria for triggering a full DB restore vs. targeted table recovery vs. standby failover.
  - Pre-restore safety checklist (putting the app in maintenance mode, stopping cron schedulers and queue workers so new writes do not conflict with the restore, and taking a final forensic snapshot of the damaged state before overwriting).
  - Exact copy-pasteable CLI commands for full restore and Point-in-Time Recovery (PITR) to a specific UTC timestamp (`--recovery-target-time`).
  - Post-restore verification checklist (schema version check, row-count sanity checks, sequences/auto-increment reset check, and flushing Redis/application caches that may hold stale keys pointing to post-snapshot IDs).
  - Criteria for exiting maintenance mode and resuming normal traffic.

## 6. Technology-Specific Adaptation Rules

Adapt backup, restore, and disaster preparedness workflows to the project's actual data stores and stack. Never force PHPStan, Pint, Pest, shadcn/ui, or Playwright where inapplicable:
- **PHP (Laravel / Symfony / CodeIgniter)**: When using `spatie/laravel-backup`, configure encrypted zip passwords (`BACKUP_ARCHIVE_PASSWORD`), remote off-site disks (S3/R2/GCS), health checks (`MaximumAgeInDays`, `MinimumStorageInMegabytes`), and exclude transient directories (`storage/framework/cache`, `node_modules`, `vendor`). Schedule `backup:clean`, `backup:run`, and `backup:monitor` with `->onOneServer()`.
- **JavaScript / TypeScript (Node.js / Next.js / Prisma / Drizzle)**: Pair managed PostgreSQL/MySQL PITR snapshots with automated logical dump verification scripts; never rely on ORM seed files as a substitute for production data backups.
- **Python (Django / FastAPI / SQLAlchemy)**: Use `django-dbbackup` (with GPG encryption) or native `pg_dump` / `pgBackRest` / `wal-g` cron jobs, and ensure media storage (`MEDIA_ROOT` / S3 bucket) is backed up alongside the relational database.
- **Go / Rust / Java (Spring Boot) / C# (.NET)**: Integrate infrastructure-level snapshots (Terraform/OpenTofu AWS RDS / GCP Cloud SQL backup policies, S3 versioning + Object Lock) with application maintenance-mode gates and post-restore migration verification (`golang-migrate`, `sqlx`, `Flyway`, `EF Core`).
- **PostgreSQL / MySQL / SQLite Engines**:
  - PostgreSQL: `pg_dump --format=custom --no-owner --no-acl` + `pg_restore --clean --if-exists --no-owner` for logical backups; `pgBackRest` or cloud PITR for physical/WAL recovery.
  - MySQL / MariaDB: `mysqldump --single-transaction --quick --routines --triggers --events` + binary log (`mysqlbinlog`) replay for PITR.
  - SQLite: `sqlite3 app.db ".backup 'backup.db'"` or `Litestream` continuous S3 replication for single-node production SQLite deployments.
- **Mobile / Flutter**: Implement encrypted local database backups (`sqflite` / `Drift` export encrypted via `FlutterSecureStorage` key) or cloud user-state synchronization so device loss does not permanently destroy user data.
- **Unknown or Mixed Stacks**: Apply the universal 3-2-1 backup rule, atomic snapshot flags, `SHA-256` checksum manifests, off-site encrypted storage, and automated ephemeral restore drills.

## 7. Security and Safety Considerations

- **Never Store Backup Decryption Keys Inside the Same Backup Bucket**: Store encryption keys in a separate KMS or secret manager so an attacker who compromises bucket read access cannot decrypt the archives.
- **Sanitize Production Backups Before Loading into Local/Dev Environments**: Never allow developers to download raw production database backups containing real customer PII, passwords, or payment tokens onto unencrypted laptops. Provide an anonymization/scrubbing pipeline for staging/dev seeding.
- **Guard Restore Commands Against Target Confusion**: Require explicit confirmation of target hostname/database name in restore scripts so an operator never accidentally overwrites the live production database when intending to restore into a staging instance.
- **Immutability Against Ransomware**: Configure S3 Object Lock (Governance or Compliance mode) or write-only backup roles so that even if a production server's root credentials are compromised, the attacker cannot purge historical backups.

## 8. Verification Criteria

Before marking backup and disaster preparedness work complete, verify:
1. **Transactional Consistency**: Database dump commands use non-locking consistent snapshot flags (`--single-transaction`, `--format=custom`, or `.backup`).
2. **Restore Path Proven**: Every backup command or script is paired with its exact inverse restore command and integrity verification step.
3. **Failure Visibility**: Backup scripts fail loudly (`set -euo pipefail`, non-zero exit code, dead-man's-switch monitor) rather than silently uploading a 0-byte `.sql.gz` file when `pg_dump` fails in a pipe.
4. **3-2-1 & Encryption Verified**: Backups are encrypted at rest and replicated off-site outside the primary compute failure domain.

## 9. Failure Handling and Edge Cases

- **Pipe Masking Failures (`pg_dump ... | gzip > backup.sql.gz`)**: Without `set -o pipefail`, if `pg_dump` fails with an authentication error, `gzip` succeeds on empty input and exits `0`, creating a corrupt empty backup and reporting success. Always enforce `set -euo pipefail` and verify uncompressed/compressed size thresholds.
- **Cache Desynchronization After Database Restore**: After rolling a database back 15 minutes via PITR, Redis or CDN caches may still hold data from those lost 15 minutes. Always flush or namespace-bump application caches as part of the database recovery runbook.
- **External Side Effects During Replay**: When restoring a database to an earlier point in time, ensure pending queued jobs inside database-backed queue tables do not re-trigger duplicate emails or duplicate webhook charges for events that already completed before the crash.

## 10. Expected Outputs and Reporting Requirements

Always provide a structured **Backup, Recovery & Disaster Preparedness Report**:

```markdown
# Backup, Recovery & Disaster Preparedness Report

## 1. Stateful Assets & RPO/RTO Matrix
| Stateful Asset | Backup Method & Frequency | Off-Site Storage & Encryption | Target RPO | Target RTO | Retention Policy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `<Primary PostgreSQL DB>` | `<Daily snapshot + continuous WAL>` | `<S3 off-region, KMS AES-256, Object Lock>` | `<5 mins>` | `<30 mins>` | `<30d daily, 12m monthly>` |
| `<User Uploads Bucket>` | `<S3 Versioning + Cross-Region Repl>` | `<Secondary Region S3>` | `<15 mins>` | `<15 mins>` | `<90d non-current versions>` |

## 2. Restore Verification & Access Controls
- **Credential Isolation & Immutability**: `<Separate IAM role; WORM Object Lock status>`
- **Restore Testing Cadence & Evidence**: `<Automated weekly restore test into ephemeral container>`
- **Dead-Man's-Switch Alerting**: `<Alert trigger if backup heartbeat > 26h old>`

## 3. Disaster Recovery Runbook Summary
- **Recovery Owner**: `<Role / Escalation Path>`
- **Exact Restore Commands**: `<Step-by-step commands including maintenance mode and cache flush>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Aligns with `database-architecture-integrity` (`SKILL-24`) for schema and storage layout, and `privacy-data-protection` (`SKILL-12`) for data retention and encryption compliance.
- **Downstream Skills**: Supplies mandatory pre-release backup and rollback readiness evidence to `deployment-readiness` (`SKILL-33`) and `final-quality-gate` (`SKILL-38`), and operational runbooks to `documentation-developer-handoff` (`SKILL-37`).

## 12. Source References

- **NIST SP 800-34 Rev. 1 (Contingency Planning Guide for Federal Information Systems)**: https://csrc.nist.gov/pubs/sp/800/34/r1/final
- **AWS Well-Architected Framework (Reliability Pillar: Plan for Disaster Recovery)**: https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/plan-for-disaster-recovery-dr.html
- **Shared Deployment Readiness & Quality Gate Matrix**: [../../references/deployment-readiness-quality-gate-matrix.md](../../references/deployment-readiness-quality-gate-matrix.md)
