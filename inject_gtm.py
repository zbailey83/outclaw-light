import os

head_code = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-5VC26C47');</script>
<!-- End Google Tag Manager -->"""

body_code = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5VC26C47"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

for root, dirs, files in os.walk('.'):
    for name in files:
        if name.endswith(".html"):
            path = os.path.join(root, name)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if GTM is already there
            if "GTM-5VC26C47" in content:
                print(f"Skipping {path} - already contains GTM.")
                continue
            
            new_content = content
            # Insert in head
            if "<head>" in content:
                new_content = new_content.replace("<head>", f"<head>\n  {head_code}")
            elif "<HEAD>" in content:
                new_content = new_content.replace("<HEAD>", f"<HEAD>\n  {head_code}")
            
            # Insert in body
            if "<body>" in new_content:
                new_content = new_content.replace("<body>", f"<body>\n  {body_code}")
            elif "<body " in new_content:
                # Handle cases like <body class="...">
                idx = new_content.find("<body")
                close_bracket = new_content.find(">", idx)
                if close_bracket != -1:
                    new_content = new_content[:close_bracket+1] + f"\n  {body_code}" + new_content[close_bracket+1:]
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {path}")
