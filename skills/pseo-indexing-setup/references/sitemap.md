# Sitemaps Reference

## Sitemap Fundamentals

### URL Limits
- Max **50,000 URLs per sitemap file**
- Max **50MB uncompressed** per file
- For pSEO sites over 50k pages: use a **sitemap index** that references child sitemaps

### Required Fields
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page</loc>          <!-- required, absolute URL -->
    <lastmod>2025-01-15</lastmod>                 <!-- recommended, ISO 8601 -->
    <changefreq>weekly</changefreq>               <!-- optional, mostly ignored -->
    <priority>0.8</priority>                      <!-- optional, 0.0–1.0, mostly ignored -->
  </url>
</urlset>
```

> `changefreq` and `priority` are largely ignored by Google. Include `lastmod` — it does matter for recrawl prioritization.

---

## Sitemap Index (for large pSEO sites)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemaps/cities-1.xml</loc>
    <lastmod>2025-04-01</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemaps/cities-2.xml</loc>
    <lastmod>2025-04-01</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemaps/categories.xml</loc>
    <lastmod>2025-04-01</lastmod>
  </sitemap>
</sitemapindex>
```

Segment child sitemaps by **template type**, not alphabetically. This gives you clean crawl data in GSC per template.

---

## Framework-Specific Implementations

### Next.js 13+ (App Router)

**`/app/sitemap.ts`** — dynamic sitemap:

```typescript
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://example.com'
  
  // Fetch your pSEO data
  const cities = await db.cities.findMany({ select: { slug: true, updatedAt: true } })
  const categories = await db.categories.findMany({ select: { slug: true, updatedAt: true } })
  
  const cityUrls = cities.map((city) => ({
    url: `${baseUrl}/cities/${city.slug}`,
    lastModified: city.updatedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }))
  
  const categoryUrls = categories.map((cat) => ({
    url: `${baseUrl}/categories/${cat.slug}`,
    lastModified: cat.updatedAt,
    changeFrequency: 'monthly' as const,
    priority: 0.6,
  }))
  
  return [
    { url: baseUrl, lastModified: new Date(), priority: 1.0 },
    ...cityUrls,
    ...categoryUrls,
  ]
}
```

**For large datasets (50k+ pages), use multiple sitemap files:**

```typescript
// /app/sitemap/[type]/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(
  request: NextRequest,
  { params }: { params: { type: string } }
) {
  const { type } = params
  const baseUrl = 'https://example.com'
  
  let urls: string[] = []
  
  if (type === 'cities') {
    const cities = await db.cities.findMany({ select: { slug: true } })
    urls = cities.map(c => `${baseUrl}/cities/${c.slug}`)
  }
  
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(url => `  <url><loc>${url}</loc></url>`).join('\n')}
</urlset>`
  
  return new NextResponse(xml, {
    headers: { 'Content-Type': 'application/xml' }
  })
}
```

### Next.js Pages Router

```typescript
// /pages/sitemap.xml.ts
import { GetServerSideProps } from 'next'

function Sitemap() { return null }

export const getServerSideProps: GetServerSideProps = async ({ res }) => {
  const baseUrl = 'https://example.com'
  const pages = await fetchAllPages()
  
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map(p => `
  <url>
    <loc>${baseUrl}/${p.slug}</loc>
    <lastmod>${p.updatedAt.toISOString().split('T')[0]}</lastmod>
  </url>`).join('')}
</urlset>`

  res.setHeader('Content-Type', 'text/xml')
  res.write(xml)
  res.end()
  
  return { props: {} }
}

export default Sitemap
```

### Astro

```typescript
// /src/pages/sitemap.xml.ts
import type { APIRoute } from 'astro'
import { getCollection } from 'astro:content'

export const GET: APIRoute = async ({ site }) => {
  const baseUrl = site?.toString() ?? 'https://example.com'
  const pages = await getCollection('pages')
  
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map(page => `  <url>
    <loc>${baseUrl}${page.slug}</loc>
    <lastmod>${page.data.updatedAt ?? new Date().toISOString()}</lastmod>
  </url>`).join('\n')}
</urlset>`

  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' }
  })
}
```

> Alternatively, use the official `@astrojs/sitemap` integration for small-to-medium sites.

### SvelteKit

```typescript
// /src/routes/sitemap.xml/+server.ts
import type { RequestHandler } from './$types'
import { db } from '$lib/db'

export const GET: RequestHandler = async () => {
  const baseUrl = 'https://example.com'
  const pages = await db.pages.findMany({ select: { slug: true, updatedAt: true } })
  
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map(p => `  <url>
    <loc>${baseUrl}/${p.slug}</loc>
    <lastmod>${p.updatedAt.toISOString().split('T')[0]}</lastmod>
  </url>`).join('\n')}
</urlset>`

  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml' }
  })
}
```

### Nuxt 3

```typescript
// /server/routes/sitemap.xml.ts
export default defineEventHandler(async (event) => {
  const baseUrl = 'https://example.com'
  const pages = await $fetch('/api/pages')
  
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map((p: any) => `  <url>
    <loc>${baseUrl}/${p.slug}</loc>
    <lastmod>${p.updatedAt}</lastmod>
  </url>`).join('\n')}
</urlset>`

  setHeader(event, 'Content-Type', 'application/xml')
  return xml
})
```

> Also consider `@nuxtjs/sitemap` module for complex setups.

---

## Sitemap Segmentation Strategy (pSEO)

For pSEO sites, segment sitemaps by template so GSC shows per-template indexing health:

```
/sitemap-index.xml
  ├── /sitemaps/homepage.xml        (1 URL)
  ├── /sitemaps/category.xml        (100–10k URLs)
  ├── /sitemaps/city.xml            (1k–100k URLs)
  ├── /sitemaps/city-category.xml   (10k–1M URLs)
  └── /sitemaps/blog.xml            (100–10k URLs)
```

This lets you see exactly which template Google is struggling to crawl/index.

---

## Common Sitemap Mistakes

| Mistake | Fix |
|---------|-----|
| Including `noindex` pages | Only index pages you want indexed |
| Non-canonical URLs in sitemap | sitemap URLs must match `<link rel="canonical">` exactly |
| Including 404 pages | Audit sitemap vs live URLs monthly |
| Static sitemap for dynamic content | Generate dynamically at build or request time |
| Missing `lastmod` | Always include — affects recrawl scheduling |
| Relative URLs | All `<loc>` values must be absolute (`https://`) |
| HTTP instead of HTTPS | Use HTTPS even if HTTP redirects to it |
