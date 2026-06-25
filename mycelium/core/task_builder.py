import uuid
from mycelium.core.task_contract import TaskContract


def build_task(intent: dict) -> TaskContract:
    """
    Convert raw intent → structured execution contract
    """

    return TaskContract(
        task_id=str(uuid.uuid4()),
        intent=intent.get("name"),
        payload=intent.get("payload", {}),
        context=intent.get("context", {}),

        constraints={
            "safe_mode": True,
            "allow_side_effects": True
        },

        tools_allowed=[
            intent.get("name")  # minimal gating for v1
        ]
    )
