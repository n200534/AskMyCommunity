from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./askmycommunity.db"
    test_database_url: str = "sqlite:///./test_askmycommunity.db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # External APIs
    google_maps_api_key: str = ""
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    
    # AI Services
    openai_api_key: str = ""
    google_ai_api_key: str = ""
    ai_service: str = "google_ai"  # openai, google_ai, or custom
    
    # Google Maps
    google_maps_api_key: str = ""
    
    # App Settings
    debug: bool = True
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
