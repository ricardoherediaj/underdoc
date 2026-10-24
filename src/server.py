"""Underdoc MCP server."""

from argparse import ArgumentParser

from fastmcp import FastMCP

from .config.settings import settings
from .routers.prompts import register_mcp_prompts
from .routers.resources import register_mcp_resources
from .routers.tools import register_mcp_tools


def create_mcp_server() -> FastMCP:
    """Create and configure the MCP server instance."""
    mcp = FastMCP(name=settings.server_name, version=settings.version)

    register_mcp_tools(mcp)
    register_mcp_resources(mcp)
    register_mcp_prompts(mcp)

    return mcp


def main() -> None:
    parser = ArgumentParser(description="Underdoc MCP server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["stdio", "http"],
        default="stdio",
        help="The transport protocol to use for the MCP server.",
    )
    args = parser.parse_args()

    create_mcp_server().run(transport=args.transport)


if __name__ == "__main__":
    main()
