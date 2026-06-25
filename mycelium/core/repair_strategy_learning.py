from collections import defaultdict
from mycelium.core.repair_strategy_memory import load


def rank_strategies():
    logs = load()

    if not logs:
        return None

    scores = defaultdict(list)

    for entry in logs:
        scores[entry["strategy"]].append(entry["score"])

    ranked = [
        (k, sum(v)/len(v))
        for k, v in scores.items()
    ]

    ranked.sort(key=lambda x: x[1], reverse=True)

    return ranked


def pick_strategies():
    """
    Returns ordered strategy list.
    Top strategies get used first.
    """

    ranked = rank_strategies()

    base = ["minimal", "structural", "replay", "exploratory"]

    if not ranked:
        return base

    learned = [k for k, _ in ranked]

    # merge learned + defaults (avoid missing strategies)
    merged = learned + [s for s in base if s not in learned]

    return merged
