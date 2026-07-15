import subprocess
import os
from typing import Any, Dict, Optional

class SystemTool:
    """
    Provides the Executive Agent with capabilities to control the local 
    system environment (audio, volume, apps, and network).
    """
    def __init__(self):
        pass

    def set_volume(self, level: int) -> str:
        """
        Sets the system volume. 
        Args: {level: int} (0-100)
        """
        try:
            # Use amixer or pactl depending on the system. 
            # Assuming PulseAudio/PipeWire based on previous pactl usage.
            level_percent = f"{level}%"
            subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", level_percent], check=True)
            return f"System volume set to {level}%."
        except Exception as e:
            return f"Error setting volume: {str(e)}"

    def mute_system(self, mute: bool) -> str:
        """
        Mutes or unmutes the system audio.
        Args: {mute: bool}
        """
        try:
            state = "mute" if mute else "unmute"
            subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", state], check=True)
            return f"System audio {state}d."
        except Exception as e:
            return f"Error changing mute state: {str(e)}"

    def launch_app(self, app_name: str) -> str:
        """
        Attempts to launch a specified application.
        Args: {app_name: str}
        """
        try:
            # Simple launch via shell. In a real scenario, this might be more complex.
            subprocess.Popen([app_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"Attempted to launch {app_name}."
        except Exception as e:
            return f"Error launching {app_name}: {str(e)}"

    def get_network_status(self) -> Dict[str, Any]:
        """
        Checks the current network connectivity.
        """
        try:
            # Check if we can ping a reliable server
            result = subprocess.run(["ping", "-c", "1", "8.8.8.8"], capture_output=True)
            return {
                "online": result.returncode == 0,
                "latency": "low" if result.returncode == 0 else "N/A"
            }
        except Exception as e:
            return {"error": str(e)}
