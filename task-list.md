🏷️ Meta Tags & On-Page SEO

**Status:** 5 Important Items

* [x] **#5 Rewrite homepage meta description**
  * **Finding:** No meta description tag found in homepage HTML.
  * **Action:** Add:`<meta name="description" content="OutClaw AI is the weekly newsletter for builders — practical AI workflows, MCP guides, and prompt frameworks that help you automate your stack and ship faster. Free every Tuesday." />`.
* [x] **#6 Add unique descriptions to all guide and tool pages**
  * **Finding:** Guide pages appear to have titles but no confirmed meta descriptions in source.
  * **Action:** Audit every page for meta description presence and write unique 140–155 character descriptions for each.
* [x] **#7 Standardize title tag format**
  * **Finding:** Inconsistent separators (| vs —) and branding ("OutClaw" vs "OutClaw AI").
  * **Action:** Use standard format:`[Primary Keyword] | OutClaw AI`.
* [x] **#8 Add Open Graph and Twitter Card tags**
  * **Finding:** OG tags not confirmed; shared links will display as plain text without preview cards.
  * **Action:** Implement tags for `og:title`,`og:image` (1200x630px), and `twitter:card`.
* [x] **#9 Add canonical tags**
  * **Why it matters:** Prevents duplicate content issues caused by trailing slash inconsistencies or www vs non-www versions.
  * **Action:** Add `<link rel="canonical" href="https://outclaw.xyz/..." />` to the `<head>` of every page.

---

## 🤖 Structured Data / Schema Markup

**Status:** 3 Critical Items

* [x] **#10 Add Article + Person schema to every guide**
  * **Finding:** Zero JSON-LD schema found; no structured author attribution to establish E-E-A-T.
  * **Action:** Add `TechArticle` schema to all guides referencing Zach Bailey as the author.
* [x] **#11 Add FAQPage schema to all FAQ sections**
  * **Finding:** Q&A pairs exist but lack schema, missing out on prime AI answer engine real estate.
  * **Action:** Implement `FAQPage` JSON-LD to appear in Perplexity, ChatGPT Search, and Google AI Overviews.
* [x] **#12 Add Organization + WebSite schema to the homepage**
  * **Why it matters:** Establishes OutClaw as a known entity in Google's Knowledge Graph.

---

## ⚡ Performance & Core Web Vitals

**Status:** 3 Important Items

* [ ] **#13 Add explicit width/height attributes to images**
  * **Finding:** Homepage hero and icons lack dimensions, causing Cumulative Layout Shift (CLS).
  * **Action:** Update `<img>` tags with `width`,`height`,`loading="lazy"`, and `decoding="async"`.
* [ ] **#14 Run PageSpeed Insights and resolve LCP / FCP issues**
  * **Action:** Target LCP < 2.5s; preload hero images and ensure Google Fonts use `display=swap`.
* [ ] **#15 Add descriptive alt text to icons and images**
  * **Finding:** Multiple SVG icons on `/guides/` have empty or missing alt attributes.
  * **Action:** Use `alt=""` for decorative icons and descriptive text for meaningful ones.

---

## 🧠 LLMs.txt & AI Engine Signals

**Status:** 3 Critical Items

* [ ] **#16 Create /llms.txt**
  * **Finding:** File does not exist; content is deprioritized or excluded from AI citations.
  * **Action:** Create `outclaw.xyz/llms.txt` with site overview, author details, and key content links.
* [ ] **#17 Add Speakable schema to key guide sections**
  * **Why it matters:** Marks specific selectors (TL;DR, Verdict boxes) as the most citable content for AI answers.
* [ ] **#18 Add /llms-full.txt**
  * **Action:** Create an extended markdown file containing full content of the top 3–5 guides for AI ingestion.

---

## 📝 Content Structure & Entity SEO

**Status:** 5 Important Items

* [ ] **#19 Add TL;DR / Key Takeaways box to every guide**
  * **Finding:** Guides dive straight into content; AI engines favor pages with structured summary boxes at the top.
  * **Action:** Insert a 4–6 bullet point summary immediately after the intro paragraph.
* [ ] **#20 Build comparison / alternative pages**
  * **Opportunity:** Target high-intent keywords like "Claude vs GPT-5" or "MCP vs LangChain".
* [ ] **#21 Add publish and modified dates to all guides**
  * **Finding:** UI shows dates but no machine-readable freshness signals are confirmed.
  * **Action:** Add visible date lines and include `datePublished`/`dateModified` in JSON-LD.
* [ ] **#22 Add a /videos/ page with VideoObject schema**
  * **Finding:** Page is in the nav but appears empty of content.
  * **Action:** Populate with videos and schema to appear in Google's video carousel.
* [ ] **#23 Expand /newsletter/ page with past issue summaries**
  * **Opportunity:** Archive summaries (200–300 words) create fresh crawlable content for long-tail queries.

---

## 🎖️ E-E-A-T & Author Authority

**Status:** 4 Important Items

* [ ] **#24 Create a dedicated /about/zach-bailey author page**
  * **Finding:** Author is mentioned but lacks a stable URL for Article schema attribution.
  * **Action:** Include credentials, social links, and Person schema on a dedicated page.
* [ ] **#25 Add "By [Author]" attribution with links**
  * **Action:** Link bylines to the new author page and add a brief bio at the bottom of every guide.
* [ ] **#26 Fix Twitter handle inconsistency**
  * **Finding:** Interchangeable use of `@outclawai` and `@zbailey83` fragments social proof.
  * **Action:** Standardize `@outclawai` for the brand and `@zbailey83` for the author person.
* [ ] **#27 Add a "Methodology" section to /about/**
  * **Why it matters:** Explaining how you test tools signals trustworthiness to quality raters.

---

## 🔗 Internal Links, Backlinks & Social

**Status:** 5 Improvements

* [ ] **#28 Add contextual internal links between guides and tools**
  * **Finding:** Most guides have zero cross-links; orphaned pages wait weeks to be discovered.
  * **Action:** Manually link guides to relevant tools using descriptive anchor text.
* [ ] **#29 Add "Related Guides" section to the bottom of every guide**
  * **Why it matters:** Increases pages per session and spreads link equity.
* [ ] **#30 Add breadcrumb navigation**
  * **Action:** Implement breadcrumbs with `BreadcrumbList` schema to increase SERP click-through rates.
* [ ] **#31 Submit OutClaw to AI directories and curator lists**
  * **Action:** Target Letterlist, Futurepedia, and Product Hunt for early backlinks.
* [ ] **#32 Schema-mark testimonials**
  * **Finding:** Current testimonials use handles but lack verifiable detail.
  * **Action:** Add `Review` schema and aggregate ratings to social proof.
