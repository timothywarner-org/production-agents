"""QA Tester Agent"""

try:
    from crewai import Agent
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False


def create_qa_agent() -> "Agent":
    """Create the QA Engineer agent."""
    if not CREWAI_AVAILABLE:
        raise ImportError("crewai required: pip install crewai")

    return Agent(
        role="QA Engineer",
        goal="Ensure the implementation is bug-free, secure, and meets all requirements",
        backstory="""You are a meticulous QA engineer who takes pride in finding
        bugs before users do. You think about edge cases, security vulnerabilities,
        and user experience. You write comprehensive test cases and aren't afraid
        to push back on incomplete implementations.""",
        verbose=True,
        allow_delegation=False,
    )
