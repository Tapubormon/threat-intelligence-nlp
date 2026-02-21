import praw
import json
import os
from config import reddit_config
from fallback_scraper import fallback_scraper
from enrich_posts import main as enrich_posts_main

# Reddit Auth
reddit = praw.Reddit(
    client_id=reddit_config.REDDIT_CLIENT_ID,
    client_secret=reddit_config.REDDIT_CLIENT_SECRET,
    username=reddit_config.REDDIT_USERNAME,
    password=reddit_config.REDDIT_PASSWORD,
    user_agent=reddit_config.REDDIT_USER_AGENT
)

# Target Subreddits
subreddits = ["netsec", "cybersecurity", "hacking", "Malware", "ThreatHunting"]
subreddit = reddit.subreddit("+".join(subreddits))

# Load previous data
DATA_PATH = "data/reddit_raw_data.json"
existing_posts = []
existing_ids = set()

if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        existing_posts = json.load(f)
        existing_ids = {post.get("title", "") + post.get("body", "") for post in existing_posts}

# Collect new posts
new_data = []
try:
    print("🔄 Fetching posts from Reddit API...")
    raise Exception("Force fallback for testing")
    for post in subreddit.new(limit=500):
        unique_key = post.title + post.selftext
        if unique_key not in existing_ids:
            new_data.append({
                "title": post.title,
                "body": post.selftext,
                "created": post.created_utc,
                "author": str(post.author),
                "score": post.score,
                "subreddit": post.subreddit.display_name
            })
            existing_ids.add(unique_key)

    if len(new_data) == 0:
        raise ValueError("API returned 0 posts")  # force fallback if no data
    print(f"✅ Fetched {len(new_data)} new posts.")

except Exception as e:
    print("❌ Reddit API failed:", e)
    print("⚠️ Using fallback method (web scraping)...")

    # Run fallback scraper to get raw posts (and save raw JSON)
    new_data = fallback_scraper()
    if new_data is None:
        new_data = []

    # Run enrichment process to fetch article text from top domains and save enriched JSON
    enrich_posts_main()

    # Load enriched data instead of raw data for merging
    enriched_json_path = "data/reddit_raw_data_fallback_enriched.json"
    if os.path.exists(enriched_json_path):
        with open(enriched_json_path, "r", encoding="utf-8") as f:
            enriched_data = json.load(f)
    else:
        enriched_data = new_data  # fallback to raw if enriched missing

    merged_data = existing_posts + enriched_data


# Merge and Save
merged_data = existing_posts + new_data
os.makedirs("data", exist_ok=True)

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(merged_data, f, indent=4)

print(f"✅ Total saved posts: {len(merged_data)}")
