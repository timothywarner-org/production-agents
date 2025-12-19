"""
05_parallel_execution.py - Performance Optimization

Parallel vs sequential execution tradeoffs.
"""

from rich.console import Console
from rich.table import Table

console = Console()


def show_execution_comparison():
    """Compare execution strategies."""
    table = Table(title="Execution Strategy Comparison")

    table.add_column("Strategy", style="cyan")
    table.add_column("Speed", style="green")
    table.add_column("Context", style="yellow")
    table.add_column("Use Case", style="magenta")

    table.add_row(
        "Sequential",
        "Slower",
        "Full (each gets previous output)",
        "Dependent tasks"
    )
    table.add_row(
        "Parallel",
        "Faster",
        "Limited (independent)",
        "Independent analysis"
    )
    table.add_row(
        "Hybrid",
        "Balanced",
        "Partial",
        "Mixed dependencies"
    )

    console.print(table)


def show_optimization_tips():
    """Show optimization tips."""
    tips = """
[bold cyan]Optimization Tips:[/bold cyan]

1. [yellow]Batch independent tasks[/yellow]
   Run independent analyses in parallel

2. [yellow]Minimize context passing[/yellow]
   Only pass what's needed, not everything

3. [yellow]Use smaller models for simple tasks[/yellow]
   Not every agent needs the largest model

4. [yellow]Cache common operations[/yellow]
   Store results of repeated tool calls

5. [yellow]Set reasonable timeouts[/yellow]
   Don't let agents loop forever
"""
    console.print(tips)


def main():
    console.print("\n[bold blue]═══ Parallel Execution ═══[/bold blue]\n")
    show_execution_comparison()
    console.print()
    show_optimization_tips()


if __name__ == "__main__":
    main()
