#!/usr/bin/env python3
"""WCAG 2.x Relative Luminance and Contrast Ratio Calculator.

Computes exact unrounded WCAG 2.2 contrast ratios between two hex colors (#RGB or #RRGGBB)
and reports PASS/FAIL for:
- Normal text AA (>= 4.5:1)
- Large text & Non-text UI boundaries AA (>= 3.0:1)
- Normal text AAA (>= 7.0:1)

Usage:
    python3 contrast-check.py "#767676" "#FFFFFF"
    python3 contrast-check.py 0f172a f8fafc --json
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Tuple


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute exact WCAG 2.2 relative luminance contrast ratio for two hex colors."
    )
    parser.add_argument(
        "foreground",
        help="Foreground hex color (e.g., '#767676' or '0f172a').",
    )
    parser.add_argument(
        "background",
        help="Background hex color (e.g., '#FFFFFF' or 'f8fafc').",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output machine-readable JSON result.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        fg_r, fg_g, fg_b, fg_hex = parse_hex_color(args.foreground)
        bg_r, bg_g, bg_b, bg_hex = parse_hex_color(args.background)
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

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Foreground : {fg_hex} (L = {fg_lum:.6f})")
        print(f"Background : {bg_hex} (L = {bg_lum:.6f})")
        print(f"Contrast   : {ratio:.2f}:1 (exact: {ratio:.4f}:1)")
        print(
            f"Normal Text AA  (>= 4.5:1) : {result['wcag_aa_normal_text_4_5']}"
        )
        print(
            f"Large/UI AA     (>= 3.0:1) : {result['wcag_aa_large_text_or_ui_3_0']}"
        )
        print(
            f"Normal Text AAA (>= 7.0:1) : {result['wcag_aaa_normal_text_7_0']}"
        )

    return 0 if pass_large_or_ui_aa else 1


if __name__ == "__main__":
    sys.exit(main())
