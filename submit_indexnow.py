import os
import xml.etree.ElementTree as ET
import urllib.request
import json

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
SITEMAP_INDEX = os.path.join(WORKSPACE_DIR, "sitemap.xml")
API_KEY = "20edf0faf575488db214556b12d3a27e"
HOST = "outclaw.xyz"

def get_sub_sitemaps():
    print(f"Reading sitemap index: {SITEMAP_INDEX}")
    if not os.path.exists(SITEMAP_INDEX):
        print("Sitemap index not found.")
        return []
    
    try:
        tree = ET.parse(SITEMAP_INDEX)
        root = tree.getroot()
        namespace = ""
        if root.tag.startswith("{"):
            namespace = root.tag.split("}")[0] + "}"
        
        sitemaps = []
        for sitemap in root.findall(f"{namespace}sitemap"):
            loc = sitemap.find(f"{namespace}loc")
            if loc is not None:
                sitemaps.append(loc.text)
        return sitemaps
    except Exception as e:
        print(f"Error parsing sitemap index: {e}")
        return []

def get_urls_from_sitemap(sitemap_url):
    rel_path = sitemap_url.replace("https://outclaw.xyz/", "").replace("/", os.sep)
    local_path = os.path.join(WORKSPACE_DIR, rel_path)
    
    print(f"Parsing local sitemap: {local_path}")
    if not os.path.exists(local_path):
        print(f"Sitemap file not found locally: {local_path}")
        return []
        
    try:
        tree = ET.parse(local_path)
        root = tree.getroot()
        namespace = ""
        if root.tag.startswith("{"):
            namespace = root.tag.split("}")[0] + "}"
            
        urls = []
        for url in root.findall(f"{namespace}url"):
            loc = url.find(f"{namespace}loc")
            if loc is not None:
                urls.append(loc.text)
        return urls
    except Exception as e:
        print(f"Error parsing sitemap {local_path}: {e}")
        return []

def main():
    sub_sitemaps = get_sub_sitemaps()
    all_urls = []
    for sitemap_url in sub_sitemaps:
        urls = get_urls_from_sitemap(sitemap_url)
        all_urls.extend(urls)
        
    all_urls = sorted(list(set(all_urls)))
    print(f"Found {len(all_urls)} unique URLs across sitemaps.")
    
    if not all_urls:
        print("No URLs found to submit.")
        return
        
    payload = {
        "host": HOST,
        "key": API_KEY,
        "keyLocation": f"https://{HOST}/{API_KEY}.txt",
        "urlList": all_urls
    }
    
    indexnow_url = "https://api.indexnow.org/indexnow"
    print(f"Submitting payload to IndexNow: {indexnow_url}")
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            indexnow_url,
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_text = response.read().decode("utf-8")
            print(f"IndexNow API response status: {status_code}")
            if status_code == 200:
                print("IndexNow submission successful (HTTP 200). Search engines notified.")
            else:
                print(f"Submission returned status: {status_code}. Response: {response_text}")
    except Exception as e:
        print(f"Submission failed with error: {e}")

if __name__ == "__main__":
    main()
