"""
07_antipatterns.py - When NOT to Use Agents

Common antipatterns and when simpler solutions work better.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def show_antipatterns():
    """Show common agent antipatterns."""
    table = Table(title="Agent Antipatterns")

    table.add_column("Antipattern", style="red")
    table.add_column("Problem", style="yellow")
    table.add_column("Better Approach", style="green")

    table.add_row(
        "Agent for everything",
        "Expensive, slow, unreliable",
        "Use agents only for complex reasoning"
    )
    table.add_row(
        "No human oversight",
        "Unrecoverable mistakes",
        "Add approval for high-risk actions"
    )
    table.add_row(
        "Unbounded loops",
        "Infinite token usage",
        "Set iteration limits"
    )
    table.add_row(
        "Over-autonomous",
        "Actions without consent",
        "Default to asking, not doing"
    )
    table.add_row(
        "Single point of failure",
        "One agent failure breaks all",
        "Modular, independent agents"
    )
    table.add_row(
        "No fallback",
        "Complete failure on errors",
        "Graceful degradation"
    )

    console.print(table)


def show_decision_tree():
    """Show when to use agents."""
    tree = """
[bold cyan]Decision: Should I Use an Agent?[/bold cyan]

START
  │
  ▼
Is the task deterministic? ──Yes──► Use traditional code
  │
  No
  │
  ▼
Does it need multi-step reasoning? ──No──► Single LLM call
  │
  Yes
  │
  ▼
Does it need tools? ──No──► Chain of prompts
  │
  Yes
  │
  ▼
Does it need to decide its own flow? ──No──► Scripted workflow
  │
  Yes
  │
  ▼
[green]USE AN AGENT[/green]
  │
  ▼
Is it high-stakes? ──Yes──► Add human-in-the-loop
  │
  No
  │
  ▼
[green]FULL AUTONOMY OK[/green]
"""
    console.print(Panel(tree, border_style="blue"))


def main():
    console.print("\n[bold blue]═══ Agent Antipatterns ═══[/bold blue]\n")
    show_antipatterns()
    console.print()
    show_decision_tree()


if __name__ == "__main__":
    main()
