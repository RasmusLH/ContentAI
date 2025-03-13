from openai import OpenAI  # Updated import
import logging
from ..config import settings
from ..utils.error_handlers import APIError

logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self):
        self.client = None
        self._initialize_model()
    
    def _initialize_model(self):
        try:
            logger.info("Initializing OpenAI client")
            self.client = OpenAI(api_key=settings.openai_api_key)
            logger.info("OpenAI client initialized successfully")
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
