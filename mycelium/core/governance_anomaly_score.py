def score_anomalies(result):
    """
    Convert anomaly list into severity score.
    """

    score = 100

    for a in result.get("anomalies", []):
        severity = a["severity"]

        if severity == "HIGH":
            score -= 40
        elif severity == "MEDIUM":
            score -= 20
        elif severity == "LOW":
            score -= 5

    return max(0, score)
