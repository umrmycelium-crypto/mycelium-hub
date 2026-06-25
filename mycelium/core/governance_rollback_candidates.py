from mycelium.core.constitution_store import CONSTITUTION_HISTORY


def get_recent_versions(limit=5):
    return CONSTITUTION_HISTORY[-limit:]


def list_candidates(limit=5):
    history = get_recent_versions(limit)

    candidates = []

    for i, entry in enumerate(history):
        candidates.append({
            "index": len(CONSTITUTION_HISTORY) - len(history) + i,
            "version": entry["constitution"]["version"],
            "reason": entry.get("reason", "unknown"),
            "timestamp": entry["timestamp"]
        })

    return candidates
