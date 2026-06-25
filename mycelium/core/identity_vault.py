from mycelium.core.secure_memory_vault import VAULT
import hashlib
from time import time


IDENTITIES = {}


def register_identity(name: str, metadata: dict = None):
    key = hashlib.sha256(name.encode()).hexdigest()

    IDENTITIES[key] = {
        "name": name,
        "metadata": metadata or {},
        "created_at": time()
    }

    return {"status": "OK", "identity": key}


def list_identities():
    return IDENTITIES


def scoped_store(identity: str, data: dict):
    from mycelium.core.secure_memory_vault import store_personal_context

    return store_personal_context(
        identity=identity,
        data=data,
        permissions={"default": False}
    )


def system_identity_status(payload, context):
    return {
        "identities": len(IDENTITIES),
        "vault_entries": len(VAULT)
    }
