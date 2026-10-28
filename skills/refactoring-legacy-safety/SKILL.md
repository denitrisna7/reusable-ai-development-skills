---
name: refactoring-legacy-safety
description: "Guides safe, incremental refactoring and modification of legacy or tightly coupled codebases by characterizing existing behavior first, preserving backward compatibility, minimizing blast radius, and verifying regression tests. Activate when restructuring code, removing dead code, or modernizing legacy modules. Do not use for greenfield feature architecture."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-08"
  category: "Core Development Quality"
---

# Refactoring & Legacy Code Safety

This skill governs the safe modification, decoupling, cleanup, and incremental modernization of existing and legacy codebases. It prevents accidental regressions by requiring engineers to characterize and verify existing runtime behavior (including subtle side effects and implicit contracts) before changing structure. Every refactoring step prioritizes backward compatibility, minimal blast radius, regression test coverage, careful verification before removing suspected unused code, and avoiding risky big-bang rewrites.

## 1. Activation Conditions

Activate this skill under any of the following scenarios:
- Refactoring existing classes, functions, controllers, database queries, or UI components to improve readability, testability, or maintainability without altering external behavior.
- Adding a bug fix or new capability inside a fragile, tightly coupled, or poorly tested legacy module ("god classes", long procedural controllers, deeply nested scripts).
- Extracting shared modules, introducing dependency seams, or migrating a legacy component toward a newer project pattern incrementally.
- Investigating and safely removing suspected dead code, unused routes, orphaned methods, or deprecated feature flags.
- Evaluating migration risks before upgrading framework patterns, ORM layers, or internal APIs.

## 2. When Not to Use

Do not use this skill in the following situations:
- Designing a brand-new, greenfield module that has no existing callers or legacy constraints; use [`adaptive-architecture`](../adaptive-architecture/SKILL.md) (`SKILL-03`) and [`adaptive-engineering`](../adaptive-engineering/SKILL.md) (`SKILL-06`).
- Changing intentional business requirements or user-visible functionality without first specifying those behavior changes via [`requirements-analysis`](../requirements-analysis/SKILL.md) (`SKILL-02`).
- Performing database schema expansions/contractions in isolation; pair with `database-architecture-integrity` (`SKILL-24`).
- Upgrading third-party package versions in manifest/lockfiles; pair with [`dependency-supply-chain-security`](../dependency-supply-chain-security/SKILL.md) (`SKILL-09`).

## 3. Scope and Objectives

Every legacy modification or refactoring task must explicitly cover the following eight safety disciplines:
- **Understanding existing behavior before modification**: Tracing all callers, inputs, outputs, database mutations, session/global state side effects, and error behaviors before altering a single line.
- **Preserving backward compatibility**: Maintaining public method signatures, return payload shapes, HTTP routes, webhook contracts, database column names, and serialized job formats unless an explicit migration plan is approved.
- **Regression testing**: Running existing tests first and writing characterization tests ("golden master" or behavior-pinning tests) when test coverage around the target code is missing or weak.
- **Incremental refactoring**: Decomposing structural changes into small, atomic steps (Extract Method, Sprout Class, Wrap Method, Branch by Abstraction, Strangler Fig) verified after every step.
- **Identifying unused code carefully**: Proving that suspected dead code is unreachable across static references, dynamic dispatch/reflection, string-based route/container bindings, templates, cron jobs, and external consumers before deletion.
- **Avoiding unnecessary rewrites**: Resisting the temptation to rewrite working, battle-tested legacy code merely because its style differs from personal preference.
- **Minimizing change scope**: Separating structural refactoring commits/steps from functional behavior changes and avoiding drive-by formatting edits in unrelated files.
- **Evaluating migration risks**: Assessing blast radius, rollback complexity, in-flight queue/session compatibility, and performance impact before executing structural transitions.

## 4. Prerequisites and Context Requirements

- Repository stack and test runner inventory from [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`).
- Read access to the entire repository to search for both static and dynamic callers of the target code.
- A clean or known working tree baseline (`git status`, `git diff`) so any unintended regression can be reverted immediately.

## 5. Step-by-Step Workflow

Execute this six-step safety procedure whenever refactoring or modifying legacy code:

### Step 1: Map the Blast Radius and Characterize Existing Behavior
1. Locate all direct and indirect callers of the target function, class, route, or component across the codebase.
2. Document the current contract, including non-obvious quirks that callers may depend on:
   - Input types, default parameter values, and tolerated malformed inputs.
   - Return types, array/JSON key ordering, null vs. empty-collection behavior, and HTTP status codes.
   - Side effects: database writes, cache invalidations, session mutations, emitted events, global variables, or file I/O.
3. Separate **pure structural refactoring** (zero external behavior change) from **functional bug fixes or enhancements**. Never mix an unrequested architectural rewrite into a targeted bug fix.

### Step 2: Establish a Regression Safety Net (Characterization Tests)
1. Execute the existing test suite covering the target module to verify the baseline passes before making edits.
2. If the legacy code lacks automated tests:
   - Write focused **characterization tests** that exercise the main execution paths, edge cases, and error branches of the existing code and assert its current actual outputs.
   - If the code is too tightly coupled to instantiate in a unit test (e.g., hardcoded static database calls or global state), test through the nearest stable seam (HTTP controller/integration test or CLI harness) first, then introduce a minimal constructor/parameter seam using **Sprout Method**, **Sprout Class**, or **Extract and Override Call**.

### Step 3: Evaluate Migration Risks and Preserve Backward Compatibility
1. Check whether external or asynchronous consumers depend on the target code:
   - **Serialized Jobs / Events in Queue**: Renaming a queued Job class or changing its constructor properties in PHP/Python/Node can cause in-flight Redis/SQS jobs to fail during deployment. Keep compatibility shims or default values during transition.
   - **Public API & Webhook Payloads**: Preserve existing JSON keys and status codes; add new fields additively rather than renaming or deleting active fields.
   - **Public Library / Module Signatures**: When changing a method signature called across many files, consider keeping an adapter overload or default parameter so existing callers continue working while migrating incrementally.

### Step 4: Execute Atomic, Incremental Refactoring Steps
1. Perform one small, behavior-preserving transformation at a time:
   - **Extract Function / Method**: Isolate a cohesive block of logic with explicit inputs and outputs.
   - **Guard Clauses**: Flatten deeply nested legacy conditionals one branch at a time.
   - **Introduce Parameter / Seam**: Pass a dependency as an optional parameter defaulting to the existing concrete implementation so legacy callers do not break while tests can inject a fake.
   - **Strangler Fig**: Route new behavior to a clean new module while keeping legacy paths intact until verified.
2. Run the characterization tests and static analyzer after **every** step. If a test fails, fix or revert immediately before proceeding to the next step.

### Step 5: Verify Suspected Dead Code Before Removal
Never delete a function, class, route, CSS rule, or database column based solely on a single static IDE reference check. Before removing suspected unused code, verify all six dynamic vectors:
1. **Static Symbol Search**: Grep for the exact identifier across the entire workspace.
2. **Dynamic / Reflection / String Dispatch**: Check for string concatenation or reflection calls (`call_user_func`, `$container->make()`, `getattr()`, `importlib`, Symfony/Laravel service container bindings, route controller strings `'UserController@index'`, magic `__call` / `__get` methods, ORM model observers/events, or serialization hooks).
3. **Templates & Views**: Search Blade (`.blade.php`), Twig, PHP views, JSX/TSX, Vue SFCs, and dynamic CSS class builders.
4. **Configuration, Crons & CI**: Search `config/`, `routes/`, `crontab`, `Supervisor` configs, `Makefile`, and `.github/workflows/`.
5. **Database & Queue Artifacts**: Check whether old migrations, seeders, or queued job payloads reference the class.
6. If any dynamic vector is uncertain, keep the code, mark it `@deprecated` with the reason, or ask the user before deleting.

### Step 6: Run Post-Refactoring Verification Gate
1. Run [`code-quality-static-analysis`](../code-quality-static-analysis/SKILL.md) (`SKILL-07`) and all relevant unit, integration, and browser regression tests.
2. Inspect `git diff` line by line to confirm that change scope is minimal, no unrelated files were touched, and every behavioral invariant is preserved.

### Legacy Safety & Refactoring Checklist
- [ ] All static and dynamic callers traced before modifying target code.
- [ ] Existing behavior, side effects, and return contracts documented.
- [ ] Baseline tests executed (or characterization tests added where coverage was missing).
- [ ] Backward compatibility preserved for APIs, callers, sessions, and in-flight queued jobs.
- [ ] Changes applied in small, incremental steps rather than a risky rewrite.
- [ ] Suspected dead code verified against dynamic dispatch, config, and template vectors before deletion.
- [ ] Minimal `git diff` blast radius confirmed and all regression tests passing.

## 6. Technology-Specific Adaptation Rules

Account for ecosystem-specific legacy and dynamic-dispatch hazards:
- **PHP (Laravel / CodeIgniter / Legacy PHP)**:
  - Watch out for magic methods (`__get`, `__set`, `__call`, `__callStatic`), Eloquent dynamic accessors/mutators (`getFooAttribute` -> `$model->foo`), dynamic query scopes (`scopeActive` -> `::active()`), Facades, Service Provider container bindings, string-based route actions, and CodeIgniter `$this->load->library('foo')` dynamic property injection.
  - Preserve loose vs. strict comparison behavior (`==` vs `===`) carefully when legacy code compares numeric strings (e.g., database IDs returned as strings vs. integers) until covered by tests.
- **JavaScript / TypeScript (React / Next.js / Vue / Node)**:
  - Watch out for dynamic property indexing (`obj[key]`), implicit truthy/falsy coercion (`0` or `""` vs `null`/`undefined`), barrel file (`index.ts`) re-exports, and React component prop spreading (`{...props}`).
- **Python (Django / FastAPI / Legacy Python)**:
  - Watch out for `getattr()` / `setattr()`, `**kwargs` pass-throughs, Django signal receivers (`@receiver(post_save)`), metaclass registrations, Celery task string names (`@shared_task(name=...)`), and template tag dynamic lookups.
- **Go / Rust / Java / C# (.NET)**:
  - In Java/Spring and C#/.NET, check reflection, DI container auto-scanning (`@ComponentScan`, `@EventListener`), Jackson/JSON reflection serialization, and JPA entity lifecycle callbacks (`@PrePersist`) before removing seemingly unused methods or constructors.

## 7. Security and Safety Considerations

- **Never Weaken Security Controls During Refactoring**: When extracting or simplifying legacy controllers or middleware, verify that authentication guards, RBAC/ownership checks, CSRF validation, and SQL parameter bindings remain intact on every execution path.
- **Preserve Audit & Financial Precision**: In billing, accounting, or audit-logging code, never alter rounding modes, decimal precision (`bcmath`, `Decimal`, integer cents), or transaction ordering during a structural cleanup.

## 8. Verification Criteria

A refactoring or legacy modification is complete and verified only when:
1. All pre-existing tests and newly added characterization/regression tests pass (`PASS` with recorded output).
2. Public contracts, return structures, and side effects match the pre-refactoring baseline (unless an explicit requirement change was requested and tested).
3. Any deleted code has documented grep/search evidence confirming zero static or dynamic callers.
4. `git diff` shows a tightly scoped change with zero unrelated formatting noise.

## 9. Failure Handling and Edge Cases

- **Untestable Legacy Code with No Safe Seam**: If a legacy script executes side effects on file import or directly inside a global script without functions, first wrap the script body in a callable function without changing a single line inside it, verify syntax, and then write characterization tests against that function before refactoring internals.
- **Discovery of a Latent Bug During Pure Refactoring**: If you uncover an existing bug while performing a behavior-preserving refactor, do **not** silently alter behavior if callers might depend on it. Document the latent bug, isolate it, and either fix it in a separate, explicitly tested step or ask the user if the behavior appears intentional.
- **Regression Detected Mid-Refactor**: Immediately revert to the last known green state (`git checkout -- <file>` or undo the failing step) rather than stacking speculative fixes on top of a broken intermediate state.

## 10. Expected Outputs and Reporting Requirements

Report every refactoring or legacy modification using the following template:

```markdown
## Legacy Refactoring & Safety Report

### 1. Behavior Characterization & Blast Radius
- **Target Module(s)**: `<paths>`
- **Identified Callers & Consumers**: `<Static callers, routes, dynamic/queue consumers>`
- **Preserved Contracts & Invariants**: `<Signatures, payload shapes, side effects preserved>`

### 2. Incremental Steps & Dead-Code Verification
1. `<Step 1: e.g., Added characterization test covering X and Y>`
2. `<Step 2: e.g., Extracted method/class while keeping backward-compatible signature>`
3. `<Dead Code Check (if applicable)>`: `<Verified 0 static, reflection, route, or template references>`

### 3. Regression & Compatibility Verification
- **Characterization / Regression Tests**: `<Command + PASS result>`
- **Static Analysis & Diff Scope**: `<Command + PASS result; confirmed minimal diff>`
- **Residual Migration Risks**: `<None, or explicit notes on in-flight queues/clients>`
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**:
  - Uses repository topology from [`project-discovery`](../project-discovery/SKILL.md) (`SKILL-01`) and target architecture from [`adaptive-architecture`](../adaptive-architecture/SKILL.md) (`SKILL-03`).
- **Companion & Downstream Skills**:
  - Pairs with [`adaptive-engineering`](../adaptive-engineering/SKILL.md) (`SKILL-06`) and [`code-quality-static-analysis`](../code-quality-static-analysis/SKILL.md) (`SKILL-07`) for language idioms and static verification.
  - Pairs with `backend-testing-tdd` (`SKILL-16`) and `playwright-mcp-browser-qa` (`SKILL-17`) to build and execute regression test suites.

## 12. Source References

- Reference: Michael Feathers, *Working Effectively with Legacy Code* (Characterization Tests, Sprout Method/Class, Wrap Method, Seams)
- Reference: Martin Fowler, *Refactoring: Improving the Design of Existing Code* (`https://refactoring.com/`)
- Reference: Martin Fowler, *Branch by Abstraction* (`https://martinfowler.com/bliki/BranchByAbstraction.html`)
