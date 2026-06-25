def compile_intent_graph(text: str):
    """
    Converts natural language into structured intent graph.
    """

    text = text.strip().lower()

    graph = {
        "nodes": [],
        "edges": []
    }

    if "explain" in text:
        graph["nodes"].append({
            "id": "n1",
            "type": "knowledge.query",
            "input": text
        })

    elif "play" in text:
        graph["nodes"].append({
            "id": "n1",
            "type": "media.play",
            "input": text
        })

    else:
        graph["nodes"].append({
            "id": "n1",
            "type": "system.unknown",
            "input": text
        })

    return {
        "status": "OK",
        "graph": graph
    }


def system_compile_graph(payload, context):
    return compile_intent_graph(payload.get("text", ""))
