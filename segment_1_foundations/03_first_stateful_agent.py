"""
03_first_stateful_agent.py - Demo: Building Your First Stateful Agent

This is the main demo for Segment 1. We build a complete stateful agent
that can:
- Maintain conversation memory
- Make decisions about what to do next
- Use tools to accomplish tasks
- Track its own execution state

This agent helps users analyze text and make decisions based on the analysis.
"""

import asyncio
import operator
import os
from typing import Annotated, Any, Literal, TypedDict

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv()

console = Console()


# =============================================================================
# State Definition
# =============================================================================


class Message(TypedDict):
    """A single message in the conversation."""

    role: Literal["user", "assistant", "system", "tool"]
    content: str


class AgentState(TypedDict):
    """
    Complete state for our stateful agent.

    This state persists across the entire agent execution and can be
    checkpointed for resumption.
    """

    # Conversation history (accumulates)
    messages: Annotated[list[Message], operator.add]

    # Current task being worked on
    current_task: str

    # Analysis results from tools
    analysis: dict[str, Any]

    # Decisions made by the agent
    decisions: Annotated[list[str], operator.add]

    # Execution count for loop detection
    iteration: int

    # Final output
    output: str


# =============================================================================
# Tool Functions (Simulated)
# =============================================================================


def analyze_sentiment(text: str) -> dict[str, Any]:
    """Simulate sentiment analysis tool."""
    # In production, this would call an API or model
    positive_words = {"good", "great", "excellent", "happy", "love", "amazing"}
    negative_words = {"bad", "terrible", "awful", "hate", "sad", "angry"}

    words = set(text.lower().split())
    pos_count = len(words & positive_words)
    neg_count = len(words & negative_words)

    if pos_count > neg_count:
        sentiment = "positive"
        score = 0.7
    elif neg_count > pos_count:
        sentiment = "negative"
        score = 0.3
    else:
        sentiment = "neutral"
        score = 0.5

    return {
        "sentiment": sentiment,
        "score": score,
        "positive_words": list(words & positive_words),
        "negative_words": list(words & negative_words),
    }


def analyze_complexity(text: str) -> dict[str, Any]:
    """Simulate text complexity analysis."""
    words = text.split()
    sentences = text.count(".") + text.count("!") + text.count("?") or 1

    avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
    words_per_sentence = len(words) / sentences

    if avg_word_length > 6 or words_per_sentence > 20:
        complexity = "high"
    elif avg_word_length > 4 or words_per_sentence > 12:
        complexity = "medium"
    else:
        complexity = "low"

    return {
        "complexity": complexity,
        "word_count": len(words),
        "sentence_count": sentences,
        "avg_word_length": round(avg_word_length, 2),
        "words_per_sentence": round(words_per_sentence, 2),
    }


def generate_recommendations(analysis: dict[str, Any]) -> list[str]:
    """Generate recommendations based on analysis."""
    recommendations = []

    sentiment = analysis.get("sentiment_analysis", {}).get("sentiment", "neutral")
    complexity = analysis.get("complexity_analysis", {}).get("complexity", "medium")

    if sentiment == "negative":
        recommendations.append("Consider addressing negative sentiment")
        recommendations.append("Review tone for potential improvements")
    elif sentiment == "positive":
        recommendations.append("Sentiment is positive - maintain this tone")

    if complexity == "high":
        recommendations.append("Consider simplifying complex passages")
        recommendations.append("Break long sentences into shorter ones")
    elif complexity == "low":
        recommendations.append("Text is accessible - good readability")

    return recommendations or ["No specific recommendations"]


# =============================================================================
# Agent Nodes
# =============================================================================


def receive_input(state: AgentState) -> dict:
    """
    Entry node: Receive and validate user input.
    """
    console.print("[dim]Node: receive_input[/dim]")

    task = state.get("current_task", "")

    if not task:
        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": "No task provided. Please provide text to analyze.",
                }
            ],
            "output": "Error: No input provided",
        }

    return {
        "messages": [
            {"role": "assistant", "content": f"Received task: Analyzing '{task[:50]}...'"}
        ],
        "iteration": 0,
    }


def analyze_content(state: AgentState) -> dict:
    """
    Analysis node: Run multiple analysis tools on the content.
    """
    console.print("[dim]Node: analyze_content[/dim]")

    task = state["current_task"]

    # Run both analysis tools
    sentiment_result = analyze_sentiment(task)
    complexity_result = analyze_complexity(task)

    analysis = {
        "sentiment_analysis": sentiment_result,
        "complexity_analysis": complexity_result,
    }

    return {
        "messages": [
            {
                "role": "tool",
                "content": f"Analysis complete: {sentiment_result['sentiment']} sentiment, {complexity_result['complexity']} complexity",
            }
        ],
        "analysis": analysis,
        "decisions": [
            f"Detected {sentiment_result['sentiment']} sentiment (score: {sentiment_result['score']})"
        ],
        "iteration": state.get("iteration", 0) + 1,
    }


def make_decision(state: AgentState) -> dict:
    """
    Decision node: Decide what to do based on analysis.
    """
    console.print("[dim]Node: make_decision[/dim]")

    analysis = state.get("analysis", {})
    recommendations = generate_recommendations(analysis)

    decision_summary = (
        f"Based on analysis, generated {len(recommendations)} recommendations"
    )

    return {
        "messages": [{"role": "assistant", "content": decision_summary}],
        "decisions": [decision_summary],
        "analysis": {**analysis, "recommendations": recommendations},
    }


def generate_output(state: AgentState) -> dict:
    """
    Output node: Generate final output for the user.
    """
    console.print("[dim]Node: generate_output[/dim]")

    analysis = state.get("analysis", {})
    decisions = state.get("decisions", [])

    # Build comprehensive output
    output_parts = [
        "## Analysis Complete\n",
        f"**Sentiment**: {analysis.get('sentiment_analysis', {}).get('sentiment', 'unknown')}",
        f"**Complexity**: {analysis.get('complexity_analysis', {}).get('complexity', 'unknown')}",
        f"**Word Count**: {analysis.get('complexity_analysis', {}).get('word_count', 0)}",
        "\n### Recommendations:",
    ]

    for rec in analysis.get("recommendations", []):
        output_parts.append(f"- {rec}")

    output_parts.append(f"\n### Agent Decisions Made: {len(decisions)}")

    output = "\n".join(output_parts)

    return {
        "messages": [{"role": "assistant", "content": "Analysis complete."}],
        "output": output,
    }


def should_continue(state: AgentState) -> Literal["continue", "finish"]:
    """
    Router: Decide whether to continue analysis or finish.

    This demonstrates the agent's ability to make decisions about its own flow.
    """
    iteration = state.get("iteration", 0)
    analysis = state.get("analysis", {})

    # Simple logic: finish if we have analysis, or hit iteration limit
    if analysis and iteration >= 1:
        return "finish"

    if iteration >= 3:  # Safety limit
        return "finish"

    return "continue"


# =============================================================================
# Graph Construction
# =============================================================================


def build_agent() -> StateGraph:
    """
    Build the complete stateful agent graph.

    Flow:
        START -> receive -> analyze -> decide -> (check) -> output -> END
                                          |          |
                                          └──────────┘
                                          (if more analysis needed)
    """
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("receive", receive_input)
    graph.add_node("analyze", analyze_content)
    graph.add_node("decide", make_decision)
    graph.add_node("output", generate_output)

    # Add edges
    graph.add_edge(START, "receive")
    graph.add_edge("receive", "analyze")
    graph.add_edge("analyze", "decide")

    # Conditional edge: continue analysis or finish
    graph.add_conditional_edges(
        "decide",
        should_continue,
        {
            "continue": "analyze",  # Loop back for more analysis
            "finish": "output",  # Proceed to output
        },
    )

    graph.add_edge("output", END)

    return graph


# =============================================================================
# Demonstration
# =============================================================================


def display_state(state: AgentState) -> None:
    """Display the current agent state in a table."""
    table = Table(title="Agent State")

    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Messages", str(len(state.get("messages", []))))
    table.add_row("Current Task", state.get("current_task", "")[:50] + "...")
    table.add_row("Iteration", str(state.get("iteration", 0)))
    table.add_row("Decisions", str(len(state.get("decisions", []))))
    table.add_row("Has Analysis", str(bool(state.get("analysis"))))

    console.print(table)


def run_demo() -> None:
    """Run the stateful agent demo."""
    console.print("\n[bold blue]═══ First Stateful Agent Demo ═══[/bold blue]\n")

    # Build agent with memory (checkpointing)
    graph = build_agent()
    memory = MemorySaver()
    agent = graph.compile(checkpointer=memory)

    # Sample text to analyze
    sample_text = """
    This is an excellent product! I absolutely love how it works.
    The interface is intuitive and the performance is amazing.
    However, there are some complex configurations that might be
    challenging for new users to understand without documentation.
    """

    console.print("[yellow]Input Text:[/yellow]")
    console.print(Panel(sample_text.strip()))

    # Initial state
    initial_state: AgentState = {
        "messages": [],
        "current_task": sample_text,
        "analysis": {},
        "decisions": [],
        "iteration": 0,
        "output": "",
    }

    # Thread config for memory
    config = {"configurable": {"thread_id": "demo-1"}}

    console.print("\n[cyan]Executing Agent...[/cyan]\n")

    # Run the agent
    result = agent.invoke(initial_state, config)

    console.print("\n[green]═══ Execution Complete ═══[/green]\n")

    # Display results
    display_state(result)

    console.print("\n[yellow]Agent Output:[/yellow]")
    console.print(Panel(result.get("output", "No output"), border_style="green"))

    console.print("\n[yellow]Decisions Made:[/yellow]")
    for decision in result.get("decisions", []):
        console.print(f"  • {decision}")

    # Demonstrate memory persistence
    console.print("\n[cyan]═══ Memory Demonstration ═══[/cyan]")
    console.print(
        "The agent's state is persisted. In a real application, "
        "you could resume this thread later."
    )

    # Show the conversation history
    console.print("\n[yellow]Conversation History:[/yellow]")
    for msg in result.get("messages", [])[:5]:  # Show first 5
        role_color = {
            "user": "blue",
            "assistant": "green",
            "tool": "yellow",
            "system": "red",
        }.get(msg["role"], "white")
        console.print(f"  [{role_color}]{msg['role']}[/{role_color}]: {msg['content']}")


def main() -> None:
    """Main entry point."""
    console.print(
        Panel(
            "[bold]Demo: First Stateful Agent[/bold]\n\n"
            "This demo shows a complete stateful agent that:\n"
            "• Maintains conversation memory\n"
            "• Uses tools for analysis\n"
            "• Makes decisions about its own flow\n"
            "• Persists state for resumption",
            title="Segment 1 Demo",
            border_style="blue",
        )
    )

    run_demo()

    console.print(
        "\n[bold green]Key Takeaways:[/bold green]\n"
        "1. State flows through the graph and accumulates\n"
        "2. Nodes are pure functions that return state updates\n"
        "3. Conditional edges let the agent decide its own path\n"
        "4. Memory (checkpointing) enables persistence and resumption\n"
    )


if __name__ == "__main__":
    main()
