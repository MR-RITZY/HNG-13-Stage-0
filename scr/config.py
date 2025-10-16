from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    email: str
    name: str
    redis_db: str
    redis_host: str
    redis_password: str
    redis_port: str
    redis_username: str
    stack: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
