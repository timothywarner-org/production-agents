"""
04_conflict_resolution.py - Managing Agent Conflicts

Strategies for when agents disagree:
- Voting mechanisms
- Hierarchical override
- Human arbitration
"""

from rich.console import Console
from rich.table import Table

console = Console()


def show_conflict_strategies():
    """Display conflict resolution strategies."""
    table = Table(title="Conflict Resolution Strategies")

    table.add_column("Strategy", style="cyan")
    table.add_column("When to Use", style="green")
    table.add_column("Implementation", style="yellow")

    table.add_row(
        "Manager Override",
        "Hierarchical process",
        "Manager agent makes final call"
    )
    table.add_row(
        "Confidence Voting",
        "Peer agents",
        "Agent with highest confidence wins"
    )
    table.add_row(
        "Human Arbitration",
        "High stakes decisions",
        "Pause and ask human"
    )
    table.add_row(
        "Consensus Required",
        "Critical actions",
        "All agents must agree"
    )

    console.print(table)


def main():
    console.print("\n[bold blue]═══ Conflict Resolution ═══[/bold blue]\n")
    show_conflict_strategies()

    console.print("\n[yellow]Key insight:[/yellow] Design for conflict upfront.")
    console.print("Define clear authority hierarchies in your crew.")


if __name__ == "__main__":
    main()
