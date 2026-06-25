from mycelium.core.repair_scoring import score_patch


def choose_best(patches, failure):
    """
    Deterministic winner selection.
    """

    scored = []

    for p in patches:
        score = score_patch(p, failure)
        scored.append((score, p))

    scored.sort(key=lambda x: x[0], reverse=True)

    return scored[0]  # (best_score, best_patch)
