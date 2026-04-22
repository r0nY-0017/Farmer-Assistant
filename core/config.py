from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    openai_api_key: str = ""
    max_file_size_mb: int = 5

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
