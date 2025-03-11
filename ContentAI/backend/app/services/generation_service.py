import logging
from .model_service import ModelService
from ..config import settings

logger = logging.getLogger(__name__)

class GenerationService:
    def __init__(self, model_service: ModelService):
        self.model_service = model_service

    def generate_text(self, prompt: str) -> str:
        try:
            model = self.model_service.get_model()
            result = model(
                prompt,
                max_length=settings.max_tokens,
                min_length=settings.min_tokens,
                do_sample=True,
                temperature=settings.temperature,
                num_return_sequences=1
            )
            
            if not result or not result[0].get("generated_text"):
                raise RuntimeError("Model returned empty result")
                
            return result[0]["generated_text"]
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            raise
