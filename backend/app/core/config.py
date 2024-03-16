import os
from typing import List, Literal

from pydantic import AnyHttpUrl, PostgresDsn, field_validator, model_validator
from pydantic_settings import BaseSettings


class CoreConfig(BaseSettings):
    ENVIRONMENT: Literal["dev", "prod"]
    SECRET_KEY: str
    IS_DEV: bool
    IS_PROD: bool
    PROJECT_NAME: str = "Cocktail Finder"
    API_PREFIX: str = "/api"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
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

    ECHO_SQL: bool = False

    @model_validator(mode="before")
    def set_environment(cls, values):
        if values["ENVIRONMENT"] == "dev":
            values["IS_DEV"] = True
            values["IS_PROD"] = False
        else:
            values["IS_DEV"] = False
            values["IS_PROD"] = True
        return values


core_config = CoreConfig()
