from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )
    DATABASE_URL: str = 'default'
    SECRET_KEY: str = 'default'
    ALGORITHM: str = 'default'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0


settings = Settings()
