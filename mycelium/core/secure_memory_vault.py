import hashlib
from time import time


VAULT = {}
ACCESS_LOG = []


def _hash_identity(identity: str):
    return hashlib.sha256(identity.encode()).hexdigest()


def store_personal_context(identity: str, data: dict, permissions: dict):
    """
    Stores encrypted-scoped context.
    """

    key = _hash_identity(identity)

    VAULT[key] = {
        "data": data,
        "permissions": permissions,
        "created_at": time()
    }

    return {
        "status": "STORED",
        "key": key
    }


def retrieve_context(identity: str, requester: str, intent: str):
    """
    Permission-gated retrieval only.
    """

    key = _hash_identity(identity)

    entry = VAULT.get(key)
    if not entry:
        return None

    ACCESS_LOG.append({
        "identity": key,
        "requester": requester,
        "intent": intent,
        "time": time()
    })

    # basic permission gate
    if entry["permissions"].get(intent) is True:
        return entry["data"]

    return {
        "status": "DENIED",
        "reason": "intent not permitted"
    }


def system_vault_status(payload, context):
    return {
        "stored_entities": len(VAULT),
        "access_events": len(ACCESS_LOG)
    }
