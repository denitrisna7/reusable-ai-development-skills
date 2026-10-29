---
name: playwright-mcp-browser-qa
description: "Executes evidence-based interactive browser QA using Playwright MCP accessibility snapshots, semantic locators, network inspection, and console diagnostics. Activate when verifying web UI flows, forms, navigation, auth states, negative validation, and regressions in a real browser without routine screenshot spam. Do not use for non-web CLI/API projects or static linting."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-17"
  category: "Testing and Quality Assurance"
---

# Playwright MCP Browser QA

This skill defines an evidence-based browser quality assurance workflow powered by Playwright MCP (`https://playwright.dev/docs/getting-started-mcp`). It prioritizes deterministic accessibility tree snapshots (`browser_snapshot`, `browser_find`), semantic element `ref` targeting, network request inspection (`browser_network_requests`), and console error auditing (`browser_console_messages`) over token-heavy screenshot spam, and strictly forbids claiming `PASS` merely because a page loads.

## 1. Activation Conditions

Activate this skill when the task involves any of the following scenarios:
- Verifying a newly implemented or modified web UI page, component, form, modal, table, or multi-step workflow in a real browser.
- Executing functional end-to-end (E2E) QA across authentication, role-based authorization redirects, CRUD operations, search/filter controls, and client-server state synchronization.
- Auditing browser console logs (`browser_console_messages`) and XHR/Fetch API calls (`browser_network_requests`, `browser_network_request`) during interactive user flows.
- Performing negative browser testing (empty/malformed form validation, unauthorized URL access, mocked `4xx`/`5xx`/offline network responses via `browser_route`).
- Verifying keyboard navigation (`Tab`, `Enter`, `Escape`), accessible role/name semantics, responsive viewports (`browser_resize`), or dark/reduced-motion media emulation (`browser_emulate_media`).

## 2. When Not to Use

Do not use this skill as the primary workflow for the following tasks:
- Projects with no web/HTML interface (pure CLI tools, background workers, native mobile apps, or headless REST/gRPC microservices): route to `backend-testing-tdd` (`SKILL-16`).
- Designing the high-level project test pyramid before execution: start with `testing-strategy-design` (`SKILL-15`).
- Deep WCAG 2.2 AA design/code remediation before browser testing: coordinate with `accessibility-engineering` (`SKILL-21`).
- Static code linting or type checking: route to `code-quality-static-analysis` (`SKILL-07`).

## 3. Scope and Objectives

Every browser QA session conducted with this skill must uphold the following engineering standards and cover all applicable areas:
- **Accessibility Snapshots Over Routine Screenshots**: Use `browser_snapshot` and `browser_find` as the primary mechanism to inspect DOM state, verify text/roles, and obtain element `ref` identifiers (`[ref=e12]`). Capture screenshots (`browser_take_screenshot`) **only** when visual layout, CSS overlap, contrast, or visual defect evidence is genuinely required.
- **Page Load Never Equals `PASS`**: Never mark a test or feature `PASS` simply because `browser_navigate` succeeded or the initial page rendered. Exercise the actual interactive behavior and verify state changes.
- **Semantic Locators & Element `ref` Targeting**: Target elements using exact `ref` identifiers from the latest `browser_snapshot` / `browser_find` output alongside descriptive `element` labels.
- **Functional Browser Tests & Form Validation**: Test both positive submissions (`browser_fill_form`, `browser_type`, `browser_select_option`, `browser_click`) and negative validation states (required fields, invalid formats, boundary lengths, duplicate entries).
- **Navigation & History Resilience**: Verify internal link navigation, dynamic route params, query string filters, and browser back-button behavior (`browser_navigate_back`).
- **Authentication, Session & Authorization Verification**: Verify login, logout, protected-route redirects for unauthenticated users, role-based access denial for unauthorized users, and cookie security attributes (`browser_cookie_list` / `browser_storage_state` when storage capability is enabled).
- **Network Requests & API Contract Verification**: Inspect `browser_network_requests` and `browser_network_request` after user actions to confirm expected API calls fired, returned `2xx` (or expected `4xx` on negative tests), and did not trigger hidden `500` errors or infinite polling loops.
- **Console & Runtime Error Diagnostics**: Inspect `browser_console_messages` after every navigation and interaction to catch uncaught `TypeError`/`ReferenceError` exceptions, React/Vue hydration mismatches, CSP violations, or failed asset loads.
- **Negative & Regression Testing**: Test rapid double-clicks on submit buttons, Escape/backdrop dismissal on modals, empty states, and simulated upstream API errors (`browser_route` when network capability is active).
- **Evidence-Based Reporting**: Record every verified step with concrete snapshot, network status, and console evidence using strict `PASS` / `FAIL` / `BLOCKED` / `NOT TESTED` statuses.

## 4. Prerequisites and Context Requirements

Before starting a Playwright MCP browser session, verify:
1. **Target Application Server & Safe Environment**: Confirm the local or staging web server is running (or start it in a background task if authorized) and verify the target URL is a safe test/local host (`localhost`, `127.0.0.1`, `.test`, or isolated staging), **never** a live production system with real customer transactions (`SKILL-18`).
2. **Playwright MCP Availability & Strict Anti-Hallucination Lock**: Check whether Playwright MCP tools (`browser_navigate`, `browser_snapshot`, `browser_click`, etc.) are registered in the current agent environment. If Playwright MCP tools are NOT available or the local web server is NOT running, the agent MUST immediately report: `[BROWSER QA BLOCKED: Playwright MCP tools not registered or local server not running]`. The agent is STRICTLY FORBIDDEN from simulating, assuming, or claiming `PASS` for any browser test without calling real browser MCP tools.
3. **Test Accounts & Seeded Data**: Identify valid test credentials or storage states for each required user role (guest, standard user, admin, second tenant user).

## 5. Step-by-Step Workflow

Follow this numbered procedure during every Playwright MCP QA session. The agent MUST stream every step progressively in the chat response (displaying navigation status, snapshot element counts, mobile resize results, and console error counts) so observers can verify real testing progress in real time (refer to `[references/playwright-mcp-tools.md](references/playwright-mcp-tools.md)` for full tool parameter details):

### Step 1: Navigate and Audit Initial Page Health
1. Call `browser_navigate` to open the target URL.
2. Immediately call `browser_snapshot` to inspect the accessibility tree:
   - Verify the page title, primary `heading`, landmark structure, and interactive controls.
   - If the page is very large, use `browser_find` (with `text` or `regex`) or scoped `browser_snapshot(target=..., depth=...)` to inspect the relevant section efficiently.
3. Call `browser_console_messages` and `browser_network_requests` to verify zero console errors, hydration warnings, or failed (`4xx`/`5xx`) initial data fetches occurred on load.

### Step 2: Execute Negative Validation and Boundary Checks First
Before submitting valid data that navigates away from the form, test validation defenses:
1. Submit the form empty or populate invalid values using `browser_fill_form` and `browser_click` on the submit button (referencing exact `ref` values from the latest snapshot).
2. Call `browser_snapshot` (or `browser_find`) to confirm:
   - Clear, accessible field-level validation messages appear in the accessibility tree.
   - Previously entered user input is preserved (not wiped out on validation error).
   - No unhandled exception appeared in `browser_console_messages`.

### Step 3: Execute Positive Functional Flows and Verify Persistence
1. Populate valid inputs using `browser_fill_form` (or `browser_type` / `browser_select_option` / `browser_file_upload`) and trigger submission via `browser_click` or `browser_press_key(key="Enter")`.
2. If asynchronous processing occurs, call `browser_wait_for(text="...")` or `browser_wait_for(textGone="Loading...")` rather than arbitrary sleep intervals.
3. Capture a fresh `browser_snapshot` after the mutation completes:
   - Verify the UI updated with the expected confirmation feedback and newly created/updated data record.
4. Call `browser_network_requests` and `browser_network_request(index=...)`:
   - Confirm the mutation request (`POST`/`PUT`/`PATCH`/`DELETE`) returned the expected `200`/`201`/`204`/`302` status code and valid response body.
5. Call `browser_console_messages` to confirm zero runtime errors occurred during the state transition.
6. **Verify True Persistence**: Refresh or re-navigate to the listing/detail view to confirm the change persisted in the backend database rather than existing only in transient client memory.

### Step 4: Verify Keyboard Accessibility, Modals, and Responsive States
1. **Keyboard & Dialogs**: Open interactive dialogs/drawers, test focus progression with `browser_press_key(key="Tab")`, and verify `browser_press_key(key="Escape")` closes dismissible modals cleanly.
2. **Responsive & Media Checks (When UI/Layout Changed)**:
   - Use `browser_resize` to verify Mobile (`375x812`) and Desktop (`1440x900`) viewports, using `browser_snapshot(boxes=true)` to check element bounding boxes and detect clipped or zero-width controls.
   - Use `browser_emulate_media(colorScheme="dark", reducedMotion="reduce")` when dark mode or animation behavior is in scope.
   - Take a targeted `browser_take_screenshot` **only** if visual layout verification or visual bug documentation is needed.

### Step 5: Verify Authentication and Authorization Boundaries
1. Test protected routes in an unauthenticated session (or after logout) to verify redirection to login and confirm `browser_navigate_back` does not expose cached private screens.
2. When multi-role or multi-tenant rules apply, log in as a lower-privileged or secondary-tenant user and verify restricted actions/URLs return a safe `403`/`404` state.

## 6. Technology-Specific Adaptation Rules

- **React / Next.js / Vue / Nuxt / SvelteKit / Angular SPAs & SSR Apps**:
  - Watch `browser_console_messages` closely for SSR hydration mismatches (`Hydration failed because the initial UI does not match`), unhandled promise rejections, and missing React `key` warnings.
  - Remember that `ref` identifiers change when components re-render; always take a fresh `browser_snapshot` or `browser_find` after any DOM-mutating click or route transition before issuing the next click.
- **Server-Rendered Apps (Laravel Blade / Livewire / Inertia, Django Templates / HTMX, Rails Turbo)**:
  - For Livewire, HTMX, or Inertia partial updates, inspect `browser_network_requests` for `/livewire/update`, `HX-Request`, or `X-Inertia` exchanges and verify `419`/`403` CSRF errors do not occur.
- **Projects Using Autonomous Playwright CLI Test Files (`*.spec.ts`) Alongside Playwright MCP**:
  - Use Playwright MCP for interactive exploration, accessibility snapshot verification, and live debugging, and translate repeatable regression scenarios into permanent Playwright test files (`getByRole`, `getByLabel`, `expect(page).toHaveURL(...)`) when the repository maintains an E2E suite.
- **Non-Web Projects**:
  - Never require Playwright MCP on backend-only APIs, CLI binaries, or native mobile codebases where no browser UI exists.

## 7. Security and Safety Considerations

- **Never Execute Destructive QA on Production**: Verify the target domain before clicking delete buttons, submitting orders, or triggering emails/payments.
- **Avoid `browser_run_code_unsafe` by Default**: Do not use arbitrary JS execution tools (`browser_run_code_unsafe`) when standard declarative MCP tools (`browser_click`, `browser_fill_form`, `browser_snapshot`) suffice.
- **Protect Credentials in Logs & Screenshots**: Never capture screenshots of plaintext password fields or live secret keys, and use disposable test accounts (`SKILL-18`).

## 8. Verification Criteria

A Playwright MCP browser QA task is complete only when all of the following are satisfied:
- [ ] Every user flow in scope was interactively exercised beyond initial page load using semantic `browser_snapshot` / `browser_find` verification.
- [ ] Both positive happy-path submissions and negative validation/authorization scenarios were verified.
- [ ] `browser_network_requests` confirmed expected API status codes (`2xx` on success, `4xx` on validation/auth rejection, zero unexpected `500` errors).
- [ ] `browser_console_messages` confirmed zero unhandled JavaScript errors or framework hydration failures.
- [ ] Screenshots were used judiciously (only when visual evidence was necessary), and results are reported with strict `PASS` / `FAIL` / `BLOCKED` / `NOT TESTED` labels.

## 9. Failure Handling and Edge Cases

- **Stale Element `ref` Error**: If `browser_click` or `browser_type` fails because an element `ref` changed after an async re-render, run `browser_snapshot` or `browser_find` to get the updated `ref` and retry once.
- **Browser Profile Locked (`userDataDir` in use)**: If another browser instance locks the profile directory, run Playwright MCP with `--isolated` (optionally seeding auth state via `--storage-state`) so concurrent sessions do not collide.
- **Dev Server or Browser Unavailable in Environment**: If the sandboxed environment forbids opening ports or launching a headless browser binary, do not fabricate browser QA results. Record the exact error message, mark all browser QA items as `BLOCKED`, and verify backend/component behavior via `SKILL-16`.

## 10. Expected Outputs and Reporting Requirements

Report Playwright MCP browser QA findings using the following evidence-based template:

```markdown
# Playwright MCP Browser QA Report

## 1. Environment & Target Scope
- **Target URL**: `<http://localhost:3000/...>`
- **Viewports / Modes Tested**: `<Desktop 1440x900, Mobile 375x812, Light/Dark>`
- **Auth Roles Tested**: `<Guest, Standard User, Admin>`

## 2. Interactive Flow Verification Matrix
| Flow ID | User Journey & Action | Snapshot / DOM Evidence | Network Evidence (`browser_network_requests`) | Console Diagnostics (`browser_console_messages`) | Status (`PASS`/`FAIL`/`BLOCKED`/`NOT TESTED`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `BQA-01` | Submit empty checkout form (Negative) | Error alerts rendered for `email` & `address` (`[ref=e24]`). | Zero mutation requests sent. | `0` errors, `0` warnings. | `PASS` |
| `BQA-02` | Submit valid checkout form & reload (Positive) | Order confirmation heading `[ref=e41]` visible; persists after reload. | `POST /api/orders` -> `201 Created`. | `0` errors, `0` warnings. | `PASS` |
| `BQA-03` | Guest accesses `/admin/settings` (Auth Guard) | Redirected to `/login` heading `[ref=e5]`. | `GET /admin/settings` -> `302` to `/login`. | `0` errors. | `PASS` |

## 3. Defects Found & Visual/Trace Evidence
- `<None, or detailed reproduction steps + console/network logs + targeted screenshot path if visual bug>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Receive test scenarios from `testing-strategy-design` (`SKILL-15`), UI specifications from `ui-ux-design-systems` (`SKILL-20`), and accessibility requirements from `accessibility-engineering` (`SKILL-21`).
- **Parallel / Sibling Skills**: Coordinate with `cross-browser-responsive-qa` (`SKILL-23`) for multi-viewport/browser matrices and `test-data-environment-isolation` (`SKILL-18`) for safe test accounts and seeded data.
- **Downstream Skills**: Feed structured results into `test-reporting-failure-diagnosis` (`SKILL-19`) and `final-quality-gate-release-audit` (`SKILL-38`).

## 12. Source References

- **Playwright MCP Official Documentation**: https://playwright.dev/docs/getting-started-mcp
- **Microsoft Playwright MCP Repository**: https://github.com/microsoft/playwright-mcp (Apache-2.0)
- **Playwright Locators & Best Practices**: https://playwright.dev/docs/locators
- **Local Tool Reference**: [references/playwright-mcp-tools.md](references/playwright-mcp-tools.md)
- **Library Reference**: [../../references/playwright-mcp-reference.md](../../references/playwright-mcp-reference.md)
