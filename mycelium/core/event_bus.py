from collections import defaultdict

class EventBus:
    """
    A simple, synchronous event bus for decoupling intent detection from action execution.
    """
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_type, handler):
        """
        Registers a handler for a specific event type.
        """
        self.subscribers[event_type].append(handler)

    def publish(self, event_type, payload):
        """
        Notifies all subscribers of an event and returns their results.
        """
        results = []
        if event_type not in self.subscribers:
            # Fallback to 'unknown' or just return empty
            pass

        for handler in self.subscribers[event_type]:
            results.append(handler(payload))

        return results
