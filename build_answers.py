import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from answers_data import ANSWERS

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
ANSWERS_DIR = os.path.join(WORKSPACE_DIR, "answers")

CATEGORIES = {
    "mcp-connectors": "MCP & Connectors",
    "claude-api": "Claude API",
    "tool-use": "Tool Use & Function Calling",
    "agent-frameworks": "Agent Frameworks",
    "claude-code": "Claude Code"
}

CATEGORY_DESCS = {
    "mcp-connectors": "How to connect Claude and AI agents to third-party apps via MCP servers — Gmail, Notion, GitHub, Slack, and more.",
    "claude-api": "Rate limits, model strings, authentication, streaming, errors — the technical reference developers use at runtime.",
    "tool-use": "Schemas, parallel execution, result handling, and parameters for Claude function calling.",
    "agent-frameworks": "LangGraph, CrewAI, AutoGen, LlamaIndex, and the Vercel AI SDK — how Claude plugs into agentic systems.",
    "claude-code": "CLI setup, config files, slash commands, headless CI execution, and agentic workspace workflows."
}

GA4_SNIPPET = """<!-- GA4 User Journey Tag -->
<script>
  window.GA4_MEASUREMENT_ID = "G-JHMN90H7MC";
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  if (window.location.hostname !== 'outclaw.xyz') {
    console.log('GA4 Analytics: Local development environment detected. Mocking script load.');
    gtag('config', window.GA4_MEASUREMENT_ID, { 'debug_mode': true });
  } else {
    (function() {
      var script = document.createElement('script');
      script.async = true;
      script.src = 'https://www.googletagmanager.com/gtag/js?id=' + window.GA4_MEASUREMENT_ID;
      document.head.appendChild(script);
    })();
    gtag('config', window.GA4_MEASUREMENT_ID);
  }
</script>
<script src="/analytics-journey.js" defer></script>
"""

GTM_SNIPPET = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-5VC26C47');</script>
<!-- End Google Tag Manager -->
"""

def build_navbar(prefix, active_cat):
    about_active = ' class="active"' if active_cat == 'about' else ''
    guides_active = ' class="active"' if active_cat == 'guides' else ''
    answers_active = ' class="active"' if active_cat == 'answers' else ''
    videos_active = ' class="active"' if active_cat == 'videos' else ''
    tools_active = ' class="active"' if active_cat == 'tools' else ''
    newsletter_active = ' class="active"' if active_cat == 'newsletter' else ''
    
    logo_path = f"{prefix}outclaw-icons/Wild-Bird-Flamingo--Streamline-Ultimate.png"
    
    return f"""<nav class="navbar" id="mainNav">
    <a href="{prefix or './'}" class="navbar-logo">
      <img src="{logo_path}" alt="OutClaw AI" class="navbar-logo-img">
      <div class="navbar-wordmark">Out<em>claw</em> AI</div>
    </a>
    <div class="navbar-links">
      <a href="{prefix}about/"{about_active}>About</a>
      <a href="{prefix}guides/"{guides_active}>Guides</a>
      <a href="{prefix}answers/"{answers_active}>Answers</a>
      <a href="{prefix}videos/"{videos_active}>Videos</a>
      <a href="{prefix}tools/"{tools_active}>Tools</a>
      <a href="{prefix}newsletter/"{newsletter_active}>Newsletter</a>
    </div>
    <div class="navbar-right">
      <a href="{prefix}newsletter/" class="nav-cta">Subscribe Free &#x2192;</a>
      <button class="nav-hamburger" onclick="toggleDrawer()" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>
  <div class="nav-drawer" id="navDrawer">
    <a href="{prefix}about/"{about_active}>About</a>
    <a href="{prefix}guides/"{guides_active}>Guides</a>
    <a href="{prefix}answers/"{answers_active}>Answers</a>
    <a href="{prefix}videos/"{videos_active}>Videos</a>
    <a href="{prefix}tools/"{tools_active}>Tools</a>
    <a href="{prefix}newsletter/"{newsletter_active}>Newsletter</a>
    <a href="{prefix}newsletter/" class="nav-cta">Subscribe Free &#x2192;</a>
  </div>"""

def build_footer(prefix, active_cat):
    about_active = ' class="active"' if active_cat == 'about' else ''
    guides_active = ' class="active"' if active_cat == 'guides' else ''
    answers_active = ' class="active"' if active_cat == 'answers' else ''
    videos_active = ' class="active"' if active_cat == 'videos' else ''
    tools_active = ' class="active"' if active_cat == 'tools' else ''
    newsletter_active = ' class="active"' if active_cat == 'newsletter' else ''
    
    logo_path = f"{prefix}outclaw-icons/Wild-Bird-Flamingo--Streamline-Ultimate.png"
    
    return f"""<footer>
    <a href="{prefix or './'}" class="footer-logo">
      <img src="{logo_path}" alt="OutClaw AI Footer Logo" style="width: 22px; height: 22px; filter: drop-shadow(0 2px 6px rgba(244, 103, 138, .2));">
      <div class="footer-wordmark">Out<em>claw</em> AI</div>
      <p style="font-size:12px;color:rgba(255,255,255,.2);margin-top:4px;"><a href="https://seolittleton.com" target="_blank" style="color:inherit;text-decoration:underline;font-weight:bold;">SEO Littleton</a> &amp; <a href="https://distropixel.com" target="_blank" style="color:inherit;text-decoration:underline;font-weight:bold;">DistroPixel</a></p>
    </a>
    <div class="footer-links">
      <a href="{prefix}about/"{about_active}>About</a>
      <a href="{prefix}guides/"{guides_active}>Guides</a>
      <a href="{prefix}answers/"{answers_active}>Answers</a>
      <a href="{prefix}videos/"{videos_active}>Videos</a>
      <a href="{prefix}tools/"{tools_active}>Tools</a>
      <a href="{prefix}newsletter/"{newsletter_active}>Newsletter</a>
      <a href="{prefix}privacy/">Privacy</a>
      <a href="mailto:zbailey83@gmail.com">Contact</a>
    </div>
    <div class="footer-copy">&copy; 2026 OutClaw AI. All rights reserved.</div>
  </footer>"""

def create_dirs():
    os.makedirs(ANSWERS_DIR, exist_ok=True)
    for cat in CATEGORIES:
        os.makedirs(os.path.join(ANSWERS_DIR, cat), exist_ok=True)

def generate_individual_pages():
    for item in ANSWERS:
        slug = item["slug"]
        question = item["question"]
        cat = item["category"]
        cat_name = item["category_name"]
        quick_ans = item["quick_answer"]
        ans_type = item["answer_type"]
        body = item["body"]
        verified_ag = item["verified_against"]
        verified_dt = item["verified_date"]
        related_slugs = item.get("related_slugs", [])

        # Fetch related answers details
        related_html = ""
        related_items = [x for x in ANSWERS if x["slug"] in related_slugs]
        if related_items:
            related_html += '<div class="related-answers"><h3>Related answers</h3><ul>'
            for r in related_items:
                r_url = f"/answers/{r['category']}/{r['slug']}.html"
                related_html += f'<li><a href="{r_url}">{r["question"]}</a></li>'
            related_html += f'<li><a href="/answers/{cat}/">See all {cat_name} answers</a></li>'
            related_html += '</ul></div>'

        # Generate JSON-LD schema
        schema_graph = []
        
        # 1. BreadcrumbList
        schema_graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Answers",
                    "item": "https://outclaw.xyz/answers/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": cat_name,
                    "item": f"https://outclaw.xyz/answers/{cat}/"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": question,
                    "item": f"https://outclaw.xyz/answers/{cat}/{slug}.html"
                }
            ]
        })

        # 2. HowTo / DefinedTerm / FAQPage
        if ans_type == "steps":
            # Extract steps from body html roughly
            steps_list = []
            import re
            lis = re.findall(r'<li>(.*?)</li>', body, re.DOTALL)
            # Remove any HTML tags inside list items for schema text
            clean_re = re.compile('<.*?>')
            for i, li in enumerate(lis):
                clean_text = re.sub(clean_re, '', li).strip()
                if clean_text:
                    steps_list.append({
                        "@type": "HowToStep",
                        "name": f"Step {i+1}",
                        "text": clean_text
                    })
            schema_graph.append({
                "@context": "https://schema.org",
                "@type": "HowTo",
                "name": question,
                "description": quick_ans,
                "step": steps_list,
                "datePublished": "2026-06-01",
                "dateModified": "2026-07-05"
            })
        else:
            # FAQ / Reference type
            schema_graph.append({
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [{
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": quick_ans
                    }
                }]
            })

        # 3. Article schema
        schema_graph.append({
            "@type": "Article",
            "headline": question,
            "description": quick_ans,
            "datePublished": "2026-06-01",
            "dateModified": "2026-07-05",
            "author": {
                "@type": "Organization",
                "name": "openclaw.xyz"
            },
            "publisher": {
                "@type": "Organization",
                "name": "openclaw.xyz",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://outclaw.xyz/outclaw-icons/Wild-Bird-Flamingo--Streamline-Ultimate.png"
                }
            }
        })

        schema_json = json.dumps({"@context": "https://schema.org", "@graph": schema_graph}, indent=2)

        # Meta description (max 145 chars)
        meta_desc = quick_ans[:142] + "..." if len(quick_ans) > 145 else quick_ans

        navbar_html = build_navbar("../../", "answers")
        footer_html = build_footer("../../", "answers")

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  {GA4_SNIPPET}
  {GTM_SNIPPET}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{question} | Answers for Agents | openclaw.xyz</title>
  <meta name="description" content="{meta_desc}">
  <link rel="canonical" href="https://outclaw.xyz/answers/{cat}/{slug}.html">
  
  <meta property="og:title" content="{question}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:type" content="article">
  <meta property="article:modified_time" content="2026-07-05T00:00:00Z">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/answers/style.css">
  
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body>
  {navbar_html}

  <div class="layout-container">
    <nav class="breadcrumb-nav" aria-label="breadcrumb">
      <a href="/answers/">openclaw.xyz</a> / <a href="/answers/">Answers</a> / <a href="/answers/{cat}/">{cat_name}</a> / {question}
    </nav>

    <article>
      <div class="category-chip">{cat_name}</div>
      <h1>{question}</h1>
      
      <div class="entry-meta">
        Last verified: {verified_dt} &middot; 2 min read
      </div>

      <div class="quick-answer">
        <span class="qa-label">QUICK ANSWER</span>
        <p>{quick_ans}</p>
      </div>

      <div class="answer-body">
        {body}
      </div>

      <div class="verified-against">
        Verified against: {verified_ag}
      </div>

      {related_html}
    </article>
  </div>

  {footer_html}
  
  <script>
    function toggleDrawer() {{ document.getElementById("navDrawer").classList.toggle("open"); }}
    document.addEventListener("click", function (e) {{
      var n = document.getElementById("mainNav"), d = document.getElementById("navDrawer");
      if (!n.contains(e.target) && !d.contains(e.target)) d.classList.remove("open");
    }});
  </script>
</body>
</html>"""

        file_path = os.path.join(ANSWERS_DIR, cat, f"{slug}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

def generate_category_pages():
    for cat, cat_name in CATEGORIES.items():
        desc = CATEGORY_DESCS[cat]
        cat_answers = [x for x in ANSWERS if x["category"] == cat]
        
        # Grid list cards
        cards_html = ""
        for item in cat_answers:
            r_url = f"/answers/{cat}/{item['slug']}.html"
            preview = item["quick_answer"]
            if len(preview) > 130:
                preview = preview[:127] + "..."
            cards_html += f"""
    <div class="answer-card">
      <h3><a href="{r_url}">{item["question"]}</a></h3>
      <p>{preview}</p>
      <div class="meta">Last verified: {item["verified_date"]}</div>
    </div>"""

        # FAQ Cluster (top 5 questions as summary/details blocks)
        faq_html = ""
        faq_answers = cat_answers[:5]
        faq_entities = []
        if faq_answers:
            faq_html += '<section class="faq-cluster"><h2>Common questions</h2>'
            for item in faq_answers:
                faq_html += f"""
  <details>
    <summary>{item["question"]}</summary>
    <p>{item["quick_answer"]}</p>
  </details>"""
                faq_entities.append({
                    "@type": "Question",
                    "name": item["question"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item["quick_answer"]
                    }
                })
            faq_html += '</section>'

        # JSON-LD Schema (CollectionPage + FAQPage)
        schema_graph = [
            {
                "@context": "https://schema.org",
                "@type": "CollectionPage",
                "name": f"{cat_name} — AI Agent Reference",
                "description": desc,
                "url": f"https://outclaw.xyz/answers/{cat}/",
                "publisher": { "@type": "Organization", "name": "openclaw.xyz" }
            },
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    { "@type": "ListItem", "position": 1, "name": "Answers", "item": "https://outclaw.xyz/answers/" },
                    { "@type": "ListItem", "position": 2, "name": cat_name }
                ]
            }
        ]
        
        if faq_entities:
            schema_graph.append({
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": faq_entities
            })

        schema_json = json.dumps({"@context": "https://schema.org", "@graph": schema_graph}, indent=2)

        navbar_html = build_navbar("../../", "answers")
        footer_html = build_footer("../../", "answers")

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  {GA4_SNIPPET}
  {GTM_SNIPPET}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{cat_name} &mdash; AI Agent Reference | Answers | openclaw.xyz</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://outclaw.xyz/answers/{cat}/">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/answers/style.css">
  
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body>
  {navbar_html}

  <div class="layout-container">
    <nav class="breadcrumb-nav" aria-label="breadcrumb">
      <a href="/answers/">openclaw.xyz</a> / <a href="/answers/">Answers</a> / {cat_name}
    </nav>

    <h1>{cat_name} &mdash; Agent Reference</h1>
    <p>{desc}</p>

    <div class="answer-grid">
      {cards_html}
    </div>

    {faq_html}
  </div>

  {footer_html}
  
  <script>
    function toggleDrawer() {{ document.getElementById("navDrawer").classList.toggle("open"); }}
    document.addEventListener("click", function (e) {{
      var n = document.getElementById("mainNav"), d = document.getElementById("navDrawer");
      if (!n.contains(e.target) && !d.contains(e.target)) d.classList.remove("open");
    }});
  </script>
</body>
</html>"""
        
        file_path = os.path.join(ANSWERS_DIR, cat, "index.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

def generate_master_page():
    # Category Grid Cards with counts and 2 featured questions
    grid_html = ""
    for cat, cat_name in CATEGORIES.items():
        desc = CATEGORY_DESCS[cat]
        cat_answers = [x for x in ANSWERS if x["category"] == cat]
        featured = cat_answers[:2]
        
        featured_html = ""
        for f in featured:
            featured_html += f'<li><a href="/answers/{cat}/{f["slug"]}.html">{f["question"]}</a></li>'
            
        grid_html += f"""
    <div class="category-card">
      <h3><a href="/answers/{cat}/">{cat_name} &rarr;</a></h3>
      <div class="count">{len(cat_answers)} reference entries</div>
      <p>{desc}</p>
      <ul class="featured-links">
        {featured_html}
      </ul>
    </div>"""

    # Recently Updated: Last 10 answers
    recent_html = ""
    # Sort or just slice the last 10
    recent_answers = ANSWERS[:10]
    for item in recent_answers:
        url = f"/answers/{item['category']}/{item['slug']}.html"
        recent_html += f"""
      <div class="recently-updated-item">
        <div class="left">
          <span class="cat">{item["category_name"]}</span>
          <a href="{url}">{item["question"]}</a>
        </div>
        <div class="date">{item["verified_date"]}</div>
      </div>"""

    # JSON-LD Schema
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "name": "Answers for Agents — Claude & AI Tool Reference | openclaw.xyz",
                "description": "Short, specific answers to questions AI agents and developers encounter when building with Claude and integrating AI tools.",
                "url": "https://outclaw.xyz/answers/",
                "publisher": { "@type": "Organization", "name": "openclaw.xyz" }
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    { "@type": "ListItem", "position": 1, "name": "openclaw.xyz", "item": "https://outclaw.xyz/" },
                    { "@type": "ListItem", "position": 2, "name": "Answers" }
                ]
            }
        ]
    }
    schema_json = json.dumps(schema, indent=2)

    navbar_html = build_navbar("../", "answers")
    footer_html = build_footer("../", "answers")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  {GA4_SNIPPET}
  {GTM_SNIPPET}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Answers for Agents &mdash; Claude &amp; AI Tool Reference | openclaw.xyz</title>
  <meta name="description" content="Short, specific answers to questions AI agents and developers encounter when building with Claude and integrating AI tools.">
  <link rel="canonical" href="https://outclaw.xyz/answers/">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/answers/style.css">
  
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body>
  {navbar_html}

  <div class="layout-container">
    <h1>Answers for Agents</h1>
    <p>Short, specific answers to questions AI agents and developers hit when building with Claude — updated as tools change.</p>

    <div class="search-wrapper">
      <input type="text" id="search-input" class="search-input" placeholder="Search categories, tools, or questions...">
    </div>

    <div class="category-grid">
      {grid_html}
    </div>

    <div class="recently-updated">
      <h2>Recently updated</h2>
      <div class="recently-updated-list">
        {recent_html}
      </div>
    </div>
  </div>

  {footer_html}
  
  <script>
    function toggleDrawer() {{ document.getElementById("navDrawer").classList.toggle("open"); }}
    document.addEventListener("click", function (e) {{
      var n = document.getElementById("mainNav"), d = document.getElementById("navDrawer");
      if (!n.contains(e.target) && !d.contains(e.target)) d.classList.remove("open");
    }});
    
    document.addEventListener('DOMContentLoaded', () => {{
      const searchInput = document.getElementById('search-input');
      const cards = document.querySelectorAll('.category-card');
      const recentItems = document.querySelectorAll('.recently-updated-item');
      
      searchInput.addEventListener('input', (e) => {{
        const query = e.target.value.toLowerCase().trim();
        
        cards.forEach(c => {{
          const text = c.textContent.toLowerCase();
          c.style.display = text.includes(query) ? 'flex' : 'none';
        }});
        
        recentItems.forEach(r => {{
          const text = r.textContent.toLowerCase();
          r.style.display = text.includes(query) ? 'flex' : 'none';
        }});
      }});
    }});
  </script>
</body>
</html>"""
    
    file_path = os.path.join(ANSWERS_DIR, "index.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

def generate_answers_sitemap():
    # Build answers/sitemap.xml
    root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # 1. Master index url
    url_element = ET.SubElement(root, "url")
    ET.SubElement(url_element, "loc").text = "https://outclaw.xyz/answers/"
    ET.SubElement(url_element, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
    
    # 2. Categories urls
    for cat in CATEGORIES:
        url_element = ET.SubElement(root, "url")
        ET.SubElement(url_element, "loc").text = f"https://outclaw.xyz/answers/{cat}/"
        ET.SubElement(url_element, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
        
    # 3. Individual pages urls
    for item in ANSWERS:
        url_element = ET.SubElement(root, "url")
        ET.SubElement(url_element, "loc").text = f"https://outclaw.xyz/answers/{item['category']}/{item['slug']}.html"
        ET.SubElement(url_element, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
        
    # Write formatted XML
    xml_str = ET.tostring(root, encoding="utf-8")
    
    # Simple pretty print for XML
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="   ")
    
    # minidom adds a header like <?xml version="1.0" ?> but we want to make sure it includes UTF-8
    if '<?xml version="1.0" ?>' in pretty_xml:
        pretty_xml = pretty_xml.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>')
        
    sitemap_path = os.path.join(ANSWERS_DIR, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    print("Generated sitemap: /answers/sitemap.xml")

def generate_llms_full():
    content = "# Answers for Agents — Quick Answers Full Catalog\n\n"
    content += "This catalog contains the self-contained Quick Answer snippets for all agent references on openclaw.xyz.\n\n"
    
    for item in ANSWERS:
        content += f"## {item['question']}\n"
        content += f"Category: {item['category_name']} | Slug: {item['slug']}\n\n"
        content += f"> {item['quick_answer']}\n\n"
        content += f"Full URL: https://outclaw.xyz/answers/{item['category']}/{item['slug']}.html\n"
        content += "\n---\n\n"
        
    llms_full_path = os.path.join(WORKSPACE_DIR, "llms-full.txt")
    with open(llms_full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Generated llms-full.txt")

def update_root_configs():
    # 1. Update robots.txt
    robots_path = os.path.join(WORKSPACE_DIR, "robots.txt")
    if os.path.exists(robots_path):
        robots_content = """# General
User-agent: *
Allow: /
Allow: /answers/

# Google
User-agent: Googlebot
Allow: /
Allow: /answers/

# AI answer engines
User-agent: GPTBot
Allow: /answers/

User-agent: PerplexityBot
Allow: /answers/

User-agent: ClaudeBot
Allow: /answers/

User-agent: anthropic-ai
Allow: /answers/

User-agent: Bytespider
Allow: /answers/

User-agent: cohere-ai
Allow: /answers/

Sitemap: https://outclaw.xyz/sitemap.xml
"""
        with open(robots_path, "w", encoding="utf-8") as f:
            f.write(robots_content)
        print("Updated robots.txt")

    # 2. Update llms.txt
    llms_path = os.path.join(WORKSPACE_DIR, "llms.txt")
    if os.path.exists(llms_path):
        with open(llms_path, "r", encoding="utf-8") as f:
            llms_content = f.read()
            
        # Check if already added
        if "## Answers for Agents" not in llms_content:
            answers_llms_section = """
## Answers for Agents
Short, specific answers to questions AI agents and developers encounter 
when building with Claude and integrating AI tools. Updated as tools change.

## Categories
- [MCP & Connectors](https://outclaw.xyz/answers/mcp-connectors/) — Connecting Claude to Gmail, Notion, GitHub, Slack via MCP
- [Claude API](https://outclaw.xyz/answers/claude-api/) — Rate limits, models, auth, streaming, error codes
- [Tool Use & Function Calling](https://outclaw.xyz/answers/tool-use/) — Schemas, parallel calls, result handling
- [Agent Frameworks](https://outclaw.xyz/answers/agent-frameworks/) — LangGraph, CrewAI, AutoGen, Claude SDK
- [Claude Code](https://outclaw.xyz/answers/claude-code/) — CLI setup, MCP config, slash commands, CI mode
"""
            # Inject before Content Pillars or at the end
            if "## Content Pillars" in llms_content:
                llms_content = llms_content.replace("## Content Pillars", answers_llms_section + "\n## Content Pillars")
            else:
                llms_content += "\n" + answers_llms_section
                
            with open(llms_path, "w", encoding="utf-8") as f:
                f.write(llms_content)
            print("Updated llms.txt")

    # 3. Update sitemap.xml index
    sitemap_index_path = os.path.join(WORKSPACE_DIR, "sitemap.xml")
    if os.path.exists(sitemap_index_path):
        with open(sitemap_index_path, "r", encoding="utf-8") as f:
            sitemap_content = f.read()
            
        if "sitemap-answers.xml" not in sitemap_content and "answers/sitemap.xml" not in sitemap_content:
            new_sitemap_block = f"""   <sitemap>
      <loc>https://outclaw.xyz/answers/sitemap.xml</loc>
      <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
   </sitemap>
</sitemapindex>"""
            sitemap_content = sitemap_content.replace("</sitemapindex>", new_sitemap_block)
            with open(sitemap_index_path, "w", encoding="utf-8") as f:
                f.write(sitemap_content)
            print("Updated root sitemap.xml index")

def main():
    print("Starting Answers compilation...")
    create_dirs()
    generate_individual_pages()
    generate_category_pages()
    generate_master_page()
    generate_answers_sitemap()
    generate_llms_full()
    update_root_configs()
    print("Compilation completed successfully!")

if __name__ == "__main__":
    main()
