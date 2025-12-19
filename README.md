# Build Production-Ready AI Agents

[![O'Reilly Live Learning](https://img.shields.io/badge/O'Reilly-Live%20Learning-red)](https://learning.oreilly.com/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.0+-green.svg)](https://www.langchain.com/langgraph)
[![CrewAI](https://img.shields.io/badge/CrewAI-latest-purple.svg)](https://www.crewai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**O'Reilly Live Learning Session | January 12, 2026 | 9am-1pm CST**

Production-ready AI agents go beyond chatbots—they plan, execute, maintain state, and make decisions independently. This course teaches you to build autonomous agents using the enterprise stack that's actually shipping: **LangGraph** for stateful orchestration, **CrewAI** for multi-agent collaboration, and **Claude's Model Context Protocol (MCP)** for universal tool connectivity.

## What You'll Build

A working **AI Software Development Team** with three collaborating agents:

| Agent | Role | Capabilities |
|-------|------|--------------|
| **Product Manager** | Requirements & Planning | Analyzes requests, creates specs, prioritizes tasks |
| **Developer** | Implementation | Writes code, follows patterns, handles edge cases |
| **QA Tester** | Quality Assurance | Reviews code, writes tests, validates functionality |

These agents collaborate to complete real software development tasks—not toy demos.

## Learning Objectives

By the end of this course, you'll be able to:

- Design and deploy **stateful agents** using LangGraph's workflow engine
- Orchestrate **multi-agent systems** with CrewAI for collaborative problem-solving
- Build **MCP servers** to connect agents to databases, APIs, and tools
- Evaluate **agent ROI** with a framework for when to use agents vs. traditional automation

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Python** | 3.11+ with async/await proficiency |
| **LLM Fundamentals** | Experience with ChatGPT, Claude, or similar |
| **Command Line** | Comfortable with pip, venv, environment variables |
| **API Experience** | REST endpoints and JSON |

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/timothywarner-org/production-agents.git
cd production-agents

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

Required API keys:
- `ANTHROPIC_API_KEY` - Claude API (Pro account recommended)
- `OPENAI_API_KEY` - For comparison demos

### 3. Verify Installation

```bash
python -m scripts.verify_setup
```

## Repository Structure

```
production-agents/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .env.example
│
├── segment_1_foundations/          # Agents vs "Agents" - Architecture
│   ├── README.md
│   ├── 01_what_is_an_agent.py      # True agents vs prompted chatbots
│   ├── 02_langgraph_basics.py      # Nodes, edges, state management
│   ├── 03_first_stateful_agent.py  # Demo: Agent with memory
│   ├── 04_crewai_intro.py          # Role-based agents introduction
│   ├── 05_cost_analysis.py         # When agents are worth it
│   └── exercises/
│       └── design_your_workflow.md
│
├── segment_2_langgraph/            # LangGraph Deep Dive
│   ├── README.md
│   ├── 01_complex_graphs.py        # Conditional edges and loops
│   ├── 02_state_persistence.py     # Checkpointing for long-running agents
│   ├── 03_code_review_agent.py     # Demo: Context across files
│   ├── 04_error_handling.py        # Fallback strategies
│   ├── 05_human_in_loop.py         # Critical decision patterns
│   └── exercises/
│       └── add_state_management.py
│
├── segment_3_crewai/               # Multi-Agent Orchestration
│   ├── README.md
│   ├── 01_specialized_agents.py    # PM, Developer, QA Tester roles
│   ├── 02_communication.py         # Agent delegation strategies
│   ├── 03_software_team_demo.py    # End-to-end feature completion
│   ├── 04_conflict_resolution.py   # Managing contradictions
│   ├── 05_parallel_execution.py    # Performance optimization
│   └── exercises/
│       └── two_agent_collab.py
│
├── segment_4_mcp/                  # MCP Servers & Production
│   ├── README.md
│   ├── 01_mcp_architecture.py      # Universal tool protocol
│   ├── 02_database_server/         # Demo: MCP for database access
│   │   ├── server.py
│   │   ├── Dockerfile
│   │   └── README.md
│   ├── 03_github_integration.py    # Connecting to GitHub
│   ├── 04_slack_integration.py     # Connecting to Slack
│   ├── 05_production_concerns.py   # Rate limits, costs, monitoring
│   ├── 06_evaluation_framework.py  # Metrics that matter
│   ├── 07_antipatterns.py          # When NOT to use agents
│   └── exercises/
│       └── architecture_review.md
│
├── projects/
│   └── ai_dev_team/                # Main Course Project
│       ├── README.md
│       ├── agents/
│       │   ├── product_manager.py
│       │   ├── developer.py
│       │   └── qa_tester.py
│       ├── workflows/
│       │   ├── feature_workflow.py
│       │   └── bug_fix_workflow.py
│       ├── mcp_servers/
│       │   ├── github_server/
│       │   └── code_analysis_server/
│       └── examples/
│           └── complete_feature_request.py
│
├── scripts/
│   ├── verify_setup.py             # Verify installation
│   └── cost_calculator.py          # Estimate API costs
│
├── docker/
│   ├── docker-compose.yml
│   └── mcp-servers/
│
└── docs/
    ├── SETUP.md
    ├── TROUBLESHOOTING.md
    └── ARCHITECTURE.md
```

## Course Schedule

### Segment 1: Agents vs "Agents" - Foundations (50 min)

| Topic | File | Description |
|-------|------|-------------|
| What makes a true agent | `01_what_is_an_agent.py` | Autonomous agents vs prompted chatbots |
| LangGraph fundamentals | `02_langgraph_basics.py` | Nodes, edges, state management |
| **Demo**: First stateful agent | `03_first_stateful_agent.py` | Agent with memory and decisions |
| CrewAI introduction | `04_crewai_intro.py` | Role-based agents and delegation |
| Cost reality check | `05_cost_analysis.py` | When agents are worth the investment |

**Exercise**: Design an agent workflow for your use case

### Segment 2: LangGraph Deep Dive (50 min)

| Topic | File | Description |
|-------|------|-------------|
| Complex graphs | `01_complex_graphs.py` | Conditional edges and loops |
| State persistence | `02_state_persistence.py` | Checkpointing for durability |
| **Demo**: Code review agent | `03_code_review_agent.py` | Context across multiple files |
| Error handling | `04_error_handling.py` | Fallback strategies |
| Human-in-the-loop | `05_human_in_loop.py` | Patterns for critical decisions |

**Exercise**: Add state management to a basic agent

### Segment 3: Multi-Agent Orchestration with CrewAI (50 min)

| Topic | File | Description |
|-------|------|-------------|
| Specialized agents | `01_specialized_agents.py` | PM, Developer, QA roles |
| Communication | `02_communication.py` | Delegation strategies |
| **Demo**: Software team | `03_software_team_demo.py` | End-to-end feature completion |
| Conflict resolution | `04_conflict_resolution.py` | Managing agent disagreements |
| Performance | `05_parallel_execution.py` | Parallel vs sequential |

**Exercise**: Build a two-agent collaboration

### Segment 4: MCP Servers & Production (50 min)

| Topic | File | Description |
|-------|------|-------------|
| MCP architecture | `01_mcp_architecture.py` | Universal tool protocol |
| **Demo**: Database MCP | `02_database_server/` | Connect agents to data |
| GitHub integration | `03_github_integration.py` | Real-world connectivity |
| Production concerns | `05_production_concerns.py` | Rate limits, costs, monitoring |
| Evaluation framework | `06_evaluation_framework.py` | Metrics that matter |
| Antipatterns | `07_antipatterns.py` | When NOT to use agents |

**Exercise**: Architecture review of complete system

## Key Concepts

### LangGraph: Stateful Workflows

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Define state that persists across nodes
class AgentState(TypedDict):
    messages: list[BaseMessage]
    current_task: str
    decisions: list[str]

# Build graph with nodes and edges
graph = StateGraph(AgentState)
graph.add_node("analyze", analyze_task)
graph.add_node("execute", execute_task)
graph.add_node("validate", validate_result)

# Add conditional routing
graph.add_conditional_edges("analyze", route_by_complexity)

# Enable persistence
memory = MemorySaver()
app = graph.compile(checkpointer=memory)
```

### CrewAI: Multi-Agent Collaboration

```python
from crewai import Agent, Task, Crew

# Define specialized agents
pm = Agent(
    role="Product Manager",
    goal="Define clear requirements and acceptance criteria",
    backstory="Experienced PM who bridges technical and business needs"
)

developer = Agent(
    role="Senior Developer",
    goal="Implement clean, tested code that meets requirements",
    backstory="Pragmatic engineer focused on maintainable solutions"
)

# Create collaborative crew
crew = Crew(
    agents=[pm, developer],
    tasks=[requirements_task, implementation_task],
    process=Process.sequential  # or Process.hierarchical
)
```

### Claude MCP: Universal Tool Protocol

```python
from mcp.server import Server
from mcp.types import Tool

# Create MCP server
server = Server("database-tools")

@server.tool()
async def query_database(sql: str) -> str:
    """Execute a read-only SQL query"""
    # Connect agents to your database
    return await execute_query(sql)

@server.tool()
async def get_schema(table: str) -> str:
    """Get schema for a database table"""
    return await fetch_schema(table)
```

## Decision Framework: When to Use Agents

| Use Case | Agent? | Why |
|----------|--------|-----|
| Multi-step reasoning with context | Yes | Agents excel at maintaining state |
| Dynamic tool selection | Yes | Agents can choose appropriate tools |
| Simple, predictable workflows | No | Traditional automation is cheaper |
| High-stakes with no review | No | Agents need human oversight |
| One-off data transformation | No | Scripts are more efficient |

## Troubleshooting

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues.

**Quick fixes:**

```bash
# API key issues
echo $ANTHROPIC_API_KEY  # Verify it's set

# Package conflicts
pip install --upgrade langgraph crewai anthropic

# MCP server won't start
docker-compose logs mcp-server
```

## Resources

### Official Documentation
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Anthropic API Reference](https://docs.anthropic.com/)

### Related O'Reilly Content
- [How to Prompt Like a Pro](https://learning.oreilly.com/) - Tim Warner
- [AI Agents at Work](https://learning.oreilly.com/) - Shaun Wassell
- [AI Catalyst: Enterprise Agent Deployments](https://learning.oreilly.com/) - Jon Krohn

## Instructor

**Tim Warner** - Microsoft MVP in Azure AI and Cloud/Datacenter Management (6 years), Microsoft Certified Trainer (25+ years)

- [LinkedIn](https://www.linkedin.com/in/intrepidtechie/)
- [GitHub](https://github.com/timothywarner-org)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Ready to build production-ready agents?** Start with [Segment 1](segment_1_foundations/README.md) or dive into the [AI Dev Team project](projects/ai_dev_team/README.md).
