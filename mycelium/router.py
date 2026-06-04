import yaml
import os
from rapidfuzz import fuzz
from .agents.router_agent import route_intent

# Load intents relative to this file's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, "intents.yaml")

with open(INTENTS_PATH, "r") as f:
    INTENTS = yaml.safe_load(f)

def detect_intent(text):
    """
    Hybrid intent detection:
    1. First, attempt semantic routing via LLM (Ollama).
    2. If LLM confidence is low or fails, fallback to keyword fuzzy matching.
    """
    # 1. Semantic Path
    llm_result = route_intent(text)
    if llm_result.get("confidence", 0) > 0.8:
        return llm_result

    # 2. Heuristic Path (Fallback)
    text = text.lower()
    best_intent = "unknown"
    best_score = 0

    for intent, keywords in INTENTS.items():
        for keyword in keywords:
            keyword = keyword.lower()
            if keyword in text:
                score = 100
            else:
                score = fuzz.partial_ratio(keyword, text)
            
            if score > 80 and score > best_score:
                best_score = score
                best_intent = intent

    return {
        "intent": best_intent,
        "confidence": best_score / 100.0,
        "entities": {"query": text} # Fallback puts raw text in query
    }
