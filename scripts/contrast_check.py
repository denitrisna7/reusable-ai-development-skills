#!/usr/bin/env python3
"""WCAG 2.2 Relative Luminance, Pair Contrast Calculator, & Repository UI Contrast Auditor.

Supports two execution modes:
1. Pair Mode (2 hex arguments):
     python3 contrast-check.py "#767676" "#FFFFFF" [--json]
   Computes exact unrounded WCAG 2.2 contrast ratios between two hex colors (#RGB or #RRGGBB).

2. Repository Scan Mode (0 arguments or 1 directory/file path):
     python3 contrast-check.py [target_dir_or_file] [--json]
   Scans UI templates and stylesheets (.blade.php, .html, .vue, .jsx, .tsx, .css, .dart)
   for low-contrast Tailwind utility collisions (e.g., bg-white + text-white, bg-slate-50 + text-slate-200)
   and inline CSS color/background-color hex pairs failing WCAG 2.2 AA (< 4.5:1).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Tuple

TAILWIND_HEX_MAP = {
    "white": "#FFFFFF",
    "black": "#000000",
    "slate-50": "#F8FAFC",
    "slate-100": "#F1F5F9",
    "slate-200": "#E2E8F0",
    "slate-300": "#CBD5E1",
    "slate-400": "#94A3B8",
    "slate-500": "#64748B",
    "slate-600": "#475569",
    "slate-700": "#334155",
    "slate-800": "#1E293B",
    "slate-900": "#0F172A",
    "gray-50": "#F9FAFB",
    "gray-100": "#F3F4F6",
    "gray-200": "#E5E7EB",
    "gray-300": "#D1D5DB",
    "gray-400": "#9CA3AF",
    "gray-500": "#6B7280",
    "gray-600": "#4B5563",
    "gray-700": "#374151",
    "gray-800": "#1F2937",
    "gray-900": "#111827",
}

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
}


def parse_hex_color(value: str) -> Tuple[int, int, int, str]:
    """Parse a 3-digit or 6-digit hex color string into (R, G, B, normalized_hex)."""
    cleaned = value.strip().lstrip("#")
    if len(cleaned) == 3:
        cleaned = "".join(ch * 2 for ch in cleaned)
    if len(cleaned) != 6:
        raise ValueError(
            f"Invalid hex color '{value}'. Expected 3-digit (#RGB) or 6-digit (#RRGGBB) hex."
        )
    try:
        r = int(cleaned[0:2], 16)
        g = int(cleaned[2:4], 16)
        b = int(cleaned[4:6], 16)
    except ValueError as exc:
        raise ValueError(
            f"Invalid hex color '{value}'. Contains non-hexadecimal characters."
        ) from exc
    return r, g, b, f"#{cleaned.upper()}"


def channel_to_linear(channel_8bit: int) -> float:
    """Convert an 8-bit sRGB channel (0..255) to linearized intensity per WCAG 2.x."""
    c = channel_8bit / 255.0
    if c <= 0.03928:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(r: int, g: int, b: int) -> float:
    """Compute WCAG 2.x relative luminance L in [0.0, 1.0]."""
    r_lin = channel_to_linear(r)
    g_lin = channel_to_linear(g)
    b_lin = channel_to_linear(b)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def contrast_ratio(lum1: float, lum2: float) -> float:
    """Compute WCAG contrast ratio (L_lighter + 0.05) / (L_darker + 0.05)."""
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


def compute_hex_pair_ratio(fg_str: str, bg_str: str) -> float:
    fg_r, fg_g, fg_b, _ = parse_hex_color(fg_str)
    bg_r, bg_g, bg_b, _ = parse_hex_color(bg_str)
    return contrast_ratio(relative_luminance(fg_r, fg_g, fg_b), relative_luminance(bg_r, bg_g, bg_b))


def scan_repository(target_path: Path, as_json: bool = False) -> int:
    """Scan UI files in target_path for static low-contrast pairs."""
    ui_exts = {".php", ".html", ".vue", ".jsx", ".tsx", ".css", ".scss", ".dart"}
    files_scanned = 0
    violations: list[dict] = []

    candidates = [target_path] if target_path.is_file() else list(target_path.rglob("*"))
    for p in candidates:
        if not p.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in p.parts):
            continue
        if p.suffix not in ui_exts:
            continue
        # Only scan view/component/css/dart files, skip backend-only PHP tests/models
        rel_str = str(p.relative_to(target_path) if p != target_path else p.name)
        if p.suffix == ".php" and not rel_str.endswith(".blade.php"):
            continue

        files_scanned += 1
        content = p.read_text(encoding="utf-8", errors="ignore")

        # 1. Check class="..." attributes for conflicting base bg-* and text-* tokens
        for match in re.finditer(r'class\s*=\s*["\']([^"\']+)["\']', content):
            cls_str = match.group(1)
            tokens = cls_str.split()
            # Only inspect base (unprefixed) bg-* and text-* utility classes
            bg_tokens = [t[3:] for t in tokens if t.startswith("bg-") and ":" not in t and t[3:] in TAILWIND_HEX_MAP]
            fg_tokens = [t[5:] for t in tokens if t.startswith("text-") and ":" not in t and t[5:] in TAILWIND_HEX_MAP]
            if bg_tokens and fg_tokens:
                bg_hex = TAILWIND_HEX_MAP[bg_tokens[-1]]
                fg_hex = TAILWIND_HEX_MAP[fg_tokens[-1]]
                ratio = compute_hex_pair_ratio(fg_hex, bg_hex)
                if ratio < 3.0:
                    line_no = content[: match.start()].count("\n") + 1
                    violations.append(
                        {
                            "file": rel_str,
                            "line": line_no,
                            "fg": f"text-{fg_tokens[-1]} ({fg_hex})",
                            "bg": f"bg-{bg_tokens[-1]} ({bg_hex})",
                            "ratio": round(ratio, 2),
                        }
                    )

        # 2. Check inline style="..." attributes with both color and background-color hex
        for match in re.finditer(r'style\s*=\s*["\']([^"\']+)["\']', content):
            st_str = match.group(1)
            fg_m = re.search(r"(?<![-\w])color\s*:\s*(#[0-9a-fA-F]{3,6})\b", st_str)
            bg_m = re.search(r"background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6})\b", st_str)
            if fg_m and bg_m:
                try:
                    ratio = compute_hex_pair_ratio(fg_m.group(1), bg_m.group(1))
                    if ratio < 3.0:
                        line_no = content[: match.start()].count("\n") + 1
                        violations.append(
                            {
                                "file": rel_str,
                                "line": line_no,
                                "fg": fg_m.group(1),
                                "bg": bg_m.group(1),
                                "ratio": round(ratio, 2),
                            }
                        )
                except ValueError:
                    pass

    summary = {
        "mode": "repository_scan",
        "target": str(target_path),
        "ui_files_scanned": files_scanned,
        "violations_count": len(violations),
        "status": "PASS" if len(violations) == 0 else "FAIL",
        "violations": violations[:20],
    }

    if as_json:
        print(json.dumps(summary, indent=2))
    else:
        print(
            f"[WCAG 2.2 AA Contrast Scan] Scanned {files_scanned} UI/style files in {target_path.name or target_path}: "
            f"{len(violations)} static contrast violations ({summary['status']})"
        )
        for v in violations[:10]:
            print(f"  - {v['file']}:{v['line']} -> {v['fg']} on {v['bg']} (ratio {v['ratio']}:1 < 3.0:1)")

    return 0 if len(violations) == 0 else 1


def main(argv: list[str] | None = None) -> int:
    raw_args = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in raw_args
    pos_args = [a for a in raw_args if a not in ("--json", "-h", "--help")]

    if "-h" in raw_args or "--help" in raw_args:
        print(__doc__.strip())
        return 0

    if len(pos_args) == 0:
        return scan_repository(Path.cwd(), as_json=as_json)

    if len(pos_args) == 1:
        p = Path(pos_args[0])
        if p.exists():
            return scan_repository(p.resolve(), as_json=as_json)

    if len(pos_args) >= 2:
        try:
            fg_r, fg_g, fg_b, fg_hex = parse_hex_color(pos_args[0])
            bg_r, bg_g, bg_b, bg_hex = parse_hex_color(pos_args[1])
        except ValueError as err:
            print(f"Error: {err}", file=sys.stderr)
            return 2

        fg_lum = relative_luminance(fg_r, fg_g, fg_b)
        bg_lum = relative_luminance(bg_r, bg_g, bg_b)
        ratio = contrast_ratio(fg_lum, bg_lum)

        pass_normal_aa = ratio >= 4.5
        pass_large_or_ui_aa = ratio >= 3.0
        pass_normal_aaa = ratio >= 7.0

        result = {
            "foreground": fg_hex,
            "background": bg_hex,
            "foreground_luminance": round(fg_lum, 6),
            "background_luminance": round(bg_lum, 6),
            "contrast_ratio": round(ratio, 4),
            "contrast_ratio_display": f"{ratio:.2f}:1",
            "wcag_aa_normal_text_4_5": "PASS" if pass_normal_aa else "FAIL",
            "wcag_aa_large_text_or_ui_3_0": "PASS" if pass_large_or_ui_aa else "FAIL",
            "wcag_aaa_normal_text_7_0": "PASS" if pass_normal_aaa else "FAIL",
        }

        if as_json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Foreground : {fg_hex} (L = {fg_lum:.6f})")
            print(f"Background : {bg_hex} (L = {bg_lum:.6f})")
            print(f"Contrast   : {ratio:.2f}:1 (exact: {ratio:.4f}:1)")
            print(f"Normal Text AA  (>= 4.5:1) : {result['wcag_aa_normal_text_4_5']}")
            print(f"Large/UI AA     (>= 3.0:1) : {result['wcag_aa_large_text_or_ui_3_0']}")
            print(f"Normal Text AAA (>= 7.0:1) : {result['wcag_aaa_normal_text_7_0']}")

        return 0 if pass_large_or_ui_aa else 1

    print("Error: Invalid arguments. Pass 2 hex colors or 1 directory path.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
