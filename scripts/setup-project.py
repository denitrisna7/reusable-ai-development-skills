#!/usr/bin/env python3
"""Zero-Touch Project Bootstrap & Forced 38-Skill Rule Installer.

Ensures that whenever this library is cloned into any project via:
git clone https://github.com/denitrisna7/reusable-ai-development-skills.git .agents/skills/ai-skills

Executing this script:
python3 .agents/skills/ai-skills/scripts/setup-project.py .

Forces Antigravity and any AI coding agent to:
1. Auto-inject AGENTS.md rules into <user_rules> across the project workspace:
   - <target>/AGENTS.md
   - <target>/.gemini/rules/AGENTS.md
   - <target>/.agents/rules/AGENTS.md
2. Register all 38 skills in <target>/.agents/skills.json so Antigravity discovers all 38 skills natively.
3. Sync .agents/scripts/ and .agents/references/ with project-relative paths.
4. Auto-heal PATH for node, npm, npx, composer, flutter, dart (preventing Exit Code 127).
5. Automatically trigger the full forced 38-skill audit (`run-audit.py . --force-all`).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LIBRARY_ROOT = SCRIPT_DIR.parent


def bootstrap_project(target_dir: Path, force_audit: bool = True) -> int:
    target_dir = target_dir.resolve()
    print("=" * 80)
    print("  🚀 REUSABLE AI DEVELOPMENT SKILLS — ZERO-TOUCH PROJECT BOOTSTRAP")
    print("=" * 80)
    print(f"Target Project : {target_dir}")
    print(f"Skills Source  : {LIBRARY_ROOT}")

    is_self = target_dir == LIBRARY_ROOT.resolve()

    # 1. Sync rules into target project
    rules_src = LIBRARY_ROOT / "rules" / "AGENTS.md"
    root_agents_src = LIBRARY_ROOT / "AGENTS.md"
    before_src = LIBRARY_ROOT / "BEFORE_ACTION.md"
    skills_dir = LIBRARY_ROOT / "skills"
    refs_src = LIBRARY_ROOT / "references"
    scripts_src = LIBRARY_ROOT / "scripts"

    if not is_self:
        # A. .agents/ directory structure
        agents_dir = target_dir / ".agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        # B. .agents/rules/AGENTS.md
        rules_dst = agents_dir / "rules"
        rules_dst.mkdir(parents=True, exist_ok=True)
        if rules_src.is_file():
            shutil.copy2(rules_src, rules_dst / "AGENTS.md")
            print("  ✔ Synced: .agents/rules/AGENTS.md")

        # C. .gemini/rules/AGENTS.md (Native Antigravity Workspace Rule discovery)
        gemini_rules = target_dir / ".gemini" / "rules"
        gemini_rules.mkdir(parents=True, exist_ok=True)
        if rules_src.is_file():
            shutil.copy2(rules_src, gemini_rules / "AGENTS.md")
            print("  ✔ Injected: .gemini/rules/AGENTS.md (Antigravity <user_rules> active)")

        # D. Project root AGENTS.md
        target_root_agents = target_dir / "AGENTS.md"
        if not target_root_agents.exists() and root_agents_src.is_file():
            shutil.copy2(root_agents_src, target_root_agents)
            print("  ✔ Injected: AGENTS.md (Root workspace rule)")
        elif target_root_agents.exists() and root_agents_src.is_file():
            content = target_root_agents.read_text(encoding="utf-8", errors="ignore")
            if "Reusable AI Development Skills" not in content:
                # Prepend rule to project AGENTS.md
                new_content = root_agents_src.read_text(encoding="utf-8") + "\n\n---\n\n" + content
                target_root_agents.write_text(new_content, encoding="utf-8")
                print("  ✔ Updated: AGENTS.md (Prepended 38-skill mandatory execution rules)")

        # E. .agents/skills.json registration
        try:
            entry_path = str(skills_dir.resolve().relative_to(target_dir))
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
        if not any(e.get("path") == entry_path for e in entries if isinstance(e, dict)):
            entries.append({"path": entry_path})
            cfg_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
        print("  ✔ Registered: .agents/skills.json (All 38 skills mapped for Antigravity)")

        # F. Sync references, scripts, and BEFORE_ACTION.md
        if refs_src.is_dir():
            shutil.copytree(refs_src, agents_dir / "references", dirs_exist_ok=True)
            print("  ✔ Synced: .agents/references/")
        if scripts_src.is_dir():
            shutil.copytree(scripts_src, agents_dir / "scripts", dirs_exist_ok=True)
            print("  ✔ Synced: .agents/scripts/")
        if before_src.is_file():
            shutil.copy2(before_src, agents_dir / "BEFORE_ACTION.md")
            print("  ✔ Synced: .agents/BEFORE_ACTION.md")

    # 2. Heal PATH
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
    print("  ✔ PATH Environment Healed: ~/.local/bin and tool directories active")

    print("\n" + "=" * 80)
    print("  🎯 PROJECT BOOTSTRAP COMPLETE — ALL 38 SKILLS READY & FORCED ACTIVE")
    print("=" * 80)

    # 3. Trigger full forced audit
    if force_audit:
        print("\n⚡ Triggering Mandatory Forced All-38-Skill Execution Audit...")
        run_audit_script = LIBRARY_ROOT / "scripts" / "run-audit.py"
        if not run_audit_script.is_file():
            run_audit_script = SCRIPT_DIR / "run-audit.py"
        if run_audit_script.is_file():
            cmd = [sys.executable, str(run_audit_script), str(target_dir), "--force-all"]
            res = subprocess.run(cmd)
            return res.returncode
    return 0


if __name__ == "__main__":
    target = Path.cwd()
    force = True
    for arg in sys.argv[1:]:
        if arg == "--no-audit":
            force = False
        elif not arg.startswith("-"):
            target = Path(arg).resolve()
    sys.exit(bootstrap_project(target, force_audit=force))
