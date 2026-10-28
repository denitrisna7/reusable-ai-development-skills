# shadcn/ui Architecture, Tokens, and Component Patterns Reference

> Primary Source:
> - **shadcn/ui Official Documentation**: https://ui.shadcn.com/docs
> - **Anti-Slop UI Craftsmanship Rules**: `https://github.com/miqdadbadjuber/anti-slop` (`antislop-ui`, MIT License)

This reference defines implementation patterns for projects that pass the **shadcn/ui Compatibility Gate** (React / Next.js / Vite / Astro / Remix / React Router / TanStack Start / Laravel Inertia React with Tailwind CSS and `components.json`, or greenfield React + Tailwind CSS projects where `shadcn/ui` is explicitly requested).

---

## 1. Compatibility Gate Checklist

Before running `shadcn` CLI commands or importing `@/components/ui/*`:

1. **Check for `components.json`**:
   - Inspect `"style"`, `"rsc"`, `"tsx"`, `"tailwind.css"`, `"tailwind.cssVariables"`, and `"aliases"` (`components`, `utils`, `ui`, `lib`, `hooks`).
   - Identify the underlying headless primitive library (`radix-ui` or `@base-ui-components/react`) and icon set (`lucide-react`, `@radix-ui/react-icons`, `@tabler/icons-react`).
2. **Forbidden Stacks for `shadcn/ui`**:
   - React applications already standardized on Material UI (`@mui/material`), Mantine, Chakra UI, Ant Design, or Bootstrap.
   - Non-React SPA frameworks (Vue/Nuxt, Angular, Svelte, Solid) unless using their native ecosystem equivalent already installed in `package.json`.
   - Server-rendered templates (Laravel Blade/Livewire, CodeIgniter 3/4 views, Django/Jinja2 templates, Ruby on Rails ERB, Go `html/template`, ASP.NET Razor).
   - Native mobile or desktop frameworks (Flutter, SwiftUI, Jetpack Compose, React Native).

---

## 2. Design Token Architecture (`CSS Variables` + Tailwind)

Always style components using semantic token classes rather than hardcoded palette colors (`bg-slate-900`, `text-gray-500`) so light and dark modes (`R-34`) remain synchronized:

| Semantic Token Class | Purpose | Typical Pairing |
| :--- | :--- | :--- |
| `bg-background` / `text-foreground` | Primary page canvas and body text | Root layout, page containers |
| `bg-card` / `text-card-foreground` | Elevated cards, panels, summary surfaces | `Card`, dashboard panels |
| `bg-popover` / `text-popover-foreground` | Floating menus, comboboxes, tooltips, dropdowns | `PopoverContent`, `DropdownMenuContent`, `SelectContent` |
| `bg-primary` / `text-primary-foreground` | Primary call-to-action button, active brand indicators | Primary `<Button variant="default">` |
| `bg-secondary` / `text-secondary-foreground` | Secondary actions, subtle badges, filter chips | `<Button variant="secondary">`, `<Badge variant="secondary">` |
| `bg-muted` / `text-muted-foreground` | Subdued backgrounds, table headers, helper captions | Empty state backgrounds, `CardDescription`, form helper text (`>= 4.5:1` contrast) |
| `bg-accent` / `text-accent-foreground` | Hover/focus highlight inside menus and interactive rows | Menu items, command palette selections |
| `bg-destructive` / `text-destructive-foreground` | High-risk/irreversible actions and error states | Delete confirmations, `<Alert variant="destructive">` |
| `border-border` / `border-input` / `ring-ring` | Hairline dividers, form control borders, keyboard `:focus-visible` ring | Tables, cards, inputs, buttons |

---

## 3. Open-Code Component Composition (`cva` + `cn`)

1. **Extend Variants Cleanly**:
   - Use `cva` (`class-variance-authority`) in `components/ui/<component>.tsx` when adding project-wide visual variants (`size`, `intent`, `density`).
   - Always pass incoming `className` through `cn(variants({ variant, size }), className)` so consumers can override spacing or layout classes safely without specificity collisions.
2. **Preserve Accessibility Subcomponents**:
   - **Dialog / Sheet / AlertDialog**: Always render `<DialogHeader>`, `<DialogTitle>`, and `<DialogDescription>` inside `<DialogContent>`. If a visual title is intentionally hidden, wrap `<DialogTitle>` in `<VisuallyHidden>` rather than deleting it, or screen readers will fail WCAG 4.1.2.
   - **Icon-Only Buttons**: Every `<Button size="icon">` must declare `aria-label="Action name"` and contain `<Icon className="h-4 w-4" aria-hidden="true" />`.

---

## 4. Accessible Forms and Validation Pattern

Combine `Field` / `Form` primitives with schema validation (`zod` + `react-hook-form` or TanStack Form) and server-side error mapping:

- **Programmatic Association (`R-39`)**: Every `<Input>`, `<Textarea>`, `<SelectTrigger>`, or `<Checkbox>` must link to a visible `<Label htmlFor={id}>`.
- **Error Binding**: Set `aria-invalid={!!error}` on the control and `aria-describedby={`${id}-description ${id}-error`}` pointing to the helper text and error message element (`id={`${id}-error`}`, `role="alert"`).
- **In-Flight Submission Lock**: Disable or mark `aria-busy="true"` on the submit button while the request is pending, replacing or augmenting the label with contextual progress (`"Saving changes..."`).
- **Input Preservation**: Never clear form state when server or client validation fails; focus the first invalid field so keyboard and screen-reader users can recover immediately.

---

## 5. Data Table and Four-State View Pattern (`R-27`)

When building data tables (`@tanstack/react-table` + `components/ui/table.tsx`):

1. **Loading State**: Render skeleton rows matching the exact column count and row height (`aria-busy="true"`) to prevent Cumulative Layout Shift (`CLS`).
2. **Empty State**: Distinguish between:
   - *Zero domain records created yet*: Explain what the resource does and offer a primary creation CTA (e.g., `"Create first invoice"`).
   - *Zero filter/search matches*: Show the active query/filters and provide a `"Reset filters"` button.
3. **Error State**: Render a structured error panel naming what failed to load and providing a `"Try again"` action without exposing raw stack traces.
4. **Populated State**: Use semantic `<Table>`, `<TableHeader>`, `<TableHead scope="col">`, `<TableBody>`, and `<TableCell>`. Provide responsive horizontal scroll wrappers (`overflow-x-auto`) and keyboard-operable pagination and sorting controls.
