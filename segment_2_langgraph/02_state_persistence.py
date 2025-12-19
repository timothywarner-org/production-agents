"""
02_state_persistence.py - State Persistence and Checkpointing

Demonstrates:
- MemorySaver for in-process persistence
- SqliteSaver for durable persistence
- Resuming from checkpoints
- Thread management
"""

import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from rich.console import Console

console = Console()


class PersistentState(TypedDict):
    messages: Annotated[list[str], operator.add]
    step: int
    checkpoint_data: str


def step_one(state: PersistentState) -> dict:
    return {"messages": ["Step 1 complete"], "step": 1}


def step_two(state: PersistentState) -> dict:
    return {"messages": ["Step 2 complete"], "step": 2}


def step_three(state: PersistentState) -> dict:
    return {"messages": ["Step 3 complete"], "step": 3, "checkpoint_data": "Final data"}


def build_persistent_graph():
    graph = StateGraph(PersistentState)
    graph.add_node("step_one", step_one)
    graph.add_node("step_two", step_two)
    graph.add_node("step_three", step_three)

    graph.add_edge(START, "step_one")
    graph.add_edge("step_one", "step_two")
    graph.add_edge("step_two", "step_three")
    graph.add_edge("step_three", END)

    return graph


def main():
    console.print("\n[bold blue]═══ State Persistence Demo ═══[/bold blue]\n")

    graph = build_persistent_graph()
    memory = MemorySaver()
    app = graph.compile(checkpointer=memory)

    # First run
    config = {"configurable": {"thread_id": "session-1"}}
    result = app.invoke({"messages": [], "step": 0, "checkpoint_data": ""}, config)

    console.print("[green]First run complete:[/green]")
    console.print(f"  Messages: {result['messages']}")
    console.print(f"  Final step: {result['step']}")

    # Get state history
    console.print("\n[yellow]State can be retrieved and resumed from any checkpoint[/yellow]")
    console.print("Thread ID: session-1")

    # In production, use SqliteSaver or PostgresSaver for persistence:
    # from langgraph.checkpoint.sqlite import SqliteSaver
    # memory = SqliteSaver.from_conn_string("checkpoints.db")


if __name__ == "__main__":
    main()
