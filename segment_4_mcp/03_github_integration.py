"""
03_github_integration.py - Connecting Agents to GitHub

Patterns for GitHub integration via MCP.
"""

from rich.console import Console
from rich.syntax import Syntax

console = Console()


def show_github_mcp_example():
    """Show GitHub MCP server example."""
    code = '''
from mcp.server import Server
import httpx
import os

server = Server("github-tools")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@server.tool()
async def get_pull_request(repo: str, pr_number: int) -> str:
    """Get details of a pull request."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{repo}/pulls/{pr_number}",
            headers={"Authorization": f"token {GITHUB_TOKEN}"}
        )
        return response.json()

@server.tool()
async def list_issues(repo: str, state: str = "open") -> str:
    """List issues in a repository."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{repo}/issues",
            params={"state": state},
            headers={"Authorization": f"token {GITHUB_TOKEN}"}
        )
        return response.json()

@server.tool()
async def create_comment(repo: str, issue_number: int, body: str) -> str:
    """Create a comment on an issue or PR."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments",
            json={"body": body},
            headers={"Authorization": f"token {GITHUB_TOKEN}"}
        )
        return response.json()
'''
    console.print(Syntax(code, "python", theme="monokai", line_numbers=True))


def main():
    console.print("\n[bold blue]═══ GitHub MCP Integration ═══[/bold blue]\n")
    show_github_mcp_example()

    console.print("\n[yellow]Pre-built GitHub MCP servers available at:[/yellow]")
    console.print("  github.com/modelcontextprotocol/servers")


if __name__ == "__main__":
    main()
