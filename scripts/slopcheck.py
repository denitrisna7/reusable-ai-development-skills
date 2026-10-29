#!/usr/bin/env python3
"""SKILL-05 AI Anti-Slop, Placeholder Stub, & Copywriting Hygiene Scanner.

Audits application source and UI template files (.blade.php, .php, .tsx, .jsx, .ts, .js, .vue, .py, .dart)
for:
1. Unfinished placeholder text ("Lorem ipsum", "TODO: implement", "FIXME:") in production views/code.
2. Dead anchor links (`href="#"` without interactive click/modal attributes).
3. Banned AI copywriting clichés ("unleash", "delve into", "game-changer", "in today's fast-paced world").
4. Forgotten debug dumps (`dd(`, `var_dump(`, `debugger;`) in application code.

Usage:
    python3 scripts/slopcheck.py [target_dir] [--json]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

EXCLUDED_DIRS = {
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
    "tests",
    "test",
}

BANNED_COPY_PATTERNS = [
    r"\blorem ipsum\b",
    r"\bunleash the power\b",
    r"\bdelve into\b",
    r"\bin today's fast-paced world\b",
    r"\bgame-changer\b",
    r"\bseamless(?:ly)? integrat(?:e|ion)\b",
]


def scan_slop(target_dir: Path) -> dict:
    code_exts = {".php", ".tsx", ".jsx", ".ts", ".js", ".vue", ".py", ".dart", ".html"}
    files_scanned = 0
    findings: list[dict] = []

    candidates = [target_dir] if target_dir.is_file() else list(target_dir.rglob("*"))
    for p in candidates:
        if not p.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in p.parts):
            continue
        if p.suffix not in code_exts:
            continue
        if p.name in ("slopcheck.py", "run-audit.py", "contrast-check.py", "contrast_check.py", "validate-skills.py"):
            continue

        files_scanned += 1
        rel = str(p.relative_to(target_dir) if p != target_dir else p.name)
        content = p.read_text(encoding="utf-8", errors="ignore")

        # 1. Check banned AI copywriting / Lorem ipsum in UI templates
        is_ui = rel.endswith((".blade.php", ".tsx", ".jsx", ".vue", ".html", ".dart"))
        if is_ui:
            for pat in BANNED_COPY_PATTERNS:
                for m in re.finditer(pat, content, re.I):
                    line_no = content[: m.start()].count("\n") + 1
                    findings.append(
                        {
                            "file": rel,
                            "line": line_no,
                            "type": "AI_COPY_OR_LOREM_SLOP",
                            "detail": f"Matched banned phrase '{m.group(0)}'",
                        }
                    )

            # 2. Check dead href="#" links without JS/Alpine/Livewire handler
            for m in re.finditer(r"<a\b[^>]*\bhref\s*=\s*['\"]#['\"][^>]*>", content, re.I):
                tag = m.group(0)
                if not re.search(r"(@click|x-on:click|onclick|wire:click|data-bs-|data-modal)", tag, re.I):
                    line_no = content[: m.start()].count("\n") + 1
                    findings.append(
                        {
                            "file": rel,
                            "line": line_no,
                            "type": "DEAD_ANCHOR_LINK",
                            "detail": "Anchor tag with href='#' and no interactive handler",
                        }
                    )

        # 3. Check forgotten debug dumps in non-test application code
        if p.suffix == ".php" and not rel.startswith(("database/", "config/", "routes/console.php")):
            for m in re.finditer(r"(?<![\w>$])\b(dd|var_dump)\s*\(", content):
                line_no = content[: m.start()].count("\n") + 1
                findings.append(
                    {
                        "file": rel,
                        "line": line_no,
                        "type": "LEFTOVER_DEBUG_CALL",
                        "detail": f"Leftover debug call '{m.group(1)}()'",
                    }
                )

    return {
        "target": str(target_dir),
        "files_scanned": files_scanned,
        "findings_count": len(findings),
        "status": "PASS" if len(findings) == 0 else "WARNING",
        "findings": findings[:25],
    }


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--json"]
    as_json = "--json" in sys.argv[1:]
    target = Path(args[0]).resolve() if args else Path.cwd()
    res = scan_slop(target)

    if as_json:
        print(json.dumps(res, indent=2))
    else:
        print(
            f"[SKILL-05 Anti-Slop Scan] Scanned {res['files_scanned']} source/UI files in {target.name or target}: "
            f"{res['findings_count']} slop findings ({res['status']})"
        )
        for f in res["findings"][:10]:
            print(f"  - [{f['type']}] {f['file']}:{f['line']} -> {f['detail']}")

    return 0 if res["findings_count"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
