from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession
import asyncio
import json
import os

server_params = StdioServerParameters(
    command="uv",
    args=["run", "mcp/server.py"],
    env={**os.environ, "PYTHONPATH": "."}
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
        list = await list_tools()
        print("List",list)

        result = await call_tool("get_transactions", {
            "user_id": 1,
            "start_date": "2024-03-01",
            "end_date": "2024-05-31"
        })
        print("TRANSACTIONS:", result)

        result = await call_tool("detect_anomalies", {
            "user_id": 1
        })
        print("ANOMALIES:", result)

        result = await call_tool("get_spending_summary", {
            "user_id": 1,
            "start_date": "2024-03-01",
            "end_date": "2024-05-31"
        })
        print("SUMMARY:", result)

    asyncio.run(test())

