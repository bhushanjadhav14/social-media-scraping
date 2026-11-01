
import json

INPUT_FILE = "deshdoot_kumbh_news_clean.json"
OUTPUT_FILE = "deshdoot_kumbh_review.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    articles = json.load(f)

def classify(article):
    text = " ".join([
        article.get("title", ""),
        article.get("description", ""),
        article.get("content_text", ""),
        " ".join(article.get("categories", [])),
    ]).lower()

    infrastructure_terms = [
        "infrastructure", "पायाभूत सुविधा", "रस्त", "खड्डा",
        "parking", "पार्किंग", "traffic", "वाहतूक",
        "पाणी", "घाट", "tent city", "निवास"
    ]

    event_terms = [
        "ध्वजारोहण", "ध्वजस्तंभ", "शंखनाद",
        "धार्मिक सोहळा", "कुंभमेळा आयुक्त"
    ]

    security_terms = [
        "पोलीस", "सुरक्षा", "police", "security"
    ]

    if any(term in text for term in security_terms):
        category = "Security & Crowd Management"
    elif any(term in text for term in infrastructure_terms):
        category = "Infrastructure & Facilities"
    elif any(term in text for term in event_terms):
        category = "Events & Governance"
    else:
        category = "General Kumbh News"

    return category

for article in articles:
    article["proposed_category"] = classify(article)
    article["review_status"] = "needs_manual_review"
    article["relevance_label"] = None

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"Prepared {len(articles)} articles for manual review.")
print(f"Saved to {OUTPUT_FILE}")
print("\nProposed categories:")

for i, article in enumerate(articles, 1):
    print(f"{i}. [{article['proposed_category']}] {article['title']}")
