"""Feature Development Workflow using LangGraph + CrewAI"""

import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver


class FeatureState(TypedDict):
    """State for feature development workflow."""
    feature_request: str
    requirements: str
    implementation: str
    test_results: str
    status: str
    messages: Annotated[list[str], operator.add]


def gather_requirements(state: FeatureState) -> dict:
    """PM gathers and documents requirements."""
    return {
        "requirements": f"Requirements for: {state['feature_request']}",
        "messages": ["PM: Requirements documented"],
        "status": "requirements_complete",
    }


def implement_feature(state: FeatureState) -> dict:
    """Developer implements the feature."""
    return {
        "implementation": f"Implementation based on: {state['requirements']}",
        "messages": ["Dev: Implementation complete"],
        "status": "implementation_complete",
    }


def test_feature(state: FeatureState) -> dict:
    """QA tests the implementation."""
    return {
        "test_results": "All tests passed",
        "messages": ["QA: Testing complete"],
        "status": "done",
    }


def build_feature_workflow():
    """Build the feature development workflow."""
    graph = StateGraph(FeatureState)

    graph.add_node("requirements", gather_requirements)
    graph.add_node("implement", implement_feature)
    graph.add_node("test", test_feature)

    graph.add_edge(START, "requirements")
    graph.add_edge("requirements", "implement")
    graph.add_edge("implement", "test")
    graph.add_edge("test", END)

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)


if __name__ == "__main__":
    workflow = build_feature_workflow()
    result = workflow.invoke({
        "feature_request": "Add user login",
        "requirements": "",
        "implementation": "",
        "test_results": "",
        "status": "started",
        "messages": [],
    }, {"configurable": {"thread_id": "feature-1"}})
    print(result)
