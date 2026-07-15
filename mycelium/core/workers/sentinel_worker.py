import requests
import logging
from mycelium.core.event_bus import EVENT_BUS
from mycelium.agents.executive_agent import executive_agent_personal

# --- Configuration ---
VOICE_SERVER_URL = "http://localhost:7001/speak"

# Trigger Map: Event Type -> Base Prompt for the Executive Agent
# This tells the agent WHY it is being woken up.
TRIGGER_MAP = {
    "user.presence": "The user has just been detected as present in the environment. Based on the current time, system state, and memory, should you greet them or provide a proactive update? If yes, generate a short, natural greeting. If no, respond with 'SKIP'.",
    "system.alert": "A system alert has occurred: {payload}. Determine if this requires immediate user notification. If so, explain the issue concisely and suggest a fix. If not, respond with 'SKIP'.",
    "audio.activate": "A new audio stream has been activated from {source}. Monitor the initial context and decide if a proactive acknowledgment is needed. If so, respond naturally. If not, respond with 'SKIP'.",
    "vision.activate": "A live vision feed from {source} is now active. Based on what is seen (if available in memory), decide if you should initiate a conversation. If so, respond naturally. If not, respond with 'SKIP'.",
}

def sentinel_worker(event):
    """
    The Sentinel monitors the event bus for specific triggers that should 
    initiate proactive agency.
    """
    etype = event.get("type", "unknown")
    payload = event.get("payload", {})
    
    if etype in TRIGGER_MAP:
        # Generate the specific prompt for this event
        base_prompt = TRIGGER_MAP[etype]
        
        # Inject payload details into the prompt if placeholders exist
        try:
            prompt = base_prompt.format(**payload)
        except KeyError:
            prompt = base_prompt

        # 1. Ask the Executive Agent to reason about the trigger
        decision = executive_agent_personal.run(prompt)

        # 2. Check if the agent decided to act
        if decision and "SKIP" not in decision.upper():
            speak_proactively(decision)

def speak_proactively(text):
    """
    Routes the agent's decision to the voice server for audible output.
    """
    try:
        requests.post(VOICE_SERVER_URL, json={"text": text}, timeout=5)
    except Exception as e:
        logging.error(f"Sentinel failed to route proactive speech: {e}")

def bootstrap_sentinel_workers():
    """
    Connects the Sentinel to the nervous system.
    """
    EVENT_BUS.subscribe(sentinel_worker)
