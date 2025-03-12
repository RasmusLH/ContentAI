from fastapi import APIRouter, HTTPException, Query, File, UploadFile, Form
import logging
from datetime import datetime
from typing import List
from ..database import db
from ..schemas import GenerationRequest, TEMPLATE_PROMPTS
from ..services.model_service import ModelService
from ..services.generation_service import GenerationService

logger = logging.getLogger(__name__)

# Define constants
MIN_WORDS = 5
MAX_FILE_SIZE = 50 * 1024  # 50KB per file
MAX_TOTAL_SIZE = 200 * 1024  # 200KB total

# Initialize services
model_service = ModelService()
generation_service = GenerationService(model_service)

router = APIRouter(prefix="/api", tags=["generation"])

@router.post("/generate")
async def generate_post(
    template: str = Form(...),
    objective: str = Form(...),
    context: str = Form(...),
    documents: List[UploadFile] = File([])  # Changed from None to empty list
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
            
        # Store result
        post_dict = {
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
):
    """Retrieve generation history"""
    cursor = db.posts_collection.find().sort("created_at", -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)
    return posts
