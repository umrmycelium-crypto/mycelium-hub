import yaml
import os
from rapidfuzz import fuzz
from .agents.router_agent import route_intent
from .core.agent_router import AgentRouter

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

def dispatch_intent(text):
    """
    The complete execution flow:
    1. Detect the intent from the raw text.
    2. Resolve the agent responsible for that intent.
    3. Execute the agent's handler with the extracted entities.
    """
    # 1. Detect
    intent_data = detect_intent(text)
    intent_name = intent_data.get("intent")
    
    if intent_name == "unknown":
        return {
            "status": "ERROR",
            "message": f"Could not resolve intent for input: '{text}'"
        }

    # 2. Resolve
    agent = AgentRouter.resolve(intent_name)
    if not agent:
        return {
            "status": "ERROR",
            "message": f"No agent registered for intent: '{intent_name}'"
        }

    # 3. Execute
    try:
        # We pass the entities as the payload to the handler
        result = agent.handler(intent_data.get("entities", {}), {})
        return {
            "status": "OK",
            "intent": intent_name,
            "agent": agent.name,
            "result": result
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "intent": intent_name,
            "agent": agent.name,
            "message": f"Execution failed: {str(e)}"
        }
