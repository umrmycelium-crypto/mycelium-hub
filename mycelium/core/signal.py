from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import time


@dataclass
class Signal:
    source: str
    type: str
    payload: Dict[str, Any]
    context: Dict[str, Any] = field(default_factory=dict)
    trace_id: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
