
RISK_MAP = {
    "allow_self_modify_kernel": "CRITICAL",
    "allow_auto_registry_changes": "CRITICAL",
    "allow_policy_mutation": "HIGH",
    "min_confidence_to_execute": "MEDIUM",
    "required_simulation": "SAFE"
}


def classify_diff(diff):
    """
    Assign semantic risk levels to changes.
    """

    classifications = []

    for k in diff.get("added", {}):
        classifications.append({
            "field": k,
            "type": "added",
            "risk": RISK_MAP.get(k, "UNKNOWN")
        })

    for k, v in diff.get("removed", {}).items():
        classifications.append({
            "field": k,
            "type": "removed",
            "risk": RISK_MAP.get(k, "UNKNOWN")
        })

    for k, v in diff.get("changed", {}).items():
        classifications.append({
            "field": k,
            "type": "modified",
            "risk": RISK_MAP.get(k, "UNKNOWN"),
            "change": v
        })

    return classifications
