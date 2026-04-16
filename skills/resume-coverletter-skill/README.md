# 📄 Resume, Cover Letter & Application Pages

> **Skill path:** `/mnt/skills/user/resume-coverletter/SKILL.md`

Produces three production-grade job application deliverables: an ATS-optimized resume, a sharp cover letter, and a dark-theme HTML application page with Skill Map — all mapped directly to the actual role requirements.

> **Rule #1:** Read the job description carefully. Everything — every bullet, every skill card, every table row — must map back to the actual role requirements.

---

## When This Skill Triggers

| Keyword / Request | Example |
|---|---|
| Writing or improving a resume / CV | "rewrite my resume for this role" |
| Drafting a cover letter | "write a cover letter for this job posting" |
| Applying for a job | "help me apply for this position" |
| ATS optimization | "make my resume ATS-friendly" |
| HTML application / portfolio page | "make me an HTML application page" |
| Skill map page | "build a skill map for this JD" |
| Resume bullet rewrites | "improve these resume bullets" |
| Tailoring to a specific JD | "tailor my resume to this job description" |

---

## The Three Deliverables

### 1. Cover Letter
Plain text / PDF-ready. 250–350 words. One page.

**Structure:**
1. **Hook** — Specific, factual, tied to the role. Show you read the JD.
2. **Proof paragraph** — 2–3 sentences. Concrete accomplishments with numbers.
3. **Fit statement** — Why this company/role specifically. One sentence.
4. **Close + CTA** — Clean, direct. One sentence max.

### 2. Resume / CV
ATS-safe structured text. No tables, headers/footers for contact info, or images.

**Section order:** Contact → Summary → Portfolio/Projects → Experience → Skills → Education

**Bullet formula:** `[Verb] + [what] + [how/tool] + [outcome/scale]`

```
✅  Built and shipped 16 technical products with complete setup documentation, generating 300+ downloads.
❌  Responsible for product documentation and distribution.
```

**Length:** 1 page (under 7 years experience) · 2 pages (senior). No fluff to fill space.

### 3. HTML Application Page
A polished, dark-theme, single-file application site. The high-value differentiator — especially for creative, tech, and content roles.

---

## Step-by-Step Workflow

### Step 1 — Gather Inputs
Before writing anything, confirm you have:
- [ ] Applicant's current resume / CV text (or uploaded PDF)
- [ ] Target job description (paste or summarize)
- [ ] Company name and role title
- [ ] Applicant's location and remote / in-office notes
- [ ] Portfolio URLs (personal site, GitHub, Gumroad, etc.)
- [ ] Contact info (email, LinkedIn)

> If any are missing, ask before writing.

### Step 2 — Extract & Map Keywords
Scan the JD for:
- **Hard requirements** — tools, platforms, deliverable types
- **Soft signals** — tone words, team culture cues ("fast-moving," "cross-functional")
- **Verbs they use** — mirror these back. If they say "maintain," write "maintain," not "manage"

### Step 3 — Write the Cover Letter
Follow the structure above. Apply the rules below. 250–350 words.

### Step 4 — Write the Resume
Apply bullet formula to every experience entry. Quantify everything possible. Keep it ATS-safe.

**Summary block:** 2–3 lines. What you are, years of experience, 2–3 clearest proof points. End with what you bring to this type of role.

### Step 5 — Build the HTML Application Page
Single `.html` file. No external CSS or JS. All inline. See design spec below.

---

## Writing Rules (Non-Negotiable)

### Banned Openers
| ❌ Never | ✅ Instead |
|---|---|
| "I am writing to express my interest in…" | Start with a fact or a claim |
| "I would like to highlight that…" | Say the thing directly |

### Banned Words
| ❌ Never | ✅ Instead |
|---|---|
| Synergy, orchestrate, spearhead | Led, built, shipped |
| Empower, impactful | Cut to what actually happened |
| Utilize | Use |
| Facilitate, assist, support, manage | Specific action verb |
| "Responsible for" | Start with the verb |
| "Helped with" | What did you actually do? |

### Banned Patterns
- Nominalizations: "the optimization of" → "optimized"
- Adverbs: find a stronger verb instead
- Passive voice: active voice only
- "In order to" → "to"

---

## HTML Application Page — Design Spec

### Design Tokens
```css
--green:       #C8F100       /* accent, highlights, dots, borders */
--green-dark:  #b0d400
--green-glow:  rgba(200,241,0,0.12)
--black:       #0A0A0A       /* page background */
--off-black:   #111111
--card:        #161616       /* card backgrounds */
--border:      rgba(255,255,255,0.07)
--border-green: rgba(200,241,0,0.3)
--text:        #F5F5F5
--muted:       #888
```

**Fonts:** DM Serif Display (headings, italic accent) + DM Sans (body) — loaded from Google Fonts.

### Page Sections (in order)

| Section | Contents |
|---|---|
| **1. Header** | Animated tag pill · Name (DM Serif Display) · Subtitle · Location/availability pills · Social links row |
| **2. Pitch / Why I'm a Fit** | Green-bordered card · 2–3 sentences · Direct · No hedging · Names a specific project or output |
| **3. Alignment Table** | Left: verbatim JD requirement · Right: applicant's specific proof. Every major JD requirement mapped. |
| **4. Portfolio Accordion** | "Strongest match" (green badge) and supplemental cards. Expand/collapse. Green border on top matches. |
| **5. Skills Grid** | 3-column grid · 12–16 cards · Each card: green dot + bold skill + 1–2 sentence proof from actual work. Skills drawn from JD only. |
| **6. CTA Footer** | "Let's talk." · Location/availability · Green "Get in touch" button → mailto link |

### Technical Requirements
- Single `.html` file — no external CSS or JS files
- Fonts loaded via Google Fonts `<link>`
- `fadeUp` keyframe animation on sections (staggered `animation-delay`)
- `pulse` keyframe on the header tag green dot
- Grid noise texture on body via `::before` pseudo-element
- Accordion JS inline in `<script>` tag — toggle `maxHeight` for smooth expand/collapse
- Mobile-responsive: `clamp()` on font sizes, `flex-wrap` on social rows, responsive grid

---

## Pre-Delivery Checklist

- [ ] Cover letter opens with a fact/claim, not "I am writing to…"
- [ ] No banned words: synergy, orchestrate, spearhead, empower, impactful, utilize, facilitate
- [ ] Every resume bullet starts with an action verb and includes a number or scale indicator
- [ ] HTML alignment table maps every major JD requirement
- [ ] Skill cards in the HTML are drawn from JD requirements, not a generic list
- [ ] Social links in HTML are correct for this applicant
- [ ] File saved to `/mnt/user-data/outputs/` and presented to user

---

## Output File Naming

```
[Name]_CoverLetter_[Company].txt   — for copy/paste/print
[Name]_Resume_[Company].txt        — for copy/paste/ATS upload
[Name]_ApplicationPage_[Company].html  — the polished HTML page
```

> If the user only asks for one deliverable, produce that one — but always offer the others.

---

## Reference Files

| File | Contents |
|---|---|
| `references/cover-letter-examples.md` | Role-type hooks and CTAs by industry |
| `references/resume-bullets.md` | Before/after bullet rewrites by role type |
| `references/html-component-library.md` | Complete, copy-pasteable CSS blocks and HTML patterns |

---

*Trigger keywords: resume · CV · cover letter · job application · ATS · HTML portfolio page · skill map · application landing page · bullet rewrites · tailor to JD*
