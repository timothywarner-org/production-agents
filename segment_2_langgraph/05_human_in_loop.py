"""
05_human_in_loop.py - Human-in-the-Loop Patterns

Patterns for critical decisions:
- Interrupt for approval
- Human feedback integration
- Override capabilities
"""

import operator
from typing import Annotated, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from rich.console import Console
from rich.prompt import Confirm

console = Console()


class ApprovalState(TypedDict):
    action: str
    risk_level: str
    approved: bool | None
    executed: bool
    messages: Annotated[list[str], operator.add]


def assess_risk(state: ApprovalState) -> dict:
    """Assess risk level of action."""
    action = state["action"].lower()

    if "delete" in action or "drop" in action:
        risk = "HIGH"
    elif "update" in action or "modify" in action:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {"risk_level": risk, "messages": [f"Risk assessed: {risk}"]}


def route_by_risk(state: ApprovalState) -> Literal["auto_approve", "request_approval"]:
    """Route based on risk level."""
    if state["risk_level"] == "LOW":
        return "auto_approve"
    return "request_approval"


def auto_approve(state: ApprovalState) -> dict:
    return {"approved": True, "messages": ["Auto-approved (low risk)"]}


def request_approval(state: ApprovalState) -> dict:
    """Request human approval."""
    console.print(f"\n[yellow]⚠️  {state['risk_level']} RISK ACTION[/yellow]")
    console.print(f"Action: {state['action']}")

    approved = Confirm.ask("Approve this action?")

    msg = "Human approved" if approved else "Human rejected"
    return {"approved": approved, "messages": [msg]}


def execute_action(state: ApprovalState) -> dict:
    """Execute if approved."""
    if state["approved"]:
        return {"executed": True, "messages": ["Action executed"]}
    return {"executed": False, "messages": ["Action skipped (not approved)"]}


def build_approval_graph():
    graph = StateGraph(ApprovalState)

    graph.add_node("assess", assess_risk)
    graph.add_node("auto_approve", auto_approve)
    graph.add_node("request_approval", request_approval)
    graph.add_node("execute", execute_action)

    graph.add_edge(START, "assess")
    graph.add_conditional_edges("assess", route_by_risk, {
        "auto_approve": "auto_approve",
        "request_approval": "request_approval",
    })
    graph.add_edge("auto_approve", "execute")
    graph.add_edge("request_approval", "execute")
    graph.add_edge("execute", END)

    return graph


def main():
    console.print("\n[bold blue]═══ Human-in-the-Loop Demo ═══[/bold blue]\n")

    graph = build_approval_graph()
    app = graph.compile()

    actions = [
        "Read user profile",
        "Update user email",
        "Delete user account",
    ]

    for action in actions:
        console.print(f"\n[cyan]Processing:[/cyan] {action}")
        result = app.invoke({
            "action": action,
            "risk_level": "",
            "approved": None,
            "executed": False,
            "messages": [],
        })

        console.print(f"  Executed: {result['executed']}")
        for msg in result["messages"]:
            console.print(f"  → {msg}")


if __name__ == "__main__":
    main()
