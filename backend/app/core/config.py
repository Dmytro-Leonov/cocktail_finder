import os
from typing import List, Literal

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class CoreConfig(BaseSettings):
    ENVIRONMENT: Literal["dev", "prod"]
    PROJECT_NAME: str = "Cocktail Finder"
    API_PREFIX: str = "/api"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: str = str(
        PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_SERVER"),
            path=os.getenv("POSTGRES_DB"),
        )
    )

    ECHO_SQL: bool = os.getenv("ECHO_SQL", "false").lower() in ("true", "1")


core_config = CoreConfig()
