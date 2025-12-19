"""
MCP Database Server - Connect AI agents to your database

A simple MCP server that provides database query capabilities.
"""

import asyncio
import json
import os
from typing import Any

# MCP imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("Install mcp: pip install mcp")

import aiosqlite

# Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "demo.db")

# Create server
if MCP_AVAILABLE:
    server = Server("database-tools")


async def init_database():
    """Initialize demo database with sample data."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                amount REAL,
                status TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Insert sample data if empty
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        count = (await cursor.fetchone())[0]
        if count == 0:
            await db.executemany(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                [
                    ("Alice", "alice@example.com"),
                    ("Bob", "bob@example.com"),
                    ("Charlie", "charlie@example.com"),
                ]
            )
            await db.executemany(
                "INSERT INTO orders (user_id, amount, status) VALUES (?, ?, ?)",
                [
                    (1, 99.99, "completed"),
                    (1, 149.99, "pending"),
                    (2, 299.99, "completed"),
                ]
            )
        await db.commit()


if MCP_AVAILABLE:
    @server.tool()
    async def query_database(sql: str) -> str:
        """
        Execute a read-only SQL query on the database.

        Args:
            sql: The SQL query to execute (SELECT only)

        Returns:
            JSON string of query results
        """
        # Security: Only allow SELECT queries
        sql_upper = sql.strip().upper()
        if not sql_upper.startswith("SELECT"):
            return json.dumps({"error": "Only SELECT queries are allowed"})

        try:
            async with aiosqlite.connect(DATABASE_PATH) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(sql)
                rows = await cursor.fetchall()
                result = [dict(row) for row in rows]
                return json.dumps(result, indent=2, default=str)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @server.tool()
    async def get_table_schema(table_name: str) -> str:
        """
        Get the schema of a database table.

        Args:
            table_name: Name of the table

        Returns:
            JSON string of column information
        """
        try:
            async with aiosqlite.connect(DATABASE_PATH) as db:
                cursor = await db.execute(f"PRAGMA table_info({table_name})")
                columns = await cursor.fetchall()
                schema = [
                    {"name": col[1], "type": col[2], "nullable": not col[3]}
                    for col in columns
                ]
                return json.dumps(schema, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @server.tool()
    async def list_tables() -> str:
        """
        List all tables in the database.

        Returns:
            JSON array of table names
        """
        try:
            async with aiosqlite.connect(DATABASE_PATH) as db:
                cursor = await db.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
                tables = await cursor.fetchall()
                return json.dumps([t[0] for t in tables])
        except Exception as e:
            return json.dumps({"error": str(e)})


async def main():
    """Run the MCP server."""
    if not MCP_AVAILABLE:
        print("MCP not available")
        return

    # Initialize database
    await init_database()
    print("Database initialized")

    # Run server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
