from collections import defaultdict
import time

OUTCOMES = []

STRATEGY_STATS = defaultdict(lambda: {
    "success": 0,
    "fail": 0,
    "score_bias": 0.0
})


def log_outcome(entry):
    entry["timestamp"] = time.time()
    OUTCOMES.append(entry)


def record_result(strategy, success, score):
    stats = STRATEGY_STATS[strategy]

    if success:
        stats["success"] += 1
        stats["score_bias"] += 0.02
    else:
        stats["fail"] += 1
        stats["score_bias"] -= 0.03


def get_strategy_bias(strategy):
    return STRATEGY_STATS[strategy]["score_bias"]


def get_memory():
    return OUTCOMES[-100:]
