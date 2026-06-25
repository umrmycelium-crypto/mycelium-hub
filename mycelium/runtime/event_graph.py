from collections import defaultdict, deque

class EventGraph:
    """
    Lightweight in-memory event DAG.
    Nodes = event types
    Edges = temporal transitions
    """

    def __init__(self, max_edges=500):
        self.edges = defaultdict(lambda: defaultdict(int))
        self.last_event = None
        self.history = deque(maxlen=max_edges)

    def ingest(self, event):
        """
        Event expected format:
        {
            "type": str,
            "timestamp": float (optional)
        }
        """

        etype = None

        if isinstance(event, dict):
            etype = event.get("type") or event.get("event")
        elif isinstance(event, str):
            etype = event
        else:
            etype = "unknown"

        if self.last_event is not None:
            self.edges[self.last_event][etype] += 1

        self.last_event = etype
        self.history.append(etype)

    def snapshot(self):
        return {
            "nodes": list(self.edges.keys()),
            "edges": {
                k: dict(v) for k, v in self.edges.items()
            },
            "last": self.last_event,
            "depth": len(self.history)
        }


EVENT_GRAPH = EventGraph()
