# UI/UX Design Systems & shadcn/ui Reference

> Primary Source:
> - **shadcn/ui Official Documentation**: https://ui.shadcn.com/docs

This reference provides decision rules and architectural guidance for integrating design systems—specifically detailing when and how to use **shadcn/ui** versus preserving an application's existing UI stack.

---

## 1. Compatibility Gate: When to Use (and Not Use) shadcn/ui

**CRITICAL RULE**: Never force `shadcn/ui` into an application that uses a different UI framework, styling system, or non-React stack unless the user explicitly asks to migrate or initialize it.

| Project Stack / Existing Setup | Action |
| :--- | :--- |
| **React / Next.js / Vite / Astro / Remix / React Router / TanStack Start / Laravel (React Inertia)** WITH `components.json` present | **Use shadcn/ui natively.** Inspect `components.json` for aliases (`@/components/ui`, `@/lib/utils`), base library (Radix UI or Base UI), icon library, and Tailwind CSS configuration. |
| **React + Tailwind CSS** WITHOUT `components.json` (greenfield or user requests component library) | **Recommend or initialize shadcn/ui** (`npx shadcn@latest init` / `pnpm dlx shadcn@latest init`) if appropriate for the task, or use existing project components if already established. |
| **React + MUI / Chakra UI / Mantine / Ant Design / Bootstrap** | **Do NOT use shadcn/ui.** Use the existing component library's primitives, theme tokens, and form patterns. |
| **Vue / Nuxt, Angular, Svelte, Solid** | **Do NOT use React shadcn/ui.** Use the framework's existing component system (or community ports like `shadcn-vue` / `shadcn-svelte` only if already present in `package.json`). |
| **Server-Rendered Templates (Laravel Blade/Livewire, CodeIgniter Views, Django Templates, Rails ERB, Go `html/template`)** | **Do NOT use shadcn/ui.** Use the project's native template components, CSS framework, and progressive enhancement stack (e.g., Alpine.js, HTMX, Stimulus, vanilla JS). |
| **Mobile / Desktop Native (Flutter, SwiftUI, Jetpack Compose, Qt, .NET MAUI)** | **Do NOT use web design systems.** Use Material 3 / Cupertino (Flutter), Human Interface Guidelines (iOS), or Material Design (Android). |

---

## 2. Core Principles of shadcn/ui (When Applicable)

1. **Open-Code Ownership**: Components are copied into the project source tree (typically `src/components/ui/` or `components/ui/`), not hidden inside `node_modules`. Customize behavior or styling by editing the component source or composing variants with `class-variance-authority` (`cva`) and `cn()` (`clsx` + `tailwind-merge`).
2. **Composable Interface**: Follow standard compound-component patterns (`Dialog` -> `DialogTrigger`, `DialogContent`, `DialogHeader`, `DialogTitle`, `DialogDescription`, `DialogFooter`). Never omit required accessibility subcomponents like `DialogTitle`.
3. **Design Tokens via CSS Variables**: Use semantic tokens (`bg-background`, `text-foreground`, `bg-primary`, `text-primary-foreground`, `bg-muted`, `text-muted-foreground`, `border-border`, `ring-ring`, `text-destructive`) rather than hardcoded Tailwind palette classes (`bg-slate-900`, `text-blue-500`) so light and dark themes work automatically (`R-34`).
4. **Headless Primitive Accessibility**: Preserve the underlying Radix UI or Base UI attributes (`aria-expanded`, `aria-controls`, `data-state`, keyboard handlers, focus trapping). Never strip focus-visible rings (`focus-visible:ring-2`).
5. **Forms & Validation**: Pair accessible `Field` / `Label` / `Input` / error message primitives with schema validation (`zod` + `react-hook-form` or TanStack Form), ensuring every input has a programmatic `<Label htmlFor>` (`R-39`), `aria-invalid`, and `aria-describedby` linking to the error message.
6. **CLI Component Addition**: When adding new primitives to a project configured with `components.json`, prefer the project's package manager (`pnpm dlx shadcn@latest add <component>`, `npx shadcn@latest add <component>`, `bunx shadcn@latest add <component>`) and verify changes in version control.

---

## 3. Universal Design System Standards (All Stacks)

Regardless of the underlying framework:
- **Token Consistency**: Define and reuse spacing, typography, border-radius, elevation, and color tokens via CSS custom properties, theme files, or framework config.
- **Four Mandatory View States (`R-27`)**:
  1. **Loading**: Skeleton or contextual progress indicator that preserves layout dimensions (`CLS` prevention) and announces loading state (`aria-busy="true"`).
  2. **Empty**: Explains why no records exist (first run vs. zero filter matches) and provides a primary action when applicable.
  3. **Error**: Explains what failed in plain language without leaking stack traces, and provides a retry or recovery path.
  4. **Success / Populated**: Structured around the primary decision or action the user performs on the screen (`C-3`).
- **Data Tables & Forms**:
  - Tables must reflect real domain columns, support keyboard navigation, handle horizontal overflow cleanly on small screens, and provide clear sort/filter states.
  - Forms must validate both client-side (for immediate feedback) and server-side (for security), preserve user input on validation failure, and prevent double submission while in flight.
