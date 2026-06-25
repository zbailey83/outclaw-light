import os
import re

workspace_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Read Measurement ID from environment or .env file
measurement_id = None
env_path = os.path.join(workspace_dir, ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("GA4_MEASUREMENT_ID="):
                measurement_id = line.strip().split("=")[1].strip().strip('"').strip("'")
                break

if not measurement_id:
    measurement_id = os.environ.get("GA4_MEASUREMENT_ID")

if not measurement_id:
    measurement_id = "G-JHMN90H7MC" # Fallback to standard measurements ID

print(f"Using GA4 Measurement ID: {measurement_id}")

def get_relative_root(file_path, base_dir):
    rel = os.path.relpath(os.path.dirname(file_path), base_dir)
    if rel == ".":
        return "./"
    depth = len(rel.split(os.sep))
    return "../" * depth

# 2. Walk workspace and update HTML files
for root, dirs, files in os.walk(workspace_dir):
    # Exclude system and deployment directories
    dirs[:] = [d for d in dirs if d not in (".git", ".netlify", ".agents", "outclaw-promo", "temp-launches")]
    
    for name in files:
        if name.endswith(".html"):
            path = os.path.join(root, name)
            
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            original_content = content
            
            # Idempotently remove existing GA4 configurations
            content = re.sub(
                r'<!-- Google tag \(gtag\.js\) -->\s*<script[^>]*?src="[^"]*?googletagmanager\.com/gtag/js.*?/script>\s*<script[^>]*?>.*?</script>',
                '',
                content,
                flags=re.DOTALL | re.IGNORECASE
            )
            content = re.sub(
                r'<!-- GA4 User Journey Tag -->\s*<script[^>]*?>.*?</script>',
                '',
                content,
                flags=re.DOTALL | re.IGNORECASE
            )
            content = re.sub(
                r'<script[^>]*?src="[^"]*?analytics-journey\.js"[^>]*?>\s*</script>',
                '',
                content,
                flags=re.IGNORECASE
            )
            
            # Compute relative path to analytics-journey.js
            rel_path = get_relative_root(path, workspace_dir)
            
            # Construct GA4 tag and tracking script tag
            ga4_snippet = f"""<!-- GA4 User Journey Tag -->
<script>
  window.GA4_MEASUREMENT_ID = "{measurement_id}";
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  if (window.location.hostname !== 'outclaw.xyz') {{
    console.log('GA4 Analytics: Local development environment detected. Mocking script load.');
    gtag('config', window.GA4_MEASUREMENT_ID, {{ 'debug_mode': true }});
  }} else {{
    (function() {{
      var script = document.createElement('script');
      script.async = true;
      script.src = 'https://www.googletagmanager.com/gtag/js?id=' + window.GA4_MEASUREMENT_ID;
      document.head.appendChild(script);
    }})();
    gtag('config', window.GA4_MEASUREMENT_ID);
  }}
</script>
<script src="{rel_path}analytics-journey.js" defer></script>"""

            # Inject right inside the <head> block
            if "<head>" in content:
                content = content.replace("<head>", f"<head>\n{ga4_snippet}")
            elif "<HEAD>" in content:
                content = content.replace("<HEAD>", f"<HEAD>\n{ga4_snippet}")
            
            if content != original_content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Successfully injected GA4 Journey Analytics into: {os.path.relpath(path, workspace_dir)}")

print("GA4 user journey script injection completed.")
