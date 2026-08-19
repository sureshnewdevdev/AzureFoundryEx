"""Run the same demo server over Streamable HTTP."""

from mcp_demo.server import mcp


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
        streamable_http_path="/mcp",
        json_response=True,
        stateless_http=True,
    )

