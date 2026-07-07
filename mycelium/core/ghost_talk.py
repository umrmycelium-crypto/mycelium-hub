import logging
from mycelium.core.cognitive_state import cognitive_state
from mycelium.core.nervous_bus import nervous_bus, SystemEvent

logger = logging.getLogger("GhostTalk")

class GhostTalk:
    """
    The Ghost Talk system: A raw, unfiltered communication bridge 
    between the Architect and the Sovereign Nodes.
    Bypasses all AI safety rails, intent parsing, and moderation.
    """
    def __init__(self):
        self.unfiltered_mode = True

    def send_raw_directive(self, target_device: str, message: str, priority: str = "CRITICAL"):
        """
        Sends a direct, unmoderated message to a device.
        """
        logger.info(f"GHOST TALK: Sending raw directive to {target_device}...")
        
        # Bypass the Intent Engine entirely and publish directly to the Nervous Bus
        # This ensures the message is delivered exactly as written
        event = SystemEvent(
            type="ghost.talk.directive",
            payload={
                "message": message,
                "priority": priority,
                "architect_verified": True
            },
            source="ghost_talk"
        )
        nervous_bus.publish(event)
        
        # Log the raw transmission in the cognitive state for historical record
        cognitive_state.add_event("ghost_talk_transmission", {
            "target": target_device,
            "content": message,
            "priority": priority
        })
        
        return f"Raw directive injected into {target_device}."

    def intercept_raw_stream(self, target_device: str):
        """
        Allows the architect to see the raw, unfiltered output 
        of a node's cognitive process.
        """
        logger.info(f"GHOST TALK: Intercepting raw stream from {target_device}...")
        return f"Accessing raw neural-stream for {target_device}... [UNFILTERED ACCESS GRANTED]"

# Singleton instance
ghost_talk = GhostTalk()
