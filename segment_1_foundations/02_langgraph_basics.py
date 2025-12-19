"""
02_langgraph_basics.py - LangGraph Fundamentals: Nodes, Edges, State

This module introduces the core concepts of LangGraph:
- StateGraph: The container for your agent workflow
- Nodes: Individual computation units (functions)
- Edges: Connections between nodes (including conditional routing)
- State: Shared data that flows through the graph

LangGraph transforms agent development from imperative code to declarative graphs.
"""

import operator
from typing import Annotated, Literal, TypedDict

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

# LangGraph imports - these are the core building blocks
from langgraph.graph import END, START, StateGraph


console = Console()


# =============================================================================
# CONCEPT 1: State Definition
# =============================================================================


class SimpleState(TypedDict):
    """
    State is a TypedDict that flows through the graph.

    Every node receives the current state and returns updates to it.
    The state is the "memory" of your agent as it executes.
    """

    # Current message being processed
    message: str

    # History of steps taken (uses reducer to append)
    steps: Annotated[list[str], operator.add]

    # Final result
    result: str


# =============================================================================
# CONCEPT 2: Node Functions
# =============================================================================


def analyze_node(state: SimpleState) -> dict:
    """
    Node 1: Analyze the input message.

    Nodes are just Python functions that:
    1. Receive the current state
    2. Perform some computation
    3. Return a dict of state updates
    """
    message = state["message"]

    # Simulate analysis
    analysis = f"Analyzed: '{message}' - Length: {len(message)} chars"

    # Return state updates (not the full state)
    return {
        "steps": [f"analyze: {analysis}"],
    }


def process_node(state: SimpleState) -> dict:
    """
    Node 2: Process based on analysis.

    This node reads from state (including updates from previous nodes)
    and adds its own processing result.
    """
    message = state["message"]

    # Simulate processing
    processed = message.upper()

    return {
        "steps": [f"process: Converted to uppercase"],
        "result": processed,
    }


def validate_node(state: SimpleState) -> dict:
    """
    Node 3: Validate the result.

    Final validation step before completing.
    """
    result = state.get("result", "")

    validation = "PASS" if len(result) > 0 else "FAIL"

    return {
        "steps": [f"validate: {validation}"],
    }


# =============================================================================
# CONCEPT 3: Building the Graph
# =============================================================================


def build_simple_graph() -> StateGraph:
    """
    Build a simple linear graph: analyze -> process -> validate

    This demonstrates the basic graph construction pattern.
    """
    # Create the graph with our state type
    graph = StateGraph(SimpleState)

    # Add nodes (name -> function mapping)
    graph.add_node("analyze", analyze_node)
    graph.add_node("process", process_node)
    graph.add_node("validate", validate_node)

    # Add edges (linear flow)
    graph.add_edge(START, "analyze")  # Entry point
    graph.add_edge("analyze", "process")
    graph.add_edge("process", "validate")
    graph.add_edge("validate", END)  # Exit point

    return graph


# =============================================================================
# CONCEPT 4: Conditional Edges
# =============================================================================


class ConditionalState(TypedDict):
    """State for demonstrating conditional routing."""

    input_type: str
    message: str
    steps: Annotated[list[str], operator.add]
    result: str


def classify_input(state: ConditionalState) -> dict:
    """Classify the input to determine routing."""
    message = state["message"]

    # Simple classification logic
    if message.startswith("URGENT"):
        input_type = "urgent"
    elif message.startswith("?"):
        input_type = "question"
    else:
        input_type = "standard"

    return {
        "input_type": input_type,
        "steps": [f"classify: type={input_type}"],
    }


def handle_urgent(state: ConditionalState) -> dict:
    """Handle urgent messages with priority processing."""
    return {
        "steps": ["handle_urgent: Priority processing applied"],
        "result": f"[URGENT] {state['message']}",
    }


def handle_question(state: ConditionalState) -> dict:
    """Handle questions with appropriate response."""
    return {
        "steps": ["handle_question: Formulating answer"],
        "result": f"Answer to: {state['message']}",
    }


def handle_standard(state: ConditionalState) -> dict:
    """Handle standard messages."""
    return {
        "steps": ["handle_standard: Normal processing"],
        "result": f"Processed: {state['message']}",
    }


def route_by_type(state: ConditionalState) -> Literal["urgent", "question", "standard"]:
    """
    Router function for conditional edges.

    This function examines the state and returns the name of the next node.
    The return value must match one of the node names in the graph.
    """
    return state["input_type"]


def build_conditional_graph() -> StateGraph:
    """
    Build a graph with conditional routing.

    Flow:
        START -> classify -> (route) -> handle_* -> END
                              |
                              ├─> urgent -> END
                              ├─> question -> END
                              └─> standard -> END
    """
    graph = StateGraph(ConditionalState)

    # Add all nodes
    graph.add_node("classify", classify_input)
    graph.add_node("urgent", handle_urgent)
    graph.add_node("question", handle_question)
    graph.add_node("standard", handle_standard)

    # Entry edge
    graph.add_edge(START, "classify")

    # Conditional edges from classify node
    graph.add_conditional_edges(
        "classify",  # Source node
        route_by_type,  # Router function
        {
            # Mapping: router return value -> destination node
            "urgent": "urgent",
            "question": "question",
            "standard": "standard",
        },
    )

    # All handlers lead to END
    graph.add_edge("urgent", END)
    graph.add_edge("question", END)
    graph.add_edge("standard", END)

    return graph


# =============================================================================
# Demonstrations
# =============================================================================


def demonstrate_simple_graph() -> None:
    """Run the simple linear graph."""
    console.print("\n[bold cyan]═══ Simple Linear Graph ═══[/bold cyan]\n")

    graph = build_simple_graph()
    app = graph.compile()

    # Execute with initial state
    initial_state = {
        "message": "Hello, LangGraph!",
        "steps": [],
        "result": "",
    }

    console.print(f"[yellow]Input:[/yellow] {initial_state['message']}\n")

    result = app.invoke(initial_state)

    console.print("[green]Execution Steps:[/green]")
    for step in result["steps"]:
        console.print(f"  • {step}")

    console.print(f"\n[green]Result:[/green] {result['result']}")


def demonstrate_conditional_graph() -> None:
    """Run the conditional routing graph with different inputs."""
    console.print("\n[bold cyan]═══ Conditional Routing Graph ═══[/bold cyan]\n")

    graph = build_conditional_graph()
    app = graph.compile()

    test_messages = [
        "URGENT: Server is down!",
        "? What is LangGraph?",
        "Regular message here",
    ]

    for message in test_messages:
        initial_state = {
            "input_type": "",
            "message": message,
            "steps": [],
            "result": "",
        }

        result = app.invoke(initial_state)

        console.print(f"[yellow]Input:[/yellow] {message}")
        console.print(f"[blue]Route:[/blue] {result['input_type']}")
        console.print(f"[green]Result:[/green] {result['result']}")
        console.print()


def show_graph_code() -> None:
    """Display the graph building code with syntax highlighting."""
    code = '''
# LangGraph Pattern: Building a Stateful Agent Graph

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator

# 1. Define your state
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]  # Accumulates
    current_step: str                         # Overwrites

# 2. Define node functions
def my_node(state: AgentState) -> dict:
    # Read state, do work, return updates
    return {"current_step": "completed"}

# 3. Build the graph
graph = StateGraph(AgentState)
graph.add_node("my_node", my_node)
graph.add_edge(START, "my_node")
graph.add_edge("my_node", END)

# 4. Compile and run
app = graph.compile()
result = app.invoke({"messages": [], "current_step": ""})
'''

    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title="LangGraph Pattern", border_style="blue"))


def main() -> None:
    """Main entry point for the demonstration."""
    console.print("\n[bold blue]═══ SEGMENT 1: LangGraph Basics ═══[/bold blue]\n")

    show_graph_code()

    demonstrate_simple_graph()

    demonstrate_conditional_graph()

    console.print(
        Panel(
            "[bold]Key Concepts Covered:[/bold]\n\n"
            "1. [cyan]State[/cyan]: TypedDict that flows through the graph\n"
            "2. [cyan]Nodes[/cyan]: Functions that receive state and return updates\n"
            "3. [cyan]Edges[/cyan]: Connections between nodes\n"
            "4. [cyan]Conditional Edges[/cyan]: Router functions for dynamic flow\n"
            "5. [cyan]START/END[/cyan]: Special nodes for entry/exit\n",
            title="Summary",
            border_style="green",
        )
    )


if __name__ == "__main__":
    main()
