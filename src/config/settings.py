"""Server configuration settings."""

import os

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


def env_file_path() -> str:
    return os.getenv("ENV_FILE_PATH", ".env")


class Settings(BaseSettings):
    """Application settings for the Underdoc MCP server."""

    model_config = SettingsConfigDict(env_file=env_file_path(), extra="ignore", env_file_encoding="utf-8")

    server_name: str = Field(default="underdoc", description="The name of the server")
    version: str = Field(default="0.1.0", description="The version of the server")

    opencode_api_key: SecretStr | None = Field(default=None, alias="OPENCODE_API_KEY", description="OpenCode Go key")
    opik_api_key: SecretStr | None = Field(default=None, alias="OPIK_API_KEY", description="Opik observability key")
    opik_workspace: str | None = Field(default=None, alias="OPIK_WORKSPACE", description="Opik workspace")
    underdoc_harness_path: str | None = Field(default=None, alias="UNDERDOC_HARNESS_PATH", description="Path to the voice rules")


settings = Settings()
