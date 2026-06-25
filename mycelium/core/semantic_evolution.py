from mycelium.core.proposal_ledger import submit_proposal


PATTERN_MAP = {
    "what is": "knowledge.query",
    "explain": "knowledge.query",
    "show me": "visual.query",
    "run": "system.execute"
}


def infer_intent(raw_text: str):
    raw = raw_text.lower()

    for pattern, intent_name in PATTERN_MAP.items():
        if raw.startswith(pattern):
            return intent_name

    return "system.unknown"


def evolve_language(events):
    """
    Learns new mappings (proposal-only, never auto-applied)
    """

    suggestions = []

    for e in events[-100:]:
        payload = e.get("payload", {})
        raw = payload.get("raw")

        if not raw:
            continue

        if "unknown" in str(e.get("intent", "")):
            inferred = infer_intent(raw)

            suggestions.append({
                "name": f"semantic.{inferred}",
                "intent_schema": {
                    "name": inferred,
                    "payload": {"raw": raw},
                    "context": {}
                },
                "reason": "semantic pattern detection",
                "confidence": 0.4,
                "risk": "low",
                "handler": None
            })

    return [submit_proposal(s) for s in suggestions]
