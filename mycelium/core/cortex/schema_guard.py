def enforce_schema(intent_graph):
    if "intents" not in intent_graph:
        return False

    for intent in intent_graph["intents"]:
        if "name" not in intent:
            return False
        if "confidence" not in intent:
            return False
        if not (0.0 <= intent["confidence"] <= 1.0):
            return False

    return True
