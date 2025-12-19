"""
04_error_handling.py - Error Handling and Fallback Strategies

Patterns for resilient agents:
- Try/retry with exponential backoff
- Fallback nodes
- Error state tracking
- Graceful degradation
"""

import operator
import random
from typing import Annotated, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from rich.console import Console

console = Console()


class ResilientState(TypedDict):
    input: str
    attempts: int
    max_attempts: int
    errors: Annotated[list[str], operator.add]
    result: str
    used_fallback: bool


def primary_action(state: ResilientState) -> dict:
    """Primary action that might fail."""
    attempts = state["attempts"] + 1

    # Simulate 60% failure rate
    if random.random() < 0.6:
        return {
            "attempts": attempts,
            "errors": [f"Attempt {attempts}: Primary action failed"],
        }

    return {
        "attempts": attempts,
        "result": f"Success on attempt {attempts}",
        "used_fallback": False,
    }


def fallback_action(state: ResilientState) -> dict:
    """Fallback when primary fails."""
    return {
        "result": "Fallback result (degraded)",
        "used_fallback": True,
        "errors": ["Used fallback after max attempts"],
    }


def route_after_primary(state: ResilientState) -> Literal["retry", "fallback", "done"]:
    """Route based on result."""
    if state.get("result"):
        return "done"
    if state["attempts"] >= state["max_attempts"]:
        return "fallback"
    return "retry"


def build_resilient_graph():
    graph = StateGraph(ResilientState)

    graph.add_node("primary", primary_action)
    graph.add_node("fallback", fallback_action)

    graph.add_edge(START, "primary")
    graph.add_conditional_edges("primary", route_after_primary, {
        "retry": "primary",
        "fallback": "fallback",
        "done": END,
    })
    graph.add_edge("fallback", END)

    return graph


def main():
    console.print("\n[bold blue]═══ Error Handling Demo ═══[/bold blue]\n")

    graph = build_resilient_graph()
    app = graph.compile()

    for i in range(3):
        console.print(f"\n[yellow]Run {i + 1}:[/yellow]")
        result = app.invoke({
            "input": "test",
            "attempts": 0,
            "max_attempts": 3,
            "errors": [],
            "result": "",
            "used_fallback": False,
        })

        console.print(f"  Result: {result['result']}")
        console.print(f"  Attempts: {result['attempts']}")
        console.print(f"  Fallback used: {result['used_fallback']}")
        if result["errors"]:
            console.print(f"  Errors: {result['errors']}")


if __name__ == "__main__":
    main()
