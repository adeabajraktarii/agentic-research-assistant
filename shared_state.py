from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TypedDict


class Citation(TypedDict):
    source_id: str          # e.g., "doc:pricing.pdf#chunk_12"
    quote: str              # short supporting snippet
    location: str           # page/section/chunk info


class ResearchNote(TypedDict):
    claim: str
    citations: List[Citation]


class TraceLogRow(TypedDict):
    step: str               # plan | research | draft | verify
    agent: str              # planner | researcher | writer | verifier
    action: str             # what was attempted
    outcome: str            # result / warnings / not-found


@dataclass
class SharedState:
    # user input
    task: str

    # planner output
    plan: List[str] = field(default_factory=list)

    # researcher output
    research_notes: List[ResearchNote] = field(default_factory=list)

    # writer output
    draft: Optional[str] = None

    # verifier output
    verification_notes: List[str] = field(default_factory=list)

    # final deliverable (what we return to the user)
    final_output: Optional[str] = None

    # transparency / traceability
    trace: List[TraceLogRow] = field(default_factory=list)

    # extra scratch space for tools
    meta: Dict[str, Any] = field(default_factory=dict)
