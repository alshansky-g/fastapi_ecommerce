from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    ALGORITHM: str = ""
    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0
    REFRESH_TOKEN_EXPIRE_DAYS: int = 0

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
