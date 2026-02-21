import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

SUBREDDITS = ["netsec", "cybersecurity", "hacking", "Malware", "ThreatHunting"]
MAX_SCROLLS = 15
DELAY = 3  # seconds

RAW_JSON = "data/reddit_raw_data_fallback.json"

def configure_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    )
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(MAX_SCROLLS):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(DELAY + 2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_posts_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    posts = soup.find_all("shreddit-post")
    scraped = []

    for post in posts:
        try:
            title_tag = post.find("a", {"slot": "title"})
            title = title_tag.get_text(strip=True) if title_tag else ""

            text_body_tag = post.find("div", {"property": "schema:articleBody"})
            if text_body_tag:
                body = text_body_tag.get_text("\n", strip=True)
            else:
                link_tag = post.find("a", class_="post-link")
                body = link_tag["href"] if link_tag else ""

            created_str = post.get("created-timestamp", "")
            created = datetime.fromisoformat(created_str.replace("Z", "+00:00")).timestamp() if created_str else time.time()

            author_tag = post.find("a", href=lambda x: x and "/user/" in x)
            author = author_tag.get_text(strip=True) if author_tag else "unknown"

            score = int(post.get("score", "0"))
            subreddit = post.get("subreddit-name", "unknown")

            if title and body:
                scraped.append({
                    "title": title,
                    "body": body,
                    "created": created,
                    "author": author,
                    "score": score,
                    "subreddit": subreddit
                })

        except Exception as e:
            print("⚠️ Skipping a post due to error:", e)

    return scraped

def fallback_scraper():
    print("⚠️ Using Fallback Scraper via Selenium...")
    driver = configure_driver()
    all_data = []

    for sub in SUBREDDITS:
        print(f"🔄 Loading https://www.reddit.com/r/{sub}/new/")
        url = f"https://www.reddit.com/r/{sub}/new/"
        driver.get(url)
        time.sleep(3)
        scroll_down(driver)

        html = driver.page_source
        posts = extract_posts_from_html(html)
        print(f"✅ Scraped {len(posts)} posts from r/{sub}")
        all_data.extend(posts)

    driver.quit()

    import os
    os.makedirs("data", exist_ok=True)
    with open(RAW_JSON, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4)

    print(f"✅ Total fallback data saved: {len(all_data)} posts")
    return all_data

if __name__ == "__main__":
    fallback_scraper()
