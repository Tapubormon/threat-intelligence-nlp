import time
import requests
import trafilatura
from urllib.parse import urlparse

RAW_JSON = "data/reddit_raw_data_fallback.json"
ENRICHED_JSON = "data/reddit_raw_data_fallback_enriched.json"
REQUEST_TIMEOUT = 10
DELAY_BETWEEN_REQUESTS = 2

def fetch_article_text(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            extracted = trafilatura.extract(resp.text)
            if extracted:
                return extracted.strip()
    except Exception as e:
        print(f"⚠️ Failed to fetch {url}: {e}")
    return None

def enrich_posts_with_article_text(posts, whitelist_domains):
    enriched_count = 0

    for post in posts:
        body = post.get("body", "")
        if isinstance(body, str) and body.startswith(("http://", "https://")):
            parsed = urlparse(body)
            domain = parsed.netloc.lower()
            if domain.startswith("www."):
                domain = domain[4:]
            if domain in whitelist_domains:
                print(f"🔗 Fetching content from {body}")
                article_text = fetch_article_text(body)
                if article_text:
                    post["body"] = article_text
                    enriched_count += 1
                    print(f"✅ Extracted article text from {domain}")
                else:
                    print(f"❌ Could not extract article text from {domain}")
                time.sleep(DELAY_BETWEEN_REQUESTS)  # polite delay
            else:
                print(f"⚠️ Domain {domain} not in whitelist")
        else:
            print(f"⚠️ Body is not a URL or empty: {body[:30]}...")

    print(f"✅ Enriched {enriched_count} posts out of {len(posts)} total")
    return posts

def main():
    import json
    from top_domain import extract_all_domains  # <-- Import the new function

    with open(RAW_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)

    whitelist_domains = extract_all_domains(RAW_JSON)  # <-- Get all domains, no top N limit

    enriched_posts = enrich_posts_with_article_text(posts, whitelist_domains)

    with open(ENRICHED_JSON, "w", encoding="utf-8") as f:
        json.dump(enriched_posts, f, indent=4)

    print(f"✅ Enriched data saved to {ENRICHED_JSON}")


if __name__ == "__main__":
    main()
