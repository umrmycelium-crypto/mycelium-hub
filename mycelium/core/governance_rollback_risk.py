from mycelium.core.governance_anomaly_pipeline import analyze_governance_health


def compute_risk_trend():
    """
    Simple heuristic: compare current health score to threshold bands.
    """

    health = analyze_governance_health()

    score = health["score"]

    if score < 40:
        trend = "degrading"
    elif score < 70:
        trend = "unstable"
    else:
        trend = "stable"

    return {
        "health_score": score,
        "trend": trend
    }
