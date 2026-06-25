
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Intent:
    name: str
    confidence: float
    payload: Dict[str, Any]
    context: Dict[str, Any]
