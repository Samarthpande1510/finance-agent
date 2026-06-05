from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession
import asyncio
import json
import os

server_params = StdioServerParameters(
    command="uv",
    args=["run", "mcp/server.py"],
    env={**os.environ, "PYTHONPATH": "."},
    read_timeout_seconds=30.0
)

async def call_tool(name: str, arguments: dict):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(name, arguments)
            return json.loads(result.content[0].text)

async def list_tools():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.list_tools()
            return result.tools

if __name__ == "__main__":
    async def test():
        result = await call_tool("search_spending_history", {
            "user_id": 1,
            "query": "food delivery"
        })
        print("SEARCH:", result)

    asyncio.run(test())

