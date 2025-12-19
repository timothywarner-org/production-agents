"""
01_what_is_an_agent.py - Defining Autonomous Agents vs Prompted Chatbots

This module explores the fundamental distinction between:
- Prompted LLMs (chatbots): Stateless, reactive, human-driven
- Autonomous Agents: Stateful, proactive, self-directed with tool use

Key Insight: An agent is defined by its ability to perceive, reason, and act
in a loop - maintaining state and making decisions about what to do next.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


console = Console()


class SystemType(Enum):
    """Classification of AI system types by autonomy level."""

    CHATBOT = "chatbot"
    COPILOT = "copilot"
    AGENT = "agent"
    MULTI_AGENT = "multi_agent"


@dataclass
class AISystemCharacteristics:
    """Characteristics that define an AI system's autonomy level."""

    name: str
    system_type: SystemType
    has_memory: bool
    has_state: bool
    uses_tools: bool
    self_directed: bool
    can_plan: bool
    can_delegate: bool

    @property
    def autonomy_score(self) -> int:
        """Calculate autonomy score (0-6) based on characteristics."""
        return sum(
            [
                self.has_memory,
                self.has_state,
                self.uses_tools,
                self.self_directed,
                self.can_plan,
                self.can_delegate,
            ]
        )


# Example systems for comparison
EXAMPLE_SYSTEMS = [
    AISystemCharacteristics(
        name="Basic ChatGPT",
        system_type=SystemType.CHATBOT,
        has_memory=False,
        has_state=False,
        uses_tools=False,
        self_directed=False,
        can_plan=False,
        can_delegate=False,
    ),
    AISystemCharacteristics(
        name="GitHub Copilot",
        system_type=SystemType.COPILOT,
        has_memory=True,  # Context window
        has_state=False,
        uses_tools=False,  # Suggestions only
        self_directed=False,
        can_plan=False,
        can_delegate=False,
    ),
    AISystemCharacteristics(
        name="Claude with MCP",
        system_type=SystemType.AGENT,
        has_memory=True,
        has_state=True,
        uses_tools=True,
        self_directed=True,
        can_plan=True,
        can_delegate=False,
    ),
    AISystemCharacteristics(
        name="CrewAI Dev Team",
        system_type=SystemType.MULTI_AGENT,
        has_memory=True,
        has_state=True,
        uses_tools=True,
        self_directed=True,
        can_plan=True,
        can_delegate=True,
    ),
]


def display_comparison_table() -> None:
    """Display a comparison table of AI system characteristics."""
    table = Table(title="AI System Autonomy Comparison")

    table.add_column("System", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Memory", justify="center")
    table.add_column("State", justify="center")
    table.add_column("Tools", justify="center")
    table.add_column("Self-Dir", justify="center")
    table.add_column("Planning", justify="center")
    table.add_column("Delegate", justify="center")
    table.add_column("Score", justify="center", style="bold green")

    for system in EXAMPLE_SYSTEMS:
        table.add_row(
            system.name,
            system.system_type.value,
            "Yes" if system.has_memory else "No",
            "Yes" if system.has_state else "No",
            "Yes" if system.uses_tools else "No",
            "Yes" if system.self_directed else "No",
            "Yes" if system.can_plan else "No",
            "Yes" if system.can_delegate else "No",
            str(system.autonomy_score),
        )

    console.print(table)


def display_agent_definition() -> None:
    """Display the formal definition of an autonomous agent."""
    definition = """
[bold cyan]An Autonomous AI Agent is a system that:[/bold cyan]

1. [yellow]PERCEIVES[/yellow] its environment through inputs and tool results
2. [yellow]MAINTAINS STATE[/yellow] across interactions (memory + context)
3. [yellow]REASONS[/yellow] about what actions to take next
4. [yellow]ACTS[/yellow] using tools to affect the environment
5. [yellow]LOOPS[/yellow] until a goal is achieved or intervention occurs

[bold green]The key differentiator:[/bold green] Agents decide their own next steps.
Chatbots wait for human prompts. Agents drive their own execution flow.
"""
    console.print(Panel(definition, title="What Makes an Agent?", border_style="blue"))


def display_agent_loop() -> None:
    """Display the fundamental agent loop diagram."""
    diagram = """
    ┌────────────────────────────────────────────────────────────┐
    │                   THE AGENT LOOP                           │
    ├────────────────────────────────────────────────────────────┤
    │                                                            │
    │         ┌─────────┐                                        │
    │         │  START  │                                        │
    │         └────┬────┘                                        │
    │              │                                             │
    │              ▼                                             │
    │    ┌─────────────────┐                                     │
    │    │    PERCEIVE     │◄─────────────────────────┐          │
    │    │  (get context)  │                          │          │
    │    └────────┬────────┘                          │          │
    │             │                                   │          │
    │             ▼                                   │          │
    │    ┌─────────────────┐                          │          │
    │    │     REASON      │                          │          │
    │    │  (plan action)  │                          │          │
    │    └────────┬────────┘                          │          │
    │             │                                   │          │
    │             ▼                                   │          │
    │    ┌─────────────────┐     ┌────────────┐       │          │
    │    │      ACT        │────▶│ Tool Call  │───────┘          │
    │    │ (execute tool)  │     └────────────┘                  │
    │    └────────┬────────┘                                     │
    │             │                                              │
    │             ▼                                              │
    │    ┌─────────────────┐                                     │
    │    │  GOAL REACHED?  │──── No ────▶ Continue Loop          │
    │    └────────┬────────┘                                     │
    │             │ Yes                                          │
    │             ▼                                              │
    │         ┌───────┐                                          │
    │         │  END  │                                          │
    │         └───────┘                                          │
    │                                                            │
    └────────────────────────────────────────────────────────────┘
"""
    console.print(Panel(diagram, title="Agent Execution Flow", border_style="green"))


def classify_system(
    has_memory: bool = False,
    has_state: bool = False,
    uses_tools: bool = False,
    self_directed: bool = False,
    can_plan: bool = False,
    can_delegate: bool = False,
) -> SystemType:
    """
    Classify an AI system based on its characteristics.

    Args:
        has_memory: Can the system remember previous interactions?
        has_state: Does the system maintain state between actions?
        uses_tools: Can the system use external tools?
        self_directed: Does the system decide its own next steps?
        can_plan: Can the system create multi-step plans?
        can_delegate: Can the system delegate to other agents?

    Returns:
        The SystemType classification
    """
    if can_delegate:
        return SystemType.MULTI_AGENT
    elif self_directed and uses_tools and can_plan:
        return SystemType.AGENT
    elif has_memory or has_state:
        return SystemType.COPILOT
    else:
        return SystemType.CHATBOT


def demonstrate_chatbot_vs_agent() -> None:
    """Demonstrate the difference between chatbot and agent behavior."""
    chatbot_example = """
[bold red]CHATBOT INTERACTION:[/bold red]

User: "What's the status of PR #123?"
Bot:  "I don't have access to your GitHub repository."
User: "Can you check it?"
Bot:  "I'm unable to access external systems."
User: *manually checks GitHub*
User: "It has 2 failing tests"
Bot:  "You should fix those tests before merging."

[dim]→ Human drives every step. Bot only responds.[/dim]
"""

    agent_example = """
[bold green]AGENT INTERACTION:[/bold green]

User: "What's the status of PR #123?"
Agent: *calls GitHub API tool*
       "PR #123 has 2 failing tests in the CI pipeline."
Agent: *calls test analysis tool*
       "The failures are in test_auth.py - null check issue."
Agent: *calls code analysis tool*
       "I've identified the fix: add null guard on line 47."
Agent: "Would you like me to create a fix commit?"

[dim]→ Agent drives the investigation. Asks for approval to act.[/dim]
"""

    console.print(Panel(chatbot_example, border_style="red"))
    console.print(Panel(agent_example, border_style="green"))


def main() -> None:
    """Main entry point for the demonstration."""
    console.print("\n[bold blue]═══ SEGMENT 1: What Is An Agent? ═══[/bold blue]\n")

    display_agent_definition()
    console.print()

    display_agent_loop()
    console.print()

    display_comparison_table()
    console.print()

    demonstrate_chatbot_vs_agent()

    console.print(
        "\n[bold cyan]Key Takeaway:[/bold cyan] "
        "True agents are defined by their ability to autonomously "
        "perceive, reason, and act in a loop—not by how sophisticated "
        "their responses are.\n"
    )


if __name__ == "__main__":
    main()
