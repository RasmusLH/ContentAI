from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    app_name: str = "LinkedIn Post Generator"
    api_prefix: str = "/api"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = "gpt-4o-mini-2024-07-18"  # Model name for OpenAI API
    max_tokens: int = 500  # Adjusted for OpenAI context
    min_tokens: int = 128   # Increased from 64
    min_words: int = 50    # Decreased from 200
    temperature: float = 0.7  # Slightly reduced for more focused outputs
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
