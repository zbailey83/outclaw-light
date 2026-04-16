# llms.txt Reference

## What is llms.txt?

`llms.txt` is a proposed standard (llmstxt.org) that tells AI language model crawlers —
Perplexity, ChatGPT Browse, Claude, Gemini — what your site is about and which pages
to include or exclude from their knowledge and citations.

Think of it as `robots.txt` for AI answer engines, combined with a structured summary
of your site for LLM context windows.

**Why it matters for pSEO:** AI-powered search is growing. Sites with well-structured
`llms.txt` files get cited more accurately in AI search results. Sites without one
get ignored or hallucinated about.

---

## The Two Files

| File | Purpose | Size |
|------|---------|------|
| `/llms.txt` | Short summary + key links. Fits in a single LLM context window. | < 2,000 tokens |
| `/llms-full.txt` | Complete site content map, all pages, full descriptions. | Unlimited |

`llms.txt` links to `llms-full.txt`. LLMs use the short version first and pull the full
version only if they need deeper context.

---

## llms.txt Format (Standard)

```markdown
# [Site Name]

> [One sentence description of what the site is and who it serves]

[2-4 sentence overview of the site's purpose, main topics, and value proposition]

## [Main Section 1]

- [Page Title](https://example.com/page-1): [One-line description of what this page covers]
- [Page Title](https://example.com/page-2): [One-line description]

## [Main Section 2]

- [Page Title](https://example.com/page-3): [One-line description]

## Optional

- [llms-full.txt](https://example.com/llms-full.txt): Complete content map with all pages
```

---

## Example: pSEO City Guide Site

```markdown
# LocalGuide — Best Things To Do By City

> Programmatic guides for 10,000+ US cities, covering restaurants, activities,
> neighborhoods, and day trips for travelers and locals.

LocalGuide covers every US city with population over 1,000. Each city guide is written
by combining local data sources with editorial curation. Content is updated monthly.
We cover dining, outdoor activities, neighborhoods, nightlife, and seasonal guides.

## Top City Guides

- [Best Restaurants in Austin TX](https://localguide.com/austin-tx/restaurants): Curated list of 50+ Austin restaurants by neighborhood and cuisine type
- [Things to Do in Denver CO](https://localguide.com/denver-co/activities): Outdoor activities, museums, and events across all seasons
- [Nashville TN Neighborhoods](https://localguide.com/nashville-tn/neighborhoods): Guide to every Nashville neighborhood including cost of living and vibe

## Category Index

- [All City Restaurant Guides](https://localguide.com/restaurants): Index of restaurant guides for 10,000+ US cities
- [All Outdoor Activity Guides](https://localguide.com/activities/outdoor): Hiking, biking, and nature guides by city

## About

- [About LocalGuide](https://localguide.com/about): How we research and write our city guides
- [Data Sources](https://localguide.com/data-sources): Third-party data we use

## Optional

- [llms-full.txt](https://localguide.com/llms-full.txt): Complete index of all 10,000+ city pages
```

---

## llms-full.txt Format

The full version lists every significant page on the site:

```markdown
# LocalGuide — Complete Content Index

> Full index of all pages on LocalGuide.com for AI crawler reference.

Last updated: 2025-04-01
Total pages: 47,832

## City Guides — Texas

- [Austin TX Complete Guide](https://localguide.com/austin-tx): Full city guide for Austin, Texas
- [Austin TX Restaurants](https://localguide.com/austin-tx/restaurants): Restaurant guide for Austin TX
- [Austin TX Activities](https://localguide.com/austin-tx/activities): Things to do in Austin TX
- [Dallas TX Complete Guide](https://localguide.com/dallas-tx): Full city guide for Dallas, Texas
[... continues for all pages ...]
```

---

## Generating llms.txt Dynamically

**Next.js:**
```typescript
// app/llms.txt/route.ts
import { getAllCategories, getFeaturedPages } from '@/lib/data'

export async function GET() {
  const categories = await getAllCategories()
  const featured = await getFeaturedPages(20)

  const content = `# ${process.env.SITE_NAME}

> ${process.env.SITE_DESCRIPTION}

${process.env.SITE_ABOUT}

## Featured Pages

${featured.map(p => `- [${p.title}](${process.env.SITE_URL}/${p.slug}): ${p.description}`).join('\n')}

## Categories

${categories.map(c => `- [${c.name}](${process.env.SITE_URL}/${c.slug}): ${c.description}`).join('\n')}

## Optional

- [llms-full.txt](${process.env.SITE_URL}/llms-full.txt): Complete page index
`

  return new Response(content, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' }
  })
}
```

**llms-full.txt endpoint (paginated):**
```typescript
// app/llms-full.txt/route.ts
import { getAllPages } from '@/lib/data'

export async function GET() {
  const pages = await getAllPages()
  
  const grouped = groupByCategory(pages)
  
  let content = `# ${process.env.SITE_NAME} — Complete Index\n\n`
  content += `> Full page index. Last updated: ${new Date().toISOString().split('T')[0]}\n\n`
  
  for (const [category, items] of Object.entries(grouped)) {
    content += `## ${category}\n\n`
    content += items.map(p => 
      `- [${p.title}](${process.env.SITE_URL}/${p.slug}): ${p.description}`
    ).join('\n')
    content += '\n\n'
  }

  return new Response(content, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' }
  })
}
```

---

## Declare in robots.txt

Add to your robots.txt to help crawlers find these files:

```
# AI crawler guidance
llms.txt: https://example.com/llms.txt
```

Some crawlers also look for these automatically at `/llms.txt` — serve it at the root.

---

## Best Practices

1. **Put your most important pages first** — LLMs often read top-to-bottom and stop early
2. **Descriptions must be unique and accurate** — Vague descriptions get ignored
3. **Keep llms.txt under 2,000 tokens** — It must fit in a single context window pass
4. **Update llms-full.txt on every publish** — Stale indexes undermine trust
5. **Include canonical URL format** — Match exactly what's in your sitemap
6. **Link between the two files** — llms.txt → llms-full.txt, and vice versa

---

## Validation

No official validator yet. Manual checklist:
- [ ] File loads at `https://example.com/llms.txt`
- [ ] File is plain text, not HTML
- [ ] Markdown renders correctly
- [ ] All linked URLs are live (spot check 10)
- [ ] File is under 2,000 tokens (use tokenizer: platform.openai.com/tokenizer)
- [ ] llms-full.txt linked from llms.txt
