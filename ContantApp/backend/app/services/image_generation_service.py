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
        prompt = self._create_prompt(template, objective, context)
        return await handle_api_operation(
            "image generation",
            self.model_service.generate_image(prompt),
            "Image generation failed"
        )
