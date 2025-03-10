from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from transformers import pipeline
import logging
from enum import Enum
from typing import Optional

# Move constants to top
MAX_TOKENS = 512
MIN_TOKENS = 64
MIN_WORDS = 200
TEMPERATURE = 0.7

class TemplateType(str, Enum):
    TECH_INSIGHT = "tech-insight"
    STARTUP_STORY = "startup-story"
    PRODUCT_LAUNCH = "product-launch"
    INDUSTRY_UPDATE = "industry-update"

class GenerationRequest(BaseModel):
    template: TemplateType
    objective: str = Field(..., min_length=10, max_length=500)
    context: str = Field(..., min_length=10, max_length=1000)

    class Config:
        schema_extra = {
            "example": {
                "template": "tech-insight",
                "objective": "Discuss the impact of AI on software development",
                "context": "Recent advancements in AI tools and their adoption in dev teams"
            }
        }

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
router = APIRouter(prefix="/api/v1", tags=["generation"])

@router.post("/generate", response_model=dict)
async def generate_post(request: GenerationRequest):
    try:
        template_base = TEMPLATE_PROMPTS.get(request.template)
        prompt = create_generation_prompt(template_base, request)
        generated_text = generator_service.generate(prompt)
        processed_text = process_generated_text(generated_text)
        
        if len(processed_text.split()) < MIN_WORDS:
            return await generate_post(request)
            
        return {"post": processed_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

TEMPLATE_PROMPTS = {
    TemplateType.TECH_INSIGHT: "Create a LinkedIn post discussing technology trends, focusing on innovation impact and future implications.",
    TemplateType.STARTUP_STORY: "Write an inspiring LinkedIn post about a startup journey, highlighting key milestones, challenges overcome, and lessons learned.",
    TemplateType.PRODUCT_LAUNCH: "Craft an engaging LinkedIn announcement about a new product launch, emphasizing unique features and customer benefits.",
    TemplateType.INDUSTRY_UPDATE: "Compose a LinkedIn post analyzing industry trends, market developments, and their business implications."
}

@router.get("/")
async def root():
    return {"message": "Welcome to the Social Media Post Generator API!"}
