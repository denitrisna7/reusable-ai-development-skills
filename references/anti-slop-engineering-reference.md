# AI Anti-Slop & Engineering Craftsmanship Reference

> Adapted from **Anti Slop: Rules for AI Coding Agents** (`https://github.com/miqdadbadjuber/anti-slop`, commit `13883c779a45291b005c6b1a29e06c0c26715223`), Copyright (c) 2026 Miqdad Badjuber, licensed under the MIT License.

This reference consolidates the core engineering discipline, UI/visual anti-slop filter, copywriting hygiene, and code comment standards for use across the library.

---

## 1. The Five Craftsmanship Standards (`C-1` to `C-5`)

1. **`C-1` — Intentionality**: Every architectural, code, visual, and copy decision must have an articulable reason rooted in project requirements or brand identity. "It is the AI default" is never a valid justification.
2. **`C-2` — Functional Completeness**: Every interactive element, endpoint, or CLI command must actually work or not exist. Dead buttons, unimplemented stub routes disguised as complete, and links pointing to non-existent sections (`href="#"`) are defects.
3. **`C-3` — Content-Driven Composition**: Every module, abstraction, database table, or UI section must exist because the product's actual domain requires it—not to fill a template.
4. **`C-4` — Resilience**: Implementations must hold up across all states (empty, loading, error, success), all supported themes (light/dark if shipped), all responsive breakpoints, and keyboard-only navigation.
5. **`C-5` — Evidence Over Claims**: Anything presented as fact (test results, performance improvements, statistics, testimonials, security compliance claims) must be real and verified, or omitted entirely.

---

## 2. Code & Engineering Anti-Slop Rules

### A. Code Comment Hygiene (Adapted from `antislop-code`)
- **No Decorative Separators**: Never write ASCII/box-drawing banners (`// ====================`, `// ---- WORKFLOW ----`).
- **No Restating the Obvious**: Never write comments that repeat the code (`// Initialize count` above `let count = 0`).
- **No Step-by-Step Workflow Narration**: Do not litter functions with `// Step 1: Validate`, `// Step 2: Save`, `// Step 3: Return`.
- **No Empty Category Labels**: Remove generic headers like `// Main logic`, `// Helper function`, `// Business logic`.
- **No Vague TODOs**: Only write `TODO` comments when they name a concrete task, constraint, or ticket reference.
- **No Decorative Emoji in Code**: Never place emoji (`✅`, `🚀`, `🔒`) in code comments or log strings unless explicitly required by an existing CLI convention.
- **Preserve High-Value Comments**: Always retain comments that explain non-obvious business intent, security invariants, concurrency traps, protocol edge cases, regulatory rules, or third-party workarounds. Keep comments concise (1–2 lines per fact).

### B. Architectural & Implementation Discipline
- **No Premature Abstractions**: Do not create generic factory-of-factories, single-implementation interfaces, or wrapper layers unless required by existing architecture or test seam isolation.
- **No Placeholder Masquerading**: Never present mocked return values, hardcoded arrays, or `pass` / `// TODO: implement` blocks as completed features.
- **No Source/CSS Patching Scripts (`R-33`)**: Never mutate source code or stylesheets via ad-hoc regex replacement scripts left in the repo; edit the canonical source files directly.
- **No Unnecessary Dependencies**: Before adding any third-party package, verify whether the language standard library or an already-installed package solves the problem.

---

## 3. UI, Visual, and Copywriting Filter Summary (`R-01` to `R-40`)

### Tier 1: Hard Gate (Absolute Requirements — Zero Exceptions)
- **`R-02` No Unapproved Em Dashes**: Avoid mechanical AI em-dash (`—`) overuse in generated UI copy and prose; use commas, periods, colons, or parentheses unless matching an explicit user writing sample.
- **`R-03` Mobile Responsiveness**: Zero horizontal overflow, no text escaping containers, minimum `44x44px` touch targets, and purposeful mobile layout reflow across breakpoints (including tablet/small laptop `600px–1024px`).
- **`R-17` & `R-18` No Fake Data or Testimonials**: Never invent statistics (`10K+ users`, `99.9% uptime`), fake customer quotes, AI avatars, or filler activity feeds (`Sarah Chen updated a document`). Use real data or explicit placeholders (`[REAL DATA]`).
- **`R-23` Clarification for Visual Assets**: Do not invent brand logos, team photos, or unrequested navigation hierarchies without user confirmation or honest placeholders (`[LOGO]`).
- **`R-24` & `R-26` Real Navigation & Interactive Controls**: Every nav link must point to a real destination; every button, modal, toggle, or form must execute real behavior or carry an explicit visible `"Coming soon"` label + code `TODO`.
- **`R-25` WCAG AA Contrast**: Minimum `4.5:1` for normal text, `3.0:1` for large text (`18px+` or `14px+` bold) and non-text UI boundaries (`WCAG 1.4.11`), verified across the entire background/gradient.
- **`R-27` Complete UI States**: Every data-driven view must implement explicit, informative **Empty**, **Loading**, and **Error** states (naming the cause and next action).
- **`R-28` Product-Specific FAQ**: Never generate generic template FAQs unrelated to the specific product.
- **`R-32` & `R-39` Keyboard & Semantic Affordances**: Use native `<button>` for actions and `<a href>` for navigation; set `cursor: pointer` on enabled controls; provide visible `:focus-visible` indicators (never `outline: none` without replacement); include accessible names (`aria-label`) on icon-only buttons; respect `prefers-reduced-motion: reduce`.
- **`R-34` Theme Completeness**: If a light/dark toggle is shipped, both themes must pass contrast and layout checks completely.
- **`R-35` Verify Before Delivery**: Build/run the application and verify interactive elements and console errors before claiming completion.
- **`R-36` & `R-38` No Fabricated Claims**: Never invent SOC 2 / ISO 27001 badges, unmeasured Lighthouse/Web Vitals scores, or fake `John Doe` table rows where empty or honest placeholders belong.
- **`R-37` Design Direction Required**: Load `DESIGN.md` or existing project design tokens before building UI. If no direction exists and the user cannot be asked, label the output `"draft without direction"` with dials `ENERGY 1 / RHYTHM 1 / MOTION 1`.
- **`R-40` Performance Mechanisms**: Every `<img>`, `<video>`, and `<iframe>` must declare `width`/`height` or `aspect-ratio`; hero images must use `fetchpriority="high"` and never `loading="lazy"`; third-party scripts in `<head>` must not block rendering.

### Tier 2: Purpose-Gate (Allowed Only With Articulated Purpose & Dose Caps)
- **Gradients & Colors (`R-01`)**: No default blue-to-purple gradients or neon glows unless rooted in brand identity or hierarchy.
- **Icons & Illustrations (`R-04`, `R-22`)**: No generic sparkle/robot/orb icons or unrelated stock illustrations.
- **Typography (`R-06`)**: Choose typefaces for brand character and readability, not AI defaults.
- **Backgrounds, Arrows, Badges (`R-07`, `R-08`, `R-09`)**: No default blueprint grids, arrows on every button, or decorative `"AI Powered"` eyebrow pills duplicating the H1.
- **Glassmorphism, Shadows, Glow (`R-10`, `R-12`, `R-13`)**: Cap glassmorphism and focus glow to at most 1–2 focal elements; use shadows strictly for elevation hierarchy.
- **Feature Cards & Animations (`R-14`, `R-19`)**: Vary feature presentation by content weight; tie motion to UX purpose and the declared `MOTION` dial.

### Tier 3: Quality Locks & Liveliness Toolkit
- **Page Structure (`R-05`)**: Avoid monotonous AI landing/dashboard templates (`Hero + 3 cards`, forced 3-step `How It Works`, default 4-stat-card + chart + table shell) when content calls for a task-specific hierarchy.
- **Palette & Identity (`R-11`, `R-15`, `R-16`, `R-20`, `R-21`, `R-29`, `R-30`, `R-31`)**: Cap active palette to 2–3 core colors + 1 accent; write action-specific CTAs; ban empty AI marketing buzzwords (`Seamless`, `Revolutionary`, `Next-Gen`); never clone another product's identity unasked.
- **Three Liveliness Dials**:
  - `ENERGY` (`1 Calm` / `2 Balanced` / `3 Bold`)
  - `RHYTHM` (`1 Uniform` / `2 Consistent with breaks` / `3 Asymmetric/Varied`)
  - `MOTION` (`1 Hover only` / `2 Scroll/Transitions` / `3 Choreographed`)
