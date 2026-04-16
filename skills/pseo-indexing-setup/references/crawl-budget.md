# Crawl Budget & Large-Scale Indexing Reference

## What is Crawl Budget?

Crawl budget is the number of pages Google will crawl on your site within a given period.
It's determined by two factors:
1. **Crawl capacity limit** — How fast Google can crawl without overwhelming your server
2. **Crawl demand** — How often Google thinks your pages change and how popular they are

For small sites (<1,000 pages), crawl budget is rarely a concern.
For pSEO sites with 10,000–1,000,000+ pages, it's the primary indexing bottleneck.

---

## Crawl Budget Warning Signs

```
□ New pages take 30+ days to appear in GSC
□ "Discovered - currently not indexed" count keeps growing
□ GSC Crawl Stats show drops in pages crawled/day
□ Only a fraction of sitemap URLs are indexed after 90+ days
□ Old pages being dropped while new ones aren't picked up
```

---

## Crawl Budget Optimization: The Full Playbook

### 1. Eliminate crawl waste

Every 4xx/5xx response, redirect chain, and noindex page wastes crawl budget.
Google uses budget to crawl these even if they don't index them.

**Audit:**
```bash
# Find broken links with screaming frog or similar
# In GSC: Indexing → Pages → filter by "Not found (404)"
# Aim for 0 URLs in sitemap that return non-200
```

**Fix:**
- Remove 404 URLs from sitemap immediately
- Redirect old pSEO URLs that changed slug structure (301)
- Remove noindex pages from sitemap (indexability mismatch wastes budget)
- Consolidate near-duplicate pages rather than publishing thin variations

---

### 2. Improve page response time

Google crawls faster when pages respond faster. Target TTFB < 200ms.

```bash
# Test current TTFB
curl -w "@curl-format.txt" -o /dev/null -s https://example.com/any-page

# curl-format.txt contents:
#     time_starttransfer:  %{time_starttransfer}\n
```

**For pSEO on databases:**
- Add database indexes on slug/ID columns used in URL routing
- Use caching (Redis, in-memory, CDN edge caching)
- Pre-render or SSG your pSEO pages rather than SSR where possible

---

### 3. Strengthen internal linking

Crawl budget is allocated based on PageRank flow. Pages with more internal links get
crawled more frequently.

For pSEO:
- Every pSEO page should link to at least 3-5 related pages
- Category/hub pages should link to all their child pages
- Homepage or main nav should link to top category pages
- Add pagination links (`rel="prev"` / `rel="next"`) for paginated category pages
- Add a footer sitemap linking to main categories

**Minimum internal link structure for pSEO:**
```
Homepage → Category pages (5-20)
Category pages → All detail pages in that category
Detail pages → Related detail pages (3-5 per page)
Detail pages → Parent category page
```

---

### 4. Use sitemap lastmod correctly

Google uses `<lastmod>` to decide crawl priority. If all pages show the same date,
Google treats them with equal (low) priority.

**Best practice:**
```xml
<!-- Use the actual last modification date, not today's date for all pages -->
<url>
  <loc>https://example.com/austin-tx</loc>
  <lastmod>2025-03-15</lastmod>  <!-- When content actually changed -->
</url>
```

For pSEO built from a database, store and use actual `updated_at` timestamps.

---

### 5. Segment sitemaps by priority

Google processes submitted sitemaps but not necessarily in full or in order.
Help it by segmenting:

```xml
<!-- sitemap-index.xml -->
<sitemapindex>
  <!-- Highest priority pages — crawled first -->
  <sitemap>
    <loc>https://example.com/sitemap-tier1.xml</loc>
  </sitemap>
  <!-- Large volume pSEO pages — crawled based on demand -->
  <sitemap>
    <loc>https://example.com/sitemap-cities.xml</loc>
  </sitemap>
  <!-- Low priority / thin pages — let Google decide -->
  <sitemap>
    <loc>https://example.com/sitemap-tags.xml</loc>
  </sitemap>
</sitemapindex>
```

Submit the index sitemap in GSC. Google will process Tier 1 first.

---

### 6. Manage large URL spaces

For 100,000+ page pSEO sites:

**Consider not indexing everything:**
Not every URL needs to be indexed. Use `<meta name="robots" content="noindex">` for:
- Filter/sort pages (e.g., `/restaurants?sort=price&cuisine=italian`)
- Paginated pages beyond page 3-5
- Thin location combinations that add little value
- Test/preview pages

This concentrates crawl budget on your best content.

**Use canonical tags:**
```html
<!-- On paginated pages, point to canonical -->
<link rel="canonical" href="https://example.com/austin-tx/restaurants" />
```

---

### 7. Use GSC Crawl Stats for diagnosis

GSC → **Settings** → **Crawling** → **Open Crawl Stats report**

Key metrics:
- **Total crawl requests** — Should be rising as you add pages
- **Response codes** — Anything other than 200/301 is a budget drain
- **Crawl requests breakdown by file type** — Excessive JS/CSS crawling = inefficiency
- **Crawl requests by Googlebot type** — Desktop vs. mobile crawling balance

---

## Crawl Budget Benchmarks by Site Size

| Site Size | Expected Time to Full Index | Primary Strategy |
|-----------|---------------------------|-----------------|
| < 1,000 pages | 1-4 weeks | Normal sitemap + GSC submission |
| 1,000–10,000 | 2-8 weeks | + Internal linking audit |
| 10,000–100,000 | 4-16 weeks | + Response time optimization + segmented sitemaps |
| 100,000–1M | 3-12 months | + Noindex thin pages + prioritized crawl segments |
| 1M+ | Ongoing | + Crawl budget dedicated to "best" content only |

---

## Emergency: Pages Dropping From Index

If indexed pages start disappearing:
1. Check GSC Coverage report for new "Crawled - currently not indexed" entries
2. Pull the affected URLs and inspect via URL Inspection tool
3. Common causes: content became too thin, canonical confusion, robots.txt change
4. Check server uptime/response time during Googlebot crawls (GSC Crawl Stats timing)
5. Check if a site migration or URL change happened without proper redirects
