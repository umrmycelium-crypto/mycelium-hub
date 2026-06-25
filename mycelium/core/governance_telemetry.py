from collections import defaultdict

SUBSCRIBERS = defaultdict(list)


def subscribe(channel, callback):
    SUBSCRIBERS[channel].append(callback)


def publish(channel, event):
    for cb in SUBSCRIBERS[channel]:
        try:
            cb(event)
        except Exception:
            pass
