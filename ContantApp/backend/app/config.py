from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
import logging

# Load .env file
load_dotenv()

# Configure logging
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("motor").setLevel(logging.WARNING)

class Settings(BaseSettings):
    app_name: str = "LinkedIn Post Generator"
    api_prefix: str = "/api"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = "gpt-4o-mini-2025-07-18"
    openai_image_model: str = "dall-e-2" 
    max_tokens: int = 1000  # Increased for longer posts
    min_tokens: int = 128
    min_words: int = 50
    temperature: float = 0.7
    presence_penalty: float = 0.6  # Added missing setting
    frequency_penalty: float = 0.3  # Added missing setting
    allowed_origins: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    mongodb_name: str = os.getenv("MONGODB_NAME", "contentai_db")
    jwt_secret: str = os.getenv("JWT_SECRET", "your-secret-key")
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 30  # days
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        env_file = ".env"

settings = Settings()
