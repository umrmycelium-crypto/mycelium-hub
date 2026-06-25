from mycelium.core.memory.intent_memory import IntentMemory

memory = IntentMemory()


def apply_weights(intent_graph):
    for intent in intent_graph.get("intents", []):
        w = memory.weight(intent["name"])

        # adjust confidence, but clamp
        intent["confidence"] = min(
            1.0,
            max(0.0, intent["confidence"] * (0.5 + w))
        )

    return intent_graph
