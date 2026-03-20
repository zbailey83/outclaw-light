import xml.etree.ElementTree as ET
import sys

try:
    ET.parse('sitemap.xml')
    print("Sitemap is well-formed XML.")
except ET.ParseError as e:
    print(f"XML Parse Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
