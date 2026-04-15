# Platform-Specific Implementation Reference

## Next.js (App Router)

The cleanest pSEO platform. App Router has native metadata API for sitemap and robots.

### Complete file structure
```
app/
├── sitemap.ts          ← Dynamic sitemap
├── robots.ts           ← robots.txt
├── llms.txt/
│   └── route.ts        ← llms.txt endpoint
├── llms-full.txt/
│   └── route.ts        ← llms-full.txt endpoint
└── [your-indexnow-key].txt/
    └── route.ts        ← IndexNow key verification
```

### sitemap.ts with database
```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export const revalidate = 3600 // Revalidate every hour

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const res = await fetch(`${process.env.API_URL}/pages`, {
    next: { revalidate: 3600 }
  })
  const pages = await res.json()

  return [
    { url: process.env.SITE_URL!, priority: 1.0, changeFrequency: 'weekly' },
    ...pages.map((p: any) => ({
      url: `${process.env.SITE_URL}/${p.slug}`,
      lastModified: new Date(p.updatedAt),
      changeFrequency: 'monthly' as const,
      priority: 0.7,
    }))
  ]
}
```

### robots.ts
```typescript
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: '*', allow: '/', disallow: ['/api/', '/admin/'] },
    sitemap: `${process.env.SITE_URL}/sitemap.xml`,
  }
}
```

### Handling 50,000+ URLs (Split Sitemaps)
```typescript
// app/sitemap/[page]/route.ts — individual sitemap files
// app/sitemap.xml/route.ts — sitemap index

const CHUNK_SIZE = 5000

export async function GET(req: Request, { params }: { params: { page: string } }) {
  const pageNum = parseInt(params.page)
  const offset = pageNum * CHUNK_SIZE
  
  const pages = await db.query(
    'SELECT slug, updated_at FROM pages ORDER BY id LIMIT $1 OFFSET $2',
    [CHUNK_SIZE, offset]
  )

  const xml = buildSitemapXML(pages)
  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } })
}
```

---

## Astro

### Installation
```bash
npm install @astrojs/sitemap
```

### astro.config.mjs
```javascript
import { defineConfig } from 'astro/config'
import sitemap from '@astrojs/sitemap'

export default defineConfig({
  site: 'https://example.com',
  integrations: [
    sitemap({
      // Exclude non-content routes
      filter: (page) => 
        !page.includes('/api/') && 
        !page.includes('/admin/') &&
        !page.includes('/auth/'),
      
      // Custom serialization
      serialize(item) {
        // Boost homepage priority
        if (item.url === 'https://example.com/') {
          return { ...item, priority: 1.0, changefreq: 'weekly' }
        }
        return { ...item, priority: 0.7, changefreq: 'monthly' }
      },
      
      // Add custom pages not in file system
      customPages: [
        'https://example.com/dynamically-generated-page',
      ],
    })
  ],
})
```

### robots.txt (static file)
```
# public/robots.txt
User-agent: *
Allow: /
Disallow: /api/

Sitemap: https://example.com/sitemap-index.xml
```

### Dynamic llms.txt endpoint
```typescript
// src/pages/llms.txt.ts
import type { APIRoute } from 'astro'
import { getAllCategories } from '../lib/data'

export const GET: APIRoute = async () => {
  const categories = await getAllCategories()
  
  const content = `# My Site\n\n> Site description\n\n## Categories\n\n${
    categories.map(c => `- [${c.name}](https://example.com/${c.slug}): ${c.description}`)
    .join('\n')
  }\n`
  
  return new Response(content, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' }
  })
}
```

---

## SvelteKit

### sitemap.xml endpoint
```typescript
// src/routes/sitemap.xml/+server.ts
import { getAllSlugs } from '$lib/server/data'
import type { RequestHandler } from './$types'

export const GET: RequestHandler = async () => {
  const slugs = await getAllSlugs()
  const BASE = 'https://example.com'
  
  const entries = slugs.map(slug => `
  <url>
    <loc>${BASE}/${slug}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>`).join('')

  return new Response(
    `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${entries}\n</urlset>`,
    { headers: { 'Content-Type': 'application/xml' } }
  )
}
```

### robots.txt endpoint
```typescript
// src/routes/robots.txt/+server.ts
export function GET() {
  return new Response(`User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: https://example.com/sitemap.xml`, {
    headers: { 'Content-Type': 'text/plain' }
  })
}
```

---

## Nuxt 3

### nuxt-simple-sitemap
```bash
npx nuxi module add sitemap
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  site: { url: 'https://example.com' },
  sitemap: {
    sources: ['/api/__sitemap__/urls'],  // API endpoint that returns URLs
    exclude: ['/admin/**', '/api/**'],
    defaults: { changefreq: 'monthly', priority: 0.7 },
  },
  robots: {
    disallow: ['/api/', '/admin/'],
    sitemap: 'https://example.com/sitemap.xml',
  },
})
```

---

## WordPress

### Yoast SEO (recommended)
- Settings → SEO → General → Features → XML Sitemaps → Enable
- Sitemap at: `https://example.com/sitemap_index.xml`
- Submit THIS URL to GSC and Bing (not sitemap.xml)

**For large pSEO WordPress sites:**
- Settings → SEO → Search Appearance → Content Types → toggle off post types you don't want indexed
- Yoast limits sitemap entries per file to 1,000 by default — increase with filter:
  ```php
  add_filter('wpseo_sitemap_entries_per_page', function() { return 5000; });
  ```

### robots.txt (WordPress)
Edit via: Yoast SEO → Tools → File Editor → robots.txt

```
User-agent: *
Allow: /wp-content/uploads/
Disallow: /wp-admin/
Disallow: /wp-includes/
Disallow: /?s=

Sitemap: https://example.com/sitemap_index.xml
```

---

## Static Sites (11ty / Hugo / Jekyll)

### 11ty
```javascript
// _data/sitemap.js — generates sitemap data
module.exports = async function() {
  // Return array of { url, lastmod }
}
```
Use `eleventy-plugin-sitemap` or generate via template.

### Hugo
```
# config.toml
[outputs]
home = ["HTML", "RSS", "SITEMAP"]

# Built-in sitemap at /sitemap.xml
```

### Jekyll
Use `jekyll-sitemap` gem — adds sitemap automatically from all published pages.

---

## Cloudflare Pages / Workers

### Sitemap via Worker
```javascript
// worker.js
addEventListener('fetch', event => {
  if (event.request.url.endsWith('/sitemap.xml')) {
    event.respondWith(generateSitemap())
  }
})

async function generateSitemap() {
  const pages = await fetch('https://your-api.com/pages').then(r => r.json())
  
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map(p => `  <url><loc>https://example.com/${p.slug}</loc></url>`).join('\n')}
</urlset>`

  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } })
}
```

### IndexNow with Cloudflare (Automatic)
Cloudflare → Speed → Optimization → Enable IndexNow
Cloudflare automatically pings IndexNow when it detects new/changed content.
