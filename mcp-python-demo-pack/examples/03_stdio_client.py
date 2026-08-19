"""Launch the MCP server as a subprocess and communicate over stdio."""

import asyncio
import sys

from mcp import Client, StdioServerParameters, stdio_client


async def main() -> None:
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_demo.server"],
    )
    # Building the transport explicitly is compatible across the v2 release line.
    async with Client(stdio_client(params)) as client:
        result = await client.call_tool("get_employee", {"employee_id": 102})
        print(result.structured_content)


if __name__ == "__main__":
    asyncio.run(main())
