from mycelium.knowledge import search_notes


def knowledge_handler(payload, context):
    """
    Handles knowledge-related intents by searching the Obsidian vault.
    """
    query = payload.get("query") or payload.get("text") or "unknown"

    results = search_notes(query)

    if isinstance(results, dict) and "error" in results:
        return {
            "status": "ERROR",
            "action": "knowledge.search",
            "message": results["error"]
        }

    return {
        "status": "OK",
        "action": "knowledge.search",
        "query": query,
        "results": results,
        "count": len(results)
    }
