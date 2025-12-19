"""
03_software_team_demo.py - Complete Software Team Demo

A full demonstration of PM, Developer, and QA working together
to complete a feature request.
"""

import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()

try:
    from crewai import Agent, Task, Crew, Process
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False


def create_software_team():
    """Create the full software development team."""

    pm = Agent(
        role="Product Manager",
        goal="Create clear requirements for the login feature",
        backstory="Experienced PM who writes detailed user stories",
        verbose=True,
    )

    dev = Agent(
        role="Senior Developer",
        goal="Implement secure, clean login functionality",
        backstory="Security-focused developer with auth experience",
        verbose=True,
    )

    qa = Agent(
        role="QA Engineer",
        goal="Thoroughly test login for security and usability",
        backstory="Security-minded tester who finds edge cases",
        verbose=True,
    )

    # Define tasks
    req_task = Task(
        description="""Create requirements for a user login feature:
        - Email/password authentication
        - Password reset flow
        - Remember me option
        Output: User stories with acceptance criteria""",
        expected_output="Requirements document with user stories",
        agent=pm,
    )

    dev_task = Task(
        description="""Based on the requirements, design the login implementation:
        - API endpoints needed
        - Security considerations
        - Database schema
        Output: Technical design document""",
        expected_output="Technical design for login feature",
        agent=dev,
        context=[req_task],
    )

    qa_task = Task(
        description="""Create a test plan for the login feature:
        - Test cases for each requirement
        - Security test scenarios
        - Edge cases
        Output: Comprehensive test plan""",
        expected_output="Test plan with test cases",
        agent=qa,
        context=[req_task, dev_task],
    )

    crew = Crew(
        agents=[pm, dev, qa],
        tasks=[req_task, dev_task, qa_task],
        process=Process.sequential,
        verbose=True,
    )

    return crew


def main():
    console.print("\n[bold blue]═══ Software Team Demo ═══[/bold blue]\n")

    if not CREWAI_AVAILABLE:
        console.print("[red]Install crewai: pip install crewai[/red]")
        return

    api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[yellow]Set API key to run this demo[/yellow]")
        console.print("\n[dim]Demo structure:[/dim]")
        console.print("1. PM creates requirements")
        console.print("2. Developer creates technical design")
        console.print("3. QA creates test plan")
        return

    console.print("[cyan]Creating software team...[/cyan]")
    crew = create_software_team()

    console.print("[cyan]Starting feature development...[/cyan]\n")
    result = crew.kickoff(inputs={"feature": "User Login"})

    console.print(Panel(str(result), title="Final Output", border_style="green"))


if __name__ == "__main__":
    main()
