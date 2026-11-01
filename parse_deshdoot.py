
import json
import urllib.request
import xml.etree.ElementTree as ET
import html

FEED_URL = "https://deshdoot.com/search/kumbh+mela+nashik/feed/rss2/"

namespaces = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
}

request = urllib.request.Request(
    FEED_URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(request, timeout=30) as response:
    xml_data = response.read()

root = ET.fromstring(xml_data)
channel = root.find("channel")

if channel is None:
    raise RuntimeError("RSS channel not found.")

articles = []

for item in channel.findall("item"):
    content = item.findtext("content:encoded", default="", namespaces=namespaces)
    description = item.findtext("description", default="")

    articles.append({
        "title": item.findtext("title", default="").strip(),
        "link": item.findtext("link", default="").strip(),
        "author": item.findtext("dc:creator", default="", namespaces=namespaces).strip(),
        "published_at": item.findtext("pubDate", default="").strip(),
        "categories": [
            category.text.strip()
            for category in item.findall("category")
            if category.text
        ],
        "description": html.unescape(description),
        "content_html": content,
    })

output_file = "deshdoot_kumbh_news.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(articles, file, ensure_ascii=False, indent=2)

print(f"Success: extracted {len(articles)} articles.")
print(f"Saved to: {output_file}")

if articles:
    print("\nFirst article:")
    print(json.dumps(articles[0], ensure_ascii=False, indent=2)[:2500])
