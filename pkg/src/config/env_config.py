"""Module providing a function printing python version."""

import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings


os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"


class Settings(BaseSettings):
    """
    This class represents the settings for the application.
    It includes configuration for JWT, ASTRADB, and base directory.
    """

    JWT_SECRET: str
    JWT_ALGORITHM: str
    ENVIRONMENT: str

    ASTRADB_KEYSPACE: str
    ASTRADB_CLIENT_SECRET: str
    ASTRADB_CLIENT_ID: str
    ASTRADB_TOKEN: str

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent

    class Config:
        """
        The Config class defines application settings. It includes attributes like env_file.
        """

        env_file = ".env.development"


@lru_cache()
def settings():
    """
    Retrieve and return the settings.

    Returns:
        Settings: The settings object.
    """
    return Settings()
