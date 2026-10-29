#!/usr/bin/env python3
"""Automated pre-flight project auditor, environment healer, test runner, and Playwright Chromium trigger.

Executes real ground-truth checks on the host project:
1. Auto-PATH & Binary Healing: Ensures node, npm, npx, composer, flutter, and dart in ~/.local/bin
   or ~/development/flutter/bin are accessible in PATH and ~/.gemini/antigravity/bin (preventing Exit Code 127).
2. Stack & Architecture Detection (Node/React/Next, PHP/Laravel, Python/Django, Go, Flutter).
3. Environment & Secret Inspection (.env vs .env.example, DEBUG mode, secret leak scan).
4. Full Verbose Unit & Feature Test Execution (./vendor/bin/phpunit --testdox, npm test, pytest -v, flutter test).
5. Automatic Local Dev Server Boot (if none active) + Real Headless Chromium Playwright Audit (run-browser-audit.mjs).

Outputs empirical, non-hallucinatable logs across all engineering domains in a single run without requiring IDE reloads.
"""

from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BROWSER_AUDIT_SCRIPT = SCRIPT_DIR / "run-browser-audit.mjs"


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
    healed_bins = ensure_environment_binaries()

    results: dict = {
        "target_dir": str(target_dir),
        "healed_bins": healed_bins,
        "stack": [],
        "env_check": {"status": "UNKNOWN", "details": []},
        "dev_servers": [],
        "active_url": None,
        "test_run": {"status": "NOT TESTED", "command": None, "output": None, "returncode": None},
        "flutter_run": {"status": "NOT APPLICABLE", "command": None, "output": None, "returncode": None},
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
                env_issues.append("WARNING: DEBUG mode is active in local .env (must be APP_DEBUG=false in production).")
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

    # 3. Automated Backend/Unit Test Runner Execution (Verbose TestDox output)
    phpunit_bin = target_dir / "vendor" / "bin" / "phpunit"
    if phpunit_bin.is_file():
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

    # Optional Flutter Mobile Analysis & Test Suite
    flutter_dir = target_dir / "mobile" if mobile_pubspec.is_file() else (target_dir if flutter_pubspec.is_file() else None)
    if flutter_dir:
        f_code, f_out, f_err = run_cmd(["flutter", "test"], flutter_dir, timeout=120)
        if f_code != 127:
            results["flutter_run"]["command"] = f"flutter test (in {flutter_dir.name})"
            results["flutter_run"]["returncode"] = f_code
            results["flutter_run"]["output"] = (f_out + "\n" + f_err).strip()
            results["flutter_run"]["status"] = "PASS" if f_code == 0 else "FAIL"

    # 4. Local Server Detection or Temporary Ephemeral Server Boot for Playwright
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
    if not results["active_url"]:
        # Automatically boot a temporary local server so Playwright Browser QA NEVER gets skipped!
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
        elif pkg_json.is_file() and "dev" in results.get("pkg_scripts", []):
            temp_port = 18124
            temp_server_proc = subprocess.Popen(
                ["npm", "run", "dev", "--", "--host", "127.0.0.1", "--port", str(temp_port)],
                cwd=str(target_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if wait_for_port("127.0.0.1", temp_port, timeout=12.0):
                results["active_url"] = f"http://127.0.0.1:{temp_port}"
                results["dev_servers"].append(f"AUTO-STARTED EPHEMERAL SERVER: {results['active_url']} (npm run dev)")

    # 5. Execute Real Headless Chromium Browser QA via run-browser-audit.mjs
    try:
        if results["active_url"] and BROWSER_AUDIT_SCRIPT.is_file():
            b_cmd = ["node", str(BROWSER_AUDIT_SCRIPT), results["active_url"]]
            b_code, b_out, b_err = run_cmd(b_cmd, target_dir, timeout=90)
            results["browser_run"]["command"] = f"node {BROWSER_AUDIT_SCRIPT} {results['active_url']}"
            results["browser_run"]["returncode"] = b_code
            results["browser_run"]["output"] = (b_out + "\n" + b_err).strip()
            results["browser_run"]["status"] = "PASS" if b_code == 0 else "FAIL"
        else:
            results["browser_run"]["status"] = (
                "PENDING: Start local dev server and run: "
                f"node {BROWSER_AUDIT_SCRIPT} http://127.0.0.1:8000"
            )
    finally:
        if temp_server_proc is not None:
            temp_server_proc.terminate()
            try:
                temp_server_proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                temp_server_proc.kill()

    return results


def print_report(res: dict) -> None:
    print("=" * 72)
    print("  PROJECT GROUND-TRUTH PRE-FLIGHT & EXECUTION AUDIT REPORT")
    print("=" * 72)
    print(f"Directory   : {res['target_dir']}")
    print(f"Stack       : {', '.join(res['stack'])}")
    if res.get("healed_bins"):
        print(f"PATH Healed : Linked {len(res['healed_bins'])} binaries into Antigravity PATH")
    print(f"Env Check   : {res['env_check']['status']}")
    for d in res['env_check']['details']:
        print(f"  - {d}")

    print("\nLocal Servers:")
    if res['dev_servers']:
        for s in res['dev_servers']:
            print(f"  - {s}")
    else:
        print("  - NONE DETECTED on ports 8000, 3000, 5173, 8080")

    print(f"\nAutomated Backend/Unit Tests ({res['test_run']['status']}):")
    if res['test_run']['command']:
        print(f"  Command    : {res['test_run']['command']} (exit: {res['test_run']['returncode']})")
        print("  TestDox / Execution Output:")
        lines = (res['test_run']['output'] or "").splitlines()
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
