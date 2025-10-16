from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    CAT_FACT_URL: str
    EMAIL: str
    NAME: str
    STACK: str
    REDIS_USERNAME: str
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


settings = Settings()
