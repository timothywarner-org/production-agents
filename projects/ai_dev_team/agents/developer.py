"""Developer Agent"""

try:
    from crewai import Agent
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False


def create_developer_agent() -> "Agent":
    """Create the Senior Developer agent."""
    if not CREWAI_AVAILABLE:
        raise ImportError("crewai required: pip install crewai")

    return Agent(
        role="Senior Developer",
        goal="Implement clean, secure, well-tested code that meets all requirements",
        backstory="""You are a pragmatic senior developer with 12 years of experience.
        You write maintainable code, follow SOLID principles, and always consider
        security implications. You prefer simple solutions over clever ones and
        believe in the power of good abstractions.""",
        verbose=True,
        allow_delegation=False,
    )
