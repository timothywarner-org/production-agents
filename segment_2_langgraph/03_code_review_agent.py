"""
03_code_review_agent.py - Demo: Code Review Agent with Multi-File Context

A practical agent that reviews code across multiple files,
maintaining context and providing actionable feedback.
"""

import operator
from typing import Annotated, Literal, TypedDict
from dataclasses import dataclass

from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from rich.console import Console
from rich.panel import Panel

console = Console()


@dataclass
class CodeFile:
    path: str
    content: str
    language: str


class ReviewState(TypedDict):
    files: list[dict]
    current_file_index: int
    reviews: Annotated[list[str], operator.add]
    issues: Annotated[list[str], operator.add]
    summary: str


# Sample files to review
SAMPLE_FILES = [
    CodeFile("auth.py", '''
def login(user, pwd):
    if user == "admin" and pwd == "password123":  # Hardcoded!
        return True
    return check_db(user, pwd)
''', "python"),
    CodeFile("api.py", '''
def get_user(id):
    query = f"SELECT * FROM users WHERE id = {id}"  # SQL injection!
    return db.execute(query)
''', "python"),
]


def load_files(state: ReviewState) -> dict:
    """Load files to review."""
    files = [{"path": f.path, "content": f.content, "language": f.language}
             for f in SAMPLE_FILES]
    return {"files": files, "current_file_index": 0}


def review_current_file(state: ReviewState) -> dict:
    """Review the current file for issues."""
    idx = state["current_file_index"]
    file = state["files"][idx]

    issues = []
    # Simple pattern matching for demo
    if "password" in file["content"].lower():
        issues.append(f"{file['path']}: Potential hardcoded credentials")
    if "f\"SELECT" in file["content"] or "f'SELECT" in file["content"]:
        issues.append(f"{file['path']}: SQL injection vulnerability")

    review = f"Reviewed {file['path']}: {len(issues)} issue(s) found"

    return {
        "reviews": [review],
        "issues": issues,
        "current_file_index": idx + 1,
    }


def should_continue(state: ReviewState) -> Literal["next_file", "summarize"]:
    """Check if more files to review."""
    if state["current_file_index"] < len(state["files"]):
        return "next_file"
    return "summarize"


def generate_summary(state: ReviewState) -> dict:
    """Generate final review summary."""
    total_issues = len(state["issues"])
    summary = f"Code Review Complete: {len(state['files'])} files, {total_issues} issues"
    return {"summary": summary}


def build_review_agent():
    graph = StateGraph(ReviewState)

    graph.add_node("load", load_files)
    graph.add_node("review", review_current_file)
    graph.add_node("summarize", generate_summary)

    graph.add_edge(START, "load")
    graph.add_edge("load", "review")
    graph.add_conditional_edges("review", should_continue, {
        "next_file": "review",
        "summarize": "summarize",
    })
    graph.add_edge("summarize", END)

    return graph


def main():
    console.print("\n[bold blue]═══ Code Review Agent Demo ═══[/bold blue]\n")

    graph = build_review_agent()
    memory = MemorySaver()
    agent = graph.compile(checkpointer=memory)

    config = {"configurable": {"thread_id": "review-1"}}
    result = agent.invoke({
        "files": [],
        "current_file_index": 0,
        "reviews": [],
        "issues": [],
        "summary": "",
    }, config)

    console.print(Panel(result["summary"], title="Summary", border_style="green"))

    console.print("\n[yellow]Issues Found:[/yellow]")
    for issue in result["issues"]:
        console.print(f"  [red]•[/red] {issue}")

    console.print("\n[cyan]Review Log:[/cyan]")
    for review in result["reviews"]:
        console.print(f"  • {review}")


if __name__ == "__main__":
    main()
