from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import json
from db.database import SessionLocal
from db.queries import *
from contextlib import contextmanager
from db.vector_store import get_embedding, search as vector_search
from db.queries import get_transactions_by_ids
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

server = Server("clearmoney")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [ Tool(
        name="get_transactions",
        description="Fetch transactions for a user within a date range",
        inputSchema={
            "type": "object",
            "properties":{
                "user_id": {"type": "integer", "description": "The user's ID"},
                "start_date": {"type": "string", "description": "Start date in YYYY-MM-DD format"},
                "end_date": {"type": "string", "description": "End date in YYYY-MM-DD format"}
        },
            "required": ["user_id", "start_date", "end_date"]

        }
    ),
            Tool(
                name="categorize_transaction",
                description="Categorize a transaction by updating its agent_category label",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "The user's ID"},
                        "description": {"type": "string", "description": "Raw description of the transaction from the bank"},
                        "amount": {"type": "number", "description": "Amount of the transaction"},
                        "category": {"type": "string", "description": "Category to assign eg: food, shopping, transport"}
                    },
                    "required": ["user_id", "description", "amount", "category"]
                }
            ),
            Tool(
                name="get_spending_summary",
                description="analyze the user's transactions and give an overall summary of how he spent his money and where he did it in a particular time period",
                inputSchema={
                    "type":"object",
                    "properties": {
                        "user_id": {"type": "integer","description":"The user's ID"},
                        "start_date": {"type": "string", "description": "Start date in YYYY-MM-DD format"},
                        "end_date": {"type": "string", "description": "End date in YYYY-MM-DD format"}
                    },
                    "required": ["user_id", "start_date", "end_date"]
                }
            ),
            Tool(
                name="detect_anomalies",
                description="detect any weird or unsual spendings for a particular user",
                inputSchema={
                    "type":"object",
                    "properties": {
                        "user_id": {"type": "integer","description":"The user's ID"}
                    },
                    "required": ["user_id"]
                }
            ),
            Tool(
                name="search_spending_history",
                description="within the user's transaction search for a particular entry",
                inputSchema={
                    "type":"object",
                    "properties": {
                        "user_id": {"type": "integer","description":"The user's ID"},
                        "query": {"type":"string","description":"what to search for in the transactions"}
                    },
                    "required": ["user_id", "query"]
                }
            )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_transactions":
        with get_db() as db:
            result = get_transactions(db, **arguments)
            return [TextContent(type="text", text=json.dumps(result))]

    elif name == "categorize_transaction":
         with get_db() as db:
            result = categorize_transaction(db, **arguments)
            return [TextContent(type="text", text=json.dumps(result))]

    elif name == "get_spending_summary":
         with get_db() as db:
            result = get_spending_summary(db, **arguments)
            return [TextContent(type="text", text=json.dumps(result))]

    elif name == "detect_anomalies":
         with get_db() as db:
            result = detect_anomalies(db, **arguments)
            return [TextContent(type="text", text=json.dumps(result))]

    elif name == "search_spending_history":
        query_vector = get_embedding(arguments["query"], is_query=True)
        qdrant_results = vector_search(arguments["user_id"], query_vector,limit = 7)

        if not qdrant_results:
            return [TextContent(type="text", text=json.dumps([]))]
        
        ids = [r["transaction_id"] for r in qdrant_results]
        with get_db() as db:
            transactions = get_transactions_by_ids(db, arguments["user_id"], ids)
        
        score_map = {r["transaction_id"]: r["score"] for r in qdrant_results}
        for t in transactions:
            t["score"] = score_map.get(t["id"], 0)
        
        result = sorted(transactions, key=lambda x: x["score"], reverse=True)
        return [TextContent(type="text", text=json.dumps(result))]


    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, 
            write_stream, 
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())