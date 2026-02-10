from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from langgraph.graph import StateGraph, END

from shared_state import SharedState
from agents.planner import planner_agent
from agents.researcher import researcher_agent
from agents.writer import writer_agent
from agents.verifier import verifier_agent


def _dict_to_state(state_dict: Dict[str, Any]) -> SharedState:
    """
    Convert a LangGraph state dict -> SharedState dataclass.
    Must always have 'task'. Everything else is optional.
    """
    task = state_dict.get("task", "")
    s = SharedState(task=task)

    # If keys exist, copy them over (keep defaults otherwise)
    for k in ["plan", "research_notes", "draft", "verification_notes", "final_output", "trace", "meta"]:
        if k in state_dict and state_dict[k] is not None:
            setattr(s, k, state_dict[k])
    return s


def _state_to_dict(state: SharedState) -> Dict[str, Any]:
    """Convert SharedState -> plain dict for LangGraph."""
    return asdict(state)


def node_planner(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    s = _dict_to_state(state_dict)
    s = planner_agent(s)
    return _state_to_dict(s)


def node_researcher(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    s = _dict_to_state(state_dict)
    s = researcher_agent(s)
    return _state_to_dict(s)


def node_writer(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    s = _dict_to_state(state_dict)
    s = writer_agent(s)
    return _state_to_dict(s)


def node_verifier(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    s = _dict_to_state(state_dict)
    s = verifier_agent(s)
    return _state_to_dict(s)


def build_graph():
    """
    Builds the required workflow:
    plan -> research -> draft -> verify -> END
    """
    graph = StateGraph(dict)

    graph.add_node("planner", node_planner)
    graph.add_node("researcher", node_researcher)
    graph.add_node("writer", node_writer)
    graph.add_node("verifier", node_verifier)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "verifier")
    graph.add_edge("verifier", END)

    return graph.compile()


def run_task(task: str) -> Dict[str, Any]:
    """
    Convenience runner for UI/testing.
    Returns final state dict containing:
    final_output, trace, citations (inside research_notes), etc.
    """
    app = build_graph()
    initial_state = {"task": task}
    final_state = app.invoke(initial_state)
    return final_state

