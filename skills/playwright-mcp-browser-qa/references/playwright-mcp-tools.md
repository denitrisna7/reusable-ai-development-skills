# Playwright MCP Tools & Evidence-Based Browser QA Reference

> **Primary Sources**:
> - Official Playwright MCP Docs: https://playwright.dev/docs/getting-started-mcp
> - Microsoft Playwright MCP Repository: https://github.com/microsoft/playwright-mcp (Apache-2.0 License)

This reference provides the complete tool inventory, parameter schemas, capability suites, and verification patterns for executing deterministic browser QA via Playwright MCP.

---

## 1. Core Operating Rules for Playwright MCP

1. **Accessibility Tree First (`browser_snapshot` & `browser_find`)**:
   - Playwright MCP represents the live DOM through Playwright's semantic accessibility tree, assigning deterministic `ref` identifiers (e.g., `[ref=e12]`) to interactive and structural nodes (`heading`, `button`, `textbox`, `combobox`, `checkbox`, `link`, `dialog`, `alert`, `table`).
   - Always inspect the accessibility snapshot before clicking, typing, or asserting UI state.
   - On large pages, use `browser_find` (with `text` or `regex`) or `browser_snapshot` with `target` / `depth` to locate specific subtrees without flooding context.
2. **Screenshot Feature Disabled (`browser_take_screenshot` IS STRICTLY FORBIDDEN)**:
   - Taking screenshots (`browser_take_screenshot`) is **permanently disabled**. Do NOT take or dump screenshot files.
   - All browser testing must run in the **foreground live on screen** with a real Chromium window so users observe the actual test running.
3. **Page Load Never Equals `PASS`**:
   - Navigating to a URL and receiving a non-empty snapshot only proves the initial document rendered.
   - A feature is `PASS` only when the full interactive workflow (form fill, submission, state mutation, DOM update, expected network status code `2xx`/`4xx`, and zero unexpected console/page errors) is verified.

---

## 2. Complete Playwright MCP Tool Reference

### A. Inspection, Search & Diagnostic Tools (Read-Only)

| Tool Name | Purpose | Parameters & Usage Notes |
| :--- | :--- | :--- |
| `browser_snapshot` | Capture the semantic accessibility tree of the current page or a specific element subtree. | `target` (optional `ref` or selector to scope snapshot), `depth` (optional max tree depth), `boxes` (optional boolean; set `true` to include `[box=x,y,w,h]` CSS pixel bounding boxes for layout/overlap/tap-target checks), `filename` (optional output file). |
| `browser_find` | Search the current page's accessibility tree by substring or regular expression. | `text` (case-insensitive substring) or `regex` (pattern such as `"/invalid|required/i"`). Returns matching elements with their `ref` IDs and surrounding context. |
| `browser_console_messages` | Retrieve console messages and uncaught page exceptions (`error`, `warning`, `info`, `debug`). | `level` (optional minimum severity, default `"info"`), `all` (`true` for entire session, `false` since last navigation), `filename` (optional). Check after every page load and user interaction. |
| `browser_network_requests` | List numbered HTTP/XHR/Fetch network requests since page load. | `static` (boolean, default `false` to exclude static assets like images/fonts/CSS), `filter` (regex string, e.g., `"/api/(orders|auth)/"`), `filename` (optional). Returns 1-based request indices, methods, URLs, and status codes. |
| `browser_network_request` | Inspect detailed request/response headers and body for a specific network request. | `index` (required 1-based integer from `browser_network_requests`), `part` (optional filter for request/response headers or body). Use to verify exact API payloads and error codes. |
| `browser_take_screenshot` | **[DISABLED / FORBIDDEN]** Screenshots are disabled in favor of live foreground on-screen browser execution. | Do not invoke. All visual verification is performed live on screen. |

### B. Navigation & Element Interaction Tools

| Tool Name | Purpose | Parameters & Usage Notes |
| :--- | :--- | :--- |
| `browser_navigate` | Navigate the active tab to a target URL. | `url` (required string). Always verify the URL points to a safe local/test/staging target before navigating. |
| `browser_navigate_back` | Navigate back one entry in the tab's history stack. | None. Use to test browser back-button behavior, wizard state preservation, and post-logout history protection. |
| `browser_click` | Click a button, link, checkbox, radio, or interactive control. | `target` (required `ref` from snapshot or unique selector), `element` (human-readable label for audit trail), `doubleClick` (optional boolean), `button` (`"left"`, `"right"`, `"middle"`), `modifiers` (array of `"Alt"`, `"Control"`, `"Meta"`, `"Shift"`). |
| `browser_fill_form` | Populate multiple form controls (textboxes, checkboxes, dropdowns) in a single atomic tool call. | `fields` (required array of field objects with `name`, `type`, `ref`, `value`). Strongly preferred over multiple sequential `browser_type` calls when filling multi-field forms. |
| `browser_type` | Type text into a single editable input or textarea. | `target` (required `ref`), `text` (string to enter), `submit` (optional boolean to press `Enter` after typing), `slowly` (optional boolean to dispatch key-by-key events for autocomplete/search inputs). |
| `browser_select_option` | Select one or more options in a native `<select>` or combobox element. | `target` (required `ref`), `values` (required array of option values or visible labels). |
| `browser_press_key` | Press a keyboard key or shortcut on the page or focused element. | `key` (required string, e.g., `"Tab"`, `"Shift+Tab"`, `"Enter"`, `"Escape"`, `"ArrowDown"`, `"Space"`). Essential for testing keyboard accessibility, focus traps, and Escape dialog dismissal. |
| `browser_hover` | Move the pointer over a target element. | `target` (required `ref`), `element` (description). Use to trigger tooltips, dropdown menus, or hover states. |
| `browser_drag` / `browser_drop` | Drag an element to a drop target or drop files/MIME data. | `startTarget` + `endTarget` (for `browser_drag`), or `target` + `paths`/`data` (for `browser_drop`). |
| `browser_file_upload` | Supply local file paths to an active file chooser dialog. | `paths` (array of absolute local file paths; omit to cancel chooser). Trigger the file input click first, then invoke `browser_file_upload`. |
| `browser_handle_dialog` | Accept or dismiss native browser `alert`, `confirm`, or `prompt` dialogs. | `accept` (required boolean), `promptText` (optional string when accepting a `prompt` dialog). |
| `browser_wait_for` | Wait for expected text to appear, transient loading text to disappear, or a short time to elapse. | `text` (wait for substring to appear), `textGone` (wait for spinner/loading text to vanish), `time` (seconds, max 30). Prefer `text` / `textGone` over fixed `time` sleeps. |

### C. Viewport, Media Emulation & Tab Management Tools

| Tool Name | Purpose | Parameters & Usage Notes |
| :--- | :--- | :--- |
| `browser_resize` | Resize the browser viewport to specific pixel dimensions. | `width` (number), `height` (number). Standard breakpoints: Mobile (`375x812`), Tablet (`768x1024`), Desktop (`1440x900`). |
| `browser_emulate_media` | Emulate CSS media queries and accessibility preferences. | `colorScheme` (`"light"`, `"dark"`, `"no-preference"`, `null`), `reducedMotion` (`"reduce"`, `"no-preference"`, `null`), `forcedColors` (`"active"`, `"none"`, `null`), `contrast` (`"more"`, `"no-preference"`, `null`). |
| `browser_tabs` | Inspect, open, switch, or close browser tabs. | `action` (`"list"`, `"new"`, `"select"`, `"close"`), `index` (optional tab index), `url` (optional URL for `"new"`). Use when testing `target="_blank"` links or OAuth popups. |

### D. Opt-In Capability Suites (`--caps=...`)

| Capability Flag | Tools Unlocked | Primary QA Use Cases |
| :--- | :--- | :--- |
| `--caps=network` | `browser_route`, `browser_route_list`, `browser_unroute`, `browser_network_state_set` | Deterministic negative/error testing: mock `500 Internal Server Error`, `422 Unprocessable Entity`, `429 Too Many Requests`, delayed responses, or `"offline"` network state to verify UI error banners and retry buttons. |
| `--caps=storage` | `browser_cookie_list`, `browser_cookie_get`, `browser_cookie_set`, `browser_cookie_delete`, `browser_cookie_clear`, `browser_localstorage_*`, `browser_sessionstorage_*`, `browser_storage_state`, `browser_set_storage_state` | Authentication & session QA: inspect `HttpOnly`, `Secure`, and `SameSite` flags on session cookies; save and restore authenticated storage states across test runs; test session expiration behavior. |
| `--caps=devtools` | `browser_start_tracing`, `browser_stop_tracing`, `browser_start_video`, `browser_stop_video`, `browser_highlight`, `browser_annotate` | Deep failure diagnosis: record Playwright trace zips (`trace.zip`) or video artifacts when diagnosing intermittent race conditions or complex layout regressions. |

---

## 3. Standard Browser QA Verification Checklist

1. **Initial Render & Semantics**:
   - `browser_navigate` -> `browser_snapshot`: Verify landmark roles (`main`, `navigation`), page `heading`, and interactive controls have accessible names.
   - `browser_console_messages`: Confirm zero uncaught JavaScript errors or hydration mismatches on initial load.
2. **Negative Form Validation**:
   - Submit empty or invalid inputs using `browser_fill_form` / `browser_click`.
   - `browser_snapshot` / `browser_find`: Confirm accessible error messages render next to invalid fields (`aria-invalid`, alert text) and verify no premature `200 OK` mutation fired in `browser_network_requests`.
3. **Positive Interactive Flow & Persistence**:
   - Fill valid inputs (`browser_fill_form`) and submit (`browser_click`).
   - Check `browser_network_requests` and `browser_network_request` to confirm the expected `POST`/`PUT`/`PATCH` request returned `200`/`201`/`204` (or valid redirect).
   - Check `browser_console_messages` to confirm zero runtime exceptions occurred during submission.
   - Reload or navigate back/forward to confirm the mutated state actually persisted in the backend rather than only updating optimistic client state.
4. **Authentication & Authorization Boundaries**:
   - Verify unauthenticated access to protected routes redirects to login (`401`/`302`).
   - Verify unauthorized role access to admin/restricted routes renders a safe `403` / access-denied state without firing privileged API mutations.
