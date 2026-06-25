def score_patch(patch, context):
    """
    Deterministic heuristic scoring (NO LLM trust required yet)
    """

    score = 0.5  # baseline

    if "handler" in patch.target:
        score += 0.2

    if "fix" in patch.reason.lower():
        score += 0.1

    if len(str(patch.change)) < 200:
        score += 0.1

    return min(score, 1.0)
