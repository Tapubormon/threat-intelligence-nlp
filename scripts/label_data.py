import pandas as pd
import re

# Load CSV
df = pd.read_csv("data/reddit_ml_ready.csv")

# Define rule-based relevance classifier
def is_relevant(text):
    if pd.isna(text):
        return 0

    text = str(text).lower()

    # 1. Technical indicators
    if re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text):  # IP address
        return 1
    if re.search(r'\b[a-f0-9]{32,64}\b', text):  # Hashes
        return 1
    if re.search(r'cve-\d{4}-\d{4,7}', text):  # CVE ID
        return 1
    if re.search(r'\bt\d{4}\b', text):  # MITRE ATT&CK ID
        return 1

    # 2. Threat-related keywords
    relevant_keywords = [
        "phishing", "malware", "ioc", "indicator of compromise", "exploit",
        "vulnerability", "zero-day", "zeroday", "apt", "ransomware", "trojan",
        "leak", "data breach", "payload", "backdoor", "ddos", "rootkit", "botnet",
        "hash", "ip address", "command and control", "exfiltrate", "mitre",
        "tactic", "technique", "infection", "breach"
    ]
    for kw in relevant_keywords:
        if kw in text:
            return 1

    return 0  # Default: Not relevant

# Apply labeling
df["label"] = df["clean_text"].apply(is_relevant)

# Save updated CSV
df.to_csv("data/reddit_ml_ready_labeled.csv", index=False, encoding="utf-8")

print("✅ Labeled and saved to reddit_ml_ready_labeled.csv")
