from threading import Thread
from mycelium.core.event_bus import EVENT_BUS
from mycelium.core.events import RAW_INPUT
from mycelium.core.workers.shell_workers import bootstrap_shell_workers
from mycelium.runtime.acquisition_worker import handle_acquisition


# -----------------------------
# BOOTSTRAP LAYER (IMPORTANT)
# -----------------------------

EVENT_BUS.subscribe(handle_acquisition)


def input_collector():
    """
    The only blocking part of the system. 
    Sits in a separate thread just to listen for keystrokes.
    """
    while True:
        try:
            raw = input("mshell> ")
            
            if raw.strip() == "exit":
                print("Exiting Mycelium Shell...")
                break

            # Just throw the job onto the table and forget about it
            EVENT_BUS.publish({
                "type": RAW_INPUT,
                "payload": {"text": raw}
            })
        except EOFError:
            break
        except Exception as e:
            print(f"Input Error: {e}")


def main():
    print("🧠 Mycelium MSHELL Router v2 (Event-Driven)")
    print("(Type 'exit' to quit)")

    # Sit the workers at the table
    bootstrap_shell_workers()

    # Start the input listener in the background
    collector_thread = Thread(target=input_collector, daemon=True)
    collector_thread.start()

    # Keep the main thread alive so the workers can work
    try:
        collector_thread.join()
    except KeyboardInterrupt:
        print("\nShutdown requested.")


if __name__ == "__main__":
    main()

# -----------------------------
# AUTONOMOUS REPAIR BOOTSTRAP
# -----------------------------
from mycelium.core.event_bus import EVENT_BUS
from mycelium.runtime.repair_layer import suggest_repair

EVENT_BUS.subscribe_post(lambda e: suggest_repair())
