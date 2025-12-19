# MCP Database Server

A simple MCP server that provides database query capabilities to AI agents.

## Tools Provided

- `query_database(sql)` - Execute read-only SQL queries
- `get_table_schema(table_name)` - Get column information
- `list_tables()` - List all tables

## Running Locally

```bash
pip install mcp aiosqlite
python server.py
```

## Running with Docker

```bash
docker build -t mcp-database .
docker run -p 3000:3000 mcp-database
```

## Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "database": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```
