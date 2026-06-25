import time
from mycelium.core.event_bus import EVENT_BUS
from mycelium.runtime.jellyfin import search_media, add_to_library


def start_acquisition_worker(poll_interval=2):
    """
    Background loop that reacts to acquisition.requested events.
    """

    print("[acquisition-worker] started")

    while True:
        events = EVENT_BUS.subscribers  # (we will improve later)
        time.sleep(poll_interval)
