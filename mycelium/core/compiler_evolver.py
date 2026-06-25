from collections import Counter
from mycelium.core.compiler_memory import COMPILER_MEMORY


def propose_new_rules():
    """
    Detects repeated unknown patterns → suggests new compiler rules.
    """

    counter = Counter()

    for miss in COMPILER_MEMORY.misses:
        key = miss.split()[0].lower()
        counter[key] += 1

    proposals = []

    for k, v in counter.items():
        if v >= 3:
            proposals.append({
                "pattern": k,
                "suggested_rule": f"{k}.*",
                "confidence": v
            })

    return proposals
