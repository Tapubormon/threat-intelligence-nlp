import json
import os
import re
import contractions


def remove_repeated_characters(text):
    # Replace repeated characters (>2) with 2 characters (coooool -> coool)
    return re.sub(r'(.)\1{2,}', r'\1\1', text)


def clean_text(text):
    if not text:
        return ""

    # Expand contractions
    text = contractions.fix(text)

    # Lowercase
    text = text.lower()

    # Replace URLs with token [URL]
    text = re.sub(r'http\S+|www\S+', ' [URL] ', text)

    # Remove Reddit usernames and subreddits
    text = re.sub(r'/r/\S+|u/\S+', '', text)

    # Remove Reddit placeholders [deleted], [removed]
    text = re.sub(r'\[deleted\]|\[removed\]', '', text)

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove literal unicode escape sequences like \u2019
    text = re.sub(r'\\u[0-9a-fA-F]{4}', '', text)

    # Remove special characters except common punctuation and whitespace
    text = re.sub(r'[^\w\s.,!?]', '', text)

    # Remove repeated characters (optional)
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    # Remove newlines and carriage returns
    text = text.replace('\n', ' ').replace('\r', ' ')

    # Remove non-ASCII characters (including superscripts, emojis, etc.)
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    # Collapse multiple spaces into one and trim
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def preprocess_reddit_data(input_path="data/reddit_raw_data.json", output_path="data/reddit_clean_data.json",
                           min_length=10):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    clean_data = []

    for post in raw_data:
        title = clean_text(post.get("title", ""))
        body = clean_text(post.get("body", ""))
        combined = f"{title} {body}".strip()

        # Filter out very short posts if desired
        if combined and len(combined.split()) >= min_length:
            post["clean_text"] = combined
            clean_data.append(post)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=4)

    print(f"✅ Preprocessed and saved {len(clean_data)} posts.")


if __name__ == "__main__":
    preprocess_reddit_data()
