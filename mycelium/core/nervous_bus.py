from collections import defaultdict


class NervousBus:

    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, signal_type, handler):
        self.subscribers[signal_type].append(handler)

    def emit(self, signal):

        results = []

        handlers = self.subscribers.get(signal.type, [])

        for handler in handlers:
            try:
                results.append(handler(signal))
            except Exception as e:
                results.append({
                    "error": str(e),
                    "handler": handler.__name__
                })

        return results
