from mycelium.core.event_store import append_event
from mycelium.core.projections import apply_live


class EventBus:
    def __init__(self):
        self.subscribers = []
        self.post_hooks = []

    def subscribe(self, fn):
        self.subscribers.append(fn)

    def subscribe_post(self, fn):
        self.post_hooks.append(fn)

    def publish(self, event: dict):

        append_event(event)
        apply_live(event)

        results = []

        for sub in self.subscribers:
            try:
                results.append(sub(event))
            except Exception as e:
                results.append({"error": str(e)})

        # -----------------------------
        # POST HOOKS (non-blocking logic)
        # -----------------------------
        for hook in self.post_hooks:
            try:
                hook(event)
            except Exception:
                pass

        return results


EVENT_BUS = EventBus()
