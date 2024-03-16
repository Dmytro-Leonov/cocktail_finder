from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    HASH_ALGORITHM: str = "HS256"
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 24 * 31  # 1 month
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 15  # 15 minutes


auth_config = AuthConfig()
