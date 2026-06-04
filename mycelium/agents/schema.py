# Defined intent schema for the Mycelium Ecosystem
INTENT_SCHEMA = {
    "intent": "media.play | media.search | system.status | knowledge.search | developer.assist | unknown",
    "confidence": "float 0-1",
    "entities": {
        "title": "string (optional)",
        "query": "string (optional)"
    }
}
