from fastapi import APIRouter, HTTPException, Query
import logging
from datetime import datetime
from .database import db
from .schemas import GenerationRequest, TEMPLATE_PROMPTS  # Add TEMPLATE_PROMPTS import
from .services.model_service import ModelService
from .services.generation_service import GenerationService 

logger = logging.getLogger(__name__)

# Define constants
MIN_WORDS = 5

# Initialize services
model_service = ModelService()
generation_service = GenerationService(model_service)

router = APIRouter(prefix="/api", tags=["generation"])

@router.post("/generate")
async def generate_post(request: GenerationRequest):
    try:
        template_base = TEMPLATE_PROMPTS.get(request.template)
        if not template_base:
            raise HTTPException(status_code=400, detail="Invalid template type")
            
        generated_text = generation_service.generate_text(
            template_base,
            request.objective,
            request.context
        )
        
        if not generated_text or len(generated_text.split()) < MIN_WORDS:
            raise HTTPException(status_code=500, detail="Generated text too short")
            
        # Store result
        post_dict = {
            "template": request.template,
            "objective": request.objective,
            "context": request.context,
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

@router.get("/debug/generator")
async def debug_generator():
    """
    Debug endpoint to test text generation with a fixed prompt.
    """
    try:
        # Test with a simple tech insight template
        generated = generation_service.generate_text(
            "Create a test tech insight post.",
            "Test generation",
            "Testing the generator functionality"
        )
        return {"generated_text": generated, "message": "Generator working correctly"}
    except Exception as e:
        logger.error(f"Debug generator failed: {str(e)}")
        if isinstance(e, RuntimeError):
            raise HTTPException(
                status_code=503, 
                detail="Text generation service unavailable"
            )
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
