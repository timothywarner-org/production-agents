# Segment 1: Agents vs "Agents" - Foundations & Architecture

**Duration**: 50 minutes + 10 min Q&A

This segment establishes the foundation for understanding what makes a true autonomous agent versus a sophisticated chatbot. You'll learn the core concepts of LangGraph and CrewAI, and develop a framework for evaluating when agents are the right solution.

## Learning Objectives

By the end of this segment, you will:

1. Distinguish between true autonomous agents and prompted chatbots
2. Understand LangGraph's node/edge/state architecture
3. Build your first stateful agent with memory and decision-making
4. Grasp CrewAI's role-based agent paradigm
5. Evaluate cost/benefit tradeoffs for agent adoption

## Files in This Segment

| File | Description | Run Time |
|------|-------------|----------|
| `01_what_is_an_agent.py` | Defines autonomous agents vs chatbots | Demo |
| `02_langgraph_basics.py` | Nodes, edges, and state management | Interactive |
| `03_first_stateful_agent.py` | **Demo**: Agent with memory | 5 min |
| `04_crewai_intro.py` | Role-based agents introduction | Demo |
| `05_cost_analysis.py` | When agents are worth it | Discussion |

## Key Concepts

### What Makes a True Agent?

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHATBOT vs AGENT                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   CHATBOT (Prompted LLM)          AUTONOMOUS AGENT              │
│   ────────────────────           ────────────────               │
│   • Single turn                  • Multi-turn with memory       │
│   • Stateless                    • Stateful (persists context)  │
│   • Human drives flow            • Agent drives flow            │
│   • No tool use                  • Dynamic tool selection       │
│   • Responds to prompts          • Plans and executes           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### The Agent Loop

```
        ┌──────────────────────────────────────┐
        │                                      │
        ▼                                      │
    ┌───────┐      ┌───────┐      ┌───────┐   │
    │OBSERVE│ ──▶  │ THINK │ ──▶  │  ACT  │ ──┘
    └───────┘      └───────┘      └───────┘
        │              │              │
        │              │              │
    Perceive       Reason &       Execute
    environment    plan next      actions
                   steps
```

### LangGraph Architecture

```python
# State flows through the graph
State ─▶ [Node A] ─▶ [Node B] ─▶ [Node C] ─▶ Result
              │           │
              └───────────┘
              (conditional edge)
```

## Running the Examples

```bash
# Ensure you're in the repo root with venv activated
cd production-agents
source .venv/bin/activate

# Run individual examples
python -m segment_1_foundations.01_what_is_an_agent
python -m segment_1_foundations.02_langgraph_basics
python -m segment_1_foundations.03_first_stateful_agent
python -m segment_1_foundations.04_crewai_intro
python -m segment_1_foundations.05_cost_analysis
```

## Mini-Exercise: Design Your Agent Workflow

See `exercises/design_your_workflow.md` for the exercise template.

**Task**: Sketch an agent workflow for a use case relevant to your work.

Consider:
- What's the input/trigger?
- What decisions does the agent need to make?
- What tools does it need access to?
- Where might it fail, and how should it recover?
- Does it need human approval at any step?

## Discussion Points

1. **The Autonomy Spectrum**: Where do your current automations fall?
2. **Cost vs Value**: What's the ROI breakeven for agent adoption?
3. **Failure Modes**: What happens when an agent makes a wrong decision?
4. **Trust Boundaries**: What should agents never do autonomously?

## Next: Segment 2

After mastering these foundations, we'll dive deep into LangGraph's advanced features: complex graphs with conditional edges, state persistence, and human-in-the-loop patterns.

→ Continue to [Segment 2: LangGraph Deep Dive](../segment_2_langgraph/README.md)
