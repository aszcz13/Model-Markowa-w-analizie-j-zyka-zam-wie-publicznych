import json
import os
import spacy
import string
import pandas as pd
from collections import Counter

DATA_DIR = "data"
RAW_DATA_FILE = os.path.join(DATA_DIR, "raw_tenders.json")
PROCESSED_DATA_FILE = os.path.join(DATA_DIR, "processed_tenders.json")

def load_data():
    with open(RAW_DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_text(text):
    if not text:
        return ""
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def process_data():
    print("Loading spacy model...")
    try:
        nlp = spacy.load("pl_core_news_sm")
    except OSError:
        print("Model not found. Please run: python -m spacy download pl_core_news_sm")
        return

    data = load_data()
    processed_data = []

    print(f"Processing {len(data)} records...")
    
    for item in data:
        # Extract text. 'orderObject' seems to be the main description.
        # Sometimes there might be more details, but we'll stick to what we have.
        raw_text = item.get('orderObject', '')
        label = item.get('orderType', 'Unknown')
        
        if not raw_text:
            continue

        cleaned_text = clean_text(raw_text)
        doc = nlp(cleaned_text)
        
        tokens = [token.text for token in doc if not token.is_stop and not token.is_space]
        lemmas = [token.lemma_ for token in doc if not token.is_stop and not token.is_space]
        pos_tags = [token.pos_ for token in doc if not token.is_stop and not token.is_space]
        
        # Basic stats
        word_count = len(tokens)
        sentence_count = len(list(doc.sents)) # This might be 1 if we removed punctuation, but spacy handles it reasonably
        
        processed_item = {
            "original_text": raw_text,
            "cleaned_text": cleaned_text,
            "tokens": tokens,
            "lemmas": lemmas,
            "pos_tags": pos_tags,
            "label": label,
            "stats": {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "noun_count": pos_tags.count("NOUN"),
                "adj_count": pos_tags.count("ADJ"),
                "verb_count": pos_tags.count("VERB")
            }
        }
        processed_data.append(processed_item)

    # Save processed data
    with open(PROCESSED_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)
        
    print(f"Processed data saved to {PROCESSED_DATA_FILE}")
    return processed_data

def analyze_stats(processed_data):
    df = pd.DataFrame([item['stats'] for item in processed_data])
    print("\n--- Text Analysis Statistics ---")
    print(df.describe())
    
    # Label distribution
    labels = [item['label'] for item in processed_data]
    print("\n--- Label Distribution ---")
    print(pd.Series(labels).value_counts())

if __name__ == "__main__":
    processed = process_data()
    if processed:
        analyze_stats(processed)
