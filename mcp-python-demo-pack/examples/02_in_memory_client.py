"""Exercise the server directly in one Python process."""

import asyncio
import json

from mcp import Client
from mcp_demo.server import mcp


async def main() -> None:
    async with Client(mcp) as client:
        tools = await client.list_tools()
        print("TOOLS:", [tool.name for tool in tools.tools])

        calc = await client.call_tool(
            "calculate", {"operation": "multiply", "a": 12, "b": 5}
        )
        print("CALCULATE:", calc.structured_content)

        employees = await client.call_tool(
            "search_employees", {"query": "Python", "limit": 5}
        )
        print("EMPLOYEES:", json.dumps(employees.structured_content, indent=2))

        resource = await client.read_resource("policy://reorder")
        print("RESOURCE:", resource.contents[0].text)

        prompt = await client.get_prompt(
            "inventory_risk_review", {"reorder_level": "10"}
        )
        print("PROMPT:", prompt.messages[0].content.text)


if __name__ == "__main__":
    asyncio.run(main())

