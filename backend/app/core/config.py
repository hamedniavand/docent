from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Docent"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    BASE_URL: str
    TIMEZONE: str = "Asia/Dubai"
    
    # Database
    DATABASE_URL: str
    POSTGRES_PASSWORD: str
    
    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Admin
    SYSTEM_ADMIN_EMAIL: str
    DEMO_COMPANY_NAME: str
    
    # Email
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAIL_FROM: str
    
    # Resend Email
    RESEND_API_KEY: str = ""
    
    # Google
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GEMINI_API_KEY: str
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 50
    
    # Search
    VECTOR_TOP_K: int = 5
    CHUNK_SIZE: int = 800
    
    # Paths
    STORAGE_PATH: str
    CHROMA_PATH: str
    LOG_PATH: str
    BACKUP_PATH: str
    
    class Config:
        env_file = "/opt/docent/.env"  # Absolute path
        case_sensitive = True

settings = Settings()
