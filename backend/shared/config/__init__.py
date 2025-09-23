"""Configuration management for microservices."""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database settings
    database_url: str = Field(
        default="sqlite:///./inventory.db",
        env="DATABASE_URL"
    )
    
    # Redis settings
    redis_url: str = Field(
        default="redis://localhost:6379",
        env="REDIS_URL"
    )
    
    # JWT settings
    jwt_secret_key: str = Field(
        default="your-secret-key-change-in-production",
        env="JWT_SECRET_KEY"
    )
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(
        default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    
    # Service settings
    service_name: str = Field(default="microservice", env="SERVICE_NAME")
    service_version: str = Field(default="1.0.0", env="SERVICE_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # API settings
    api_v1_prefix: str = Field(default="/api/v1", env="API_V1_PREFIX")
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:80"],
        env="CORS_ORIGINS"
    )
    
    # Inventory Service settings
    inventory_service_url: str = Field(
        default="http://localhost:8001",
        env="INVENTORY_SERVICE_URL"
    )
    
    # CRM Service settings
    crm_service_url: str = Field(
        default="http://localhost:8002",
        env="CRM_SERVICE_URL"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
