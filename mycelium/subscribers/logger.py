from mycelium.core.logger import log_event

def handle_log(event_type, payload, results):
    """
    Subscriber handler for global event logging.
    """
    return log_event(event_type, payload, results)
