from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any

class MediaType(Enum):
    MOVIE = "movie"
    SERIES = "series"
    EPISODE = "episode"

@dataclass
class MediaItem:
    title: str
    media_type: MediaType
    id: Optional[str] = None  # Internal ID (e.g., Jellyfin ID)
    external_id: Optional[str] = None  # External ID (e.g., TMDB ID)
    year: Optional[int] = None
    status: Optional[str] = None  # e.g., "Available", "Requested", "Downloading"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "title": self.title,
            "media_type": self.media_type.value,
            "id": self.id,
            "external_id": self.external_id,
            "year": self.year,
            "status": self.status,
            "metadata": self.metadata
        }
