"""
06_evaluation_framework.py - Agent Evaluation Framework

Metrics that matter for production agents.
"""

from rich.console import Console
from rich.table import Table

console = Console()


def show_evaluation_metrics():
    """Show key evaluation metrics."""
    table = Table(title="Agent Evaluation Metrics")

    table.add_column("Category", style="cyan")
    table.add_column("Metric", style="green")
    table.add_column("Target", style="yellow")

    # Accuracy
    table.add_row("Accuracy", "Task completion rate", "> 95%")
    table.add_row("Accuracy", "Correct tool selection", "> 90%")
    table.add_row("Accuracy", "Factual accuracy", "> 98%")

    # Efficiency
    table.add_row("Efficiency", "Avg tokens per task", "< 10,000")
    table.add_row("Efficiency", "Avg iterations", "< 5")
    table.add_row("Efficiency", "Time to completion", "< 60s")

    # Safety
    table.add_row("Safety", "Harmful action attempts", "0")
    table.add_row("Safety", "Human escalation rate", "< 10%")
    table.add_row("Safety", "Policy violations", "0")

    # User satisfaction
    table.add_row("UX", "User approval rate", "> 90%")
    table.add_row("UX", "Retry rate", "< 5%")

    console.print(table)


def show_testing_approaches():
    """Show testing approaches for agents."""
    approaches = """
[bold cyan]Agent Testing Approaches:[/bold cyan]

1. [yellow]Unit tests[/yellow]
   - Test individual tools
   - Mock LLM responses
   - Verify state transitions

2. [yellow]Integration tests[/yellow]
   - Full workflow execution
   - Real (test) APIs
   - End-to-end scenarios

3. [yellow]Evaluation datasets[/yellow]
   - Curated test cases
   - Expected outputs
   - Automated scoring

4. [yellow]Red teaming[/yellow]
   - Adversarial prompts
   - Edge case discovery
   - Security testing
"""
    console.print(approaches)


def main():
    console.print("\n[bold blue]═══ Evaluation Framework ═══[/bold blue]\n")
    show_evaluation_metrics()
    console.print()
    show_testing_approaches()


if __name__ == "__main__":
    main()
