"""
Context source loaders for the Mycelium Context Compiler.

Each loader returns raw content (str). The compiler is responsible
for ordering, budgeting, and compression. Loaders are pure I/O
and never truncate.
"""
import json
from dataclasses import dataclass
from pathlib import Path

# Source paths — single source of truth, mirrors docs/CURRENT_STATE.md
SYSTEM_CONTEXT_PATH = Path("docs/SYSTEM_CONTEXT.md")
CURRENT_STATE_PATH = Path("docs/CURRENT_STATE.md")
INTENT_MEMORY_PATH = Path("mycelium/memory/intent_memory.json")
EVENT_LOG_PATH = Path("mycelium/logs/event_log.jsonl")
ARCHITECTURE_PATH = Path("docs/ARCHITECTURE.md")
DECISIONS_PATH = Path("docs/DECISIONS.md")
DEPLOYMENT_PATH = Path("docs/DEPLOYMENT.md")
ROADMAP_PATH = Path("docs/ROADMAP.md")
SERVICES_PATH = Path("docs/SERVICES.md")
GEMINI_INSTRUCTIONS_PATH = Path("docs/GEMINI_INSTRUCTIONS.md")


@dataclass
class ContextBundle:
    """Raw, uncompressed context layers. Order matters — see compiler."""
    system: str        # [0] Identity + contract
    state: str         # [1] Current system state
    architecture: str  # [1.5] System architecture reference
    memory: str        # [2] Long-term behavioral memory
    events: str        # [3] Recent event trace
    query: str         # [4] User input (always preserved)


def _read_or_empty(path: Path) -> str:
    """Read a file or return empty string. Never raises."""
    try:
        if path.exists():
            return path.read_text(encoding="utf-8")
    except Exception:
        pass
    return ""


def load_system_context() -> str:
    """Layer 0: system contract and identity."""
    return _read_or_empty(SYSTEM_CONTEXT_PATH)


def load_state() -> str:
    """Layer 1: current runtime state of all services."""
    return _read_or_empty(CURRENT_STATE_PATH)


def load_architecture() -> str:
    """Layer 1.5: architecture reference for system reasoning."""
    return _read_or_empty(ARCHITECTURE_PATH)


def load_memory() -> str:
    """Layer 2: long-term behavioral memory (JSON, pretty-printed)."""
    raw = _read_or_empty(INTENT_MEMORY_PATH)
    if not raw:
        return ""
    try:
        parsed = json.loads(raw)
        return json.dumps(parsed, indent=2)
    except json.JSONDecodeError:
        return raw


def load_events(limit: int = 50) -> str:
    """Layer 3: recent event log entries (newest N)."""
    if not EVENT_LOG_PATH.exists():
        return ""
    try:
        lines = EVENT_LOG_PATH.read_text(encoding="utf-8").splitlines()
        return "\n".join(lines[-limit:])
    except Exception:
        return ""


def load_all(query: str, event_limit: int = 50) -> ContextBundle:
    """Single-call loader for the full context bundle."""
    return ContextBundle(
        system=load_system_context(),
        state=load_state(),
        architecture=load_architecture(),
        memory=load_memory(),
        events=load_events(limit=event_limit),
        query=query or "",
    )
