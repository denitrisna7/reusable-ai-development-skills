---
name: cross-browser-responsive-qa
description: "Verifies responsive reflow from 320px mobile to 1440px desktop, zero horizontal overflow, 44x44px touch targets, and zero text overlap. Use for responsive QA. Do not use for APIs."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-23"
  category: "Frontend and User Experience"
---

# Cross-Browser and Responsive QA

This skill verifies that user interfaces adapt cleanly across mobile, tablet/small-laptop, and desktop viewports and behave consistently across target browser engines (Chromium, Firefox, WebKit/Safari). It enforces the Anti-Slop mobile and layout resilience rules (`C-4`, `R-03`, `R-25`, `R-32`, `R-34`) and uses Playwright MCP (`browser_resize`, `browser_snapshot(boxes=true)`, `browser_emulate_media`, and multi-browser configurations) to catch horizontal overflow, clipped text, undersized touch targets, and engine-specific CSS/JS regressions.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Verifying responsive layout behavior across phone, tablet, small laptop, and desktop screen sizes after creating or modifying UI components or pages.
- Diagnosing or fixing mobile layout bugs: horizontal scroll leaks, text escaping containers, overlapping sticky headers/bottom bars, or broken mobile navigation drawers.
- Auditing touch target dimensions (`44x44px` minimum on mobile viewports per `R-03`), hover-only interaction traps, or mobile virtual keyboard occlusion.
- Testing cross-browser compatibility across Chromium, Firefox, and WebKit/Safari or selecting target browsers based on `browserslist` and audience requirements.

## 2. When Not to Use

Do not use this skill as the primary workflow for:
- Designing component hierarchies or initializing `shadcn/ui` primitives from scratch: start with `ui-ux-design-systems` (`SKILL-20`) first, then route here for verification.
- Deep WCAG 2.2 screen-reader ARIA semantics and contrast math: pair with `accessibility-engineering` (`SKILL-21`).
- Backend service, database, or CLI testing with no browser or viewport rendering: route to `backend-testing-tdd` (`SKILL-16`).

## 3. Scope and Objectives

Every cross-browser and responsive QA check must cover:
- **Target-Browser Selection**: Determine required browser engines (Chromium, Firefox, WebKit/Safari) and minimum versions from project configuration (`browserslist`, `.browserslistrc`, `package.json`, Playwright `projects`), product requirements, and user base.
- **Viewport Matrix Testing**: Verify layout integrity across the five canonical widths:
  - `320px x 568px` (Small mobile & WCAG 1.4.10 Reflow floor)
  - `375px x 812px` (Standard mobile phone)
  - `768px x 1024px` (Tablet portrait & intermediate breakpoint `600px-1024px`)
  - `1024px x 768px` (Tablet landscape / small laptop)
  - `1440px x 900px` (Standard desktop)
- **True Responsive Reflow (`R-03`)**: Ensure layouts genuinely adapt across breakpoints (e.g., multi-column grids collapsing cleanly, desktop navigation transitioning to an accessible mobile drawer or bottom bar, data tables scrolling inside a bounded container or adapting layout) rather than squeezing a desktop layout into a narrow screen.
- **Touch & Keyboard Interaction (`R-03`, `R-32`)**: Enforce `>= 44x44px` tap targets with `>= 8px` spacing between adjacent controls on touch viewports; provide tap/focus equivalents for all hover-dependent UI (tooltips, action menus, card overlays); ensure mobile virtual keyboards do not obscure active inputs or submit buttons.
- **Layout Regression Detection**: Eliminate unintended document-level horizontal scrolling (`document.documentElement.scrollWidth > document.documentElement.clientWidth`), text clipped by fixed heights + `overflow: hidden`, broken flex/grid wrapping (`min-w-0` missing on flex children), and sticky headers/bottom navs covering page content or focused controls (`WCAG 2.4.11`).
- **Browser-Specific Failure Prevention**: Check for WebKit/Safari, Firefox, and mobile browser differences including `100dvh` vs. `100vh` mobile address-bar collapse, iOS Safari auto-zoom on `<input>` with `font-size < 16px`, date/time input formatting, flexbox/grid intrinsic sizing, `backdrop-filter` prefixes, and smooth-scroll / scrollbar gutter behavior.

## 4. Prerequisites and Context Requirements

Before executing cross-browser and responsive QA, inspect:
1. **Browser & Viewport Configuration**: `package.json` (`browserslist`), `playwright.config.*` (`projects` for `chromium`, `firefox`, `webkit`, mobile device descriptors), PostCSS/Autoprefixer/LightningCSS config, and Tailwind/CSS breakpoints.
2. **Target Routes & Interactive States**: All modified pages, including open mobile menus, active modals/drawers, populated data tables, and validation error states.
3. **Playwright MCP Reference**: Read [../../references/playwright-mcp-reference.md](../../references/playwright-mcp-reference.md) for `browser_resize`, `browser_snapshot(boxes=true)`, and `browser_emulate_media`.

## 5. Step-by-Step Workflow

### Step 1: Determine Target Browsers and Breakpoints
- [ ] Inspect `package.json`, `.browserslistrc`, and `playwright.config.*` to identify supported browser engines and breakpoint definitions (`sm: 640px`, `md: 768px`, `lg: 1024px`, `xl: 1280px`).
- [ ] Identify all views and states affected by the task (including empty, loading, error, and populated states, plus open navigation drawers and modals).

### Step 2: Audit CSS and Markup for Known Cross-Browser & Mobile Traps
- [ ] **Viewport Meta Tag**: Confirm `<meta name="viewport" content="width=device-width, initial-scale=1">` is present and does **not** restrict zooming (`maximum-scale=1` and `user-scalable=no` are forbidden per `WCAG 1.4.4`).
- [ ] **Dynamic Viewport Height**: Replace full-screen `100vh` locks on mobile layouts with `min-h-dvh` (`100dvh` with `100vh` fallback) so mobile browser toolbars do not clip bottom actions.
- [ ] **iOS Safari Input Auto-Zoom**: Ensure all `<input>`, `<select>`, and `<textarea>` elements render with `font-size >= 16px` (`1rem`) on mobile viewports (`text-base sm:text-sm` in Tailwind) to prevent iOS Safari from unexpectedly zooming the viewport on focus.
- [ ] **Flex/Grid Overflow Containment**: Verify flex and grid children containing text, URLs, or code blocks include `min-w-0` and `break-words` / `truncate`, and wrap wide tables or code blocks in `overflow-x-auto` containers so they never expand the page body.
- [ ] **Safe Area Insets**: On edge-to-edge mobile web or hybrid views with fixed bottom bars, account for `env(safe-area-inset-bottom)`.

### Step 3: Execute Viewport Matrix Verification (`320px` to `1440px`)
When a live server and Playwright MCP are available:
- [ ] Navigate to the target URL (`browser_navigate`) and verify zero console/network errors (`browser_console_messages`, `browser_network_requests`).
- [ ] Resize sequentially across the viewport matrix using `browser_resize`:
  1. `width: 320, height: 568` (Minimum reflow check)
  2. `width: 375, height: 812` (Mobile phone check)
  3. `width: 768, height: 1024` (Tablet portrait / `600-1024px` intermediate layout check)
  4. `width: 1024, height: 768` (Small laptop / tablet landscape check)
  5. `width: 1440, height: 900` (Desktop check)
- [ ] At each viewport, run `browser_snapshot(boxes=true)` to inspect element bounding boxes `[box=x,y,width,height]`:
  - Verify no element's `x + width` exceeds the viewport width (unless inside an intentional horizontal scroll container).
  - On `320px` and `375px`, verify interactive controls have `width >= 44` and `height >= 44` (or an equivalent hit area) and do not overlap (`R-03`).
  - Take targeted screenshots (`browser_take_screenshot`) only when visual evidence of layout reflow or a discovered defect is needed.

### Step 4: Verify Touch, Hover-Alternative, Keyboard, and Theme Behavior
- [ ] **Mobile Navigation & Drawers**: At `375px`, open the mobile navigation menu or filter drawer (`browser_click`), verify all links are reachable, and verify closing works via both the close button and `Escape` (`browser_press_key`).
- [ ] **Hover-Only Feature Check**: Confirm that any action revealed on `:hover` on desktop (e.g., row actions, delete buttons, info tooltips) is either visible by default on touch devices (`@media (hover: none)`) or reachable via tap/focus.
- [ ] **Theme & Media Emulation (`R-34`)**: Use `browser_emulate_media` to test `colorScheme: "dark"` and `reducedMotion: "reduce"` across mobile and desktop widths.

### Step 5: Verify Multi-Browser Engine Compatibility
- [ ] If automated Playwright suites are configured (`npx playwright test`), run across configured browser projects (`--project=chromium`, `--project=firefox`, `--project=webkit`) when browsers are installed in the environment.
- [ ] Check for CSS feature compatibility against target browsers (e.g., CSS Subgrid, `@container` queries, `:has()`, `scrollbar-gutter`, `backdrop-filter`) and provide fallbacks where required.

## 6. Technology-Specific Adaptation Rules

| Stack / Ecosystem | Responsive & Cross-Browser Adaptation | Verification & Tooling |
| :--- | :--- | :--- |
| **Tailwind CSS (React / Vue / Blade / Nuxt / Next.js)** | Design mobile-first (`base` styles for `< 640px`, then `sm:`, `md:`, `lg:`, `xl:`). Use `text-base sm:text-sm` on inputs, `min-h-dvh`, `min-w-0` on flex items, and `overflow-x-auto` on tables. | Playwright MCP (`browser_resize`, `browser_snapshot(boxes=true)`), Playwright Test (`chromium`, `firefox`, `webkit`). |
| **CSS Modules / Vanilla CSS / SCSS** | Use fluid typography/spacing (`clamp()`), CSS Grid `repeat(auto-fit, minmax(min(100%, 280px), 1fr))` to avoid horizontal overflow below `280px`, and `@media (hover: hover)` guards. | Stylelint, Autoprefixer / LightningCSS with `browserslist`, Playwright MCP. |
| **Server-Rendered Apps (Laravel / CodeIgniter / Django / Rails)** | Test server-rendered pagination controls, flash banners, and validation error summaries at `320px` and `375px` to ensure error banners do not push form actions offscreen. | Playwright MCP or Cypress/Dusk responsive viewport tests. |
| **Java / Spring, C# / .NET, Go, Rust Web Templates** | Ensure responsive table wrappers, form grids, and navigation headers degrade gracefully when JavaScript is delayed or disabled, and verify viewport meta tags in base layout templates. | Playwright MCP viewport matrix and multi-browser verification. |
| **Flutter (Mobile / Tablet / Web / Desktop)** | Use `MediaQuery.sizeOf(context)` and `LayoutBuilder` (avoid hardcoded phone widths); switch between `NavigationBar` (`< 600dp`), `NavigationRail` (`600-840dp`), and `NavigationDrawer` (`>= 840dp`); wrap scrollable forms in `SingleChildScrollView` with `viewInsets.bottom` padding for on-screen keyboards. | `flutter test` with `tester.view.physicalSize` across phone, foldable, and tablet sizes. |

### High-Risk Cross-Browser & Mobile Defect Patterns

- **Horizontal Scroll Leak (`scrollWidth > clientWidth`)**:
  - *Typical Cause*: `width: 100vw` when a vertical scrollbar is present, negative horizontal margins (`-mx-4`) outside a padded container, or unbroken long strings inside flex/grid items lacking `min-w-0`.
  - *Remediation*: Replace `100vw` with `100%`, add `min-w-0` and `overflow-wrap: anywhere` / `break-words` to flex/grid children, and wrap wide data tables in `overflow-x-auto`.
- **Sticky Bar Occlusion**:
  - *Typical Cause*: Fixed bottom action bar or sticky top navbar covers the bottom of forms or obscures elements jumped to via keyboard `Tab` or `#hash` links.
  - *Remediation*: Add bottom padding matching the fixed bar height (`pb-20` + `env(safe-area-inset-bottom)`) and set `scroll-padding-top` / `scroll-padding-bottom` on `html`.
- **Safari / WebKit Specific Regressions**:
  - *Typical Cause*: `<input>` with `font-size: 14px` triggers automatic page zoom on iOS; `100vh` clips bottom controls under the dynamic URL bar; `backdrop-filter` missing `-webkit-backdrop-filter` in older WebKit builds; flex items with `<img>` children stretching aspect ratios when `align-items: stretch` is default.
  - *Remediation*: Use `16px` (`1rem`) minimum font size on mobile inputs, `100dvh`, and `align-self: flex-start` or explicit `aspect-ratio` on flex image children.

## 7. Security and Safety Considerations

- **Safe Browser QA Target**: Never run automated browser interactions against production environments with real user accounts or live payment/mutation endpoints. Verify the target URL is a local development server (`localhost`, `127.0.0.1`) or an isolated test environment.
- **Avoid `browser_run_code_unsafe`**: Rely on declarative Playwright MCP tools (`browser_resize`, `browser_snapshot`, `browser_click`, `browser_emulate_media`) rather than executing arbitrary JavaScript strings.
- **Clickjacking & Z-Index Overlays**: Ensure fixed/sticky overlays, cookie banners, or invisible full-screen containers (`pointer-events: none` missing) do not intercept clicks intended for underlying security or confirmation controls.

## 8. Verification Criteria

Before marking cross-browser and responsive QA as `PASS`:
1. **Viewport Matrix Evidence**: All five canonical widths (`320px`, `375px`, `768px`, `1024px`, `1440px`) have been checked with zero unintended horizontal overflow and zero clipped or overlapping text.
2. **Touch & Interaction Evidence (`R-03`)**: Interactive controls on mobile viewports meet `>= 44x44px` tap target dimensions (or documented WCAG 2.5.8 `24x24px` floor with spacing) and hover-only actions have tap/keyboard equivalents.
3. **Browser Engine Coverage**: Every browser engine actually tested (`Chromium`, `Firefox`, `WebKit`) is explicitly recorded, and any browser engine not installed in the environment is honestly reported as `NOT TESTED` or `BLOCKED`.

## 9. Failure Handling and Edge Cases

- **Missing Browser Binaries in Container/CI**: If Firefox or WebKit binaries are not installed in the sandboxed environment, execute full viewport matrix verification in the available browser (e.g., Chromium), perform static CSS compatibility checks for WebKit/Firefox (`font-size >= 16px` on inputs, `-webkit-backdrop-filter`, `dvh` fallback), and record WebKit/Firefox runtime execution as `BLOCKED (browser binary not installed)`.
- **Intermediate Tablet / Small-Laptop Breakpoint (`600px-1024px`)**: Many layouts only test `375px` and `1440px` and break at `768px` or `900px` (e.g., sidebar + 3-column grid cramping cards to `120px` wide). Always inspect `768px` and `1024px` explicitly (`R-03`).
- **Sticky Header + Anchor Navigation**: Jumping to `#section-id` or tabbing backward often hides headings under a sticky header; fix with `scroll-margin-top` / `scroll-padding-top`.

## 10. Expected Outputs and Reporting Requirements

Report responsive and cross-browser QA results using this template:

```markdown
## Cross-Browser & Responsive QA Report

### 1. Target Scope
- **Routes / Views Tested**: [List of URLs or components]
- **Target Browser Matrix**: [Chromium / Firefox / WebKit - specify which were executed live vs. static check]

### 2. Viewport Matrix Results
| Viewport (`WxH`) | Device Class | Horizontal Overflow | Tap Targets (`>=44x44px`) | Layout Reflow & Sticky Bars | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `320 x 568` | Small Phone (Reflow) | [0px / Details] | [PASS / FAIL] | [Details] | [PASS/FAIL/NOT TESTED] |
| `375 x 812` | Mobile Phone | [0px / Details] | [PASS / FAIL] | [Details] | [PASS/FAIL/NOT TESTED] |
| `768 x 1024` | Tablet Portrait | [0px / Details] | [PASS / FAIL] | [Details] | [PASS/FAIL/NOT TESTED] |
| `1024 x 768` | Small Laptop / Tablet | [0px / Details] | [N/A or PASS] | [Details] | [PASS/FAIL/NOT TESTED] |
| `1440 x 900` | Desktop | [0px / Details] | [N/A or PASS] | [Details] | [PASS/FAIL/NOT TESTED] |

### 3. Cross-Browser & Interaction Checks
- **Mobile Navigation / Drawers / Modals**: [Status & evidence]
- **Hover-Alternative & Keyboard Focus (`WCAG 2.4.11`)**: [Status & evidence]
- **iOS Safari / WebKit Checks (`16px` inputs, `dvh`, safe-area)**: [Status & evidence]
- **Dark Mode & Reduced Motion (`R-34`, `R-39`)**: [Status & evidence]
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - `ui-ux-design-systems` (`SKILL-20`): Produces the responsive component layouts to be verified.
  - `accessibility-engineering` (`SKILL-21`): Defines the `320px` reflow (`WCAG 1.4.10`), focus not obscured (`WCAG 2.4.11`), and target size (`WCAG 2.5.8` / `R-03`) requirements.
- **Downstream / Co-Activated Skills**:
  - `playwright-mcp-browser-qa` (`SKILL-17`): Provides the underlying browser automation toolset (`browser_resize`, `browser_snapshot`).
  - `test-reporting-failure-diagnosis` (`SKILL-19`): Formats any discovered visual or browser-specific regressions into actionable defect reports.

## 12. Source References

- **Playwright MCP Official Documentation**: https://playwright.dev/docs/getting-started-mcp
- **Anti-Slop Mobile & Layout Rules (`antislop-layoutmobile`)**: https://github.com/miqdadbadjuber/anti-slop (MIT License)
- **WCAG 2.2 Understanding 1.4.10 Reflow**: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- **Shared Library Reference (Playwright MCP Browser QA)**: [../../references/playwright-mcp-reference.md](../../references/playwright-mcp-reference.md)
- **Shared Library Reference (Anti-Slop Engineering `R-03`, `R-34`)**: [../../references/anti-slop-engineering-reference.md](../../references/anti-slop-engineering-reference.md)
