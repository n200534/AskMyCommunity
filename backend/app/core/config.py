from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AskMyCommunity"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_V1_STR: str = "/api/v1"
    
    # Gemini API
    GEMINI_API_KEY: str
    
    # MongoDB
    MONGODB_URI: str = "mongodb://localhost:27017/askmycommunity"
    
    # Google Maps API
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    
    # Reddit API
    REDDIT_CLIENT_ID: Optional[str] = None
    REDDIT_CLIENT_SECRET: Optional[str] = None
    REDDIT_USER_AGENT: str = "AskMyCommunity/1.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
