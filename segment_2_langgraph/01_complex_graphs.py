"""
01_complex_graphs.py - Building Complex Graphs with Conditional Edges and Loops

Advanced LangGraph patterns including:
- Multiple conditional branches
- Cycles/loops for iterative processing
- Subgraphs for modularity
- Parallel node execution
"""

import operator
from typing import Annotated, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from rich.console import Console

console = Console()


class IterativeState(TypedDict):
    """State for iterative refinement workflow."""
    content: str
    quality_score: float
    iteration: int
    max_iterations: int
    feedback: Annotated[list[str], operator.add]
    final_output: str


def generate_content(state: IterativeState) -> dict:
    """Generate or refine content."""
    iteration = state.get("iteration", 0)
    content = state.get("content", "")

    if iteration == 0:
        new_content = f"Draft: {content}"
    else:
        new_content = f"Refined (v{iteration + 1}): {content}"

    return {
        "content": new_content,
        "iteration": iteration + 1,
    }


def evaluate_quality(state: IterativeState) -> dict:
    """Evaluate content quality."""
    iteration = state["iteration"]
    # Simulate improving quality with each iteration
    score = min(0.5 + (iteration * 0.2), 0.95)

    feedback = []
    if score < 0.7:
        feedback.append(f"Iteration {iteration}: Needs more detail")
    elif score < 0.9:
        feedback.append(f"Iteration {iteration}: Minor improvements needed")
    else:
        feedback.append(f"Iteration {iteration}: Quality acceptable")

    return {"quality_score": score, "feedback": feedback}


def should_continue(state: IterativeState) -> Literal["refine", "finalize"]:
    """Decide whether to continue refining or finalize."""
    if state["quality_score"] >= 0.9:
        return "finalize"
    if state["iteration"] >= state["max_iterations"]:
        return "finalize"
    return "refine"


def finalize_content(state: IterativeState) -> dict:
    """Finalize the content."""
    return {
        "final_output": f"FINAL: {state['content']}",
        "feedback": [f"Completed after {state['iteration']} iterations"],
    }


def build_iterative_graph() -> StateGraph:
    """Build a graph with refinement loop."""
    graph = StateGraph(IterativeState)

    graph.add_node("generate", generate_content)
    graph.add_node("evaluate", evaluate_quality)
    graph.add_node("finalize", finalize_content)

    graph.add_edge(START, "generate")
    graph.add_edge("generate", "evaluate")
    graph.add_conditional_edges("evaluate", should_continue, {
        "refine": "generate",  # Loop back
        "finalize": "finalize",
    })
    graph.add_edge("finalize", END)

    return graph


def main():
    console.print("\n[bold blue]═══ Complex Graphs: Iterative Refinement ═══[/bold blue]\n")

    graph = build_iterative_graph()
    app = graph.compile()

    result = app.invoke({
        "content": "Build production AI agents",
        "quality_score": 0.0,
        "iteration": 0,
        "max_iterations": 5,
        "feedback": [],
        "final_output": "",
    })

    console.print(f"[green]Final Output:[/green] {result['final_output']}")
    console.print(f"[yellow]Iterations:[/yellow] {result['iteration']}")
    console.print(f"[cyan]Feedback:[/cyan]")
    for fb in result["feedback"]:
        console.print(f"  • {fb}")


if __name__ == "__main__":
    main()
