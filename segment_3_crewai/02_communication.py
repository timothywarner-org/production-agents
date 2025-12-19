"""
02_communication.py - Agent Communication and Delegation

Patterns for agent-to-agent communication:
- Sequential handoffs
- Hierarchical delegation
- Context passing
"""

from rich.console import Console
from rich.table import Table

console = Console()


def show_process_types():
    """Display CrewAI process types."""
    table = Table(title="CrewAI Process Types")

    table.add_column("Process", style="cyan")
    table.add_column("Flow", style="green")
    table.add_column("Best For", style="yellow")

    table.add_row(
        "Sequential",
        "A → B → C",
        "Linear workflows, clear dependencies"
    )
    table.add_row(
        "Hierarchical",
        "Manager → Workers",
        "Complex tasks needing coordination"
    )

    console.print(table)


def show_context_passing():
    """Show how context flows between agents."""
    code = '''
# Context flows via task dependencies
requirements_task = Task(
    description="Write requirements",
    expected_output="Requirements doc",
    agent=pm_agent
)

dev_task = Task(
    description="Implement based on requirements",
    expected_output="Code implementation",
    agent=dev_agent,
    context=[requirements_task]  # Gets PM's output
)

qa_task = Task(
    description="Test against requirements",
    expected_output="Test results",
    agent=qa_agent,
    context=[requirements_task, dev_task]  # Gets both outputs
)
'''
    from rich.syntax import Syntax
    console.print(Syntax(code, "python", theme="monokai"))


def main():
    console.print("\n[bold blue]═══ Agent Communication ═══[/bold blue]\n")

    show_process_types()
    console.print()
    show_context_passing()


if __name__ == "__main__":
    main()
