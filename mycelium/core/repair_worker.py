import time
from mycelium.core.repair_engine import run_multi_strategy_repair
from mycelium.core.event_bus import EVENT_BUS


class RepairWorker:
    """
    Background autonomous repair loop.
    """

    def __init__(self, interval=10):
        self.interval = interval
        self.running = False

    def start(self):
        self.running = True

        while self.running:
            try:
                drift_event = {
                    "type": "system.repair.tick"
                }

                result = run_multi_strategy_repair(drift_event)

                EVENT_BUS.publish({
                    "type": "repair.result",
                    "payload": result
                })

            except Exception as e:
                EVENT_BUS.publish({
                    "type": "repair.error",
                    "payload": {"error": str(e)}
                })

            time.sleep(self.interval)

    def stop(self):
        self.running = False


REPAIR_WORKER = RepairWorker()
