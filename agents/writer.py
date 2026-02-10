from __future__ import annotations

from typing import List, Dict

from shared_state import SharedState, ResearchNote, Citation


def _format_citations(notes: List[ResearchNote]) -> str:
    lines = []
    seen = set()

    for n in notes:
        for c in n.get("citations", []):
            key = (c.get("source_id"), c.get("location"), c.get("quote"))
            if key in seen:
                continue
            seen.add(key)
            quote = (c.get("quote") or "").replace("\n", " ").strip()
            if len(quote) > 220:
                quote = quote[:220] + "..."
            lines.append(f"- {c.get('source_id')} — {c.get('location')}: \"{quote}\"")

    return "\n".join(lines) if lines else "- None"


def _has_evidence(notes: List[ResearchNote]) -> bool:
    return any(n.get("citations") for n in notes)


def writer_agent(state: SharedState) -> SharedState:
    notes = state.research_notes or []
    has_evidence = _has_evidence(notes)

    # --- Executive Summary ---
    if has_evidence:
        exec_summary = (
            "- Summary based on retrieved evidence from project docs.\n"
            "- See citations for exact supporting excerpts."
        )
    else:
        exec_summary = "- Not found in sources. Provide relevant docs or broaden retrieval."

    # --- Client-ready email ---
    if has_evidence:
        email = (
            "Subject: Weekly Update — Progress, Risks, and Next Steps\n\n"
            "Hi [Client Name],\n\n"
            "Here’s a quick update based on this week’s project notes:\n"
            "- Progress: [supported by citations]\n"
            "- Risks/Watch-outs: [supported by citations]\n"
            "- Next steps: [supported by citations]\n\n"
            "We’ll keep you posted as we hit the next milestones.\n\n"
            "Best,\n"
            "[Your Name]"
        )
    else:
        email = "Not found in sources: cannot draft a grounded client email without evidence."

    # --- Action items (deadlines + owners) ---
    if has_evidence:
        action_items = (
            "- Extracted action items require explicit Owner + Due Date evidence.\n"
            "- If the retrieved chunks don’t include owners/dates, the system will say so in verification."
        )
    else:
        action_items = "Not found in sources: cannot extract deadlines + owners without evidence."

    # Build final draft
    draft = []
    draft.append("## Deliverable Package")
    draft.append("")
    draft.append("### Executive Summary")
    draft.append(exec_summary)
    draft.append("")
    draft.append("### Client Update Email (Draft)")
    draft.append(email)
    draft.append("")
    draft.append("### Action Items (Draft)")
    draft.append(action_items)
    draft.append("")
    draft.append("### Citations")
    draft.append(_format_citations(notes))

    state.draft = "\n".join(draft)

    state.trace.append({
        "step": "draft",
        "agent": "writer",
        "action": "Generated deliverable package (exec summary + client email + action items) using research_notes only",
        "outcome": "Draft created",
    })
    return state

