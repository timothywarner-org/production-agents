"""Product Manager Agent"""

try:
    from crewai import Agent
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False


def create_pm_agent() -> "Agent":
    """Create the Product Manager agent."""
    if not CREWAI_AVAILABLE:
        raise ImportError("crewai required: pip install crewai")

    return Agent(
        role="Product Manager",
        goal="Transform feature requests into clear, actionable requirements with acceptance criteria",
        backstory="""You are a seasoned Product Manager with 15 years of experience
        in software development. You excel at understanding user needs, writing
        clear user stories, and defining acceptance criteria that leave no room
        for ambiguity. You always consider edge cases and non-functional requirements.""",
        verbose=True,
        allow_delegation=False,
    )
