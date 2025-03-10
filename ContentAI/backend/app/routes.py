from fastapi import APIRouter, HTTPException, Query
from transformers import pipeline
import logging
from typing import Optional, List
from .database import db
from .models import StoredPost, StoredPrompt
from .schemas import TemplateType, GenerationRequest, TEMPLATE_PROMPTS
from datetime import datetime

# Move constants to top
MAX_TOKENS = 512
MIN_TOKENS = 64
MIN_WORDS = 200
TEMPERATURE = 0.7

class GenerationService:
    def __init__(self):
        self.generator = self._initialize_generator()
        self.logger = logging.getLogger(__name__)

    def _initialize_generator(self):
        try:
            return pipeline("text2text-generation",
                          model="google/flan-t5-small",
                          tokenizer="google/flan-t5-small")
        except Exception as e:
            self.logger.error(f"Model initialization error: {e}")
            raise

    def generate(self, prompt: str) -> str:
        try:
            result = self.generator(
                prompt,
                max_length=MAX_TOKENS,
                min_length=MIN_TOKENS,
                do_sample=True,
                temperature=TEMPERATURE,
                num_return_sequences=1
            )
            return result[0]["generated_text"]
        except Exception as e:
            self.logger.error(f"Generation error: {e}")
            raise

generator_service = GenerationService()

# Router setup and route handlers
router = APIRouter(tags=["generation"])

@router.post("/generate", response_model=dict)
async def generate_post(request: GenerationRequest):
    try:
        template_base = TEMPLATE_PROMPTS.get(request.template)
        prompt = create_generation_prompt(template_base, request)
        generated_text = generator_service.generate(prompt)
        processed_text = process_generated_text(generated_text)
        
        if len(processed_text.split()) < MIN_WORDS:
            return await generate_post(request)
        
        # Store the generated post
        stored_post = StoredPost(
            template=request.template,
            objective=request.objective,
            context=request.context,
            generated_content=processed_text
        )
        await db.posts_collection.insert_one(stored_post.dict(by_alias=True))
        
        # Update or create prompt
        await db.prompts_collection.update_one(
            {
                "template": request.template,
                "objective": request.objective,
                "context": request.context
            },
            {
                "$inc": {"use_count": 1},
                "$setOnInsert": {
                    "created_at": datetime.utcnow()
                }
            },
            upsert=True
        )
            
        return {"post": processed_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[StoredPost])
async def get_post_history(
    limit: int = Query(10, gt=0, le=100),
    skip: int = Query(0, ge=0),
):
    """Retrieve generation history"""
    cursor = db.posts_collection.find()
    cursor.sort("created_at", -1).skip(skip).limit(limit)
    posts = await cursor.to_list(length=limit)
    return posts

@router.get("/popular-prompts", response_model=List[StoredPrompt])
async def get_popular_prompts(
    limit: int = Query(5, gt=0, le=20)
):
    """Retrieve most used prompts"""
    cursor = db.prompts_collection.find()
    cursor.sort("use_count", -1).limit(limit)
    prompts = await cursor.to_list(length=limit)
    return prompts

# Helper functions
def create_generation_prompt(template: str, request: GenerationRequest) -> str:
    return (
        "Task: Generate a detailed professional LinkedIn post of MINIMUM 500 words.\n\n"
        f"Style: {template}\n"
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

def process_generated_text(text: str) -> str:
    if "Generated Post:" in text:
        return text.split("Generated Post:", 1)[1].strip()
    return text.strip()
