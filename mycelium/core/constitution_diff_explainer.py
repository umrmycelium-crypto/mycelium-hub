

def explain_diff(diff, classifications):
    """
    Converts structural diff into human explanation.
    """

    explanations = []

    for c in classifications:
        field = c["field"]
        risk = c["risk"]

        if c["type"] == "added":
            explanations.append(
                f"➕ New capability added: {field} (risk={risk})"
            )

        elif c["type"] == "removed":
            explanations.append(
                f"➖ Capability removed: {field} (risk={risk})"
            )

        elif c["type"] == "modified":
            change = c.get("change", {})
            explanations.append(
                f"✏️ Modified {field}: {change.get('from')} → {change.get('to')} (risk={risk})"
            )

    return {
        "summary": explanations,
        "risk_profile": classifications
    }
