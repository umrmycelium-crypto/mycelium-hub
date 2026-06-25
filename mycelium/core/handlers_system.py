from mycelium.core.registry_decorator import register


# ----------------------------------
# BASIC SYSTEM HANDLERS
# ----------------------------------

@register("system.ping")
def system_ping(payload, context):
    return {
        "status": "OK",
        "message": "pong",
        "layer": "runtime"
    }


@register("system.status")
def system_status(payload, context):
    return {
        "status": "OK",
        "layer": "kernel"
    }


# ----------------------------------
# CONSTITUTION HANDLERS
# ----------------------------------

@register("system.constitution.current")
def constitution_current(payload, context):
    from mycelium.core.constitution_store import get_constitution
    return get_constitution()


@register("system.constitution.history")
def constitution_history(payload, context):
    from mycelium.core.constitution_store import history
    return history()


@register("system.constitution.audit")
def constitution_audit(payload, context):
    from mycelium.core.constitution_audit import get_audit
    return get_audit()


@register("system.constitution.rollback")
def constitution_rollback(payload, context):
    from mycelium.core.constitution_rollback import rollback

    version = payload.get("version")

    if version is None:
        return {
            "status": "ERROR",
            "message": "version required"
        }

    try:
        result = rollback(version)

        return {
            "status": "OK",
            "constitution": result
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }


from mycelium.core.registry_decorator import register
from mycelium.core.constitution_mutation import propose_mutation
from mycelium.core.constitution_mutation_pipeline import run_mutation_pipeline


@register("system.constitution.propose")
def constitution_propose(payload, context):
    return propose_mutation(
        payload.get("change", {}),
        payload.get("reason", "cli")
    )


@register("system.constitution.mutate")
def constitution_mutate(payload, context):
    return run_mutation_pipeline(
        payload.get("proposal_id")
    )


from mycelium.core.registry_decorator import register
from mycelium.core.constitution_human_override import set_decision
from mycelium.core.constitution_human_resume import resume_with_human_decision


@register("system.constitution.human.decide")
def human_decide(payload, context):
    return set_decision(
        payload.get("request_id"),
        payload.get("decision"),
        payload.get("reason", "")
    )


@register("system.constitution.human.resume")
def human_resume(payload, context):
    return resume_with_human_decision(
        payload.get("request_id")
    )
