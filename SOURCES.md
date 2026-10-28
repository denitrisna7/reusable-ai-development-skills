# Source Manifest & Maintenance Guide (`SOURCES.md`)

This document records every primary source, specification, repository, and official documentation set researched to build the **Reusable AI Development Skills Library**, along with retrieval status, licensing, key findings, adaptations, and ongoing maintenance procedures.

---

## 1. Primary Source Manifest

### Source 01 — Agent Skills Specification (`agentskills.io`)
- **Source Name**: Agent Skills Format Specification & Reference Validator (`skills-ref`)
- **Official URLs**:
  - https://agentskills.io/
  - https://github.com/agentskills/agentskills
- **Source Type**: Open Specification & Reference Library
- **License**: Apache License 2.0 (code / `skills-ref`) and Creative Commons Attribution 4.0 International (`CC-BY-4.0`, documentation)
- **Access Date**: 2026-10-28
- **Retrieval Status**: **RETRIEVED & VERIFIED** (Cloned into `sources/agentskills/` at commit `69ef37e9424c0a7ea9dd2293b559e43ec8176379`)
- **Main Findings**:
  1. Every skill resides in a directory `<skill-name>/SKILL.md` where the frontmatter `name` field **must** match the parent directory name exactly (`1–64` chars, lowercase alphanumeric + hyphens, no leading/trailing/consecutive hyphens).
  2. In `skills-ref/src/skills_ref/validator.py`, the allowed top-level YAML frontmatter keys are strictly restricted to: `name`, `description`, `license`, `allowed-tools`, `metadata`, and `compatibility`. Any extra top-level YAML key causes validation failure (`Unexpected fields in frontmatter`).
  3. Custom key-value pairs (`author`, `version`, `skill_id`, `category`) belong inside the `metadata` mapping (where keys and values are strings).
  4. Progressive disclosure divides context into 3 tiers: Metadata (`name` + `description`, ~100 tokens loaded at startup), Instructions (`SKILL.md` body, recommended `< 500` lines / `< 5,000` tokens loaded on activation), and Resources (`references/`, `scripts/`, `assets/` loaded on demand, referenced one level deep from `SKILL.md`).
- **Skill Areas Informed**: All 38 skills (`SKILL-01` through `SKILL-38`), library packaging, and `scripts/validate-skills.py`.
- **Adaptations Made**: Embedded the exact `skills-ref` frontmatter and naming validation logic into `scripts/validate-skills.py` using Python's standard library so the entire 38-skill library can be validated deterministically without requiring external Python virtualenvs, while also supporting `skills-ref` directly.
- **Known Limitations**: The `allowed-tools` frontmatter field is marked experimental in the specification and varies across host agent implementations; therefore, tool usage guidance is provided explicitly in the Markdown instructions of each skill rather than relying on `allowed-tools` enforcement.

---

### Source 02 — Google Antigravity Documentation & Built-in Customization Guides
- **Source Name**: Google Antigravity Official Documentation & Built-in Customization Reference
- **Official URLs**:
  - https://antigravity.google/
  - https://antigravity.google/docs/skills
  - Local runtime skills inspected: `/home/denitrisna7/.gemini/antigravity/builtin/skills/agy-customizations/` and `/home/denitrisna7/.gemini/antigravity/builtin/skills/plugin/`
- **Source Type**: Platform Documentation & Runtime Specification
- **License**: Google Documentation Terms of Service (Proprietary documentation; referenced for platform interoperability)
- **Access Date**: 2026-10-28
- **Retrieval Status**: **RETRIEVED & VERIFIED** (Saved HTML snapshot at `sources/web-docs/antigravity-skills.html` and verified against local built-in customization docs)
- **Main Findings**:
  1. Antigravity does **not** automatically load skills from arbitrary directory names (such as `reusable-ai-development-skills/skills/` alone) unless registered or placed in a supported discovery path.
  2. Verified discovery mechanisms across Antigravity surfaces:
     - **Workspace Automatic Discovery**: `<workspace-root>/.agents/skills/<skill-name>/SKILL.md` (with legacy fallback for `.agent/skills/`, `_agents/skills/`, `_agent/skills/`).
     - **Declarative JSON Config (`skills.json`)**: `<workspace-root>/.agents/skills.json` (workspace) or `~/.gemini/config/skills.json` (global) containing `{"entries": [{"path": "..."}]}` which scans each entry path one level deep for `<skill-name>/SKILL.md`.
     - **Global Skills Directory**: `~/.gemini/config/skills/<skill-name>/SKILL.md` (App & IDE) and `~/.gemini/antigravity-cli/skills/<skill-name>/SKILL.md` (CLI).
     - **Plugin Bundle**: `<plugin-root>/plugin.json` + `<plugin-root>/skills/<skill-name>/SKILL.md` installed in `~/.gemini/config/plugins/<name>/` or via `agy plugin install ./reusable-ai-development-skills`.
  3. Loading priority order (highest to lowest): (1) Workspace Project (`.agents/`), (2) Workspace Declared Configurations (`skills.json`/`plugins.json`), (3) Global Discovery (`~/.gemini/config/`), (4) Built-in Customizations, (5) Global Declared Configurations.
- **Skill Areas Informed**: Library packaging (`plugin.json`, `.agents/skills.json`), `README.md`, `SKILL_ROUTING.md`, and `COMPLETENESS_AUDIT.md`.
- **Adaptations Made**: Packaged `reusable-ai-development-skills/` so it simultaneously satisfies the standalone `skills/<name>/SKILL.md` layout, works with `.agents/skills.json` / `~/.gemini/config/skills.json`, and includes a valid `plugin.json` at its root for one-command plugin installation (`agy plugin install`).
- **Known Limitations**: Creating a new plugin directory or updating global configurations requires an Antigravity session restart for newly discovered skill directories to be indexed at startup.

---

### Source 03 — Playwright MCP
- **Source Name**: Microsoft Playwright Model Context Protocol (MCP) Server
- **Official URLs**:
  - https://playwright.dev/docs/getting-started-mcp
  - https://github.com/microsoft/playwright-mcp
- **Source Type**: Official Documentation & Open-Source Repository
- **License**: Apache License 2.0 (`sources/playwright-mcp/LICENSE`)
- **Access Date**: 2026-10-28
- **Retrieval Status**: **RETRIEVED & VERIFIED** (Cloned into `sources/playwright-mcp/` at commit `0c4107acbecb75472b23c05c0e42471a0011874f` and saved docs snapshot at `sources/web-docs/playwright-getting-started-mcp.html`)
- **Main Findings**:
  1. Playwright MCP operates on the browser's structured **accessibility tree** (`browser_snapshot` and `browser_find`) using deterministic element references (`[ref=e5]`), avoiding slow and ambiguous pixel/screenshot guessing.
  2. Core verification tools include `browser_navigate`, `browser_snapshot`, `browser_find`, `browser_click`, `browser_fill_form`, `browser_type`, `browser_select_option`, `browser_press_key`, `browser_hover`, `browser_wait_for`, `browser_resize`, `browser_emulate_media`, `browser_console_messages`, `browser_network_requests`, and `browser_network_request`.
  3. Opt-in capability flags (`--caps=network`, `--caps=storage`, `--caps=devtools`, `--caps=vision`, `--caps=pdf`) unlock route mocking (`browser_route`, `browser_network_state_set`), cookie/storage inspection (`browser_cookie_list`, `browser_storage_state`), and trace/video recording.
  4. `browser_run_code_unsafe` executes arbitrary JS in the server process (RCE-equivalent) and must be avoided or restricted to trusted environments.
  5. Persistent profiles lock `~/.cache/ms-playwright/mcp-...` per workspace; concurrent sessions require `--isolated` (optionally with `--storage-state`).
- **Skill Areas Informed**: `SKILL-17` (`playwright-mcp-browser-qa`), `SKILL-19` (`test-reporting-failure-diagnosis`), `SKILL-21` (`accessibility-engineering`), `SKILL-23` (`cross-browser-responsive-qa`), `SKILL-38` (`final-quality-gate`).
- **Adaptations Made**: Synthesized an evidence-based browser QA protocol that prioritizes semantic snapshots (`browser_snapshot`, `browser_find`), console error verification (`browser_console_messages`), and network inspection (`browser_network_requests`) over routine screenshot capture, while forbidding `PASS` claims based solely on page load.
- **Known Limitations**: Playwright MCP requires Node.js 18/20+ and an active browser binary when executing live browser tests; in headless CI or sandboxed environments without browser binaries, tests must be reported as `BLOCKED` rather than fabricated.

---

### Source 04 — AI Anti-Slop (`miqdadbadjuber/anti-slop`)
- **Source Name**: Anti Slop: Rules for AI Coding Agents (`v3.2.24`)
- **Official URL**: https://github.com/miqdadbadjuber/anti-slop
- **Source Type**: Open-Source Agent Rules & Skills Repository
- **License**: MIT License, Copyright (c) 2026 Miqdad Badjuber (`sources/anti-slop/LICENSE`); includes sub-references adapted from MIT-licensed `web-quality-skills` by Addy Osmani (`sources/anti-slop/skills/antislop-ui/LICENSE-web-quality-skills`).
- **Access Date**: 2026-10-28
- **Retrieval Status**: **RETRIEVED & VERIFIED** (Cloned into `sources/anti-slop/` at commit `13883c779a45291b005c6b1a29e06c0c26715223`)
- **Main Findings**:
  1. Defines 5 Craftsmanship Standards (`C-1` Intentionality, `C-2` Functional Completeness, `C-3` Content-Driven Composition, `C-4` Resilience, `C-5` Evidence Over Claims).
  2. Defines 40 numbered rules (`R-01` through `R-40`) across three tiers:
     - **Hard Gate**: Absolute bans on fabricated statistics/testimonials/claims (`R-17`, `R-18`, `R-36`, `R-38`), dead links/controls (`R-24`, `R-26`), missing empty/loading/error states (`R-27`), poor contrast (`R-25`), missing keyboard/focus support (`R-32`, `R-39`), broken mobile layouts (`R-03`), script-based CSS/file patching (`R-33`), broken theme toggles (`R-34`), unverified delivery (`R-35`), missing design direction (`R-37`), and unsized media / lazy hero images (`R-40`).
     - **Purpose-Gate**: Requires articulated purpose and dose caps for gradients (`R-01`), icons (`R-04`), typography (`R-06`), background grids (`R-07`), button arrows (`R-08`), badges (`R-09`), glassmorphism (`R-10`), shadows (`R-12`), glow (`R-13`), feature cards (`R-14`), animations (`R-19`), and illustrations (`R-22`).
     - **Quality Locks**: Layout rhythm (`R-05`), border radius (`R-11`), specific CTAs (`R-15`), buzzword bans (`R-16`), visual identity (`R-20`), dark mode (`R-21`), palette limits (`R-29`), no unasked product cloning (`R-30`), and one-line decision rationale (`R-31`).
  3. Includes specialized domain modules: `antislop-code` (code comment hygiene—removing decorative banners, obvious restatements, workflow narration, and vague TODOs while preserving architectural/security/business comments), `antislop-ui` (landing page and app/dashboard anti-slop), `antislop-copywriting`, `antislop-human` (WCAG contrast math and affordances), and `antislop-layoutmobile` (multi-breakpoint reflow).
- **Skill Areas Informed**: `SKILL-05` (`ai-anti-slop`), `SKILL-07` (`code-quality-static-analysis`), `SKILL-20` (`ui-ux-design-systems`), `SKILL-21` (`accessibility-engineering`), `SKILL-22` (`frontend-performance`), `SKILL-23` (`cross-browser-responsive-qa`), `SKILL-37` (`documentation-developer-handoff`), `SKILL-38` (`final-quality-gate`).
- **Adaptations Made**: Expanded the Anti-Slop philosophy beyond UI/copy/comments into full-stack software engineering discipline—preventing over-engineered abstractions, placeholder backend stubs, unnecessary third-party dependencies, and unverified completion claims across all languages and frameworks.
- **Known Limitations**: Anti-Slop acts as a quality filter and liveliness mechanism, not a substitute for brand/product design direction (`DESIGN.md` or existing project tokens).

---

### Source 05 — shadcn/ui Official Documentation
- **Source Name**: shadcn/ui Documentation
- **Official URL**: https://ui.shadcn.com/ (and https://ui.shadcn.com/docs)
- **Source Type**: Official Component & Design System Documentation
- **License**: MIT License (shadcn/ui open-source project)
- **Access Date**: 2026-10-28
- **Retrieval Status**: **RETRIEVED & VERIFIED** (Saved HTML snapshot at `sources/web-docs/shadcn-docs.html`)
- **Main Findings**:
  1. Operates on an **Open Code** distribution model (`components.json` + CLI `shadcn@latest init` / `add`), placing modifiable source components directly in the repository (`components/ui/`) rather than hiding them in opaque npm packages.
  2. Built on composable headless primitives (Radix UI / Base UI) styled with Tailwind CSS and semantic CSS custom properties (`--background`, `--foreground`, `--primary`, `--muted`, `--destructive`, `--ring`).
  3. Supports React-based frameworks (Next.js, Vite, Astro, Remix/React Router, TanStack Start, Laravel with React/Inertia).
- **Skill Areas Informed**: `SKILL-20` (`ui-ux-design-systems`), `SKILL-21` (`accessibility-engineering`), `SKILL-06` (`adaptive-engineering`).
- **Adaptations Made**: Added a strict **Technology Compatibility Gate** in `SKILL-20` and `references/shadcn-ui-design-system-reference.md` ensuring `shadcn/ui` is used seamlessly when the project uses React + Tailwind (`components.json`), while explicitly forbidding forcing `shadcn/ui` onto Vue, Angular, Blade, CodeIgniter views, MUI/Chakra/AntD, or mobile/desktop stacks.
- **Known Limitations**: Native `shadcn/ui` targets React + Tailwind CSS; non-React stacks require native framework component patterns.

---

### Source 06 — OWASP ASVS & OWASP Top 10
- **Source Name**: OWASP Application Security Verification Standard (ASVS) & OWASP Top 10
- **Official URLs**:
  - https://owasp.org/www-project-application-security-verification-standard/
  - https://owasp.org/www-project-top-ten/
- **Source Type**: Industry Security Standards
- **License**: Creative Commons Attribution-ShareAlike 4.0 International (`CC-BY-SA-4.0`)
- **Access Date**: 2026-10-28
- **Retrieval Status**: **RETRIEVED & VERIFIED** (Saved HTML snapshots at `sources/web-docs/owasp-asvs.html` and `sources/web-docs/owasp-top-ten.html`)
- **Main Findings**:
  1. OWASP ASVS defines three progressive assurance levels (**L1 Baseline**, **L2 Standard** for most sensitive data/business apps, **L3 Advanced** for critical high-value systems) across 14 verification chapters (`V1` Architecture/Threat Modeling through `V14` Configuration).
  2. OWASP Top 10 (2021) prioritizes `A01` Broken Access Control, `A02` Cryptographic Failures, `A03` Injection, `A04` Insecure Design, `A05` Security Misconfiguration, `A06` Vulnerable Components, `A07` Identification & Authentication Failures, `A08` Software & Data Integrity Failures, `A09` Security Logging & Monitoring Failures, and `A10` SSRF.
- **Skill Areas Informed**: `SKILL-09` (`dependency-supply-chain-security`), `SKILL-10` (`application-security-owasp`), `SKILL-11` (`api-security-webhook-reliability`), `SKILL-12` (`privacy-data-protection`), `SKILL-13` (`threat-modeling-risk-assessment`), `SKILL-14` (`ai-security-prompt-injection`), `SKILL-38` (`final-quality-gate`).
- **Adaptations Made**: Mapped ASVS L1/L2/L3 and Top 10 A01–A10 into stack-adaptive code review and security verification checklists across backend, frontend, API, and database layers.
- **Known Limitations**: Static code review and local tests cannot verify external cloud IAM or production WAF configurations without environment access; such checks must be marked `BLOCKED` or verified during deployment readiness.

---

### Source 07 — W3C Web Content Accessibility Guidelines (WCAG) 2.2
- **Source Name**: Web Content Accessibility Guidelines (WCAG) 2.2 W3C Recommendation
- **Official URL**: https://www.w3.org/TR/WCAG22/
- **Source Type**: International Web Standard (W3C Recommendation)
- **License**: W3C Document License
- **Access Date**: 2026-10-28
- **Retrieval Status**: **RETRIEVED & VERIFIED** (Saved HTML snapshot at `sources/web-docs/wcag22.html` and cross-referenced with `sources/anti-slop/skills/antislop-human/references/WCAG.md`)
- **Main Findings**:
  1. Establishes Level A, AA, and AAA success criteria across Perceivable, Operable, Understandable, and Robust (POUR) principles.
  2. WCAG 2.2 removes `4.1.1 Parsing` and adds 9 criteria including `2.4.11 Focus Not Obscured (Minimum)` (AA), `2.5.7 Dragging Movements` (AA), `2.5.8 Target Size (Minimum)` (AA), `3.2.6 Consistent Help` (A), `3.3.7 Redundant Entry` (A), and `3.3.8 Accessible Authentication (Minimum)` (AA).
- **Skill Areas Informed**: `SKILL-21` (`accessibility-engineering`), `SKILL-17` (`playwright-mcp-browser-qa`), `SKILL-20` (`ui-ux-design-systems`), `SKILL-23` (`cross-browser-responsive-qa`).
- **Adaptations Made**: Bundled both the complete WCAG 2.2 criterion reference and a deterministic Python 3 relative luminance contrast calculator (`skills/accessibility-engineering/scripts/contrast-check.py`).
- **Known Limitations**: Automated DOM snapshots catch ~30–50% of accessibility defects; keyboard traversal, focus order, and screen-reader announcements require interactive verification (`browser_press_key` / `browser_snapshot`).

---

### Source 08 — Google Core Web Vitals (`web.dev`)
- **Source Name**: Web Vitals Official Guide
- **Official URL**: https://web.dev/articles/vitals
- **Source Type**: Official Web Performance Documentation
- **License**: Creative Commons Attribution 4.0 International (`CC-BY-4.0`) / Apache 2.0 code samples
- **Access Date**: 2026-10-28
- **Retrieval Status**: **RETRIEVED & VERIFIED** (Saved HTML snapshot at `sources/web-docs/web-dev-vitals.html`)
- **Main Findings**:
  1. Core Web Vitals evaluate real-user experience at the **75th percentile (p75)**: **LCP <= 2.5s** (Loading), **INP <= 200ms** (Interactivity, which replaced FID), and **CLS <= 0.1** (Visual Stability).
  2. Distinguishes field data (CrUX / RUM) from lab diagnostics (DevTools performance traces / Lighthouse).
- **Skill Areas Informed**: `SKILL-22` (`frontend-performance`), `SKILL-29` (`performance-profiling-optimization`), `SKILL-36` (`seo-web-discoverability`).
- **Adaptations Made**: Integrated p75 Core Web Vitals targets alongside backend/database latency, memory, and CPU profiling so `SKILL-29` applies to both web frontends and backend/API/CLI systems.
- **Known Limitations**: Field p75 metrics cannot be measured on unvisited local dev builds; agents must measure lab traces or inspect code mechanisms (`R-40`) and state `"not measured in field"` honestly.

---

### Source 09 — GitHub Actions Documentation
- **Source Name**: GitHub Actions Official Documentation
- **Official URL**: https://docs.github.com/en/actions
- **Source Type**: Official CI/CD Platform Documentation
- **License**: Creative Commons Attribution 4.0 International (`CC-BY-4.0`) / MIT code examples
- **Access Date**: 2026-10-28
- **Retrieval Status**: **RETRIEVED & VERIFIED** (Saved HTML snapshot at `sources/web-docs/github-actions.html`)
- **Main Findings**:
  1. Defines workflow syntax, job dependencies, matrix builds, caching, artifacts, `concurrency` groups, and protected `environment` rules with required reviewers.
  2. Security hardening requires least-privilege `permissions` on `GITHUB_TOKEN`, pinning third-party actions to full commit SHAs, avoiding untrusted `${{ github.event... }}` interpolation directly in `run:` scripts (script injection), and protecting `.github/workflows/` via `CODEOWNERS`.
- **Skill Areas Informed**: `SKILL-31` (`ci-cd-release-engineering`), `SKILL-09` (`dependency-supply-chain-security`), `SKILL-33` (`deployment-readiness`).
- **Adaptations Made**: Generalized CI/CD pipeline design and security hardening patterns across GitHub Actions, GitLab CI (`.gitlab-ci.yml`), Jenkins (`Jenkinsfile`), CircleCI, Azure Pipelines, and Bitbucket Pipelines.
- **Known Limitations**: Environment protection rules and secret store bindings reside in repository hosting settings outside VCS files and must be verified with the repository administrator.

---

## 2. Library Review & Maintenance Procedure

When upstream standards, framework versions, or Antigravity platform capabilities evolve, update this library using the following deterministic workflow:

1. **Refresh Upstream Sources in `sources/`**:
   - Pull or re-clone upstream repositories (`anti-slop`, `playwright-mcp`, `agentskills`) into `sources/` and record the new commit SHA and date in `sources/README.md` and `SOURCES.md`.
   - Re-fetch updated official documentation pages into `sources/web-docs/`.
   - **Never** execute untrusted scripts from refreshed repositories during inspection.
2. **Diff Upstream Changes Against Adapted Skills**:
   - Check if `agentskills/skills-ref/src/skills_ref/validator.py` modified `ALLOWED_FIELDS` or length constraints.
   - Check if `anti-slop` added new rule numbers (`R-41+`) or updated existing rule definitions.
   - Check if `playwright-mcp` added, renamed, or deprecated MCP tool names or CLI flags.
   - Check if OWASP Top 10 / ASVS or WCAG released a new version.
3. **Update Affected `SKILL.md` and `references/` Files**:
   - Preserve the 12-section universal skill structure and technology-agnostic adaptation rules.
   - Keep `SKILL.md` files under the 500-line progressive disclosure threshold by placing bulky tables in `references/`.
   - Bump `metadata.version` in modified `SKILL.md` files and `plugin.json`.
4. **Run Validation Suite**:
   - Execute `python3 reusable-ai-development-skills/scripts/validate-skills.py` and verify 0 errors and 0 broken reference links.
   - Update `COMPLETENESS_AUDIT.md` with the new validation timestamp and results.
