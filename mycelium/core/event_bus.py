from collections import defaultdict

class EventBus:
    """
    A synchronous event bus supporting type-specific and global '*' subscribers.
    """
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_type, handler):
        """
        Registers a handler for a specific event type or '*' for all events.
        """
        self.subscribers[event_type].append(handler)

    def publish(self, event_type, payload):
        """
        Notifies all subscribers and then global '*' hooks.
        """
        results = []
        
        # 1. Notify specific subscribers
        for handler in self.subscribers.get(event_type, []):
            results.append(handler(payload))

        # 2. Notify global '*' subscribers (traceability/logging)
        for handler in self.subscribers.get("*", []):
            # Global handlers receive (type, payload, results) for context
            handler(event_type, payload, results)

        return results
