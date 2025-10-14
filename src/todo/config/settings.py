from __future__ import annotations

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


_ROOT_DIR = Path(__file__).resolve().parents[3]
_ENV_PATH = _ROOT_DIR / ".env"


class AppSettings(BaseSettings):
    MAX_NUMBER_OF_PROJECTS: int = 5
    MAX_NUMBER_OF_TASKS: int = 50
    MAX_PROJECT_NAME_LENGTH: int = 30
    MAX_PROJECT_DESCRIPTION_LENGTH: int = 150
    MAX_TASK_TITLE_LENGTH: int = 30
    MAX_TASK_DESCRIPTION_LENGTH: int = 150

    model_config = SettingsConfigDict(
        env_file=_ENV_PATH,
        env_file_encoding="utf-8",
    )


settings = AppSettings()
