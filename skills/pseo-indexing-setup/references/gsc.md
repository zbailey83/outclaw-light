# Google Search Console Reference

## What GSC Does for pSEO

Google Search Console is the primary interface for:
- Telling Google your site exists (verification)
- Submitting sitemaps (so Google knows what to index)
- Monitoring indexing status per URL
- Inspecting crawl errors and coverage reports
- Requesting indexing for specific URLs

For pSEO, it's non-negotiable. Without GSC submission, Google may take 30+ days to
discover new pages. With submission, that drops to 4–14 days and often less.

---

## Step 1: Add Property in GSC

1. Go to [search.google.com/search-console](https://search.google.com/search-console)
2. Click **Add property**
3. Choose **Domain** (recommended) or **URL prefix**

| Property Type | Covers | Verification |
|--------------|--------|-------------|
| Domain | All subdomains + http/https | DNS TXT record only |
| URL prefix | Exact URL and below | 5 options (HTML tag recommended) |

**Use Domain property** for pSEO — captures everything including `www`, `blog.`, etc.

---

## Step 2: Verify Ownership

### Method A: DNS TXT Record (for Domain property — recommended)

1. GSC provides a TXT record like: `google-site-verification=abc123xyz`
2. Add it to your DNS provider (Cloudflare, Route53, Namecheap, etc.):
   - Type: `TXT`
   - Name: `@` (root domain)
   - Value: `google-site-verification=abc123xyz`
   - TTL: 300 (or default)
3. Click Verify in GSC — takes 30 seconds to a few minutes

### Method B: HTML Meta Tag (for URL prefix property)

Add to `<head>` of your homepage:
```html
<meta name="google-site-verification" content="abc123xyz" />
```

**Next.js:**
```typescript
// app/layout.tsx
export const metadata = {
  verification: {
    google: 'abc123xyz',
  },
}
```

**Astro:**
```html
<!-- src/layouts/Base.astro -->
<meta name="google-site-verification" content="abc123xyz" />
```

### Method C: HTML File Upload

Download `googleabc123.html` from GSC, upload to `public/` folder.
Accessible at `https://example.com/googleabc123.html`.

---

## Step 3: Submit Sitemap

1. In GSC, select your property
2. Left sidebar → **Indexing** → **Sitemaps**
3. Enter your sitemap URL: `sitemap.xml` (GSC adds the domain)
4. Click **Submit**

For sitemap index:
```
sitemap-index.xml
```

**Common mistakes:**
- Submitting `https://example.com/sitemap.xml` — enter just `sitemap.xml`
- Submitting before sitemap is live — verify URL returns 200 first
- Forgetting to resubmit after major URL structure changes

---

## Step 4: Monitor Indexing Coverage

**GSC → Indexing → Pages**

Key statuses to understand:

| Status | Meaning | Action |
|--------|---------|--------|
| Indexed | Page is in Google's index ✅ | None |
| Crawled - currently not indexed | Google crawled but chose not to index | Improve content quality / internal links |
| Discovered - currently not indexed | In sitemap but not crawled yet | Normal for new sites; wait |
| Page with redirect | URL redirects to another | Check redirect target is indexed |
| Not found (404) | URL in sitemap returns 404 | Remove from sitemap / fix the URL |
| Soft 404 | Returns 200 but looks empty to Google | Fix the content or redirect |
| Excluded by noindex tag | `<meta name="robots" content="noindex">` | Intentional or fix the tag |
| Blocked by robots.txt | robots.txt disallows this path | Review robots.txt |
| Duplicate, selected canonical | Google found a better canonical | Add explicit canonical tags |

**For pSEO:** "Crawled - currently not indexed" on many pages is a signal of thin content.
Either improve content quality or reduce the number of near-duplicate pages.

---

## Step 5: Request Indexing (Individual URLs)

For priority pages or pages that aren't indexing fast enough:

1. GSC → **URL Inspection** (top search bar)
2. Enter the full URL
3. Click **Request Indexing**

Limits: ~10 requests/day per property. Use for:
- Homepage and main category pages
- High-priority pSEO pages you just published
- Pages you just made significant updates to

**Do NOT bulk request indexing** — Google treats this as spammy if overdone.
The sitemap submission is the bulk mechanism; URL inspection is surgical.

---

## Step 6: Adjust Crawl Rate (Large Sites Only)

For 10,000+ page pSEO sites experiencing slow crawling:

GSC → **Settings** → **Crawling** → **Open Google Search Console Settings** → Crawl rate

Options:
- Let Google optimize (default — recommended unless you have a specific issue)
- Limit Google's crawl rate (use only if your server is being overwhelmed)

**Better approach than limiting:** Optimize page response times (< 200ms TTFB) so
Google crawls more aggressively naturally.

---

## Weekly GSC Monitoring Checklist

Run this every Monday for any active pSEO site:

```
□ Indexing → Pages: Check "Total indexed" trend (should grow week-over-week)
□ Indexing → Pages → "Why pages aren't indexed": Triage top errors
□ Search results → Performance: Check impressions + clicks for new pages
□ URL Inspection: Spot-check 3-5 recently published pages for indexing status
□ Sitemaps: Confirm sitemap shows green (no errors)
□ Crawl stats (Settings → Crawling): Check for crawl spikes or drops
```

---

## GSC API (For Automated Monitoring)

For pSEO at scale, automate GSC data pulls:

```python
# pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
KEY_FILE = 'service-account-key.json'
SITE_URL = 'https://example.com/'

credentials = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
service = build('searchconsole', 'v1', credentials=credentials)

# Get indexing coverage
response = service.urlInspection().index().inspect(
    body={
        'inspectionUrl': 'https://example.com/austin-tx',
        'siteUrl': SITE_URL
    }
).execute()

print(response['inspectionResult']['indexStatusResult']['coverageState'])
```
