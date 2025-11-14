"""Configuration management"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file="config.env",
        case_sensitive=True,
    )
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:Admin@123@localhost:5432/postgres"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_SECRET_KEY: str = "dev-secret-key-change-in-production"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    # AI
    DEFAULT_AI_TIMEOUT: int = 5000
    MAX_AI_RETRIES: int = 3
    
    # Game
    MIN_PLAYERS: int = 2
    MAX_PLAYERS: int = 9
    DEFAULT_SMALL_BLIND: int = 5
    DEFAULT_BIG_BLIND: int = 10
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
settings = Settings()

