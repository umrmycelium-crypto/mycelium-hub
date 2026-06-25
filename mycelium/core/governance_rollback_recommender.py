from mycelium.core.governance_rollback_candidates import list_candidates
from mycelium.core.governance_rollback_risk import compute_risk_trend
from mycelium.core.governance_anomaly_detector import detect_anomalies


def recommend_rollback():
    candidates = list_candidates()
    risk = compute_risk_trend()
    anomalies = detect_anomalies()

    recommendations = []

    # ----------------------------------
    # RULE 1: system unstable → suggest rollback
    # ----------------------------------
    if risk["trend"] == "degrading":
        recommendations.append({
            "type": "global_recommendation",
            "action": "rollback_latest",
            "reason": "system health degrading"
        })

    # ----------------------------------
    # RULE 2: high anomaly load → suggest rollback
    # ----------------------------------
    if len(anomalies["anomalies"]) > 2:
        recommendations.append({
            "type": "anomaly_based",
            "action": "review_recent_changes",
            "reason": "multiple governance anomalies detected"
        })

    # ----------------------------------
    # RULE 3: provide safest rollback target
    # ----------------------------------
    if candidates:
        recommendations.append({
            "type": "candidate_suggestion",
            "recommended_index": candidates[-2]["index"] if len(candidates) > 1 else candidates[0]["index"],
            "reason": "last stable known configuration"
        })

    return {
        "risk": risk,
        "candidates": candidates,
        "anomalies": anomalies,
        "recommendations": recommendations
    }
