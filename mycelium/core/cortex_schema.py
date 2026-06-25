from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class CortexDecision:
    allow: bool
    signals: List[Dict[str, Any]] = field(default_factory=list)
    reasoning: str = ""
    modified_intent: Dict[str, Any] = field(default_factory=dict)
