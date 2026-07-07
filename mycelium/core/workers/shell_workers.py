from mycelium.core.event_bus import EVENT_BUS
from mycelium.core.events import RAW_INPUT, INTENT_RESOLVED, INTENT_RESULT, SYSTEM_ERROR
from mycelium.core.compiler import IntentCompiler
from mycelium.core.router import route

# -----------------------------------------------------------------------------
# THE WORKERS ("People at the table")
# -----------------------------------------------------------------------------

def compiler_worker(event):
    """
    Job: Translate raw text into a structured intent.
    Trigger: RAW_INPUT
    """
    if event.get("type") != RAW_INPUT:
        return

    try:
        text = event.get("payload", {}).get("text", "")
        if not text.strip():
            return

        intent = IntentCompiler.compile(text)
        
        # Pass the job to the next person: The Router
        EVENT_BUS.publish({
            "type": INTENT_RESOLVED,
            "payload": intent
        })
    except Exception as e:
        EVENT_BUS.publish({
            "type": SYSTEM_ERROR,
            "payload": {"message": f"Compiler Error: {str(e)}"}
        })

def router_worker(event):
    """
    Job: Execute the resolved intent.
    Trigger: INTENT_RESOLVED
    """
    if event.get("type") != INTENT_RESOLVED:
        return

    try:
        intent = event.get("payload", {})
        result = route(intent)
        
        # Pass the job to the next person: The Renderer
        EVENT_BUS.publish({
            "type": INTENT_RESULT,
            "payload": {
                "intent": intent,
                "result": result
            }
        })
    except Exception as e:
        EVENT_BUS.publish({
            "type": SYSTEM_ERROR,
            "payload": {"message": f"Router Error: {str(e)}"}
        })

def output_worker(event):
    """
    Job: Show the result to the user.
    Trigger: INTENT_RESULT or SYSTEM_ERROR
    """
    if event.get("type") == INTENT_RESULT:
        payload = event.get("payload", {})
        result = payload.get("result")
        print(f"\n{result}")
        print("mshell> ", end="", flush=True)
    
    elif event.get("type") == SYSTEM_ERROR:
        msg = event.get("payload", {}).get("message", "Unknown Error")
        print(f"\n❌ {msg}")
        print("mshell> ", end="", flush=True)

def persist_unhandled(event):
    """
    Persist unhandled intents to persistent intent memory.
    Trigger: INTENT_RESULT with result.status == 'NO_HANDLER'
    """
    if event.get("type") != INTENT_RESULT:
        return

    payload = event.get("payload", {})
    intent = payload.get("intent", {})
    result = payload.get("result", {})

    try:
        if isinstance(result, dict) and result.get("status") == "NO_HANDLER":
            # Prefer the original raw text if available
            raw = intent.get("payload", {}).get("raw") or intent.get("payload", {}).get("title") or str(intent)
            from mycelium.memory.manager import record_failure
            record_failure(result.get("intent"), raw)
    except Exception:
        pass


def bootstrap_shell_workers():
    """
    Sits everyone down at the table.
    """
    EVENT_BUS.subscribe(compiler_worker)
    EVENT_BUS.subscribe(router_worker)
    EVENT_BUS.subscribe(output_worker)
    EVENT_BUS.subscribe(persist_unhandled)
