from fastapi import APIRouter, Query, File, UploadFile, Form, Depends, Header, Body, Request, HTTPException
import logging
from typing import List
from ..services.model_service import ModelService
from ..services.generation_service import GenerationService
from ..services.auth_service import AuthService
from ..services.post_service import PostService
from ..services.file_service import FileService
from ..controllers.post_controller import PostController
from ..utils.rate_limiter import rate_limiter
from ..utils.token_utils import get_token_from_header  # Import utility function

logger = logging.getLogger(__name__)

# Initialize services and controller
model_service = ModelService()
generation_service = GenerationService(model_service)
auth_service = AuthService()
file_service = FileService()
post_service = PostService()
post_controller = PostController(post_service, generation_service, file_service)

router = APIRouter(prefix="/api", tags=["generation"])

async def get_current_user_id(token: str = Depends(get_token_from_header)) -> str:
    return auth_service.verify_token(token)

@router.post("/generate")
async def generate_post(
    request: Request,
    template: str = Form(...),
    objective: str = Form(...),
    context: str = Form(...),
    documents: List[UploadFile] = File([]),
    authorization: str = Header(None)
):
    await rate_limiter.check_rate_limit(request)
    try:
        user_id = "anonymous"
        if authorization and authorization.startswith("Bearer "):
            try:
                token = authorization.split(" ")[1]
                user_id = auth_service.verify_token(token)
            except Exception:
                pass  # Continue with anonymous user

        return await post_controller.generate_post(template, objective, context, documents, user_id)
    except Exception as e:
        logger.error(f"Post generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/image/")  # Added trailing slash
async def generate_image(
    request: Request,
    template: str = Form(...),
    objective: str = Form(...),
    context: str = Form(...),
    authorization: str = Header(None)
):
    # For testing, comment out rate limiting:
    # await rate_limiter.check_rate_limit(request)

    logger.info(f"Image generation request received: template={template}, objective={objective}, context={context}")
    try:
        user_id = "anonymous"
        if authorization and authorization.startswith("Bearer "):
            try:
                token = authorization.split(" ")[1]
                user_id = auth_service.verify_token(token)
            except Exception:
                pass

        response = await post_controller.generate_image(
            template=template,
            objective=objective,
            context=context,
            user_id=user_id
        )
        logger.info(f"Image generation response from controller: {response}")
        return response
    except Exception as e:
        logger.error(f"Image generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_post_history(
    limit: int = Query(10, gt=0, le=100),
    skip: int = Query(0, ge=0),
    search: str = Query(None),
    user_id: str = Depends(get_current_user_id)
):
    return await post_controller.get_user_posts(user_id, limit, skip, search)

@router.post("/posts")
async def save_post(
    post_data: dict = Body(...),
    user_id: str = Depends(get_current_user_id)
):
    return await post_controller.save_post(post_data, user_id)

@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: str,
    user_id: str = Depends(get_current_user_id)
):
    success = await post_controller.delete_post(post_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
