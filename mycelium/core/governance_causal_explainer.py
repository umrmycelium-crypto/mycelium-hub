

def explain_causal_chain(chain):
    explanation = []

    for step in chain:
        explanation.append(f"{step['event']} → triggered next stage")

    return {
        "explanation": explanation,
        "length": len(chain)
    }
