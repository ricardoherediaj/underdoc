"""MCP resources registration."""

from fastmcp import FastMCP
from fastmcp.resources import FileResource

from ..resources import voice


def register_mcp_resources(mcp: FastMCP) -> None:
    """Register all MCP resources with the server instance."""
    root = voice.voice_dir()

    for path in voice.voice_files(root):
        mcp.add_resource(
            FileResource(
                uri=voice.resource_uri(root, path),
                path=path,
                name=path.relative_to(root).as_posix(),
                description=voice.describe(root, path),
                mime_type="text/markdown",
                tags={"voice", path.relative_to(root).parts[0]},
            )
        )

    @mcp.resource(
        voice.CORPUS_INDEX_URI,
        name="corpus-index",
        description="Index of the published Underdoc posts in the corpus, with their resource URIs.",
        mime_type="text/markdown",
        tags={"voice", "corpus"},
    )
    def corpus_index() -> str:
        return voice.corpus_index(root)
