from mycelium.core.repair_memory import get_strategy_bias

def adaptive_score(base_score, strategy):
    """
    Self-improving scoring function (safe learning)
    """

    bias = get_strategy_bias(strategy)

    score = base_score + bias

    # clamp
    return max(0.0, min(1.0, score))
