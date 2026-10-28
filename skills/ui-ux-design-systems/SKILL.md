---
name: ui-ux-design-systems
description: "Designs, implements, and audits user interface components, design tokens, forms, tables, dialogs, navigation, and view states while respecting the existing UI stack. Activate when building, styling, or refactoring frontend screens, component libraries, or design systems, including shadcn/ui when compatible. Do not use for backend APIs, low-level WCAG audits (use accessibility-engineering), or runtime bundle profiling (use frontend-performance)."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-20"
  category: "Frontend and User Experience"
---

# UI/UX Engineering & Design Systems

This skill governs user interface engineering, reusable component design, semantic design tokens, layout hierarchy, interactive forms, data tables, dialogs, navigation, and four-state view completeness across frontend and server-rendered stacks. It enforces strict stack compatibility (using `shadcn/ui` only when the project uses React + Tailwind CSS without a conflicting UI framework) and applies the Anti-Slop craftsmanship rules (`C-1` through `C-5`, `R-01` through `R-40`) to eliminate generic template bloat.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Designing, building, refactoring, or reviewing user interfaces, dashboards, forms, data tables, modals/dialogs, or navigation layouts.
- Creating or extending a reusable component library, token system (colors, typography, spacing, elevation, radius), or theme (light/dark mode).
- Integrating or customizing `shadcn/ui` components in a compatible React + Tailwind CSS codebase.
- Auditing screens for missing loading, empty, error, or populated view states (`R-27`), or removing generic AI UI anti-patterns (`C-1` to `C-5`).

## 2. When Not to Use

Do not use this skill as the primary workflow for:
- Deep WCAG 2.2 compliance auditing, screen-reader tree verification, or mathematical contrast validation: route to `accessibility-engineering` (`SKILL-21`).
- Bundle size reduction, Core Web Vitals (LCP, INP, CLS) profiling, or network caching: route to `frontend-performance` (`SKILL-22`).
- Multi-browser matrix verification and viewport resize testing: route to `cross-browser-responsive-qa` (`SKILL-23`) and `playwright-mcp-browser-qa` (`SKILL-17`).
- Purely backend services, CLI utilities, database migrations, or headless API endpoints without a visual user interface.

## 3. Scope and Objectives

Every UI/UX implementation or review under this skill must cover:
- **Existing Design System Integration & Compatibility Gate**: Detect the active UI framework, styling system, and component primitives before writing code. Apply `shadcn/ui` only when compatible with the actual project.
- **Design Tokens & Theme Completeness (`R-34`, `R-37`)**: Centralize colors, typography scales, spacing, border radii, and shadows in design tokens (CSS custom properties, Tailwind config, or platform theme files). Ensure both light and dark modes pass contrast and visual hierarchy checks when a theme toggle exists.
- **Intentional Visual Hierarchy & Anti-Slop Craftsmanship (`C-1` to `C-5`)**: Set explicit Liveliness Dials (`ENERGY`, `RHYTHM`, `MOTION`) grounded in `DESIGN.md` or existing product identity. Avoid unmotivated blue-to-purple gradients (`R-01`), generic 3-card feature rows (`R-05`), decorative sparkle/robot icons (`R-04`), and fabricated social proof or metrics (`R-17`, `R-18`).
- **Reusable Component Architecture**: Build composable, single-responsibility UI primitives with explicit prop contracts, predictable variant handling, and zero leaked layout margins.
- **Layout Consistency & Responsive Structure (`R-03`)**: Maintain consistent page shells, container max-widths, grid/flex gaps, and responsive reflow across mobile, tablet/small-laptop (`600px-1024px`), and desktop breakpoints.
- **Forms & Validation (`R-39`)**: Provide programmatic `<label>` associations, inline helper text, field-level and summary validation errors, input preservation on failure, and double-submit protection during async requests.
- **Tables & Data Views**: Build domain-specific tables with semantic headers (`<th scope="col">`), clear sort/filter indicators, pagination, and responsive horizontal containment.
- **Dialogs, Drawers, & Navigation (`R-24`, `R-26`)**: Ensure every navigation item points to a real route and every dialog, drawer, or popover traps focus cleanly, supports `Escape` dismissal, and restores focus to its trigger.
- **Complete View States (`R-27`)**: Implement explicit **Loading**, **Empty** (distinguishing first-use vs. zero-filter matches), **Error** (with actionable retry), and **Success/Populated** states for every data-driven screen.
- **Avoiding Unnecessary UI Complexity**: Reject over-engineered state stores, nested modal-in-modal flows, and decorative chrome that distracts from the primary user task.

## 4. Prerequisites and Context Requirements

Before modifying or creating UI code, gather:
1. **Stack & Styling Manifest**: `package.json`, `composer.json`, `pubspec.yaml`, Tailwind configuration (`tailwind.config.*` or Tailwind v4 `@theme` CSS), `components.json` (if present), and global stylesheets (`globals.css`, `app.css`).
2. **Design Direction (`R-37`)**: Existing `DESIGN.md`, brand guidelines, Figma tokens, or established screens in the repository.
3. **Target User Task & Domain Model**: The real domain entities, fields, actions, and edge cases the screen must serve.

## 5. Step-by-Step Workflow

### Step 1: Run the Stack & Design System Discovery Gate
- [ ] Inspect the repository to identify the templating engine or frontend framework, CSS system, icon library, and existing shared components (e.g., `src/components/ui/`, `resources/views/components/`, `lib/widgets/`).
- [ ] Evaluate the **shadcn/ui Compatibility Gate** using [../../references/shadcn-ui-design-system-reference.md](../../references/shadcn-ui-design-system-reference.md) and [references/shadcn-ui-patterns.md](references/shadcn-ui-patterns.md):
  - If `components.json` is present in a React project, use the project's configured `shadcn/ui` aliases, headless primitive library (Radix UI or Base UI), and token conventions.
  - If the project uses Vue, Angular, Svelte, Laravel Blade, CodeIgniter views, Django templates, Material UI, Chakra UI, Mantine, Bootstrap, or Flutter, **do not** introduce `shadcn/ui`. Use the project's native component system.

### Step 2: Establish Design Direction, Tokens, and Liveliness Dials
- [ ] Read `DESIGN.md` or sample 2-3 existing production screens to extract color tokens, typography hierarchy, border radius, and spacing rhythm.
- [ ] If no design direction exists in a greenfield project and the user cannot be consulted, mark the UI plan as `"draft without direction"` and default to conservative dials: `ENERGY 1 (Calm)`, `RHYTHM 1 (Uniform)`, `MOTION 1 (Hover only)` (`R-37`).
- [ ] Map all colors to semantic token names (`background`, `foreground`, `primary`, `muted`, `border`, `destructive`) rather than raw hex codes or hardcoded utility palette classes.

### Step 3: Architect Layout Hierarchy and Component Boundaries
- [ ] Identify the single primary user decision or task on the screen (`C-3`) and structure the visual hierarchy around it (1 primary focal area, clear section groupings, max 3-4 distinct data points per card).
- [ ] Reuse existing project components before creating new ones. When a new reusable component is needed, separate layout positioning (owned by the parent container via `gap` or grid placement) from internal padding and visual variants (owned by the component).
- [ ] Enforce consistent spacing scales (`4px` / `0.25rem` base unit: `4, 8, 12, 16, 24, 32, 48, 64px`) and border-radius hierarchy (nested elements must use a smaller or equal radius compared to their parent container).
- [ ] Verify that every button, link, tab, filter, and menu item is wired to real application behavior (`C-2`, `R-24`, `R-26`). Never render dead action icons or `href="#"` links.
- [ ] Avoid modal overload: use inline editing or disclosure panels for simple secondary inputs, reserving modal dialogs for focused sub-tasks or destructive confirmations.

### Step 4: Implement Forms, Tables, Dialogs, and All Four View States (`R-27`)
- [ ] **Loading State**: Add layout-matched skeletons or progress indicators with `aria-busy="true"` so dimensions do not jump when data arrives.
- [ ] **Empty State**: Provide specific copy explaining why the view is empty and render a direct action button (e.g., `"New Project"` or `"Clear search filters"`).
- [ ] **Error State**: Display user-safe error feedback explaining what failed and offering a recovery button (`"Retry"`), while logging technical details safely.
- [ ] **Populated / Success State**: Provide immediate visual confirmation (toast notification with `role="status"` or inline banner) after mutations, updating optimistic or re-fetched state cleanly.
- [ ] **Forms**: Bind `<label>` elements, client/server validation messages (`aria-invalid`, `aria-describedby`), sensible input types/`autocomplete` values, and pending submit locks. Preserve all user-entered field values when server-side validation fails.
- [ ] **Tables & Dialogs**: Use semantic table markup with real domain columns, right-align numeric/currency columns with `tabular-nums`, and ensure dialogs include accessible titles/descriptions, keyboard Escape support, and explicit confirmation for destructive actions.

### Step 5: Apply the Anti-Slop Visual & Copy Audit
- [ ] Replace generic marketing filler (`"Seamless"`, `"Next-Gen"`, `"Revolutionary"`, `"Supercharge"`) with concrete functional copy.
- [ ] Remove unapproved em dashes in UI labels and prose (`R-02`), fake metric badges (`R-17`), and stock placeholder names (`John Doe`, `Acme Corp`) in production templates (`R-38`).
- [ ] Pair with `accessibility-engineering` (`SKILL-21`) and `cross-browser-responsive-qa` (`SKILL-23`) to verify contrast, keyboard focus rings, and responsive breakpoints.

## 6. Technology-Specific Adaptation Rules

| Stack / Ecosystem | UI & Design System Adaptation | Tooling & Prohibited Mismatches |
| :--- | :--- | :--- |
| **React / Next.js / Vite / Remix / Inertia React** | If `components.json` or Tailwind is used without a competing library, follow [references/shadcn-ui-patterns.md](references/shadcn-ui-patterns.md). If MUI, Mantine, Chakra, or AntD is installed, use its native `ThemeProvider` and components. | Never install `shadcn/ui` over an existing MUI/Chakra/AntD setup. Never strip Radix/Base UI accessibility attributes. |
| **Vue / Nuxt / Svelte / Angular** | Use the active component library (`Nuxt UI`, `PrimeVue`, `Vuetify`, `shadcn-vue` if already installed, `Angular Material`, `bits-ui`). Manage tokens via CSS variables and scoped styles. | Never copy React JSX `shadcn/ui` primitives into Vue/Svelte/Angular projects. |
| **PHP (Laravel Blade / Livewire / CodeIgniter)** | Use Anonymous/Class Blade Components (`<x-button>`, `<x-modal>`), Livewire wire:loading states, or CodeIgniter view partials/cells with the project's CSS stack (Tailwind, Bootstrap, or vanilla CSS). | Never assume React or `shadcn/ui` in Blade or CodeIgniter views. Do not force PHPStan/Pint onto frontend-only tasks unless PHP view classes are modified. |
| **Python (Django / FastAPI / Flask + Jinja2 / HTMX)** | Use template inheritance (`{% extends %}`, `{% include %}`), template partials for HTMX swaps (`hx-target`, `hx-indicator` for loading states), and CSS custom properties. | Do not introduce a Node/React build pipeline into a server-rendered Python template app unless requested. |
| **Go / Java / C# / Rust Server Templates** | Use `html/template`/`templ` (Go), Thymeleaf/JTE (Java), Razor/Blazor (C#), or Askama/Maud (Rust) with modular partials and semantic HTML/CSS tokens. | Respect existing asset bundling and static file serving conventions. |
| **Mobile & Native (Flutter / iOS / Android)** | In Flutter, use `ThemeData`, `ColorScheme.fromSeed`, `ThemeExtension`, and Material 3 / Cupertino widgets. Use `LayoutBuilder` and `Sliver` lists for responsive states. | Never apply web CSS/HTML or `shadcn/ui` concepts to native mobile widget trees. |

## 7. Security and Safety Considerations

- **XSS Prevention in UI Rendering**: Always rely on framework auto-escaping (`{variable}`, `{{ $variable }}`). Never use `dangerouslySetInnerHTML`, `v-html`, `{!! $raw !!}`, or `|safe` on untrusted user content without an allowlist HTML sanitizer (such as DOMPurify or server-side HTMLPurifier).
- **Safe External Links**: Any link opening a new tab (`target="_blank"`) to an external origin must include `rel="noopener noreferrer"`.
- **Sensitive Data Masking & Error Hygiene**: Mask sensitive tokens/keys by default with an explicit reveal toggle, disable autocomplete on one-time secrets where appropriate, and never render raw database exceptions or stack traces inside UI error states.
- **Client vs. Server Authorization**: Hiding a button or navigation link in the UI is a UX convenience, never an access control boundary. Every protected route and mutation must enforce authorization server-side (coordinate with `application-security-owasp`, `SKILL-10`).

## 8. Verification Criteria

Before declaring any UI/UX task complete, verify with concrete evidence:
1. **Build & Type Check**: The project compiles and type-checks cleanly (`tsc --noEmit`, `npm run build`, `vite build`, `flutter analyze`, or template compilation) with zero unresolved imports or missing components.
2. **Four-State Verification (`R-27`)**: Loading, Empty, Error, and Populated states are implemented and verified in code (and in browser via `playwright-mcp-browser-qa` when a live server is available).
3. **Interactive Completeness (`C-2`, `R-24`, `R-26`)**: Every visible interactive element has a bound handler or valid destination route; zero console errors occur during interaction.
4. **Token & Theme Hygiene (`R-34`)**: Semantic tokens are used consistently; if dark mode is supported, no unreadable hardcoded dark-on-dark or light-on-light text exists.

## 9. Failure Handling and Edge Cases

- **Missing Subcomponents or Icons**: If a `shadcn/ui` component imports a missing primitive (`@radix-ui/*` or `lucide-react`), inspect `package.json` and install or generate the component via the project's package manager rather than leaving broken imports.
- **Extreme Content Lengths**: Test layouts against long unbroken strings (URLs, emails, UUIDs), multi-line titles, and zero/huge numeric values using `truncate`, `line-clamp-*`, `break-words`, or `min-w-0` inside flex/grid children so containers do not blow out horizontally.
- **No Live Browser Environment**: If the runtime environment cannot launch a dev server or browser, verify component structure, props, tokens, and build output statically, and explicitly record `"Visual browser rendering: NOT TESTED (environment limitation)"` in the report.

## 10. Expected Outputs and Reporting Requirements

Provide a structured summary using the following template:

```markdown
## UI/UX & Design System Report

### 1. Stack & Design System Detection
- **Detected UI Stack**: [e.g., Next.js + Tailwind CSS + shadcn/ui (Radix) / Laravel Blade + Alpine.js / Flutter Material 3]
- **shadcn/ui Compatibility Gate**: [APPLICABLE / NOT APPLICABLE - Reason]
- **Design Direction & Liveliness Dials**: [Source: DESIGN.md / Existing Repo | ENERGY: X, RHYTHM: X, MOTION: X]

### 2. Components & Tokens Implemented or Modified
- **Design Tokens**: [Summary of semantic color, spacing, or typography tokens used/updated]
- **Components & Views**: [List of file paths created or updated]
- **View States Covered (`R-27`)**:
  - Loading: [Implemented / Verified]
  - Empty: [Implemented / Verified]
  - Error: [Implemented / Verified]
  - Populated: [Implemented / Verified]

### 3. Verification Summary
| Check | Status (PASS / FAIL / BLOCKED / NOT TESTED) | Evidence |
| :--- | :--- | :--- |
| Build / Type Check | [Status] | [Command & output] |
| Interactive Controls & Navigation (`C-2`, `R-24`, `R-26`) | [Status] | [Verification details] |
| Four View States (`R-27`) | [Status] | [Verification details] |
| Anti-Slop Visual & Copy Gate (`R-01`..`R-40`) | [Status] | [Verification details] |

### 4. Residual Risks & Follow-Up Routing
- [Any follow-up checks routed to `accessibility-engineering` or `cross-browser-responsive-qa`]
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - `project-discovery-context` (`SKILL-01`): Identifies the active frontend framework, CSS tooling, and `components.json`.
  - `requirements-acceptance-criteria` (`SKILL-02`): Defines the user journeys and state requirements.
  - `ai-anti-slop-craftsmanship` (`SKILL-05`): Supplies the `C-1` to `C-5` craftsmanship rules and copy hygiene constraints.
- **Downstream / Co-Activated Skills**:
  - `accessibility-engineering` (`SKILL-21`): Must be paired when creating or modifying interactive components, forms, dialogs, or color tokens.
  - `frontend-performance` (`SKILL-22`): Ensures new assets, images, and client components meet LCP, INP, and CLS targets.
  - `cross-browser-responsive-qa` (`SKILL-23`) and `playwright-mcp-browser-qa` (`SKILL-17`): Verifies layout reflow and interactive behavior across viewports.

## 12. Source References

- **shadcn/ui Official Documentation**: https://ui.shadcn.com/docs
- **Anti-Slop UI Craftsmanship (`antislop-ui`)**: https://github.com/miqdadbadjuber/anti-slop (MIT License)
- **Local Skill Reference (shadcn/ui Patterns)**: [references/shadcn-ui-patterns.md](references/shadcn-ui-patterns.md)
- **Shared Library Reference (Design Systems & shadcn/ui)**: [../../references/shadcn-ui-design-system-reference.md](../../references/shadcn-ui-design-system-reference.md)
- **Shared Library Reference (Anti-Slop Engineering)**: [../../references/anti-slop-engineering-reference.md](../../references/anti-slop-engineering-reference.md)
