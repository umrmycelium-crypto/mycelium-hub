from mycelium.core.execution_trace import get_trace

def build_graph(trace):
    nodes = {}
    edges = {}

    # trace expected: list of events
    for event in trace:
        src = event.get("source", "unknown")
        dst = event.get("target", "dashboard")

        nodes[src] = nodes.get(src, 0) + 1
        nodes[dst] = nodes.get(dst, 0) + 1

        key = f"{src}->{dst}"
        edges[key] = edges.get(key, 0) + 1

    return {
        "nodes": [
            {"id": k, "weight": v}
            for k, v in nodes.items()
        ],
        "edges": [
            {"id": k, "weight": v}
            for k, v in edges.items()
        ],
        "heartbeat": {
            "total_events": len(trace),
            "active_nodes": len(nodes)
        }
    }
