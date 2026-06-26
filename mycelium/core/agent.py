from mycelium.core.router import route


class MyceliumAgent:
    """
    Unified dict-intent agent runtime.
    """

    def __init__(self, name: str, capabilities: list, handler):
        self.name = name
        self.capabilities = capabilities
        self.handler = handler

    def run(self, task: dict):
        # HARD STANDARDIZATION: dict-only intent
        intent = self.normalize(task)
        return route(intent)

    def normalize(self, task: dict):
        """
        Accepts legacy or dict inputs and forces standard shape.
        """

        # already correct format
        if isinstance(task, dict) and "name" in task:
            return task

        # legacy object fallback (safe bridge)
        name = getattr(task, "intent", None) or getattr(task, "name", None)

        return {
            "name": name,
            "payload": getattr(task, "payload", {}) if hasattr(task, "payload") else {},
            "context": getattr(task, "context", {}) if hasattr(task, "context") else {}
        }
