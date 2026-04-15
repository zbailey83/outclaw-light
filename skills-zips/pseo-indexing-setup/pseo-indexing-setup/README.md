# pSEO Indexing Setup Skill

**For:** Claude Code · Openclaw · Antigravity  
**Version:** 1.0  
**Category:** Programmatic SEO · Technical SEO · Search Indexing

---

## What This Skill Does

Gets your programmatic SEO website's pages crawled, indexed, and discoverable by
Google, Bing, and AI answer engines — completely and fast.

Covers the full technical indexing stack:

| File / Tool | What It Does |
|-------------|-------------|
| `sitemap.xml` | Tells crawlers every URL that exists on your site |
| `robots.txt` | Controls what crawlers can access + declares sitemap location |
| `llms.txt` | Tells AI search engines (Perplexity, ChatGPT, Claude) about your site |
| `llms-full.txt` | Complete page-by-page index for AI crawlers |
| GSC submission | Forces Google to know your sitemap exists |
| Bing IndexNow | Pings Bing/DuckDuckGo the moment you publish a new URL |

---

## When To Use This Skill

**Use it when you're:**
- Launching a new pSEO site and need to get pages indexed fast
- Adding a large batch of new pSEO pages and want them crawled immediately
- Building the technical foundation for a programmatic SEO project
- Debugging why your pages aren't appearing in Google or Bing
- Setting up a new framework (Next.js, Astro, SvelteKit, etc.) for pSEO

**Trigger phrases (Claude will load this skill):**
- "set up my sitemap"
- "get pages indexed"
- "submit to GSC" / "Google Search Console setup"
- "IndexNow" / "Bing Webmaster Tools"
- "llms.txt" / "robots.txt"
- "why aren't my pages indexed"
- "programmatic SEO crawling"

---

## File Structure

```
pseo-indexing-setup/
├── SKILL.md                    ← Main skill (always loaded)
├── README.md                   ← This file
└── references/
    ├── sitemap.md              ← sitemap.xml generation for all frameworks
    ├── robots.md               ← robots.txt setup + AI crawler controls
    ├── llms-txt.md             ← llms.txt + llms-full.txt creation
    ├── gsc.md                  ← Google Search Console full setup guide
    ├── bing.md                 ← Bing Webmaster Tools + IndexNow
    ├── crawl-budget.md         ← Crawl budget optimization (10k+ page sites)
    ├── platforms.md            ← Framework-specific code (Next.js, Astro, etc.)
    └── diagnostics.md         ← Fixing indexing problems
```

Reference files are loaded on demand — only what's needed for the user's specific request.

---

## What Claude Produces With This Skill

**Ready-to-deploy files:**
- `sitemap.xml` or framework-specific sitemap code
- `robots.txt` for your specific setup and page structure
- `llms.txt` and `llms-full.txt` tuned to your site's content
- IndexNow key verification file

**Code snippets for your stack:**
- Next.js `app/sitemap.ts`, `app/robots.ts`
- Astro `@astrojs/sitemap` config
- SvelteKit endpoint code
- Python/Node.js build scripts for static generation

**Step-by-step checklists:**
- GSC property creation and verification
- Sitemap submission in GSC
- Bing Webmaster Tools setup (including GSC import shortcut)
- IndexNow key generation and activation

**Diagnostic reports:**
- Audit of why specific pages aren't indexing
- Crawl budget analysis for large sites
- robots.txt conflict detection

---

## The 5-File Stack (Always Deploy All Five)

The biggest mistake in pSEO: deploying only some of these. Here's what each one costs you
if skipped:

| Skip This | Cost |
|-----------|------|
| sitemap.xml | Google discovers pages slowly via links only — weeks of lag |
| robots.txt (no sitemap declaration) | Crawlers don't find your sitemap automatically |
| llms.txt | Invisible to Perplexity, ChatGPT search, Claude, Gemini |
| GSC submission | Google may take 30+ days to process new page batches |
| IndexNow | Bing/DuckDuckGo discovers new pages via crawl only — days to weeks of lag |

**Time to deploy all five correctly:** 45-90 minutes.  
**Time it saves you:** Weeks of indexing lag per page batch, forever.

---

## Supported Platforms

| Platform | Sitemap | robots.txt | llms.txt | IndexNow |
|----------|---------|------------|---------|---------|
| Next.js (App Router) | Native `sitemap.ts` | Native `robots.ts` | Route handler | Script / Vercel integration |
| Astro | `@astrojs/sitemap` | Static file or endpoint | API endpoint | Script |
| SvelteKit | `+server.ts` endpoint | `+server.ts` endpoint | `+server.ts` endpoint | Script |
| Nuxt 3 | `nuxt-simple-sitemap` | Module | Endpoint | Script |
| WordPress | Yoast / Rank Math | Plugin + file | Static | Rank Math Pro |
| Hugo | Built-in | Static | Template | Build script |
| Static / Custom | Build script | Static file | Build script | Deploy hook |
| Cloudflare Pages | Worker | Static | Worker | Native integration |

---

## Concepts You Should Know

**Crawl budget** — The number of pages a search engine will crawl on your site per period.
For large pSEO sites, this is the primary limiting factor on indexing speed. See `references/crawl-budget.md`.

**IndexNow** — An open protocol where you ping search engines the moment you publish or update
a URL, instead of waiting for them to crawl your sitemap. Supported by Bing, Yandex, DuckDuckGo.

**llms.txt** — An emerging standard (llmstxt.org) for telling AI crawlers what your site is
about and which pages to include in AI answer engine citations.

**Soft 404** — A page that returns HTTP 200 but has no real content (empty template, "no results"
state). Google treats these as low quality and often won't index them.

**Crawled - currently not indexed** — GSC status meaning Google visited the page but chose not
to index it. Usually a content quality or duplication issue, not a technical one.

---

## Installation

This skill is structured as a standard Claude skill. To install:

1. Copy the `pseo-indexing-setup/` folder to your skills directory
2. The skill will trigger automatically on indexing-related requests

Or deploy as a `.skill` file using the skill packager:
```bash
python -m scripts.package_skill pseo-indexing-setup/
```

---

## Changelog

### v1.0 (2025-04)
- Initial release
- Full coverage: sitemap, robots, llms.txt, GSC, Bing, IndexNow
- Platform support: Next.js, Astro, SvelteKit, Nuxt, WordPress, Hugo, Cloudflare
- Diagnostic framework for indexing failures
- Crawl budget optimization for 10k–1M+ page sites
