from mycelium.core.governance_memory import search_by_tag


def query_memory(tag: str):
    results = search_by_tag(tag)

    return {
        "tag": tag,
        "count": len(results),
        "results": results
    }
