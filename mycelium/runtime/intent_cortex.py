from collections import defaultdict, deque

class IntentCortex:
    """
    Tracks intent chains and causal flow:
    intent A → intent B → intent C
    """

    def __init__(self, max_items=500):
        self.chain = defaultdict(list)
        self.history = deque(maxlen=max_items)
        self.last_intent = None

    def ingest(self, intent_event):
        intent = None

        if isinstance(intent_event, dict):
            intent = (
                intent_event.get("intent")
                or intent_event.get("name")
                or intent_event.get("type")
            )
        elif isinstance(intent_event, str):
            intent = intent_event
        else:
            intent = "unknown"

        if self.last_intent:
            self.chain[self.last_intent].append(intent)

        self.last_intent = intent
        self.history.append(intent)

    def snapshot(self):
        return {
            "nodes": list(self.chain.keys()),
            "edges": {k: v for k, v in self.chain.items()},
            "last": self.last_intent,
            "depth": len(self.history)
        }


INTENT_CORTEX = IntentCortex()
