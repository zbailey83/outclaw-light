# robots.txt Reference

## What robots.txt Does

robots.txt tells crawlers what they're allowed and not allowed to crawl. For pSEO:
- Protect admin, API, and internal routes from crawl budget waste
- Declare sitemap location (every crawler reads this)
- Optionally rate-limit crawlers on resource-heavy sites

**Critical:** robots.txt controls *crawling*, not *indexing*. A noindexed page can still
be crawled. A blocked page can still be indexed if linked from elsewhere.

---

## Standard pSEO robots.txt

```
User-agent: *
Allow: /

# Block non-content paths (saves crawl budget)
Disallow: /api/
Disallow: /admin/
Disallow: /_next/
Disallow: /static/
Disallow: /auth/
Disallow: /dashboard/
Disallow: /*.json$
Disallow: /*.xml$

# Declare sitemap
Sitemap: https://example.com/sitemap.xml
```

For sitemap index:
```
Sitemap: https://example.com/sitemap-index.xml
```

Multiple sitemaps:
```
Sitemap: https://example.com/sitemap-pages.xml
Sitemap: https://example.com/sitemap-locations.xml
Sitemap: https://example.com/sitemap-categories.xml
```

---

## Crawl Budget Directives (Large Sites)

For 10,000+ page sites, optionally add crawl delay to prevent server overload:

```
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/

# Crawl delay in seconds (only Bingbot respects this reliably; Googlebot ignores it)
Crawl-delay: 1

Sitemap: https://example.com/sitemap.xml
```

**Note:** Google does NOT respect `Crawl-delay`. To adjust Googlebot's crawl rate,
use GSC → Settings → Crawl rate. See `references/gsc.md`.

---

## AI Crawler Controls

As of 2024-2025, multiple AI companies have their own crawlers. For pSEO, you typically
WANT AI crawlers to index your content (drives llms.txt citations). But if you want to
selectively block:

```
# Block AI training scrapers (not search/answer bots)
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Google-Extended
Disallow: /

# Allow everything else (including Bing search + Google search)
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/

Sitemap: https://example.com/sitemap.xml
```

**For pSEO:** Do NOT block AI crawlers. You want Perplexity, ChatGPT, and Claude
to be able to cite and surface your pages. Block only if you have specific legal reasons.

---

## Next.js robots.ts (App Router)

```typescript
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/api/', '/admin/', '/_next/', '/auth/'],
      },
    ],
    sitemap: 'https://example.com/sitemap.xml',
  }
}
```

---

## Astro (public/robots.txt)

Astro serves static files from `public/`. Create `public/robots.txt` directly:

```
User-agent: *
Allow: /
Disallow: /api/

Sitemap: https://example.com/sitemap.xml
```

Or generate dynamically via endpoint:
```typescript
// src/pages/robots.txt.ts
export async function get() {
  const content = `User-agent: *
Allow: /
Disallow: /api/

Sitemap: https://example.com/sitemap.xml`

  return {
    body: content,
    headers: { 'Content-Type': 'text/plain' }
  }
}
```

---

## SvelteKit

```typescript
// src/routes/robots.txt/+server.ts
export function GET() {
  return new Response(`User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/

Sitemap: https://example.com/sitemap.xml`, {
    headers: { 'Content-Type': 'text/plain' }
  })
}
```

---

## Common robots.txt Mistakes in pSEO

| Mistake | Effect | Fix |
|---------|--------|-----|
| `Disallow: /` for all bots | Blocks all crawling | Audit and narrow the rule |
| Missing `Sitemap:` directive | Crawler has to find sitemap itself | Always declare sitemap |
| `Disallow: /*.html` | Blocks all HTML pages | Remove or narrow |
| Trailing slash inconsistency | `Disallow: /blog` ≠ `Disallow: /blog/` | Add both if needed |
| Noindex via robots.txt | robots.txt can't noindex (that's meta tags) | Use `<meta name="robots" content="noindex">` |

---

## Validation

```bash
# Confirm it loads
curl https://example.com/robots.txt

# Test with Google's robots.txt Tester
# GSC → Settings → robots.txt Tester (legacy)
# Or: https://support.google.com/webmasters/answer/6062598
```
