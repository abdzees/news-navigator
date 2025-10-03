"""
Configuration utilities for the backend using pydantic BaseSettings.
"""
from typing import Optional
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

# load .env early so values are available to BaseSettings and other modules
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment or .env file."""

    news_api_key: Optional[str] = Field(None, env="NEWSAPI_KEY")
    database_url: str = Field("sqlite+aiosqlite:///./data/news.db", env="DATABASE_URL")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    api_url: str = Field("http://127.0.0.1:8501", env="API_URL")
    embeddings_model: str = Field("sentence-transformers/all-MiniLM-L6-v2", env="EMBEDDINGS_MODEL")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
