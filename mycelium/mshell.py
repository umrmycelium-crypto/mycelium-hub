from mycelium.core.compiler import IntentCompiler
from mycelium.core.router import route
from mycelium.core.event_bus import EVENT_BUS
from mycelium.runtime.acquisition_worker import handle_acquisition


# -----------------------------
# BOOTSTRAP LAYER (IMPORTANT)
# -----------------------------

EVENT_BUS.subscribe(handle_acquisition)


def main():
    print("🧠 Mycelium MSHELL Router v1 (type 'exit')")

    while True:
        try:
            raw = input("mshell> ")

            if raw.strip() == "exit":
                break

            intent = IntentCompiler.compile(raw)
            result = route(intent)

            print(result)

        except Exception as e:
            print({"status": "ERROR", "message": str(e)})


if __name__ == "__main__":
    main()

# -----------------------------
# AUTONOMOUS REPAIR BOOTSTRAP
# -----------------------------
from mycelium.core.event_bus import EVENT_BUS
from mycelium.runtime.repair_layer import suggest_repair

EVENT_BUS.subscribe_post(lambda e: suggest_repair())
