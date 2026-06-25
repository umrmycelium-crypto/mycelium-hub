from mycelium.core.ai_backend import ai_generate


def knowledge_query(payload, context):
    query = payload.get("query", "")

    response = ai_generate(
        f"Explain clearly and concisely: {query}",
        context
    )

    return {
        "status": "OK",
        "type": "ai.knowledge",
        "query": query,
        "response": response
    }
