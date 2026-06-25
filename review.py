import sys
import json


def main():
    if len(sys.argv) < 2:
        print("commands: queue | inspect <id> | approve <id> | reject <id> | stress <n>")
        return

    cmd = sys.argv[1]

    if cmd == "queue":
        from mycelium.tools.review_cli import show_queue
        show_queue()

    elif cmd == "inspect":
        from mycelium.tools.review_cli import inspect
        inspect(sys.argv[2])

    elif cmd == "approve":
        from mycelium.tools.review_cli import approve
        print(approve(sys.argv[2]))

    elif cmd == "reject":
        from mycelium.tools.review_cli import reject
        print(reject(sys.argv[2]))

    elif cmd == "stress":
        from mycelium.core.governance_stress_simulator import run_stress_simulation

        cycles = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        print(json.dumps(run_stress_simulation(cycles), indent=2))

    else:
        print({"error": "unknown command", "cmd": cmd})


if __name__ == "__main__":
    main()
