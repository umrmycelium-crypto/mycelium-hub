from mycelium.core.execution_trace import get_trace
from collections import defaultdict

def build_self_graph(limit=200):
    trace = get_trace(limit)

    nodes = defaultdict(int)
    edges = defaultdict(int)

    for event in trace:
        src = event.get("module", "unknown")
        dst = event.get("target", "system")

        nodes[src] += 1
        edges[(src, dst)] += 1

    return {
        "nodes": [
            {"id": n, "weight": w}
            for n, w in nodes.items()
        ],
        "edges": [
            {"source": a, "target": b, "weight": w}
            for (a, b), w in edges.items()
        ]
    }
