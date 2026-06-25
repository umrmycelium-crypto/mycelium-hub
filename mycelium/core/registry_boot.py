from mycelium.core.handlers import register
from mycelium.runtime.media import media_play as media_play_runtime
from mycelium.runtime.ai import ai_ask as ai_ask_runtime
from mycelium.core.event_store import read_events
from mycelium.core.projections import LIVE_STATE
from mycelium.core.replay import replay_state_only
from mycelium.core.reasoning import emit_reason
from mycelium.core.system_governance import system_governance


# -------------------------
# SYSTEM
# -------------------------

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


# -------------------------
# MEDIA
# -------------------------

@register("media.play")
def media_play(payload, context):
    emit_reason({"intent": "media.play"}, "execute")
    return media_play_runtime(payload, context)


# -------------------------
# AI
# -------------------------

@register("ai.ask")
def ai_ask(payload, context):
    return ai_ask_runtime(payload, context)


# -------------------------
# GOVERNANCE
# -------------------------

@register("system.governance")
def governance(payload, context):
    return system_governance(payload, context)
