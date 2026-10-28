# WCAG 2.2 Level A, AA, and Selected AAA Engineering Checklist

> Primary Source:
> - **W3C Web Content Accessibility Guidelines (WCAG) 2.2 Recommendation**: https://www.w3.org/TR/WCAG22/
> - **Anti-Slop Human & Accessibility Rules**: `https://github.com/miqdadbadjuber/anti-slop` (`antislop-human`, MIT License)

Use this checklist during code review, static template auditing, and browser accessibility snapshot verification.

---

## 1. Principle 1: Perceivable

| Criterion | Level | Engineering Requirement | Verification Method |
| :--- | :--- | :--- | :--- |
| **1.1.1 Non-text Content** | A | Informative images/icons have concise `alt` or `aria-label`; decorative SVGs/images use `alt=""` or `aria-hidden="true"`. | Inspect `<img>`, `<svg>`, and icon `<button>` nodes in DOM/snapshot. |
| **1.3.1 Info and Relationships** | A | Page uses `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`; headings (`h1`-`h6`) follow hierarchy without skipping levels; tables use `<th scope="col\|row">`; form fields use `<label for>` or `<fieldset>`/`<legend>`. | Check heading outline and accessibility tree roles. |
| **1.3.2 Meaningful Sequence** | A | DOM order matches visual reading order (`flex-direction: row-reverse` or CSS Grid reordering does not scramble screen reader sequence). | Linearize page reading order. |
| **1.3.4 Orientation** | AA | Views are not locked to portrait or landscape unless essential. | Verify CSS/manifest orientation locks. |
| **1.3.5 Identify Input Purpose** | AA | Personal user inputs declare standard `autocomplete` tokens (`name`, `email`, `tel`, `username`, `current-password`, `new-password`, `street-address`, `cc-number`). | Inspect `<input autocomplete="...">`. |
| **1.4.1 Use of Color** | A | Status, required fields, active nav tabs, and form errors are never communicated by color alone (include text, icon, underline, or border change). | Test in grayscale mode. |
| **1.4.3 Contrast (Minimum)** | AA | Normal text (`< 24px` or `< 18.66px` bold) has `>= 4.5:1` contrast; large text (`>= 24px` or `>= 18.66px` bold) has `>= 3.0:1` contrast across all themes (`R-25`, `R-34`). | Run `python3 scripts/contrast-check.py <fg> <bg>`. |
| **1.4.4 Resize Text & 1.4.10 Reflow** | AA | Text scales to 200% and layout reflows at `320px` CSS width without 2D scrolling or clipped text (`overflow: hidden` traps). Never set `maximum-scale=1` or `user-scalable=no`. | Inspect `<meta name="viewport">` and test at `320px` width. |
| **1.4.6 Contrast (Enhanced)** | AAA | Normal text `>= 7.0:1`; large text `>= 4.5:1` (recommended for long-form reading and high-visibility medical/financial interfaces). | Run `python3 scripts/contrast-check.py <fg> <bg>`. |
| **1.4.11 Non-text Contrast** | AA | Interactive control borders (inputs, checkboxes, buttons, toggles), focus rings, and chart segments have `>= 3.0:1` contrast against adjacent surfaces. | Run `python3 scripts/contrast-check.py <border> <bg>`. |
| **1.4.12 Text Spacing** | AA | Layout tolerates line-height `1.5x`, paragraph spacing `2x`, letter spacing `0.12em`, and word spacing `0.16em` without clipping. | Avoid fixed pixel heights on text containers. |
| **1.4.13 Content on Hover or Focus** | AA | Custom tooltips/popovers are dismissible via `Escape`, hoverable with the pointer, and persistent until focus/hover leaves. | Test tooltip with keyboard `Tab` + `Escape` and mouse hover. |

---

## 2. Principle 2: Operable

| Criterion | Level | Engineering Requirement | Verification Method |
| :--- | :--- | :--- | :--- |
| **2.1.1 Keyboard & 2.1.2 No Keyboard Trap** | A | All interactive controls are reachable and operable via keyboard (`Tab`, `Shift+Tab`, `Enter`, `Space`, `Arrow` keys). Focus traps in modals release cleanly via `Escape`. | Traverse entire screen using only keyboard. |
| **2.1.4 Character Key Shortcuts** | A | Single-key shortcuts (e.g., pressing `s` or `/`) do not fire when focus is inside an editable input, or can be remapped/disabled. | Test typing inside inputs when shortcuts exist. |
| **2.2.2 Pause, Stop, Hide** | A | Auto-advancing carousels or animations lasting `> 5s` have pause controls and honor `@media (prefers-reduced-motion: reduce)`. | Emulate `reducedMotion: "reduce"`. |
| **2.4.1 Bypass Blocks** | A | Provide a visible-on-focus `"Skip to main content"` link targeting `<main id="main-content">`. | Press `Tab` once after page load. |
| **2.4.2 Page Titled** | A | Every route renders a descriptive, specific `<title>` element. | Inspect `document.title` across routes. |
| **2.4.3 Focus Order & 2.4.7 Focus Visible** | A / AA | Focus moves logically; every interactive element displays a high-contrast `:focus-visible` indicator (`outline: none` without replacement is forbidden). | Tab through all controls and inspect focus styles. |
| **2.4.4 Link Purpose** | A | Avoid ambiguous link text (`"Click here"`, `"Read more"` alone); provide context via visible text or `aria-label`. | Inspect all `<a>` elements in accessibility snapshot. |
| **2.4.11 Focus Not Obscured (Minimum)** | AA (2.2) | Focused elements are not completely covered by sticky headers, fixed footers, or floating banners (`scroll-padding-top` / `scroll-padding-bottom`). | Tab through full page with sticky bars active. |
| **2.4.13 Focus Appearance** | AAA (2.2) | Focus indicator is at least as large as a `2px` thick perimeter around the component with `>= 3.0:1` contrast change. | Inspect `:focus-visible` CSS rules. |
| **2.5.3 Label in Name** | A | If a control has visible text `"Search"`, its `aria-label` (if set) must contain the substring `"Search"` so voice-control users can activate it. | Compare visible text with `aria-label`. |
| **2.5.7 Dragging Movements** | AA (2.2) | Any drag-and-drop interaction (Kanban cards, sliders, sortable lists) provides a single-pointer click or keyboard alternative. | Verify non-drag action controls exist. |
| **2.5.8 Target Size (Minimum) & 2.5.5 (Enhanced)** | AA (2.2) / AAA | Interactive targets are at least `24x24px` (WCAG 2.2 AA floor) and `44x44px` on touch/mobile viewports (`R-03`, WCAG 2.5.5 AAA). | Measure bounding boxes (`boxes: true` in Playwright snapshot). |

---

## 3. Principle 3: Understandable

| Criterion | Level | Engineering Requirement | Verification Method |
| :--- | :--- | :--- | :--- |
| **3.1.1 Language of Page & 3.1.2 Language of Parts** | A / AA | Root `<html lang="...">` is set; inline passages in another language declare `lang="..."`. | Inspect `<html lang>` attribute. |
| **3.2.6 Consistent Help** | A (2.2) | Help links, contact details, or support widgets appear in the same relative DOM order across pages. | Compare layout templates across views. |
| **3.3.1 Error Identification & 3.3.2 Labels/Instructions** | A | Every input has a visible `<label>`; invalid fields set `aria-invalid="true"` and link to a specific error message via `aria-describedby`. | Submit invalid form and inspect ARIA attributes. |
| **3.3.7 Redundant Entry** | A (2.2) | Multi-step wizards auto-populate or allow selecting previously entered data (e.g., `"Same as shipping address"`). | Step through multi-page forms. |
| **3.3.8 Accessible Authentication (Minimum)** | AA (2.2) | Never block paste (`onpaste` blocking forbidden) on password/code fields; support password managers and copy-pasteable 2FA codes. | Verify paste works in login/2FA fields. |

---

## 4. Principle 4: Robust

| Criterion | Level | Engineering Requirement | Verification Method |
| :--- | :--- | :--- | :--- |
| **4.1.2 Name, Role, Value** | A | Use native `<button>`, `<a href>`, `<input>`, `<select>`, `<dialog>`. Custom widgets implement full WAI-ARIA role, state (`aria-expanded`, `aria-selected`, `aria-checked`), and keyboard contracts. | Inspect accessibility tree snapshot. |
| **4.1.3 Status Messages** | AA | Toasts, async search results counts, and form submission alerts use `role="status"` (`aria-live="polite"`) or `role="alert"` (`aria-live="assertive"`). | Verify live region attributes in DOM. |
