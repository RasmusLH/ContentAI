from transformers import pipeline
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self):
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        try:
            logger.info("Initializing text generation model...")
            self.model = pipeline(
                "text2text-generation",
                model=settings.model_name,
                framework="pt",
                device=-1
            )
            logger.info("Model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize model: {str(e)}")
            logger.exception("Detailed traceback:")
            raise RuntimeError(f"Model initialization failed: {str(e)}")

    def get_model(self):
        if not self.model:
            raise RuntimeError("Text generation model not initialized")
        return self.model
