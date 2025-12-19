"""
04_crewai_intro.py - Introduction to CrewAI: Role-Based Multi-Agent Systems

CrewAI provides a higher-level abstraction for building multi-agent systems
where agents have specific roles, goals, and backstories. This module
introduces the core CrewAI concepts that we'll expand on in Segment 3.

Key Concepts:
- Agents: Individual entities with roles and goals
- Tasks: Work items assigned to agents
- Crews: Teams of agents working together
- Process: How agents coordinate (sequential, hierarchical)
"""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Any

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Load environment variables
load_dotenv()

console = Console()


# =============================================================================
# CrewAI Conceptual Model (Without requiring API keys for demo)
# =============================================================================


class ProcessType(Enum):
    """How agents in a crew coordinate their work."""

    SEQUENTIAL = "sequential"  # One after another
    HIERARCHICAL = "hierarchical"  # Manager delegates to workers
    PARALLEL = "parallel"  # Concurrent execution


@dataclass
class AgentSpec:
    """Specification for a CrewAI agent."""

    role: str
    goal: str
    backstory: str
    tools: list[str]
    allow_delegation: bool = False
    verbose: bool = True

    def display(self) -> None:
        """Display agent specification."""
        console.print(
            Panel(
                f"[bold cyan]Role:[/bold cyan] {self.role}\n"
                f"[bold green]Goal:[/bold green] {self.goal}\n"
                f"[bold yellow]Backstory:[/bold yellow] {self.backstory}\n"
                f"[bold magenta]Tools:[/bold magenta] {', '.join(self.tools)}\n"
                f"[bold blue]Can Delegate:[/bold blue] {self.allow_delegation}",
                title=f"Agent: {self.role}",
                border_style="cyan",
            )
        )


@dataclass
class TaskSpec:
    """Specification for a CrewAI task."""

    description: str
    expected_output: str
    agent_role: str  # Which agent handles this
    context_from: list[str] = None  # Task dependencies

    def __post_init__(self):
        self.context_from = self.context_from or []


@dataclass
class CrewSpec:
    """Specification for a complete crew."""

    name: str
    agents: list[AgentSpec]
    tasks: list[TaskSpec]
    process: ProcessType = ProcessType.SEQUENTIAL


# =============================================================================
# Example: Software Development Crew (Preview of Segment 3)
# =============================================================================


def build_dev_team_spec() -> CrewSpec:
    """
    Build the specification for our AI Software Development Team.

    This is a preview of what we'll build fully in Segment 3.
    """

    # Product Manager Agent
    pm_agent = AgentSpec(
        role="Product Manager",
        goal="Define clear requirements and acceptance criteria that developers can implement",
        backstory="""You are an experienced Product Manager who excels at
        translating business needs into technical requirements. You understand
        both the user perspective and technical constraints. You communicate
        clearly and ensure nothing is ambiguous.""",
        tools=["requirements_template", "user_story_generator"],
        allow_delegation=False,
    )

    # Developer Agent
    dev_agent = AgentSpec(
        role="Senior Developer",
        goal="Implement clean, well-tested code that meets the requirements",
        backstory="""You are a pragmatic senior developer with 10+ years of
        experience. You write maintainable code, follow best practices, and
        always consider edge cases. You prefer simple solutions over clever ones.""",
        tools=["code_writer", "file_reader", "test_runner"],
        allow_delegation=False,
    )

    # QA Tester Agent
    qa_agent = AgentSpec(
        role="QA Engineer",
        goal="Ensure the implementation meets requirements and is bug-free",
        backstory="""You are a meticulous QA engineer who takes pride in
        finding bugs before users do. You think about edge cases, security
        implications, and user experience. You write comprehensive test cases.""",
        tools=["test_writer", "code_reviewer", "bug_reporter"],
        allow_delegation=False,
    )

    # Define tasks
    tasks = [
        TaskSpec(
            description="Analyze the feature request and create detailed requirements with acceptance criteria",
            expected_output="A structured requirements document with user stories and acceptance criteria",
            agent_role="Product Manager",
        ),
        TaskSpec(
            description="Implement the feature according to the requirements",
            expected_output="Working code that implements all requirements",
            agent_role="Senior Developer",
            context_from=["requirements"],
        ),
        TaskSpec(
            description="Review the implementation and write test cases",
            expected_output="Test results and a list of any issues found",
            agent_role="QA Engineer",
            context_from=["requirements", "implementation"],
        ),
    ]

    return CrewSpec(
        name="AI Software Development Team",
        agents=[pm_agent, dev_agent, qa_agent],
        tasks=tasks,
        process=ProcessType.SEQUENTIAL,
    )


# =============================================================================
# CrewAI Code Examples
# =============================================================================


def show_crewai_code() -> None:
    """Display how this would look in actual CrewAI code."""
    code = '''
from crewai import Agent, Task, Crew, Process

# Define agents with roles and goals
product_manager = Agent(
    role="Product Manager",
    goal="Define clear requirements and acceptance criteria",
    backstory="Experienced PM who bridges business and technical needs",
    tools=[requirements_tool],
    verbose=True,
    allow_delegation=False
)

developer = Agent(
    role="Senior Developer",
    goal="Implement clean, tested code that meets requirements",
    backstory="Pragmatic engineer focused on maintainable solutions",
    tools=[code_tool, test_tool],
    verbose=True
)

qa_engineer = Agent(
    role="QA Engineer",
    goal="Ensure implementation is bug-free and meets requirements",
    backstory="Meticulous tester who finds bugs before users do",
    tools=[review_tool, test_tool],
    verbose=True
)

# Define tasks with dependencies
requirements_task = Task(
    description="Analyze feature request and create requirements",
    expected_output="Requirements document with acceptance criteria",
    agent=product_manager
)

implementation_task = Task(
    description="Implement the feature per requirements",
    expected_output="Working code implementation",
    agent=developer,
    context=[requirements_task]  # Depends on requirements
)

testing_task = Task(
    description="Test implementation against requirements",
    expected_output="Test results and bug report",
    agent=qa_engineer,
    context=[requirements_task, implementation_task]
)

# Create the crew
dev_team = Crew(
    agents=[product_manager, developer, qa_engineer],
    tasks=[requirements_task, implementation_task, testing_task],
    process=Process.sequential,  # Execute in order
    verbose=True
)

# Run the crew
result = dev_team.kickoff(
    inputs={"feature_request": "Add user authentication"}
)
'''
    from rich.syntax import Syntax

    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title="CrewAI Code Example", border_style="blue"))


# =============================================================================
# Comparison: LangGraph vs CrewAI
# =============================================================================


def show_comparison() -> None:
    """Compare LangGraph and CrewAI approaches."""
    table = Table(title="LangGraph vs CrewAI")

    table.add_column("Aspect", style="cyan", no_wrap=True)
    table.add_column("LangGraph", style="green")
    table.add_column("CrewAI", style="magenta")

    comparisons = [
        ("Abstraction Level", "Low-level graphs", "High-level roles"),
        ("State Management", "Explicit TypedDict", "Implicit in context"),
        ("Agent Definition", "Node functions", "Agent objects with goals"),
        ("Flow Control", "Edges and routers", "Process types"),
        ("Best For", "Complex stateful workflows", "Role-based collaboration"),
        ("Learning Curve", "Steeper", "Gentler"),
        ("Flexibility", "Maximum", "Opinionated"),
        ("Human-in-Loop", "Built-in patterns", "Tool-based"),
    ]

    for aspect, langgraph, crewai in comparisons:
        table.add_row(aspect, langgraph, crewai)

    console.print(table)


def show_when_to_use() -> None:
    """Display guidance on when to use each framework."""
    guidance = """
[bold cyan]When to Use LangGraph:[/bold cyan]
• Complex state machines with many conditional paths
• Need fine-grained control over execution flow
• Building infrastructure-level agent systems
• Require explicit checkpointing and resumption
• Need to integrate with existing LangChain tooling

[bold magenta]When to Use CrewAI:[/bold magenta]
• Role-based collaboration is natural fit
• Faster prototyping of multi-agent systems
• Team-like problem decomposition
• Want simpler agent definitions
• Building domain-specific agent teams

[bold green]Use Both Together:[/bold green]
• CrewAI for high-level agent coordination
• LangGraph for complex individual agent logic
• LangGraph as a tool within CrewAI agents
"""
    console.print(Panel(guidance, title="Decision Framework", border_style="yellow"))


# =============================================================================
# Demonstration
# =============================================================================


def run_demo() -> None:
    """Run the CrewAI introduction demo."""
    console.print("\n[bold blue]═══ CrewAI Introduction ═══[/bold blue]\n")

    # Show the conceptual model
    console.print("[bold]The AI Software Development Team[/bold]\n")

    crew_spec = build_dev_team_spec()

    console.print(f"[cyan]Crew:[/cyan] {crew_spec.name}")
    console.print(f"[cyan]Process:[/cyan] {crew_spec.process.value}\n")

    console.print("[bold]Agents:[/bold]\n")
    for agent in crew_spec.agents:
        agent.display()
        console.print()

    console.print("[bold]Task Flow:[/bold]\n")
    for i, task in enumerate(crew_spec.tasks, 1):
        deps = f" (depends on: {', '.join(task.context_from)})" if task.context_from else ""
        console.print(
            f"  {i}. [{task.agent_role}] {task.description[:60]}...{deps}"
        )

    console.print("\n")
    show_crewai_code()

    console.print("\n")
    show_comparison()

    console.print("\n")
    show_when_to_use()


def main() -> None:
    """Main entry point."""
    console.print(
        Panel(
            "[bold]Introduction to CrewAI[/bold]\n\n"
            "CrewAI provides a role-based abstraction for multi-agent systems.\n"
            "Agents have roles, goals, and backstories that guide their behavior.\n"
            "This is a preview of Segment 3, where we'll build a complete system.",
            title="Segment 1: CrewAI Introduction",
            border_style="magenta",
        )
    )

    run_demo()

    console.print(
        "\n[bold green]Key Takeaways:[/bold green]\n"
        "1. CrewAI agents are defined by role, goal, and backstory\n"
        "2. Tasks flow between agents based on the process type\n"
        "3. Context from previous tasks informs subsequent work\n"
        "4. CrewAI + LangGraph can be used together\n"
    )


if __name__ == "__main__":
    main()
