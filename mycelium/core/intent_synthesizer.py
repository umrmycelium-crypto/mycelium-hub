from collections import Counter
from mycelium.core.intent_memory import INTENT_MEMORY


def synthesize_candidates():
    """
    Converts raw unknown inputs into candidate intents.
    """

    counter = Counter()

    for event in INTENT_MEMORY.get_all():
        raw = event["input"].strip()
        if not raw:
            continue

        # crude signal: first word = intent family
        key = raw.split()[0].lower()
        counter[key] += 1

    return [
        {
            "candidate_intent": f"system.auto.{key}",
            "frequency": count,
            "examples": [
                e["input"]
                for e in INTENT_MEMORY.get_all()
                if e["input"].startswith(key)
            ][:3]
        }
        for key, count in counter.items()
        if count >= 2
    ]
