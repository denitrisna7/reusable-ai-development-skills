---
name: accessibility-engineering
description: "Audits and engineers user interfaces for WCAG 2.2 Level A and AA accessibility, semantic HTML landmarks, keyboard navigation, focus management, accessible forms, color contrast, and screen reader compatibility. Activate when building or reviewing frontend UI, dialogs, forms, or color palettes. Do not use for backend API logic or non-UI code quality checks (use code-quality-static-analysis)."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-21"
  category: "Frontend and User Experience"
---

# Accessibility Engineering (WCAG 2.2)

This skill enforces WCAG 2.2 Level A and Level AA compliance across web and native user interfaces, covering semantic structure, keyboard operability, focus management, accessible form ergonomics, deterministic color contrast calculation, screen reader announcements, and accessible dialogs/navigation. It integrates the W3C WCAG 2.2 specification with the Anti-Slop human accessibility gates (`R-25`, `R-32`, `R-34`, `R-39`) so accessibility is engineered into components from the start rather than bolted on after release.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Auditing, building, or remediating user interfaces for WCAG 2.2 Level A/AA accessibility compliance.
- Designing or modifying color palettes, dark/light theme tokens, text-over-image overlays, or UI control borders requiring contrast verification (`R-25`, `R-34`).
- Implementing interactive widgets such as modal dialogs, drawers, dropdown menus, tabs, comboboxes, tooltips, carousels, or drag-and-drop surfaces.
- Building or reviewing forms, authentication screens, validation error flows, and status/toast notifications.

## 2. When Not to Use

Do not use this skill as the primary workflow for:
- General component styling, layout composition, or `shadcn/ui` setup that does not involve accessibility requirements: pair with `ui-ux-design-systems` (`SKILL-20`).
- Asset compression, bundle splitting, or network latency tuning: route to `frontend-performance` (`SKILL-22`).
- Headless backend services, database schema migrations, or internal queue workers with no user-facing markup or output.

## 3. Scope and Objectives

Every accessibility engineering task or audit must address:
- **Semantic HTML & Document Structure**: Enforce valid `<html lang="...">`, route-specific `<title>`, semantic landmarks (`<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`), sequential headings (`<h1>` to `<h6>` without skipped levels), and native interactive elements (`<button type="button">`, `<a href="...">`).
- **Keyboard Navigation (`WCAG 2.1.1`, `2.1.2`, `2.5.7`)**: Ensure every interactive control is reachable and operable via keyboard (`Tab`, `Shift+Tab`, `Enter`, `Space`, `Arrow` keys, `Escape`), with zero accidental keyboard traps and single-pointer/keyboard alternatives for all dragging movements.
- **Focus Management (`WCAG 2.4.3`, `2.4.7`, `2.4.11`)**: Preserve logical DOM focus order, enforce high-contrast `:focus-visible` indicators (never `outline: none` without a visible replacement), trap focus inside active modal dialogs while restoring focus to the trigger upon close, and prevent sticky headers/footers from obscuring focused elements (`scroll-padding-top` / `scroll-padding-bottom`).
- **Accessible Forms & Authentication (`WCAG 1.3.5`, `3.3.1`, `3.3.2`, `3.3.7`, `3.3.8`)**: Bind every input to a visible `<label for="...">`, declare appropriate `autocomplete` tokens, associate helper and error messages via `aria-describedby` + `aria-invalid="true"`, avoid redundant re-entry across multi-step wizards, and never block password/code paste (`onpaste` blocking is forbidden).
- **Deterministic Color Contrast (`WCAG 1.4.1`, `1.4.3`, `1.4.11`, `R-25`)**: Verify unrounded contrast ratios of at least `4.5:1` for normal text (`< 24px` or `< 18.66px` bold) and `3.0:1` for large text, input borders, focus rings, and graphical status indicators across both light and dark themes (`R-34`). Never convey status by color alone.
- **Screen Reader Compatibility (`WCAG 1.1.1`, `2.5.3`, `4.1.2`, `4.1.3`)**: Provide meaningful `alt` text for informative images (`alt=""` or `aria-hidden="true"` for decorative icons), ensure visible labels match `aria-label` substrings, expose accurate ARIA states (`aria-expanded`, `aria-selected`, `aria-checked`, `aria-current="page"`), and announce dynamic status updates via `role="status"` (`aria-live="polite"`) or `role="alert"`.
- **Accessible Dialogs, Navigation, & Motion (`WCAG 2.2.2`, `2.4.1`, `2.5.8`)**: Include a `"Skip to main content"` bypass link, ensure dialogs declare accessible titles (`<DialogTitle>` / `aria-labelledby`), enforce minimum `24x24px` target sizes (`44x44px` on touch viewports per `R-03`), and honor `@media (prefers-reduced-motion: reduce)`.
- **Appropriate Accessibility Testing**: Combine deterministic contrast math, static markup inspection, automated axe/Lighthouse rules where installed, and Playwright MCP accessibility tree snapshots (`browser_snapshot`).

## 4. Prerequisites and Context Requirements

Before executing an accessibility audit or remediation, inspect:
1. **Component Templates & Stylesheets**: HTML/JSX/Vue/Blade/Jinja templates, CSS token variables (`globals.css`, `tailwind.config.*`), and theme definitions.
2. **Target Conformance Level**: Default to **WCAG 2.2 Level AA** (plus `44x44px` touch target sizing from `R-03`) unless the project explicitly requires Level AAA (`7.0:1` normal text contrast).
3. **Local Reference & Tooling**: Read [references/wcag22-checklist.md](references/wcag22-checklist.md) and use [scripts/contrast-check.py](scripts/contrast-check.py) for exact contrast verification.

## 5. Step-by-Step Workflow

### Step 1: Audit Document Semantics, Landmarks, and Native Elements
- [ ] Verify root `<html lang="...">`, unique page `<title>`, and a `"Skip to main content"` link targeting `<main id="main-content">`.
- [ ] Check that page regions use `<header>`, `<nav aria-label="...">` (when multiple `<nav>` landmarks exist), `<main>`, `<aside>`, and `<footer>`.
- [ ] Verify heading hierarchy (`<h1>` through `<h6>`) has one primary `<h1>` per view and does not skip levels for visual sizing.
- [ ] Replace any `<div onClick>` or `<span onClick>` acting as a button with `<button type="button">`, and any click-handler navigation element with `<a href="...">` (`WCAG 4.1.2`, `R-39`).

### Step 2: Verify Color Contrast Deterministically (`R-25`, `R-34`)
- [ ] Extract hex values for all foreground/background pairings (body text, muted secondary text, badge text, button labels, link text, input borders, focus rings) in both light and dark modes.
- [ ] Execute [scripts/contrast-check.py](scripts/contrast-check.py) on every pairing rather than guessing visually:
  ```bash
  python3 skills/accessibility-engineering/scripts/contrast-check.py "#64748B" "#FFFFFF"
  ```
- [ ] Adjust any token that fails (`< 4.5:1` for normal text or `< 3.0:1` for large text and UI borders). Ensure text placed over images or gradients maintains contrast against the worst-case region of the background via a solid scrim or backdrop layer.
- [ ] Confirm that required fields, validation errors, and status badges include text, icons, or shape cues rather than color alone (`WCAG 1.4.1`).

### Step 3: Engineer Keyboard Navigation, Focus Management, and Target Sizes
- [ ] Verify every interactive control has a clear `:focus-visible` indicator with `>= 3.0:1` contrast against adjacent surfaces. Remove any bare `outline: none` or ` focus:outline-none` that lacks a high-contrast `focus-visible:ring-*` replacement.
- [ ] Add `scroll-padding-top` and `scroll-padding-bottom` on the scroll container matching any sticky header or fixed bottom bar height (`WCAG 2.4.11 Focus Not Obscured`).
- [ ] For modal dialogs and drawers (`<dialog>` or Radix/Base UI `Dialog`), confirm focus moves inside on open, cycles within the modal on `Tab`/`Shift+Tab`, closes on `Escape`, and returns to the trigger button on close.
- [ ] Verify that all drag-and-drop interactions (Kanban boards, reorderable lists, range sliders) expose keyboard/click buttons (`Move up`, `Move down`, or numeric input) (`WCAG 2.5.7`).
- [ ] Ensure interactive targets meet at least `24x24px` on desktop and `44x44px` with `>= 8px` gap spacing on mobile/touch viewports (`WCAG 2.5.8`, `R-03`).

### Step 4: Harden Forms, Authentication, and Live Status Announcements
- [ ] Pair every `<input>`, `<textarea>`, and `<select>` with an explicit `<label for="...">`. Placeholder text is never a substitute for a visible label (`WCAG 3.3.2`).
- [ ] Wire validation errors using `aria-invalid="true"` and `aria-describedby="<error-id>"`, and render dynamic error summaries or toast messages inside `role="alert"` or `role="status"` (`aria-live="polite"`).
- [ ] Add appropriate `autocomplete` attributes (`username`, `current-password`, `new-password`, `one-time-code`) and verify that no `onPaste` handler blocks pasting into password or verification fields (`WCAG 3.3.8`).
- [ ] Wrap non-essential animations in `@media (prefers-reduced-motion: no-preference)` or disable transitions when `prefers-reduced-motion: reduce` is active.

### Step 5: Execute Accessibility Verification (Static + Browser Snapshot)
- [ ] Run project accessibility linters or unit tests if configured (`eslint-plugin-jsx-a11y`, `vitest-axe`, `jest-axe`, `@axe-core/playwright`, `flutter test` semantics checks).
- [ ] When a live browser environment is available, use `playwright-mcp-browser-qa` (`SKILL-17`) to capture `browser_snapshot(boxes=true)`, test full keyboard traversal (`browser_press_key` with `Tab`, `Enter`, `Escape`), and test media emulation (`browser_emulate_media` for `colorScheme: "dark"` and `reducedMotion: "reduce"`).

## 6. Technology-Specific Adaptation Rules

| Stack / Ecosystem | Accessibility Implementation Pattern | Verification & Tooling |
| :--- | :--- | :--- |
| **React / Next.js / shadcn/ui / Radix / Base UI** | Use `useId()` for deterministic `<Label htmlFor={id}>` and `aria-describedby` pairing. Preserve `<DialogTitle>` and `<DialogDescription>` in modals. | `eslint-plugin-jsx-a11y`, `@axe-core/playwright`, `vitest-axe`, Playwright MCP `browser_snapshot`. |
| **Vue / Nuxt / Svelte / Angular** | Use accessible primitives (`reka-ui`, `bits-ui`, `@angular/cdk/a11y` `FocusTrap`, `LiveAnnouncer`). Ensure custom icon buttons pass `aria-label`. | `eslint-plugin-vuejs-accessibility`, `@angular-eslint/template/accessibility-*`, Playwright MCP. |
| **Server Templates (Laravel Blade / CodeIgniter / Django / Rails / Go)** | Render semantic HTML5 landmarks, native `<button>`/`<a href>`, `<label for>`, and server-rendered error summaries with `id` + `aria-describedby` + `autofocus` on first error. | HTML validation, `contrast-check.py`, and Playwright MCP accessibility snapshots. |
| **Java / Spring (Thymeleaf) & C# / .NET (Razor / Blazor)** | Use accessible component wrappers, explicit `for`/`id` tag helpers (`asp-for`), and `EditForm` validation summaries with `role="alert"`. | Automated Playwright / Axe checks and `contrast-check.py`. |
| **Rust (Leptos / Yew / Dioxus / Askama) & Unknown Stacks** | Emit standard semantic HTML elements, preserve native focus order, and wire keyboard handlers (`Enter`, `Space`, `Escape`) on custom interactive islands. | Inspect rendered DOM accessibility tree and run `contrast-check.py` on CSS variables. |
| **Mobile & Native (Flutter / SwiftUI / Android Compose)** | In Flutter, use `Semantics` widgets, `excludeSemantics` on decorative images, `Tooltip`, `FocusTraversalGroup`, `MediaQuery.accessibleNavigationOf(context)`, and minimum `48x48dp` (`kMinInteractiveDimension`) touch targets. | `flutter_a11y_agent` subagent (when available in Flutter workspaces) and `matchesGoldenFile` / semantics tree assertions in `flutter test`. |

### Accessible Dialog & Custom Widget Contract Quick-Reference

- **Modal Dialog (`role="dialog"` / `<dialog>`)**:
  - Must set `aria-modal="true"` (or open `<dialog>` via `.showModal()`).
  - Must reference a visible or visually-hidden title via `aria-labelledby`.
  - Must trap `Tab` and `Shift+Tab` inside the dialog boundary while open.
  - Must dismiss cleanly on `Escape` (unless an explicit confirmation blocker is required) and restore focus to the invoking trigger element.
- **Tabs (`role="tablist"`, `role="tab"`, `role="tabpanel"`)**:
  - Active tab sets `aria-selected="true"` and `tabindex="0"`; inactive tabs set `aria-selected="false"` and `tabindex="-1"`.
  - Arrow keys (`ArrowLeft`/`ArrowRight` or `ArrowUp`/`ArrowDown`) move between tabs; `Tab` moves from the active tab into its linked `tabpanel` (`aria-controls` / `aria-labelledby`).
- **Disclosure / Accordion (`<button aria-expanded="true|false" aria-controls="panel-id">`)**:
  - Toggle button must always remain a native `<button>` (wrapped inside an `<h2>`/`<h3>` if it acts as a section heading).

## 7. Security and Safety Considerations

- **Accessible Authentication Without Weakening Security (`WCAG 3.3.8`)**: Supporting password managers (`autocomplete="current-password"`), passkeys/WebAuthn, and copy-paste into password fields improves both accessibility and security by enabling strong generated passwords.
- **Safe Error Descriptions (`WCAG 3.3.1` vs. OWASP)**: Make validation messages specific for legitimate users (e.g., `"Enter a valid email address including '@'"`), while keeping authentication failure messages generic against account enumeration (e.g., `"Invalid email or password"`).
- **Screen-Reader Injection Defense**: Never inject unsanitized user-controlled strings into `aria-label` or hidden live-region announcements without escaping.

## 8. Verification Criteria

Completion requires explicit evidence across these checks:
1. **Contrast Proof**: Every text and UI border token pair has been verified via [scripts/contrast-check.py](scripts/contrast-check.py) (or computed relative luminance) to meet `>= 4.5:1` (normal text) and `>= 3.0:1` (large text and non-text UI boundaries) in both light and dark modes.
2. **Semantic & ARIA Tree Proof**: Every interactive element has an accessible name, valid role, and native keyboard activation (`<button>` for actions, `<a href>` for links); zero unlabeled icon buttons or bare `<div onclick>` handlers remain.
3. **Keyboard & Focus Proof**: Focus order is sequential, `:focus-visible` is clearly rendered, sticky headers/footers do not obscure focused elements (`WCAG 2.4.11`), and modals trap and restore focus cleanly on `Escape`.
4. **Form & Reduced Motion Proof**: All inputs have `<label for>`, error states bind `aria-invalid` + `aria-describedby`, paste is permitted on auth fields (`WCAG 3.3.8`), and `prefers-reduced-motion: reduce` is respected.

## 9. Failure Handling and Edge Cases

- **Third-Party Widget Inaccessibility**: If an embedded third-party component lacks keyboard or ARIA support and its source cannot be edited, wrap it in a landmark with clear skip instructions, provide an accessible fallback control for the same task, and record the limitation in the audit report.
- **Dynamic Text Over User-Uploaded Images**: Because user-uploaded backgrounds have unpredictable luminance, always enforce a deterministic semi-opaque scrim (`rgba(0, 0, 0, 0.65)` or solid badge container) behind overlaid text so contrast never drops below `4.5:1`.
- **Headless / CLI Environment Without Browser**: Run `contrast-check.py` and static template/AST checks, and mark interactive browser focus testing as `"NOT TESTED (no live browser target)"` rather than claiming full dynamic verification.

## 10. Expected Outputs and Reporting Requirements

Report accessibility engineering results using this template:

```markdown
## Accessibility Engineering Audit & Remediation Report (WCAG 2.2 AA)

### 1. Conformance Scope
- **Target Standard**: WCAG 2.2 Level A & Level AA (+ `44x44px` touch target gate `R-03`)
- **Views / Components Audited**: [List of routes or component files]
- **Themes Checked**: [Light / Dark / High Contrast]

### 2. Deterministic Contrast Verification (`contrast-check.py`)
| Element / Token Pair | Foreground | Background | Ratio | Threshold | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [e.g., Body text (Light)] | `#0F172A` | `#FFFFFF` | `17.85:1` | `>= 4.5:1` | PASS |
| [e.g., Muted text (Light)] | `#475569` | `#F8FAFC` | `7.18:1` | `>= 4.5:1` | PASS |
| [e.g., Input border] | `#64748B` | `#FFFFFF` | `4.76:1` | `>= 3.0:1` | PASS |

### 3. WCAG 2.2 Checklist Summary
| Area | WCAG Criteria | Status (PASS / FAIL / BLOCKED / NOT TESTED) | Evidence / Remediation |
| :--- | :--- | :--- | :--- |
| Semantic Landmarks & Headings | 1.3.1, 2.4.1, 2.4.2, 3.1.1 | [Status] | [Details] |
| Keyboard & Focus Management | 2.1.1, 2.1.2, 2.4.7, 2.4.11 | [Status] | [Details] |
| Target Size & Drag Alternatives | 2.5.7, 2.5.8 (`R-03`) | [Status] | [Details] |
| Forms & Accessible Auth | 1.3.5, 3.3.1, 3.3.2, 3.3.7, 3.3.8 | [Status] | [Details] |
| Screen Reader & Live Regions | 1.1.1, 2.5.3, 4.1.2, 4.1.3 | [Status] | [Details] |
| Reflow (`320px`) & Reduced Motion | 1.4.4, 1.4.10, 2.2.2 | [Status] | [Details] |
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - `ui-ux-design-systems` (`SKILL-20`): Passes new or updated components, themes, forms, and modals for accessibility hardening.
- **Downstream / Co-Activated Skills**:
  - `playwright-mcp-browser-qa` (`SKILL-17`) and `cross-browser-responsive-qa` (`SKILL-23`): Executes live accessibility tree snapshots (`browser_snapshot`), `320px` reflow verification, and keyboard navigation tests.
  - `final-quality-gate` (`SKILL-38`): Consumes the WCAG 2.2 verification report as part of release readiness (`Gate 9: UI/UX and accessibility`).

## 12. Source References

- **W3C Web Content Accessibility Guidelines (WCAG) 2.2**: https://www.w3.org/TR/WCAG22/
- **WAI-ARIA Authoring Practices Guide (APG)**: https://www.w3.org/WAI/ARIA/apg/
- **Anti-Slop Human Accessibility Rules (`antislop-human`)**: https://github.com/miqdadbadjuber/anti-slop (MIT License)
- **Local Skill Reference (WCAG 2.2 Checklist)**: [references/wcag22-checklist.md](references/wcag22-checklist.md)
- **Local Skill Script (WCAG Contrast Calculator)**: [scripts/contrast-check.py](scripts/contrast-check.py)
- **Shared Library Reference (WCAG 2.2 Accessibility)**: [../../references/wcag22-accessibility-reference.md](../../references/wcag22-accessibility-reference.md)
