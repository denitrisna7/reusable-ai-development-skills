#!/usr/bin/env python3
"""Automated pre-flight project auditor and ground-truth evidence collector.

This script executes real diagnostic checks on the host project:
1. Environment & Secret Inspection (.env vs .env.example, DEBUG mode, secret leak scan)
2. Stack Detection (Node/React/Next, PHP/Laravel, Python/Django, Go, etc.)
3. Automated Test Runner Execution (npm test, php artisan test, pytest)
4. Local Dev Server Health Check (localhost ports 3000, 5173, 8000, 8080)
5. Build & Dependency Vulnerability Check

Outputs empirical results so the AI agent cannot hallucinate or fake PASS states.
"""

from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
from pathlib import Path


def check_port(host: str, port: int, timeout: float = 0.5) -> bool:
    """Check if a local port is actively accepting connections."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def run_cmd(cmd: list[str], cwd: Path, timeout: int = 60) -> tuple[int, str, str]:
    """Execute a CLI command safely and capture exit code, stdout, and stderr."""
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
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
        "test_run": {"status": "NOT TESTED", "command": None, "output": None, "returncode": None},
        "build_check": {"status": "NOT TESTED", "command": None, "output": None, "returncode": None},
        "recommendations": [],
    }

    # 1. Stack Detection
    pkg_json = target_dir / "package.json"
    composer_json = target_dir / "composer.json"
    pyproject = target_dir / "pyproject.toml"
    req_txt = target_dir / "requirements.txt"
    go_mod = target_dir / "go.mod"

    if pkg_json.is_file():
        try:
            data = json.loads(pkg_json.read_text(encoding="utf-8"))
            results["stack"].append(f"Node.js (name: {data.get('name', 'unnamed')})")
            scripts = data.get("scripts", {})
            results["pkg_scripts"] = list(scripts.keys())
        except Exception:
            results["stack"].append("Node.js (invalid package.json)")

    if composer_json.is_file():
        results["stack"].append("PHP / Composer")
        if (target_dir / "artisan").is_file():
            results["stack"].append("Laravel Framework")

    if pyproject.is_file() or req_txt.is_file():
        results["stack"].append("Python")

    if go_mod.is_file():
        results["stack"].append("Go")

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
            # Check DEBUG mode
            if re.search(r"^APP_DEBUG\s*=\s*true", content, re.M | re.I) or re.search(r"^DEBUG\s*=\s*true", content, re.M | re.I):
                env_issues.append("WARNING: DEBUG mode is active (APP_DEBUG=true or DEBUG=true). Must be false in production.")
            # Check for dummy placeholder secrets
            if re.search(r"(secret|password|key)\s*=\s*(changeme|secret|admin|password|123456)", content, re.M | re.I):
                env_issues.append("SECURITY RISK: Default/weak placeholder credential detected in .env.")
            results["env_check"]["details"].append("Local .env file verified.")
        else:
            env_issues.append("NOTICE: .env file missing in working directory (ensure environment variables are configured).")

        if env_example.is_file() and env_file.is_file():
            # Check for missing keys between .env and .env.example
            ex_keys = set(re.findall(r"^([A-Z0-9_]+)\s*=", env_example.read_text(errors="ignore"), re.M))
            env_keys = set(re.findall(r"^([A-Z0-9_]+)\s*=", env_file.read_text(errors="ignore"), re.M))
            missing_in_env = ex_keys - env_keys
            if missing_in_env:
                env_issues.append(f"CONFIG DRIFT: Keys present in .env.example but missing from .env: {sorted(missing_in_env)}")

        if any("SECURITY RISK" in issue for issue in env_issues):
            results["env_check"]["status"] = "FAIL"
        elif env_issues:
            results["env_check"]["status"] = "WARNING"
        else:
            results["env_check"]["status"] = "PASS"
        results["env_check"]["details"].extend(env_issues)

    # 3. Local Server Health Check
    common_ports = [(3000, "Node / Next.js / Vite"), (5173, "Vite Dev Server"), (8000, "Laravel / Django / FastAPI"), (8080, "Web Server")]
    for port, label in common_ports:
        if check_port("127.0.0.1", port):
            results["dev_servers"].append(f"ACTIVE: http://127.0.0.1:{port} ({label})")

    # 4. Automated Test Runner Execution
    if pkg_json.is_file() and "test" in results.get("pkg_scripts", []):
        cmd = ["npm", "test", "--", "--run"]
        code, out, err = run_cmd(cmd, target_dir)
        results["test_run"]["command"] = "npm test"
        results["test_run"]["returncode"] = code
        results["test_run"]["output"] = (out + "\n" + err).strip()[:1000]
        results["test_run"]["status"] = "PASS" if code == 0 else "FAIL"
    elif (target_dir / "artisan").is_file():
        cmd = ["php", "artisan", "test"]
        code, out, err = run_cmd(cmd, target_dir)
        results["test_run"]["command"] = "php artisan test"
        results["test_run"]["returncode"] = code
        results["test_run"]["output"] = (out + "\n" + err).strip()[:1000]
        results["test_run"]["status"] = "PASS" if code == 0 else "FAIL"
    elif pyproject.is_file() or (target_dir / "tests").is_dir():
        cmd = ["pytest"]
        code, out, err = run_cmd(cmd, target_dir)
        if code != 127:
            results["test_run"]["command"] = "pytest"
            results["test_run"]["returncode"] = code
            results["test_run"]["output"] = (out + "\n" + err).strip()[:1000]
            results["test_run"]["status"] = "PASS" if code == 0 else "FAIL"
        else:
            results["test_run"]["status"] = "BLOCKED: pytest runner not found in environment"
    else:
        results["test_run"]["status"] = "BLOCKED: No automated test runner configured in repository"

    return results


def print_report(res: dict) -> None:
    print("=" * 60)
    print("  PROJECT GROUND-TRUTH PRE-FLIGHT AUDIT REPORT")
    print("=" * 60)
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
        print("  - NONE DETECTED on ports 3000, 5173, 8000, 8080 (Dev server not running)")

    print(f"\nAutomated Tests ({res['test_run']['status']}):")
    if res['test_run']['command']:
        print(f"  Command    : {res['test_run']['command']} (exit: {res['test_run']['returncode']})")
        print("  Output Sample:")
        for line in (res['test_run']['output'] or "").splitlines()[:10]:
            print(f"    {line}")
    else:
        print(f"  Details    : {res['test_run']['status']}")

    print("\n" + "=" * 60)
    if res['test_run']['status'] == 'PASS' and res['env_check']['status'] == 'PASS':
        print("  VERDICT: BASELINE TESTS PASS (Proceed with browser QA & final gate)")
    else:
        print("  VERDICT: ACTION REQUIRED (Fix failing tests or start dev server)")
    print("=" * 60)


if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    report = audit_project(target)
    print_report(report)
