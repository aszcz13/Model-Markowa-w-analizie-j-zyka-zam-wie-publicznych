import json
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

DATA_DIR = "data"
PROCESSED_DATA_FILE = os.path.join(DATA_DIR, "processed_tenders.json")
REPORT_DIR = "report"

def load_data():
    with open(PROCESSED_DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def train_and_evaluate():
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
        
    data = load_data()
    df = pd.DataFrame(data)
    
    # Filter out unknown labels if any
    df = df[df['label'] != 'Unknown']
    
    # Features and Labels
    X = df['cleaned_text']
    y = df['label']
    
    print(f"Dataset size: {len(df)}")
    print(f"Label distribution:\n{y.value_counts()}")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Vectorization
    tfidf = TfidfVectorizer(max_features=1000)
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)
    
    # Models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Naive Bayes": MultinomialNB()
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train_tfidf, y_train)
        y_pred = model.predict(X_test_tfidf)
        
        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {acc:.4f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        
        results[name] = {
            "accuracy": acc,
            "report": classification_report(y_test, y_pred, output_dict=True),
            "confusion_matrix": confusion_matrix(y_test, y_pred)
        }
        
        # Plot Confusion Matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues',
                    xticklabels=model.classes_, yticklabels=model.classes_)
        plt.title(f'Confusion Matrix - {name}')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.tight_layout()
        plt.savefig(os.path.join(REPORT_DIR, f'confusion_matrix_{name.replace(" ", "_").lower()}.png'))
        plt.close()

    # Save results summary
    with open(os.path.join(REPORT_DIR, "classification_results.json"), 'w') as f:
        # Convert numpy types to python types for json serialization
        serializable_results = {}
        for name, res in results.items():
            serializable_results[name] = {
                "accuracy": res["accuracy"],
                "report": res["report"]
            }
        json.dump(serializable_results, f, indent=2)

    return results

if __name__ == "__main__":
    train_and_evaluate()
