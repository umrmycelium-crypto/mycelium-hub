AGENT_TRUST = {
    "fast": 0.60,
    "safe": 0.90,
    "ai": 0.80
}

MIN_TRUST = 0.25
MAX_TRUST = 1.00

SUCCESS_DELTA = 0.01
FAILURE_DELTA = 0.01


def get_trust(agent):
    return AGENT_TRUST.get(agent, 0.50)


def update_trust(agent, success):
    current = get_trust(agent)

    if success:
        current += SUCCESS_DELTA
    else:
        current -= FAILURE_DELTA

    current = max(MIN_TRUST, min(MAX_TRUST, current))

    AGENT_TRUST[agent] = current

    return current
