# Reddit CTI Relevance Classifier & IOC Extraction

A machine learning pipeline for collecting Reddit posts, classifying Cyber Threat Intelligence (CTI) relevance, and extracting/validating Indicators of Compromise (IOCs).

## Quick Start

### Phase 1: Model Training

#### Step 1-3: Collect & Preprocess Data

1. **Setup Configuration**
   - Copy `config/reddit_config.py.example` to `config/reddit_config.py`
   - Add your Reddit API credentials

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Collect & Preprocess Data**
   ```bash
   python scripts/reddit_collector.py      # → reddit_raw_data.json
   python scripts/preprocessor.py          # → reddit_clean_data.json
   python scripts/csv_conversion.py        # → reddit_ml_ready.csv
   ```
   
   **Note**: If `reddit_collector.py` fails, the system automatically runs:
   - `fallback_scraper.py` → merges with `top_domain.py` → `enrich_posts.py`

#### Step 4: Label Data - Choose One Option

##### Option A: Automatic Labeling (Quick - for testing)
```bash
python scripts/label_data.py             # → reddit_ml_ready_labeled.csv
```
- ⚡ Fast labeling using keyword-based matching
- ⚠️ Not 100% accurate - uses heuristics and patterns
- ✅ Good for testing, prototyping, or reducing time
- 📝 **Note**: Review results and verify manually before production use

##### Option B: Manual Labeling (Accurate - for production)
1. Open `scripts/data/reddit_ml_ready.csv` in your preferred tool (Excel, Google Sheets, etc.)
2. Label each post as CTI-relevant or non-relevant
3. Save as `reddit_ml_ready_labeled.csv` in `scripts/data/`
- ✅ High accuracy - human verification
- ⏱️ Takes more time
- 🎯 Recommended for production models

#### Step 5-6: Train Model

5. **Upload Labeled Data**
   - Upload `reddit_ml_ready_labeled.csv` to Google Drive

6. **Train Model**
   - Run all cells in `CTI_Relevance_Classifier.ipynb` in Google Colab
   - Model saves automatically to Google Drive under `distilbert_cti_model/` folder

✅ **Model training complete**

---

### Phase 2: Predict on New Data

#### Step 7-10: Collect & Preprocess New Data

7. **Collect New Posts**
   ```bash
   python scripts/reddit_collector.py      # → reddit_raw_data.json
   ```

8. **Preprocess Data**
   ```bash
   python scripts/light_preprocessor.py          # → reddit_clean_data_light.json
   ```

9. **Convert to CSV**
   ```bash
   python scripts/csv_conversion.py        # → reddit_ml_ready.csv
   ```

10. **Upload to Google Drive**
    - Upload `reddit_ml_ready.csv` to Google Drive

#### Step 11-13: Classify & Extract IOCs

11. **Classify Posts**
    - Run all cells in `CTI_Relevance_Classifier_with_new_data.ipynb`
    - Output: `relevant_posts.csv`

12. **Extract IOCs**
    - Run all cells in `IOC_Extraction_ipynp.ipynb`
    - Output: `extracted_iocs.json`

13. **Validate IOCs**
    - Run all cells in `Check_With_Virus_tools.ipynb`
    - Output: `validated_iocs.json`

## Project Structure

```
project-root/
├── config/
│   ├── reddit_config.py.example
│   └── reddit_config.py (local - not uploaded)
├── scripts/
│   ├── reddit_collector.py
│   ├── fallback_scraper.py
│   ├── preprocessor.py
│   ├── csv_conversion.py
│   ├── label_data.py           ← Auto-labeling (optional)
│   ├── enrich_posts.py
│   ├── top_domain.py
│   ├── checkLength.py
│   ├── scheduler.py
│   └── data/ (local - not uploaded)
├── CTI_Relevance_Classifier.ipynb
├── CTI_Relevance_Classifier_with_new_data.ipynb
├── IOC_Extraction_ipynp.ipynb
├── Check_With_Virus_tools.ipynb
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.8+
- Reddit API credentials
- Google Drive account (for model storage)
- VirusTotal API key (optional, for IOC validation)

See `requirements.txt` for Python dependencies.


