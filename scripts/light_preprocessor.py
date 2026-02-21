import json
import os
import re
import contractions


def light_clean_text(text, to_lower=True):
    if not text:
        return ""

    # Expand contractions
    text = contractions.fix(text)

    # Lowercase (optional)
    if to_lower:
        text = text.lower()

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove Reddit placeholders
    text = re.sub(r'\[deleted\]|\[removed\]', '', text)

    # Remove literal unicode escape sequences like \u2019
    text = re.sub(r'\\u[0-9a-fA-F]{4}', '', text)

    # Keep punctuation and symbols important for IOCs, remove control chars
    text = re.sub(r'[^\x20-\x7E]', ' ', text)

    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def preprocess_reddit_data_light(
    input_path="data/reddit_raw_data.json",
    output_path="data/reddit_clean_data_light.json",
    min_length=5
):

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    clean_data = []

    for post in raw_data:
        title = light_clean_text(post.get("title", ""))
        body = light_clean_text(post.get("body", ""))
        combined = f"{title} {body}".strip()

        if combined and len(combined.split()) >= min_length:
            post["clean_text"] = combined
            clean_data.append(post)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=4)

    print(f"✅ Light preprocessed and saved {len(clean_data)} posts.")


if __name__ == "__main__":
    preprocess_reddit_data_light()
