from mycelium.core.event_bus import EVENT_BUS
from mycelium.core.events import PRESENCE_DETECTED, PRESENCE_LOST, DEVICE_STATUS_CHANGED

# -----------------------------------------------------------------------------
# DEVICE CONFIGURATION
# -----------------------------------------------------------------------------

# These would ideally be moved to a config file or DB later
WATCHED_DEVICES = {
    "iphone": {
        "type": "bluetooth",
        "label": "User's iPhone",
        "priority": 3,
    },
    "samsung_tv": {
        "type": "network",
        "label": "Samsung Smart TV",
        "priority": 4,
        "ip": "10.0.0.X", # Placeholder
    },
    "headphones": {
        "type": "bluetooth",
        "label": "MX Headphones",
        "priority": 2,
    }
}

# -----------------------------------------------------------------------------
# THE WORKERS ("Presence Observers")
# -----------------------------------------------------------------------------

def presence_observer_worker(event):
    """
    Job: Monitor the status of watched devices.
    Trigger: Periodic scan (simulated here by reacting to any event)
    """
    # In a real implementation, this would be a background loop/timer
    # For now, we'll simulate device detection logic.
    
    # This is a placeholder for the actual discovery logic (e.g. nmap, bluetoothctl, etc.)
    pass

def device_status_manager(event):
    """
    Job: Maintain the current state of all devices.
    Trigger: PRESENCE_DETECTED, PRESENCE_LOST, DEVICE_STATUS_CHANGED
    """
    # Logic to handle state transitions and notify the Priority Engine
    pass

def bootstrap_presence_workers():
    """
    Sits the presence observers at the table.
    """
    # We'll subscribe these in the next phase once we have real scanning logic
    pass
