"""Calculate estimated API costs for agent executions."""

from rich.console import Console
from rich.prompt import Prompt, IntPrompt, FloatPrompt
from rich.table import Table

console = Console()

PRICING = {
    "claude-sonnet-4": {"input": 3.00, "output": 15.00},
    "claude-opus-4": {"input": 15.00, "output": 75.00},
    "claude-haiku-3.5": {"input": 0.80, "output": 4.00},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
}


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate cost for a single execution."""
    pricing = PRICING.get(model, PRICING["claude-sonnet-4"])
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    return input_cost + output_cost


def main():
    """Interactive cost calculator."""
    console.print("\n[bold blue]═══ API Cost Calculator ═══[/bold blue]\n")

    # Show available models
    table = Table(title="Available Models")
    table.add_column("Model")
    table.add_column("Input $/M")
    table.add_column("Output $/M")
    for model, prices in PRICING.items():
        table.add_row(model, f"${prices['input']:.2f}", f"${prices['output']:.2f}")
    console.print(table)

    # Get inputs
    model = Prompt.ask("\nModel", default="claude-sonnet-4")
    turns = IntPrompt.ask("Average turns per execution", default=5)
    input_per_turn = IntPrompt.ask("Input tokens per turn", default=2000)
    output_per_turn = IntPrompt.ask("Output tokens per turn", default=500)
    executions = IntPrompt.ask("Executions per day", default=100)

    # Calculate
    total_input = turns * input_per_turn
    total_output = turns * output_per_turn
    cost_per_exec = calculate_cost(model, total_input, total_output)
    daily = cost_per_exec * executions
    monthly = daily * 30

    console.print(f"\n[green]Cost per execution:[/green] ${cost_per_exec:.4f}")
    console.print(f"[green]Daily cost:[/green] ${daily:.2f}")
    console.print(f"[green]Monthly cost:[/green] ${monthly:.2f}")


if __name__ == "__main__":
    main()
