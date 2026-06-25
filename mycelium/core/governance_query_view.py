from mycelium.core.governance_query_parser import parse_query
from mycelium.core.governance_query_engine import run_query


def ask(query: str):
    parsed = parse_query(query)
    results = run_query(parsed)

    return {
        "query": query,
        "type": parsed["type"],
        "results": results
    }
