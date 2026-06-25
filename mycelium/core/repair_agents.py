from mycelium.core.repair_patch import Patch


def agent_fast(failure):
    return Patch(
        target=failure.get("intent"),
        change="fast heuristic fix",
        reason="fast_agent"
    )


def agent_safe(failure):
    return Patch(
        target=failure.get("intent"),
        change="conservative safe fix",
        reason="safe_agent"
    )


def agent_ai(failure, ai_generate):
    suggestion = ai_generate(failure)

    return Patch(
        target=failure.get("intent"),
        change=suggestion,
        reason="ai_agent"
    )


AGENTS = {
    "fast": agent_fast,
    "safe": agent_safe,
    "ai": agent_ai
}
