---
name: resume-coverletter
description: "Use this skill for ALL resume, CV, cover letter, and job application page creation and optimization. Trigger aggressively whenever the user mentions writing or improving a resume/CV, drafting a cover letter, applying for a job, creating a portfolio HTML page, a skill map page, or an application landing page. Also trigger for resume rewrites, bullet point improvements, ATS optimization, tailoring applications to specific job descriptions, or building any visual job-application artifact (HTML skill pages, portfolio pages, application microsites). If the user says anything like 'help me apply for a job', 'update my resume', 'write a cover letter', 'make an HTML resume page', 'create a skill map', or uploads a resume/cover letter PDF/HTML — use this skill immediately."
---

# Resume, Cover Letter & Application Page Skill

This skill produces three deliverables for job applications:
1. **Cover Letter** (plain text / PDF-ready)
2. **Resume / CV** (structured text or PDF-ready)
3. **HTML Application Page** — a polished, dark-theme single-page application site with a Skill Map section

Always read the job description carefully. Everything — every bullet, every skill card, every table row — must map back to the actual role requirements.

---

## Step 1 — Gather Inputs

Before writing anything, confirm you have:

- [ ] Applicant's current resume/CV text (or uploaded PDF)
- [ ] Target job description (paste or summarize if not provided)
- [ ] Company name and role title
- [ ] Applicant's location and any in-office / remote notes
- [ ] Portfolio URLs (personal site, GitHub, Gumroad, newsletters, etc.)
- [ ] Contact info (email, LinkedIn, etc.)

If any are missing, ask before writing.

---

## Step 2 — Extract and Map Keywords

Scan the job description for:
- **Hard requirements**: tools, platforms, deliverable types (SOPs, KBs, how-to guides, etc.)
- **Soft signals**: tone words, team culture cues ("fast-moving," "cross-functional," "operational")
- **Verbs they use**: mirror these back in bullets (if they say "maintain," you write "maintain," not "manage")

Build a mental keyword list. Every section of every deliverable should reflect these naturally — not stuffed.

---

## Step 3 — Write the Cover Letter

**Rules (non-negotiable):**
- No "I am writing to express my interest in…" openers. Start with a fact or a claim.
- No nominalizations ("the optimization of" → "optimized")
- No weak verbs: provide, facilitate, assist, support, manage — replace with specific actions
- No "in order to" — use "to"
- No adverbs. Find a stronger verb instead.
- Active voice only
- No resume tropes: synergy, orchestrate, spearhead, empower, impactful — use led, built, wrote, fixed
- No self-referential commentary ("I would like to highlight that…")
- Replace "utilize" with "use"

**Structure:**
1. **Hook (1–2 sentences)**: Specific, factual, tied to the role. Show you read the JD.
2. **Proof paragraph**: 2–3 sentences. One or two concrete accomplishments with numbers where possible.
3. **Fit statement**: Why this company / role specifically. One sentence is enough.
4. **Close + CTA**: Clean, direct. No excessive thank-yous. One sentence max.

**Length**: One page. Aim for 250–350 words.

See → `references/cover-letter-examples.md` for role-type hooks and CTAs.

---

## Step 4 — Write the Resume / CV

**Rules:**
- Every bullet starts with a strong past-tense verb (Built, Led, Wrote, Designed, Reduced, Grew, Shipped)
- Every bullet quantifies where possible (numbers, %, volume, time saved)
- No "Responsible for" or "Helped with"
- No nominalizations
- ATS-safe: no tables, no headers/footers for contact info, no images in the text resume version
- Standard sections in order: Contact → Summary → Portfolio/Projects → Experience → Skills → Education

**Summary block**: 2–3 lines. What you are, how many years, the 2–3 clearest proof points. End with what you bring to this type of role.

**Bullet formula**: `[Verb] + [what] + [how/tool] + [outcome/scale]`
- ✅ "Built and shipped 16 technical products, each with complete setup documentation, generating 300+ downloads."
- ❌ "Responsible for product documentation and distribution."

**Length**: 1 page for under 7 years experience; 2 pages for senior. No fluff to fill space.

See → `references/resume-bullets.md` for before/after bullet rewrites by role type.

---

## Step 5 — Build the HTML Application Page

This is the high-value differentiator. Build a dark-theme, single-page HTML application site.

**When to build it**: Whenever the user asks for an "HTML resume," "skill map page," "application page," or "portfolio page." Also offer it proactively when they're applying to a creative, tech, or content role where standing out visually matters.

### Design Spec

```
Design tokens:
  --green: #C8F100          (accent, highlights, dots, borders)
  --green-dark: #b0d400
  --green-glow: rgba(200,241,0,0.12)
  --black: #0A0A0A          (page background)
  --off-black: #111111
  --card: #161616           (card backgrounds)
  --border: rgba(255,255,255,0.07)
  --border-green: rgba(200,241,0,0.3)
  --text: #F5F5F5
  --muted: #888
  --muted2: #555

Fonts: DM Serif Display (headings, italic accent) + DM Sans (body)
Import from Google Fonts.
```

### Page Sections (in order)

**1. Header**
- Animated tag pill: `● APPLYING FOR [ROLE TITLE]` in green
- Name in DM Serif Display, large, with key word in `<em>` (renders green/italic)
- 1-line subtitle (muted, 300 weight)
- Meta pills: location, availability
- Social link row: LinkedIn, X/Twitter, personal site, GitHub, etc. — icon + label, pill style

**2. Pitch / Why I'm a Fit**
- Section label with line rule: `WHY I'M A FIT ————————`
- Green-bordered card with 2–3 sentences. Direct. No hedging. Names the specific project or output.

**3. Alignment Table — "What the Role Needs · What I Bring"**
- Two-column table: left = verbatim or near-verbatim JD requirement, right = specific applicant proof
- Left column slightly muted, right column full text weight
- Green accent on left column header
- Map every major JD requirement to a specific project or output

**4. Portfolio (Accordion Cards)**
- Two tiers: "Strongest match" (green badge) and "Supplemental" / thematic label (muted badge)
- Each card: title row with chevron toggle, expand/collapse body with description + link
- "Strongest match" cards use green border accent; others use standard border

**5. Skills Grid — "Skills Mapped to the Role"**
- 3-column responsive CSS grid
- Each card: green dot + bold skill name + 1–2 sentence proof from actual work
- Skills must come from the JD — no generic skill lists
- 12–16 cards, each tied to a specific JD bullet or requirement

**6. CTA Footer**
- "Let's talk." heading
- Location / availability line
- Green button: "Get in touch" → mailto link

### HTML Technical Requirements
- Single `.html` file, no external CSS or JS files
- All fonts loaded via Google Fonts `<link>`
- `fadeUp` keyframe animation on sections (staggered with `animation-delay`)
- `pulse` keyframe on the header tag green dot
- Grid noise texture on body via `::before` pseudo-element (subtle, low-opacity)
- Accordion JS inline in `<script>` tag at bottom — toggle `maxHeight` for smooth expand/collapse
- Mobile-responsive: `clamp()` on font sizes, `flex-wrap` on social rows, responsive grid

### Section Label Pattern
```html
<div class="section-label">Section Title</div>
```
Use `::after` pseudo-element for the line rule. All caps, 11px, letter-spacing 0.13em, color #666.

See → `references/html-component-library.md` for complete, copy-pasteable CSS blocks and HTML patterns.

---

## Deliverable Checklist

Before handing off, verify:

- [ ] Cover letter opens with a fact/claim, not "I am writing to…"
- [ ] No banned words: synergy, orchestrate, spearhead, empower, impactful, utilize, facilitate
- [ ] Every resume bullet starts with an action verb and includes a number or scale indicator
- [ ] HTML alignment table maps every major JD requirement
- [ ] Skill cards in the HTML are drawn from JD requirements, not from a generic list
- [ ] Social links in HTML are correct for this applicant
- [ ] File saved to `/mnt/user-data/outputs/` and presented to user

---

## Output Files

Always produce:
- `[Name]_CoverLetter_[Company].txt` (or `.md`) — for copy/paste/print
- `[Name]_Resume_[Company].txt` (or `.md`) — for copy/paste/ATS upload
- `[Name]_ApplicationPage_[Company].html` — the polished HTML page

If the user only asks for one of these, produce that one. But always offer the others.
