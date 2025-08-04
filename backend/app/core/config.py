"""
Application configuration management using Pydantic settings.
Handles environment variables, database connections, and service configurations.
"""

import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Basic App Settings
    APP_NAME: str = "CDST Diagnostic Network Optimization Platform"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Healthcare diagnostic network optimization platform by PATH"
    DEBUG: bool = False
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database Settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "cdst_user"
    POSTGRES_PASSWORD: str = "cdst_password"
    POSTGRES_DB: str = "cdst_optimization"
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: Optional[PostgresDsn] = None
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    # Redis Settings
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600  # 1 hour
    
    # Celery Settings
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # External API Settings
    OSRM_BASE_URL: str = "http://router.project-osrm.org"
    OSRM_TIMEOUT: int = 30
    OSRM_MAX_RETRIES: int = 3
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: List[str] = [".csv", ".xlsx", ".xls", ".json"]
    UPLOAD_DIR: str = "./uploads"
    
    # Optimization Settings
    OPTIMIZATION_TIMEOUT: int = 900  # 15 minutes
    MAX_CONCURRENT_OPTIMIZATIONS: int = 5
    OPTIMIZATION_POPULATION_SIZE: int = 200
    OPTIMIZATION_MAX_GENERATIONS: int = 500
    
    # Security Settings
    ALGORITHM: str = "HS256"
    PASSWORD_MIN_LENGTH: int = 8
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION: int = 900  # 15 minutes
    
    # Monitoring Settings
    SENTRY_DSN: Optional[HttpUrl] = None
    LOG_LEVEL: str = "INFO"
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 8001
    
    # Email Settings (for notifications)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["APP_NAME"]
        return v
    
    # Testing Settings
    TESTING: bool = False
    TEST_DATABASE_URL: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 100
    
    # Data Validation Settings
    MAX_LABORATORIES_PER_NETWORK: int = 1000
    MAX_SERVICE_AREAS_PER_NETWORK: int = 5000
    MAX_TEST_DEMAND_RECORDS: int = 100000
    
    # Geospatial Settings
    DEFAULT_COORDINATE_SYSTEM: str = "EPSG:4326"  # WGS84
    MAX_DISTANCE_KM: float = 1000.0
    HAVERSINE_EARTH_RADIUS: float = 6371.0  # Earth radius in km
    
    # Performance Settings
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    HTTP_TIMEOUT: int = 30
    
    # Feature Flags
    ENABLE_OPTIMIZATION: bool = True
    ENABLE_ROUTING_API: bool = True
    ENABLE_DATA_IMPORT: bool = True
    ENABLE_REPORTS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


class TestSettings(Settings):
    """Test-specific settings that override base settings."""
    
    TESTING: bool = True
    DATABASE_URL: str = "postgresql+asyncpg://test_user:test_pass@localhost:5432/test_cdst"
    REDIS_URL: str = "redis://localhost:6379/15"  # Use different Redis DB for tests
    SECRET_KEY: str = "test-secret-key-not-for-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5  # Short-lived tokens for tests
    
    # Disable external services in tests
    ENABLE_ROUTING_API: bool = False
    SENTRY_DSN: Optional[HttpUrl] = None
    
    # Fast optimization for tests
    OPTIMIZATION_TIMEOUT: int = 30
    OPTIMIZATION_POPULATION_SIZE: int = 20
    OPTIMIZATION_MAX_GENERATIONS: int = 50


def get_settings() -> Settings:
    """Get application settings based on environment."""
    import os
    
    if os.getenv("TESTING") == "true":
        return TestSettings()
    return Settings()


# Global settings instance
settings = get_settings()