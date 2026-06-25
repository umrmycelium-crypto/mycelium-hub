from mycelium.core.repair_engine import propose_patch
from mycelium.core.repair_simulator import simulate_patch
from mycelium.core.repair_policy import allow_patch
from mycelium.core.repair_scoring import score_patch
from mycelium.core.repair_prompt_learning import adaptive_score
from mycelium.core.repair_strategy_memory import label_strategy
from mycelium.core.repair_engine import finalize_result


def bounded_repair_loop(failure, suggestion):
    patch, base_score = propose_patch(failure, suggestion)

    strategy = label_strategy(failure)

    simulation = simulate_patch(patch)
    policy_ok = allow_patch(patch, simulation)

    score = adaptive_score(base_score, strategy)

    decision = {
        "patch": patch.to_dict(),
        "strategy": strategy,
        "score": score,
        "simulation": simulation,
        "policy_ok": policy_ok
    }

    if score >= 0.75 and policy_ok:
        result = {"status": "applied"}
        decision["executed"] = True
        decision["result"] = result

        finalize_result(strategy, patch, score, result)
    else:
        result = {"status": "rejected"}
        decision["executed"] = False
        decision["result"] = result

        finalize_result(strategy, patch, score, result)

    return decision
