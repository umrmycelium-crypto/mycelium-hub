from mycelium.core.repair_loop import generate_patch

# -----------------------------
# Repair Strategies
# -----------------------------

def strategy_minimal(drift):
    """
    Conservative: smallest possible fix
    """
    prompt = f"""
You are a conservative system repair agent.
Only make the smallest possible change to fix drift.

DRIFT:
{drift}
"""
    return generate_patch(prompt)


def strategy_structural(drift):
    """
    Structural: prefers architecture-level fixes
    """
    prompt = f"""
You are a structural repair agent.
Focus on system architecture and root cause fixes.

DRIFT:
{drift}
"""
    return generate_patch(prompt)


def strategy_replay_alignment(drift):
    """
    Replay-driven: tries to align live state to replay state
    """
    prompt = f"""
You are a replay alignment agent.
Make live state match replay state exactly.

DRIFT:
{drift}
"""
    return generate_patch(prompt)


def strategy_exploratory(drift):
    """
    Experimental: allows broader changes
    """
    prompt = f"""
You are an exploratory repair agent.
You may refactor or restructure if it improves consistency.

DRIFT:
{drift}
"""
    return generate_patch(prompt)


STRATEGIES = {
    "minimal": strategy_minimal,
    "structural": strategy_structural,
    "replay": strategy_replay_alignment,
    "exploratory": strategy_exploratory,
}
