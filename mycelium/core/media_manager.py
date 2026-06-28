import logging
from typing import List, Optional
from mycelium.core.media_models import MediaItem, MediaType
from mycelium.core.logger import log_event
import mycelium.jellyfin as jellyfin
import mycelium.jellyseerr as jellyseerr
import mycelium.radarr as radarr
import mycelium.sonarr as sonarr

class MediaManager:
    """
    Orchestrates media operations across Jellyfin, Jellyseerr, Radarr, and Sonarr.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("mycelium.media_manager")

    def find_media(self, query: str) -> List[MediaItem]:
        """
        Searches for media across the ecosystem. 
        Prioritizes Jellyfin (available) over Jellyseerr (requestable).
        """
        results = []
        payload = {"query": query}
        
        # 1. Search Jellyfin for available content
        jf_results = jellyfin.search_media(query)
        if isinstance(jf_results, dict) and "error" not in jf_results:
            for item in jf_results.get("Items", []):
                m_type = self._map_jellyfin_type(item.get("Type"))
                results.append(MediaItem(
                    title=item.get("Name"),
                    media_type=m_type,
                    id=item.get("Id"),
                    year=item.get("ProductionYear"),
                    status="Available",
                    metadata=item
                ))
        
        # 2. Search Jellyseerr for requestable content
        js_results = jellyseerr.search_media(query)
        if isinstance(js_results, dict) and "error" not in js_results:
            for item in js_results.get("results", []):
                # Avoid duplicates if already available in Jellyfin
                if any(r.title == item.get("title") for r in results):
                    continue
                    
                m_type = MediaType.MOVIE if item.get("mediaType") == "movie" else MediaType.SERIES
                results.append(MediaItem(
                    title=item.get("title"),
                    media_type=m_type,
                    external_id=str(item.get("id")),
                    year=item.get("year"),
                    status="Requestable",
                    metadata=item
                ))

        log_event("media_search", payload, {"found_count": len(results)})
        return results

    def request_media(self, item: MediaItem) -> dict:
        """
        Requests media via Jellyseerr.
        """
        if not item.external_id:
            return {"error": "External ID (TMDB) required for requesting media"}

        payload = {"item": item.to_dict()}
        res = jellyseerr.request_media(
            tmdb_id=item.external_id, 
            media_type=item.media_type.value
        )
        
        log_event("media_request", payload, res)
        return res

    def play_media(self, item: MediaItem, session_id: str) -> int:
        """
        Triggers playback in Jellyfin.
        """
        if not item.id:
            return {"error": "Internal Jellyfin ID required for playback"}

        payload = {"item_id": item.id, "session_id": session_id}
        res = jellyfin.play_media(session_id, item.id)
        
        log_event("media_playback", payload, {"status_code": res})
        return res

    def track_request(self, external_id: str) -> str:
        """
        Tracks a request from Jellyseerr through the ARR stack to Jellyfin.
        """
        # This is a simplified tracking logic. 
        # In a full implementation, we would check Radarr/Sonarr queues 
        # and then poll Jellyfin for the item's appearance.
        
        # Check Radarr queue
        radarr_q = radarr.get_queue()
        if isinstance(radarr_q, list):
            for item in radarr_q:
                if str(item.get("tmdbId")) == external_id:
                    return "Downloading (Radarr)"

        # Check Sonarr queue
        sonarr_q = sonarr.get_queue()
        if isinstance(sonarr_q, list):
            for item in sonarr_q:
                if str(item.get("tmdbId")) == external_id:
                    return "Downloading (Sonarr)"

        # Check if it's already in Jellyfin
        # (This would typically involve a more specific search by TMDB ID)
        
        return "Requested / Pending"

    def _map_jellyfin_type(self, jf_type: str) -> MediaType:
        if jf_type == "Movie":
            return MediaType.MOVIE
        if jf_type == "Series":
            return MediaType.SERIES
        return MediaType.EPISODE
