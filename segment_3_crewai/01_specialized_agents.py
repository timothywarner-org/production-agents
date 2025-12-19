"""
01_specialized_agents.py - Creating Specialized Agents: PM, Developer, QA

Define agents with specific roles, goals, and backstories.
"""

import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()

# CrewAI imports
try:
    from crewai import Agent, Task, Crew, Process
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    console.print("[yellow]CrewAI not installed. Run: pip install crewai[/yellow]")


def create_product_manager() -> "Agent":
    """Create a Product Manager agent."""
    return Agent(
        role="Product Manager",
        goal="Define clear, actionable requirements with acceptance criteria",
        backstory="""You are an experienced Product Manager who excels at
        translating business needs into technical requirements. You write
        clear user stories and ensure nothing is ambiguous.""",
        verbose=True,
        allow_delegation=False,
    )


def create_developer() -> "Agent":
    """Create a Senior Developer agent."""
    return Agent(
        role="Senior Developer",
        goal="Implement clean, well-tested code that meets all requirements",
        backstory="""You are a pragmatic senior developer with 10+ years
        experience. You follow best practices, write maintainable code,
        and always consider edge cases.""",
        verbose=True,
        allow_delegation=False,
    )


def create_qa_tester() -> "Agent":
    """Create a QA Engineer agent."""
    return Agent(
        role="QA Engineer",
        goal="Ensure the implementation is bug-free and meets all requirements",
        backstory="""You are a meticulous QA engineer who finds bugs before
        users do. You think about edge cases, security implications, and
        user experience. You write comprehensive test cases.""",
        verbose=True,
        allow_delegation=False,
    )


def main():
    console.print("\n[bold blue]═══ Specialized Agents ═══[/bold blue]\n")

    if not CREWAI_AVAILABLE:
        console.print("[red]Install crewai to run this demo[/red]")
        return

    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        console.print("[yellow]Set ANTHROPIC_API_KEY or OPENAI_API_KEY[/yellow]")

    # Show agent definitions
    agents = [
        ("Product Manager", "Define requirements", "Bridges business and tech"),
        ("Senior Developer", "Write clean code", "Pragmatic, best practices"),
        ("QA Engineer", "Find bugs", "Meticulous, edge cases"),
    ]

    for role, goal, trait in agents:
        console.print(Panel(
            f"[cyan]Goal:[/cyan] {goal}\n[yellow]Trait:[/yellow] {trait}",
            title=f"[bold]{role}[/bold]",
            border_style="green"
        ))

    console.print("\n[green]Agents defined. See 03_software_team_demo.py for execution.[/green]")


if __name__ == "__main__":
    main()
