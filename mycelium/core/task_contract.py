from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TaskContract:
    """
    Unified execution unit for Mycelium Agent.
    This replaces ad-hoc dict passing with a structured contract.
    """

    task_id: str
    intent: str

    payload: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)

    constraints: Dict[str, Any] = field(default_factory=dict)

    tools_allowed: List[str] = field(default_factory=list)

    expected_output: Optional[Dict[str, Any]] = None

    status: str = "PENDING"
