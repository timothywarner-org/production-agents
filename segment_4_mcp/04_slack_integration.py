"""
04_slack_integration.py - Slack Notifications for Agents

Connect agents to Slack for notifications and collaboration.
"""

from rich.console import Console
from rich.syntax import Syntax

console = Console()


def show_slack_mcp_example():
    """Show Slack MCP server example."""
    code = '''
from mcp.server import Server
import httpx
import os

server = Server("slack-tools")
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")

@server.tool()
async def send_message(channel: str, text: str) -> str:
    """Send a message to a Slack channel."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://slack.com/api/chat.postMessage",
            json={"channel": channel, "text": text},
            headers={"Authorization": f"Bearer {SLACK_TOKEN}"}
        )
        return response.json()

@server.tool()
async def get_channel_history(channel: str, limit: int = 10) -> str:
    """Get recent messages from a channel."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://slack.com/api/conversations.history",
            params={"channel": channel, "limit": limit},
            headers={"Authorization": f"Bearer {SLACK_TOKEN}"}
        )
        return response.json()
'''
    console.print(Syntax(code, "python", theme="monokai", line_numbers=True))


def main():
    console.print("\n[bold blue]═══ Slack MCP Integration ═══[/bold blue]\n")
    show_slack_mcp_example()


if __name__ == "__main__":
    main()
