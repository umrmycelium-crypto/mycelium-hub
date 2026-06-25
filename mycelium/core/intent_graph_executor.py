from mycelium.core.registry_core import get_registry


def execute_graph(graph: dict):
    registry = get_registry()

    results = []

    for node in graph.get("nodes", []):
        node_type = node.get("type")
        input_data = node.get("input")

        handler = registry.get(node_type)

        if not handler:
            results.append({
                "node": node,
                "status": "NO_HANDLER"
            })
            continue

        results.append({
            "node": node,
            "result": handler({"input": input_data}, {"source": "graph_executor"})
        })

    return {
        "status": "OK",
        "results": results
    }


def system_execute_graph(payload, context):
    return execute_graph(payload.get("graph", {}))
