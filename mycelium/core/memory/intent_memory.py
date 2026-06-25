import json
from collections import defaultdict


class IntentMemory:
    def __init__(self, path="mycelium/memory/intent_memory.json"):
        self.path = path
        self.store = self._load()

    def _load(self):
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except:
            return {
                "success": defaultdict(int),
                "failure": defaultdict(int)
            }

    def record_success(self, intent_name):
        self.store["success"][intent_name] += 1
        self._save()

    def record_failure(self, intent_name):
        self.store["failure"][intent_name] += 1
        self._save()

    def weight(self, intent_name):
        s = self.store["success"].get(intent_name, 0)
        f = self.store["failure"].get(intent_name, 0)

        total = s + f
        if total == 0:
            return 1.0

        return s / total

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.store, f, indent=2)
