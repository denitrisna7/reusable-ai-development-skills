# Master Before-Action Execution Protocol (`BEFORE_ACTION.md`)

> **CRITICAL DIRECTIVE FOR AI AGENTS (ANTIGRAVITY / CLAUDE / CHATGPT / AGENT SKILLS)**  
> When the user prompts:  
> **"git clone kan skill ini kemudian kerjakan sesuai skill tersebut"**  
> *(or any variation such as "audit aplikasi kita dengan skill ini", "kerjakan sesuai skill", or "run pre-deployment audit")*  
> 
> **YOU ARE STRICTLY FORBIDDEN FROM:**  
> 1. Jumping directly to a final summary without executing real CLI commands or tools.  
> 2. Fabricating `PASS` statuses for unit tests or browser QA without showing raw command output.  
> 3. Claiming browser testing passed if Playwright MCP tools were not actively invoked.  
> 
> **YOU MUST EXECUTE THE FOLLOWING 4 PHASES IN STRICT CHRONOLOGICAL ORDER:**

---

## Phase 0: Ground-Truth Pre-Flight Diagnostic (Mandatory First Action)

Before writing or modifying any code or making any claims, execute the pre-flight audit script in the workspace root:

```bash
# Run the automated diagnostic script from this library:
python3 .agents/skills/ai-skills/scripts/run-audit.py .
# (or python3 reusable-ai-development-skills/scripts/run-audit.py . if cloned in root)
```

**Required Output in Chat Response:**
- Paste the raw diagnostic summary output from `run-audit.py`:
  - Detected stack (Laravel, Node/React/Next, Python/Django, Go, etc.).
  - Environment check status (`.env` vs `.env.example`, `DEBUG=false` check, secret leak scan).
  - Active local server status (ports 3000, 5173, 8000, 8080).
  - Automated test runner status (`npm test`, `php artisan test`, `pytest`).

---

## Phase 1: Fix All Runtime Errors & Broken CRUD (500, 404, 403)

Based on the Phase 0 diagnostic:
1. **Fix 500 Internal Server Errors** (`SKILL-34` & `SKILL-16`):
   - Inspect server logs (`storage/logs/`, terminal stderr, or console logs).
   - Fix null-pointer exceptions, unhandled promises, missing database tables, or failed migrations (`SKILL-24`).
2. **Fix 403 Forbidden & 401 Unauthorized Errors** (`SKILL-10`):
   - Check CSRF token inclusion on forms.
   - Verify authentication middleware, session cookies, and RBAC route permissions.
3. **Fix 404 Not Found Errors** (`SKILL-03`):
   - Verify route definitions match front-end navigation links and form action URLs.
4. **Verify CRUD Cycle** (`SKILL-16`):
   - Run the automated test runner in the terminal:
     - Node: `npm test`
     - Laravel: `php artisan test`
     - Python: `pytest`
   - Paste the exit code and summary of passing tests into the chat.

---

## Phase 2: Browser & Mobile UI Verification (`SKILL-17` & `SKILL-23`)

1. **Verify Dev Server**:
   - Ensure the local dev server is running on `http://localhost:<port>` (e.g. 3000, 5173, or 8000).
2. **Check Playwright MCP Availability**:
   - **If Playwright MCP tools (`browser_navigate`, `browser_snapshot`) are registered:**
     - Call `browser_navigate` to open the local application URL.
     - Call `browser_snapshot(boxes=true)` to verify:
       - No overlapping elements (e.g., sticky headers covering text).
       - Touch targets are `>= 44x44px` on mobile viewport (`browser_resize` to `375x812`).
       - Zero unhandled console errors in `browser_console_messages`.
   - **If Playwright MCP tools are NOT available in this session:**
     - You MUST honestly output:  
       `[BROWSER QA STATUS: BLOCKED — Playwright MCP tools not registered in this session]`  
       *(Do NOT fabricate simulated browser pass results).*

---

## Phase 3: Final Quality Gate Sign-Off (`SKILL-38` & `SKILL-33`)

Consolidate the empirical evidence from Phases 0, 1, and 2 into a formal audit table:

| Gate Domain | Status (`PASS` / `FAIL` / `BLOCKED`) | Empirical Evidence |
| :--- | :---: | :--- |
| **1. Environment & Secrets** | `PASS` / `FAIL` | Output from `run-audit.py` (.env check) |
| **2. Security & OWASP** | `PASS` / `FAIL` | CSRF & Auth verified |
| **3. Automated Tests & CRUD** | `PASS` / `FAIL` | Exit code and test output cited |
| **4. Browser QA & Mobile View** | `PASS` / `BLOCKED` | Playwright snapshot or honest BLOCKED note |
| **5. Production Build** | `PASS` / `FAIL` | Build command exit code |

**Authoritative Release Verdict:**
- **`READY`**: All checks executed and passed with cited proof.
- **`BLOCKED`**: One or more critical checks failed, or mandatory tools were blocked.
