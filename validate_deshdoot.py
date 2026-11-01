
import json
from collections import Counter
from urllib.parse import urlparse

INPUT_FILE = "deshdoot_kumbh_news_clean.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    articles = json.load(f)

print(f"Total articles: {len(articles)}")

# Check duplicate URLs and titles.
urls = [a.get("link", "").strip() for a in articles if a.get("link", "").strip()]
titles = [a.get("title", "").strip() for a in articles if a.get("title", "").strip()]

print(f"Unique URLs: {len(set(urls))}")
print(f"Duplicate URLs: {len(urls) - len(set(urls))}")
print(f"Unique titles: {len(set(titles))}")
print(f"Duplicate titles: {len(titles) - len(set(titles))}")

# Check required fields and classify preliminary relevance.
missing = Counter()
review = []

kumbh_terms = [
    "kumbh", "simhastha", " कुंभ", "कुंभमेळा",
    "सिंहस्थ", "त्र्यंबकेश्वर", "नाशिक"
]

for article in articles:
    for field in ["title", "link", "published_at", "content_text"]:
        if not article.get(field):
            missing[field] += 1

    text = " ".join([
        article.get("title", ""),
        article.get("description", ""),
        article.get("content_text", ""),
        " ".join(article.get("categories", [])),
    ]).lower()

    # This is only a keyword-based review flag, not a final ML label.
    matches = [term.strip() for term in kumbh_terms if term.strip().lower() in text]
    review.append({
        "title": article.get("title", ""),
        "url": article.get("link", ""),
        "keyword_matches": matches,
        "needs_manual_review": not any(
            term in text for term in ["kumbh", "simhastha", "कुंभ", "सिंहस्थ"]
        ),
    })

print("\nMissing required fields:")
print(dict(missing) if missing else "None")

print("\nArticle review:")
for i, item in enumerate(review, 1):
    print(f"\n{i}. {item['title']}")
    print(f"   URL: {item['url']}")
    print(f"   Keyword matches: {', '.join(item['keyword_matches']) or 'None'}")
    print(f"   Needs manual review: {item['needs_manual_review']}")

print("\nValidation complete. Original files were not changed.")
