from mycelium.core.governance_events import get_events


def build_graph(limit=200):
    events = get_events()[-limit:]

    nodes = []
    edges = []

    prev = None

    for i, e in enumerate(events):
        node_id = i

        nodes.append({
            "id": node_id,
            "type": e["event"],
            "timestamp": e["timestamp"]
        })

        if prev is not None:
            edges.append({
                "from": prev,
                "to": node_id,
                "relation": "next"
            })

        prev = node_id

    return {
        "nodes": nodes,
        "edges": edges
    }
