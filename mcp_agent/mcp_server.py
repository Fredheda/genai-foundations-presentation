# mcp pinned to <2.0.0: langchain-mcp-adapters doesn't yet support the v2
# MCPServer API, so this uses v1's FastMCP.
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo Weather Server")


@mcp.tool()
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    return f"It's sunny and 21°C in {location}."


if __name__ == "__main__":
    mcp.run(transport="stdio")
