
import json
import re
from bs4 import BeautifulSoup

INPUT_FILE = "deshdoot_kumbh_news.json"
OUTPUT_FILE = "deshdoot_kumbh_news_clean.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    articles = json.load(f)

cleaned = []

for article in articles:
    content_html = article.get("content_html", "")
    description = article.get("description", "")

    # Convert HTML article content into readable text.
    content_text = BeautifulSoup(content_html, "html.parser").get_text(
        separator=" ", strip=True
    )
    description_text = BeautifulSoup(description, "html.parser").get_text(
        separator=" ", strip=True
    )

    # Normalize repeated whitespace without removing Marathi characters.
    content_text = re.sub(r"\s+", " ", content_text).strip()
    description_text = re.sub(r"\s+", " ", description_text).strip()

    cleaned.append({
        "source": "Deshdoot",
        "title": article.get("title", ""),
        "link": article.get("link", ""),
        "author": article.get("author", ""),
        "published_at": article.get("published_at", ""),
        "categories": article.get("categories", []),
        "description": description_text,
        "content_text": content_text or description_text,
    })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print(f"Cleaned {len(cleaned)} articles.")
print(f"Saved to {OUTPUT_FILE}")

if cleaned:
    print("\nFirst article text preview:")
    print(cleaned[0]["content_text"][:800])
