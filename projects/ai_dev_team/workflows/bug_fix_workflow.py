"""Bug Fix Workflow - Simpler than feature development"""

import operator
from typing import Annotated, Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class BugFixState(TypedDict):
    bug_report: str
    root_cause: str
    fix: str
    verified: bool
    messages: Annotated[list[str], operator.add]


def analyze_bug(state: BugFixState) -> dict:
    return {
        "root_cause": f"Analysis of: {state['bug_report']}",
        "messages": ["Analyzed bug report"],
    }


def implement_fix(state: BugFixState) -> dict:
    return {
        "fix": f"Fix for: {state['root_cause']}",
        "messages": ["Implemented fix"],
    }


def verify_fix(state: BugFixState) -> dict:
    return {
        "verified": True,
        "messages": ["Fix verified"],
    }


def build_bug_fix_workflow():
    graph = StateGraph(BugFixState)

    graph.add_node("analyze", analyze_bug)
    graph.add_node("fix", implement_fix)
    graph.add_node("verify", verify_fix)

    graph.add_edge(START, "analyze")
    graph.add_edge("analyze", "fix")
    graph.add_edge("fix", "verify")
    graph.add_edge("verify", END)

    return graph.compile()
