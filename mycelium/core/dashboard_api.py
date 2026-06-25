from mycelium.core.execution_trace import get_trace
from mycelium.core.registry_core import get_registry
from mycelium.core.proposal_ledger import list_proposals


def system_dashboard(payload, context):
    return {
        "trace": get_trace(100),
        "registry": list(get_registry().keys()),
        "proposals": list_proposals(),
        "status": "OK"
    }
