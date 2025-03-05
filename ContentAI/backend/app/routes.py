from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline

router = APIRouter()


try:
    generator = pipeline("text2text-generation", model="google/mt5-small")
except Exception as e:
    # Log the error if needed, but for now, we can simply pass
    raise HTTPException(status_code=500, detail=f"Model load error: {e}")

class GenerationRequest(BaseModel):
    objective: str
    tone: str  # e.g., 'friendly', 'professional', 'humorous', etc.
    hashtags: str = ""
    context: str = ""
    apply_danish_enhancements: bool = True
    formality: str = "casual"


@router.post("/generate")
async def generate_post(request: GenerationRequest):
    if generator is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Construct an English prompt based on user inputs.
    english_prompt = f"Create a social media post about: {request.objective}. "
    english_prompt += f"Tone: {request.tone}. "
    if request.hashtags:
        english_prompt += f"Include hashtags: {request.hashtags}. "
    if request.context:
        english_prompt += f"Context: {request.context}. "
    english_prompt += f"Formality: {request.formality}. "
    english_prompt += " Ensure the post is culturally tuned for a Danish audience."
    
    try:
        # Translate the English prompt to Danish.
        result = generator(english_prompt, max_length=100, num_return_sequences=1)
        # The generation pipeline returns a dict with the key "generator_text"
        generated_text = result[0]["generator_text"]
        return {"post": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {e}")


@router.get("/")
async def root():
    return {"message": "Welcome to the Danish Social Media Post Generator API!"}
