# Indexing Diagnostics Reference

## The Indexing Triage Framework

When pages aren't indexed, it's almost always one of six root causes.
Work through this in order — fix the first problem you find before moving on.

```
1. Can Google find the page? (sitemap + internal links)
2. Can Google access the page? (robots.txt + server response)
3. Does Google trust the page? (canonical + noindex tags)
4. Does Google value the page? (content quality + duplication)
5. Does Google have budget to crawl it? (crawl budget)
6. Is Google just slow? (patience + resubmission)
```

---

## Diagnostic 1: Can Google Find the Page?

### Check: Is the URL in your sitemap?

```bash
# Search for a specific URL in your sitemap
curl -s https://example.com/sitemap.xml | grep "austin-tx"
```

If not found → Add to sitemap, resubmit.

### Check: Does the sitemap submit cleanly in GSC?

GSC → Indexing → Sitemaps → Status should show green checkmark.
If error: Click on sitemap → See error details.

Common sitemap errors:
- `Couldn't fetch` → URL returns non-200 or times out
- `General HTTP error` → Server error on sitemap URL
- `Incorrect namespace` → XML namespace wrong (copy the standard template)
- `Invalid date` → lastmod date in wrong format (use YYYY-MM-DD)

### Check: Does the page have internal links?

Google follows links. Pages with zero internal links pointing to them may never be crawled.

```bash
# Grep your site's HTML for links to the page (rough check)
# Better: Use Screaming Frog or Ahrefs to find internal link count
```

Minimum: Every pSEO page should have at least 1 internal link from a crawled page.
Better: Link from category page + 2-3 related detail pages.

---

## Diagnostic 2: Can Google Access the Page?

### Check: robots.txt isn't blocking it

```bash
curl https://example.com/robots.txt
```

Test a specific URL against your robots.txt:
1. GSC → Settings → Search Console Settings → robots.txt Tester (legacy)
2. Or use: https://technicalseo.com/tools/robots-txt/

Common mistakes:
```
Disallow: /cities/    ← Blocks all city pages
Disallow: /*?*        ← May block pages with query params you want indexed
Disallow: /           ← Blocks everything (common accident)
```

### Check: Page returns HTTP 200

```bash
curl -I https://example.com/austin-tx
# Should show: HTTP/2 200
```

If it returns 404, 500, or redirect loop → Fix the server response first.

### Check: Page isn't password protected or behind auth wall

Google can't log in. If your pSEO pages require authentication, they won't index.

---

## Diagnostic 3: Does Google Trust the Canonical?

### Check: Meta robots tag

```bash
curl -s https://example.com/austin-tx | grep -i "robots"
```

Should NOT contain `noindex`. If you see:
```html
<meta name="robots" content="noindex" />
```
→ Remove it (unless intentional).

### Check: Canonical tag is correct

```bash
curl -s https://example.com/austin-tx | grep -i "canonical"
```

Should point to itself (the canonical URL):
```html
<link rel="canonical" href="https://example.com/austin-tx" />
```

Common problems:
- Canonical points to homepage (all pages look like duplicates of homepage)
- Canonical uses wrong protocol (http vs https)
- No canonical tag (Google picks one, may not be yours)
- `?` query param pages canonicalize to param-less version (usually correct, but verify)

### Check: HTTP response headers

```bash
curl -I https://example.com/austin-tx | grep -i "x-robots"
```

If server sends `X-Robots-Tag: noindex` → Override in your framework config.

---

## Diagnostic 4: Does Google Value the Page?

If Google says "Crawled - currently not indexed," the content quality is the issue.

### Signs of thin content (Google won't index these):

```
□ Page has < 300 words of meaningful content
□ 90%+ of content is identical to similar pages (template duplication)
□ Page mostly shows "No results" or empty states
□ Content adds no value over what a Wikipedia article already says
□ Multiple pSEO pages for same location with almost identical text
```

### Fixes for thin content:

1. **Add unique data** — Pull in external data that makes each page different
   (population, weather, local statistics, review counts, pricing data)

2. **Add dynamic content** — User reviews, recently added items, local events

3. **Reduce the URL space** — Better to have 1,000 high-quality indexed pages than
   10,000 thin ones. Noindex the thin ones:
   ```html
   <meta name="robots" content="noindex, follow" />
   ```

4. **Consolidate similar pages** — Instead of `/restaurants-italian-austin` and
   `/restaurants-italian-austin-tx`, pick one and 301 redirect the other.

5. **Add schema markup** — Structured data helps Google understand content type.
   LocalBusiness, FAQPage, BreadcrumbList schemas all help.

---

## Diagnostic 5: Crawl Budget

See `references/crawl-budget.md` for full guidance.

Quick check:
- GSC → Settings → Crawling → Crawl Stats
- If "Total pages crawled per day" is flat or dropping → crawl budget issue
- If your total page count far exceeds pages crawled × 30 days → pages are waiting

---

## Diagnostic 6: Patience (Check the Timeline)

Realistic timelines after sitemap submission + GSC setup:

| Site Age | Expected |
|----------|---------|
| New domain (< 3 months old) | 4-8 weeks for first pages |
| Established domain, new pages | 1-3 weeks |
| New pages after IndexNow ping | 1-3 days on Bing, 1-2 weeks Google |
| New pages with strong internal links | 3-10 days on Google |

If you're within these windows → wait and monitor GSC weekly.

---

## Quick URL Inspection Protocol

For any specific URL that isn't indexed:

1. GSC → URL Inspection → enter exact URL
2. Read the coverage status carefully
3. Click **Test Live URL** (not "Last crawl") to force a fresh check
4. If "URL is not on Google" → Request Indexing
5. Check: `Page availability`, `Indexing allowed?`, `Canonical`, `Mobile usability`

---

## Common pSEO-Specific Indexing Failures

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| 1,000 pages submitted, 50 indexed | Thin/duplicate content | Improve content differentiation |
| Pages indexed then dropped after 30 days | Soft 404 or content quality downgrade | Fix content or add more value |
| Category pages indexed but detail pages not | No internal links to detail pages | Add links from category to all children |
| New page batches take 6+ weeks | Crawl budget too low for site size | Improve response time + reduce crawl waste |
| Pages indexed on Bing but not Google | Google quality threshold higher | Improve content quality |
| 90-day-old pages still "Discovered - not indexed" | Too many pages in queue | Reduce URL space / improve crawl budget |
