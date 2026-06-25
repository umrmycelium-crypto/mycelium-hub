def compute_safety_score(risk_analysis):
    """
    Convert risk classification into a simple safety score.
    """

    score = 100

    for item in risk_analysis:
        risk = item.get("risk")

        if risk == "CRITICAL":
            score -= 40
        elif risk == "HIGH":
            score -= 20
        elif risk == "MEDIUM":
            score -= 10
        elif risk == "UNKNOWN":
            score -= 5

    return max(0, score)
