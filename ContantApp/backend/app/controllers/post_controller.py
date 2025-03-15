from fastapi import HTTPException, UploadFile
from typing import List, Dict, Any
from ..services.post_service import PostService
from ..services.generation_service import GenerationService
from ..services.file_service import FileService
from ..schemas import TEMPLATE_PROMPTS
import logging

logger = logging.getLogger("app")

class PostController:
    def __init__(self, post_service: PostService, generation_service: GenerationService, file_service: FileService):
        self.post_service = post_service
        self.generation_service = generation_service
        self.file_service = file_service

    async def generate_post(self, template: str, objective: str, context: str, documents: List[UploadFile], user_id: str) -> Dict[str, Any]:
        if not template or not objective or not context:
            raise HTTPException(status_code=400, detail="Missing required fields")
            
        template_base = TEMPLATE_PROMPTS.get(template)
        if not template_base:
            raise HTTPException(status_code=400, detail="Invalid template type")

        document_texts = await self.file_service.process_files(documents)
        
        generated_text = self.generation_service.generate_text(
            template_base,
            objective,
            context,
            document_texts
        )
        
        if not generated_text:
            raise HTTPException(status_code=500, detail="Failed to generate text")

        # Store the generated post
        await self.post_service.create_post({
            "user_id": user_id,
            "template": template,
            "objective": objective,
            "context": context,
            "generated_content": generated_text,
        })
            
        return {"post": generated_text}

    async def generate_image(
        self, 
        template: str, 
        objective: str, 
        context: str,
        user_id: str
    ) -> Dict[str, str]:
        if not template or not objective or not context:
            raise HTTPException(status_code=400, detail="Missing required fields")
            
        template_base = TEMPLATE_PROMPTS.get(template)
        if not template_base:
            raise HTTPException(status_code=400, detail="Invalid template type")

        try:
            image_url = await self.generation_service.generate_image(
                template=template_base,
                request_objective=objective,
                request_context=context
            )

            # Store the generated image
            await self.post_service.create_post({
                "user_id": user_id,
                "template": template,
                "objective": objective,
                "context": context,
                "generated_content": image_url,
                "type": "image"
            })

            return {"image_url": image_url}
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def get_user_posts(self, user_id: str, limit: int, skip: int, search: str = None):
        return await self.post_service.get_user_posts(
            user_id=user_id,
            limit=limit,
            skip=skip,
            search=search
        )

    async def save_post(self, post_data: Dict[str, Any], user_id: str):
        logger.info(f"Saving post for user {user_id}", extra={"post_data": str(post_data)})
        result = await self.post_service.create_post(post_data, user_id)
        logger.info(f"Successfully saved post for user {user_id}")
        return result

    async def delete_post(self, post_id: str, user_id: str) -> bool:
        logger.info(f"Deleting post {post_id} for user {user_id}")
        result = await self.post_service.delete_post(post_id, user_id)
        logger.info(f"Delete operation result: {result}")
        return result
