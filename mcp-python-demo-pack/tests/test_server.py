from mcp import Client

from mcp_demo.server import mcp


async def test_calculate() -> None:
    async with Client(mcp, raise_exceptions=True) as client:
        result = await client.call_tool(
            "calculate", {"operation": "add", "a": 7, "b": 8}
        )
        assert result.is_error is False
        assert result.structured_content == {"result": 15.0}


async def test_employee_search() -> None:
    async with Client(mcp, raise_exceptions=True) as client:
        result = await client.call_tool(
            "search_employees", {"query": "Data Engineering"}
        )
        assert result.is_error is False
        assert len(result.structured_content["result"]) == 2


async def test_reorder_suggestion() -> None:
    async with Client(mcp, raise_exceptions=True) as client:
        result = await client.call_tool(
            "suggest_reorder",
            {"sku": "MIC-401", "reorder_level": 10, "target_stock": 30},
        )
        assert result.structured_content["suggested_order"] == 27
        assert result.structured_content["status"] == "REORDER"


async def test_resource_and_prompt() -> None:
    async with Client(mcp, raise_exceptions=True) as client:
        resource = await client.read_resource("policy://reorder")
        assert "human must approve" in resource.contents[0].text
        prompt = await client.get_prompt("employee_skill_summary", {"department": "AI"})
        assert "AI department" in prompt.messages[0].content.text

