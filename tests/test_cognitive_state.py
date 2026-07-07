import os
from mycelium.core.cognitive_state import cognitive_state

def test_cognitive_state_lifecycle():
    print("Starting CognitiveState Lifecycle Test...")
    
    # 1. Test Fact Persistence
    print("\n[1] Testing Fact Persistence...")
    cognitive_state.update_fact("user_preference_genre", "Cyberpunk")
    cognitive_state.update_fact("system_mode", "Deep-Work")
    
    # Simulate reload by creating a new instance (though singleton is used, we test the logic)
    from mycelium.core.cognitive_state import CognitiveState
    new_instance = CognitiveState()
    assert new_instance.get_fact("user_preference_genre") == "Cyberpunk", "Fact should persist"
    print("✓ Fact persistence verified.")

    # 2. Test Working Memory sliding window
    print("\n[2] Testing Working Memory...")
    for i in range(20):
        cognitive_state.add_event(f"event_{i}", {"val": i})
    
    # Max history is 15
    assert len(cognitive_state.working_memory) == 15, "Working memory should be capped at 15"
    assert cognitive_state.working_memory[0]['event'] == "event_5", "Oldest events should be evicted"
    print("✓ Working memory window verified.")

    # 3. Test Active Focus and Anaphora Readiness
    print("\n[3] Testing Active Focus...")
    cognitive_state.set_focus("Movie", "Midsommar", {"year": 2019})
    snapshot = cognitive_state.get_snapshot()
    assert "Current Focus: Movie 'Midsommar'" in snapshot, "Snapshot should reflect active focus"
    print("✓ Active focus snapshot verified.")

    # 4. Test Snapshot completeness
    print("\n[4] Testing Snapshot completeness...")
    cognitive_state.add_event("media.search", {"query": "Midsommar"})
    snapshot = cognitive_state.get_snapshot()
    assert "Recent System History:" in snapshot, "Snapshot missing history section"
    assert "Relevant Persistent Facts:" in snapshot, "Snapshot missing facts section"
    assert "user_preference_genre: Cyberpunk" in snapshot, "Snapshot missing persistent facts"
    print("✓ Snapshot completeness verified.")

    print("\nAll CognitiveState tests passed!")

if __name__ == "__main__":
    test_cognitive_state_lifecycle()
