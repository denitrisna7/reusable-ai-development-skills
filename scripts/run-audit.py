#!/usr/bin/env python3
"""Automated pre-flight project auditor, test runner, and Playwright Chromium trigger.

Executes real ground-truth checks on the host project:
1. Stack & Architecture Detection (Node/React/Next, PHP/Laravel, Python/Django, Go, Flutter)
2. Environment & Secret Inspection (.env vs .env.example, DEBUG mode, secret leak scan)
3. Full Verbose Unit & Feature Test Execution (./vendor/bin/phpunit --testdox, npm test, pytest -v, flutter test)
4. Local Dev Server Health Check & Automatic Real Chromium Playwright Audit (run-browser-audit.mjs)

Outputs empirical, non-hallucinatable logs across all engineering domains.
"""

from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BROWSER_AUDIT_SCRIPT = SCRIPT_DIR / "run-browser-audit.mjs"


def check_port(host: str, port: int, timeout: float = 0.5) -> bool:
    """Check if a local port is actively accepting connections."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def run_cmd(cmd: list[str], cwd: Path, timeout: int = 120, env_overrides: dict | None = None) -> tuple[int, str, str]:
    """Execute a CLI command safely and capture exit code, stdout, and stderr."""
    env = os.environ.copy()
    # Prevent Laravel 12 Collision from collapsing test output into 1-line JSON in AI environments
    for key in ["CLAUDECODE", "CLAUDE_CODE", "CURSOR_TRACE_ID", "AGENT", "AI_AGENT"]:
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


def audit_project(target_dir: Path) -> dict:
    results: dict = {
        "target_dir": str(target_dir),
        "stack": [],
        "env_check": {"status": "UNKNOWN", "details": []},
        "dev_servers": [],
        "active_url": None,
        "test_run": {"status": "NOT TESTED", "command": None, "output": None, "returncode": None},
        "browser_run": {"status": "NOT TESTED", "command": None, "output": None, "returncode": None},
    }

    # 1. Stack Detection
    pkg_json = target_dir / "package.json"
    composer_json = target_dir / "composer.json"
    pyproject = target_dir / "pyproject.toml"
    req_txt = target_dir / "requirements.txt"
    go_mod = target_dir / "go.mod"
    flutter_pubspec = target_dir / "pubspec.yaml"
    mobile_pubspec = target_dir / "mobile" / "pubspec.yaml"

    if pkg_json.is_file():
        try:
            data = json.loads(pkg_json.read_text(encoding="utf-8"))
            results["stack"].append(f"Node.js ({data.get('name', 'unnamed')})")
            scripts = data.get("scripts", {})
            results["pkg_scripts"] = list(scripts.keys())
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

    # 2. Environment & Secret Inspection
    env_file = target_dir / ".env"
    env_example = target_dir / ".env.example"

    if not env_file.is_file() and not env_example.is_file():
        results["env_check"]["status"] = "PASS"
        results["env_check"]["details"].append("No .env file found (static/serverless app).")
    else:
        env_issues = []
        if env_file.is_file():
            content = env_file.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"^APP_DEBUG\s*=\s*true", content, re.M | re.I) or re.search(r"^DEBUG\s*=\s*true", content, re.M | re.I):
                env_issues.append("WARNING: DEBUG mode is active (APP_DEBUG=true or DEBUG=true). Must be false in production.")
            if re.search(r"(secret|password|key)\s*=\s*(changeme|secret|admin|password|123456)", content, re.M | re.I):
                env_issues.append("SECURITY RISK: Default/weak placeholder credential detected in .env.")
            results["env_check"]["details"].append("Local .env file verified.")
        else:
            env_issues.append("NOTICE: .env file missing in working directory.")

        if env_example.is_file() and env_file.is_file():
            ex_keys = set(re.findall(r"^([A-Z0-9_]+)\s*=", env_example.read_text(errors="ignore"), re.M))
            env_keys = set(re.findall(r"^([A-Z0-9_]+)\s*=", env_file.read_text(errors="ignore"), re.M))
            missing_in_env = ex_keys - env_keys
            if missing_in_env:
                env_issues.append(f"CONFIG DRIFT: Keys in .env.example missing from .env: {sorted(missing_in_env)}")

        if any("SECURITY RISK" in issue for issue in env_issues):
            results["env_check"]["status"] = "FAIL"
        elif env_issues:
            results["env_check"]["status"] = "WARNING"
        else:
            results["env_check"]["status"] = "PASS"
        results["env_check"]["details"].extend(env_issues)

    # 3. Local Server Health Check
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

    # 4. Automated Test Runner Execution (Verbose TestDox output so tests are never hidden in 1-line JSON)
    phpunit_bin = target_dir / "vendor" / "bin" / "phpunit"
    if phpunit_bin.is_file():
        cmd = [str(phpunit_bin), "--testdox", "--colors=never"]
        code, out, err = run_cmd(cmd, target_dir)
        results["test_run"]["command"] = "./vendor/bin/phpunit --testdox"
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
        cmd = ["npm", "test", "--", "--run"]
        code, out, err = run_cmd(cmd, target_dir)
        results["test_run"]["command"] = "npm test"
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
            results["test_run"]["status"] = "BLOCKED: pytest runner not found in environment"
    else:
        results["test_run"]["status"] = "BLOCKED: No automated test runner configured in repository"

    # 5. Automatic Real Headless Chromium Browser QA (if a local server is active and run-browser-audit.mjs exists)
    if results["active_url"] and BROWSER_AUDIT_SCRIPT.is_file():
        b_cmd = ["node", str(BROWSER_AUDIT_SCRIPT), results["active_url"]]
        b_code, b_out, b_err = run_cmd(b_cmd, target_dir, timeout=90)
        results["browser_run"]["command"] = f"node {BROWSER_AUDIT_SCRIPT.name} {results['active_url']}"
        results["browser_run"]["returncode"] = b_code
        results["browser_run"]["output"] = (b_out + "\n" + b_err).strip()
        results["browser_run"]["status"] = "PASS" if b_code == 0 else "FAIL"
    else:
        results["browser_run"]["status"] = (
            "PENDING: Start local dev server (e.g. php artisan serve / npm run dev) and run: "
            f"node {BROWSER_AUDIT_SCRIPT} http://127.0.0.1:8000"
        )

    return results


def print_report(res: dict) -> None:
    print("=" * 72)
    print("  PROJECT GROUND-TRUTH PRE-FLIGHT & EXECUTION AUDIT REPORT")
    print("=" * 72)
    print(f"Directory   : {res['target_dir']}")
    print(f"Stack       : {', '.join(res['stack'])}")
    print(f"Env Check   : {res['env_check']['status']}")
    for d in res['env_check']['details']:
        print(f"  - {d}")

    print("\nLocal Servers:")
    if res['dev_servers']:
        for s in res['dev_servers']:
            print(f"  - {s}")
    else:
        print("  - NONE DETECTED on ports 8000, 3000, 5173, 8080 (Start local server for Browser QA)")

    print(f"\nAutomated Backend/Unit Tests ({res['test_run']['status']}):")
    if res['test_run']['command']:
        print(f"  Command    : {res['test_run']['command']} (exit: {res['test_run']['returncode']})")
        print("  TestDox / Execution Output:")
        lines = (res['test_run']['output'] or "").splitlines()
        for line in lines[:80]:
            print(f"    {line}")
        if len(lines) > 80:
            print(f"    ... ({len(lines) - 80} more lines) ...")
            for line in lines[-8:]:
                print(f"    {line}")
    else:
        print(f"  Details    : {res['test_run']['status']}")

    print(f"\nPlaywright Real Chromium Browser QA ({res['browser_run']['status']}):")
    if res['browser_run']['command']:
        print(f"  Command    : {res['browser_run']['command']} (exit: {res['browser_run']['returncode']})")
        for line in (res['browser_run']['output'] or "").splitlines():
            print(f"    {line}")
    else:
        print(f"  Details    : {res['browser_run']['status']}")

    print("\n" + "=" * 72)
    if res['test_run']['status'] == 'PASS' and res['browser_run']['status'] == 'PASS':
        print("  VERDICT: ALL AUTOMATED & PLAYWRIGHT CHROMIUM BROWSER AUDITS PASSED")
    else:
        print("  VERDICT: ACTION REQUIRED (Ensure tests and Playwright browser audit pass)")
    print("=" * 72)


if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    report = audit_project(target)
    print_report(report)
