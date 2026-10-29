---
name: adaptive-architecture
description: "Evaluates system architecture, module boundaries, and incremental technical plans without unnecessary rewrites. Use when designing modules. Do not use for standalone ADRs."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-03"
  category: "Core Discovery and Planning"
---

# Adaptive Architecture & Technical Planning

This skill evaluates an application's existing architectural style and designs pragmatic, evidence-based technical plans for new features, structural evolutions, and system integrations. It rejects dogmatic, one-size-fits-all architectures and premature abstractions in favor of designs that respect established repository boundaries, compatibility constraints, maintainability, and operational simplicity. Every architectural plan emphasizes incremental delivery, explicit dependency rules, and minimizing unnecessary rewrites.

## 1. Activation Conditions

Activate this skill under any of the following scenarios:
- Designing the technical structure for a new feature, subsystem, background processing pipeline, or cross-cutting concern after discovery and requirements analysis.
- Evaluating whether to extend an existing module pattern or introduce a new design pattern, service layer, domain boundary, or abstraction seam.
- Planning a multi-step migration, structural refactoring, or third-party integration that touches multiple layers (routing, domain logic, persistence, UI).
- Resolving circular dependencies, tight coupling, god classes/controllers, or scaling bottlenecks within an existing codebase.
- When the user asks to "design the architecture", "create an implementation plan", "evaluate architectural trade-offs", or "structure this module".

## 2. When Not to Use

Do not use this skill in the following situations:
- The repository's languages, frameworks, and existing directory conventions have not yet been inspected; run [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`) first.
- The functional requirements and acceptance criteria are still vague or undecided; run [`requirements-analysis`](../requirements-analysis/SKILL.md) (`SKILL-02`) first.
- Implementing a localized bug fix or minor adjustment that fits entirely within an existing function or component with zero structural impact; route to [`adaptive-engineering`](../adaptive-engineering/SKILL.md) (`SKILL-06`).
- Writing formal user-facing setup guides, operational runbooks, or standalone ADR libraries after implementation; route to [`technical-decision-records`](../technical-decision-records/SKILL.md) (`SKILL-04`).

## 3. Scope and Objectives

Every architectural assessment and technical plan must cover the following nine core areas without imposing a preferred architecture without evidence:
- **Evaluating existing architecture**: Identifying the current architectural topology (layered MVC, modular monolith, hexagonal/clean architecture, event-driven, serverless, microservices, or legacy procedural/scripted) and assessing its strengths and friction points.
- **Selecting suitable design patterns**: Choosing patterns that solve concrete, present requirements (e.g., Strategy for interchangeable gateways, Adapter for external SDKs, Action/Service for multi-step transactions) while avoiding speculative over-engineering.
- **Architectural trade-offs**: Explicitly comparing candidate approaches across complexity, performance, testability, operational overhead, and team familiarity.
- **Dependency boundaries**: Defining strict direction-of-dependency rules between presentation/transport layers, domain/application logic, data access, and external infrastructure.
- **Maintainability and scalability**: Ensuring clear cohesion, low coupling, bounded module size, stateless horizontal scalability where applicable, and predictable data growth handling.
- **Compatibility constraints**: Preserving backward compatibility across public APIs, database schemas, queue payload formats, session structures, and runtime versions.
- **Incremental implementation plans**: Breaking complex changes into small, independently verifiable slices that keep the application buildable and working at every step.
- **Minimizing unnecessary rewrites**: Working with the grain of the existing codebase instead of proposing disruptive paradigm shifts or wholesale rewrites when targeted improvements suffice.
- **Documenting significant technical decisions**: Capturing the context, alternatives considered, chosen approach, and consequences for every major architectural choice.

## 4. Prerequisites and Context Requirements

- Verified repository facts from [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`), including the active framework, directory layout, ORM, and testing setup.
- Explicit functional and non-functional requirements from [`requirements-analysis`](../requirements-analysis/SKILL.md) (`SKILL-02`).
- Inspection of 2 to 5 existing modules in the target repository to verify how similar features are currently architected.

## 5. Step-by-Step Workflow

Execute the following architectural planning workflow in sequence:

### Step 1: Audit the Existing Architectural Baseline
1. Map how data and control flow through the existing application for a comparable feature (e.g., `Request -> Controller/Handler -> Validation -> Service/Action -> Model/Repository -> Response/View`).
2. Identify whether the codebase is organized **by technical layer** (`controllers/`, `models/`, `services/`) or **by domain/feature** (`modules/Billing/`, `features/auth/`).
3. Default to extending the repository's established organization unless there is documented evidence that the current pattern is causing defects, security flaws, or severe maintenance bottlenecks.

### Step 2: Define Module Responsibilities and Dependency Boundaries
1. Partition the required work into cohesive components with single, well-defined responsibilities:
   - **Transport / Presentation Boundary**: HTTP controllers, CLI commands, GraphQL resolvers, or UI components handle input parsing, auth enforcement, and response formatting only.
   - **Application / Domain Boundary**: Services, Actions, Use Cases, or Domain Models encapsulate business rules, state transitions, and transaction orchestration.
   - **Infrastructure / Persistence Boundary**: Repositories, ORM models, query builders, and external API clients handle I/O, retries, and serialization.
2. Enforce unidirectional dependencies: presentation depends on application/domain; domain logic must not depend directly on HTTP transport primitives or third-party vendor wire formats when an adapter seam is warranted.

### Step 3: Evaluate Design Patterns and Architectural Trade-Offs
1. Apply the **Anti-Slop Abstraction Test (`C-1`, `C-3`)**:
   - Do **not** create single-implementation interfaces (`UserServiceInterface` implemented only by `UserService`), empty pass-through wrapper layers, or generic factory-of-factories unless required by existing project conventions or essential test isolation seams.
   - Introduce an interface, adapter, or strategy pattern **only** when multiple implementations exist (e.g., Stripe vs. Midtrans payment provider, S3 vs. local storage, real client vs. deterministic test fake) or when isolating volatile third-party SDKs.
2. For any non-trivial architectural decision, compare at least two realistic options (e.g., *Option A: Synchronous in-process execution* vs. *Option B: Queued background job with status polling*) across complexity, latency, failure recovery, and infrastructure cost.

### Step 4: Verify Compatibility and Migration Constraints
1. Check database impact: ensure schema changes follow an expand-and-contract (backward-compatible) sequence if zero-downtime deployment or rolling updates apply.
2. Check contract impact: verify that existing REST/GraphQL consumers, mobile clients, webhook senders, or queued jobs in flight will not break when the new code is deployed.
3. Check runtime and infrastructure impact: verify that the design does not require unavailable extensions, unapproved cloud services, or unsupported runtime versions.

### Step 5: Construct an Incremental, Verifiable Implementation Plan
1. Decompose the architecture into ordered implementation phases where each slice leaves the system in a green, testable state:
   - **Slice 1**: Data schema / migrations, domain types, and core invariants + unit tests.
   - **Slice 2**: Application logic / service / external adapter + integration tests.
   - **Slice 3**: API endpoints / controllers / permissions + contract/feature tests.
   - **Slice 4**: UI components, state binding, and end-to-end verification.
2. Define rollback or feature-flag strategies for high-risk slices.

### Architectural Planning Checklist
- [ ] Existing repository architecture inspected and respected before proposing changes.
- [ ] No speculative abstractions, single-use interfaces, or unnecessary rewrites introduced.
- [ ] Clear boundaries defined between transport/UI, domain logic, persistence, and external APIs.
- [ ] At least two options and their trade-offs analyzed for significant architectural decisions.
- [ ] Database, API, and queue backward compatibility verified.
- [ ] Implementation broken into small, ordered, independently testable slices.

## 6. Technology-Specific Adaptation Rules

Align architectural designs with the idiomatic patterns of the detected stack:
- **PHP (Laravel)**: Work with Laravel's idioms: FormRequests for validation, Policies/Gates for authorization, focused Action classes or Service classes for multi-model orchestration, Eloquent scopes/relations for queries, Events/Listeners or Queued Jobs for side effects, and API Resources for serialization. Do not force Java-style DAO/Repository wrappers around Eloquent unless the codebase already uses them.
- **PHP (CodeIgniter 3 / 4)**: Respect CI4's `app/Controllers`, `app/Models`, `app/Entities`, `app/Filters`, and `app/Libraries` (or `Services.php`) structure, or CI3's `application/controllers`, `application/models`, and `application/libraries`. Avoid forcing Laravel-specific patterns onto CodeIgniter.
- **JavaScript / TypeScript (React / Next.js / Vue)**: Separate data-fetching and mutation orchestration (Server Components, Server Actions, TanStack Query, Pinia stores) from pure presentational components. Colocate feature modules (`features/<domain>/`) when the repo follows feature-sliced design, or use `src/components/` + `src/lib/` when the repo is flat.
- **Node.js / NestJS / Express**: In NestJS, follow the `@Module`, `@Controller`, `@Injectable` provider, Guard, and Pipe architecture. In Express/Fastify/Hono, keep route handlers thin and delegate business logic to domain modules.
- **Python (Django / FastAPI)**: In Django, follow the existing fat-model/service-layer convention (`models.py`, `services.py`, `selectors.py`, `views.py`) per app. In FastAPI, use `APIRouter`, `Depends()` dependency injection, Pydantic schemas, and async/sync SQLAlchemy session boundaries cleanly.
- **Go**: Prefer small consumer-defined interfaces, explicit dependency injection via struct constructors (`NewService(repo, logger)`), `internal/` package encapsulation, and standard `context.Context` propagation. Avoid deep inheritance hierarchies.
- **Java / Kotlin (Spring Boot) & C# (.NET)**: Follow constructor-injected `@Service` / `@Repository` / `@RestController` or ASP.NET Core DI registrations, DTO mapping at controller boundaries, and transactional service methods.
- **Rust**: Use strong domain newtypes, `Result<T, E>` error propagation, trait boundaries only where polymorphism is needed, and clear module visibility (`pub(crate)` vs `pub`).

## 7. Security and Safety Considerations

- **Defense-in-Depth Boundaries**: Enforce authentication and authorization at the transport boundary **and** pass verified actor/tenant context into domain services so multi-tenant data isolation cannot be bypassed by internal callers.
- **Fail-Closed Design**: Design external integrations, permission checks, and webhook verifiers to fail closed (deny access or abort transaction on error) with explicit timeouts and circuit-breaking where appropriate.
- **Transactional Integrity**: Ensure multi-step database writes are wrapped in atomic transactions and that external network calls (emails, webhooks, payment captures) happen outside database locks or via outbox/idempotent job patterns.

## 8. Verification Criteria

An architectural plan is ready for implementation only when:
1. Every proposed file path and module name aligns with the repository's existing directory structure and naming conventions.
2. Every new abstraction or pattern is justified by a concrete requirement from `SKILL-02` rather than generic dogma.
3. Dependency flow is acyclic and respects layer boundaries.
4. Each implementation slice specifies the exact static analysis, unit, integration, or browser tests that will verify it.

## 9. Failure Handling and Edge Cases

- **Legacy Tangled Architecture (Spaghetti / God Files)**: Do not propose halting feature work for a multi-week rewrite. Use the **Strangler Fig** or **Sprout Class/Method** pattern: extract or isolate only the new or modified behavior behind a clean seam, cover it with tests, and leave unrelated legacy code undisturbed (see [`refactoring-legacy-safety`](../refactoring-legacy-safety/SKILL.md), `SKILL-08`).
- **Performance vs. Simplicity Conflict**: If a requirement suggests heavy distributed infrastructure (e.g., introducing Kafka or microservices into a simple monolith), evaluate whether indexed database queries, caching, or the existing job queue satisfies the load first.
- **Breaking Changes Required**: If a breaking API or schema change is unavoidable, design a versioned transition path (`v1` alongside `v2`, or dual-read/dual-write schema migration) and highlight the migration risk explicitly.

## 10. Expected Outputs and Reporting Requirements

Produce a structured **Adaptive Architecture & Implementation Plan** using the following template:

```markdown
# Architecture & Implementation Plan: <Feature or Initiative>

## 1. Existing Architecture Fit
- **Current Pattern**: <Observed repo architecture and sampled reference files>
- **Integration Strategy**: <How the change fits existing conventions without unnecessary rewrites>

## 2. Component & Boundary Design
| Component / File Path | Layer | Responsibility | Dependencies |
| :--- | :--- | :--- | :--- |
| `<path/to/file>` | Presentation / Transport | ... | ... |
| `<path/to/file>` | Application / Domain | ... | ... |
| `<path/to/file>` | Persistence / Infrastructure | ... | ... |

## 3. Architectural Trade-Off Analysis
- **Decision**: <Key design choice>
- **Options Considered**:
  1. **<Option A (Selected)>**: <Pros / Cons>
  2. **<Option B (Rejected)>**: <Pros / Cons>
- **Rationale**: <Evidence-based reason rooted in requirements and repo constraints>

## 4. Compatibility, Security & Data Integrity Safeguards
- **Backward Compatibility**: <API, schema, and client compatibility notes>
- **Transaction & Failure Boundaries**: <DB transactions, idempotency, external timeouts>
- **Authorization & Tenant Isolation**: <Where policy checks execute>

## 5. Incremental Implementation Plan
1. **Slice 1 (<Scope>)**: <Files to create/modify> -> **Verification**: <Test/Check command>
2. **Slice 2 (<Scope>)**: <Files to create/modify> -> **Verification**: <Test/Check command>
3. **Slice 3 (<Scope>)**: <Files to create/modify> -> **Verification**: <Test/Check command>
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - Consumes stack and structure findings from [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`).
  - Consumes functional/non-functional specifications from [`requirements-analysis`](../requirements-analysis/SKILL.md) (`SKILL-02`).
- **Downstream Skills**:
  - Routes durable architectural choices to [`technical-decision-records`](../technical-decision-records/SKILL.md) (`SKILL-04`).
  - Routes implementation slices to [`ai-anti-slop`](../ai-anti-slop/SKILL.md) (`SKILL-05`) and [`adaptive-engineering`](../adaptive-engineering/SKILL.md) (`SKILL-06`).
  - Routes legacy decoupling slices to [`refactoring-legacy-safety`](../refactoring-legacy-safety/SKILL.md) (`SKILL-08`).
  - Routes schema design details to `database-architecture-integrity` (`SKILL-24`).

## 12. Source References

- Library Reference: [Technology Stack Detection & Adaptation Matrix](../../references/technology-stack-detection-matrix.md)
- Library Reference: [AI Anti-Slop & Engineering Craftsmanship Reference](../../references/anti-slop-engineering-reference.md) (`C-1`, `C-3`, Architectural Discipline)
- Reference: Martin Fowler, *Patterns of Enterprise Application Architecture* & *Strangler Fig Application* (`https://martinfowler.com/bliki/StranglerFigApplication.html`)
- Reference: [The Twelve-Factor App Methodology](https://12factor.net/)
