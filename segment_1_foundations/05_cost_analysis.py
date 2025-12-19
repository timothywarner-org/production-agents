"""
05_cost_analysis.py - Cost Reality Check: When Agents Are Worth It

This module provides a framework for evaluating whether to use agents
for a given use case. It covers:
- Token cost estimation
- Latency considerations
- Error rate impact
- ROI calculation
- Decision framework

Key Insight: Agents are expensive. They should only be used when the
value they provide exceeds the cost of simpler alternatives.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


console = Console()


# =============================================================================
# Cost Models
# =============================================================================


class ModelProvider(Enum):
    """Supported model providers."""

    ANTHROPIC = "anthropic"
    OPENAI = "openai"


@dataclass
class ModelPricing:
    """Pricing per million tokens (as of late 2025)."""

    name: str
    provider: ModelProvider
    input_cost_per_m: float  # Cost per 1M input tokens
    output_cost_per_m: float  # Cost per 1M output tokens
    context_window: int


# Current pricing (update as needed)
MODEL_PRICING = {
    "claude-sonnet-4": ModelPricing(
        name="Claude Sonnet 4",
        provider=ModelProvider.ANTHROPIC,
        input_cost_per_m=3.00,
        output_cost_per_m=15.00,
        context_window=200_000,
    ),
    "claude-opus-4": ModelPricing(
        name="Claude Opus 4",
        provider=ModelProvider.ANTHROPIC,
        input_cost_per_m=15.00,
        output_cost_per_m=75.00,
        context_window=200_000,
    ),
    "claude-haiku-3.5": ModelPricing(
        name="Claude 3.5 Haiku",
        provider=ModelProvider.ANTHROPIC,
        input_cost_per_m=0.80,
        output_cost_per_m=4.00,
        context_window=200_000,
    ),
    "gpt-4o": ModelPricing(
        name="GPT-4o",
        provider=ModelProvider.OPENAI,
        input_cost_per_m=2.50,
        output_cost_per_m=10.00,
        context_window=128_000,
    ),
    "gpt-4o-mini": ModelPricing(
        name="GPT-4o Mini",
        provider=ModelProvider.OPENAI,
        input_cost_per_m=0.15,
        output_cost_per_m=0.60,
        context_window=128_000,
    ),
}


@dataclass
class AgentCostEstimate:
    """Estimated costs for an agent execution."""

    model: str
    avg_turns: int
    input_tokens_per_turn: int
    output_tokens_per_turn: int
    executions_per_day: int

    @property
    def pricing(self) -> ModelPricing:
        return MODEL_PRICING.get(self.model, MODEL_PRICING["claude-sonnet-4"])

    @property
    def cost_per_execution(self) -> float:
        """Calculate cost for a single agent execution."""
        total_input = self.avg_turns * self.input_tokens_per_turn
        total_output = self.avg_turns * self.output_tokens_per_turn

        input_cost = (total_input / 1_000_000) * self.pricing.input_cost_per_m
        output_cost = (total_output / 1_000_000) * self.pricing.output_cost_per_m

        return input_cost + output_cost

    @property
    def daily_cost(self) -> float:
        return self.cost_per_execution * self.executions_per_day

    @property
    def monthly_cost(self) -> float:
        return self.daily_cost * 30


# =============================================================================
# ROI Framework
# =============================================================================


@dataclass
class ROIAnalysis:
    """ROI analysis for agent adoption."""

    name: str
    description: str

    # Costs
    development_hours: int
    hourly_rate: float
    monthly_api_cost: float
    monthly_infrastructure: float

    # Benefits
    hours_saved_per_month: float
    error_reduction_percent: float
    value_per_error_prevented: float
    monthly_errors_before: int

    @property
    def development_cost(self) -> float:
        return self.development_hours * self.hourly_rate

    @property
    def monthly_operating_cost(self) -> float:
        return self.monthly_api_cost + self.monthly_infrastructure

    @property
    def monthly_labor_savings(self) -> float:
        return self.hours_saved_per_month * self.hourly_rate

    @property
    def monthly_error_savings(self) -> float:
        errors_prevented = self.monthly_errors_before * (self.error_reduction_percent / 100)
        return errors_prevented * self.value_per_error_prevented

    @property
    def monthly_net_benefit(self) -> float:
        return (
            self.monthly_labor_savings
            + self.monthly_error_savings
            - self.monthly_operating_cost
        )

    @property
    def payback_months(self) -> Optional[float]:
        if self.monthly_net_benefit <= 0:
            return None  # Never pays back
        return self.development_cost / self.monthly_net_benefit


class UseCaseCategory(Enum):
    """Categories for agent use cases."""

    GOOD_FIT = "good_fit"
    MAYBE = "maybe"
    BAD_FIT = "bad_fit"


@dataclass
class UseCaseEvaluation:
    """Evaluation of whether agents fit a use case."""

    name: str
    category: UseCaseCategory
    reasoning: str
    alternative: Optional[str] = None


# =============================================================================
# Example Evaluations
# =============================================================================


EXAMPLE_USE_CASES = [
    UseCaseEvaluation(
        name="Multi-file code refactoring",
        category=UseCaseCategory.GOOD_FIT,
        reasoning="Requires maintaining context across files, making decisions about dependencies, and validating changes. Agents excel here.",
    ),
    UseCaseEvaluation(
        name="Customer support triage",
        category=UseCaseCategory.GOOD_FIT,
        reasoning="Involves classification, context gathering, and routing. State management helps track conversation history.",
    ),
    UseCaseEvaluation(
        name="Data pipeline orchestration",
        category=UseCaseCategory.GOOD_FIT,
        reasoning="Complex decision trees, error recovery, and multi-step processes benefit from agent architecture.",
    ),
    UseCaseEvaluation(
        name="Simple form validation",
        category=UseCaseCategory.BAD_FIT,
        reasoning="Deterministic logic. Traditional code is faster, cheaper, and more reliable.",
        alternative="Regular expressions and validation libraries",
    ),
    UseCaseEvaluation(
        name="Scheduled report generation",
        category=UseCaseCategory.MAYBE,
        reasoning="If reports are templated, scripts work. If reports require judgment about what to include, agents may help.",
        alternative="Templating engine with parameterized queries",
    ),
    UseCaseEvaluation(
        name="Log parsing and alerting",
        category=UseCaseCategory.BAD_FIT,
        reasoning="Pattern matching at scale. Traditional tools are orders of magnitude faster.",
        alternative="Regex, Elasticsearch, or specialized log tools",
    ),
    UseCaseEvaluation(
        name="Code review assistance",
        category=UseCaseCategory.GOOD_FIT,
        reasoning="Requires understanding context, patterns, and making nuanced judgments about code quality.",
    ),
    UseCaseEvaluation(
        name="API integration testing",
        category=UseCaseCategory.MAYBE,
        reasoning="If testing requires dynamic scenario generation, agents help. Standard tests should use test frameworks.",
        alternative="pytest with fixtures for standard cases",
    ),
]


# =============================================================================
# Display Functions
# =============================================================================


def display_pricing_table() -> None:
    """Display current model pricing."""
    table = Table(title="Model Pricing (per 1M tokens)")

    table.add_column("Model", style="cyan")
    table.add_column("Provider", style="magenta")
    table.add_column("Input", justify="right", style="green")
    table.add_column("Output", justify="right", style="yellow")
    table.add_column("Context", justify="right")

    for model_id, pricing in MODEL_PRICING.items():
        table.add_row(
            pricing.name,
            pricing.provider.value,
            f"${pricing.input_cost_per_m:.2f}",
            f"${pricing.output_cost_per_m:.2f}",
            f"{pricing.context_window:,}",
        )

    console.print(table)


def display_cost_estimate(estimate: AgentCostEstimate) -> None:
    """Display cost estimate for an agent."""
    table = Table(title=f"Cost Estimate: {estimate.pricing.name}")

    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right", style="green")

    table.add_row("Avg turns per execution", str(estimate.avg_turns))
    table.add_row("Input tokens/turn", f"{estimate.input_tokens_per_turn:,}")
    table.add_row("Output tokens/turn", f"{estimate.output_tokens_per_turn:,}")
    table.add_row("Executions/day", str(estimate.executions_per_day))
    table.add_row("", "")
    table.add_row("Cost per execution", f"${estimate.cost_per_execution:.4f}")
    table.add_row("Daily cost", f"${estimate.daily_cost:.2f}")
    table.add_row("[bold]Monthly cost[/bold]", f"[bold]${estimate.monthly_cost:.2f}[/bold]")

    console.print(table)


def display_roi_analysis(roi: ROIAnalysis) -> None:
    """Display ROI analysis."""
    console.print(f"\n[bold cyan]{roi.name}[/bold cyan]")
    console.print(f"[dim]{roi.description}[/dim]\n")

    table = Table(title="ROI Analysis")

    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right", style="green")

    # Costs
    table.add_row("[bold]COSTS[/bold]", "")
    table.add_row("Development cost", f"${roi.development_cost:,.0f}")
    table.add_row("Monthly API cost", f"${roi.monthly_api_cost:,.0f}")
    table.add_row("Monthly infrastructure", f"${roi.monthly_infrastructure:,.0f}")
    table.add_row("Monthly operating", f"${roi.monthly_operating_cost:,.0f}")
    table.add_row("", "")

    # Benefits
    table.add_row("[bold]BENEFITS[/bold]", "")
    table.add_row("Hours saved/month", f"{roi.hours_saved_per_month:.1f}")
    table.add_row("Labor savings/month", f"${roi.monthly_labor_savings:,.0f}")
    table.add_row("Error reduction", f"{roi.error_reduction_percent:.0f}%")
    table.add_row("Error savings/month", f"${roi.monthly_error_savings:,.0f}")
    table.add_row("", "")

    # Net
    table.add_row("[bold]NET[/bold]", "")
    net_color = "green" if roi.monthly_net_benefit > 0 else "red"
    table.add_row(
        "Monthly net benefit",
        f"[{net_color}]${roi.monthly_net_benefit:,.0f}[/{net_color}]"
    )

    if roi.payback_months:
        table.add_row("Payback period", f"{roi.payback_months:.1f} months")
    else:
        table.add_row("Payback period", "[red]Never[/red]")

    console.print(table)


def display_use_case_evaluations() -> None:
    """Display use case evaluations."""
    table = Table(title="Use Case Evaluation Matrix")

    table.add_column("Use Case", style="cyan", no_wrap=True)
    table.add_column("Fit", justify="center")
    table.add_column("Reasoning", style="dim", max_width=40)

    for uc in EXAMPLE_USE_CASES:
        fit_display = {
            UseCaseCategory.GOOD_FIT: "[green]Yes[/green]",
            UseCaseCategory.MAYBE: "[yellow]Maybe[/yellow]",
            UseCaseCategory.BAD_FIT: "[red]No[/red]",
        }[uc.category]

        table.add_row(uc.name, fit_display, uc.reasoning[:80])

    console.print(table)


def display_decision_framework() -> None:
    """Display the decision framework."""
    framework = """
[bold cyan]Agent Decision Framework[/bold cyan]

Ask these questions in order:

[yellow]1. Is the task deterministic?[/yellow]
   → Yes: Use traditional code
   → No: Continue

[yellow]2. Does it require multi-step reasoning?[/yellow]
   → No: Single LLM call may suffice
   → Yes: Continue

[yellow]3. Does it need to maintain state across steps?[/yellow]
   → No: Chain of LLM calls may work
   → Yes: Continue

[yellow]4. Does it need to make decisions about what to do next?[/yellow]
   → No: Scripted workflow may work
   → Yes: [green]Agent is likely appropriate[/green]

[yellow]5. What's the error tolerance?[/yellow]
   → Zero tolerance: Add human-in-the-loop
   → Some tolerance: Full autonomy okay

[bold magenta]Cost Threshold Rule:[/bold magenta]
If an agent execution costs more than the value it creates,
it's not worth it—no matter how cool the technology is.
"""
    console.print(Panel(framework, border_style="blue"))


# =============================================================================
# Main Demo
# =============================================================================


def run_demo() -> None:
    """Run the cost analysis demo."""
    console.print("\n[bold blue]═══ Cost Reality Check ═══[/bold blue]\n")

    # Show pricing
    display_pricing_table()
    console.print()

    # Example cost estimate
    code_review_agent = AgentCostEstimate(
        model="claude-sonnet-4",
        avg_turns=5,
        input_tokens_per_turn=2000,
        output_tokens_per_turn=500,
        executions_per_day=50,
    )
    display_cost_estimate(code_review_agent)
    console.print()

    # Example ROI
    roi = ROIAnalysis(
        name="Code Review Agent",
        description="Automated first-pass code review before human review",
        development_hours=80,
        hourly_rate=150,
        monthly_api_cost=code_review_agent.monthly_cost,
        monthly_infrastructure=100,
        hours_saved_per_month=40,
        error_reduction_percent=30,
        value_per_error_prevented=500,
        monthly_errors_before=10,
    )
    display_roi_analysis(roi)
    console.print()

    # Use case matrix
    display_use_case_evaluations()
    console.print()

    # Decision framework
    display_decision_framework()


def main() -> None:
    """Main entry point."""
    console.print(
        Panel(
            "[bold]Cost Reality Check[/bold]\n\n"
            "Agents are powerful but expensive. This module helps you\n"
            "evaluate whether agents are the right solution for your use case.",
            title="Segment 1: Cost Analysis",
            border_style="yellow",
        )
    )

    run_demo()

    console.print(
        "\n[bold green]Key Takeaways:[/bold green]\n"
        "1. Always calculate cost per execution before building\n"
        "2. Compare agent cost to alternatives (scripts, humans)\n"
        "3. Factor in development time, not just API costs\n"
        "4. Use decision framework to avoid over-engineering\n"
    )


if __name__ == "__main__":
    main()
