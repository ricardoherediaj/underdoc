"""The canonical voice in voice/, exposed as MCP resources (s3-002).

One resource per file, so a client loads only what a post needs (Context-Augmented Generation):
the skill rules, the 13 reference files, the 26 corpus posts and the brief template.
"""

from pathlib import Path

from ..config.settings import settings

CORPUS_INDEX_URI = "voice://corpus"
REPO_ROOT = Path(__file__).resolve().parents[2]


def voice_dir() -> Path:
    """Resolve the voice/ folder from UNDERDOC_HARNESS_PATH, defaulting to the repo's voice/."""
    root = Path(settings.underdoc_harness_path).expanduser() if settings.underdoc_harness_path else REPO_ROOT / "voice"
    if not (root / "skill" / "SKILL.md").is_file():
        raise FileNotFoundError(f"voice rules not found at {root}; set UNDERDOC_HARNESS_PATH to the voice/ folder")
    return root.resolve()


def voice_files(root: Path) -> list[Path]:
    """The files exposed as resources, in a stable order."""
    files = [root / "skill" / "SKILL.md"]
    files += sorted((root / "skill" / "references").glob("*.md"))
    files += sorted((root / "corpus").glob("*.md"))
    files.append(root / "pipeline" / "article_guideline.md")
    return [path for path in files if path.is_file()]


def resource_uri(root: Path, path: Path) -> str:
    return f"voice://{path.relative_to(root).as_posix()}"


def describe(root: Path, path: Path) -> str:
    folder = path.relative_to(root).parts[0]
    if folder == "corpus":
        return f"Published Underdoc post ({post_title(path)}), a voice example."
    if folder == "pipeline":
        return "Article brief template (article_guideline.md) for a new post."
    return f"Voice rule file: {path.stem}."


def post_title(path: Path) -> str:
    """The title from a corpus post's frontmatter, or its file name."""
    for line in path.read_text(encoding="utf-8").splitlines()[1:20]:
        if line.startswith("title:"):
            return line.removeprefix("title:").strip().strip('"').strip()
        if line == "---":
            break
    return path.stem


def corpus_index(root: Path) -> str:
    """A markdown list of the corpus posts and their resource URIs."""
    posts = sorted((root / "corpus").glob("*.md"))
    lines = [f"# Underdoc corpus ({len(posts)} published posts)", ""]
    lines += [f"- {post_title(post)}: {resource_uri(root, post)}" for post in posts]
    return "\n".join(lines) + "\n"
