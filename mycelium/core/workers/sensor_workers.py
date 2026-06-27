from mycelium.core.event_bus import EVENT_BUS
from mycelium.core.events import SENSOR_PULSE

# -----------------------------------------------------------------------------
# SENSOR STATE (The "nervous system" activity levels)
# -----------------------------------------------------------------------------

SENSOR_ACTIVITY = {
    "audio": 1.0,
    "video": 1.0,
}

# -----------------------------------------------------------------------------
# THE WORKERS ("Sensory Organs")
# -----------------------------------------------------------------------------

def audio_sensor_worker(event):
    """
    Job: React to sound-related activity.
    Trigger: Any event related to voice or audio.
    """
    event_name = event.get("type", "")
    if "voice" in event_name or "audio" in event_name:
        SENSOR_ACTIVITY["audio"] += 0.2
        # Cap the pulse to prevent runaway values
        SENSOR_ACTIVITY["audio"] = min(3.0, SENSOR_ACTIVITY["audio"])
        
        EVENT_BUS.publish({
            "type": SENSOR_PULSE,
            "payload": {"sensor": "audio", "strength": SENSOR_ACTIVITY["audio"]}
        })

def video_sensor_worker(event):
    """
    Job: React to vision or media-related activity.
    Trigger: Any event related to vision or media.
    """
    event_name = event.get("type", "")
    if "vision" in event_name or "media" in event_name:
        SENSOR_ACTIVITY["video"] += 0.2
        # Cap the pulse to prevent runaway values
        SENSOR_ACTIVITY["video"] = min(3.0, SENSOR_ACTIVITY["video"])

        EVENT_BUS.publish({
            "type": SENSOR_PULSE,
            "payload": {"sensor": "video", "strength": SENSOR_ACTIVITY["video"]}
        })

def decay_worker(event):
    """
    Job: Slowly return sensor activity to baseline.
    Trigger: Periodically (this is a bit hacky in a pure event-driven system, 
    but we'll simulate it by reacting to ANY event or a dedicated timer).
    """
    # In a true async system, this would be a background loop.
    # For now, we'll decay slightly on every event to simulate time passing.
    for key in SENSOR_ACTIVITY:
        SENSOR_ACTIVITY[key] = max(1.0, SENSOR_ACTIVITY[key] - 0.01)

def bootstrap_sensor_workers():
    """
    Connects the sensory organs to the nervous system.
    """
    # We subscribe to ALL events to allow the decay_worker to work 
    # and to allow specific sensors to pick what they care about.
    
    # Note: EVENT_BUS.subscribe(fn) calls fn for EVERY event.
    
    # We'll use a more surgical approach if possible, but for now:
    EVENT_BUS.subscribe(audio_sensor_worker)
    EVENT_BUS.subscribe(video_sensor_worker)
    EVENT_BUS.subscribe(decay_worker)
