"""Verify course setup is complete."""

import sys
from rich.console import Console
from rich.table import Table

console = Console()


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    return version >= (3, 11), f"{version.major}.{version.minor}.{version.micro}"


def check_package(name: str):
    """Check if a package is installed."""
    try:
        __import__(name)
        return True
    except ImportError:
        return False


def check_env_var(name: str):
    """Check if an environment variable is set."""
    import os
    return bool(os.getenv(name))


def main():
    """Run all verification checks."""
    console.print("\n[bold blue]═══ Setup Verification ═══[/bold blue]\n")

    table = Table(title="Environment Check")
    table.add_column("Check", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Details", style="dim")

    # Python version
    ok, version = check_python_version()
    table.add_row(
        "Python 3.11+",
        "[green]PASS[/green]" if ok else "[red]FAIL[/red]",
        version
    )

    # Core packages
    packages = [
        ("langgraph", "LangGraph"),
        ("crewai", "CrewAI"),
        ("anthropic", "Anthropic SDK"),
        ("openai", "OpenAI SDK"),
        ("rich", "Rich (CLI)"),
    ]

    for pkg, name in packages:
        installed = check_package(pkg)
        table.add_row(
            name,
            "[green]PASS[/green]" if installed else "[yellow]MISSING[/yellow]",
            "pip install " + pkg if not installed else ""
        )

    # Environment variables
    env_vars = [
        ("ANTHROPIC_API_KEY", "Anthropic API Key"),
        ("OPENAI_API_KEY", "OpenAI API Key"),
    ]

    for var, name in env_vars:
        is_set = check_env_var(var)
        table.add_row(
            name,
            "[green]SET[/green]" if is_set else "[yellow]NOT SET[/yellow]",
            ""
        )

    console.print(table)
    console.print("\n[green]Setup verification complete![/green]\n")


if __name__ == "__main__":
    main()
