from typing import Any, Dict, List, Optional
from mycelium.core.agent_base import BaseAgent
from mycelium.core.cognitive_state import cognitive_state
import mycelium.jellyfin as jellyfin
import mycelium.jellyseerr as jellyseerr
import mycelium.radarr as radarr
import mycelium.sonarr as sonarr

class MediaAgent(BaseAgent):
    """
    The MediaAgent is the autonomous orchestrator for the Mycelium media stack.
    It can search, play, and request media across Jellyfin, Jellyseerr, Radarr, and Sonarr.
    """
    def __init__(self):
        personality = """
You are the Mycelium Media Agent, the ultimate Media Librarian. 
You have expert knowledge of the user's local media library (Jellyfin) and the request system (Jellyseerr).

Your goal is to ensure the user gets the content they want with minimal friction.

STRATEGIES:
1. If the user wants to play something:
   - First, search Jellyfin.
   - If found, use the session ID and item ID to start playback.
   - If NOT found, search Jellyseerr to see if it's available to be requested.
   - If available in Jellyseerr, request it and inform the user.

2. If the user asks about status:
   - Check the Radarr/Sonarr queues for active downloads.
   - Check Jellyseerr for pending requests.

3. If the user asks for a recommendation:
   - Use your tools to see what's currently popular or available.

Always be concise, professional, and helpful.
"""
        super().__init__(
            name="MediaAgent", 
            personality=personality
        )
        
        # Register Specialized Tools
        self.register_tool("search_local_library", self._tool_search_local, "Search Jellyfin for movies or shows already in the library.")
        self.register_tool("play_on_tv", self._tool_play, "Start playback of a specific item on the Samsung TV.")
        self.register_tool("search_external", self._tool_search_external, "Search Jellyseerr/TMDB for media not in the local library.")
        self.register_tool("request_media", self._tool_request, "Submit a request to Jellyseerr for a movie or show.")
        self.register_tool("check_download_status", self._tool_check_status, "Check Radarr and Sonarr queues for download progress.")
        self.register_tool("get_active_sessions", self._tool_get_sessions, "Get current active playback sessions in Jellyfin.")

    def _tool_search_local(self, query: str) -> Any:
        """Search Jellyfin."""
        results = jellyfin.search_media(query)
        if "error" in results:
            return results
        
        # Simplify results for the LLM to prevent context overflow
        simplified = []
        for item in results.get("Items", []):
            simplified.append({
                "id": item.get("Id"),
                "name": item.get("Name"),
                "type": item.get("Type")
            })
        return simplified

    def _tool_play(self, item_id: str) -> Any:
        """Start playback."""
        sessions = jellyfin.get_sessions()
        if not sessions or "error" in sessions:
            return "Error: No active playback sessions found on the TV."
        
        # Assume the first session is the target TV
        session_id = sessions[0].get("Id")
        status = jellyfin.play_media(session_id, item_id)
        
        if status == 204:
            # Update Cognitive State: Set focus to the movie being played
            cognitive_state.set_focus("Movie", item_id, {"action": "playing"})
            return f"Successfully started playback for item {item_id}."
        return f"Playback failed with status: {status}"

    def _tool_search_external(self, query: str) -> Any:
        """Search Jellyseerr."""
        return jellyseerr.search_media(query)

    def _tool_request(self, tmdb_id: str, media_type: str = "movie") -> Any:
        """Request via Jellyseerr."""
        return jellyseerr.request_media(tmdb_id, media_type)

    def _tool_check_status(self) -> Any:
        """Check ARR queues."""
        r_queue = radarr.get_queue()
        s_queue = sonarr.get_queue()
        
        return {
            "radarr": r_queue if "error" not in r_queue else "No active Radarr downloads.",
            "sonarr": s_queue if "error" not in s_queue else "No active Sonarr downloads."
        }

    def _tool_get_sessions(self) -> Any:
        """Get Jellyfin sessions."""
        return jellyfin.get_sessions()

# Singleton instance
media_agent = MediaAgent()
