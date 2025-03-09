from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import logging
from enum import Enum
from typing import Optional

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Initialize with a simpler text2text model
    generator = pipeline("text2text-generation",
                        model="google/flan-t5-small",  # Smaller model that works with TensorFlow
                        tokenizer="google/flan-t5-small")
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Model load error: {e}")
    raise HTTPException(status_code=500, detail=f"Model load error: {e}")

class TemplateType(str, Enum):
    TECH_INSIGHT = "tech-insight"
    STARTUP_STORY = "startup-story"
    PRODUCT_LAUNCH = "product-launch"
    INDUSTRY_UPDATE = "industry-update"

class GenerationRequest(BaseModel):
    template: TemplateType
    objective: str
    context: str

TEMPLATE_PROMPTS = {
    TemplateType.TECH_INSIGHT: "Create a LinkedIn post discussing technology trends, focusing on innovation impact and future implications.",
    TemplateType.STARTUP_STORY: "Write an inspiring LinkedIn post about a startup journey, highlighting key milestones, challenges overcome, and lessons learned.",
    TemplateType.PRODUCT_LAUNCH: "Craft an engaging LinkedIn announcement about a new product launch, emphasizing unique features and customer benefits.",
    TemplateType.INDUSTRY_UPDATE: "Compose a LinkedIn post analyzing industry trends, market developments, and their business implications."
}

@router.post("/generate")
async def generate_post(request: GenerationRequest):
    if generator is None:
        logger.error("Model not loaded")
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    template_base = TEMPLATE_PROMPTS.get(request.template)
    
    english_prompt = (
        "Task: Generate a detailed professional LinkedIn post of MINIMUM 500 words.\n\n"
        f"Style: {template_base}\n"
        f"Topic: {request.objective}\n"
        f"Additional Context: {request.context}\n\n"
        "Instructions:\n"
        "1. Start with an attention-grabbing headline in bold\n"
        "2. Write a compelling hook in the first paragraph\n"
        "3. Develop the story across 5-7 detailed paragraphs\n"
        "4. Include specific examples, data points, and insights\n"
        "5. Add personal observations and industry expertise\n"
        "6. End with a strong call-to-action\n"
        "7. Use professional business language\n"
        "8. Include line breaks between paragraphs\n\n"
        "Format the post as follows:\n"
        "**[Compelling Headline]**\n\n"
        "[Hook paragraph]\n\n"
        "[Multiple detailed body paragraphs]\n\n"
        "[Insightful conclusion]\n\n"
        "[Engaging call-to-action]\n\n"
        "#relevanthashtags\n\n"
        "Generated Post:\n"
    )
    
    try:
        result = generator(
            english_prompt,
            max_length=512,       # Reduced max length for faster generation
            min_length=64,        # Minimum length to ensure some content
            do_sample=True,
            temperature=0.7,      # Slightly reduced temperature
            num_return_sequences=1
        )
        logger.info(f"Generation result: {result}")
        
        if not result or "generated_text" not in result[0]:
            logger.error("The key 'generated_text' is missing in the generator result")
            raise ValueError("The key 'generated_text' is missing in the generator result")
        
        full_text = result[0]["generated_text"]
        # Improved text cleaning
        if "Generated Post:" in full_text:
            generated_post = full_text.split("Generated Post:", 1)[1].strip()
        else:
            generated_post = full_text.strip()
  
        # Add length check
        if len(generated_post.split()) < 200:  # If less than 200 words
            logger.warning("Generated post too short, regenerating...")
            return await generate_post(request)  # Recursively try again
            
        return {"post": generated_post}
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Generation error: {e}")

@router.get("/")
async def root():
    return {"message": "Welcome to the Social Media Post Generator API!"}
