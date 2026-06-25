# Mycelium Community Hub

Welcome to the Mycelium evolving idea-field! This is a collaborative space for sharing knowledge, patterns, and innovations around autonomous agent systems.

## What is Mycelium?

Mycelium is a self-evolving cognitive architecture that explores emergent intelligence through distributed idea propagation. Unlike traditional branching systems, Mycelium uses a **field-based approach** where ideas evolve as coupled oscillators in a shared semantic space.

### Core Principles

- **Idea-Field Dynamics**: Ideas are not branches but evolving nodes in a continuous field
- **Emergent Intent**: System intent emerges from the collective field, not from forced hierarchies
- **Soft Stabilization**: New ideas are gently integrated, maintaining coherence without rigid control
- **Persistent Evolution**: The system remembers and builds upon its idea history

### The Evolving Idea-Field

The idea-field is a visualization and computational model where:

1. **Nodes** represent core system components (seed, memory, intent)
2. **Ideas** are dynamic entities that drift through the field
3. **Intent Field** is the emergent property that guides system behavior
4. **Vector Drift** allows ideas to move through a 3D semantic space based on system activation

Each idea has:
- `id`: Unique identifier
- `name`: Human-readable label
- `value`: Current activation in the field
- `strength`: Persistence and influence
- `phase`: Temporal oscillation parameter
- `vec`: 3D position vector [x, y, z]

## Getting Started

### Visualizing the Field

Run the dashboard to see the live idea-field:

```bash
cd mycelium-hub/daemon
python3 server.py
```

Then open `dashboard/index.html` in a browser. Connect to `ws://127.0.0.1:8000/ws`

### Understanding the HUD

The Heads-Up Display shows:
- **Intent Field**: Average activation across all ideas (0.0-1.0)
- **Tick**: Current simulation step
- **Idea Count**: Number of active ideas in the field
- **Average Strength**: Mean strength of all ideas
- **Node Activations**: Current activation levels of core nodes

## Contributing

We welcome contributions in the following areas:

### Safe to Share

✅ **Architecture Patterns** - Novel ways to structure agent systems  
✅ **Visualization Techniques** - Better ways to understand system dynamics  
✅ **Documentation** - Clear explanations of concepts and components  
✅ **Examples** - Demonstration workflows and use cases  
✅ **Bug Fixes** - Improvements to stability and correctness  

### Community Guidelines

1. **Safety First**: All shared code must be reviewed for security implications
2. **Transparency**: Document the purpose and behavior of all contributions
3. **Compatibility**: Ensure contributions work with the existing architecture
4. **Testing**: Include tests or validation for new features

### What NOT to Share

❌ **API Keys or Secrets** - Never commit credentials  
❌ **Personal Data** - Avoid user-specific configurations  
❌ **Propietary Code** - Only open-source compatible content  
❌ **Security Vulnerabilities** - Report privately, don't expose  

## Architecture Overview

### Core Components

```
┌─────────────────────────────────────────┐
│               Runtime                     │
│  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │   Seed   │  │  Memory  │  │  Intent │ │
│  │  Node    │  │   Node   │  │  Node   │ │
│  └────┬─────┘  └────┬─────┘  └────┬────┘ │
│       │              │              │       │
│       ▼              ▼              ▼       │
│  ┌─────────────────────────────────────┐ │
│  │         Evolving Idea-Field           │ │
│  │  ┌───────┐ ┌───────┐ ┌───────┐      │ │
│  │  │ Idea  │ │ Idea  │ │ Idea  │ ...   │ │
│  │  │   1   │ │   2   │ │   N   │      │ │
│  │  └───────┘ └───────┘ └───────┘      │ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Idea Evolution Process

1. **Drift**: Ideas move through 3D space based on node activations
2. **Coupling**: Ideas influence each other via field effects
3. **Emergence**: New ideas spawn from intent-memory coupling
4. **Stabilization**: Periodic addition of new ideas maintains diversity

## Current State (June 2026)

The system is in active development with the following capabilities:

- ✅ Real-time 3D visualization of idea-field
- ✅ Emergent intent calculation
- ✅ Dynamic idea generation
- ✅ Vector-based spatial evolution
- ✅ Soft stabilization mechanism

## Roadmap

### Near Term (Next 30 days)

- [ ] Add link visualization between related ideas
- [ ] Implement idea fusion/merging
- [ ] Add persistence layer for idea history
- [ ] Create REST API for field queries

### Long Term (Next 90 days)

- [ ] Multi-agent field interaction
- [ ] Semantic similarity for idea grouping
- [ ] Interactive idea injection
- [ ] Field-based decision making

## Learning Resources

### Key Concepts

- **Emergence**: How complex behavior arises from simple rules
- **Coupled Oscillators**: Mathematical model for synchronized systems
- **Vector Fields**: Using spatial relationships to represent semantics
- **Soft Computing**: Approaches that tolerate imprecision and uncertainty

### Recommended Reading

- "Emergence: The Connected Lives of Ants, Brains, Cities, and Software" - Steven Johnson
- "Sync: The Emerging Science of Spontaneous Order" - Steven Strogatz
- "Complexity: A Guided Tour" - Melanie Mitchell

## Connect with Us

- **Issues & Discussions**: Open on GitHub (coming soon)
- **Documentation**: This file and others in `/docs`
- **Examples**: Check `/examples` directory

## License

All community-contributed content is shared under permissive open-source licenses (MIT or Apache 2.0).

---

*Last updated: June 11, 2026*  
*Status: Actively evolving idea-field*
