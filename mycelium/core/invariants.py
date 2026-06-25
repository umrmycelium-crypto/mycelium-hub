"""
Mycelium System Invariants v1

These rules define execution safety and structural correctness.
They are consumed by governance + repair systems.
"""

INVARIANTS = [
    {
        "id": "intent.dict.only",
        "description": "All runtime intents must be dict-based",
        "rule": "isinstance(intent, dict) and 'name' in intent"
    },
    {
        "id": "no.object.intent",
        "description": "No .intent attribute access allowed in runtime path",
        "rule": "block_access('intent.intent')"
    },
    {
        "id": "registry.contract",
        "description": "All handlers must accept (payload, context)",
        "rule": "fn(payload, context)"
    }
]
