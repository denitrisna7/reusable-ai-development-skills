# Anti-Slop 40 Mandatory Rules (`R-01` to `R-40`) & Specialized Checklists

> Adapted from **Anti Slop: Rules for AI Coding Agents** (`https://github.com/miqdadbadjuber/anti-slop`, commit `13883c779a45291b005c6b1a29e06c0c26715223`), Copyright (c) 2026 Miqdad Badjuber, licensed under the MIT License.

This reference provides the complete 40-rule catalog (`R-01` through `R-40`) organized both by rule number and by enforcement tier (**Tier 1: Hard Gate**, **Tier 2: Purpose-Gate**, **Tier 3: Quality Locks**), along with the Code Comment (`antislop-code`) and Copywriting (`antislop-copywriting`) patterns.

---

## 1. Complete 40-Rule Catalog (`R-01` through `R-40`)

| Rule ID | Title | Enforcement Tier | Mandatory Requirement / Prohibition | Verification & Dose Cap |
| :--- | :--- | :--- | :--- | :--- |
| **`R-01`** | Color & Gradients | Tier 2: Purpose-Gate | Forbidden as default without purpose: blue-to-purple, blue-to-cyan, purple-to-pink gradients, neon glows, radial orbs, purple-and-black defaults. | Allowed only when rooted in brand identity or a stated visual hierarchy goal (reason written in 1 line). |
| **`R-02`** | Copywriting (Em Dash) | Tier 1: Hard Gate | Forbidden: mechanical em-dash character (`—`) in agent-generated UI copy, documentation, and prose. | Replace with commas, periods, colons, or parentheses. User voice samples with em dashes follow `R-37` conflict confirmation. |
| **`R-03`** | Mobile Responsiveness | Tier 1: Hard Gate | Required: zero horizontal overflow, no text escaping containers, no colliding/clipped cards, minimum `44x44px` tap targets. | Verify across mobile (`320px-480px`), tablet (`600px-1024px`), and desktop viewports. |
| **`R-04`** | Icons | Tier 2: Purpose-Gate | Forbidden as default without purpose: generic AI icons (Sparkle, Star, Magic, Lightning, Diamond, Orb, Robot) or default thin-stroke sets used purely by habit. | Every icon must be genuinely relevant to its content, with relevance written down; omit icons when none fit. |
| **`R-05`** | Layout & Page Structure | Tier 3: Quality Locks | Forbidden: default AI templates (`Hero + 3 cards`, forced 3-step `How It Works`, default bento mosaic, fake terminal hero, 3-column pricing default, generic `Trusted By` bar, 4-column template footer, uniform section rhythm). | Structure must follow actual product content (`C-3`) and match the declared `RHYTHM` dial (`1`, `2`, or `3`). |
| **`R-06`** | Typography | Tier 2: Purpose-Gate | Forbidden as default without purpose: large monospace headings for fake "terminal" feel or uppercase wide-tracking labels (`HOW IT WORKS`). | Choose typefaces for brand character and readability, and record the 1-line reason (`R-31`). |
| **`R-07`** | Background | Tier 2: Purpose-Gate | Forbidden as default without purpose: grid squares, blueprint lines, graph paper, or dot matrices. | Allowed only when supporting the product's specific visual identity with a written reason. |
| **`R-08`** | Button Arrows | Tier 2: Purpose-Gate | Forbidden as default without purpose: decorative arrows (`->`, `↗`) appended to every CTA button. | Allowed selectively when proportional and serving a clear directional purpose (written down). |
| **`R-09`** | Badges | Tier 2: Purpose-Gate | Forbidden as default without purpose: capsule pills reading `"AI Powered"`, `"Beta"`, `"New"`, `"Secure"`, `"Fast"`, or eyebrow badges above H1 repeating the headline. | Allowed only for real functional status or labels; never stack pill + thin border + glow + dot + uppercase simultaneously. |
| **`R-10`** | Glassmorphism | Tier 2: Purpose-Gate | Glassmorphism (`backdrop-filter: blur`) is an accent only, never the default treatment of the entire UI. | **Dose cap**: maximum 1 to 2 elements. Forbidden on navbar + cards + modals + sidebar simultaneously. |
| **`R-11`** | Border Radius | Tier 3: Quality Locks | Forbidden: making every element pill-shaped (`9999px` on buttons, cards, inputs, badges, modals alike). | Use radius variation deliberately as part of the design system hierarchy. |
| **`R-12`** | Shadow | Tier 2: Purpose-Gate | Forbidden as default without purpose: large soft shadows on every component making the whole page float. | Use shadows selectively as elevation markers and write the elevation reason down. |
| **`R-13`** | Glow | Tier 2: Purpose-Gate | Forbidden as default without purpose: glow applied across cards, buttons, badges, icons, backgrounds, and borders at once. | **Dose cap**: maximum 1 to 2 focal elements with written hierarchy intent. |
| **`R-14`** | Feature Cards | Tier 2: Purpose-Gate | Forbidden as default without purpose: copy-paste feature cards with identical size, height, icon, padding, and layout. | Vary presentation to match content weight; not every feature belongs inside a card. |
| **`R-15`** | Call to Action (CTA) | Tier 3: Quality Locks | Forbidden: generic default CTAs (`"Get Started"`, `"Learn More"`, `"Try Now"`, `"Explore"`, `"Discover"`). | Write action-specific CTAs tied to product context (e.g., `"Create Free Workspace"`, `"Run Live Query"`). |
| **`R-16`** | Copywriting & Buzzwords | Tier 3: Quality Locks | Forbidden: AI marketing buzzwords (`"AI Powered"`, `"Next Generation"`, `"Revolutionary"`, `"Seamless"`, `"Cutting Edge"`, `"Intelligent"`, `"Ultimate"`, `"Powerful"`, `"Effortless"`). | Replace with concrete, specific language describing actual system behavior and benefits. |
| **`R-17`** | Data & Numbers | Tier 1: Hard Gate | Forbidden: invented numbers and unverified statistics (`"10K+ Users"`, `"99.9% Uptime"`, `"500M Requests"`). | Show no numbers if real data is unavailable, or use an explicit `[REAL DATA]` placeholder. |
| **`R-18`** | Testimonials | Tier 1: Hard Gate | Forbidden: fictional customer reviews, random names, invented job titles, or AI-generated avatars. | Omit the testimonials section entirely if no real, verifiable social proof exists. |
| **`R-19`** | Animations | Tier 2: Purpose-Gate | Forbidden as default without purpose: applying `Fade Up` + `Floating` + `Scale` + `Bounce` across every element. | Tie motion to a clear UX purpose (written down) and match the declared `MOTION` dial (`1`, `2`, or `3`). |
| **`R-20`** | Visual Identity | Tier 3: Quality Locks | Required: the interface must retain distinct visual character even if the logo and product name are swapped out. | Establish identity through deliberate palette, typography, and composition choices (`C-1`). |
| **`R-21`** | Dark Mode | Tier 3: Quality Locks | Forbidden: defaulting to a dark theme solely because "dark looks tech", or using this rule as an excuse to skip requested theme support. | Choose theme based on brand/user context; if shipping a light/dark toggle, both modes must work (`R-34`). |
| **`R-22`** | Illustrations | Tier 2: Purpose-Gate | Forbidden as default without purpose: generic Undraw, Storyset, or 3D blob character illustrations unrelated to the product. | Use real product views, purposeful diagrams, or no illustration at all. |
| **`R-23`** | Clarification & Visual Assets | Tier 1: Hard Gate | Required: ask for confirmation or use explicit honest placeholders (`[LOGO]`, `[REAL DATA]`, initial avatars) before creating unrequested logos, photos, stats, or nav structures. | Never disguise assumed or generated placeholder assets as final deliverables. |
| **`R-24`** | Navigation | Tier 1: Hard Gate | Forbidden: navbar or footer links pointing to pages or anchor sections that do not exist (`href="#"` dead links). | Every nav item must resolve to a real route/section or carry a visible `"Coming soon"` label. |
| **`R-25`** | Color Contrast | Tier 1: Hard Gate | Required: WCAG AA minimum contrast (`4.5:1` normal text, `3.0:1` large text `18px+` or `14px+` bold, `3.0:1` UI components). | Forbidden: light grey on grey, or white text over light gradient regions. Verify across the full background area. |
| **`R-26`** | Interactive Elements | Tier 1: Hard Gate | Required: every button, link, modal, toggle, tab, or form must execute real behavior or be removed. | Placeholders require **both** a code `// TODO` comment with task context and a visible `"Coming soon"` UI label. |
| **`R-27`** | UI States | Tier 1: Hard Gate | Required: every data-displaying UI must implement **Empty**, **Loading**, and **Error** states alongside the happy path. | Error states must name what failed and provide the user's next recovery action. |
| **`R-28`** | FAQ | Tier 1: Hard Gate | Forbidden: generic template FAQ sections (`"Is my data secure?"`, `"Can I cancel anytime?"`) detached from real product specifics. | Omit the FAQ section if real user questions for the domain are unknown. |
| **`R-29`** | Color Palette | Tier 3: Quality Locks | Required: cap active color palette to at most `2-3 core colors + 1 accent color` (excluding neutrals white/black/grey). | Forbidden: 5 to 7 uncoordinated colors on a single page without a design system. |
| **`R-30`** | Do Not Clone Popular Products | Tier 3: Quality Locks | Forbidden: mimicking the overall visual identity of Linear, Vercel, Stripe, Notion, or Apple unless explicitly requested by the user. | Use external products as taste/energy anchors only, never as copy-paste templates. |
| **`R-31`** | Every Decision Must Have a Reason | Tier 3: Quality Locks | Required (Keystone Rule): write a concise 1-line reason for every major color, layout, typography, spacing, card, and icon choice. | If a decision cannot be justified in one line beyond "AI default", rework or remove it. |
| **`R-32`** | Keyboard Accessibility | Tier 1: Hard Gate | Required: full keyboard operability (`Tab`, `Shift+Tab` in visual order, `Enter`/`Space` activation, `Escape` closes modals) and visible focus indicators. | Forbidden: `outline: none` or `outline: 0` without a high-contrast custom `:focus-visible` indicator. |
| **`R-33`** | No File/CSS Patching via Scripts | Tier 1: Hard Gate | Forbidden: implementing or mutating source code or CSS via external regex/string-replacement scripts left in the repository. | Edit canonical source and stylesheet files directly. |
| **`R-34`** | Every Theme You Ship Must Work | Tier 1: Hard Gate | Required: if a light/dark theme toggle or multi-theme setup is shipped, every supported mode must be fully functional and contrast-verified. | Forbidden: shipping a theme mode where typography, borders, or contrast break. |
| **`R-35`** | Verify Before You Deliver | Tier 1: Hard Gate | Required: build/run the application, inspect console errors, and verify every interactive element across themes and mobile breakpoints before claiming completion. | Record an element-by-element verification log; if execution is impossible, explicitly state code-inspection-only status. |
| **`R-36`** | No Fabricated Claims | Tier 1: Hard Gate | Forbidden: inventing security/compliance badges (`"SOC 2"`, `"ISO 27001"`), unmeasured performance multipliers (`"300% faster"`), or fake customer counts. | Present only verified facts backed by repository or measurement evidence (`C-5`). |
| **`R-37`** | Design Direction Required | Tier 1: Hard Gate | Required: load `DESIGN.md` or existing project design tokens before building UI. | If no direction exists and the user cannot be asked, label output `"draft without direction"` with dials `ENERGY 1 / RHYTHM 1 / MOTION 1`. |
| **`R-38`** | Real Content or Honest Placeholder | Tier 1: Hard Gate | Required: every statistic, feature, quote, nav item, or team member must be real or an unmistakable placeholder (`[REAL DATA]`, `"Coming soon"`). | Forbidden: realistic-looking fabricated filler content (`John Doe`, `Sarah Chen`, fake company logos). |
| **`R-39`** | Accessible Semantics & Affordances | Tier 1: Hard Gate | Required: native `<button>` for actions and `<a href>` for navigation; `cursor: pointer` on enabled controls (`not-allowed` when disabled); `aria-label` on icon buttons; `<label>` on inputs; `alt` on images; `prefers-reduced-motion: reduce` support; whole HTML documents must have `<html lang>`, `<title>`, landmarks, single `<h1>`, and never disable zoom (`user-scalable=no`). | Forbidden: clickable `<div>`/`<span>` controls or ARIA attributes that contradict native semantics. |
| **`R-40`** | Performance Mechanisms | Tier 1: Hard Gate | Required: explicit `width`/`height` or `aspect-ratio` on `<img>`, `<video>`, `<iframe>`; hero `<img>` uses `fetchpriority="high"` and never `loading="lazy"`; no render-blocking third-party scripts in `<head>`. | Forbidden: reporting Lighthouse or Core Web Vitals numbers that were not actually measured (`"not measured"` if unrun). |

---

## 2. Specialized Code Comment Hygiene (`antislop-code`)

Apply these rules whenever writing, reviewing, or cleaning up comments in source code:

| Slop Comment Pattern | Tell / Warning Sign | Required Fix |
| :--- | :--- | :--- |
| **Decorative Separators** | Banner lines of `=`, `-`, `*`, box-drawing chars, or ALL CAPS section headers (`// ======== AUTH ========`). | Remove entirely or replace with a single plain sentence-case comment if context is needed (`R-31`). |
| **Restating the Obvious** | Comments repeating the code (`// Increment counter` above `count++`, `// User class` above `class User`). | Delete the comment; leave the code self-explanatory. |
| **Workflow Narration** | Numbered step narration inside functions (`// Step 1: Validate`, `// Step 2: Save`, `// First... Next...`). | Delete step narration; extract helper functions only if control flow is genuinely complex. |
| **Empty Category Labels** | Generic headers carrying zero domain facts (`// Main logic`, `// Helper functions`, `// Business logic`). | Delete unless replaced by a specific invariant (`// Retries happen only on HTTP 502/503/504`). |
| **Vague Placeholders** | Unactionable TODOs (`// TODO: Improve this`, `// Future optimization here`). | Delete vague notes; keep a `TODO` only when it names a concrete task, constraint, or ticket. |
| **Signature Echo** | Docblocks (`JSDoc`, `PHPDoc`, docstrings) that merely repeat parameter and return names (`@param id The id`). | Remove redundant echo lines; document non-obvious domain rules, units, side effects, and thrown errors. |
| **Decorative Emoji & End Markers** | Emoji in comments (`// ✅ Validated`, `// 🚀 Fast path`) or closing brace tags (`} // end if`). | Strip decorative emoji and redundant closing markers. |
| **Over-Explained Paragraphs** | Multi-sentence essays explaining a one-line constraint or historical bug narrative. | Compress to 1 line (maximum 2 lines when two distinct facts exist) stating the active constraint directly. |

**Comments to Always Preserve**: Business intent, architectural trade-offs, security invariants, concurrency/locking rules, protocol edge cases, regulatory rules, third-party bug workarounds, and license headers.

---

## 3. Specialized Copywriting & Prose Hygiene (`antislop-copywriting`)

Apply these rules whenever generating UI copy, documentation, release notes, or technical prose:

1. **Eliminate Empty AI Vocabulary (`R-16`, `R-36`)**: Strip *unlock, elevate, empower, delve, showcase, testament, landscape, journey, game-changer, next-level, seamless, cutting-edge, revolutionary*. State what the software actually does.
2. **Eliminate Significance Inflation & Weasel Attributions**: Replace *"marking a pivotal moment"* or *"Experts say"* with concrete, sourced facts or omit the claim (`C-5`).
3. **Eliminate Chatbot Closers & Signposting**: Never leave *"I hope this helps!"*, *"Let's dive in"*, or *"Here's what you need to know"* in deliverables.
4. **Use Active Voice with Named Actors (`R-02`, `R-16`)**: Avoid actorless passive (*"the configuration was updated"*) and inanimate subjects given human mental verbs (*"the dashboard understands your goals"*).
5. **Break Mechanical Rhythm Tells (`R-05`, `R-36`)**: Avoid forcing every concept into a Rule-of-Three list, negative parallelisms (*"It's not just X, it's Y"*), staccato fragment chains, or false ranges (*"from onboarding to scale"*).
6. **Markdown Hygiene**: Avoid mechanical bolding of every noun phrase, scare-quote clusters, inline-header bullet habits where the bold prefix repeats the sentence, and decorative heading emojis.
