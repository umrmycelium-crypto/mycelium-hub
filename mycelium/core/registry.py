from mycelium.runtime.media.orchestrator import handle_media_play as media_play_runtime
from mycelium.runtime.ai import ai_ask as ai_ask_runtime

from mycelium.core.event_store import read_events
from mycelium.core.projections import LIVE_STATE
from mycelium.core.replay import replay_state_only
from mycelium.core.reasoning import emit_reason


# =========================================================
# SINGLE SOURCE OF TRUTH REGISTRY (NO OTHER FILE OWNS THIS)
# =========================================================

REGISTRY = {}


def register(name: str):
    def wrapper(fn):
        REGISTRY[name] = fn
        return fn
    return wrapper


# =========================================================
# SYSTEM INTENTS
# =========================================================

@register("system.ping")
def system_ping(payload, context):
    emit_reason({"intent": "system.ping"}, "execute")
    return {"status": "OK", "message": "pong", "layer": "runtime"}


@register("system.status")
def system_status(payload, context):
    emit_reason({"intent": "system.status"}, "execute")
    return {"status": "OK", "uptime": "unknown", "services": ["runtime"]}


@register("system.events")
def system_events(payload, context):
    emit_reason({"intent": "system.events"}, "observe")
    events = read_events()
    return {"count": len(events), "events": events[-50:]}


@register("system.drift")
def system_drift(payload, context):
    emit_reason({"intent": "system.drift"}, "compare")
    replay = replay_state_only()
    return {"drift": LIVE_STATE != replay, "live": LIVE_STATE, "replay": replay}


# =========================================================
# MEDIA
# =========================================================

@register("media.play")
def media_play(payload, context):
    emit_reason({"intent": "media.play"}, "execute")
    return media_play_runtime(payload, context)


# =========================================================
# AI LAYER
# =========================================================

@register("ai.ask")
def ai_ask(payload, context):
    emit_reason({"intent": "ai.ask"}, "execute")
    return ai_ask_runtime(payload, context)

from mycelium.core.intent_learner import suggest_intents


@register("system.intents.learned")
def learned_intents(payload, context):
    return suggest_intents()

from mycelium.core.intent_patch_generator import generate_registry_patch
from mycelium.core.registry_governance import validate_patch


def system_intent_expand(payload, context):
    patch = generate_registry_patch()

    decision = validate_patch(patch["response"])

    return {
        "status": "OK",
        "approved": decision["approved"],
        "patch": patch["response"],
        "reason": decision["reason"]
    }


REGISTRY["system.intent.expand"] = system_intent_expand

from mycelium.core.compiler_evolver import propose_new_rules


def system_compiler_evolve(payload, context):
    return {
        "status": "OK",
        "proposals": propose_new_rules()
    }


REGISTRY["system.compiler.evolve"] = system_compiler_evolve

# -----------------------------
# KNOWLEDGE LAYER
# -----------------------------
from mycelium.core.registry_knowledge import knowledge_query

REGISTRY["knowledge.query"] = knowledge_query

from mycelium.core.knowledge import knowledge_query
from mycelium.core.ai_backend import ai_generate


def ai_ask(payload, context):
    prompt = payload.get("prompt", "")
    response = ai_generate(prompt, context)

    return {
        "status": "OK",
        "prompt": prompt,
        "response": response
    }


REGISTRY["ai.ask"] = ai_ask
REGISTRY["knowledge.query"] = knowledge_query

from mycelium.core.secure_memory_vault import system_vault_status
from mycelium.core.intent_graph_executor import system_execute_graph
from mycelium.core.hard_governance_kernel import system_governance_check

REGISTRY["system.vault.status"] = system_vault_status
REGISTRY["system.execute.graph"] = system_execute_graph
REGISTRY["system.governance.check"] = system_governance_check

from mycelium.core.identity_vault import (
    system_identity_status
)

from mycelium.core.agent_swarm import (
    system_swarm_status
)

from mycelium.core.formal_verifier import (
    system_verify
)

REGISTRY["system.identity.status"] = system_identity_status
REGISTRY["system.swarm.status"] = system_swarm_status
REGISTRY["system.verify"] = system_verify

from mycelium.core.execution_trace import system_trace
from mycelium.core.visualizer import system_visualize
from mycelium.core.evolution_visualizer import system_evolution_view
from mycelium.core.graph_visualizer import system_graph_view

REGISTRY["system.trace"] = system_trace
REGISTRY["system.visualize"] = system_visualize
REGISTRY["system.evolution.view"] = system_evolution_view
REGISTRY["system.graph.view"] = system_graph_view

from mycelium.core.distributed_cluster import system_cluster
from mycelium.core.dashboard_api import system_dashboard
from mycelium.core.time_travel_debugger import system_time_travel
from mycelium.core.adaptive_visualizer import system_adaptive_view

REGISTRY["system.cluster"] = system_cluster
REGISTRY["system.dashboard"] = system_dashboard
REGISTRY["system.time.travel"] = system_time_travel
REGISTRY["system.visual.adaptive"] = system_adaptive_view

from mycelium.core.node_identity import system_nodes
from mycelium.core.time_travel_v2 import system_debug
from mycelium.runtime.node_mesh import system_mesh

REGISTRY["system.nodes"] = system_nodes
REGISTRY["system.debug"] = system_debug
REGISTRY["system.mesh"] = system_mesh
