from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import logging

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Initialize the text-generation pipeline
    generator = pipeline("text-generation", model="openai-community/gpt2", tokenizer="openai-community/gpt2")
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Model load error: {e}")
    raise HTTPException(status_code=500, detail=f"Model load error: {e}")

class GenerationRequest(BaseModel):
    objective: str

@router.post("/generate")
async def generate_post(request: GenerationRequest):
    if generator is None:
        logger.error("Model not loaded")
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    english_prompt = (
        f"Generate a compelling and engaging LinkedIn post based on the following context: {request.objective}\n\n"
        "The post should include a clear headline, an informative body, and a strong call-to-action. "
        "Ensure the tone is professional, inspiring, and tailored to a business audience.\n\n"
        "Post:\n"
    )
    
    try:
        result = generator(
            english_prompt,
            max_length=300,
            num_return_sequences=1,
            truncation=True,
            pad_token_id=generator.tokenizer.eos_token_id,
            max_new_tokens=100,
            top_k=50
        )
        logger.info(f"Generation result: {result}")
        
        if not result or "generated_text" not in result[0]:
            logger.error("The key 'generated_text' is missing in the generator result")
            raise ValueError("The key 'generated_text' is missing in the generator result")
        
        full_text = result[0]["generated_text"]
        # Split on "Post:" and return only the text after it, if available.
        if "Post:" in full_text:
            generated_post = full_text.split("Post:", 1)[1].strip()
        else:
            generated_post = full_text.strip()
            
        return {"post": generated_post}
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Generation error: {e}")

@router.get("/")
async def root():
    return {"message": "Welcome to the Social Media Post Generator API!"}
