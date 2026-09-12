import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

load_dotenv()

MCP_SERVER_PATH = str(Path(__file__).parent / "mcp_server.py")


def build_mcp_client() -> MultiServerMCPClient:

    return MultiServerMCPClient(
        {
            "weather": {
                "transport": "stdio",
                "command": "python",
                "args": [MCP_SERVER_PATH],
            }
        }
    )


async def get_tools_safely(client: MultiServerMCPClient) -> list:
    try:
        return await client.get_tools()
    except Exception as exc:
        print(f"Warning: failed to fetch MCP tools ({exc}); continuing with no tools.")
        return []


def build_agent(tools: list):
    # reasoning_effort="none": gpt-5.6-luna is a reasoning model, and
    # function tools aren't supported on the chat-completions endpoint at
    # its default reasoning effort.
    model = ChatOpenAI(model="gpt-5.6-luna", reasoning_effort="none")
    return create_agent(model=model, tools=tools)


async def main() -> None:
    print("Connecting to MCP server(s)...")
    client = build_mcp_client()
    tools = await get_tools_safely(client)
    print(f"Loaded {len(tools)} tool(s): {[tool.name for tool in tools]}")
    agent = build_agent(tools)

    while True:
        question = input("Ask a question (q to quit): ").strip()
        if question.lower() == "q":
            break
        result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
        print(f"Answer: {result['messages'][-1].content}")


if __name__ == "__main__":
    asyncio.run(main())
