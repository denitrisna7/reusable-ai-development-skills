#!/usr/bin/env python3
"""Comprehensive validator for the Reusable AI Development Skills Library.

Validates:
1. All 38 required skill directories exist under skills/.
2. SKILL.md YAML frontmatter strictly conforms to the Agent Skills (agentskills.io)
   specification and skills-ref validator rules:
   - Starts and closes with '---'
   - Only allowed top-level keys: name, description, license, allowed-tools, metadata, compatibility
   - 'name' matches directory name, lowercase alphanumeric + hyphens, 1..64 chars,
     no leading/trailing/consecutive hyphens
   - 'description' is non-empty string, 1..1024 chars
   - 'compatibility' (if present) is string, 1..500 chars
   - 'metadata' (if present) maps string keys to string values
3. Every SKILL.md contains all 12 mandatory universal authoring sections.
4. Progressive disclosure compliance (line count <= 500 lines per SKILL.md).
5. All relative file links inside SKILL.md resolve to existing files on disk.
6. Technology adaptability check (verifying technology-specific adaptation rules exist).
7. Library-level documentation, references, sources, and plugin manifest exist.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

LIBRARY_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = LIBRARY_ROOT / "skills"

EXPECTED_SKILLS: list[tuple[str, str, str]] = [
    ("SKILL-01", "project-discovery", "Core Discovery and Planning"),
    ("SKILL-02", "requirements-analysis", "Core Discovery and Planning"),
    ("SKILL-03", "adaptive-architecture", "Core Discovery and Planning"),
    ("SKILL-04", "technical-decision-records", "Core Discovery and Planning"),
    ("SKILL-05", "ai-anti-slop", "Core Development Quality"),
    ("SKILL-06", "adaptive-engineering", "Core Development Quality"),
    ("SKILL-07", "code-quality-static-analysis", "Core Development Quality"),
    ("SKILL-08", "refactoring-legacy-safety", "Core Development Quality"),
    ("SKILL-09", "dependency-supply-chain-security", "Core Development Quality"),
    ("SKILL-10", "application-security-owasp", "Security Engineering"),
    ("SKILL-11", "api-security-webhook-reliability", "Security Engineering"),
    ("SKILL-12", "privacy-data-protection", "Security Engineering"),
    ("SKILL-13", "threat-modeling-risk-assessment", "Security Engineering"),
    ("SKILL-14", "ai-security-prompt-injection", "Security Engineering"),
    ("SKILL-15", "testing-strategy-design", "Testing and Quality Assurance"),
    ("SKILL-16", "backend-testing-tdd", "Testing and Quality Assurance"),
    ("SKILL-17", "playwright-mcp-browser-qa", "Testing and Quality Assurance"),
    ("SKILL-18", "test-data-environment-isolation", "Testing and Quality Assurance"),
    ("SKILL-19", "test-reporting-failure-diagnosis", "Testing and Quality Assurance"),
    ("SKILL-20", "ui-ux-design-systems", "Frontend and User Experience"),
    ("SKILL-21", "accessibility-engineering", "Frontend and User Experience"),
    ("SKILL-22", "frontend-performance", "Frontend and User Experience"),
    ("SKILL-23", "cross-browser-responsive-qa", "Frontend and User Experience"),
    ("SKILL-24", "database-architecture-integrity", "Data and Integrations"),
    ("SKILL-25", "query-optimization-performance", "Data and Integrations"),
    ("SKILL-26", "import-export-data-processing", "Data and Integrations"),
    ("SKILL-27", "api-external-service-integration", "Data and Integrations"),
    ("SKILL-28", "ai-provider-integration", "Data and Integrations"),
    ("SKILL-29", "performance-profiling-optimization", "Performance, Operations, and Deployment"),
    ("SKILL-30", "caching-background-jobs", "Performance, Operations, and Deployment"),
    ("SKILL-31", "ci-cd-release-engineering", "Performance, Operations, and Deployment"),
    ("SKILL-32", "environment-configuration-management", "Performance, Operations, and Deployment"),
    ("SKILL-33", "deployment-readiness", "Performance, Operations, and Deployment"),
    ("SKILL-34", "observability-incident-diagnosis", "Performance, Operations, and Deployment"),
    ("SKILL-35", "backup-recovery-disaster-preparedness", "Performance, Operations, and Deployment"),
    ("SKILL-36", "seo-web-discoverability", "Performance, Operations, and Deployment"),
    ("SKILL-37", "documentation-developer-handoff", "Final Quality and Maintenance"),
    ("SKILL-38", "final-quality-gate", "Final Quality and Maintenance"),
]

ALLOWED_FRONTMATTER_FIELDS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}

REQUIRED_SECTION_PATTERNS = [
    (r"^##\s+1\.\s+Activation Conditions", "1. Activation Conditions"),
    (r"^##\s+2\.\s+When Not to Use", "2. When Not to Use"),
    (r"^##\s+3\.\s+Scope and Objectives", "3. Scope and Objectives"),
    (r"^##\s+4\.\s+Prerequisites and Context Requirements", "4. Prerequisites and Context Requirements"),
    (r"^##\s+5\.\s+Step-by-Step Workflow", "5. Step-by-Step Workflow"),
    (r"^##\s+6\.\s+Technology-Specific Adaptation Rules", "6. Technology-Specific Adaptation Rules"),
    (r"^##\s+7\.\s+Security and Safety Considerations", "7. Security and Safety Considerations"),
    (r"^##\s+8\.\s+Verification Criteria", "8. Verification Criteria"),
    (r"^##\s+9\.\s+Failure Handling", "9. Failure Handling"),
    (r"^##\s+10\.\s+Expected Outputs and Reporting Requirements", "10. Expected Outputs and Reporting Requirements"),
    (r"^##\s+11\.\s+Interoperability and Skill Routing", "11. Interoperability and Skill Routing"),
    (r"^##\s+12\.\s+Source References", "12. Source References"),
]

REQUIRED_ROOT_FILES = [
    "README.md",
    "CHANGELOG.md",
    "BEFORE_ACTION.md",
    "AGENTS.md",
    "rules/AGENTS.md",
    "SKILL_CATALOG.md",
    "SKILL_ROUTING.md",
    "SOURCES.md",
    "COMPLETENESS_AUDIT.md",
    "plugin.json",
    "sources/README.md",
    "scripts/run-audit.py",
    "scripts/run-browser-audit.mjs",
    "scripts/contrast-check.py",
    "scripts/contrast_check.py",
    "scripts/slopcheck.py",
    "scripts/slopcheck.sh",
]


def parse_simple_yaml_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter without requiring third-party PyYAML/strictyaml."""
    if not content.startswith("---\n") and not content.startswith("---\r\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter delimiter '---'")

    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("SKILL.md YAML frontmatter is not properly closed with '---'")

    raw_yaml = parts[1]
    body = parts[2]

    data: dict = {}
    lines = raw_yaml.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if line.startswith(" ") or line.startswith("\t"):
            raise ValueError(f"Unexpected indentation at line: {line!r}")
        if ":" not in line:
            raise ValueError(f"Invalid YAML key-value line: {line!r}")

        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()

        if val in (">-", ">", "|", "|-"):
            block_lines = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                block_lines.append(lines[i].strip())
                i += 1
            joiner = " " if val.startswith(">") else "\n"
            data[key] = joiner.join(b for b in block_lines if b).strip()
            continue
        elif val == "":
            nested: dict[str, str] = {}
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                sub = lines[i].strip()
                if sub and not sub.startswith("#"):
                    if ":" not in sub:
                        raise ValueError(f"Invalid nested YAML line: {sub!r}")
                    skey, sval = sub.split(":", 1)
                    skey = skey.strip()
                    sval = sval.strip()
                    if (sval.startswith('"') and sval.endswith('"')) or (
                        sval.startswith("'") and sval.endswith("'")
                    ):
                        sval = sval[1:-1]
                    nested[skey] = sval
                i += 1
            data[key] = nested
            continue
        else:
            if (val.startswith('"') and val.endswith('"')) or (
                val.startswith("'") and val.endswith("'")
            ):
                val = val[1:-1]
            data[key] = val
            i += 1

    return data, body


def validate_skill(skill_id: str, skill_name: str, expected_category: str) -> tuple[list[str], list[str], dict]:
    """Validate a single skill directory and return (errors, warnings, stats)."""
    errors: list[str] = []
    warnings: list[str] = []
    skill_dir = SKILLS_DIR / skill_name
    skill_md = skill_dir / "SKILL.md"
    stats = {"skill_id": skill_id, "name": skill_name, "lines": 0, "links_checked": 0}

    if not skill_dir.exists() or not skill_dir.is_dir():
        errors.append(f"[{skill_id}] Missing skill directory: {skill_dir}")
        return errors, warnings, stats

    if not skill_md.exists():
        errors.append(f"[{skill_id}] Missing SKILL.md in {skill_dir}")
        return errors, warnings, stats

    content = skill_md.read_text(encoding="utf-8")
    lines = content.splitlines()
    stats["lines"] = len(lines)

    if len(lines) > 500:
        errors.append(
            f"[{skill_id}] {skill_name}/SKILL.md exceeds 500-line progressive disclosure limit ({len(lines)} lines)"
        )
    elif len(lines) < 100:
        warnings.append(
            f"[{skill_id}] {skill_name}/SKILL.md is relatively short ({len(lines)} lines)"
        )

    try:
        meta, body = parse_simple_yaml_frontmatter(content)
    except ValueError as exc:
        errors.append(f"[{skill_id}] {skill_name}/SKILL.md frontmatter parse error: {exc}")
        return errors, warnings, stats

    extra_fields = set(meta.keys()) - ALLOWED_FRONTMATTER_FIELDS
    if extra_fields:
        errors.append(
            f"[{skill_id}] {skill_name}/SKILL.md has unexpected top-level frontmatter fields: {sorted(extra_fields)}"
        )

    name_val = meta.get("name", "")
    if not isinstance(name_val, str) or not name_val.strip():
        errors.append(f"[{skill_id}] Missing or empty 'name' in frontmatter")
    else:
        norm_name = unicodedata.normalize("NFKC", name_val.strip())
        if norm_name != skill_name:
            errors.append(
                f"[{skill_id}] Frontmatter name '{norm_name}' does not match directory '{skill_name}'"
            )
        if len(norm_name) > 64:
            errors.append(f"[{skill_id}] Skill name exceeds 64 chars ({len(norm_name)})")
        if norm_name != norm_name.lower():
            errors.append(f"[{skill_id}] Skill name must be lowercase: '{norm_name}'")
        if norm_name.startswith("-") or norm_name.endswith("-") or "--" in norm_name:
            errors.append(f"[{skill_id}] Invalid hyphen placement in skill name: '{norm_name}'")
        if not all(c.isalnum() or c == "-" for c in norm_name):
            errors.append(f"[{skill_id}] Invalid characters in skill name: '{norm_name}'")

    desc_val = meta.get("description", "")
    if not isinstance(desc_val, str) or not desc_val.strip():
        errors.append(f"[{skill_id}] Missing or empty 'description' in frontmatter")
    elif len(desc_val) > 1024:
        errors.append(
            f"[{skill_id}] Description exceeds 1024 chars ({len(desc_val)} chars)"
        )
    elif len(desc_val) < 60:
        warnings.append(
            f"[{skill_id}] Description is very brief ({len(desc_val)} chars); consider adding explicit trigger keywords"
        )

    compat_val = meta.get("compatibility")
    if compat_val is not None:
        if not isinstance(compat_val, str) or len(compat_val) > 500:
            errors.append(f"[{skill_id}] Invalid 'compatibility' field (must be string <= 500 chars)")

    meta_block = meta.get("metadata")
    if not isinstance(meta_block, dict):
        warnings.append(f"[{skill_id}] Missing 'metadata' dictionary in frontmatter")
    else:
        if meta_block.get("skill_id") != skill_id:
            warnings.append(
                f"[{skill_id}] metadata.skill_id is {meta_block.get('skill_id')!r}, expected {skill_id!r}"
            )
        if meta_block.get("category") != expected_category:
            warnings.append(
                f"[{skill_id}] metadata.category is {meta_block.get('category')!r}, expected {expected_category!r}"
            )

    for pattern, label in REQUIRED_SECTION_PATTERNS:
        if not re.search(pattern, body, flags=re.MULTILINE):
            errors.append(f"[{skill_id}] {skill_name}/SKILL.md missing required section: '{label}'")

    # Check relative markdown links outside fenced code blocks
    body_no_code = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", body_no_code):
        target = match.group(2).strip()
        if (
            target.startswith("http://")
            or target.startswith("https://")
            or target.startswith("mailto:")
            or target.startswith("#")
            or target.startswith("file://")
            or target.startswith("customization://")
            or target.startswith("sidecar://")
        ):
            continue
        target_path_str = target.split("#", 1)[0].strip()
        if not target_path_str:
            continue
        resolved = (skill_dir / target_path_str).resolve()
        stats["links_checked"] += 1
        if not resolved.exists():
            errors.append(
                f"[{skill_id}] Broken relative link in {skill_name}/SKILL.md: '{target}' -> {resolved} (not found)"
            )

    return errors, warnings, stats


def main() -> int:
    all_errors: list[str] = []
    all_warnings: list[str] = []
    skill_stats: list[dict] = []

    print(f"Validating Reusable AI Development Skills Library at: {LIBRARY_ROOT}\n")

    # 1. Validate root files
    for rel_path in REQUIRED_ROOT_FILES:
        p = LIBRARY_ROOT / rel_path
        if not p.exists():
            all_errors.append(f"[ROOT] Missing required library file: {rel_path}")

    # Validate plugin.json syntax
    plugin_json_path = LIBRARY_ROOT / "plugin.json"
    if plugin_json_path.exists():
        try:
            pdata = json.loads(plugin_json_path.read_text(encoding="utf-8"))
            if "name" not in pdata or "description" not in pdata:
                all_errors.append("[ROOT] plugin.json must contain 'name' and 'description'")
        except Exception as exc:
            all_errors.append(f"[ROOT] Invalid JSON in plugin.json: {exc}")

    # 2. Validate all 38 required skills
    expected_names = {name for _, name, _ in EXPECTED_SKILLS}
    if SKILLS_DIR.exists():
        actual_dirs = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}
        unexpected_dirs = actual_dirs - expected_names
        if unexpected_dirs:
            all_warnings.append(f"[SKILLS] Additional skill directories present: {sorted(unexpected_dirs)}")
    else:
        all_errors.append(f"[ROOT] Missing skills directory: {SKILLS_DIR}")

    for skill_id, skill_name, category in EXPECTED_SKILLS:
        errs, warns, st = validate_skill(skill_id, skill_name, category)
        all_errors.extend(errs)
        all_warnings.extend(warns)
        skill_stats.append(st)

    total_lines = sum(s["lines"] for s in skill_stats)
    total_links = sum(s["links_checked"] for s in skill_stats)
    present_skills = sum(1 for s in skill_stats if s["lines"] > 0)

    print(f"Skills checked:         {present_skills} / {len(EXPECTED_SKILLS)}")
    print(f"Total SKILL.md lines:   {total_lines}")
    print(f"Relative links verified:{total_links}")
    print(f"Warnings:               {len(all_warnings)}")
    print(f"Errors:                 {len(all_errors)}\n")

    if all_warnings:
        print("=== WARNINGS ===")
        for w in all_warnings:
            print(f"  WARN: {w}")
        print()

    if all_errors:
        print("=== VALIDATION ERRORS ===")
        for e in all_errors:
            print(f"  ERROR: {e}")
        print("\nRESULT: FAILED")
        return 1

    print("RESULT: PASSED (All 38 skills, frontmatter schemas, sections, line budgets, and relative links are valid!)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
