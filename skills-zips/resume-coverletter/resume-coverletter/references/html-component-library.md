# HTML Application Page — Component Library

Complete, copy-pasteable CSS and HTML for the dark-theme application page.

## Table of Contents
1. [Base CSS Reset + Design Tokens](#base)
2. [Header Section](#header)
3. [Section Labels](#section-labels)
4. [Pitch Box](#pitch-box)
5. [Alignment Table](#alignment-table)
6. [Portfolio Accordion Cards](#portfolio-cards)
7. [Skills Grid](#skills-grid)
8. [CTA Footer](#cta-footer)
9. [Animations](#animations)
10. [Accordion JavaScript](#javascript)
11. [Full Page Template](#full-template)

---

## 1. Base CSS Reset + Design Tokens {#base}

```css
:root {
  --green: #C8F100;
  --green-dark: #b0d400;
  --green-glow: rgba(200,241,0,0.12);
  --black: #0A0A0A;
  --off-black: #111111;
  --card: #161616;
  --border: rgba(255,255,255,0.07);
  --border-green: rgba(200,241,0,0.3);
  --text: #F5F5F5;
  --muted: #888;
  --muted2: #555;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }

body {
  background: var(--black);
  color: var(--text);
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

/* Grid noise texture */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0,200,5,0.08) 0%, transparent 60%),
    url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h1v1H0zM20 20h1v1h-1z' fill='%23ffffff' fill-opacity='0.015'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 0;
}

.page {
  position: relative;
  z-index: 1;
  max-width: 900px;
  margin: 0 auto;
  padding: 0 24px 80px;
}
```

---

## 2. Header Section {#header}

```css
header {
  padding: 60px 0 48px;
  border-bottom: 1px solid var(--border);
  animation: fadeUp 0.6s ease both;
}

.header-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--green-glow);
  border: 1px solid var(--border-green);
  color: var(--green);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 5px 12px;
  border-radius: 100px;
  margin-bottom: 20px;
}

.header-tag::before {
  content: '';
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--green);
  animation: pulse 2s ease infinite;
}

h1 {
  font-family: 'DM Serif Display', serif;
  font-size: clamp(2.6rem, 6vw, 3.8rem);
  line-height: 1.05;
  letter-spacing: -0.02em;
  color: var(--text);
  margin-bottom: 20px;
}

h1 em {
  color: var(--green);
  font-style: italic;
}

.header-sub {
  font-size: 16px;
  color: var(--muted);
  max-width: 560px;
  line-height: 1.7;
  font-weight: 300;
  margin-bottom: 28px;
}

.meta-pill {
  font-size: 12px;
  font-weight: 500;
  color: var(--muted);
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  padding: 4px 12px;
  border-radius: 100px;
}

.header-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.social-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin-top: 16px;
}

.social-link {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  color: var(--muted);
  font-size: 11.5px;
  font-weight: 500;
  padding: 6px 13px;
  border-radius: 100px;
  text-decoration: none;
  transition: border-color 0.2s, color 0.2s, background 0.2s;
  white-space: nowrap;
}

.social-link:hover {
  border-color: var(--border-green);
  color: var(--text);
  background: rgba(0,200,5,0.06);
}

.social-link svg {
  width: 13px; height: 13px;
  flex-shrink: 0;
  opacity: 0.7;
}

.social-link:hover svg { opacity: 1; }
```

```html
<header>
  <div class="header-tag">Applying for [ROLE TITLE]</div>
  <h1>[First Name] <em>[Last Name]</em></h1>
  <p class="header-sub">[One-line tagline, 300 weight, muted — what you are + what you bring]</p>
  <div class="header-meta">
    <span class="meta-pill">📍 [City, State]</span>
    <span class="meta-pill">[Availability note, e.g. In-office 3+ days/week]</span>
  </div>
  <div class="social-row">
    <a class="social-link" href="[URL]" target="_blank">
      [SVG ICON] [Label]
    </a>
    <!-- Repeat for each social/portfolio link -->
  </div>
</header>
```

---

## 3. Section Labels {#section-labels}

```css
section {
  padding: 48px 0 0;
  animation: fadeUp 0.6s ease both;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: #666;
  margin-bottom: 26px;
}

.section-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}
```

```html
<div class="section-label">Section Title</div>
```

---

## 4. Pitch Box {#pitch-box}

```css
.pitch-box {
  background: linear-gradient(135deg, rgba(0,200,5,0.06) 0%, rgba(0,200,5,0.02) 100%);
  border: 1px solid var(--border-green);
  border-radius: 12px;
  padding: 28px 32px;
}

.pitch-box p {
  color: var(--text);
  font-size: 15px;
  line-height: 1.8;
}

.pitch-box strong {
  color: var(--green);
  font-weight: 600;
}
```

```html
<section>
  <div class="section-label">Why I'm a fit</div>
  <div class="pitch-box">
    <p>
      [2–3 sentences. Specific. Names the actual projects/outputs. No hedging.
      Bold the 1–2 strongest proof points in <strong>green</strong>.]
    </p>
  </div>
</section>
```

---

## 5. Alignment Table {#alignment-table}

```css
.align-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13.5px;
}

.align-table thead tr {
  border-bottom: 1px solid var(--border-green);
}

.align-table th {
  text-align: left;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted2);
  padding: 0 16px 14px 0;
}

.align-table th:first-child { color: var(--green); }

.align-table td {
  padding: 14px 16px 14px 0;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
  line-height: 1.6;
}

.align-table td:first-child {
  color: var(--muted);
  width: 38%;
  padding-right: 24px;
}

.align-table td:last-child {
  color: var(--text);
}
```

```html
<section>
  <div class="section-label">What the role needs · What I bring</div>
  <table class="align-table">
    <thead>
      <tr>
        <th>[Company] requires</th>
        <th>My experience</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>[Verbatim or near-verbatim JD requirement]</td>
        <td>[Specific proof: project name, output, outcome]</td>
      </tr>
      <!-- Repeat for each major JD requirement -->
    </tbody>
  </table>
</section>
```

---

## 6. Portfolio Accordion Cards {#portfolio-cards}

```css
.accordion-wrap { }

.section-group-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: #444;
  margin-bottom: 12px;
  margin-top: 4px;
}

.portfolio-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 8px;
}

.pcard {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
  transition: border-color 0.2s;
}

.pcard:hover, .pcard.open { border-color: rgba(255,255,255,0.13); }

.pcard.primary { border-color: var(--border-green); }
.pcard.primary:hover, .pcard.primary.open { border-color: rgba(200,241,0,0.5); }

.pcard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  gap: 12px;
}

.pcard-header-left { flex: 1; min-width: 0; }

.pcard-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.pcard-header-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.portfolio-badge {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 100px;
  white-space: nowrap;
}

.badge-primary {
  background: var(--green-glow);
  border: 1px solid var(--border-green);
  color: var(--green);
}

.badge-secondary {
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  color: var(--muted);
}

.pcard-chevron {
  width: 16px; height: 16px;
  color: var(--muted2);
  flex-shrink: 0;
  transition: transform 0.25s ease;
}

.pcard.open .pcard-chevron { transform: rotate(180deg); }

.pcard-body {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.pcard-body.open { }

.pcard-inner {
  padding: 0 20px 20px;
  border-top: 1px solid var(--border);
}

.pcard-desc {
  font-size: 13.5px;
  color: var(--muted);
  line-height: 1.75;
  padding-top: 16px;
  padding-bottom: 14px;
}

.portfolio-link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--green);
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
  letter-spacing: 0.03em;
}

.portfolio-link:hover { text-decoration: underline; }
.portfolio-link svg { width: 9px; height: 9px; }
```

```html
<section>
  <div class="accordion-wrap">
    <div class="section-group-label">Portfolio</div>
    <div class="portfolio-list">

      <div class="pcard primary" id="card-[id]">
        <div class="pcard-header" onclick="toggleCard('[id]')">
          <div class="pcard-header-left">
            <div class="pcard-title">[Project Name — Subtitle]</div>
          </div>
          <div class="pcard-header-right">
            <span class="portfolio-badge badge-primary">Strongest match</span>
            <svg class="pcard-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
        </div>
        <div class="pcard-body" id="body-[id]">
          <div class="pcard-inner">
            <div class="pcard-desc">[2–3 sentence description. Specific. What it is, what it demonstrates, why it's relevant.]</div>
            <a class="portfolio-link" href="[URL]" target="_blank">
              [display URL]
              <svg viewBox="0 0 10 10" fill="none"><path d="M1 9L9 1M9 1H3M9 1V7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
            </a>
          </div>
        </div>
      </div>

    </div>
  </div>
</section>
```

---

## 7. Skills Grid {#skills-grid}

```css
.skills-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

@media (max-width: 680px) {
  .skills-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 400px) {
  .skills-grid { grid-template-columns: 1fr; }
}

.skill-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 18px;
  transition: border-color 0.2s;
}

.skill-card:hover { border-color: var(--border-green); }

.dot {
  display: inline-block;
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--green);
  margin-right: 8px;
  flex-shrink: 0;
  vertical-align: middle;
  position: relative;
  top: -1px;
}

.skill-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 0;
}

.skill-desc {
  font-size: 12.5px;
  color: var(--muted);
  line-height: 1.65;
}
```

```html
<section>
  <div class="section-label">Skills mapped to the role</div>
  <div class="skills-grid">
    <div class="skill-card">
      <div class="skill-name"><span class="dot"></span>[Skill Name from JD]</div>
      <div class="skill-desc">[1–2 sentences. Proof from actual work. Specific, not generic.]</div>
    </div>
    <!-- Repeat 12–16 times -->
  </div>
</section>
```

---

## 8. CTA Footer {#cta-footer}

```css
.cta-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 64px;
  padding: 36px 40px;
  background: linear-gradient(135deg, rgba(0,200,5,0.05) 0%, rgba(0,200,5,0.02) 100%);
  border: 1px solid var(--border-green);
  border-radius: 16px;
}

.cta-text h3 {
  font-family: 'DM Serif Display', serif;
  font-size: 2rem;
  color: var(--text);
  line-height: 1.1;
  margin-bottom: 6px;
}

.cta-text p {
  font-size: 13px;
  color: var(--muted);
}

.cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--green);
  color: #000;
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 0.03em;
  padding: 12px 24px;
  border-radius: 100px;
  text-decoration: none;
  transition: background 0.2s, transform 0.15s;
  white-space: nowrap;
}

.cta-btn:hover {
  background: var(--green-dark);
  transform: translateY(-1px);
}
```

```html
<div class="cta-section">
  <div class="cta-text">
    <h3>Let's talk.</h3>
    <p>[City, State] · [Availability note]</p>
  </div>
  <a class="cta-btn" href="mailto:[email]">
    Get in touch
    <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M1 11L11 1M11 1H3M11 1V9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
    </svg>
  </a>
</div>
```

---

## 9. Animations {#animations}

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.5; transform: scale(0.85); }
}
```

Apply to sections with staggered delays:
```html
<section style="animation-delay:0.05s;">
<section style="animation-delay:0.1s;">
<section style="animation-delay:0.15s;">
```

---

## 10. Accordion JavaScript {#javascript}

```html
<script>
  function toggleCard(id) {
    const body = document.getElementById('body-' + id);
    const card = document.getElementById('card-' + id);
    const isOpen = card.classList.contains('open');

    if (isOpen) {
      body.style.maxHeight = body.scrollHeight + 'px';
      requestAnimationFrame(() => requestAnimationFrame(() => {
        body.style.maxHeight = '0';
        body.classList.remove('open');
        card.classList.remove('open');
      }));
    } else {
      card.classList.add('open');
      body.classList.add('open');
      body.style.maxHeight = body.scrollHeight + 'px';
      body.addEventListener('transitionend', function h() {
        if (card.classList.contains('open')) body.style.maxHeight = 'none';
        body.removeEventListener('transitionend', h);
      });
    }
  }
</script>
```

---

## 11. Full Page Template {#full-template}

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Role Title] — Application</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap" rel="stylesheet">
<style>
  /* ── PASTE ALL CSS FROM SECTIONS 1–9 HERE ── */
</style>
</head>
<body>
<div class="page">

  <header><!-- Section 2 --></header>

  <section style="animation-delay:0.05s;">
    <!-- Section 4: Pitch Box -->
  </section>

  <section style="animation-delay:0.1s;">
    <!-- Section 5: Alignment Table -->
  </section>

  <section style="animation-delay:0.15s;">
    <!-- Section 6: Portfolio Cards -->
  </section>

  <section style="animation-delay:0.2s;">
    <!-- Section 7: Skills Grid -->
  </section>

  <!-- Section 8: CTA Footer -->
  <div class="cta-section">...</div>

</div>
<!-- Section 10: Accordion JS -->
<script>...</script>
</body>
</html>
```
