from mycelium.core.repair_agents import AGENTS
from mycelium.core.repair_arbitrator import choose_best
from mycelium.core.repair_simulator import simulate_patch
from mycelium.core.repair_engine import finalize_result
from mycelium.core.repair_governance import govern_repair


def run_multi_strategy_repair(failure, ai_generate=None):
    patches = []

    for name, agent in AGENTS.items():
        if name == "ai" and ai_generate:
            patches.append(agent(failure, ai_generate))
        elif name != "ai":
            patches.append(agent(failure))

    best_score, best_patch = choose_best(patches, failure)

    simulation = simulate_patch(best_patch)

    governance = govern_repair(best_patch, simulation, best_score)

    decision = {
        "patches": [p.to_dict() for p in patches],
        "winner": best_patch.to_dict(),
        "score": best_score,
        "simulation": simulation,
        "governance": governance
    }

    if best_score >= 0.75 and governance["allowed"]:
        result = {"status": "applied"}
        decision["executed"] = True
        decision["result"] = result
        finalize_result("constitutional_multi", best_patch, best_score, result)

    else:
        decision["executed"] = False
        decision["result"] = {"status": "blocked_by_constitution"}
        finalize_result("constitutional_multi", best_patch, best_score, {"status": "blocked"})

    return decision
