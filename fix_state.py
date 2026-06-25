#!/usr/bin/env python3
"""
Script to normalize the Mycelium state file.
Fixes the exponential growth bug in idea strength values.
"""
import json
import sys

STATE_PATH = "/home/mycelium/mycelium-hub/state/latest.json"

def fix_state():
    try:
        with open(STATE_PATH, 'r') as f:
            state = json.load(f)
        
        print(f"Original state:")
        print(f"  Tick: {state.get('tick', 0)}")
        print(f"  Ideas: {len(state.get('ideas', []))}")
        print(f"  Nodes: {len(state.get('nodes', {}))}")
        
        # Check if normalization is needed
        ideas = state.get('ideas', [])
        needs_fix = False
        if ideas:
            max_strength = max((i.get('strength', 0) for i in ideas), default=0)
            if max_strength > 1.0:
                needs_fix = True
                print(f"  Max idea strength: {max_strength} (needs normalization)")
        
        nodes = state.get('nodes', {})
        if nodes:
            max_node = max(nodes.values())
            if max_node > 1.0:
                needs_fix = True
                print(f"  Max node value: {max_node} (needs normalization)")
        
        if not needs_fix:
            print("State is already normalized. No changes needed.")
            return
        
        # Normalize ideas
        for idea in ideas:
            if 'strength' in idea:
                old_strength = idea['strength']
                idea['strength'] = min(1.0, max(0.0, old_strength))
            if 'value' in idea:
                old_value = idea['value']
                idea['value'] = min(1.0, max(0.0, old_value))
        
        # Normalize nodes
        for node_id in nodes:
            nodes[node_id] = min(1.0, max(0.0, nodes[node_id]))
        
        # Normalize intent_field
        if 'intent_field' in state:
            state['intent_field'] = min(1.0, max(0.0, state['intent_field']))
        
        # Save fixed state
        with open(STATE_PATH, 'w') as f:
            json.dump(state, f)
        
        print(f"\nFixed state saved:")
        if ideas:
            max_strength = max((i.get('strength', 0) for i in ideas), default=0)
            avg_strength = sum((i.get('strength', 0) for i in ideas)) / len(ideas)
            print(f"  Max idea strength: {max_strength}")
            print(f"  Avg idea strength: {avg_strength:.4f}")
        
        if nodes:
            max_node = max(nodes.values())
            print(f"  Max node value: {max_node}")
        
        print(f"  Intent field: {state.get('intent_field', 0)}")
        print("\nState normalization complete!")
        
    except FileNotFoundError:
        print(f"Error: State file not found at {STATE_PATH}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in state file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_state()
