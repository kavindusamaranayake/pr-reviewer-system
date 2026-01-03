from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    github_token: str
    github_webhook_secret: str
    api_port: int = 8000
    cors_origins: str = "http://65.0.107.153:3000"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()