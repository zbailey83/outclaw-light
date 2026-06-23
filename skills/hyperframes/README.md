# HyperFrames Video Production Skill

**For:** Claude Code · Cursor · Antigravity  
**Version:** 1.0  
**Category:** Programmatic Video · Web Animations · AI Automation

---

## What This Skill Does

Teaches your AI agent (or assists developers in) building, styling, animating, and rendering high-quality videos using **HyperFrames**—the open-source framework by HeyGen that treats HTML, CSS, and JS as video code.

Covers the full video production stack:

| Concept / Tool | What It Does |
|---|---|
| **Root Composition** | The `index.html` file containing timelines and clips |
| **Data Attributes** | `data-start`, `data-duration`, `data-track-index` to sequence timelines |
| **GSAP & CSS** | Industry-standard animation engines for deterministic motion |
| **Sub-Compositions** | Decoupled, reusable HTML pages loaded dynamically |
| **Deterministic MP4** | Frame-by-frame browser rendering to pixel-perfect video |
| **TTS & Media Preprocessing** | Synthesizing voices and scripting via ElevenLabs and Whispers |

---

## When To Use This Skill

**Use it when you're:**
- Creating a product launch or promo video (e.g., website-to-video reels)
- Writing kinetic typography, text highlights, or lower-thirds
- Building data-visualizations, animated charts, or slideshows
- Generating automated voiceovers with synthesized narration
- Coding audio-reactive animations or beat-synced visuals

**Trigger phrases:**
- "create a promo video"
- "render an HTML composition to video"
- "GSAP video animation timeline"
- "npx hyperframes preview" / "npx hyperframes render"
- "heygen hyperframes" / "html-to-video"

---

## Folder Structure of a HyperFrames Project

```
my-video-project/
├── index.html                  ← Root composition & timeline coordinator
├── meta.json                   ← Project metadata & defaults
├── SCRIPT.md                   ← Spoken narration script
├── STORYBOARD.md               ← Shot-by-shot visual breakdown
└── compositions/               ← Sub-composition HTML files
    ├── intro.html              ← Scene 1
    ├── features.html           ← Scene 2
    └── cta.html                ← Ending CTA Scene
```

---

## Quick Reference: CLI Commands

Install and manage your video project's environment using the HyperFrames dev loop:

```bash
# Initialize a new project from a template
npx hyperframes init my-project --example swiss-grid

# Run the local live-reload preview studio (opens in browser)
npx hyperframes preview

# Render the composition to a deterministic MP4 video
npx hyperframes render --output promo.mp4

# Check system dependencies (FFmpeg, Chrome, Node.js)
npx hyperframes doctor
```

---

## Minimal Composition Example (`index.html`)

A basic skeleton of a HyperFrames root composition file:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Promo Video</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body, html {
        margin: 0; padding: 0;
        width: 1920px; height: 1080px;
        background: #0d0d1a; overflow: hidden;
      }
      #master-root { width: 1920px; height: 1080px; position: relative; }
    </style>
  </head>
  <body>
    <div id="master-root" data-composition-id="master" data-width="1920" data-height="1080" data-start="0" data-duration="15">
      
      <!-- Sub-Composition: Scene 1 -->
      <div id="scene-intro"
           data-composition-id="intro"
           data-composition-src="compositions/intro.html"
           data-start="0"
           data-duration="5"
           data-track-index="1">
      </div>
      
      <!-- Caption overlays -->
      <div class="cap clip" data-start="0.5" data-duration="4" data-track-index="10" style="position: absolute; bottom: 80px; left: 50%; transform: translateX(-50%); font-family: sans-serif; font-size: 32px; color: white;">
        Welcome to HyperFrames.
      </div>
      
      <!-- Voiceover Narration -->
      <audio id="voiceover" src="assets/voiceover.mp3" data-start="0" data-duration="15" data-track-index="0"></audio>
      
    </div>
    
    <script>
      window.__timelines = window.__timelines || {};
      const masterTL = gsap.timeline({ paused: true });
      window.__timelines["master"] = masterTL;
    </script>
  </body>
</html>
```
