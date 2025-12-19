# Segment 4: MCP Servers & Production Deployment

**Duration**: 50 minutes + 10 min Q&A

Claude's Model Context Protocol for universal tool connectivity.

## Files

| File | Topic |
|------|-------|
| `01_mcp_architecture.py` | MCP fundamentals |
| `02_database_server/` | **Demo**: Database MCP server |
| `03_github_integration.py` | GitHub connectivity |
| `04_slack_integration.py` | Slack notifications |
| `05_production_concerns.py` | Rate limits, costs, monitoring |
| `06_evaluation_framework.py` | Agent metrics |
| `07_antipatterns.py` | When NOT to use agents |

## MCP Server Demo

```bash
cd segment_4_mcp/02_database_server
docker build -t mcp-database .
docker run -p 3000:3000 mcp-database
```

See [Main Project](../projects/ai_dev_team/README.md)
