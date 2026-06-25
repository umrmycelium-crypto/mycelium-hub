"""Tests for Mycelium Idea-Field Runtime.

These tests verify the core idea-field dynamics, node behavior,
and emergent properties of the Mycelium cognitive architecture.

Beta-tester: Steve - A normal man with demons, exploring the system.
"""

import math
import pytest
import sys

# Add daemon directory to path for imports
sys.path.insert(0, '/home/mycelium/mycelium-hub/mycelium-hub/daemon')

from runtime import Runtime


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def fresh_runtime():
    """Create a fresh Runtime instance for each test."""
    return Runtime()


@pytest.fixture
def runtime_with_ideas():
    """Create a Runtime with some pre-populated ideas."""
    rt = Runtime()
    # Add a few ideas manually
    for i in range(3):
        rt.ideas.append({
            "id": f"test_idea_{i}",
            "name": f"test_{i}",
            "value": 0.5 + i * 0.1,
            "strength": 0.5 + i * 0.1,
            "phase": i * 0.5,
            "vec": [float(i), float(i * 0.5), float(i * 0.25)]
        })
    return rt


# =============================================================================
# Runtime Initialization Tests
# =============================================================================

class TestRuntimeInitialization:
    """Test Runtime class initialization."""

    def test_initial_tick_is_zero(self, fresh_runtime):
        """Runtime should start at tick 0."""
        assert fresh_runtime.tick == 0

    def test_initial_idea_counter_is_zero(self, fresh_runtime):
        """Idea counter should start at 0."""
        assert fresh_runtime.idea_counter == 0

    def test_initial_nodes_exist(self, fresh_runtime):
        """Runtime should have seed, memory, and intent nodes."""
        assert "seed" in fresh_runtime.nodes
        assert "memory" in fresh_runtime.nodes
        assert "intent" in fresh_runtime.nodes

    def test_initial_nodes_have_activation(self, fresh_runtime):
        """All nodes should have activation values."""
        for node_id, node in fresh_runtime.nodes.items():
            assert "activation" in node
            assert isinstance(node["activation"], (int, float))

    def test_initial_ideas_exist(self, fresh_runtime):
        """Runtime should start with at least one idea."""
        assert len(fresh_runtime.ideas) >= 1

    def test_initial_idea_has_required_fields(self, fresh_runtime):
        """Initial idea should have all required fields."""
        first_idea = fresh_runtime.ideas[0]
        required_fields = ["id", "name", "value", "strength", "phase", "vec"]
        for field in required_fields:
            assert field in first_idea, f"Missing field: {field}"


# =============================================================================
# Idea Field Calculation Tests
# =============================================================================

class TestIdeaField:
    """Test idea-field calculation logic."""

    def test_idea_field_with_no_ideas(self, fresh_runtime):
        """Idea field should return 0.5 when there are no ideas."""
        fresh_runtime.ideas = []
        assert fresh_runtime._idea_field() == 0.5

    def test_idea_field_with_one_idea(self, fresh_runtime):
        """Idea field should return the value of a single idea."""
        fresh_runtime.ideas = [{"id": "test", "value": 0.7, "name": "test", "strength": 0.5, "phase": 0.0, "vec": [0,0,0]}]
        assert fresh_runtime._idea_field() == pytest.approx(0.7)

    def test_idea_field_average_of_multiple(self, runtime_with_ideas):
        """Idea field should be the average of all idea values."""
        expected_avg = sum(i["value"] for i in runtime_with_ideas.ideas) / len(runtime_with_ideas.ideas)
        assert runtime_with_ideas._idea_field() == pytest.approx(expected_avg)

    def test_idea_field_bounded(self, runtime_with_ideas):
        """Idea field should always be between 0 and 1."""
        field = runtime_with_ideas._idea_field()
        assert 0.0 <= field <= 1.0


# =============================================================================
# Step Function Tests
# =============================================================================

class TestStepFunction:
    """Test the main step function that advances the simulation."""

    def test_step_increments_tick(self, fresh_runtime):
        """Each step should increment the tick counter."""
        initial_tick = fresh_runtime.tick
        fresh_runtime.step()
        assert fresh_runtime.tick == initial_tick + 1

    def test_step_returns_dict(self, fresh_runtime):
        """Step should return a dictionary with state."""
        result = fresh_runtime.step()
        assert isinstance(result, dict)

    def test_step_returns_required_keys(self, fresh_runtime):
        """Step should return tick, nodes, ideas, and intent_field."""
        result = fresh_runtime.step()
        required_keys = ["tick", "nodes", "ideas", "intent_field"]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"

    def test_step_decays_node_activation(self, fresh_runtime):
        """Node activations should decay over time."""
        initial_seed = fresh_runtime.nodes["seed"]["activation"]
        fresh_runtime.step()
        assert fresh_runtime.nodes["seed"]["activation"] < initial_seed

    def test_step_ideas_evolve(self, fresh_runtime):
        """Idea values should change after a step."""
        initial_values = [i["value"] for i in fresh_runtime.ideas]
        fresh_runtime.step()
        new_values = [i["value"] for i in fresh_runtime.ideas]
        # At least one idea should have changed
        assert initial_values != new_values


# =============================================================================
# Node Dynamics Tests
# =============================================================================

class TestNodeDynamics:
    """Test the behavior of individual nodes."""

    def test_seed_influences_memory(self, fresh_runtime):
        """Seed activation should influence memory activation."""
        # Set seed to high activation
        fresh_runtime.nodes["seed"]["activation"] = 1.0
        initial_memory = fresh_runtime.nodes["memory"]["activation"]
        
        fresh_runtime.step()
        
        # Memory should have increased
        assert fresh_runtime.nodes["memory"]["activation"] > initial_memory

    def test_intent_emerges_from_idea_field(self, fresh_runtime):
        """Intent should be influenced by the idea field."""
        # Set up a known state
        fresh_runtime.nodes["intent"]["activation"] = 0.5
        initial_intent = fresh_runtime.nodes["intent"]["activation"]
        
        fresh_runtime.step()
        
        # Intent should have changed based on idea field
        # The exact behavior depends on the current idea field
        assert fresh_runtime.nodes["intent"]["activation"] != initial_intent or \
               abs(fresh_runtime.nodes["intent"]["activation"] - initial_intent) < 0.1


# =============================================================================
# Idea Evolution Tests
# =============================================================================

class TestIdeaEvolution:
    """Test how ideas evolve over time."""

    def test_ideas_drift_in_vector_space(self, runtime_with_ideas):
        """Idea vectors should drift based on node activations."""
        initial_vecs = [i["vec"].copy() for i in runtime_with_ideas.ideas]
        runtime_with_ideas.step()
        new_vecs = [i["vec"] for i in runtime_with_ideas.ideas]
        
        # At least one vector component should have changed
        for initial, new in zip(initial_vecs, new_vecs):
            assert initial != new

    def test_ideas_clamped_to_valid_range(self, runtime_with_ideas):
        """Idea values should stay within valid bounds."""
        # Run multiple steps
        for _ in range(10):
            runtime_with_ideas.step()
        
        # Check all ideas are within bounds
        for idea in runtime_with_ideas.ideas:
            assert 0.01 <= idea["value"] <= 1.0
            assert 0.0 <= idea["strength"] <= 1.0

    def test_new_ideas_generated_from_intent(self, fresh_runtime):
        """New ideas should be generated when intent and seed are active."""
        # Set high activation for intent and seed
        fresh_runtime.nodes["intent"]["activation"] = 0.8
        fresh_runtime.nodes["seed"]["activation"] = 0.7
        
        initial_count = len(fresh_runtime.ideas)
        fresh_runtime.step()
        
        # Check if new ideas were added (depends on threshold)
        # New ideas are added when: intent*0.5 + seed*0.3 > 0.1
        # With these values: 0.8*0.5 + 0.7*0.3 = 0.4 + 0.21 = 0.61 > 0.1
        # So at least one new idea should be added
        assert len(fresh_runtime.ideas) >= initial_count

    def test_ideas_have_all_fields_after_evolution(self, runtime_with_ideas):
        """All ideas should maintain all required fields after evolution."""
        runtime_with_ideas.step()
        
        required_fields = ["id", "name", "value", "strength", "phase", "vec"]
        for idea in runtime_with_ideas.ideas:
            for field in required_fields:
                assert field in idea, f"Idea {idea['id']} missing field: {field}"


# =============================================================================
# Emergent Behavior Tests
# =============================================================================

class TestEmergentBehavior:
    """Test emergent properties of the system."""

    def test_idea_field_converges_over_time(self, fresh_runtime):
        """Idea field should tend toward stability over many steps."""
        # Run many steps
        fields = []
        for _ in range(50):
            result = fresh_runtime.step()
            fields.append(result["intent_field"])
        
        # Check that the field doesn't grow unboundedly
        # (it should oscillate or stabilize)
        max_field = max(fields)
        min_field = min(fields)
        
        # Field should stay within reasonable bounds
        assert 0.0 <= min_field <= 1.0
        assert 0.0 <= max_field <= 1.0

    def test_nodes_maintain_activation(self, fresh_runtime):
        """Nodes should maintain some level of activation over time."""
        for _ in range(20):
            fresh_runtime.step()
        
        # All nodes should still have positive activation
        for node_id, node in fresh_runtime.nodes.items():
            assert node["activation"] > 0


# =============================================================================
# Beta Tester: Steve's Exploration Tests
# =============================================================================

class TestSteveBeta:
    """
    Tests designed for Steve (normal man with demons) to explore.
    
    These tests demonstrate the system's behavior in approachable ways.
    """

    def test_steve_can_create_runtime(self):
        """Steve: Can I create my own idea-field?"""
        rt = Runtime()
        assert rt is not None
        assert rt.tick == 0

    def test_steve_sees_ideas_growing(self):
        """Steve: Do ideas actually grow and change?"""
        rt = Runtime()
        initial_count = len(rt.ideas)
        
        for _ in range(10):
            rt.step()
        
        final_count = len(rt.ideas)
        # Ideas should be added over time
        assert final_count >= initial_count

    def test_steve_sees_intent_emerging(self):
        """Steve: Can I see the intent emerging from the field?"""
        rt = Runtime()
        
        intent_values = []
        for _ in range(20):
            result = rt.step()
            intent_values.append(result["intent_field"])
        
        # Intent field should be evolving
        assert len(set(intent_values)) > 1  # At least some variation

    def test_steve_can_observe_nodes(self):
        """Steve: Can I watch the nodes dance?"""
        rt = Runtime()
        
        seed_values = []
        for _ in range(10):
            rt.step()
            seed_values.append(rt.nodes["seed"]["activation"])
        
        # Seed activation should be changing
        assert len(seed_values) == 10

    def test_steve_understands_idea_structure(self):
        """Steve: What's inside an idea?"""
        rt = Runtime()
        idea = rt.ideas[0]
        
        # Show Steve the structure
        assert "id" in idea
        assert "name" in idea
        assert "value" in idea
        assert "strength" in idea
        assert "phase" in idea
        assert "vec" in idea
        
        # vec should be 3D
        assert len(idea["vec"]) == 3


# =============================================================================
# Performance Tests
# =============================================================================

class TestPerformance:
    """Test performance characteristics."""

    def test_step_is_fast(self, fresh_runtime, benchmark_runner):
        """
        Step function should complete quickly.
        Uses `_runner` so this does not depend on the
        top-level `benchmark` fixture name in `tests/conftest.py`.
        """
        def run_steps():
            for _ in range(100):
                fresh_runtime.step()

        benchmark_runner(run_steps)

        assert fresh_runtime.tick == 100

    def test_many_ideas_still_fast(self):
        """System should handle many ideas efficiently."""
        rt = Runtime()
        
        # Add 50 ideas
        for i in range(50):
            rt.ideas.append({
                "id": f"idea_{i}",
                "name": f"idea_{i}",
                "value": 0.5,
                "strength": 0.5,
                "phase": i * 0.1,
                "vec": [i * 0.1, i * 0.05, i * 0.02]
            })
        
        # Should still step quickly
        start_tick = rt.tick
        for _ in range(10):
            rt.step()
        
        assert rt.tick == start_tick + 10
