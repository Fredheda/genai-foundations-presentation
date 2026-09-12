from mcp_agent.mcp_server import get_weather
from mcp_agent.agent import build_mcp_client


def test_get_weather_returns_fixed_string():
    assert get_weather("London") == "It's sunny and 21°C in London."


def test_mcp_client_constructs():
    client = build_mcp_client()
    assert client is not None
