from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


_ROOT_DIR = Path(__file__).resolve().parents[3]
_ENV_PATH = _ROOT_DIR / ".env"
load_dotenv(dotenv_path=_ENV_PATH)


@dataclass(frozen=True)
class AppSettings:
    max_number_of_projects: int
    max_number_of_tasks: int

    @staticmethod
    def _read_int(name: str, default: Optional[int] = None) -> int:
        raw_value = os.getenv(name)
        if raw_value is None:
            if default is None:
                raise ValueError(f"Missing required environment variable: {name}")
            return int(default)
        return int(raw_value)

    @classmethod
    def load(cls) -> AppSettings:
        return cls(
            max_number_of_projects=cls._read_int("MAX_NUMBER_OF_PROJECTS"),
            max_number_of_tasks=cls._read_int("MAX_NUMBER_OF_TASKS"),
        )


settings = AppSettings.load()
