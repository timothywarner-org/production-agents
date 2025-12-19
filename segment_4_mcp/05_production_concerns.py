"""
05_production_concerns.py - Production Deployment Considerations

Rate limits, costs, monitoring, and scaling.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def show_rate_limiting():
    """Show rate limiting strategies."""
    table = Table(title="Rate Limiting Strategies")

    table.add_column("Strategy", style="cyan")
    table.add_column("Implementation", style="green")

    table.add_row("Token bucket", "Allow burst, refill over time")
    table.add_row("Fixed window", "N requests per minute")
    table.add_row("Sliding window", "Rolling count of requests")
    table.add_row("Queue-based", "Process requests from queue")

    console.print(table)


def show_cost_controls():
    """Show cost control measures."""
    controls = """
[bold cyan]Cost Control Measures:[/bold cyan]

1. [yellow]Set hard spending limits[/yellow]
   - Daily/monthly caps per project
   - Alert thresholds at 50%, 80%, 95%

2. [yellow]Optimize token usage[/yellow]
   - Use smaller models for simple tasks
   - Truncate context when possible
   - Cache repeated queries

3. [yellow]Implement circuit breakers[/yellow]
   - Stop execution on repeated failures
   - Prevent runaway loops

4. [yellow]Track costs per feature[/yellow]
   - Tag requests by feature/user
   - Identify expensive operations
"""
    console.print(Panel(controls, border_style="yellow"))


def show_monitoring():
    """Show monitoring recommendations."""
    table = Table(title="Key Metrics to Monitor")

    table.add_column("Metric", style="cyan")
    table.add_column("Why", style="green")
    table.add_column("Alert When", style="red")

    table.add_row("Latency P95", "User experience", "> 30s")
    table.add_row("Error rate", "Reliability", "> 5%")
    table.add_row("Token usage", "Cost control", "> budget")
    table.add_row("Agent loops", "Stuck agents", "> 10 iterations")
    table.add_row("Human escalations", "Agent quality", "> 20%")

    console.print(table)


def main():
    console.print("\n[bold blue]═══ Production Concerns ═══[/bold blue]\n")

    show_rate_limiting()
    console.print()
    show_cost_controls()
    console.print()
    show_monitoring()


if __name__ == "__main__":
    main()
