from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    email:str
    name:str
    stack:str
    redis_username:str
    redis_host:str
    redis_port:str
    redis_db:str
    redis_password:str
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()