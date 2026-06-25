from mycelium.core.constitution_store import CONSTITUTION_HISTORY
from mycelium.core.constitution_diff_engine import diff_constitutions
from mycelium.core.constitution_diff_classifier import classify_diff
from mycelium.core.constitution_diff_explainer import explain_diff


def explain_version_change(old_index, new_index):
    history = CONSTITUTION_HISTORY

    if old_index >= len(history) or new_index >= len(history):
        return {"status": "error", "reason": "invalid_index"}

    old = history[old_index]["constitution"]
    new = history[new_index]["constitution"]

    diff = diff_constitutions(old, new)
    classified = classify_diff(diff)
    explanation = explain_diff(diff, classified)

    return {
        "from_version": old_index,
        "to_version": new_index,
        "diff": diff,
        "analysis": explanation
    }
