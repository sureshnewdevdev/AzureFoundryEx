"""Smallest useful MCP v2 server: one tool, one resource, one prompt."""

from mcp.server import MCPServer

mcp = MCPServer("Minimal Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """Create a greeting for a name."""
    return f"Hello, {name}!"


@mcp.prompt()
def explain_mcp(audience: str = "trainees") -> str:
    """Create a prompt asking for an MCP explanation."""
    return f"Explain MCP to {audience} using one simple real-world analogy."


if __name__ == "__main__":
    mcp.run(transport="stdio")

