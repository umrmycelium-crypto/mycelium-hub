"""
Intent Convergence Layer v1

Turns raw or weak intents into stronger semantic intents.
"""

class IntentConvergence:

    @staticmethod
    def refine(intent: dict) -> dict:
        name = intent.get("name", "")
        payload = intent.get("payload", {})

        # -------------------------
        # AI semantic expansion
        # -------------------------
        if name == "system.unknown":
            raw = payload.get("raw", "").lower()

            # simple convergence heuristics (v1)
            if any(x in raw for x in ["explain", "what is", "how does", "define"]):
                return {
                    "name": "knowledge.query",
                    "payload": {
                        "query": raw
                    },
                    "context": intent.get("context", {})
                }

        # default passthrough
        return intent
