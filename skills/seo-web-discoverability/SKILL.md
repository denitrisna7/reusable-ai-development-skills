---
name: seo-web-discoverability
description: "Audits and implements titles, meta descriptions, canonical URLs, sitemaps, robots directives, Open Graph, and JSON-LD for public pages. Use for public web SEO. Do not index private admin apps."
license: "MIT"
compatibility: "Antigravity (App, CLI, IDE) and Agent Skills 1.0 compatible agents"
metadata:
  author: "reusable-ai-development-skills"
  version: "1.0.0"
  skill_id: "SKILL-36"
  category: "Performance, Operations, and Deployment"
---

# SEO & Web Discoverability

This skill governs technical Search Engine Optimization (SEO), social sharing metadata, crawlability, structured data (`JSON-LD`), and public-page discoverability for web applications. Crucially, it enforces strict boundary discipline between public and private routes: **never impose public SEO indexing requirements on private dashboards, authenticated admin panels, or internal enterprise tools**; instead, ensure private surfaces are explicitly excluded from search indexing.

## 1. Activation Conditions

Activate this skill when the user request or engineering task involves:
- Building or auditing public-facing marketing websites, landing pages, blogs, documentation portals, e-commerce catalogs, or public user profiles.
- Implementing `<title>`, `<meta name="description">`, Open Graph (`og:*`), Twitter/X Card (`twitter:*`), and `<link rel="canonical">` tags.
- Generating or validating `robots.txt`, `<meta name="robots">`, `X-Robots-Tag` headers, and XML sitemaps (`sitemap.xml`).
- Adding Schema.org `JSON-LD` structured data (`Article`, `Product`, `Organization`, `BreadcrumbList`, `FAQPage`, `SoftwareApplication`).
- Fixing crawlability traps (client-only rendering blocking crawlers, Soft 404s returning HTTP `200`, redirect chains, broken internal links, or `<div>` click handlers used instead of `<a href>`).

## 2. When Not to Use

Do not activate this skill for public indexing when the task involves:
- Internal company tools, B2B SaaS authenticated workspaces, admin panels, user settings pages, checkout/billing steps, or private APIs (for these routes, apply only the **Private Route Protection** rule in Step 1: enforce authentication and `noindex, nofollow`, then stop).
- Deep backend database or CPU profiling unrelated to web rendering (route to `performance-profiling-optimization`, `SKILL-29`).
- WCAG keyboard navigation and screen reader accessibility auditing (route to `accessibility-engineering`, `SKILL-21`, which complements semantic HTML).

## 3. Scope and Objectives

For all public, indexable web pages, this skill covers:
- **Public vs. Private Route Classification**: Distinguishing public discoverable routes from private/authenticated or staging routes before applying any indexing rules.
- **Metadata Completeness**: Providing unique, accurate `<title>` (`50-60` chars recommended) and `<meta name="description">` (`120-160` chars recommended) per indexable route, plus complete Open Graph (`og:title`, `og:description`, `og:url`, `og:image`, `og:type`) and `twitter:card` metadata.
- **Canonical URLs**: Emitting an absolute, self-referencing `<link rel="canonical" href="https://...">` on every public page to prevent duplicate-content dilution from query parameters (`?utm_source=...`), trailing slashes, or protocol/host variants.
- **XML Sitemap**: Generating a valid `sitemap.xml` (or sitemap index) listing only canonical, indexable (`200 OK`) public URLs with accurate `<lastmod>` timestamps.
- **Robots Directives**: Configuring `robots.txt`, `<meta name="robots">`, and `X-Robots-Tag` HTTP headers consistently so public pages are crawlable while private, staging, search-filter permutations, and API routes are properly restricted.
- **Indexability & Rendering Architecture**: Ensuring critical page content and metadata are present in the initial Server-Side Rendered (SSR) or Statically Generated (SSG) HTML response, and returning semantic HTTP status codes (`200`, `301`/`308` permanent redirect, `404` Not Found, `410` Gone; never Soft-404s).
- **Link Integrity**: Using standard crawlable `<a href="/path">` elements for all navigation links (never `<div onClick={() => router.push(...)}>`), descriptive anchor text, and zero broken internal links.
- **Structured Data (`JSON-LD`)**: Embedding valid Schema.org `application/ld+json` blocks where appropriate and ensuring strict parity with visible page content.
- **Technical SEO & Internationalization**: Enforcing clean semantic URL slugs, single `<h1>` hierarchy, mobile viewport responsiveness, Core Web Vitals compliance (`SKILL-29`), and bidirectional `<link rel="alternate" hreflang="...">` tags for multi-language sites.

## 4. Prerequisites and Context Requirements

Before implementing SEO changes, establish:
1. **Application Visibility Classification**: Is this project a public website, a hybrid app (public marketing + private dashboard), or a 100% private/internal application?
2. **Canonical Production Domain**: Determine the canonical scheme and host (e.g., `https://www.example.com` vs `https://example.com`) so canonical URLs, Open Graph image URLs, and `sitemap.xml` entries use absolute URLs rather than relative paths.
3. **Rendering Mode**: Check whether the frontend uses SSR/SSG (Next.js, Nuxt, Astro, Laravel Blade, Django Templates, Remix) or a pure client-side SPA (`index.html` shell).

## 5. Step-by-Step Workflow

### Step 1: Classify Routes (Public vs. Private / Non-Production)
- [ ] **Private Dashboards, Admin Panels, & Internal Apps**:
  - Do **NOT** create sitemaps, JSON-LD, or keyword metadata for private routes (`/admin/*`, `/dashboard/*`, `/settings/*`, `/account/*`, `/checkout/*`).
  - Protect private routes behind authentication middleware and add `<meta name="robots" content="noindex, nofollow">` or the HTTP response header `X-Robots-Tag: noindex, nofollow`.
- [ ] **Staging / Preview Environments**:
  - Ensure non-production domains (`staging.example.com`, `*.vercel.app` previews) send `X-Robots-Tag: noindex, nofollow` so staging copies never compete with production in search results.
- [ ] Proceed with Steps 2-6 **only** for public, intentionally discoverable pages.

### Step 2: Implement Per-Route Metadata and Canonical URLs
- [ ] Ensure every public page renders a unique, descriptive `<title>` (`50-60` characters) and `<meta name="description">` (`120-160` characters) in `<head>`.
- [ ] Add an absolute `<link rel="canonical" href="https://domain.tld/clean-path">` stripped of tracking query parameters (`utm_*`, `fbclid`, `gclid`, `ref`).
- [ ] Configure social sharing tags with absolute URLs for images:
  - `og:title`, `og:description`, `og:url`, `og:site_name`, and `og:type` (`website`, `article`, `product`).
  - `og:image` (`1200x630px` recommended), `og:image:width`, `og:image:height`, and descriptive `og:image:alt`.
  - `twitter:card` (`summary_large_image` or `summary`), `twitter:title`, `twitter:description`, and `twitter:image`.
- [ ] Ensure fallback metadata is defined at the root layout level while dynamic child routes override page-specific titles, descriptions, and canonical paths.

### Step 3: Verify Indexability, HTTP Status Codes, and Semantic HTML
- [ ] Verify that missing dynamic entities (e.g., `/products/non-existent-slug`) return an actual HTTP `404` status code (not an HTTP `200` page displaying `"Product not found"` text, which creates a Soft-404 penalty).
- [ ] Ensure URL redirects use permanent `301` or `308` status codes for moved pages and resolve in a single hop without redirect chains (`A -> B -> C`).
- [ ] Verify every public page has exactly one primary `<h1>` describing the page topic and follows sequential heading hierarchy (`<h1>` -> `<h2>` -> `<h3>`).

### Step 4: Audit Internal Link Integrity & Crawlability
- [ ] Replace any non-semantic navigation triggers (`<button onClick={navigate}>` or `<span onClick>`) used for page transitions with real `<a href="...">` tags (or framework `<Link href="...">` components that render `<a>`).
- [ ] Replace generic anchor text (`"click here"`, `"read more"`) with descriptive anchor text (`"Read the API authentication guide"`).
- [ ] Ensure external untrusted/user-generated links include `rel="noopener noreferrer ugc"` (or `rel="sponsored"` for paid links).

### Step 5: Configure `robots.txt` and `sitemap.xml`
- [ ] Configure `/robots.txt` to allow crawling of public pages and static assets (CSS/JS/images required by Googlebot to render layout) while disallowing internal API endpoints, raw search/filter permutations, and admin paths. Note: `Disallow` in `robots.txt` prevents crawling, whereas `noindex` prevents indexing; do not block a URL in `robots.txt` if you rely on crawlers reading its `<meta name="robots" content="noindex">` tag.
- [ ] Generate `/sitemap.xml` dynamically or at build time containing only canonical, indexable (`200 OK`) public URLs, and reference `Sitemap: https://domain.tld/sitemap.xml` at the bottom of `robots.txt`.

### Step 6: Add Validated Structured Data (`JSON-LD`) and Internationalization Tags
- [ ] Where applicable (articles, products, events, organizations, breadcrumbs, FAQs), inject a `<script type="application/ld+json">` block in `<head>` or `<body>`.
- [ ] Safely serialize JSON-LD (escape `<`, `>`, `&` or `\u003c` so user content inside titles/descriptions cannot break out of `</script>` and cause XSS).
- [ ] Only include structured data properties that match visible content on the page (never fabricate aggregate ratings or fake review counts).
- [ ] For multi-language or multi-region public sites, render reciprocal `<link rel="alternate" hreflang="x" href="https://...">` tags including an `hreflang="x-default"` fallback.
- [ ] Ensure Core Web Vitals (`LCP <= 2.5s`, `INP <= 200ms`, `CLS <= 0.1`) and mobile viewport responsiveness (`<meta name="viewport" content="width=device-width, initial-scale=1">`) are satisfied on all public landing pages.

## 6. Technology-Specific Adaptation Rules

Adapt SEO and discoverability implementation to the project's actual web stack. Never force PHPStan, Pint, Pest, shadcn/ui, or Playwright where inapplicable:
- **JavaScript / TypeScript (Next.js / React / Vue / Nuxt / Astro / SvelteKit)**:
  - In Next.js App Router, use the typed Metadata API (`export const metadata` / `generateMetadata`), `app/sitemap.ts`, `app/robots.ts`, and `notFound()` from `next/navigation` (to emit real HTTP `404` status). Set `metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL)`.
  - In Nuxt, use `useSeoMeta()`, `useHead()`, and `@nuxtjs/seo`. In Astro or SvelteKit, render metadata and `<link rel="canonical">` in the server layout `<head>`.
- **PHP (Laravel / Blade / Livewire / Inertia / CodeIgniter)**:
  - Use Blade `<x-slot:meta>` or `@yield('meta')` in server-rendered layouts, and `spatie/laravel-sitemap` or a dedicated controller for `/sitemap.xml`.
  - If using Inertia.js for public marketing pages, enable **Inertia SSR** (`<Head>` component) so crawlers and social unfurl bots receive rendered `<title>` and `og:*` tags in the initial HTML payload.
- **Python (Django / FastAPI / Flask / Jinja2)**:
  - Render canonical URLs (using configured `SITE_URL` + `request.path`, stripped of tracking query params) and metadata blocks in base Jinja2/Django templates; use `django.contrib.sitemaps` for automated sitemap generation.
- **Go / Rust / Java (Spring Boot Thymeleaf/JTE) / C# (ASP.NET Core Razor/Blazor SSR)**:
  - Render `<title>`, `<meta name="description">`, `og:*`, `<link rel="canonical">`, and JSON-LD directly in server-rendered HTML templates, and set explicit HTTP `404`/`301` status codes on handler responses.
- **Single-Page Applications & Mobile Web (Pure CSR React / Vue / Flutter Web)**:
  - Warn the user if a public content site is built as a pure client-side SPA or canvas-rendered Flutter Web app without SSR/pre-rendering, as social unfurl bots (Slack, WhatsApp, X, LinkedIn, Discord) do **not** execute JavaScript and will fail to see dynamically injected `<meta property="og:*">` tags. Use static pre-rendering or an edge metadata proxy for public routes.
- **Private / Internal Applications Across All Stacks**:
  - Do not add public SEO metadata, sitemaps, or Schema.org markup to internal dashboards or admin portals; enforce `<meta name="robots" content="noindex, nofollow">` and `X-Robots-Tag: noindex, nofollow`.

## 7. Security and Safety Considerations

- **Prevent XSS in `<script type="application/ld+json">`**: Never interpolate unescaped strings into JSON-LD blocks (`JSON.stringify(data).replace(/</g, '\\u003c')`), because an attacker placing `</script><script>alert(1)</script>` inside a product title or blog comment will execute arbitrary JavaScript if unescaped.
- **Prevent Host Header Poisoning in Canonical & Sitemap URLs**: Generate canonical URLs and sitemaps from a trusted, configured canonical `APP_URL` / `SITE_URL` environment variable rather than blindly trusting an unvalidated incoming HTTP `Host` or `X-Forwarded-Host` header.
- **Never Leak Private URLs in `sitemap.xml` or `robots.txt`**: Do not list secret/unauthenticated URLs in `robots.txt` `Disallow:` lines as a substitute for real authentication, because `robots.txt` is publicly readable by attackers.
- **Open Redirect Prevention on SEO Redirects**: When implementing trailing-slash or lowercase URL normalization redirects (`301`), validate that the redirect target stays strictly on the canonical origin (`//evil.com` path prefix bypass defense).

## 8. Verification Criteria

Before marking SEO and discoverability tasks complete, verify:
1. **Scope Boundary Respected**: Public pages have full metadata/canonical/sitemap coverage; private dashboards/admin pages have `noindex, nofollow` and authentication.
2. **Initial HTML Inspection**: Inspecting the raw HTTP response (`curl -s` or initial document source before client JS runs) confirms `<title>`, `<meta name="description">`, `og:*`, and `<link rel="canonical">` are present.
3. **Zero Soft-404s or Broken Links**: Missing routes return HTTP `404`, and all internal `<a href>` links resolve to valid routes.
4. **Valid XML & JSON-LD Syntax**: `/sitemap.xml` is valid XML with absolute canonical URLs, and `application/ld+json` blocks parse cleanly as valid JSON with `<` escaped.

## 9. Failure Handling and Edge Cases

- **Pagination & Filtered Catalog URLs**: Ensure paginated views (`/blog?page=2`) self-canonicalize to their own page or follow consistent pagination conventions, while combinatorial facet filters (`?color=red&sort=price_asc`) canonicalize to the clean category URL or use `noindex` to avoid crawl budget exhaustion.
- **Missing `SITE_URL` in Local Development**: Fall back safely to `http://localhost:<port>` in local development while requiring the canonical HTTPS production domain in production config validation (`SKILL-32`).
- **Trailing Slash & Case Duplicate Traps**: Enforce a single URL normalization rule (either always strip trailing slashes or always append them via `301` redirect) and ensure `<link rel="canonical">` and `sitemap.xml` match that exact normalized form so crawlers never see redirect loops.

## 10. Expected Outputs and Reporting Requirements

Provide a structured **SEO & Web Discoverability Audit Report**:

```markdown
# SEO & Web Discoverability Report

## 1. Route Classification & Boundary Check
- **Public Indexable Routes**: `<e.g., /, /pricing, /blog/[slug], /docs/*>`
- **Private / Excluded Routes (`noindex`)**: `<e.g., /dashboard/*, /admin/*, /api/*>`
- **Rendering Strategy**: `<SSR / SSG / Pre-rendered>`

## 2. Technical SEO Verification Matrix
| SEO Dimension | Status | Implementation Evidence |
| :--- | :--- | :--- |
| **Title & Meta Description** | `<PASS>` | `<Unique per route, rendered in initial HTML>` |
| **Canonical & Open Graph** | `<PASS>` | `<Absolute URLs via canonical SITE_URL, og:image sized>` |
| **Robots & XML Sitemap** | `<PASS>` | `</robots.txt and /sitemap.xml verified>` |
| **HTTP Status & Link Integrity** | `<PASS>` | `<Real 404s on missing slugs; semantic <a href> links>` |
| **Structured Data (JSON-LD)** | `<PASS / N/A>` | `<XSS-safe JSON-LD Schema.org types validated>` |
```

## 11. Interoperability and Skill Routing

- **Upstream Skills**: Connects with `frontend-performance` (`SKILL-22`) and `performance-profiling-optimization` (`SKILL-29`) for Core Web Vitals ranking signals, and `accessibility-engineering` (`SKILL-21`) for semantic HTML heading and image `alt` text structure.
- **Downstream Skills**: Feeds public web readiness verification into `deployment-readiness` (`SKILL-33`) and `final-quality-gate` (`SKILL-38`).

## 12. Source References

- **Google Search Central Documentation (SEO Starter Guide & Technical Requirements)**: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- **Schema.org Official Vocabulary**: https://schema.org/
- **Open Graph Protocol Specification**: https://ogp.me/
