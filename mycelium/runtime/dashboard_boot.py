from mycelium.runtime.event_spine import install_event_spine
from mycelium.runtime.perception_layer import install_perception_layer


def boot():
    install_event_spine()
    install_perception_layer()
