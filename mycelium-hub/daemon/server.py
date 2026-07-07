# =========================
# CORTEX CORE v1
# SINGLE CLOCK COGNITIVE SYSTEM
# =========================

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from copy import deepcopy
import asyncio
import json
import os

# Load environment variables from .env file (if present)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, but env vars can still be set externally

# =========================
# APP
# =========================

app = FastAPI()
from mycelium.core.bridge import IntentSynthesizer
synthesizer = IntentSynthesizer()

# =========================
# CONFIG
# =========================

STATE_PATH = "state/latest.json"
CLOCK_INTERVAL = 0.2
TICK_LOG = []
MAX_LOG = 500

# =========================
# GLOBAL STATE (SINGLE SOURCE OF TRUTH)
# =========================

state = None
latest_state = None
state_lock = asyncio.Lock()
clock_task = None


# =========================
# DEFAULT STATE
# =========================

DEFAULT_STATE = {
    "tick": 0,
    "params": {
        "learning_rate": 0.05
    },
    "self": {
        "focus": [0.0, 0.0, 0.0],
        "coherence": 0.5,
        "novelty": 0.5,
        "stability": 0.5
    },
    "nodes": {
        "seed": 0.5,
        "memory": 0.5,
        "intent": 0.5
    },
    "ideas": [
        {"id": "origin", "name": "origin", "strength": 0.5, "age": 0}
    ],
    "intent_field": 0.5,
    "meta": {},
    "story": ""
}


# =========================
# LOAD / SAVE (SAFE I/O)
# =========================

def load_state():
    if not os.path.exists(STATE_PATH):
        return deepcopy(DEFAULT_STATE)

    try:
        with open(STATE_PATH, "r") as f:
            data = f.read().strip()
            if not data:
                return deepcopy(DEFAULT_STATE)
            state = json.loads(data)
        
        # Normalize legacy state with unbounded values
        if "ideas" in state:
            for idea in state["ideas"]:
                if "strength" in idea:
                    idea["strength"] = min(1.0, max(0.0, idea["strength"]))
                if "value" in idea:
                    idea["value"] = min(1.0, max(0.0, idea["value"]))
        
        if "nodes" in state:
            for node_id in state["nodes"]:
                state["nodes"][node_id] = min(1.0, max(0.0, state["nodes"][node_id]))
        
        if "intent_field" in state:
            state["intent_field"] = min(1.0, max(0.0, state["intent_field"]))
        
        return state
    except Exception:
        return deepcopy(DEFAULT_STATE)


def save_state(snapshot):
    os.makedirs("state", exist_ok=True)

    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(snapshot, f)

    os.replace(tmp, STATE_PATH)

def snapshot(state):
    return deepcopy(state)

# =========================
# NORMALIZATION (NO SIDE EFFECTS)
# =========================

def normalize_state(s):
    s.setdefault("tick", 0)
    s.setdefault("params", DEFAULT_STATE["params"])
    s.setdefault("self", DEFAULT_STATE["self"])
    s.setdefault("nodes", DEFAULT_STATE["nodes"])
    s.setdefault("ideas", [])
    s.setdefault("intent_field", DEFAULT_STATE["intent_field"])
    s.setdefault("meta", {})
    s.setdefault("story", "")

    return s


# =========================
# CORE COGNITION STEP (PURE FUNCTION STYLE)
# =========================

def evolve(s):
    s["tick"] += 1

    self_state = s["self"]

    c = self_state["coherence"]
    n = self_state["novelty"]
    t = self_state["stability"]

    lr = s["params"]["learning_rate"]

    # bounded dynamics (stable attractor system)
    self_state["coherence"] = max(0.0, min(1.0, c + (t - n) * lr * 0.01))
    self_state["novelty"]   = max(0.0, min(1.0, n + (0.5 - c) * lr * 0.01))
    self_state["stability"] = max(0.0, min(1.0, t + (0.5 - n) * lr * 0.01))

    # NODE DYNAMICS - decay and influence
    for node_id in s["nodes"]:
        s["nodes"][node_id] = max(0.0, s["nodes"][node_id] * 0.96)
    
    # seed influences memory
    s["nodes"]["memory"] = min(1.0, s["nodes"].get("memory", 0.5) + s["nodes"].get("seed", 0.5) * 0.01)
    
    # intent becomes EMERGENT from idea field
    idea_field_value = s.get("intent_field", 0.5)
    s["nodes"]["intent"] = max(0.0, s["nodes"].get("intent", 0.5) * 0.98 + idea_field_value * 0.02)

    # ideas evolve slowly (bounded growth + aging)
    new_ideas = []

    for idea in s["ideas"]:
        idea = deepcopy(idea)
        idea["age"] += 1
        # Bounded exponential growth with cap at 1.0 to prevent overflow
        idea["strength"] = min(1.0, idea["strength"] * 1.0005)
        new_ideas.append(idea)

    s["ideas"] = new_ideas

    # Generate new ideas from node interactions (idea convergence simulation)
    import random
    import math
    
    # Track idea counter in meta if not present
    if "idea_counter" not in s.get("meta", {}):
        s.setdefault("meta", {})
        s["meta"]["idea_counter"] = 0
    
    s["meta"]["idea_counter"] += 1
    idea_counter = s["meta"]["idea_counter"]
    
    # Generate ideas based on node activations
    intent_activation = s["nodes"].get("intent", 0.5)
    seed_activation = s["nodes"].get("seed", 0.5)
    memory_activation = s["nodes"].get("memory", 0.5)
    
    # Create new idea from intent coupling
    new_strength = intent_activation * 0.5 + seed_activation * 0.3
    if new_strength > 0.1:
        new_ideas.append({
            "id": f"idea_{idea_counter}",
            "name": f"idea_{idea_counter}",
            "value": float(min(1.0, new_strength)),
            "strength": float(min(1.0, new_strength)),
            "phase": random.random(),
            "vec": [0.0, 0.0, 0.0],
            "age": 0
        })
    
    # Also create ideas from memory-seed interactions
    if idea_counter % 10 == 0 and len(new_ideas) < 50:
        convergence_strength = (seed_activation + memory_activation) / 2 * 0.8
        if convergence_strength > 0.2:
            new_ideas.append({
                "id": f"converged_{idea_counter}",
                "name": f"converged_{idea_counter}",
                "value": float(min(1.0, convergence_strength)),
                "strength": float(min(1.0, convergence_strength)),
                "phase": random.random(),
                "vec": [0.0, 0.0, 0.0],
                "age": 0
            })
    
    # Re-assign the evolved ideas with new ones
    s["ideas"] = new_ideas

    # Calculate intent_field from ideas (using strength as value)
    if s["ideas"]:
        s["intent_field"] = sum(i.get("strength", 0.5) for i in s["ideas"]) / len(s["ideas"])
    else:
        s["intent_field"] = 0.5

    return s


# =========================
# SINGLE CLOCK LOOP (AUTHORITY)
# =========================

async def cognition_loop():
    global state, latest_state

    while True:
        await asyncio.sleep(CLOCK_INTERVAL)

        async with state_lock:
            # 1. normalize
            state = normalize_state(state)

            # 2. evolve (ONLY ONE MUTATION STEP PER CLOCK)
            state = evolve(state)

            # 3. snapshot immediately (immutable publish)
            snap = snapshot(state)

            latest_state = snap

            # 4. append to event log (bounded)
            TICK_LOG.append(snap)

            if len(TICK_LOG) > MAX_LOG:
                TICK_LOG.pop(0)

            # 5. Bridge: Autonomous Synthesis
            await synthesizer.execute_synthesis(snap)

            # 6. persist snapshot (optional but safe now)
            save_state(snap)


# =========================
# WATCHDOG - Prevents hangs
# =========================

WATCHDOG_INTERVAL = 60  # Check every 60 seconds
MAX_STALL = 120  # Restart if no tick for 120 seconds

async def watchdog():
    global state, latest_state
    
    last_tick = 0
    
    while True:
        await asyncio.sleep(WATCHDOG_INTERVAL)
        
        current_tick = state.get("tick", 0) if state else 0
        
        if current_tick == last_tick:
            # No progress - cognition loop may be stuck
            print(f"WATCHDOG: No tick progress for {WATCHDOG_INTERVAL}s, tick={current_tick}")
            
            # Try to recover by reloading state
            try:
                state = load_state()
                latest_state = deepcopy(state)
                print(f"WATCHDOG: State reloaded, tick={state.get('tick', 0)}")
            except Exception as e:
                print(f"WATCHDOG: Failed to reload state: {e}")
        else:
            last_tick = current_tick


# =========================
# STARTUP
# =========================

@app.on_event("startup")
async def start_cortex():
    global state, latest_state

    state = load_state()
    latest_state = deepcopy(state)

    asyncio.create_task(cognition_loop())
    asyncio.create_task(watchdog())


# =========================
# READ API (NO MUTATION)
# =========================

@app.get("/tick")
def tick():
    return deepcopy(latest_state)


@app.get("/health")
def health():
    return {"status": "alive"}

@app.get("/status")
def status():
    return {
        "status": "alive",
        "tick": state.get("tick", 0) if state else 0,
        "ideas_count": len(state.get("ideas", [])) if state else 0,
        "nodes_count": len(state.get("nodes", {})) if state else 0,
        "intent_field": state.get("intent_field", 0) if state else 0
    }

@app.get("/log")
def log():
    return {
        "size": len(TICK_LOG),
        "ticks": TICK_LOG[-20:]
    }
# =========================
# STREAM (READ-ONLY SNAPSHOTS)
# =========================

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            await asyncio.sleep(CLOCK_INTERVAL)

            if latest_state is None:
                continue

            try:
                await websocket.send_json({
                    "type": "tick",
                    "payload": latest_state
                })
            except Exception:
                break
    except Exception:
        pass
