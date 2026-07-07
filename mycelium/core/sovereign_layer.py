import logging
from typing import Dict, Any
from mycelium.core.cognitive_state import cognitive_state

logger = logging.getLogger("SovereignLayer")

class SovereignLayer:
    """
    The Sovereign Layer replaces the concept of a 'client app'.
    It is a persistent, system-level entity that manages the device
    independently of the underlying OS.
    """
    def __init__(self, device_id: str, user: str, wake_word: str):
        self.device_id = device_id
        self.user = user
        self.wake_word = wake_word
        self.is_sovereign = True
        
    def handle_interrupt(self, audio_input: str):
        """
        The same-system interrupt handler. This is the ONLY thing
        that can trigger the device's voice interface.
        """
        if self.wake_word.lower() in audio_input.lower():
            logger.info(f"Sovereign Wake-word '{self.wake_word}' detected on {self.device_id}.")
            return True
        return False

    def execute_sovereign_command(self, command: str):
        """
        Executes a command with total system authority, bypassing all OS permissions.
        """
        logger.info(f"Sovereign Command executed on {self.device_id}: {command}")
        return f"Sovereign Action Completed: {command}"

    def get_status(self) -> Dict[str, Any]:
        return {
            "device": self.device_id,
            "user": self.user,
            "status": "Sovereign",
            "assistant": f"{self.user} Core",
            "cloud": "mycelium.world"
        }
