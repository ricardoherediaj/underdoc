from src.config.settings import Settings, env_file_path


def test_env_file_path_defaults_to_dot_env(monkeypatch):
    monkeypatch.delenv("ENV_FILE_PATH", raising=False)
    assert env_file_path() == ".env"


def test_settings_load_values_from_env_file_path(tmp_path, monkeypatch):
    env_file = tmp_path / "custom.env"
    env_file.write_text("OPENCODE_API_KEY=fake-key\nOPIK_WORKSPACE=fake-workspace\nUNDERDOC_HARNESS_PATH=/fake/voice\n")
    monkeypatch.setenv("ENV_FILE_PATH", str(env_file))
    for name in ("OPENCODE_API_KEY", "OPIK_WORKSPACE", "UNDERDOC_HARNESS_PATH", "OPIK_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    settings = Settings(_env_file=env_file_path())
    assert settings.opencode_api_key.get_secret_value() == "fake-key"
    assert "fake-key" not in repr(settings)
    assert settings.opik_workspace == "fake-workspace"
    assert settings.underdoc_harness_path == "/fake/voice"
    assert settings.opik_api_key is None


def test_settings_defaults():
    settings = Settings(_env_file=None)
    assert settings.server_name == "underdoc"
    assert settings.version
