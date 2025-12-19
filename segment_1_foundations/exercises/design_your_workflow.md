# Exercise: Design Your Agent Workflow

**Time**: 10-15 minutes

**Objective**: Apply the concepts from Segment 1 to design an agent workflow for a use case relevant to your work.

## Instructions

Think of a task in your work that might benefit from an agent-based approach. Use this template to design the workflow.

---

## Part 1: Use Case Definition

**Task Name**: _________________________________

**Description**:

*What does this task accomplish? Who benefits?*

**Current Approach**:

*How is this done today? (Manual, scripted, not done at all?)*

**Why Consider an Agent?**

*What makes you think an agent might help?*

---

## Part 2: Agent Classification

Using the framework from `01_what_is_an_agent.py`, evaluate:

| Characteristic | Yes/No | Notes |
|----------------|--------|-------|
| Needs memory across steps? | | |
| Needs persistent state? | | |
| Requires tool use? | | |
| Must be self-directed? | | |
| Requires planning? | | |
| Could delegate to sub-agents? | | |

**Autonomy Score**: ___/6

**Recommended Approach**:

- [ ] Traditional automation
- [ ] Single LLM call
- [ ] Chain of LLM calls
- [ ] Stateful agent (LangGraph)
- [ ] Multi-agent system (CrewAI)

---

## Part 3: Workflow Design

Draw or describe your workflow:

```text
START
  │
  ▼
┌─────────────┐
│   Node 1    │  <- What happens here?
│             │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Node 2    │  <- What happens here?
│             │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Node 3    │  <- What happens here?
│             │
└──────┬──────┘
       │
       ▼
      END
```

**Nodes** (list your nodes and what they do):

1. **Node Name**: ____________
   - Input:
   - Processing:
   - Output:

2. **Node Name**: ____________
   - Input:
   - Processing:
   - Output:

3. **Node Name**: ____________
   - Input:
   - Processing:
   - Output:

**Conditional Edges** (where does the agent decide what to do?):

- After Node ___, route to ___ if ___, otherwise ___

---

## Part 4: State Definition

What state needs to flow through your graph?

```python
class MyAgentState(TypedDict):
    # List your state fields here

    # Example:
    # messages: list[Message]  # Conversation history
    # current_step: str        # What we're doing now
    # results: dict            # Accumulated results
```

---

## Part 5: Tools Needed

What tools would your agent need access to?

| Tool | Purpose | Risk Level |
|------|---------|------------|
| | | Low / Medium / High |
| | | Low / Medium / High |
| | | Low / Medium / High |

---

## Part 6: Failure Modes

**What could go wrong?**

1.
2.
3.

**How should the agent recover?**

1.
2.
3.

**Where is human-in-the-loop needed?**

- [ ] Before critical actions
- [ ] When confidence is low
- [ ] For error recovery
- [ ] Other: ____________

---

## Part 7: Cost Estimation

Using the framework from `05_cost_analysis.py`:

| Metric | Estimate |
|--------|----------|
| Avg turns per execution | |
| Input tokens per turn | |
| Output tokens per turn | |
| Executions per day | |
| **Cost per execution** | $ |
| **Monthly cost** | $ |

**Is this cost justified?** Why or why not?

---

## Part 8: Final Recommendation

Based on your analysis:

- [ ] **Build the agent** - Benefits clearly outweigh costs
- [ ] **Start smaller** - Build a simpler version first
- [ ] **Use traditional approach** - Agent is overkill
- [ ] **Need more research** - Unclear if agent will work

**Rationale**:

---

## Discussion Questions

1. What was the hardest part of this design?
2. Where might you be over-engineering?
3. What would you prototype first?
4. How would you measure success?

---

## Next Steps

After completing this exercise:

1. Share your design with the group
2. Get feedback on potential issues
3. Consider how you'd implement this in Segment 2 (LangGraph) or Segment 3 (CrewAI)
