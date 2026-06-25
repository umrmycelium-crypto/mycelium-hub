from mycelium.core.governance_anomaly_detector import detect_anomalies
from mycelium.core.governance_anomaly_score import score_anomalies


def analyze_governance_health(window_seconds=3600):
    result = detect_anomalies(window_seconds)

    score = score_anomalies(result)

    if score > 80:
        status = "STABLE"
    elif score > 50:
        status = "WATCH"
    else:
        status = "UNSTABLE"

    return {
        "score": score,
        "status": status,
        "details": result
    }
