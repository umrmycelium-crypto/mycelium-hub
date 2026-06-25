def verify_intent_structure(intent: dict):
    """
    Structural correctness check.
    """

    required_fields = ["name", "payload", "context"]

    for f in required_fields:
        if f not in intent:
            return {
                "valid": False,
                "reason": f"missing field: {f}"
            }

    if not isinstance(intent["payload"], dict):
        return {
            "valid": False,
            "reason": "payload must be dict"
        }

    return {"valid": True}


def verify_graph(graph: dict):
    if "nodes" not in graph:
        return {"valid": False, "reason": "missing nodes"}

    for node in graph["nodes"]:
        if "type" not in node:
            return {"valid": False, "reason": "node missing type"}

    return {"valid": True}


def system_verify(payload, context):
    if "graph" in payload:
        return verify_graph(payload["graph"])

    return verify_intent_structure(payload)
