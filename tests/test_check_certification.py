import json
import subprocess

import check_certification

CUSTOM = ["custom:evals", "custom:resources", "custom:observability", "custom:auth"]


def init_repo(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".gitignore").write_text(".env\n")


def tracked(tmp_path):
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)


def write_features(tmp_path, tags):
    features = [{"status": "passing", "certification": [t]} for t in tags]
    (tmp_path / "feature_list.json").write_text(json.dumps({"features": features}))


def test_strict_fails_on_fresh_skeleton(tmp_path, capsys):
    init_repo(tmp_path)
    tracked(tmp_path)
    assert check_certification.main(["--root", str(tmp_path), "--strict"]) == 1
    assert "FAIL" in capsys.readouterr().out


def test_default_mode_exits_zero_on_skeleton(tmp_path):
    init_repo(tmp_path)
    assert check_certification.main(["--root", str(tmp_path)]) == 0


def test_custom_count_reaches_four(tmp_path):
    write_features(tmp_path, CUSTOM)
    assert len(check_certification.custom_passing(tmp_path)) == 4
    write_features(tmp_path, CUSTOM[:3])
    assert len(check_certification.custom_passing(tmp_path)) == 3


def test_non_passing_features_do_not_count(tmp_path):
    (tmp_path / "feature_list.json").write_text(json.dumps({"features": [{"status": "in_progress", "certification": ["custom:evals"]}]}))
    assert check_certification.custom_passing(tmp_path) == []


def test_secret_pattern_detected(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "config.txt").write_text("key = ghp_" + "a" * 30 + "\n")
    tracked(tmp_path)
    ok, detail = check_certification.check_secrets(tmp_path)
    assert not ok and "config.txt" in detail


def test_secret_in_untracked_file_detected(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "notes.md").write_text("AIza" + "b" * 35 + "\n")
    (tmp_path / ".env").write_text("OPENCODE_API_KEY=sk-" + "c" * 30 + "\n")
    ok, detail = check_certification.check_secrets(tmp_path)
    assert not ok and "notes.md" in detail and ".env" not in detail.split(", ")


def test_clean_repo_has_no_secrets(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "a.txt").write_text("nothing here\n")
    tracked(tmp_path)
    assert check_certification.check_secrets(tmp_path)[0]


def test_tracked_env_detected(tmp_path):
    init_repo(tmp_path)
    (tmp_path / ".env").write_text("X=1\n")
    subprocess.run(["git", "-C", str(tmp_path), "add", "-f", ".env"], check=True)
    assert not check_certification.check_env_untracked(tmp_path)[0]


SECTIONS = [
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
]


def readme_text(skip=(), architecture_words=300, extra=""):
    parts = []
    for name in SECTIONS:
        if name in skip:
            continue
        level = "###" if name in ("Mandatory", "Custom") else "##"
        body = " ".join(["word"] * architecture_words) if name.startswith("Architecture") else "text"
        parts.append(f"{level} {name}\n\n{body}\n")
    return "# Underdoc\n\n" + "\n".join(parts) + extra


def write_readme(tmp_path, **kwargs):
    (tmp_path / "README.md").write_text(readme_text(**kwargs))


def test_readme_complete_passes(tmp_path):
    write_readme(tmp_path)
    assert check_certification.check_readme(tmp_path)[0]


def test_readme_missing_section_named(tmp_path):
    write_readme(tmp_path, skip=("Testing",))
    ok, detail = check_certification.check_readme(tmp_path)
    assert not ok and "Testing" in detail and "heading" in detail


def test_readme_placeholder_detected_outside_fences_only(tmp_path):
    write_readme(tmp_path, extra="Fill [your key] here\n")
    ok, detail = check_certification.check_readme(tmp_path)
    assert not ok and "placeholder" in detail
    write_readme(tmp_path, extra="```\n[your key]\n```\n")
    assert check_certification.check_readme(tmp_path)[0]


def test_readme_short_architecture_fails(tmp_path):
    write_readme(tmp_path, architecture_words=50)
    ok, detail = check_certification.check_readme(tmp_path)
    assert not ok and "Architecture" in detail and "250" in detail


def test_readme_missing_file(tmp_path):
    assert not check_certification.check_readme(tmp_path)[0]


def write_cursor(tmp_path, config):
    (tmp_path / ".cursor").mkdir()
    (tmp_path / ".cursor" / "mcp.json").write_text(json.dumps(config) if not isinstance(config, str) else config)


GOOD_CURSOR = {"mcpServers": {"underdoc": {"command": "uv", "args": ["run", "python", "-m", "src.server"]}}}


def test_cursor_config_ok(tmp_path):
    write_cursor(tmp_path, GOOD_CURSOR)
    assert check_certification.check_cursor_config(tmp_path)[0]


def test_cursor_config_accepts_mcp_servers_key(tmp_path):
    write_cursor(tmp_path, {"mcp_servers": GOOD_CURSOR["mcpServers"]})
    assert check_certification.check_cursor_config(tmp_path)[0]


def test_cursor_config_missing_invalid_or_wrong_server(tmp_path):
    assert not check_certification.check_cursor_config(tmp_path)[0]
    write_cursor(tmp_path, "{not json")
    assert "valid JSON" in check_certification.check_cursor_config(tmp_path)[1]
    (tmp_path / ".cursor" / "mcp.json").write_text(json.dumps({"mcpServers": {"x": {"command": "uv", "args": ["run", "other"]}}}))
    ok, detail = check_certification.check_cursor_config(tmp_path)
    assert not ok and "src.server" in detail


def test_settings_references_env_file_path(tmp_path):
    assert not check_certification.check_settings_env(tmp_path)[0]
    path = tmp_path / "src" / "config" / "settings.py"
    path.parent.mkdir(parents=True)
    path.write_text("x = 1\n")
    assert not check_certification.check_settings_env(tmp_path)[0]
    path.write_text('env_file = os.getenv("ENV_FILE_PATH", ".env")\n')
    assert check_certification.check_settings_env(tmp_path)[0]


def test_layout_checks_root_src(tmp_path):
    ok, detail = check_certification.check_layout(tmp_path)
    assert not ok and "src/server.py" in detail
    for name in check_certification.LAYOUT:
        path = tmp_path / name
        if "." in path.name:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("")
        else:
            path.mkdir(parents=True, exist_ok=True)
    assert check_certification.check_layout(tmp_path)[0]
    assert "src/resources" in check_certification.LAYOUT and "src/prompts" in check_certification.LAYOUT


def test_prompt_registration_detection(tmp_path):
    assert not check_certification.check_prompt(tmp_path)[0]
    src = tmp_path / "src" / "routers"
    src.mkdir(parents=True)
    (src / "prompts.py").write_text("@mcp.prompt\ndef x(): ...\n")
    assert check_certification.check_prompt(tmp_path)[0]
    (src / "prompts.py").write_text("mcp.prompt(fn)\n")
    assert check_certification.check_prompt(tmp_path)[0]
