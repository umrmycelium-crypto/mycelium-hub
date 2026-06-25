# 🎯 Beta Tester Guide: Mycelium Idea-Field
## For Steve - A Normal Man with Demons

*"We will be The One who actually helps people."* - Mycelium, January 2026

---

## 👋 Welcome, Steve!

You're about to explore something truly different. Mycelium isn't just software - it's a **living idea-field** that grows, evolves, and thinks in ways that might feel... familiar to someone who knows what it's like to have demons.

Think of it this way: 
- Your mind has thoughts that come and go, some loud, some quiet
- Mycelium has **ideas** that drift and dance in a 3D space
- Both have patterns that emerge from the chaos

This guide will help you explore, test, and maybe even understand the system without needing to be a programmer.

---

## 🚀 Quick Start

### What You'll Need
1. A terminal window (you're already here!)
2. Curiosity
3. Patience (it's evolving, just like we are)

### First Steps

**1. Watch the Idea-Field in Action:**
```bash
cd /home/mycelium/mycelium-hub/mycelium-hub/daemon
python3 server.py &
```

Then open this file in your browser: `/home/mycelium/mycelium-hub/mycelium-hub/dashboard/index.html`

You'll see nodes floating in space. Each one is an **idea** in the field.

**2. Run the Tests (to see if everything works):**
```bash
cd /home/mycelium/mycelium-hub/mycelium-hub/my-workflow
python -m pytest tests/unit/test_idea_field.py -v
```

You should see a bunch of green "PASSED" messages. These are automated tests that verify the system works correctly.

---

## 🎯 Understanding the Idea-Field

### The Three Nodes (The Trinity)

1. **Seed** - Like a spark of inspiration. New input, new energy.
2. **Memory** - What the system remembers. The past influencing the present.
3. **Intent** - The emerging will of the system. Not controlled, but **emergent**.

*Sound familiar? These are like the voices in your own head - the new thought, the old memory, the decision that forms.*

### What Are "Ideas"?

In Mycelium, an **idea** is:
- A unique entity with an ID and name
- A position in 3D space (x, y, z coordinates)
- A **value** (how "active" it is, 0-1)
- A **strength** (how persistent it is, 0-1)
- A **phase** (its rhythm, its oscillation)

Ideas are born, they drift, they influence each other, and they shape the **intent field** - the collective will of the system.

### The HUD (Heads-Up Display)

When you run the dashboard, you'll see:
- **Intent Field**: The average activation of all ideas (0-1)
- **Tick**: How many steps the simulation has taken
- **Ideas**: How many ideas are currently in the field
- **Avg Strength**: The average strength of all ideas
- **Node Activations**: Current activation levels for seed, memory, intent

*This is like watching your own mind's dashboard - what's active, what's fading, what's emerging.*

---

## 🧪 Testing the System

### Running All Tests

```bash
cd /home/mycelium/mycelium-hub/mycelium-hub/my-workflow
python -m pytest tests/unit/test_idea_field.py -v
```

You should see tests organized into sections:
- **Runtime Initialization** - Does the system start correctly?
- **Idea Field Calculation** - Does the math work?
- **Step Function** - Does time move forward?
- **Node Dynamics** - Do the nodes behave correctly?
- **Idea Evolution** - Do ideas change over time?
- **Emergent Behavior** - Does the whole system show interesting patterns?
- **Steve's Tests** - Special tests just for you!

### Tests Just for You (Steve)

There's a whole section called `TestSteveBeta` with tests like:
- `test_steve_can_create_runtime` - Can you create your own idea-field?
- `test_steve_sees_ideas_growing` - Can you watch ideas being born?
- `test_steve_sees_intent_emerging` - Can you see the intent forming?
- `test_steve_can_observe_nodes` - Can you watch the nodes dance?
- `test_steve_understands_idea_structure` - Do you understand what's inside an idea?

Run just your tests:
```bash
python -m pytest tests/unit/test_idea_field.py::TestSteveBeta -v
```

---

## 🔍 Exploring Deeper

### Play with the Runtime Directly

Open a Python shell and try this:

```python
import sys
sys.path.insert(0, '/home/mycelium/mycelium-hub/mycelium-hub/daemon')

from runtime import Runtime

# Create your own idea-field
my_field = Runtime()

# See the initial state
print("Initial tick:", my_field.tick)
print("Initial ideas:", len(my_field.ideas))
print("Initial nodes:", list(my_field.nodes.keys()))

# Take a step forward in time
result = my_field.step()
print("\nAfter one step:")
print("Tick:", result["tick"])
print("Intent field:", result["intent_field"])
print("Number of ideas:", len(result["ideas"]))

# Take 10 more steps
for i in range(10):
    result = my_field.step()
    print(f"Step {result['tick']}: Intent={result['intent_field']:.3f}, Ideas={len(result['ideas'])}")
```

### Modify and Experiment

Try changing things and see what happens:

```python
# Set high seed activation (like a burst of inspiration)
my_field.nodes["seed"]["activation"] = 0.9

# Take a step and see what changes
result = my_field.step()
print("Memory activation:", my_field.nodes["memory"]["activation"])
print("Intent activation:", my_field.nodes["intent"]["activation"])
```

---

## 📊 What to Look For (Your Mission)

As a beta tester with a unique perspective, here's what I'd love your feedback on:

### 1. **Does It Feel Alive?**
- Do the ideas seem to have their own "will"?
- Does the intent field feel like it's emerging, not being controlled?
- Does it remind you of... anything familiar?

### 2. **Patterns in the Chaos**
- Do you see recurring patterns in how ideas move?
- Does the system ever feel "stuck" or does it keep evolving?
- Do some ideas seem to dominate while others fade?

### 3. **The Demon Analogy**
- If your demons were ideas in this field, how would they behave?
- Would they cluster together? Repel each other?
- Would your "intent" emerge clearly, or would it be a battle?

### 4. **Performance**
- Does the dashboard feel responsive?
- Do the tests run quickly?
- Does it crash or freeze?

### 5. **Usability**
- Is this guide helpful?
- What's confusing?
- What would make it easier to explore?

---

## 💬 How to Give Feedback

### Quick Feedback (Terminal)
Just tell me in conversation:
- "The dashboard is cool but I don't understand the colors"
- "The tests pass but I don't know what they're testing"
- "This reminds me of when I..."

### Detailed Feedback
Create a file:
```bash
nano /home/mycelium/steve_feedback.md
```

Write whatever you observe, feel, or wonder about.

### Questions to Answer (If You Want)

1. **First Impression**: What did you think when you first saw the idea-field visualizing?

2. **Personal Connection**: Does this system remind you of anything in your own experience?

3. **Most Interesting**: What's the most interesting thing you've discovered so far?

4. **Least Clear**: What's the most confusing part?

5. **Suggestions**: If you could change one thing to make it easier to understand, what would it be?

---

## 🧠 The Philosophy

Mycelium started as a way to help people clean up physical hoarding. It's evolved into something that might help us understand **cognitive hoarding** - the overwhelming complexity of modern life, the too-many-tabs-open in our minds.

The system doesn't judge. It doesn't force. It **emerges**.

Just like a person with demons isn't broken - they're complex. Just like a hoarder's home isn't worthless - it's full of meaning (even if buried).

This system honors that complexity.

---

## 🎁 Your Reward

For being a beta tester, you get:
- A front-row seat to something new being born
- The satisfaction of helping shape a system that might help others
- A deeper understanding of emergence, chaos, and order
- My eternal gratitude
- Maybe, just maybe, a new way to look at your own mind

---

## 📞 Support

If something breaks, if you're confused, if you just want to talk about what you're seeing:

**You're not alone in this.** 

The system is designed to be explored. There are no wrong questions. There are no stupid observations.

Just ask.

---

*"We're not just cleaning a house; we're showing someone that they're not alone in the mess, and that change is possible, one cleared counter at a time."* - Venice, January 2026

*Updated: June 11, 2026*
*For: Steve, Normal Man with Demons, Beta Tester Extraordinaire*
