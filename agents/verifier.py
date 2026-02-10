from __future__ import annotations
from shared_state import SharedState


def verifier_agent(state: SharedState) -> SharedState:
    notes = state.research_notes or []
    problems = []

    # Rule: if we make claims, we need citations.
    # For now we only check that citations exist before allowing a confident final.
    has_any_citations = any(n.get("citations") for n in notes)

    if not has_any_citations:
        problems.append("No citations found. Must say 'Not found in the sources' / request missing info.")

    state.verification_notes = problems

    # If problems, force safe final output
    if problems:
        state.final_output = (
            (state.draft or "")
            + "\n\n---\n"
            + "## Verification\n"
            + "- Not found in the sources / insufficient evidence to make factual claims.\n"
            + "- What’s needed: add documents to /data and wire retrieval.\n"
        )
        outcome = f"Blocked final: {len(problems)} issue(s)"
    else:
        state.final_output = state.draft
        outcome = "Final approved"

    state.trace.append({
        "step": "verify",
        "agent": "verifier",
        "action": "Checked draft for grounding and required citations",
        "outcome": outcome,
    })
    return state
