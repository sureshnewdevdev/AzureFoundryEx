"""Connect to the Streamable HTTP server running at localhost:8000."""

import asyncio

import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client


async def main() -> None:
    # trust_env=False prevents corporate proxy variables from intercepting localhost.
    async with httpx2.AsyncClient(trust_env=False) as http_client:
        transport = streamable_http_client(
            "http://127.0.0.1:8000/mcp", http_client=http_client
        )
        async with Client(transport) as client:
            print("Protocol:", client.protocol_version)
            result = await client.call_tool(
                "suggest_reorder",
                {"sku": "MIC-401", "reorder_level": 10, "target_stock": 30},
            )
            print(result.structured_content)


if __name__ == "__main__":
    asyncio.run(main())
