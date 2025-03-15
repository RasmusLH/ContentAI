from openai import AsyncOpenAI  # Change to AsyncOpenAI
import logging
from ..config import settings
from ..utils.error_handlers import APIError
from ..utils.model_utils import get_text_generation_params, get_image_generation_params

logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self):
        self.client = None
        self._initialize_model()
    
    def _initialize_model(self):
        try:
            logger.info("Initializing AsyncOpenAI client")
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)  # Use AsyncOpenAI
            logger.info("AsyncOpenAI client initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize OpenAI client", exc_info=True)
            raise APIError(
                message="Failed to initialize AI model",
                status_code=500,
                details={"error": str(e)}
            )

    def get_model(self):
        if not self.client:
            raise APIError(
                message="OpenAI client not initialized",
                status_code=500
            )
        return self.client

    async def generate_text(self, prompt: str) -> str:
        params = get_text_generation_params()
        params["messages"] = [{"role": "user", "content": prompt}]
        
        response = await self.client.chat.completions.create(**params)
        return response.choices[0].message.content

    async def generate_image(self, prompt: str, model: str = None) -> str:
        # Simplified call matching OpenAI docs standard
        response = await self.client.images.generate(
            model = model,
            prompt = prompt,
            size = "1024x1024",
            quality = "standard",
            n = 1
        )
        return response.data[0].url
