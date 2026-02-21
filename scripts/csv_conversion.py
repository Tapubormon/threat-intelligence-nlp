import json
import pandas as pd

# Load preprocessed JSON with clean_text
with open("data/reddit_clean_data.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

df = pd.DataFrame(posts)

# Only keep the fields necessary for ML model
df = df[["clean_text"]].copy()

# Add empty label column for manual or automatic labeling
df["label"] = ""

# Export to CSV
df.to_csv(
    "data/reddit_ml_ready.csv",
    index=False,
    encoding="utf-8"
)

print("✅ Exported reddit_ml_ready.csv – Ready for labeling or model training")