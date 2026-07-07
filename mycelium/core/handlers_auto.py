from mycelium.core.registry_decorator import register
from mycelium.core.registry_knowledge import knowledge_query

@register("system.auto.explain")
def system_auto_explain(payload, context):
    """
    Handler: resolve 'explain' proposals by delegating to knowledge.query.
    Uses payload.raw or defaults to 'explain event-driven systems'.
    """
    raw = ""
    if isinstance(payload, dict):
        raw = payload.get("raw") or payload.get("query") or ""
    query = (raw or "").strip()

    if not query:
        query = "explain event-driven systems"

    return knowledge_query({"query": query}, context)
