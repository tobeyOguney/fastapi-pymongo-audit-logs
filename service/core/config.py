"""Service configuration settings."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Audit Log Service"
    MONGODB_URL: str = ""
    DB_NAME: str = "audit_log_db"
    CELERY_BROKER_URL: str = ""
    CELERY_RESULT_BACKEND: str = ""
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True


settings = Settings()
