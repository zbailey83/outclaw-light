# Bing Webmaster Tools + IndexNow Reference

## Why Bing Matters for pSEO

Bing powers:
- **Bing.com** — #2 search engine, 3-6% global share (higher in US enterprise, older demographics)
- **Microsoft Copilot** — AI search powered by Bing's index
- **DuckDuckGo** — Powered by Bing
- **Yahoo Search** — Powered by Bing
- **Ecosia** — Powered by Bing

Total reach: ~30-35% of US searches when Bing-powered engines are combined.
Setup takes 15 minutes and costs nothing. Skip it and you're invisible on 1/3 of searches.

---

## Step 1: Set Up Bing Webmaster Tools

1. Go to [bing.com/webmasters](https://www.bing.com/webmasters)
2. Sign in with Microsoft account
3. Click **Add a site**
4. Enter your site URL

### Option A: Import from GSC (Fastest — 30 seconds)

If you've already verified in GSC:
1. Click **Import from Google Search Console**
2. Sign in to Google
3. Bing imports your verified properties and sitemap automatically

This is the recommended path. It verifies your domain AND submits your sitemap in one step.

### Option B: Manual Verification

**XML file method:**
1. Download `BingSiteAuth.xml` from Bing Webmaster Tools
2. Upload to site root: accessible at `https://example.com/BingSiteAuth.xml`
3. Click Verify

**Meta tag method:**
```html
<meta name="msvalidate.01" content="ABC123" />
```

**CNAME method (for DNS verification):**
Add a CNAME record pointing to `verify.bing.com`

---

## Step 2: Submit Sitemap to Bing

If you didn't import from GSC:

1. Bing Webmaster Tools → **Sitemaps**
2. Click **Submit sitemap**
3. Enter: `https://example.com/sitemap.xml`

Bing accepts the same sitemap format as Google.

---

## Step 3: Set Up IndexNow (The Real Win)

**IndexNow is the most underused pSEO tool that exists.**

IndexNow is a protocol that lets you ping Bing (and other search engines) the moment you
publish or update a URL. Instead of waiting for Bing to crawl your sitemap, it processes
new URLs within minutes to hours.

**Participating engines:** Bing, Yandex, DuckDuckGo (via Bing), Seznam.cz
Google has not joined IndexNow as of 2025 but watches Bing's index for signals.

### IndexNow Setup: Manual

**1. Generate your key**

Create a random key (32+ character alphanumeric string):
```bash
openssl rand -hex 32
# → a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4
```

**2. Host the key file**

Create a file at `https://example.com/[your-key].txt` containing just the key:
```
a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4
```

For Next.js, put it in `public/[key].txt`.
For Astro, put it in `public/[key].txt`.

**3. Ping IndexNow on publish**

```bash
curl -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json" \
  -d '{
    "host": "example.com",
    "key": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4",
    "keyLocation": "https://example.com/a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4.txt",
    "urlList": [
      "https://example.com/new-page-1",
      "https://example.com/new-page-2"
    ]
  }'
```

**4. Verify the key in Bing Webmaster Tools**

1. Bing Webmaster Tools → **Settings** → **IndexNow**
2. Enter your key
3. Click Verify

---

### IndexNow: Node.js Post-Deploy Script

```javascript
// scripts/ping-indexnow.js
const fetch = require('node-fetch')

const INDEXNOW_KEY = process.env.INDEXNOW_KEY
const SITE_URL = process.env.SITE_URL || 'https://example.com'

async function pingIndexNow(urls) {
  if (!urls || urls.length === 0) {
    console.log('No URLs to ping')
    return
  }

  // IndexNow accepts max 10,000 URLs per request
  const chunks = []
  for (let i = 0; i < urls.length; i += 10000) {
    chunks.push(urls.slice(i, i + 10000))
  }

  for (const chunk of chunks) {
    const response = await fetch('https://api.indexnow.org/indexnow', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        host: new URL(SITE_URL).hostname,
        key: INDEXNOW_KEY,
        keyLocation: `${SITE_URL}/${INDEXNOW_KEY}.txt`,
        urlList: chunk
      })
    })

    if (response.ok) {
      console.log(`✅ Pinged IndexNow for ${chunk.length} URLs`)
    } else {
      console.error(`❌ IndexNow error: ${response.status}`, await response.text())
    }
  }
}

// Get URLs from command line args or a file
const urls = process.argv.slice(2).length > 0 
  ? process.argv.slice(2)
  : require('./data/new-urls.json')

pingIndexNow(urls)
```

### IndexNow: Python Post-Deploy Script

```python
# scripts/ping_indexnow.py
import os
import json
import requests
from urllib.parse import urlparse

INDEXNOW_KEY = os.environ['INDEXNOW_KEY']
SITE_URL = os.environ.get('SITE_URL', 'https://example.com')
INDEXNOW_ENDPOINT = 'https://api.indexnow.org/indexnow'

def ping_indexnow(urls: list[str]) -> None:
    if not urls:
        print("No URLs to ping")
        return
    
    hostname = urlparse(SITE_URL).netloc
    
    # Chunk into 10k URL batches
    for i in range(0, len(urls), 10000):
        chunk = urls[i:i + 10000]
        payload = {
            "host": hostname,
            "key": INDEXNOW_KEY,
            "keyLocation": f"{SITE_URL}/{INDEXNOW_KEY}.txt",
            "urlList": chunk
        }
        
        response = requests.post(
            INDEXNOW_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        if response.ok:
            print(f"✅ Pinged IndexNow for {len(chunk)} URLs")
        else:
            print(f"❌ IndexNow error: {response.status_code}: {response.text}")

if __name__ == "__main__":
    import sys
    urls = sys.argv[1:] if len(sys.argv) > 1 else json.load(open("data/new_urls.json"))
    ping_indexnow(urls)
```

---

### IndexNow: Platform Integrations

**Vercel:**
- Install the [Bing Webmaster Tools integration](https://vercel.com/integrations/bing-webmaster-tools)
- Automatically pings IndexNow on every deployment

**Cloudflare:**
- Cloudflare has native IndexNow support in Speed → Optimization

**WordPress:**
- Rank Math Pro has IndexNow built in
- Yoast SEO Premium has IndexNow built in

**GitHub Actions (CI/CD):**
```yaml
# .github/workflows/deploy.yml
- name: Ping IndexNow
  run: |
    node scripts/ping-indexnow.js
  env:
    INDEXNOW_KEY: ${{ secrets.INDEXNOW_KEY }}
    SITE_URL: https://example.com
```

---

## IndexNow Response Codes

| Code | Meaning |
|------|---------|
| 200 | Accepted — all URLs queued |
| 202 | Accepted — some may be filtered |
| 400 | Bad request — check JSON format |
| 403 | Forbidden — key mismatch or not found |
| 422 | Unprocessable — URLs don't match `host` |
| 429 | Too many requests — rate limited |

---

## Bing Webmaster Tools Weekly Monitoring

```
□ Dashboard: Check "Total crawled" and "Total indexed" trends
□ Reports → Index Explorer: Look for crawl errors on pSEO pages
□ Reports → Search Performance: Impressions/clicks for new page batches
□ Sitemaps: Confirm sitemap processes without errors
□ IndexNow: Verify recent pings show in the IndexNow log
```
