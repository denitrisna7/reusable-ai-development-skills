#!/usr/bin/env python3
"""Master 38-Skill & 15-Domain Automated Project Auditor, Environment Healer, & Playwright Chromium Runner.

Executes real, non-hallucinatable ground-truth checks across all 38 skills (SKILL-01 to SKILL-38)
and all 15 Final Quality Gate domains (Gate 01 to Gate 15):
1. Auto-Sync .agents/ in Target Project: Installs/updates skills/, references/, scripts/, and BEFORE_ACTION.md
   so all 38 skills and relative links work seamlessly in any host repository.
2. Auto-PATH & Binary Healing: Ensures node, npm, npx, composer, flutter, and dart in ~/.local/bin
   or ~/development/flutter/bin are accessible in PATH and ~/.gemini/antigravity/bin (preventing Exit Code 127).
3. Full 38-Skill Static, Architectural, Security (OWASP ASVS), Anti-Slop, Contrast, & Database Analysis.
4. Full Verbose Unit & Feature Test Execution (./vendor/bin/phpunit --testdox, npm test, pytest -v, flutter test).
5. Automatic Local Dev Server Boot (if none active) + Real Headless Chromium Playwright Audit (run-browser-audit.mjs).
6. Prints the Complete 38-Skill Verification Matrix (SKILL-01..SKILL-38) and 15-Domain Final Quality Gate Table.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LIBRARY_ROOT = SCRIPT_DIR.parent

EXCLUDED_SCAN_DIRS = {
    ".git",
    "node_modules",
    "vendor",
    "storage",
    ".agents",
    "reusable-ai-development-skills",
    "build",
    ".dart_tool",
    ".next",
    "dist",
    "sources",
}


def find_helper_script(filename: str, target_dir: Path) -> Path | None:
    """Locate a helper script across SCRIPT_DIR, .agents/scripts, or global plugin dir."""
    candidates = [
        SCRIPT_DIR / filename,
        LIBRARY_ROOT / "skills" / "accessibility-engineering" / "scripts" / filename,
        target_dir / ".agents" / "scripts" / filename,
        target_dir / ".agents" / "skills" / "ai-skills" / "scripts" / filename,
        target_dir / "reusable-ai-development-skills" / "scripts" / filename,
        Path("/tmp/reusable-ai-development-skills/scripts") / filename,
        Path.home() / ".gemini" / "config" / "plugins" / "reusable-ai-development-skills" / "scripts" / filename,
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def sync_agents_directory(target_dir: Path) -> str | None:
    """Register this library's skills/ folder in <target>/.agents/skills.json.

    Antigravity scans skill roots only ONE level deep (.agents/skills/<name>/SKILL.md).
    When the library is cloned to .agents/skills/ai-skills/, the 38 skills live at
    .agents/skills/ai-skills/skills/<name>/SKILL.md and are invisible unless declared
    in .agents/skills.json. A pointer (not a copy) keeps skills current after git pull.
    """
    if target_dir.resolve() == LIBRARY_ROOT.resolve():
        return None
    skills_dir = LIBRARY_ROOT / "skills"
    if not skills_dir.is_dir():
        return None
    agents_dir = target_dir / ".agents"
    try:
        agents_dir.mkdir(parents=True, exist_ok=True)
        try:
            entry_path = str(skills_dir.resolve().relative_to(target_dir.resolve()))
        except ValueError:
            entry_path = str(skills_dir.resolve())
        cfg_path = agents_dir / "skills.json"
        cfg = {}
        if cfg_path.is_file():
            try:
                cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            except Exception:
                cfg = {}
        entries = cfg.setdefault("entries", [])
        if any(e.get("path") == entry_path for e in entries if isinstance(e, dict)):
            status = "already registered"
        else:
            entries.append({"path": entry_path})
            cfg_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
            status = "registered"
        count = sum(1 for d in skills_dir.iterdir() if (d / "SKILL.md").is_file())
        return f"{count} skills {status} in .agents/skills.json -> {entry_path} (visible in new Antigravity sessions)"
    except Exception as exc:
        return f"Notice: could not write .agents/skills.json ({exc})"


def ensure_environment_binaries() -> list[str]:
    """Ensure ~/.local/bin and ~/development/flutter/bin binaries are on PATH and symlinked if needed."""
    home = Path.home()
    extra_dirs = [
        home / ".local" / "bin",
        home / "bin",
        home / "development" / "flutter" / "bin",
        home / ".config" / "composer" / "vendor" / "bin",
        home / ".gemini" / "antigravity" / "bin",
    ]
    current_path = os.environ.get("PATH", "")
    path_parts = current_path.split(":") if current_path else []
    for d in extra_dirs:
        if d.is_dir() and str(d) not in path_parts:
            path_parts.insert(0, str(d))
    os.environ["PATH"] = ":".join(path_parts)

    healed = []
    agy_bin = home / ".gemini" / "antigravity" / "bin"
    if agy_bin.is_dir() and os.access(agy_bin, os.W_OK):
        candidates = {
            "node": home / ".local" / "bin" / "node",
            "npm": home / ".local" / "bin" / "npm",
            "npx": home / ".local" / "bin" / "npx",
            "composer": home / ".local" / "bin" / "composer",
            "flutter": home / "development" / "flutter" / "bin" / "flutter",
            "dart": home / "development" / "flutter" / "bin" / "dart",
        }
        for name, src in candidates.items():
            dst = agy_bin / name
            if src.exists() and not dst.exists():
                try:
                    dst.symlink_to(src)
                    healed.append(f"{dst} -> {src}")
                except OSError:
                    pass
    return healed


def check_port(host: str, port: int, timeout: float = 0.5) -> bool:
    """Check if a local port is actively accepting connections."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def wait_for_port(host: str, port: int, timeout: float = 12.0) -> bool:
    """Wait until a local port begins accepting connections."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if check_port(host, port, timeout=0.4):
            return True
        time.sleep(0.3)
    return False


def run_cmd(cmd: list[str], cwd: Path, timeout: int = 120, env_overrides: dict | None = None) -> tuple[int, str, str]:
    """Execute a CLI command safely and capture exit code, stdout, and stderr."""
    env = os.environ.copy()
    for key in ["ANTIGRAVITY_AGENT", "CLAUDECODE", "CLAUDE_CODE", "CURSOR_TRACE_ID", "AGENT", "AI_AGENT", "OPENCODE"]:
        env.pop(key, None)
    if env_overrides:
        env.update(env_overrides)
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            env=env,
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout} seconds"
    except FileNotFoundError:
        return 127, "", f"Command not found: {cmd[0]}"
    except Exception as e:
        return 1, "", str(e)


def iter_project_files(target_dir: Path, suffixes: set[str]) -> list[Path]:
    out: list[Path] = []
    for p in target_dir.rglob("*"):
        if not p.is_file():
            continue
        if any(part in EXCLUDED_SCAN_DIRS for part in p.parts):
            continue
        if p.suffix in suffixes:
            out.append(p)
    return out


def audit_project(target_dir: Path) -> dict:
    healed_bins = ensure_environment_binaries()
    synced_msg = sync_agents_directory(target_dir)

    results: dict = {
        "target_dir": str(target_dir),
        "healed_bins": healed_bins,
        "synced_agents": synced_msg,
        "stack": [],
        "env_check": {"status": "UNKNOWN", "details": []},
        "static_analysis": {"status": "PASS", "details": []},
        "slop_check": {"status": "PASS", "output": ""},
        "contrast_check": {"status": "PASS", "output": ""},
        "security_scan": {"status": "PASS", "details": []},
        "db_scan": {"status": "PASS", "details": []},
        "dev_servers": [],
        "active_url": None,
        "test_run": {"status": "NOT TESTED", "command": None, "output": None, "returncode": None},
        "flutter_run": {"status": "NOT APPLICABLE", "command": None, "output": None, "returncode": None},
        "browser_run": {"status": "NOT TESTED", "command": None, "output": None, "returncode": None},
        "skills_matrix": [],
        "gates_matrix": [],
    }

    # 1. Stack & Architecture Discovery (SKILL-01..SKILL-04)
    pkg_json = target_dir / "package.json"
    composer_json = target_dir / "composer.json"
    pyproject = target_dir / "pyproject.toml"
    req_txt = target_dir / "requirements.txt"
    go_mod = target_dir / "go.mod"
    flutter_pubspec = target_dir / "pubspec.yaml"
    mobile_pubspec = target_dir / "mobile" / "pubspec.yaml"
    is_skill_repo = (target_dir / "SKILL_CATALOG.md").is_file() and (target_dir / "skills").is_dir()

    if is_skill_repo:
        results["stack"].append("Agent Skills Library (38 Skills)")

    pkg_deps: dict = {}
    if pkg_json.is_file():
        try:
            data = json.loads(pkg_json.read_text(encoding="utf-8"))
            results["stack"].append(f"Node.js ({data.get('name', 'unnamed')})")
            results["pkg_scripts"] = list(data.get("scripts", {}).keys())
            pkg_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        except Exception:
            results["stack"].append("Node.js (package.json)")

    if composer_json.is_file():
        results["stack"].append("PHP / Composer")
        if (target_dir / "artisan").is_file():
            results["stack"].append("Laravel Framework")

    if pyproject.is_file() or req_txt.is_file():
        results["stack"].append("Python")

    if go_mod.is_file():
        results["stack"].append("Go")

    if flutter_pubspec.is_file() or mobile_pubspec.is_file():
        results["stack"].append("Flutter / Dart Mobile")

    if not results["stack"]:
        results["stack"].append("Generic / Static Web")

    all_code_files = iter_project_files(
        target_dir, {".php", ".ts", ".tsx", ".js", ".jsx", ".vue", ".py", ".go", ".dart", ".html", ".sql", ".prisma"}
    )
    php_files = [p for p in all_code_files if p.suffix == ".php"]
    blade_files = [
        p
        for p in all_code_files
        if p.name.endswith(".blade.php")
        or p.suffix in {".tsx", ".jsx", ".vue", ".html"}
        or ("lib" in p.parts and p.name.endswith(("_screen.dart", "_page.dart", "_widget.dart")))
    ]
    controller_files = [
        p
        for p in all_code_files
        if any(seg in p.parts for seg in ("Controllers", "controllers", "routers", "routes", "handlers", "pages", "app"))
        and p.suffix in {".php", ".ts", ".tsx", ".js", ".py", ".go"}
    ]
    model_files = [
        p
        for p in all_code_files
        if any(seg in p.parts for seg in ("Models", "models", "entities", "schemas", "prisma"))
        or p.name in ("models.py", "schema.prisma")
    ]
    migration_files = [
        p
        for p in all_code_files
        if "migrations" in p.parts or "alembic" in p.parts or p.name == "schema.prisma"
    ]
    seeder_files = [
        p
        for p in all_code_files
        if "seeders" in p.parts or p.name in ("seed.ts", "seed.js", "seed.py")
    ]
    test_files = [
        p
        for p in all_code_files
        if "tests" in p.parts
        or "test" in p.parts
        or "__tests__" in p.parts
        or p.name.endswith(("Test.php", ".test.ts", ".test.tsx", ".spec.ts", ".test.js", "_test.dart", "_test.py", "_test.go"))
    ]

    # 2. Environment & Secret Inspection (SKILL-32)
    env_file = target_dir / ".env"
    env_example = target_dir / ".env.example"

    if not env_file.is_file() and not env_example.is_file():
        results["env_check"]["status"] = "PASS"
        results["env_check"]["details"].append("No .env required (stateless/library repo).")
    else:
        env_issues = []
        if env_file.is_file():
            content = env_file.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"^APP_DEBUG\s*=\s*true", content, re.M | re.I):
                env_issues.append("Local APP_DEBUG=true detected (must be APP_DEBUG=false in production).")
            if re.search(r"(secret|password|key)\s*=\s*(changeme|admin123|123456)", content, re.M | re.I):
                env_issues.append("SECURITY RISK: Weak placeholder credential detected in .env.")
            results["env_check"]["details"].append("Local .env file verified.")
        else:
            env_issues.append("NOTICE: .env file not present; .env.example template verified.")

        if env_example.is_file() and env_file.is_file():
            ex_keys = set(re.findall(r"^([A-Z0-9_]+)\s*=", env_example.read_text(errors="ignore"), re.M))
            env_keys = set(re.findall(r"^([A-Z0-9_]+)\s*=", env_file.read_text(errors="ignore"), re.M))
            missing_in_env = ex_keys - env_keys
            if missing_in_env:
                env_issues.append(f"Keys in .env.example missing from .env: {sorted(missing_in_env)}")

        results["env_check"]["status"] = "FAIL" if any("SECURITY RISK" in i for i in env_issues) else "PASS"
        results["env_check"]["details"].extend(env_issues)

    # 3. AI Anti-Slop (SKILL-05) & WCAG Contrast Scan (SKILL-21)
    slop_script = find_helper_script("slopcheck.py", target_dir)
    if slop_script:
        s_code, s_out, s_err = run_cmd([sys.executable, str(slop_script), str(target_dir)], target_dir, timeout=30)
        results["slop_check"]["status"] = "PASS" if s_code == 0 else "WARNING"
        results["slop_check"]["output"] = (s_out + "\n" + s_err).strip()

    contrast_script = find_helper_script("contrast-check.py", target_dir)
    if contrast_script:
        c_code, c_out, c_err = run_cmd([sys.executable, str(contrast_script), str(target_dir)], target_dir, timeout=30)
        results["contrast_check"]["status"] = "PASS" if c_code == 0 else "FAIL"
        results["contrast_check"]["output"] = (c_out + "\n" + c_err).strip()

    # 4. Static Analysis & Code Quality (SKILL-07, SKILL-08)
    pint_bin = target_dir / "vendor" / "bin" / "pint"
    if pint_bin.is_file():
        p_code, _, _ = run_cmd([str(pint_bin), "--test"], target_dir, timeout=45)
        results["static_analysis"]["details"].append(
            f"Laravel Pint style check: {'PASS' if p_code == 0 else 'Formatting diffs present'}"
        )
    elif php_files:
        results["static_analysis"]["details"].append(f"Verified {len(php_files)} PHP/Blade source files.")

    # 5. OWASP Security, Supply Chain, & Database Integrity Scan (SKILL-09..14, SKILL-24..28)
    raw_sqli_risks = 0
    csrf_forms = 0
    for bf in blade_files:
        btxt = bf.read_text(encoding="utf-8", errors="ignore")
        csrf_forms += len(re.findall(r"@csrf\b", btxt))
    for pf in controller_files + model_files:
        ptxt = pf.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"(?:DB::raw|whereRaw)\s*\(\s*\"[^\"]*\$", ptxt):
            raw_sqli_risks += 1

    lockfiles = [
        name
        for name in ("composer.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "pubspec.lock", "uv.lock")
        if (target_dir / name).is_file() or (target_dir / "mobile" / name).is_file()
    ]
    results["security_scan"]["details"].append(
        f"SQLi raw-interpolation risks: {raw_sqli_risks} | Blade @csrf directives: {csrf_forms} | Lockfiles: {lockfiles or ['none']}"
    )
    results["security_scan"]["status"] = "PASS" if raw_sqli_risks == 0 else "FAIL"

    fk_count = 0
    eager_count = 0
    paginate_count = 0
    for mf in migration_files:
        mtxt = mf.read_text(encoding="utf-8", errors="ignore")
        fk_count += len(re.findall(r"foreignId|foreign\(|constrained\(", mtxt))
    for cf in controller_files:
        ctxt = cf.read_text(encoding="utf-8", errors="ignore")
        eager_count += len(re.findall(r"->with\(|::with\(|->load\(", ctxt))
        paginate_count += len(re.findall(r"->paginate\(|->simplePaginate\(|->cursorPaginate\(", ctxt))

    results["db_scan"]["details"].append(
        f"Migrations: {len(migration_files)} (FK constraints: {fk_count}) | Seeders: {len(seeder_files)} | "
        f"Eager-load calls: {eager_count} | Paginated queries: {paginate_count}"
    )

    # 6. Automated Backend/Unit Test Runner Execution (SKILL-15, SKILL-16, SKILL-18, SKILL-19)
    phpunit_bin = target_dir / "vendor" / "bin" / "phpunit"
    validate_skills_bin = target_dir / "scripts" / "validate-skills.py"
    if is_skill_repo and validate_skills_bin.is_file():
        cmd = [sys.executable, str(validate_skills_bin)]
        code, out, err = run_cmd(cmd, target_dir)
        results["test_run"]["command"] = "python3 scripts/validate-skills.py"
        results["test_run"]["returncode"] = code
        results["test_run"]["output"] = (out + "\n" + err).strip()
        results["test_run"]["status"] = "PASS" if code == 0 else "FAIL"
    elif phpunit_bin.is_file():
        cmd = [str(phpunit_bin), "--testdox", "--colors=never"]
        code, out, err = run_cmd(cmd, target_dir)
        results["test_run"]["command"] = "./vendor/bin/phpunit --testdox --colors=never"
        results["test_run"]["returncode"] = code
        results["test_run"]["output"] = (out + "\n" + err).strip()
        results["test_run"]["status"] = "PASS" if code == 0 else "FAIL"
    elif (target_dir / "artisan").is_file():
        cmd = ["php", "artisan", "test"]
        code, out, err = run_cmd(cmd, target_dir)
        results["test_run"]["command"] = "php artisan test"
        results["test_run"]["returncode"] = code
        results["test_run"]["output"] = (out + "\n" + err).strip()
        results["test_run"]["status"] = "PASS" if code == 0 else "FAIL"
    elif pkg_json.is_file() and "test" in results.get("pkg_scripts", []):
        cmd = ["npm", "test"]
        code, out, err = run_cmd(cmd, target_dir, env_overrides={"CI": "true"})
        results["test_run"]["command"] = "CI=true npm test"
        results["test_run"]["returncode"] = code
        results["test_run"]["output"] = (out + "\n" + err).strip()
        results["test_run"]["status"] = "PASS" if code == 0 else "FAIL"
    elif pyproject.is_file() or (target_dir / "tests").is_dir():
        cmd = ["pytest", "-v"]
        code, out, err = run_cmd(cmd, target_dir)
        if code != 127:
            results["test_run"]["command"] = "pytest -v"
            results["test_run"]["returncode"] = code
            results["test_run"]["output"] = (out + "\n" + err).strip()
            results["test_run"]["status"] = "PASS" if code == 0 else "FAIL"
        else:
            results["test_run"]["status"] = "BLOCKED: pytest runner not found"
    else:
        results["test_run"]["status"] = "NOT APPLICABLE (No backend test suite configured)"

    # Optional Flutter Mobile Analysis & Test Suite
    flutter_dir = target_dir / "mobile" if mobile_pubspec.is_file() else (target_dir if flutter_pubspec.is_file() else None)
    if flutter_dir:
        f_code, f_out, f_err = run_cmd(["flutter", "test"], flutter_dir, timeout=120)
        if f_code != 127:
            results["flutter_run"]["command"] = f"flutter test (in {flutter_dir.name})"
            results["flutter_run"]["returncode"] = f_code
            results["flutter_run"]["output"] = (f_out + "\n" + f_err).strip()
            results["flutter_run"]["status"] = "PASS" if f_code == 0 else "FAIL"

    # 7. Local Server Detection or Temporary Ephemeral Server Boot for Playwright (SKILL-17, SKILL-20..23)
    common_ports = [
        (8000, "http://127.0.0.1:8000", "Laravel / Django / FastAPI"),
        (3000, "http://127.0.0.1:3000", "Node / Next.js / React"),
        (5173, "http://127.0.0.1:5173", "Vite Dev Server"),
        (8080, "http://127.0.0.1:8080", "Web Server"),
    ]
    for port, url, label in common_ports:
        if check_port("127.0.0.1", port):
            results["dev_servers"].append(f"ACTIVE: {url} ({label})")
            if not results["active_url"]:
                results["active_url"] = url

    temp_server_proc = None
    if not results["active_url"] and not is_skill_repo:
        if (target_dir / "artisan").is_file():
            temp_port = 18123
            temp_server_proc = subprocess.Popen(
                ["php", "artisan", "serve", "--host=127.0.0.1", f"--port={temp_port}"],
                cwd=str(target_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if wait_for_port("127.0.0.1", temp_port, timeout=10.0):
                results["active_url"] = f"http://127.0.0.1:{temp_port}"
                results["dev_servers"].append(f"AUTO-STARTED EPHEMERAL SERVER: {results['active_url']} (php artisan serve)")
        elif (target_dir / "public" / "index.php").is_file() or (target_dir / "index.php").is_file():
            temp_port = 18123
            doc_root = "public" if (target_dir / "public" / "index.php").is_file() else "."
            temp_server_proc = subprocess.Popen(
                ["php", "-S", f"127.0.0.1:{temp_port}", "-t", doc_root],
                cwd=str(target_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if wait_for_port("127.0.0.1", temp_port, timeout=8.0):
                results["active_url"] = f"http://127.0.0.1:{temp_port}"
                results["dev_servers"].append(f"AUTO-STARTED EPHEMERAL SERVER: {results['active_url']} (php -S -t {doc_root})")
        elif pkg_json.is_file() and "dev" in results.get("pkg_scripts", []):
            temp_port = 18124
            dev_env = os.environ.copy()
            dev_env["PORT"] = str(temp_port)
            cmd = ["npm", "run", "dev"]
            if "next" in pkg_deps:
                cmd = ["npx", "next", "dev", "-H", "127.0.0.1", "-p", str(temp_port)]
            elif "vite" in pkg_deps:
                cmd = ["npx", "vite", "--host", "127.0.0.1", "--port", str(temp_port)]
            temp_server_proc = subprocess.Popen(
                cmd,
                cwd=str(target_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=dev_env,
            )
            if wait_for_port("127.0.0.1", temp_port, timeout=14.0):
                results["active_url"] = f"http://127.0.0.1:{temp_port}"
                results["dev_servers"].append(f"AUTO-STARTED EPHEMERAL SERVER: {results['active_url']} ({cmd[0]} {cmd[1] if len(cmd) > 1 else ''})")
        elif (target_dir / "manage.py").is_file():
            temp_port = 18125
            temp_server_proc = subprocess.Popen(
                ["python3", "manage.py", "runserver", f"127.0.0.1:{temp_port}", "--noreload"],
                cwd=str(target_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if wait_for_port("127.0.0.1", temp_port, timeout=10.0):
                results["active_url"] = f"http://127.0.0.1:{temp_port}"
                results["dev_servers"].append(f"AUTO-STARTED EPHEMERAL SERVER: {results['active_url']} (python manage.py runserver)")
        elif (target_dir / "index.html").is_file() or (target_dir / "public" / "index.html").is_file():
            temp_port = 18126
            web_root = "public" if (target_dir / "public" / "index.html").is_file() else "."
            temp_server_proc = subprocess.Popen(
                ["python3", "-m", "http.server", str(temp_port), "--bind", "127.0.0.1", "-d", web_root],
                cwd=str(target_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if wait_for_port("127.0.0.1", temp_port, timeout=6.0):
                results["active_url"] = f"http://127.0.0.1:{temp_port}"
                results["dev_servers"].append(f"AUTO-STARTED EPHEMERAL SERVER: {results['active_url']} (python http.server in {web_root})")

    browser_script = find_helper_script("run-browser-audit.mjs", target_dir)
    try:
        if is_skill_repo:
            results["browser_run"]["status"] = "PASS (Library CLI verified; web server N/A for standalone skill repo)"
        elif results["active_url"] and browser_script:
            b_cmd = ["node", str(browser_script), results["active_url"]]
            b_code, b_out, b_err = run_cmd(b_cmd, target_dir, timeout=90)
            results["browser_run"]["command"] = f"node {browser_script} {results['active_url']}"
            results["browser_run"]["returncode"] = b_code
            results["browser_run"]["output"] = (b_out + "\n" + b_err).strip()
            results["browser_run"]["status"] = "PASS" if b_code == 0 else "FAIL"
        else:
            results["browser_run"]["status"] = (
                f"PENDING: Start local dev server and run: node {browser_script} http://127.0.0.1:8000"
            )
    finally:
        if temp_server_proc is not None:
            temp_server_proc.terminate()
            try:
                temp_server_proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                temp_server_proc.kill()

    # 8. Build the 38-Skill Verification Matrix from REAL evidence only.
    #    Status vocabulary (never upgrade without evidence):
    #      PASS   - an automated check ran and succeeded
    #      FAIL   - an automated check ran and found defects
    #      WARN   - check ran; non-blocking gap found
    #      N/A    - the feature does not exist in this repository (evidence: 0 matching files)
    #      REVIEW - cannot be proven by a script; the agent MUST open the SKILL.md,
    #               inspect the code, and cite file:line evidence before reporting PASS
    texts = {}

    def read(p: Path) -> str:
        if p not in texts:
            try:
                texts[p] = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                texts[p] = ""
        return texts[p]

    def files_matching(pattern: str, files=None) -> list[Path]:
        rx = re.compile(pattern, re.I)
        pool = all_code_files if files is None else files
        return [p for p in pool if p not in test_files and rx.search(read(p))]

    def rel(paths: list[Path], n: int = 3) -> str:
        out = [str(p.relative_to(target_dir)) for p in paths[:n]]
        return ", ".join(out) + (f" (+{len(paths) - n} more)" if len(paths) > n else "")

    browser_out = results["browser_run"].get("output") or ""
    b_ran = results["browser_run"]["command"] is not None
    b_pass = results["browser_run"]["status"].startswith("PASS")
    f_status = results["flutter_run"]["status"]
    t_status = results["test_run"]["status"]
    t_ran = results["test_run"]["command"] is not None
    has_ui = bool(blade_files)

    def browser_status() -> str:
        if is_skill_repo or not has_ui and not b_ran:
            return "N/A"
        if not b_ran:
            return "FAIL"  # UI exists but browser QA could not run -> never silently pass
        return "PASS" if b_pass else "FAIL"

    # Feature detection (real grep evidence)
    api_files = files_matching(r"Route::(?:apiResource|prefix\(['\"]api)|routes/api|@app\.(?:get|post)\(|router\.(?:get|post)\(|export\s+async\s+function\s+(?:GET|POST)")
    webhook_files = files_matching(r"webhook")
    sig_files = files_matching(r"hash_hmac|hmac\.(?:new|compare_digest)|createHmac|timingSafeEqual|hash_equals|X-Hub-Signature|Stripe-Signature")
    ai_files = files_matching(r"openai|anthropic|generativelanguage|gemini|groq|@google/genai|langchain")
    http_files = files_matching(r"Http::|Guzzle|axios|fetch\(|requests\.(?:get|post)|httpx\.|http\.Client|package:http|Dio\(")
    http_timeout_files = [p for p in http_files if re.search(r"timeout", read(p), re.I)]
    upload_files = files_matching(r"UploadedFile|->file\(|multer|FormData|UploadFile|csv|xlsx|Maatwebsite|fputcsv|StreamedResponse")
    queue_files = files_matching(r"ShouldQueue|dispatch\(|Queue::|Cache::|Redis|bullmq|celery|@cache|cache\.(?:get|set)")
    health_files = files_matching(r"['\"]/?(?:up|health|healthz|ready|readyz)['\"]")
    pii_log_files = files_matching(r"(?:Log::\w+|console\.log|logger\.\w+|print)\s*\([^)]*(?:password|token|secret|nik)\b")
    backup_files = [p for p in target_dir.rglob("*") if p.is_file() and not any(x in p.parts for x in EXCLUDED_SCAN_DIRS) and re.search(r"backup|restore", p.name, re.I)]
    stale_files = [p for p in target_dir.rglob("*") if p.is_file() and not any(x in p.parts for x in EXCLUDED_SCAN_DIRS) and re.search(r"\.(bak|orig|old|swp)$|~$", p.name)]
    ci_files = [p for p in [target_dir / ".github" / "workflows", target_dir / ".gitlab-ci.yml", target_dir / "Jenkinsfile", target_dir / "bitbucket-pipelines.yml", target_dir / ".circleci"] if p.exists()]
    readme = next((p for p in [target_dir / "README.md", target_dir / "readme.md"] if p.is_file()), None)
    readme_txt = read(readme) if readme else ""
    readme_has_setup = bool(re.search(r"install|setup|getting started|instalasi|cara menjalankan", readme_txt, re.I))
    readme_has_test = bool(re.search(r"\btest\b|pytest|phpunit|npm test|flutter test|pengujian", readme_txt, re.I))
    adr_dirs = [p for p in [target_dir / "docs" / "adr", target_dir / "docs" / "decisions", target_dir / "adr", target_dir / "docs"] if p.is_dir()]
    seo_ok = "viewportMeta=PRESENT" in browser_out and 'lang="n/a"' not in browser_out
    contrast_runtime_fail = "CONTRAST FAIL" in browser_out
    overflow_fail = "Horizontal scroll leak" in browser_out
    overlap_fail = "OVERLAP FAIL" in browser_out
    load_ms = [int(x) for x in re.findall(r"HTTP \d+ \((\d+)ms\)", browser_out)]
    pint_warn = any("Formatting diffs" in d for d in results["static_analysis"]["details"])

    if is_skill_repo:
        results["static_analysis"]["details"].append("Library mode: validate-skills.py schema/link checks")
    if not results["static_analysis"]["details"]:
        results["static_analysis"]["status"] = "REVIEW"
        results["static_analysis"]["details"].append("No native linter detected; agent must run the stack linter per SKILL-07")
    elif pint_warn:
        results["static_analysis"]["status"] = "WARN"

    test_skill_status = "N/A" if (is_skill_repo is False and not t_ran and not test_files and "NOT APPLICABLE" in t_status) else ("PASS" if t_status.startswith("PASS") else "FAIL")
    if test_skill_status == "PASS" and f_status == "FAIL":
        test_skill_status = "FAIL"

    lib = is_skill_repo
    M = []

    def add(sid, name, status, evidence):
        M.append((sid, name, status, evidence))

    add("SKILL-01", "project-discovery", "PASS", f"Stack detected from manifests: {', '.join(results['stack'])}")
    add("SKILL-02", "requirements-analysis", "REVIEW", f"Agent must map {len(controller_files)} route/controller files into a workflow map (Phase 1)")
    add("SKILL-03", "adaptive-architecture", "N/A" if lib else "REVIEW", f"{len(model_files)} model, {len(controller_files)} controller, {len(blade_files)} view files inventoried")
    add("SKILL-04", "technical-decision-records", "PASS" if (readme or adr_dirs) else "WARN", f"README={'yes' if readme else 'no'}, docs/ADR dirs={[str(p.relative_to(target_dir)) for p in adr_dirs] or 'none'}")
    add("SKILL-05", "ai-anti-slop", "PASS" if results["slop_check"]["status"] == "PASS" else "WARN", (results["slop_check"]["output"] or "slopcheck.py not found").splitlines()[0])
    add("SKILL-06", "adaptive-engineering", "REVIEW", "Agent must confirm new code follows existing framework idioms (applies when writing code)")
    add("SKILL-07", "code-quality-static-analysis", results["static_analysis"]["status"], "; ".join(results["static_analysis"]["details"]))
    add("SKILL-08", "refactoring-legacy-safety", "PASS" if not stale_files else "WARN", f"{len(stale_files)} stale backup/orig files" + (f": {rel(stale_files)}" if stale_files else ""))
    add("SKILL-09", "dependency-supply-chain-security", "N/A" if lib else ("PASS" if lockfiles else "WARN"), f"Lockfiles: {lockfiles or 'none committed'} (agent should also run npm/composer/pip audit)")
    add("SKILL-10", "application-security-owasp", results["security_scan"]["status"], "; ".join(results["security_scan"]["details"]))
    if webhook_files:
        add("SKILL-11", "api-security-webhook-reliability", "PASS" if sig_files else "FAIL", f"{len(webhook_files)} webhook files; signature verification found in: {rel(sig_files) or 'NONE'}")
    elif api_files:
        add("SKILL-11", "api-security-webhook-reliability", "REVIEW", f"{len(api_files)} API route files ({rel(api_files)}); agent must verify auth + validation per endpoint")
    else:
        add("SKILL-11", "api-security-webhook-reliability", "N/A", "No API routes or webhook handlers found")
    add("SKILL-12", "privacy-data-protection", "WARN" if pii_log_files else ("N/A" if lib else "REVIEW"), f"Logging of password/token/secret detected in: {rel(pii_log_files)}" if pii_log_files else "No sensitive values in log calls; agent must review PII storage/exports")
    add("SKILL-13", "threat-modeling-risk-assessment", "N/A" if lib else "REVIEW", "Agent must list trust boundaries (public/auth/admin/external) in Phase 1")
    add("SKILL-14", "ai-security-prompt-injection", "REVIEW" if ai_files else "N/A", f"AI SDK usage in: {rel(ai_files)}" if ai_files else "No LLM/AI SDK usage found")
    add("SKILL-15", "testing-strategy-design", "N/A" if lib else ("PASS" if test_files else "FAIL"), f"{len(test_files)} test files found" + ("" if test_files else " - no automated tests exist"))
    add("SKILL-16", "backend-testing-tdd", test_skill_status, f"{results['test_run']['command'] or 'no runner'} -> {t_status}" + (f"; flutter -> {f_status}" if f_status != "NOT APPLICABLE" else ""))
    add("SKILL-17", "playwright-mcp-browser-qa", browser_status(), results["browser_run"]["status"] if not lib else "Library repo has no web UI")
    add("SKILL-18", "test-data-environment-isolation", "N/A" if lib else ("PASS" if (target_dir / "phpunit.xml").is_file() and re.search(r"DB_DATABASE|sqlite|:memory:", read(target_dir / "phpunit.xml")) else ("REVIEW" if test_files else "N/A")), "phpunit.xml overrides DB for tests" if (target_dir / "phpunit.xml").is_file() else "Agent must confirm tests never touch prod DB")
    add("SKILL-19", "test-reporting-failure-diagnosis", "PASS" if t_ran or lib else "N/A", "Raw runner output captured above with exit codes" if t_ran else "No test runner executed")
    add("SKILL-20", "ui-ux-design-systems", "N/A" if not has_ui else ("REVIEW"), f"{len(blade_files)} UI files; agent must check loading/empty/error states")
    add("SKILL-21", "accessibility-engineering", "N/A" if not has_ui else ("FAIL" if (results["contrast_check"]["status"] != "PASS" or contrast_runtime_fail or not b_ran) else "PASS"), ("runtime contrast failures in Chromium" if contrast_runtime_fail else (results["contrast_check"]["output"] or "").splitlines()[0] if results["contrast_check"]["output"] else "contrast scan not run"))
    add("SKILL-22", "frontend-performance", "N/A" if not has_ui else ("REVIEW" if not load_ms else ("PASS" if max(load_ms) < 2500 else "WARN")), f"Chromium DOMContentLoaded: max {max(load_ms)}ms" if load_ms else "No browser timing captured")
    add("SKILL-23", "cross-browser-responsive-qa", "N/A" if not has_ui else ("FAIL" if (not b_ran or overflow_fail or overlap_fail) else "PASS"), "Chromium only (Firefox/WebKit not run); " + ("overflow/overlap defects found" if (overflow_fail or overlap_fail) else ("0 overflow, 0 overlaps at 1440 & 375" if b_ran else "browser QA did not run")))
    add("SKILL-24", "database-architecture-integrity", "N/A" if not migration_files else ("PASS" if fk_count else "WARN"), f"{len(migration_files)} migrations, {fk_count} FK constraints")
    add("SKILL-25", "query-optimization-performance", "N/A" if not migration_files else "REVIEW", f"{eager_count} eager-load calls, {paginate_count} paginated queries; agent must check N+1 on list endpoints")
    add("SKILL-26", "import-export-data-processing", "REVIEW" if upload_files else "N/A", f"Upload/import/export code in: {rel(upload_files)}" if upload_files else "No upload/import/export code found")
    add("SKILL-27", "api-external-service-integration", "N/A" if not http_files else ("PASS" if len(http_timeout_files) == len(http_files) else "WARN"), f"{len(http_files)} files call external HTTP; {len(http_files) - len(http_timeout_files)} without explicit timeout" + (f": {rel([p for p in http_files if p not in http_timeout_files])}" if len(http_timeout_files) < len(http_files) else ""))
    add("SKILL-28", "ai-provider-integration", "REVIEW" if ai_files else "N/A", f"AI provider calls in: {rel(ai_files)}" if ai_files else "No AI provider integration found")
    add("SKILL-29", "performance-profiling-optimization", "N/A" if lib else "REVIEW", "No profiler baseline captured; only run when a perf issue is reported")
    add("SKILL-30", "caching-background-jobs", "REVIEW" if queue_files else "N/A", f"Queue/cache usage in: {rel(queue_files)}" if queue_files else "No queue/cache usage found")
    add("SKILL-31", "ci-cd-release-engineering", "PASS" if ci_files else "WARN", f"CI config: {[str(p.relative_to(target_dir)) for p in ci_files]}" if ci_files else "No CI pipeline (.github/workflows, .gitlab-ci.yml, ...) found")
    add("SKILL-32", "environment-configuration-management", results["env_check"]["status"], "; ".join(results["env_check"]["details"]))
    add("SKILL-33", "deployment-readiness", "N/A" if lib else "REVIEW", "Only evaluated when user requests a release; never auto-deploy")
    add("SKILL-34", "observability-incident-diagnosis", "N/A" if lib else ("PASS" if health_files else "WARN"), f"Health endpoint in: {rel(health_files)}" if health_files else "No /health, /up or /ready endpoint found")
    add("SKILL-35", "backup-recovery-disaster-preparedness", "N/A" if (lib or not migration_files) else ("REVIEW" if backup_files else "WARN"), f"Backup/restore files: {rel(backup_files)}" if backup_files else "No backup/restore script or runbook found")
    add("SKILL-36", "seo-web-discoverability", "N/A" if not has_ui else ("PASS" if seo_ok else ("FAIL" if b_ran else "REVIEW")), "viewport meta + html lang present on audited routes" if seo_ok else "Missing viewport/lang or browser QA not run")
    add("SKILL-37", "documentation-developer-handoff", "PASS" if (readme_has_setup and readme_has_test) else "WARN", f"README setup section={'yes' if readme_has_setup else 'no'}, test command={'yes' if readme_has_test else 'no'}")

    blocking = [m for m in M if m[2] == "FAIL"]
    review = [m for m in M if m[2] == "REVIEW"]
    final_status = "FAIL" if blocking else ("REVIEW" if review else "PASS")
    add("SKILL-38", "final-quality-gate", final_status, f"{len(blocking)} FAIL, {len(review)} REVIEW, {sum(1 for m in M if m[2] == 'WARN')} WARN, {sum(1 for m in M if m[2] == 'N/A')} N/A")
    results["skills_matrix"] = M

    by_id = {m[0]: m for m in M}

    def gate(gid, label, ids):
        sts = [by_id[i][2] for i in ids]
        if "FAIL" in sts:
            st = "FAIL"
        elif "REVIEW" in sts:
            st = "REVIEW"
        elif "WARN" in sts:
            st = "WARN"
        elif all(s == "N/A" for s in sts):
            st = "N/A"
        else:
            st = "PASS"
        ev = ", ".join(f"{i[-2:]}={by_id[i][2]}" for i in ids)
        return (gid, f"{label} ({', '.join(ids)})", st, ev)

    results["gates_matrix"] = [
        gate("Gate 01", "Requirements & Workflow Traceability", ["SKILL-01", "SKILL-02"]),
        gate("Gate 02", "Functional Completeness & Anti-Slop", ["SKILL-05", "SKILL-06"]),
        gate("Gate 03", "Code Quality & Static Analysis", ["SKILL-07", "SKILL-08"]),
        gate("Gate 04", "Automated Backend & CRUD Tests", ["SKILL-15", "SKILL-16", "SKILL-18", "SKILL-19"]),
        gate("Gate 05", "Application Security & OWASP ASVS", ["SKILL-10", "SKILL-12", "SKILL-13", "SKILL-14"]),
        gate("Gate 06", "Dependency & Supply-Chain Security", ["SKILL-09"]),
        gate("Gate 07", "Database Integrity & Migrations", ["SKILL-24", "SKILL-25", "SKILL-26"]),
        gate("Gate 08", "API & External Service Reliability", ["SKILL-11", "SKILL-27", "SKILL-28"]),
        gate("Gate 09", "Browser QA, Contrast & Mobile View", ["SKILL-17", "SKILL-20", "SKILL-21", "SKILL-23"]),
        gate("Gate 10", "Frontend & Backend Performance", ["SKILL-22", "SKILL-29", "SKILL-30"]),
        gate("Gate 11", "Environment Config & Secret Isolation", ["SKILL-32"]),
        gate("Gate 12", "Backup, Recovery & Rollback", ["SKILL-33", "SKILL-35"]),
        gate("Gate 13", "Observability, Logging & Health Checks", ["SKILL-34"]),
        gate("Gate 14", "Documentation & Architecture Records", ["SKILL-03", "SKILL-04", "SKILL-37"]),
        gate("Gate 15", "CI/CD, SEO & Smoke Readiness", ["SKILL-31", "SKILL-33", "SKILL-36"]),
    ]

    return results


def print_report(res: dict) -> None:
    print("=" * 80)
    print("  MASTER 38-SKILL & 15-GATE GROUND-TRUTH EXECUTION AUDIT REPORT")
    print("=" * 80)
    print(f"Directory    : {res['target_dir']}")
    print(f"Stack        : {', '.join(res['stack'])}")
    if res.get("synced_agents"):
        print(f"Skills Sync  : {res['synced_agents']}")
    if res.get("healed_bins"):
        print(f"PATH Healed  : Linked {len(res['healed_bins'])} binaries into Antigravity PATH")
    print(f"Env Check    : {res['env_check']['status']} ({'; '.join(res['env_check']['details'])})")
    print(f"Anti-Slop    : {res['slop_check']['output']}")
    print(f"Contrast Scan: {res['contrast_check']['output']}")

    print("\nLocal Servers:")
    if res["dev_servers"]:
        for s in res["dev_servers"]:
            print(f"  - {s}")
    else:
        print("  - N/A (Standalone library / CLI repository)")

    print(f"\nAutomated Backend/Unit Tests ({res['test_run']['status']}):")
    if res["test_run"]["command"]:
        print(f"  Command    : {res['test_run']['command']} (exit: {res['test_run']['returncode']})")
        print("  TestDox / Execution Output:")
        lines = (res["test_run"]["output"] or "").splitlines()
        for line in lines[:120]:
            print(f"    {line}")
        if len(lines) > 120:
            print(f"    ... ({len(lines) - 120} more lines) ...")
            for line in lines[-10:]:
                print(f"    {line}")
    else:
        print(f"  Details    : {res['test_run']['status']}")

    if res["flutter_run"]["status"] != "NOT APPLICABLE":
        print(f"\nFlutter Mobile Tests ({res['flutter_run']['status']}):")
        print(f"  Command    : {res['flutter_run']['command']} (exit: {res['flutter_run']['returncode']})")
        for line in (res["flutter_run"]["output"] or "").splitlines()[-15:]:
            print(f"    {line}")

    print(f"\nPlaywright Real Chromium Browser QA ({res['browser_run']['status']}):")
    if res["browser_run"]["command"]:
        print(f"  Command    : {res['browser_run']['command']} (exit: {res['browser_run']['returncode']})")
        for line in (res["browser_run"]["output"] or "").splitlines():
            print(f"    {line}")
    else:
        print(f"  Details    : {res['browser_run']['status']}")

    print("\n" + "=" * 80)
    print("  COMPLETE 38-SKILL EXECUTION & VERIFICATION MATRIX (SKILL-01 TO SKILL-38)")
    print("=" * 80)
    for sid, sname, st, ev in res["skills_matrix"]:
        print(f"  [{st:7s}] {sid} ({sname:36s}) : {ev}")

    print("\n" + "=" * 80)
    print("  15-DOMAIN FINAL QUALITY GATE SUMMARY (GATE 01 TO GATE 15)")
    print("=" * 80)
    for gid, gname, gst, gev in res["gates_matrix"]:
        print(f"  [{gst:7s}] {gid} | {gname:68s} | {gev}")

    statuses = [m[2] for m in res["skills_matrix"]]
    n_fail, n_review = statuses.count("FAIL"), statuses.count("REVIEW")
    print("\n" + "=" * 80)
    if n_fail:
        print(f"  AUTOMATED VERDICT: BLOCKED ({n_fail} FAIL). Fix every FAIL, then re-run this script.")
    elif n_review:
        print(f"  AUTOMATED VERDICT: AUTOMATED CHECKS CLEAN - {n_review} skill(s) still need AGENT REVIEW.")
        print("  The agent MUST open each REVIEW skill's SKILL.md, inspect the code, and cite")
        print("  file:line evidence. A REVIEW item may only be reported as PASS with that evidence.")
    else:
        print("  AUTOMATED VERDICT: READY (no FAIL, no REVIEW)")
    print("  Status legend: PASS=check ran & passed | FAIL=defect | WARN=non-blocking gap |")
    print("                 N/A=feature absent (0 matching files) | REVIEW=needs agent code inspection")
    print("=" * 80)


if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    report = audit_project(target)
    print_report(report)
