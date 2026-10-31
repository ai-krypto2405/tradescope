"""
Application Configuration
Manages environment variables and settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "TradeScope"
    DEBUG: bool = False
    
    # Database (Railway provides DATABASE_URL automatically)
    DATABASE_URL: str = "sqlite:///./tradescope.db"  # Fallback for local dev
    
    # Redis & Celery (Railway provides REDIS_URL automatically)
    REDIS_URL: str = ""  # Empty = in-memory mode (local dev)
    CELERY_BROKER_URL: str = ""  # Will use eager mode (local dev)
    CELERY_RESULT_BACKEND: str = ""
    
    # JWT Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_ID: str = ""  # Monthly subscription price ID
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Binance API (optional for user's own keys)
    BINANCE_API_KEY: Optional[str] = None
    BINANCE_API_SECRET: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
