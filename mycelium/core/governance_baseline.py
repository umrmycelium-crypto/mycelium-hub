from collections import defaultdict
from mycelium.core.governance_events import get_events


BASELINE = defaultdict(int)


def compute_baseline():
    """
    Very simple baseline: total historical averages.
    """

    events = get_events()

    for e in events:
        BASELINE[e["event"]] += 1

    return dict(BASELINE)


def get_baseline():
    return dict(BASELINE)
