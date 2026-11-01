"""s3-002: the canonical voice in voice/ is exposed as MCP resources."""

import asyncio
from pathlib import Path

import pytest
from fastmcp import Client

from src import server
from src.resources import voice

VOICE_DIR = Path(__file__).resolve().parents[2] / "voice"


def expected_files(root: Path) -> dict[str, Path]:
    files = [root / "skill" / "SKILL.md"]
    files += sorted((root / "skill" / "references").glob("*.md"))
    files += sorted((root / "corpus").glob("*.md"))
    files.append(root / "pipeline" / "article_guideline.md")
    return {f"voice://{path.relative_to(root).as_posix()}": path for path in files}


async def list_and_read(mcp, uris=None):
    async with Client(mcp) as client:
        listed = await client.list_resources()
        contents = {}
        for uri in uris or [str(resource.uri) for resource in listed]:
            contents[uri] = (await client.read_resource(uri))[0].text
        return listed, contents


def test_client_lists_every_voice_file_and_the_corpus_index():
    listed, _ = asyncio.run(list_and_read(server.create_mcp_server(), uris=[]))
    uris = {str(resource.uri) for resource in listed}
    expected = set(expected_files(VOICE_DIR)) | {voice.CORPUS_INDEX_URI}
    assert uris == expected
    assert len(expected_files(VOICE_DIR)) == 41  # SKILL.md + 13 references + 26 posts + brief template


def test_each_voice_resource_matches_its_file_byte_for_byte():
    files = expected_files(VOICE_DIR)
    _, contents = asyncio.run(list_and_read(server.create_mcp_server(), uris=list(files)))
    for uri, path in files.items():
        assert contents[uri].encode("utf-8") == path.read_bytes(), uri


def test_corpus_index_lists_every_corpus_post():
    _, contents = asyncio.run(list_and_read(server.create_mcp_server(), uris=[voice.CORPUS_INDEX_URI]))
    index = contents[voice.CORPUS_INDEX_URI]
    posts = sorted((VOICE_DIR / "corpus").glob("*.md"))
    assert len(posts) == 26
    for post in posts:
        assert f"voice://corpus/{post.name}" in index


def test_voice_dir_follows_underdoc_harness_path(tmp_path, monkeypatch):
    (tmp_path / "skill" / "references").mkdir(parents=True)
    (tmp_path / "corpus").mkdir()
    (tmp_path / "pipeline").mkdir()
    (tmp_path / "skill" / "SKILL.md").write_text("# Skill\n")
    (tmp_path / "skill" / "references" / "voice-tonality.md").write_text("tone\n")
    (tmp_path / "corpus" / "2026-01-01-a-post.md").write_text("---\ntitle: A post\n---\nbody\n")
    (tmp_path / "pipeline" / "article_guideline.md").write_text("brief\n")
    monkeypatch.setattr(voice.settings, "underdoc_harness_path", str(tmp_path))

    listed, contents = asyncio.run(list_and_read(server.create_mcp_server()))

    assert {str(resource.uri) for resource in listed} == set(expected_files(tmp_path)) | {voice.CORPUS_INDEX_URI}
    assert contents["voice://corpus/2026-01-01-a-post.md"] == "---\ntitle: A post\n---\nbody\n"


def test_missing_voice_dir_fails_loudly(tmp_path, monkeypatch):
    monkeypatch.setattr(voice.settings, "underdoc_harness_path", str(tmp_path / "missing"))
    with pytest.raises(FileNotFoundError, match="voice"):
        server.create_mcp_server()
