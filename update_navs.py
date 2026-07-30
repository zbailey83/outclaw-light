import os
import re

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCLUDE_DIRS = {'.git', '.netlify', '.agents', 'outclaw-promo', 'temp-launches', 'ace-handyman', 'admin'}

# Regex patterns to locate Navbar (including mobile drawer) and Footer
NAVBAR_REGEX = re.compile(
    r'(?:<!--\s*NAVBAR\s*-->\s*)?<nav class="navbar"[^>]*>.*?</nav>(?:\s*|<!--.*?-->)*<div class="nav-drawer"[^>]*>.*?</div>',
    re.DOTALL | re.IGNORECASE
)
FOOTER_REGEX = re.compile(
    r'(?:<!--\s*FOOTER\s*-->\s*)?<footer[^>]*>.*?</footer>(?:\s*<div class="footer-bottom">.*?</div>)?',
    re.DOTALL | re.IGNORECASE
)

def get_relative_prefix(filepath):
    relpath = os.path.relpath(filepath, WORKSPACE_DIR)
    parts = relpath.split(os.sep)
    depth = len(parts) - 1
    if depth == 0:
        return ""
    else:
        return "../" * depth

def get_active_category(filepath):
    relpath = os.path.relpath(filepath, WORKSPACE_DIR)
    parts = relpath.replace('\\', '/').split('/')
    if len(parts) > 1:
        first_dir = parts[0]
        if first_dir in ['about', 'guides', 'answers', 'videos', 'tools', 'newsletter']:
            return first_dir
    return None

def build_navbar(prefix, active_cat):
    about_active = ' class="active"' if active_cat == 'about' else ''
    guides_active = ' class="active"' if active_cat == 'guides' else ''
    answers_active = ' class="active"' if active_cat == 'answers' else ''
    videos_active = ' class="active"' if active_cat == 'videos' else ''
    tools_active = ' class="active"' if active_cat == 'tools' else ''
    newsletter_active = ' class="active"' if active_cat == 'newsletter' else ''
    
    logo_path = f"{prefix}outclaw-icons/Wild-Bird-Flamingo--Streamline-Ultimate.png"
    
    navbar_html = f"""<nav class="navbar" id="mainNav">
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
    return navbar_html

def build_footer(prefix, active_cat):
    about_active = ' class="active"' if active_cat == 'about' else ''
    guides_active = ' class="active"' if active_cat == 'guides' else ''
    answers_active = ' class="active"' if active_cat == 'answers' else ''
    videos_active = ' class="active"' if active_cat == 'videos' else ''
    tools_active = ' class="active"' if active_cat == 'tools' else ''
    newsletter_active = ' class="active"' if active_cat == 'newsletter' else ''
    
    logo_path = f"{prefix}outclaw-icons/Wild-Bird-Flamingo--Streamline-Ultimate.png"
    
    footer_html = f"""<footer>
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
    return footer_html

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    rel_path = os.path.relpath(filepath, WORKSPACE_DIR)
    prefix = get_relative_prefix(filepath)
    active_cat = get_active_category(filepath)
    
    new_navbar = build_navbar(prefix, active_cat)
    new_footer = build_footer(prefix, active_cat)
    
    modified = False
    
    # Replace navbar
    if NAVBAR_REGEX.search(content):
        content = NAVBAR_REGEX.sub(new_navbar, content)
        modified = True
    
    # Replace footer
    if FOOTER_REGEX.search(content):
        content = FOOTER_REGEX.sub(new_footer, content)
        modified = True
        
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated header/footer for: {rel_path} (Depth: {len(prefix)//3}, Category: {active_cat})")
    else:
        print(f"Skipped (No navbar/footer found): {rel_path}")

def main():
    print("Scanning HTML files for header/footer updates...")
    updated_count = 0
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                # Skip answers dynamically generated pages since they are handled by build_answers.py
                # But keep answers/index.html and answers/*/index.html if we want,
                # actually build_answers.py generates those too, so skip the whole answers folder
                # to avoid overwriting dynamically managed files.
                rel_path = os.path.relpath(filepath, WORKSPACE_DIR)
                if rel_path.startswith("answers" + os.sep) or rel_path == "answers":
                    continue
                process_file(filepath)
                updated_count += 1
    print(f"Finished. Scanned and processed {updated_count} static files.")

if __name__ == "__main__":
    main()
