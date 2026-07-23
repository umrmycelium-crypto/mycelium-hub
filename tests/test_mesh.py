import unittest
import time
import socket
import os
import shutil
from mycelium.core.node_identity import (
    create_node_identity,
    verify_node,
    register_remote_node,
    system_nodes,
    get_or_create_local_identity,
)
from mycelium.core.mesh_registry import MeshRegistry
from mycelium.core.distributed_bus import DistributedBus, SystemEvent
from mycelium.core.mesh_state import MeshState
from mycelium.core.capability_router import CapabilityRouter


class TestMyceliumMesh(unittest.TestCase):
    def setUp(self):
        self.test_dir = "state_test_mesh"
        os.makedirs(self.test_dir, exist_ok=True)
        self.registry_file = os.path.join(self.test_dir, "mesh_registry.json")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_node_identity(self):
        identity = create_node_identity("test-node-1", "secret-key-123")
        self.assertIn("node_id", identity)
        self.assertIn("token", identity)
        self.assertTrue(verify_node(identity["node_id"], identity["token"]))
        self.assertFalse(verify_node(identity["node_id"], "invalid-token"))

        register_remote_node("remote-id-999", "remote-macbook", "remote-token-abc")
        nodes_info = system_nodes()
        self.assertGreaterEqual(nodes_info["count"], 2)

    def test_mesh_registry_and_pruning(self):
        registry = MeshRegistry(node_id="primary-node", state_file=self.registry_file)
        
        # 1. Update nodes
        manifest_linux = {
            "os": "Linux",
            "hardware": ["CPU", "GPU", "RAM"],
            "agents": ["MediaAgent", "DevelopmentAgent"]
        }
        manifest_mac = {
            "os": "Darwin",
            "hardware": ["CPU", "RAM"],
            "agents": ["KnowledgeAgent"]
        }
        manifest_win = {
            "os": "Windows",
            "hardware": ["CPU", "GPU", "Storage"],
            "agents": ["SystemAgent"]
        }

        registry.update_node("primary-node", manifest_linux)
        registry.update_node("mac-node", manifest_mac)
        registry.update_node("win-node", manifest_win)

        self.assertEqual(len(registry.nodes), 3)

        # 2. Test routing heuristics
        self.assertEqual(registry.get_best_node_for_task("high_vram"), "primary-node")
        self.assertEqual(registry.get_best_node_for_task("darwin"), "mac-node")
        self.assertEqual(registry.get_best_node_for_task("windows"), "win-node")
        self.assertEqual(registry.get_best_node_for_task("KnowledgeAgent"), "mac-node")

        # 3. Test heartbeat and pruning
        registry.heartbeat_node("mac-node")
        # Artificially set win-node last_seen to old date
        registry.nodes["win-node"]["last_seen"] = "2020-01-01T00:00:00+00:00"
        pruned = registry.prune_stale_nodes(timeout_seconds=60.0)
        
        self.assertIn("win-node", pruned)
        self.assertNotIn("win-node", registry.nodes)
        self.assertIn("mac-node", registry.nodes)

    def test_distributed_bus_and_mesh_state(self):
        port1 = 6111
        port2 = 6112
        
        bus1 = DistributedBus(node_id="node1", port=port1, mesh_nodes=["127.0.0.1"])
        bus2 = DistributedBus(node_id="node2", port=port2, mesh_nodes=["127.0.0.1"])
        bus1.mesh_nodes = ["127.0.0.1"]
        time.sleep(0.2)  # Allow sockets to start listening
        
        # Override _send_to_node to target port2 for bus1
        def mock_send(ip, data):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(3.0)
                    s.connect((ip, port2))
                    s.sendall(data.encode('utf-8'))
            except Exception as e:
                pass
        bus1._send_to_node = mock_send

        received_events = []
        def on_event(event: SystemEvent):
            received_events.append(event)

        bus2.subscribe("state.update", on_event)

        state1 = MeshState(bus=bus1)
        state2 = MeshState(bus=bus2)

        # Update fact on bus1 -> publishes globally to bus2
        state1.update_global_fact("user_location", "studio")
        time.sleep(0.8)

        self.assertGreaterEqual(len(received_events), 1)
        self.assertEqual(received_events[0].payload["key"], "user_location")
        self.assertEqual(received_events[0].payload["value"], "studio")
        self.assertEqual(state2.get_global_fact("user_location"), "studio")

        bus1.stop()
        bus2.stop()


    def test_capability_router(self):
        registry = MeshRegistry(node_id="node-a", state_file=self.registry_file)
        registry.update_node("node-a", {"os": "Linux", "hardware": ["GPU"], "agents": []})
        registry.update_node("node-b", {"os": "Linux", "hardware": ["Storage", "NAS"], "agents": []})

        router = CapabilityRouter(registry=registry)
        self.assertEqual(router.resolve_execution_node("rendering"), "node-a")
        self.assertEqual(router.resolve_execution_node("knowledge_synthesis"), "node-b")


if __name__ == "__main__":
    unittest.main()
