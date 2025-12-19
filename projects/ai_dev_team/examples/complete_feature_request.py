"""
Complete Feature Request Example

Demonstrates the full AI Dev Team working together.
"""

import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()

try:
    from crewai import Task, Crew, Process
    from ..agents import create_pm_agent, create_developer_agent, create_qa_agent
    AVAILABLE = True
except ImportError:
    AVAILABLE = False


def run_feature_request(feature: str):
    """Run a complete feature request through the team."""
    if not AVAILABLE:
        console.print("[red]Install crewai: pip install crewai[/red]")
        return

    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        console.print("[yellow]Set API key to run[/yellow]")
        return

    console.print(f"\n[bold blue]Feature Request: {feature}[/bold blue]\n")

    # Create agents
    pm = create_pm_agent()
    dev = create_developer_agent()
    qa = create_qa_agent()

    # Create tasks
    req_task = Task(
        description=f"Create detailed requirements for: {feature}",
        expected_output="Requirements document with user stories",
        agent=pm,
    )

    dev_task = Task(
        description="Design technical implementation",
        expected_output="Technical design document",
        agent=dev,
        context=[req_task],
    )

    qa_task = Task(
        description="Create comprehensive test plan",
        expected_output="Test plan with test cases",
        agent=qa,
        context=[req_task, dev_task],
    )

    # Run crew
    crew = Crew(
        agents=[pm, dev, qa],
        tasks=[req_task, dev_task, qa_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    console.print(Panel(str(result), title="Result", border_style="green"))


if __name__ == "__main__":
    run_feature_request("User Authentication with OAuth2")
