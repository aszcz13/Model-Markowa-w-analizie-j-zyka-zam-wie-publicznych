import json
import os
import random
from collections import defaultdict

DATA_DIR = "data"
PROCESSED_DATA_FILE = os.path.join(DATA_DIR, "processed_tenders.json")

class MarkovModel:
    def __init__(self):
        self.transitions = defaultdict(list)
        self.start_words = []

    def train(self, texts):
        for text in texts:
            words = text.split() # Assuming text is already tokenized or space-separated
            if not words:
                continue
            
            self.start_words.append(words[0])
            
            for i in range(len(words) - 1):
                current_word = words[i]
                next_word = words[i+1]
                self.transitions[current_word].append(next_word)
                
            # Add a terminator for the last word to indicate end of sentence
            self.transitions[words[-1]].append(None)

    def generate(self, length=20):
        if not self.start_words:
            return ""
            
        current_word = random.choice(self.start_words)
        result = [current_word]
        
        for _ in range(length - 1):
            next_candidates = self.transitions.get(current_word)
            if not next_candidates:
                break
                
            next_word = random.choice(next_candidates)
            if next_word is None:
                break
                
            result.append(next_word)
            current_word = next_word
            
        return " ".join(result)

def load_processed_data():
    with open(PROCESSED_DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    data = load_processed_data()
    # Use cleaned_text for better flow, or join tokens
    texts = [item['cleaned_text'] for item in data]
    
    model = MarkovModel()
    print(f"Training Markov Model on {len(texts)} texts...")
    model.train(texts)
    
    print("\n--- Generated Tender Descriptions ---")
    for i in range(10):
        generated_text = model.generate(length=30)
        print(f"{i+1}. {generated_text}")

if __name__ == "__main__":
    main()
