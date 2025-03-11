from openai import OpenAI
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self):
        self.client = None
        self._initialize_model()
    
    def _initialize_model(self):
        try:
            logger.info("Initializing OpenAI client...")
            self.client = OpenAI(api_key=settings.openai_api_key)
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            logger.exception("Detailed traceback:")
            raise RuntimeError(f"OpenAI initialization failed: {str(e)}")

    def get_model(self):
        if not self.client:
            raise RuntimeError("OpenAI client not initialized")
        return self.client
