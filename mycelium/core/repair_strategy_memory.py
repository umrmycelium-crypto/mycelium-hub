def label_strategy(failure):
    """
    Deterministic strategy classifier.
    """

    intent = failure.get("intent", "")

    if "system" in intent:
        return "system_fix"

    if "ai" in intent:
        return "ai_fix"

    return "generic_fix"
