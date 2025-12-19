# AI Software Development Team

The main course project: A complete multi-agent system with PM, Developer, and QA Tester.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Product   │────►│  Developer  │────►│     QA      │
│   Manager   │     │             │     │   Tester    │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
  Requirements         Code              Test Results
```

## Quick Start

```bash
cd projects/ai_dev_team
python -m examples.complete_feature_request
```

## Components

- `agents/` - Individual agent definitions
- `workflows/` - LangGraph workflows
- `mcp_servers/` - Tool servers
- `examples/` - Usage examples
