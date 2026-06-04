import yaml
import os
from rapidfuzz import fuzz

# Load intents relative to this file's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, "intents.yaml")

with open(INTENTS_PATH, "r") as f:
    INTENTS = yaml.safe_load(f)

def detect_intent(text):
    text = text.lower()
    best_intent = "unknown"
    best_score = 0

    for intent, keywords in INTENTS.items():
        for keyword in keywords:
            keyword = keyword.lower()
            # If keyword is directly in text, it's a very strong match
            if keyword in text:
                score = 100
            else:
                # Fallback to fuzzy matching
                score = fuzz.partial_ratio(keyword, text)
            
            if score > 80 and score > best_score:
                best_score = score
                best_intent = intent

    return best_intent
