"""
01_mcp_architecture.py - Model Context Protocol Architecture

MCP enables AI models to interact with external tools and data sources
through a standardized protocol.

Components:
- MCP Server: Exposes tools, resources, and prompts
- MCP Client: Connects to servers (e.g., Claude Desktop)
- MCP Host: Runtime environment managing connections
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def show_mcp_architecture():
    """Display MCP architecture diagram."""
    diagram = """
    ┌─────────────────────────────────────────────────────────┐
    │                    MCP ARCHITECTURE                      │
    ├─────────────────────────────────────────────────────────┤
    │                                                          │
    │   ┌──────────────┐         ┌──────────────────────┐     │
    │   │  MCP CLIENT  │◄───────►│     MCP SERVER       │     │
    │   │ (Claude App) │  JSON   │  (Your Tools/Data)   │     │
    │   └──────────────┘  RPC    └──────────────────────┘     │
    │          │                          │                    │
    │          │                          │                    │
    │          ▼                          ▼                    │
    │   ┌──────────────┐         ┌──────────────────────┐     │
    │   │   AI Model   │         │  - Tools (functions) │     │
    │   │   (Claude)   │         │  - Resources (data)  │     │
    │   └──────────────┘         │  - Prompts           │     │
    │                            └──────────────────────┘     │
    │                                                          │
    └─────────────────────────────────────────────────────────┘
    """
    console.print(Panel(diagram, title="MCP Architecture", border_style="blue"))


def show_mcp_primitives():
    """Show the three MCP primitives."""
    table = Table(title="MCP Primitives")

    table.add_column("Primitive", style="cyan")
    table.add_column("Purpose", style="green")
    table.add_column("Example", style="yellow")

    table.add_row(
        "Tools",
        "Functions the model can call",
        "query_database(), send_email()"
    )
    table.add_row(
        "Resources",
        "Data the model can read",
        "file://docs/readme.md"
    )
    table.add_row(
        "Prompts",
        "Reusable prompt templates",
        "summarize_document()"
    )

    console.print(table)


def show_server_example():
    """Show MCP server code example."""
    code = '''
from mcp.server import Server
from mcp.types import Tool

server = Server("my-tools")

@server.tool()
async def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # Call weather API
    return f"Weather in {city}: 72°F, Sunny"

@server.tool()
async def query_database(sql: str) -> str:
    """Execute a read-only SQL query."""
    # Execute query safely
    return await db.execute(sql)

# Run server
if __name__ == "__main__":
    server.run()
'''
    from rich.syntax import Syntax
    console.print(Syntax(code, "python", theme="monokai", line_numbers=True))


def main():
    console.print("\n[bold blue]═══ MCP Architecture ═══[/bold blue]\n")

    show_mcp_architecture()
    console.print()
    show_mcp_primitives()
    console.print("\n[bold]MCP Server Example:[/bold]\n")
    show_server_example()


if __name__ == "__main__":
    main()
