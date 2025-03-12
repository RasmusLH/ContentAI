from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    app_name: str = "LinkedIn Post Generator"
    api_prefix: str = "/api"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = "gpt-4"  # Fixed model name
    max_tokens: int = 1000  # Increased for longer posts
    min_tokens: int = 128
    min_words: int = 50
    temperature: float = 0.7
    presence_penalty: float = 0.6  # Added missing setting
    frequency_penalty: float = 0.3  # Added missing setting
    allowed_origins: list = ["http://localhost:3000"]
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    mongodb_name: str = os.getenv("MONGODB_NAME", "contentai_db")
    jwt_secret: str = os.getenv("JWT_SECRET", "your-secret-key")
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 30  # days
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")

    class Config:
        env_file = ".env"

settings = Settings()
