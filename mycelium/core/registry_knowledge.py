from mycelium.core.reasoning import emit_reason


def knowledge_query(payload, context):
    emit_reason({"intent": "knowledge.query"}, "execute")

    query = payload.get("query", "")

    return {
        "status": "OK",
        "type": "knowledge.response",
        "query": query,
        "response": f"[simulated knowledge engine] received: {query}"
    }
