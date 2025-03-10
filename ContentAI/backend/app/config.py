from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    app_name: str = "LinkedIn Post Generator"
    api_prefix: str = "/api/v1"
    model_name: str = "google/flan-t5-small"
    max_tokens: int = 512
    min_tokens: int = 64
    min_words: int = 200
    temperature: float = 0.7
    allowed_origins: list = ["http://localhost:3000"]
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    mongodb_name: str = os.getenv("MONGODB_NAME", "contentai_db")

    class Config:
        env_file = ".env"

settings = Settings()
