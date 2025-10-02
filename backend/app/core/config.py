"""
Configuration utilities for the backend.

Store environment keys, API keys and application settings here. Use pydantic's
BaseSettings to load .env variables for production-ready configuration.
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment or .env file."""
    app_name: str = "news-navigator-backend"
    newsapi_key: str = ""  # set in .env for production
    database_url: str = "sqlite+aiosqlite:///./data/news.db"
    embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"


settings = Settings()
