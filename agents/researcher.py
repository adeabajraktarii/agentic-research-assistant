from __future__ import annotations
from shared_state import SharedState


def researcher_agent(state: SharedState) -> SharedState:
    # Placeholder: retrieval will be added in the next steps.
    # For now, produce an explicit "not found" note so the system is honest by default.
    state.research_notes = [{
        "claim": "Not found in the sources (retrieval not wired yet).",
        "citations": []
    }]

    state.trace.append({
        "step": "research",
        "agent": "researcher",
        "action": "Attempted document retrieval (not wired yet)",
        "outcome": "No retrieval connected yet; returned safe placeholder note",
    })
    return state
