# Architecture Overview

## System Components

```text
┌─────────────────────────────────────────────────────────────────┐
│                     AI Dev Team System                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   CrewAI     │  │  LangGraph   │  │    MCP       │          │
│  │   Agents     │  │  Workflows   │  │   Servers    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                 │                  │                  │
│         └─────────────────┼──────────────────┘                  │
│                           │                                      │
│                    ┌──────▼──────┐                              │
│                    │    LLM      │                              │
│                    │  (Claude)   │                              │
│                    └─────────────┘                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

1. User submits feature request
2. PM Agent creates requirements
3. Developer Agent creates implementation
4. QA Agent validates and tests
5. Results returned to user

## Technology Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | CrewAI |
| Workflow Engine | LangGraph |
| Tool Protocol | MCP |
| LLM | Claude (Anthropic) |
| Database | SQLite/PostgreSQL |

## Key Design Decisions

1. **Sequential Process** - Agents work in order for clarity
2. **Explicit State** - All state is typed and tracked
3. **Human-in-Loop** - Approval gates for risky actions
4. **Tool Isolation** - Each tool has limited scope
