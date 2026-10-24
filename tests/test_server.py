import asyncio

from fastmcp import Client

from src import server


async def capabilities(mcp):
    async with Client(mcp) as client:
        return await client.list_tools(), await client.list_resources(), await client.list_prompts()


def test_server_builds_and_registers_routers(monkeypatch):
    called = []
    for name in ("register_mcp_tools", "register_mcp_resources", "register_mcp_prompts"):
        monkeypatch.setattr(server, name, lambda mcp, name=name: called.append(name))
    mcp = server.create_mcp_server()
    assert mcp.name == "underdoc"
    assert called == ["register_mcp_tools", "register_mcp_resources", "register_mcp_prompts"]


def test_server_exposes_no_capabilities_yet():
    tools, resources, prompts = asyncio.run(capabilities(server.create_mcp_server()))
    assert tools == []
    assert resources == []
    assert prompts == []
