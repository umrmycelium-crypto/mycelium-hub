import sys
import time
sys.path.insert(0, r'D:\mycelium-hub')

print('Starting non-interactive MSHELL test...')

from mycelium.core.event_bus import EVENT_BUS
from mycelium.core.workers.shell_workers import bootstrap_shell_workers
from mycelium.core.workers.sensor_workers import bootstrap_sensor_workers
from mycelium.core.events import RAW_INPUT
from mycelium.core.event_store import read_events

# Bootstrap workers
bootstrap_shell_workers()
bootstrap_sensor_workers()

# Publish a test input that should trigger our new handler
EVENT_BUS.publish({"type": RAW_INPUT, "payload": {"text": "explain event-driven systems"}})

# Give synchronous subscribers a moment (publish is synchronous, but be safe)
time.sleep(0.5)

events = read_events()
print('Recent events (last 8):')
for e in events[-8:]:
    print(e)

print('Test complete.')
