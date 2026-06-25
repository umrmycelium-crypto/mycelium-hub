class IntentMemory:
    """
    Stores unknown or implicit intents for learning.
    """

    def __init__(self):
        self.raw_events = []

    def record(self, raw_input: str, resolved: str):
        self.raw_events.append({
            "input": raw_input,
            "resolved": resolved
        })

    def get_all(self):
        return self.raw_events


INTENT_MEMORY = IntentMemory()
