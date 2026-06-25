# Google Analytics 4 (GA4) User Journey Tracking Reference

This document outlines the GA4 instrumentation implemented on outclaw.xyz to measure user journeys, from landing on technical guides through to newsletter conversions.

---

## 1. Tag Installation & Environment Config

- **Measurement ID**: Configured via the environment variable `GA4_MEASUREMENT_ID` in the local `.env` file (see template in `.env.example`).
- **sitewide Injection**: The dynamic injection script `inject_ga4.py` parses `.env` and updates all HTML pages in the codebase.
- **Local Dev Mocking**: 
  - To prevent local test data from skewing production metrics, analytics only load when the hostname is exactly `outclaw.xyz`.
  - When running locally (e.g. `localhost` or `127.0.0.1`), a mock logger fires in the console to allow local testing and verification.

---

## 2. Event Reference & Param Mapping

The following custom events are dispatched using the standard `gtag('event', ...)` helper:

### A. `article_view`
Fires automatically on load for any individual guide page.
- **Event Name**: `article_view`
- **Parameters**:
  - `article_slug` (string) — The basename of the guide file (e.g., `openmontage-chad-ai-video-editing`).
  - `article_category` (string) — The category parsed from `.eyebrow` or the first `.tag-chip` (e.g., `Model Benchmarks`, `Workflows`).

### B. `scroll_depth`
Fires when a reader scrolls to specific depths on guide pages.
- **Event Name**: `scroll_depth`
- **Parameters**:
  - `article_slug` (string) — Basename of the guide.
  - `depth_percent` (integer) — Triggers exactly once per page load at `50` and `90` percent.

### C. `cta_click`
Fires when any newsletter signup link, button, or input receives a click.
- **Event Name**: `cta_click`
- **Parameters**:
  - `cta_location` (string) — Resolved dynamically based on DOM hierarchy:
    - `"nav"` — Click occurred in the navigation header or responsive drawer.
    - `"footer"` — Click occurred in the site footer.
    - `"inline"` — Click occurred in the body CTA banners or other page cards.
  - `article_slug` (string) — Basename of the guide if clicked on an article page, otherwise `"none"`.

### D. `newsletter_signup`
Fires only on confirmed, successful subscription attempts (not just button clicks).
- **Event Name**: `newsletter_signup`
- **Parameters**:
  - `method` (string) — The form type used to complete the signup:
    - `"beehiiv_redirect"` — User submitted a standard form targeting Beehiiv with `method="get" target="_blank"`.
    - `"cta_banner_form"` — User submitted the inline AJAX form at the bottom of a guide page, successfully passing client-side validation checks.
  - `article_slug` (string) — Basename of the guide if clicked on an article page, otherwise `"none"`.

---

## 3. GA4 Admin Actions Checklist (Required)

> [!IMPORTANT]
> Mark these custom events as conversions inside the GA4 User Interface, as this cannot be configured from code.

- [ ] **Step 1**: Log in to [Google Analytics](https://analytics.google.com/).
- [ ] **Step 2**: Navigate to **Admin** (bottom left gear icon) -> **Property settings** -> **Data display** -> **Custom definitions**.
- [ ] **Step 3**: Click **Create custom dimensions** to register the custom parameters:
  - Register `article_slug` (Scope: Event).
  - Register `article_category` (Scope: Event).
  - Register `cta_location` (Scope: Event).
  - Register `depth_percent` (Scope: Event).
- [ ] **Step 4**: Navigate to **Conversions** (in the Admin panel).
- [ ] **Step 5**: Click **New conversion event** and add:
  - `cta_click`
  - `newsletter_signup`
- [ ] **Step 6**: Ensure the status toggles are switched to **Active**.

---

## 4. How to Verify Locally

1. Open any guide page locally (e.g. `guides/openmontage-chad-ai-video-editing.html`).
2. Open browser Developer Tools (F12) and inspect the **Console** tab.
3. You will see initial logs confirming mock mode:
   - `GA4 Analytics: Local development environment detected. Mocking script load.`
   - `GA4 Tracking: Tracked article_view: openmontage-chad-ai-video-editing [Category]`
4. Scroll down to the middle of the article and observe:
   - `GA4 Tracking: Tracked scroll_depth 50%`
5. Scroll to the bottom of the article and observe:
   - `GA4 Tracking: Tracked scroll_depth 90%`
6. Click the navbar CTA "Subscribe Free →" or footer newsletter link, and observe:
   - `GA4 Tracking: Tracked cta_click at location: nav` (or `footer`).
7. Enter a valid email (e.g. `test@example.com`) in the bottom banner input and click "Get the playbook →". Upon successful validation and green banner state, observe:
   - `GA4 Tracking: Tracked newsletter_signup (cta banner success)`
