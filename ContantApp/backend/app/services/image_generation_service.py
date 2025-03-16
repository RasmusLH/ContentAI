import logging
from .model_service import ModelService
from ..config import settings
from ..utils.error_handlers import handle_api_operation

logger = logging.getLogger(__name__)

class ImageGenerationService:
    def __init__(self, model_service: ModelService):
        self.model_service = model_service

    def _create_prompt(self, template: str, objective: str, context: str) -> str:
        # DALL-E 2 works better with simpler, more direct prompts
        return (
            f"Professional LinkedIn visual representing: {objective}. "
            f"Context: {context}. "
            f"Professional and minimalist style, "
            f"suitable for {template} content on LinkedIn. "
            "No text, clean corporate look."
        )

    async def generate(self, template: str, objective: str, context: str) -> str:
        try:
            prompt = self._create_prompt(template, objective, context)
            logger.info(f"Generating image with prompt: {prompt}")
            
            # Explicitly pass the model from settings to ensure it's using dall-e-2
            result = await handle_api_operation(
                "image generation",
                self.model_service.generate_image(prompt, model=settings.openai_image_model),
                "Image generation failed"
            )
            
            logger.info(f"Image generation successful, URL received: {result[:30]}...")
            return result
        except Exception as e:
            logger.error(f"Image generation error: {str(e)}", exc_info=True)
            raise
