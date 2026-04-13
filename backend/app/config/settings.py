"""
Configuration settings for IBM Blueboard API
"""

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Project info
    PROJECT_NAME: str = "IBM Blueboard API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # Database credentials (from docker-compose)
    POSTGRES_USER: str = "blueboard"
    POSTGRES_PASSWORD: str = "blueboard_password"
    POSTGRES_DB: str = "blueboard"
    POSTGRES_HOST: str = "database"
    POSTGRES_PORT: int = 5432

    # Database URL (constructed from credentials)
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    # Environment
    ENVIRONMENT: str = "development"

    class Config:
        case_sensitive = True
        extra = "allow"


settings = Settings()
