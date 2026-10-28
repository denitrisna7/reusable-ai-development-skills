---
name: requirements-analysis
description: "Translates ambiguous user requests and feature briefs into explicit functional and non-functional requirements, user workflows, edge cases, security and privacy constraints, performance expectations, and testable acceptance criteria. Activate when scoping new features, enhancements, or complex fixes. Do not use for repository stack discovery or low-level architectural pattern design."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-02"
  category: "Core Discovery and Planning"
---

# Requirements Analysis & Acceptance Criteria

This skill transforms high-level, incomplete, or ambiguous user requests into structured, verifiable engineering requirements and testable acceptance criteria. It systematically uncovers implicit user workflows, state transitions, edge cases, failure modes, security and privacy constraints, performance budgets, and integration boundaries before design or coding begins. It prevents wasted implementation effort by resolving material ambiguities early while avoiding unnecessary question dumps when reasonable defaults can be derived from the existing codebase.

## 1. Activation Conditions

Activate this skill under any of the following scenarios:
- Receiving a feature request, bug report, or enhancement brief that lacks explicit acceptance criteria, failure handling rules, or boundary conditions.
- Planning a multi-step user workflow (e.g., checkout, onboarding, role management, data import/export, webhook processing) where state transitions and error recovery must be defined.
- Translating product requirements into testable specifications for backend TDD, API contracts, or Playwright browser verification.
- Evaluating how a proposed change affects existing permissions, data privacy, performance targets, or third-party integrations.
- When the user asks to "define requirements", "write acceptance criteria", "scope this feature", or "break down what needs to be built".

## 2. When Not to Use

Do not use this skill in the following situations:
- Executing a trivial, fully specified, single-line change where inputs, outputs, and side effects are already unambiguous.
- Inspecting an unfamiliar repository to detect its programming languages, frameworks, and build tools; run [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`) first.
- Selecting software design patterns, defining module dependency graphs, or authoring migration plans; route to [`adaptive-architecture`](../adaptive-architecture/SKILL.md) (`SKILL-03`).
- Recording finalized architectural decisions or API reference docs after design; route to [`technical-decision-records`](../technical-decision-records/SKILL.md) (`SKILL-04`).

## 3. Scope and Objectives

Every requirements analysis pass must explicitly address and document the following nine areas:
- **Functional requirements**: Concrete system behaviors, inputs, validations, state mutations, calculations, and outputs required for each user role or system actor.
- **Non-functional requirements**: Reliability, availability, accessibility (WCAG AA), observability, maintainability, and compatibility expectations.
- **User workflows**: End-to-end actor journeys including entry conditions, happy-path steps, alternative branches, cancellation paths, and post-conditions.
- **Acceptance criteria**: Deterministic, observable conditions (written in Given/When/Then or explicit checklist form) that prove each requirement is satisfied.
- **Edge cases and failure states**: Boundary values, empty states, loading states, malformed inputs, concurrent updates, network timeouts, partial failures, and idempotency rules.
- **Security and privacy requirements**: Authentication requirements, role/permission checks (RBAC/ABAC/ownership), input sanitization, audit logging, PII minimization, and data retention rules.
- **Performance expectations**: Response time targets, query complexity bounds (no N+1 queries), payload pagination limits, background job offloading, and frontend rendering budgets.
- **Integration constraints**: Upstream and downstream API contracts, rate limits, webhook retry semantics, backward compatibility with existing clients, and database schema constraints.
- **Testable completion criteria**: Specific unit, integration, API, and browser verification checks required before the task can be claimed complete.

## 4. Prerequisites and Context Requirements

- A completed stack and domain baseline from [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`), or verified knowledge of existing models, routes, and user roles in the repository.
- The user's initial request, prompt, issue description, or specification document.
- Access to existing domain models, validation rules, and tests in the codebase to infer established business conventions before asking the user.

## 5. Step-by-Step Workflow

Follow this disciplined procedure to convert a request into verifiable requirements:

### Step 1: Parse the Request and Cross-Reference Existing Domain Context
1. Extract the core objective, target actors (anonymous user, authenticated user, admin, external webhook, cron job), and affected domain entities from the user's request.
2. Inspect the existing codebase for related models, controllers, validation schemas, and tests so you do not ask the user questions the code already answers.
3. Separate what is **explicitly stated** in the request from what is **inferred from codebase conventions** and what is **genuinely missing**.

### Step 2: Evaluate Material Ambiguities (Ask Only When Necessary)
1. Identify missing decisions that materially alter the data model, security posture, user experience, or external integrations (e.g., whether deletion is soft or hard, who is authorized to approve a record, or how duplicate imports are handled).
2. Apply the **Clarification Discipline Rule**:
   - Do **not** ask questions whose answers are already visible in the repository's existing patterns or `DESIGN.md`.
   - Do **not** stall on minor implementation details that have a safe, standard engineering default; document the chosen default clearly instead.
   - When missing information **does** materially affect the solution, formulate a concise, prioritized set of clarifying questions (presenting recommended defaults and trade-offs) and wait for confirmation before finalizing irreversible changes.

### Step 3: Map User Workflows and State Transitions
1. Trace each user or system workflow from trigger to completion:
   - Pre-conditions (authentication state, required permissions, initial data state).
   - Step-by-step interaction sequence (UI views or API calls).
   - State transitions on domain entities (e.g., `draft -> pending -> approved -> archived`) and forbidden transitions.
   - Post-conditions (database persistence, emitted events, queued jobs, audit log entries, user notifications).

### Step 4: Enumerate Edge Cases, UI States, and Failure Modes
1. For every data view or interactive flow, specify:
   - **Empty State**: What the user or API caller receives when zero records exist (`R-27`).
   - **Loading / Processing State**: How in-flight requests or asynchronous background jobs are represented (`R-27`).
   - **Error State**: How validation errors (422), unauthorized access (401/403), missing resources (404), conflicts (409), and upstream service failures (502/503) are communicated and recovered from (`R-27`).
2. Identify boundary conditions: zero/negative numbers, empty strings, Unicode/multi-byte text, oversized payloads, timezone/DST boundaries, and double-click or duplicate-request race conditions.

### Step 5: Define Non-Functional, Security, Privacy, and Performance Constraints
1. **Security & Privacy**: Specify required authorization policies (preventing IDOR), CSRF/XSS/SQLi defenses, sensitive field redaction in logs/responses, and rate limiting on sensitive endpoints.
2. **Performance**: Define pagination defaults and maximum page sizes, eager-loading expectations to prevent N+1 queries, file size upload caps, and whether heavy operations must run asynchronously via queues.
3. **Integration**: Document third-party timeout thresholds, retry/backoff policies, idempotency keys, and API backward compatibility requirements.

### Step 6: Author Testable Acceptance Criteria and Completion Gate
1. Write numbered Functional Requirements (`FR-01`, `FR-02`, ...) and Non-Functional Requirements (`NFR-01`, `NFR-02`, ...).
2. Attach verifiable Acceptance Criteria (`AC-01`, `AC-02`, ...) using `Given / When / Then` or explicit verification assertions covering both positive (happy path) and negative (unauthorized, invalid input, failure) scenarios.
3. Map each acceptance criterion to the concrete verification layer that will prove it (unit test, integration/API test, static analysis, or browser QA check).

### Requirements Analysis Checklist
- [ ] Existing codebase inspected first to avoid redundant questions.
- [ ] Material unknowns surfaced with concise questions or documented safe defaults.
- [ ] Functional requirements and actor workflows mapped end-to-end.
- [ ] Empty, loading, and error states defined for every UI/data surface (`R-27`).
- [ ] Concurrency, boundary values, and external service failure states covered.
- [ ] Authorization, privacy, performance, and integration constraints specified.
- [ ] Every requirement paired with testable, evidence-backed acceptance criteria.

## 6. Technology-Specific Adaptation Rules

Adapt how requirements and acceptance criteria are expressed to match the target ecosystem:
- **PHP (Laravel / CodeIgniter / Symfony)**: Map validation requirements to FormRequest rules or framework validators, authorization to Policies/Gates or Middleware/Filters, and async requirements to Queue Jobs (`ShouldQueue`) where configured.
- **JavaScript / TypeScript (React / Next.js / Vue / Node)**: Specify client vs. server validation boundaries (e.g., Zod/Valibot schemas shared across forms and API routes/Server Actions), URL search-param state persistence, optimistic UI updates, and keyboard/screen-reader accessibility (`R-32`, `R-39`).
- **Python (Django / FastAPI / Flask)**: Express data validation constraints in terms of Pydantic models, Django Forms, or DRF Serializers, and specify sync vs. async endpoint or Celery/RQ task boundaries.
- **Go / Rust / Java / C# (.NET)**: Explicitly define DTO/struct validation rules, context cancellation and timeout propagation, transaction isolation expectations, and typed error contracts.
- **Mobile (Flutter / Native)**: Include offline/poor-connectivity behavior, app lifecycle background/foreground transitions, device permission prompts, and screen orientation/safe-area constraints.
- **Unknown or Mixed Stacks**: Keep requirements protocol- and behavior-focused (HTTP status codes, payload schemas, database invariants, UI state transitions) until stack architecture is finalized.

## 7. Security and Safety Considerations

- **Security by Default in Requirements**: Never treat authentication, object-level authorization (IDOR prevention), or input validation as "future enhancements"; include them as mandatory acceptance criteria on every state-changing requirement.
- **No Fabricated Business Rules (`C-5`, `R-36`, `R-38`)**: Do not invent regulatory compliance requirements, pricing tiers, or legal commitments without user confirmation.
- **Privacy & AI Data Boundaries**: When requirements involve external APIs or AI/LLM integrations, explicitly specify which user fields must be stripped, anonymized, or excluded from outbound payloads and application logs.

## 8. Verification Criteria

A requirements specification is complete and verified only when:
1. Every functional requirement is atomic, unambiguous, and traceable to the user's request or an identified domain invariant.
2. Every acceptance criterion is falsifiable and specifies both the trigger condition and the observable outcome (e.g., exact HTTP status, database state change, or UI feedback).
3. Happy paths, negative validation paths, unauthorized access paths, and failure/empty states are all explicitly represented.
4. Any remaining open questions are strictly limited to material product decisions that cannot be inferred from the codebase.

## 9. Failure Handling and Edge Cases

- **Contradictory User Requirements**: If a request conflicts with itself or with an existing hard constraint in the codebase (e.g., requesting unauthenticated access to tenant-isolated data), highlight the exact conflict, explain the risk, and ask the user to resolve it before implementation.
- **Scope Creep in Broad Prompts**: When a request spans multiple large subsystems, decompose the specification into a foundational MVP slice (`Phase 1`) and incremental follow-up slices (`Phase 2+`) so each slice can be built and verified safely.
- **User Unavailable to Answer Clarifying Questions**: If interactive clarification is impossible, proceed with the safest, most conservative interpretation, document all assumptions prominently at the top of the specification, and avoid destructive or irreversible schema changes.

## 10. Expected Outputs and Reporting Requirements

Produce a structured **Requirements & Acceptance Criteria Specification** using the following template:

```markdown
# Requirements Specification: <Feature or Task Name>

## 1. Objective & Scope Summary
- **Goal**: <Concise statement of what is being built or fixed>
- **Target Actors**: <Roles, permissions, or system triggers>
- **Documented Assumptions & Resolved Defaults**: <Explicit list>

## 2. User Workflows & State Transitions
1. **<Workflow Name>**: <Pre-conditions -> Steps -> State Changes -> Post-conditions>

## 3. Functional Requirements
- **`FR-01`**: <Requirement description>
- **`FR-02`**: <Requirement description>

## 4. Non-Functional, Security, Privacy & Performance Requirements
- **Security & Privacy (`NFR-SEC`)**: <Authz, validation, PII handling, rate limits>
- **Performance (`NFR-PERF`)**: <Pagination, query bounds, async processing>
- **Integration & Compatibility (`NFR-INT`)**: <Timeouts, retries, idempotency, backward compatibility>

## 5. Edge Cases, UI States & Failure Handling
| Scenario / State | Trigger Condition | Expected System & UI Behavior |
| :--- | :--- | :--- |
| Empty State | No records match query | Render informative empty view with primary action |
| Loading State | Request in flight | Disable duplicate submit; show accessible loading indicator |
| Validation Failure | Invalid/missing fields | Return 422 / preserve user input / highlight field error |
| Unauthorized / IDOR | Actor lacks resource ownership | Return 403/404; log security event; mutate nothing |
| Upstream Timeout | External API fails | Fail gracefully; retry safely or show actionable error |

## 6. Testable Acceptance Criteria & Verification Mapping
| ID | Given | When | Then | Verification Method |
| :--- | :--- | :--- | :--- | :--- |
| `AC-01` | ... | ... | ... | <Unit / Integration / API / Browser Test> |
| `AC-02` | ... | ... | ... | <Unit / Integration / API / Browser Test> |
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - Receives repository structure, stack facts, and domain conventions from [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`).
- **Downstream Skills**:
  - Feeds verified requirements into [`adaptive-architecture`](../adaptive-architecture/SKILL.md) (`SKILL-03`) for technical design and implementation planning.
  - Feeds security and privacy constraints into `application-security-owasp` (`SKILL-10`), `privacy-data-protection` (`SKILL-12`), and `threat-modeling-risk` (`SKILL-13`).
  - Feeds acceptance criteria directly into `testing-strategy-design` (`SKILL-15`), `backend-testing-tdd` (`SKILL-16`), and `playwright-mcp-browser-qa` (`SKILL-17`).

## 12. Source References

- Library Reference: [AI Anti-Slop & Engineering Craftsmanship Reference](../../references/anti-slop-engineering-reference.md) (`C-1` to `C-5`, `R-26`, `R-27`, `R-35`)
- Standard: [ISO/IEC/IEEE 29148 Systems and Software Engineering: Requirements Engineering](https://www.iso.org/standard/72089.html)
- Standard: [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
