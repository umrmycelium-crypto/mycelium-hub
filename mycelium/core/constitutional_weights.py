"""
Agent trust / influence weights
"""

AGENT_WEIGHTS = {
    "fast": 0.6,
    "safe": 0.9,
    "ai": 0.8
}


def get_weight(agent_name: str):
    return AGENT_WEIGHTS.get(agent_name, 0.5)


def update_weight(agent_name: str, delta: float):
    current = AGENT_WEIGHTS.get(agent_name, 0.5)
    AGENT_WEIGHTS[agent_name] = max(0.1, min(1.0, current + delta))
