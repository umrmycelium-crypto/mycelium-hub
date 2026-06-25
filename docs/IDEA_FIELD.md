# Mycelium Idea-Field: Technical Deep Dive

## Overview

The Mycelium Idea-Field is a novel computational model for representing and evolving cognitive states. Unlike traditional symbolic AI or neural networks, the idea-field treats concepts as **dynamic particles** moving through a continuous multi-dimensional space.

## Mathematical Foundation

### Core Equation

Each idea `i` has a position vector `v_i` in 3D space and evolves according to:

```
dv_i/dt = Σ (w_j * (v_j - v_i)) + F_external + noise
```

Where:
- `w_j` = coupling strength with idea j (based on semantic similarity)
- `F_external` = forces from system nodes (seed, memory, intent)
- `noise` = stochastic exploration term

### Implementation Simplification

Our current implementation uses a discrete-time approximation:

```python
# Vector drift from system nodes
idea["vec"][0] += (nodes["seed"]["activation"] - 0.5) * 0.01
idea["vec"][1] += (nodes["memory"]["activation"] - 0.5) * 0.01
idea["vec"][2] += (nodes["intent"]["activation"] - 0.5) * 0.01

# Field coupling
field = idea_field - idea["value"]
idea["value"] += drift + field * 0.02
```

## Node Dynamics

### Seed Node
- Represents **input/perception**
- High activation = system is receiving new stimuli
- Influences the x-dimension of idea vectors

### Memory Node
- Represents **retention/recall**
- High activation = system is remembering past states
- Influences the y-dimension of idea vectors
- Also drives idea strength through drift mechanism

### Intent Node
- Represents **goal-direction**
- **Emerges** from the idea-field (not controlled top-down)
- High activation = system has strong direction
- Influences the z-dimension of idea vectors

## Idea Lifecycle

### Birth

New ideas are created through two mechanisms:

1. **Stabilization Spawning** (every 30 ticks, max 20 ideas):
   - Creates ideas with random initial conditions
   - Ensures diversity in the field

2. **Intent Coupling** (continuous):
   - New ideas emerge when intent and seed activations combine
   - Strength proportional to: `intent_activation * 0.5 + seed_activation * 0.3`
   - Only spawned if strength > 0.1 threshold

### Evolution

Each tick, every idea:

1. **Vector Drift**: Position updates based on node activations
2. **Field Coupling**: Value adjusts based on distance from field average
3. **Strength Update**: Gradually increases based on memory activation
4. **Phase Oscillation**: Sinusoidal modulation adds temporal dynamics

### Death

Currently, ideas never die - they persist in the field. Future enhancements:
- Strength decay based on relevance
- Pruning of weak ideas
- Fusion of similar ideas

## Field Properties

### Intent Field

The **intent field** is the primary emergent property:

```python
def _idea_field(self):
    if not self.ideas:
        return 0.5
    return sum(i["value"] for i in self.ideas) / len(self.ideas)
```

This simple average creates a **mean-field approximation** where:
- All ideas contribute equally to the collective intent
- High average = system is in an active, exploratory state
- Low average = system is in a restful, consolidated state

### Coupling Behavior

The coupling term `field = idea_field - idea["value"]` creates:

- **Attraction**: Ideas below average are pulled up
- **Repulsion**: Ideas above average are pushed down
- **Result**: Natural clustering around the mean

This is a **negative feedback** mechanism that promotes stability.

## Visualization

### 3D Force-Directed Graph

The dashboard uses Three.js via `3d-force-graph` to render:

- **Nodes**: Ideas and system components
- **Position**: Determined by `vec` [x, y, z]
- **Size**: Proportional to `val` (activation/strength)
- **Color**: Auto-assigned based on node ID
- **Opacity**: Based on activation level

### HUD Information

Real-time display of:
- `Intent Field`: The emergent system intent (0-1)
- `Tick`: Simulation time step
- `Ideas`: Count of active ideas
- `Avg Strength`: Mean idea strength
- Node activations for seed, memory, intent

## Comparison with Other Models

### vs. Neural Networks

| Feature | Idea-Field | Neural Networks |
|---------|-----------|-----------------|
| Representation | Discrete particles | Continuous weights |
| Dynamics | Explicit physics | Backpropagation |
| Interpretability | High | Low |
| Scalability | O(n²) coupling | O(1) per layer |
| Learning | Emergent | Supervised |

### vs. Symbolic AI

| Feature | Idea-Field | Symbolic AI |
|---------|-----------|--------------|
| Representation | Vector positions | Logic rules |
| Reasoning | Emergent | Explicit |
| Flexibility | High | Low |
| Precision | Approximate | Exact |

### vs. Swarm Intelligence

| Feature | Idea-Field | Swarm |
|---------|-----------|-------|
| Agents | Ideas | Particles/ants |
| Space | Continuous 3D | Discrete/continuous |
| Rules | Physics-based | Heuristic |
| Goal | Emergent intent | Task-specific |

## Future Directions

### Enhanced Coupling

```python
# Semantic similarity-based coupling
def semantic_distance(idea1, idea2):
    return euclidean(idea1["vec"], idea2["vec"])

# Coupling strength based on distance
def coupling_strength(distance):
    return exp(-distance / coupling_range)
```

### Idea Fusion

```python
# Merge ideas that are too close
def should_fuse(idea1, idea2):
    return distance < fusion_threshold and similarity > fusion_similarity

def fuse(idea1, idea2):
    return {
        "id": f"fused_{idea1['id']}_{idea2['id']}",
        "vec": [(a+b)/2 for a,b in zip(idea1["vec"], idea2["vec"])],
        "value": (idea1["value"] + idea2["value"])/2,
        "strength": idea1["strength"] + idea2["strength"]
    }
```

### Hierarchical Fields

Nested fields where:
- Local fields cluster similar ideas
- Global field represents overall system state
- Cross-field interactions enable multi-scale reasoning

## Performance Characteristics

### Time Complexity

- **Idea evolution**: O(n) where n = number of ideas
- **Field calculation**: O(n) 
- **Pairwise coupling** (future): O(n²) - requires optimization

### Space Complexity

- **Per idea**: O(1) - constant size data structure
- **Total**: O(n) where n = number of ideas

### Optimization Strategies

1. **Spatial partitioning**: Grid-based neighbor lookup
2. **Barnes-Hut approximation**: For large n, use tree-based methods
3. **Lazy evaluation**: Only update visible ideas in dashboard

## Applications

### Cognitive Modeling
- Simulating thought processes
- Modeling creativity and insight
- Understanding decision making

### Multi-Agent Systems
- Coordination without central control
- Emergent task allocation
- Swarm robotics

### Data Visualization
- Dynamic clustering of high-dimensional data
- Interactive exploration of datasets
- Anomaly detection via field perturbations

### Creative AI
- Idea generation systems
- Artistic concept evolution
- Music composition assistance

## References

1. Strogatz, S. H. (2003). Sync: The emerging science of spontaneous order.
2. Turing, A. M. (1952). The chemical basis of morphogenesis.
3. Wilson, E. O. (1998). Consilience: The unity of knowledge.
4. Holland, J. H. (1992). Adaptation in natural and artificial systems.

---

*Technical specification version: 1.0*  
*Last updated: June 11, 2026*
