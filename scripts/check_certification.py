"""Report Part 4 certification status. Default mode exits 0; --strict exits 1 on any failure."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

CUSTOM_REQUIRED = 4
SECRET_PATTERNS = [
    re.compile(p) for p in (r"sk-[A-Za-z0-9_-]{16,}", r"AIza[0-9A-Za-z_-]{20,}", r"ghp_[A-Za-z0-9]{20,}", r"-----BEGIN [A-Z ]*PRIVATE KEY")
]
PLACEHOLDER = re.compile(r"\[[^\]\n]+\](?!\()")
LAYOUT = (
    "src/server.py",
    "src/routers/tools.py",
    "src/routers/resources.py",
    "src/routers/prompts.py",
    "src/tools",
    "src/resources",
    "src/prompts",
    "src/app",
    "src/utils",
    "src/config/settings.py",
)
PROMPT_REGISTRATION = re.compile(r"@\w+\.prompt\b|\b\w+\.prompt\(")
README_SECTIONS = (
    "Project Overview",
    "Architecture & System Design",
    "Project Structure",
    "Features",
    "Mandatory",
    "Custom",
    "Setup Instructions",
    "Environment Variables",
    "Running the Server",
    "Connecting from an MCP Client",
    "Testing",
    "License",
)
ARCHITECTURE_MIN_WORDS = 250
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)


def git(root: Path, *args: str) -> list[str] | None:
    try:
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError, FileNotFoundError:
        return None
    return result.stdout.splitlines()


def check_python(root: Path) -> tuple[bool, str]:
    path = root / ".python-version"
    if not path.exists():
        return False, ".python-version missing"
    value = path.read_text().strip()
    return value.startswith("3.14"), value


def check_env_sample(root: Path) -> tuple[bool, str]:
    return (root / ".env.sample").exists(), ".env.sample present" if (root / ".env.sample").exists() else ".env.sample missing"


def check_env_untracked(root: Path) -> tuple[bool, str]:
    tracked = git(root, "ls-files")
    if tracked is None:
        return False, "not a git repo, cannot tell"
    return ".env" not in tracked, ".env not tracked" if ".env" not in tracked else ".env is tracked: git rm --cached .env"


def check_secrets(root: Path) -> tuple[bool, str]:
    # Untracked but not ignored files are one `git add -A` away from a public commit, so scan them too.
    candidates = git(root, "ls-files", "--cached", "--others", "--exclude-standard")
    if candidates is None:
        return False, "not a git repo, cannot tell"
    hits = []
    for name in candidates:
        path = root / name
        if not path.is_file() or name == "scripts/check_certification.py":
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError, OSError:
            continue
        if any(p.search(text) for p in SECRET_PATTERNS):
            hits.append(name)
    return not hits, "no secret patterns" if not hits else "secret pattern in " + ", ".join(hits)


def architecture_words(text: str) -> int:
    headings = list(HEADING.finditer(text))
    for i, match in enumerate(headings):
        if not match.group(2).lower().startswith("architecture"):
            continue
        level = len(match.group(1))
        end = next((h.start() for h in headings[i + 1 :] if len(h.group(1)) <= level), len(text))
        return len(text[match.end() : end].split())
    return 0


def check_readme(root: Path) -> tuple[bool, str]:
    path = root / "README.md"
    if not path.exists():
        return False, "README.md missing: copy the course README template"
    text = path.read_text()
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    titles = [m.group(2).lower() for m in HEADING.finditer(prose)]
    problems = []
    missing = [s for s in README_SECTIONS if not any(s.lower() in t for t in titles)]
    if missing:
        problems.append("missing heading(s): " + ", ".join(missing) + " (add each as a '##' or '###' heading)")
    if PLACEHOLDER.search(prose):
        problems.append("template placeholders left: replace every [...] outside code fences")
    if "Architecture & System Design" not in missing and (words := architecture_words(prose)) < ARCHITECTURE_MIN_WORDS:
        problems.append(f"Architecture section has {words} words, needs {ARCHITECTURE_MIN_WORDS}: expand it")
    return not problems, "README complete" if not problems else "; ".join(problems)


def check_layout(root: Path) -> tuple[bool, str]:
    missing = [p for p in LAYOUT if not (root / p).exists()]
    return not missing, "src layout present" if not missing else "missing under src/: " + ", ".join(missing)


def check_prompt(root: Path) -> tuple[bool, str]:
    base = root / "src"
    files = list(base.rglob("*.py")) if base.exists() else []
    found = any(PROMPT_REGISTRATION.search(f.read_text()) for f in files)
    return found, "prompt registration found" if found else "no @mcp.prompt registration found under src/"


def check_cursor_config(root: Path) -> tuple[bool, str]:
    path = root / ".cursor" / "mcp.json"
    if not path.exists():
        return False, ".cursor/mcp.json missing: add the server under mcpServers"
    try:
        config = json.loads(path.read_text())
    except json.JSONDecodeError:
        return False, ".cursor/mcp.json is not valid JSON"
    servers = config.get("mcpServers") or config.get("mcp_servers") or {}
    if any("src.server" in server.get("args", []) for server in servers.values()):
        return True, "Cursor config runs src.server"
    return False, ".cursor/mcp.json has no server whose args run src.server"


def check_settings_env(root: Path) -> tuple[bool, str]:
    path = root / "src" / "config" / "settings.py"
    if not path.exists():
        return False, "src/config/settings.py missing"
    ok = "ENV_FILE_PATH" in path.read_text()
    return ok, "settings read ENV_FILE_PATH" if ok else "src/config/settings.py must read the env file from ENV_FILE_PATH"


def custom_passing(root: Path) -> list[str]:
    path = root / "feature_list.json"
    if not path.exists():
        return []
    tags: set[str] = set()
    for feature in json.loads(path.read_text()).get("features", []):
        if feature.get("status") == "passing":
            tags.update(t for t in feature.get("certification", []) if t.startswith("custom:"))
    return sorted(tags)


def build_report(root: Path) -> tuple[list[tuple[str, bool, str]], list[str]]:
    mandatory = [
        ("uv on Python 3.14", *check_python(root)),
        (".env.sample exists", *check_env_sample(root)),
        (".env not tracked", *check_env_untracked(root)),
        ("no secrets in committable files", *check_secrets(root)),
        ("README follows course template", *check_readme(root)),
        ("Cursor MCP config (.cursor/mcp.json)", *check_cursor_config(root)),
        ("settings read ENV_FILE_PATH", *check_settings_env(root)),
        ("src layout at repo root", *check_layout(root)),
        ("HITL MCP prompt registered", *check_prompt(root)),
    ]
    return mandatory, custom_passing(root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    mandatory, custom = build_report(args.root)
    print(f"{'Mandatory item':<38} {'Status':<6} Detail")
    for name, ok, detail in mandatory:
        print(f"{name:<38} {'OK' if ok else 'FAIL':<6} {detail}")
    custom_ok = len(custom) >= CUSTOM_REQUIRED
    print(
        f"{'Custom features (passing)':<38} {'OK' if custom_ok else 'FAIL':<6} {len(custom)}/{CUSTOM_REQUIRED}: {', '.join(custom) or 'none'}"
    )
    failed = [n for n, ok, _ in mandatory if not ok] + ([] if custom_ok else ["custom features"])
    if args.strict and failed:
        print(f"strict: {len(failed)} item(s) failing")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
