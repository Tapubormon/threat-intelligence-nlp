import json
from urllib.parse import urlparse
from collections import Counter

RAW_JSON = "data/reddit_raw_data_fallback.json"

def extract_all_domains(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    domains = []
    for post in posts:
        body = post.get('body', '')
        if isinstance(body, str) and body.startswith(('http://', 'https://')):
            parsed_url = urlparse(body)
            domain = parsed_url.netloc.lower()
            if domain.startswith('www.'):
                domain = domain[4:]
            domains.append(domain)

    domain_counts = Counter(domains)

    print(f"🔍 All linked domains extracted ({len(domain_counts)} unique domains):")
    for domain, count in domain_counts.most_common():
        print(f" - {domain}: {count} links")

    return list(domain_counts.keys())

if __name__ == "__main__":
    extract_all_domains(RAW_JSON)
