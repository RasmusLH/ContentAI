from fastapi import APIRouter, HTTPException, Query, File, UploadFile, Form, Depends, Header, Body
import logging
from datetime import datetime
from typing import List
from ..database import db
from ..schemas import GenerationRequest, TEMPLATE_PROMPTS
from ..services.model_service import ModelService
from ..services.generation_service import GenerationService
from ..services.auth_service import AuthService
from bson import ObjectId

logger = logging.getLogger(__name__)

# Define constants
MIN_WORDS = 5
MAX_FILE_SIZE = 50 * 1024  # 50KB per file
MAX_TOTAL_SIZE = 200 * 1024  # 200KB total

# Initialize services
model_service = ModelService()
generation_service = GenerationService(model_service)
auth_service = AuthService()

router = APIRouter(prefix="/api", tags=["generation"])

async def get_current_user_id(token: str = Depends(auth_service.get_token_from_header)) -> str:
    return auth_service.verify_token(token)

@router.post("/generate")
async def generate_post(
    template: str = Form(...),
    objective: str = Form(...),
    context: str = Form(...),
    documents: List[UploadFile] = File([]),
    authorization: str = Header(None)  # optional auth header
):
    try:
        if not template or not objective or not context:
            raise HTTPException(status_code=400, detail="Missing required fields")
            
        template_base = TEMPLATE_PROMPTS.get(template)
        if not template_base:
            raise HTTPException(status_code=400, detail="Invalid template type")

        # Validate total file size
        total_size = 0
        if documents:
            for doc in documents:
                content = await doc.read()
                size = len(content)
                if size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"File {doc.filename} exceeds maximum size of 50KB"
                    )
                total_size += size
                if total_size > MAX_TOTAL_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail="Total size of all files exceeds 200KB"
                    )
                await doc.seek(0)

        # Process uploaded documents
        document_texts = []
        if documents:
            for doc in documents:
                content = await doc.read()
                try:
                    text = content.decode('utf-8')
                    document_texts.append(text)
                except UnicodeDecodeError:
                    logger.warning(f"Could not decode file {doc.filename} - skipping")
        
        generated_text = generation_service.generate_text(
            template_base,
            objective,
            context,
            document_texts
        )
        
        if not generated_text or len(generated_text.split()) < MIN_WORDS:
            raise HTTPException(status_code=500, detail="Generated text too short")
            
        # Determine user_id based on optional token; use "anonymous" if missing/invalid.
        user_id = "anonymous"
        if authorization and authorization.startswith("Bearer "):
            try:
                token = authorization.split(" ")[1]
                user_id = auth_service.verify_token(token)
            except Exception:
                pass  # leave as "anonymous"

        # Store result with user_id
        post_dict = {
            "user_id": user_id,
            "template": template,
            "objective": objective,
            "context": context,
            "generated_content": generated_text,
            "created_at": datetime.utcnow()
        }
        await db.posts_collection.insert_one(post_dict)
            
        return {"post": generated_text}
    except Exception as e:
        logger.error(f"Post generation failed: {str(e)}")
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_post_history(
    limit: int = Query(10, gt=0, le=100),
    skip: int = Query(0, ge=0),
    user_id: str = Depends(get_current_user_id)
):
    """Retrieve generation history for specific user"""
    cursor = db.posts_collection.find({"user_id": user_id}).sort("created_at", -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)
    # Convert _id to string for each document
    for post in posts:
        if "_id" in post:
            post["_id"] = str(post["_id"])
    return posts

@router.post("/posts")
async def save_post(
    post_data: dict = Body(...),
    user_id: str = Depends(get_current_user_id)
):
    try:
        post_data["user_id"] = user_id
        post_data["created_at"] = datetime.utcnow()
        await db.posts_collection.insert_one(post_data)
        return {"message": "Post saved successfully"}
    except Exception as e:
        logger.error(f"Failed to save post: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save post")

@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete a post if it belongs to the user"""
    try:
        result = await db.posts_collection.delete_one({
            "_id": ObjectId(post_id),
            "user_id": user_id  # Ensure user can only delete their own posts
        })
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Post not found")
        return {"message": "Post deleted successfully"}
    except Exception as e:
        logger.error(f"Failed to delete post: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete post")
