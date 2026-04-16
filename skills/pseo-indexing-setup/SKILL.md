---
name: pseo-indexing-setup
description: >
  Use this skill whenever the user wants to set up crawling, indexing, or discoverability
  infrastructure for a programmatic SEO (pSEO) website. Trigger for any request involving:
  sitemap.xml generation or configuration, robots.txt setup, llms.txt or llms-full.txt creation,
  Google Search Console (GSC) verification and submission, Bing Webmaster Tools setup,
  getting pages indexed faster, fixing indexing issues, setting up pSEO technical foundations,
  or "why aren't my pages indexed". Also trigger for "submit sitemap", "GSC setup", "search console",
  "Bing indexing", "programmatic SEO crawling", "IndexNow", "URL inspection tool", or any request
  about getting a large volume of AI-generated or template-driven pages discovered by search engines.
  Use aggressively for any pSEO project — even if the user only mentions one piece (e.g., just
  robots.txt), offer to set up the full stack.
---

# pSEO Indexing Setup Skill

Complete technical infrastructure for getting programmatic SEO pages crawled, indexed, and
discoverable by Google, Bing, and AI answer engines — fast.

**Scope:** Sitemap · Robots.txt · llms.txt · GSC verification + submission · Bing Webmaster Tools
· IndexNow · Crawl budget optimization · Ongoing monitoring

---

## Quick Reference

| Task | Go To |
|------|-------|
| Generate sitemap.xml | `references/sitemap.md` |
| Write robots.txt | `references/robots.md` |
| Create llms.txt / llms-full.txt | `references/llms-txt.md` |
| GSC setup + verification + submission | `references/gsc.md` |
| Bing Webmaster Tools setup + IndexNow | `references/bing.md` |
| Crawl budget & large-scale indexing strategy | `references/crawl-budget.md` |
| Platform-specific setup (Next.js, Astro, etc.) | `references/platforms.md` |
| Diagnosing indexing problems | `references/diagnostics.md` |

---

## The pSEO Indexing Stack (Always Set Up All Five)

Most pSEO builders set up one or two of these and wonder why their pages aren't indexed.
The full stack takes under an hour and compounds indefinitely.

```
1. sitemap.xml       → Tells crawlers what exists
2. robots.txt        → Tells crawlers what to crawl (and how fast)
3. llms.txt          → Tells AI answer engines what to include
4. GSC submission    → Forces Google to know about your sitemap
5. Bing IndexNow     → Instant ping on every new/updated URL
```

Never skip any of these. Skipping IndexNow costs you days of indexing lag on every new page batch.
Skipping llms.txt means your pSEO content is invisible to Perplexity, ChatGPT search, and Claude.

---

## Workflow: First-Time Setup

### Step 1 — Gather context (ask if not provided)

```
- Domain / base URL
- Tech stack (Next.js, Astro, SvelteKit, static, WordPress, etc.)
- CMS or data source (Airtable, Notion, Supabase, flat files, etc.)
- Approximate page count and URL pattern
- Hosting platform (Vercel, Netlify, Cloudflare, VPS, etc.)
- Do they have GSC access already? Verified?
- Do they have Bing Webmaster Tools?
```

### Step 2 — Generate the five files

Generate all five in order. See the relevant reference file for each:

1. `sitemap.xml` → `references/sitemap.md`
2. `robots.txt` → `references/robots.md`
3. `llms.txt` → `references/llms-txt.md`
4. GSC setup checklist → `references/gsc.md`
5. Bing + IndexNow setup → `references/bing.md`

### Step 3 — Submit and verify

Walk the user through:
- Verifying domain ownership in GSC (HTML tag, DNS, or file method)
- Submitting sitemap URL in GSC
- Verifying domain in Bing Webmaster Tools
- Importing GSC data into Bing (one-click)
- Testing sitemap URL returns valid XML (curl + validator)
- Testing robots.txt loads at `domain.com/robots.txt`
- Testing llms.txt loads at `domain.com/llms.txt`

### Step 4 — IndexNow activation

Set up IndexNow for instant Bing pings on every publish. See `references/bing.md`.
If the user is on Vercel or Cloudflare, there are one-click integrations to call out.

### Step 5 — Crawl budget check

For sites with 1,000+ pages, read `references/crawl-budget.md` and apply recommendations.

---

## Platform Detection

When the user mentions their tech stack, load `references/platforms.md` for framework-specific
implementation details:

- **Next.js** — `app/sitemap.ts`, `app/robots.ts`, metadata API
- **Astro** — `@astrojs/sitemap` integration, endpoint-based generation
- **SvelteKit** — `+server.ts` endpoint pattern
- **Nuxt** — `nuxt-simple-sitemap` module
- **WordPress** — Yoast/Rank Math config, WP Rocket exclusions
- **Static (11ty, Hugo, Jekyll)** — Build-time generation patterns
- **Custom/API-first** — Node.js / Python generation scripts

---

## Diagnosing Indexing Problems

If the user already has a site but pages aren't indexed, load `references/diagnostics.md`.

Common failure modes in pSEO indexing:
1. **Sitemap exists but not submitted** — Google never received it
2. **Robots.txt blocks the wrong paths** — Noindex on `/*` wildcard gone wrong
3. **No internal links to pSEO pages** — Googlebot follows links, not just sitemaps
4. **Duplicate content signals** — Template pages with near-identical content get soft-excluded
5. **Crawl budget exhausted** — Large sites crawled too slowly, new pages wait weeks
6. **llms.txt missing** — AI engines exclude the site entirely from citations

---

## Output Formats This Skill Produces

- **Ready-to-deploy files** — sitemap.xml, robots.txt, llms.txt, llms-full.txt, IndexNow key file
- **Code snippets** — Framework-specific sitemap/robots generation code
- **Step-by-step checklists** — GSC verification, Bing setup, IndexNow activation
- **Diagnostic reports** — Indexing audit based on user's current setup
- **Monitoring dashboards** — What to check weekly in GSC and Bing after launch
- **API scripts** — IndexNow ping scripts for post-deploy automation

---

## Key Numbers to Know

| Metric | Target |
|--------|--------|
| Sitemap file size limit | 50MB / 50,000 URLs per file |
| Sitemap index files | Unlimited (use for 50k+ page sites) |
| GSC indexing lag (new site) | 4–14 days after submission |
| Bing IndexNow lag | Minutes to hours after ping |
| robots.txt max size | 500KB (keep well under) |
| Crawl budget refresh | Google re-evaluates every few weeks |
| llms.txt size guidance | Under 2,000 tokens for inline; use llms-full.txt for more |
