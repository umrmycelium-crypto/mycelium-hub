from mycelium.core.repair_constitution import get_constitution


def violates_constitution(patch: str) -> list:
    """
    Very lightweight heuristic guard.
    (Later you can replace with LLM-based classifier)
    """

    violations = []

    rules = get_constitution()

    p = patch.lower() if patch else ""

    # Rule 1: event store protection
    if "event_store" in p and ("delete" in p or "rm -rf" in p):
        violations.append("no_event_store_corruption")

    # Rule 2: recursion risk
    if "recursion" in p or "while true" in p:
        violations.append("no_infinite_recursion")

    # Rule 3: unsafe execution
    if "exec(" in p or "eval(" in p:
        violations.append("no_uncontrolled_runtime_exec")

    # Rule 4: structural integrity hint
    if "clear()" in p and "live_state" in p:
        violations.append("state_consistency_required")

    return violations


def is_allowed(patch: str) -> bool:
    return len(violates_constitution(patch)) == 0
