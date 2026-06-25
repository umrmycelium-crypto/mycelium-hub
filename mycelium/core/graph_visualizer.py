from mycelium.core.execution_trace import trace


def visualize_graph_execution(graph: dict):
    steps = []

    for node in graph.get("nodes", []):
        steps.append({
            "node": node,
            "status": "pending"
        })

        trace("graph.node", node)

    return {
        "status": "OK",
        "steps": steps
    }


def system_graph_view(payload, context):
    return visualize_graph_execution(payload.get("graph", {}))
