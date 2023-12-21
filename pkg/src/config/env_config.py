import os
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache


os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"


class Settings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ENVIRONMENT: str

    ASTRADB_KEYSPACE: str
    ASTRADB_CLIENT_SECRET: str
    ASTRADB_CLIENT_ID: str
    ASTRADB_TOKEN: str

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent

    class Config:
        env_file = ".env.development"


@lru_cache()
def settings():
    return Settings()
