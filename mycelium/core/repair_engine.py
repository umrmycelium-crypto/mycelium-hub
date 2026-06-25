from mycelium.core.repair_patch import Patch
from mycelium.core.repair_scoring import score_patch
from mycelium.core.repair_ledger import log_repair
from mycelium.core.repair_memory import record_result, log_outcome


def analyze_failure(failure):
    return {"status": "analyzed", "failure": failure}


def propose_patch(failure, suggestion):
    patch = Patch(
        target=failure.get("intent"),
        change=suggestion,
        reason="repair loop"
    )

    score = score_patch(patch, failure)

    return patch, score


def finalize_result(strategy, patch, score, result):
    """
    Learning signal ingestion
    """

    success = result.get("status") == "applied"

    record_result(strategy, success, score)

    log_outcome({
        "strategy": strategy,
        "success": success,
        "score": score,
        "patch": patch.to_dict()
    })
