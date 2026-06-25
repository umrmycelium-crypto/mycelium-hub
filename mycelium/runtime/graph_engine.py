from collections import defaultdict
import time
import math

class LiveGraph:
    """
    Stable, UI-safe graph state generator.
    Produces deterministic JSON for frontend rendering.
    """

    def __init__(self):
        self.nodes = {}
        self.edges = {}

    # ----------------------------
    # ingestion (event -> graph)
    # ----------------------------
    def ingest(self, trace):
        now = time.time()

        for event in trace:
            t = event.get("type") or event.get("event") or "unknown"

            if t not in self.nodes:
                self.nodes[t] = {
                    "id": t,
                    "weight": 0,
                    "pulse": 0.0,
                    "last_seen": now
                }

            node = self.nodes[t]
            node["weight"] += 1
            node["last_seen"] = now
            node["pulse"] = min(1.0, node["pulse"] + 0.35)

        self._decay(now)

    # ----------------------------
    # smooth decay = “heartbeat”
    # ----------------------------
    def _decay(self, now):
        for n in self.nodes.values():
            age = now - n["last_seen"]
            n["pulse"] *= math.exp(-age * 0.8)

            # clamp noise
            if n["pulse"] < 0.01:
                n["pulse"] = 0.0

    # ----------------------------
    # frontend-safe snapshot
    # ----------------------------
    def snapshot(self):
        return {
            "nodes": list(self.nodes.values()),
            "edges": list(self.edges.values()),
            "meta": {
                "node_count": len(self.nodes),
                "edge_count": len(self.edges),
                "timestamp": time.time()
            }
        }


GRAPH = LiveGraph()
