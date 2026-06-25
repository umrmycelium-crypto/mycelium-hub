def parse_query(q: str):
    q = q.lower().strip()

    if "rollback" in q:
        return {"type": "rollback"}

    if "human" in q:
        return {"type": "human_events"}

    if "risk" in q or "high-risk" in q:
        return {"type": "risk_events"}

    if "drift" in q:
        return {"type": "drift"}

    if "simulation" in q:
        return {"type": "simulation"}

    return {"type": "unknown", "raw": q}
