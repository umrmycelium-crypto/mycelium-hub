from .router import detect_intent
from .agents.decomposer import decompose
from .agents.context_agent import build_context
from .core.registry import register_all
from .memory.manager import record_success, record_failure
import json

def main():
    print("Mycelium Intent Engine v0.8 (Behavior Adaptive - Type 'exit' to quit)")

    # Initialize Registry and Bus
    bus = register_all()

    while True:
        try:
            command = input("> ")
            if not command.strip():
                continue
            if command.lower() in ["exit", "quit"]:
                break

            # Build current system context (State + History + Memory)
            context = build_context()

            # Decompose complex input with state and memory awareness
            print(f"DEBUG: Decomposing input with memory-aware context...")
            events = decompose(command, context)

            if not events:
                print("[UNKNOWN] Could not decompose input.")
                continue

            for i, event_data in enumerate(events):
                intent = event_data.get("intent", "unknown")
                entities = event_data.get("entities", {})

                # Payload construction
                payload = entities.copy()
                payload["text"] = command

                print(f"--- Event {i+1}: {intent} ---")
                if entities:
                    print(f"DEBUG: Entities: {entities}")

                # Publish to the bus
                results = bus.publish(intent, payload)

                if not results:
                    print(f"[UNKNOWN] No subscribers for intent: {intent}")
                    record_failure(intent, command)
                    continue

                # Analyze results for success/failure to update memory
                result = results[0]
                status = result.get('status', 'unknown')

                print(f"[{status.upper()}] {result['message']}")

                if status in ['success', 'ok']:
                    # Extract primary entity value for success tracking
                    entity_val = entities.get('title') or entities.get('query')
                    if entity_val:
                        record_success(intent, entity_val)
                elif status in ['error', 'not_found', 'failed']:
                    record_failure(intent, command)

                # Special handling for developer analysis
                if result['intent'] == 'developer.assist' and status == 'ok':
                     print("\nAnalysis Output:")
                     print(result['data'].get('analysis'))

            print("-" * 30)


        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break

            
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
