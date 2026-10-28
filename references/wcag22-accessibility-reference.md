# WCAG 2.2 Accessibility Engineering Reference

> Primary Source:
> - **W3C Web Content Accessibility Guidelines (WCAG) 2.2 Recommendation**: https://www.w3.org/TR/WCAG22/
> - Additional patterns adapted from `miqdadbadjuber/anti-slop` (`antislop-human`, MIT License) and `addyosmani/web-quality-skills` (MIT License).

This reference summarizes WCAG 2.2 Level A and Level AA requirements, contrast mathematics, semantic HTML patterns, and keyboard interaction contracts.

---

## 1. The Four POUR Principles & Key WCAG 2.2 Criteria

### A. Perceivable (Principle 1)
- **1.1.1 Non-text Content (A)**: Every informative `<img>`, `<svg>`, or icon control must have an accessible text alternative (`alt="..."` or `aria-label="..."`). Decorative images must have `alt=""` or `aria-hidden="true"`.
- **1.3.1 Info and Relationships (A)**: Use semantic landmarks (`<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`), sequential headings (`<h1>` to `<h6>` without skipping levels), `<label for="...">` for inputs, and `<th>` with `scope="col"` / `scope="row"` for tables.
- **1.3.5 Identify Input Purpose (AA)**: Provide appropriate `autocomplete` attributes (`email`, `username`, `current-password`, `new-password`, `given-name`, `tel`) on personal data inputs.
- **1.4.1 Use of Color (A)**: Never rely on color alone to convey status, required fields, or validation errors; always pair color with text, icons, or patterns.
- **1.4.3 Contrast Minimum (AA)**:
  - Normal text (`< 18pt` / `< 24px`, or `< 14pt` / `< 18.66px` bold): **>= 4.5:1**
  - Large text (`>= 24px` or `>= 18.66px` bold): **>= 3.0:1**
- **1.4.4 Resize Text (AA) & 1.4.10 Reflow (AA)**: Content must scale to 200% zoom and reflow at a `320px` CSS width without horizontal scrolling or clipped text (`overflow: hidden` traps). Never set `user-scalable=no` or `maximum-scale=1` in `<meta name="viewport">`.
- **1.4.11 Non-text Contrast (AA)**: Interactive control boundaries (inputs, buttons, focus rings, toggles) and graphical status segments must have **>= 3.0:1** contrast against adjacent backgrounds.
- **1.4.13 Content on Hover or Focus (AA)**: Custom tooltips/popovers triggered on hover/focus must be dismissible (`Escape`), hoverable (cursor can move onto the tooltip without it disappearing), and persistent.

### B. Operable (Principle 2)
- **2.1.1 Keyboard (A) & 2.1.2 No Keyboard Trap (A)**: Every interactive control must be reachable and operable via keyboard (`Tab`, `Shift+Tab`, `Enter`, `Space`, `Arrow` keys). Modal focus traps must release cleanly on close (`Escape`).
- **2.2.2 Pause, Stop, Hide (A)**: Auto-moving or blinking content lasting > 5 seconds must provide a pause/stop control; respect `@media (prefers-reduced-motion: reduce)`.
- **2.4.1 Bypass Blocks (A)**: Provide a "Skip to main content" link at the top of full pages alongside semantic landmarks.
- **2.4.3 Focus Order (A) & 2.4.7 Focus Visible (AA)**: DOM order must match visual reading order; every focusable element must display a clear `:focus-visible` indicator.
- **2.4.11 Focus Not Obscured — Minimum (AA) [New in WCAG 2.2]**: When an item receives keyboard focus, it must not be entirely hidden by sticky headers, fixed bottom navs, or cookie banners. Use `scroll-padding-top` and `scroll-padding-bottom`.
- **2.5.7 Dragging Movements (AA) [New in WCAG 2.2]**: Any operation that uses dragging (Kanban boards, sliders, sortable lists, file dropzones) must also provide a single-pointer/keyboard alternative (e.g., move up/down buttons or click-to-select).
- **2.5.8 Target Size — Minimum (AA) [New in WCAG 2.2]**: Interactive targets must be at least `24x24` CSS pixels (WCAG AA floor), while engineering best practice (`R-03`, WCAG 2.5.5 AAA) targets **`44x44` CSS pixels** on touch viewports.

### C. Understandable (Principle 3)
- **3.1.1 Language of Page (A)**: Root `<html>` element must declare a valid `lang` attribute (e.g., `<html lang="en">`).
- **3.2.6 Consistent Help (A) [New in WCAG 2.2]**: Help mechanisms repeated across pages must appear in the same relative order.
- **3.3.1 Error Identification (A) & 3.3.2 Labels or Instructions (A)**: Every form input requires a visible label; validation errors must identify the field in text and describe the error (`aria-invalid="true"`, `aria-describedby="field-error"`).
- **3.3.7 Redundant Entry (A) [New in WCAG 2.2]**: Multi-step workflows must not force users to re-type information already provided in the same session.
- **3.3.8 Accessible Authentication — Minimum (AA) [New in WCAG 2.2]**: Never block password paste (`onpaste="return false"` is forbidden), and support password managers (`autocomplete`) and WebAuthn/passkeys.

### D. Robust (Principle 4)
- **4.1.2 Name, Role, Value (A)**: Use native HTML elements (`<button type="button">`, `<a href="...">`, `<input>`, `<select>`, `<dialog>`). Never attach click handlers to bare `<div>` or `<span>` elements without role, `tabindex="0"`, and `keydown` (`Enter`/`Space`) handlers.
- **4.1.3 Status Messages (AA)**: Dynamic toast messages, filter counts, and async form errors must be announced via `role="status"` (`aria-live="polite"`) or `role="alert"` (`aria-live="assertive"`).

---

## 2. Deterministic Contrast Calculation Formula

Never guess or eyeball grey-on-grey or tinted text contrast. Compute relative luminance $L$:
1. For each RGB channel $C \in \{R, G, B\}$ in $[0, 255]$, normalize $c = C / 255$.
2. Linearize:
   - If $c \le 0.03928$, $c_{\text{lin}} = c / 12.92$
   - Else $c_{\text{lin}} = ((c + 0.055) / 1.055)^{2.4}$
3. Compute luminance: $L = 0.2126 R_{\text{lin}} + 0.7152 G_{\text{lin}} + 0.0722 B_{\text{lin}}$.
4. Compute contrast ratio between lighter luminance $L_1$ and darker luminance $L_2$:
   $$\text{Ratio} = \frac{L_1 + 0.05}{L_2 + 0.05}$$
5. Compare the **unrounded** ratio against `4.5` (normal text) or `3.0` (large text / UI boundaries). For example, `#777777` on `#FFFFFF` yields `4.48:1` and **FAILS** normal text AA.
