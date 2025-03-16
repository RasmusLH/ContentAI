import logging
from typing import List, Optional
from .model_service import ModelService
from .text_generation_service import TextGenerationService
from .image_generation_service import ImageGenerationService

logger = logging.getLogger(__name__)

class GenerationService:
    def __init__(self, model_service: ModelService):
        self.model_service = model_service
        self.text_service = TextGenerationService(model_service)
        self.image_service = ImageGenerationService(model_service)

    async def generate_text(
        self, 
        template: str, 
        request_objective: str, 
        request_context: str,
        document_texts: Optional[List[str]] = None
    ) -> str:
        return await self.text_service.generate(template, request_objective, request_context, document_texts)

    async def generate_image(
        self, 
        template: str, 
        request_objective: str, 
        request_context: str
    ) -> str:
        try:
            logger.info(f"Calling image_service.generate with template={template}, objective={request_objective}, context={request_context}")
            image_url = await self.image_service.generate(template, request_objective, request_context)
            logger.info(f"Image service returned: {image_url}")
            return image_url
        except Exception as e:
            logger.error(f"Generation service image generation failed: {str(e)}", exc_info=True)
            raise
