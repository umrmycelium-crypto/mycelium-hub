from collections import defaultdict
from mycelium.core.intent_memory import INTENT_MEMORY


def suggest_intents():
    """
    Groups similar unknown inputs (v1 heuristic).
    """

    buckets = defaultdict(list)

    for event in INTENT_MEMORY.get_all():
        words = event["input"].split()
        if not words:
            continue

        key = words[0]  # naive clustering by first token
        buckets[key].append(event["input"])

    return {
        k: v[:5]  # sample only
        for k, v in buckets.items()
        if len(v) > 1
    }
