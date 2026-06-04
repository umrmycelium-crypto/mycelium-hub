from .router import detect_intent
from .agents.decomposer import decompose
from .agents.context_agent import build_context
from .core.registry import register_all
import json

def main():
    print("Mycelium Intent Engine v0.7 (State-Aware Orchestration - Type 'exit' to quit)")

    # Initialize Registry and Bus
    bus = register_all()

    while True:
        try:
            command = input("> ")
            if not command.strip():
                continue
            if command.lower() in ["exit", "quit"]:
                break

            # Build current system context
            context = build_context()

            # Decompose complex input with state awareness
            print(f"DEBUG: Decomposing input with context...")
            events = decompose(command, context)
            if not events:
                print("[UNKNOWN] Could not decompose input.")
                continue

            for i, event_data in enumerate(events):
                intent = event_data.get("intent", "unknown")
                payload = event_data.get("entities", {})
                payload["text"] = command # Include original for fallback

                # Debug info per event
                print(f"--- Event {i+1}: {intent} ---")
                if payload:
                    print(f"DEBUG: Entities: {payload}")

                # Publish to the bus
                results = bus.publish(intent, payload)

                if not results:
                    print(f"[UNKNOWN] No subscribers for intent: {intent}")
                    continue

                # Handle the first result (primary action)
                result = results[0]
                print(f"[{result['status'].upper()}] {result['message']}")

                # Special handling for developer analysis
                if result['intent'] == 'developer.assist' and result['status'] == 'ok':
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
