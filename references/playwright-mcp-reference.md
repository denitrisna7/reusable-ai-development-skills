# Playwright MCP Browser QA Reference

> Primary Sources:
> - **Playwright MCP Official Docs**: https://playwright.dev/docs/getting-started-mcp
> - **Microsoft Playwright MCP Repository**: https://github.com/microsoft/playwright-mcp (commit `0c4107acbecb75472b23c05c0e42471a0011874f`, Apache-2.0 License)

This reference documents the verified capabilities, tool schemas, configuration flags, and evidence-based browser QA workflows for Playwright MCP.

---

## 1. Core Design Philosophy: Accessibility Snapshots Over Screenshots

Playwright MCP interacts with web pages via Playwright's **accessibility tree**, returning deterministic element references (e.g., `[ref=e5]`, `[ref=e10]`) alongside semantic roles (`heading`, `textbox`, `button`, `checkbox`, `link`, `dialog`).

1. **Snapshot-First Interaction**: Always use `browser_snapshot` (or `browser_find` for targeted searches on large pages) to inspect the DOM/accessibility state and obtain `ref` identifiers before interacting.
2. **No Routine Screenshot Spam**: Do **not** capture screenshots after every click or navigation. Use `browser_take_screenshot` only when:
   - Visual layout, overflow, contrast, or CSS rendering must be inspected visually.
   - Recording visual proof of a UI failure or layout regression.
   - Capturing final milestone visual evidence when explicitly required.
3. **Page Load != PASS**: A `200 OK` navigation or non-empty snapshot never proves a feature works. Every interactive flow must be exercised through its actual state transitions, network responses, and console error checks.

---

## 2. Playwright MCP Tool Inventory

### A. Core Inspection & Search Tools (Read-Only)
| Tool Name | Purpose | Key Parameters & Best Practices |
| :--- | :--- | :--- |
| `browser_snapshot` | Capture accessibility tree of current page or subtree. | Optional `target` (element ref/selector), `depth` (limit tree depth), `boxes` (`true` to include `[box=x,y,width,height]` in CSS pixels for layout/tap-target verification), `filename`. |
| `browser_find` | Search current page's accessibility snapshot by text or regex. | `text` (case-insensitive substring) or `regex` (e.g., `"/error/i"`). Much more token-efficient than full `browser_snapshot` on large pages when locating a specific control and its `ref`. |
| `browser_console_messages` | Retrieve browser console logs (`error`, `warning`, `info`, `debug`). | `level` (defaults to `"info"`), `all` (`true` for entire session, `false` since last navigation). **Mandatory** check after every user action and page load. |
| `browser_network_requests` | List numbered network requests since page load. | `static` (`false` by default to omit images/fonts/scripts), `filter` (regex, e.g., `"/api/.*"`). Use to verify API calls, status codes (`4xx`/`5xx`), and payload triggers. |
| `browser_network_request` | Inspect full headers and body of a specific network request. | `index` (1-based number from `browser_network_requests`), optional `part`. Check before claiming an API integration succeeded. |
| `browser_take_screenshot` | Capture viewport, full-page, or element image. | Optional `target`/`element`, `fullPage`, `type` (`png`/`jpeg`/`webp`), `scale` (`"css"` default vs `"device"`), `filename`. Cannot be used to target actions—use `browser_snapshot` for actions. |

### B. Core Interaction & Navigation Tools
| Tool Name | Purpose | Key Parameters & Best Practices |
| :--- | :--- | :--- |
| `browser_navigate` | Open a URL in the current tab. | `url` (string). Verify target environment is a safe local/test URL before navigating. |
| `browser_navigate_back` | Navigate back in browser history. | None. Useful for testing history state and back-button resilience. |
| `browser_click` | Click an element. | `target` (exact `ref` from snapshot or unique selector), `element` (human-readable description), optional `doubleClick`, `button`, `modifiers`. |
| `browser_fill_form` | Fill multiple form fields in a single call. | `fields` (array of field objects). Preferred over multiple separate `browser_type` calls when populating standard forms. |
| `browser_type` | Type text into an editable element. | `target`, `text`, optional `submit` (`true` to press Enter), `slowly` (`true` for key-by-key handlers like autocomplete). |
| `browser_select_option` | Select dropdown option(s). | `target`, `values` (array of option values/labels). |
| `browser_press_key` | Press a keyboard key (`Tab`, `Enter`, `Escape`, `ArrowDown`, etc.). | `key` (string). Essential for verifying keyboard navigation (`R-32`) and modal Escape closing (`R-26`). |
| `browser_hover` | Hover mouse over an element. | `target`, `element`. Use to test tooltips, menus, and hover states. |
| `browser_drag` / `browser_drop` | Drag between elements or drop files/MIME data. | `startTarget`/`endTarget` or `target` + `paths`/`data`. |
| `browser_file_upload` | Upload one or more local files to a file chooser. | `paths` (array of absolute paths; omit to cancel chooser). |
| `browser_handle_dialog` | Accept or dismiss `alert`, `confirm`, or `prompt` dialogs. | `accept` (boolean), optional `promptText`. |
| `browser_wait_for` | Wait for text to appear, disappear, or time to elapse. | `text`, `textGone`, or `time` (max 30s). Prefer waiting for deterministic text (`text` / `textGone`) over arbitrary sleep timers. |
| `browser_resize` | Change browser viewport dimensions. | `width`, `height` (numbers). Essential for responsive QA across mobile (`375x812`), tablet (`768x1024`), and desktop (`1440x900`). |
| `browser_emulate_media` | Emulate CSS media features. | `colorScheme` (`"light"`/`"dark"`/`null`), `reducedMotion` (`"reduce"`/`"no-preference"`), `forcedColors`, `contrast`. Essential for dark mode (`R-34`) and reduced motion (`R-39`) verification. |
| `browser_tabs` | Manage browser tabs (`list`, `new`, `close`, `select`). | `action`, optional `index`, `url`. |

### C. Opt-In Capability Suites (`--caps=...`)
- **Network Mocking (`--caps=network`)**: `browser_route` (mock URL patterns with custom status/body/headers), `browser_route_list`, `browser_unroute`, `browser_network_state_set` (`"offline"` / `"online"`). Ideal for testing loading, error, and offline states (`R-27`) deterministically.
- **Storage Management (`--caps=storage`)**: `browser_cookie_list`, `browser_cookie_get`, `browser_cookie_set`, `browser_cookie_delete`, `browser_cookie_clear`, `browser_localstorage_*`, `browser_sessionstorage_*`, `browser_storage_state`, `browser_set_storage_state`. Ideal for verifying auth cookies (`HttpOnly`, `Secure`, `SameSite`) and session persistence.
- **DevTools & Tracing (`--caps=devtools`)**: `browser_start_tracing`, `browser_stop_tracing`, `browser_start_video`, `browser_stop_video`, `browser_highlight`, `browser_annotate`.

---

## 3. Security & Safety Guardrails for Browser Automation

1. **Avoid `browser_run_code_unsafe` Unless Explicitly Necessary**: `browser_run_code_unsafe` executes arbitrary JS in the Playwright server process (RCE-equivalent). Prefer standard declarative tools (`browser_click`, `browser_fill_form`, `browser_snapshot`).
2. **Workspace File Access Boundary**: Never enable `--allow-unrestricted-file-access` against untrusted pages.
3. **Session Isolation for Concurrent Runs**: A persistent profile locks its user-data directory. Use `--isolated` (optionally with `--storage-state`) when running clean, reproducible test sessions or parallel agents.
4. **Never Test Destructive Actions Against Production**: Verify the target host (`localhost`, `127.0.0.1`, or staging/test environment) before submitting forms, deleting records, or triggering webhooks/payments.
