from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline

router = APIRouter()

try:
    generator = pipeline("text-generation", model="Maltehb/danish-gpt2")
except Exception as e:
    # Log the error if needed, but for now, we can simply pass
    generator = None
    print(f"Error loading model: {e}")

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
    
    prompt = f"Create a Danish social media post about: {request.objective}. "
    prompt += f"Tone: {request.tone}. "
    if request.hashtags:
        prompt += f"Include hashtags: {request.hashtags}. "
    if request.context:
        prompt += f"Context: {request.context}. "
    prompt += f"Formality: {request.formality}. "
    prompt += " Ensure the post is culturally tuned for a Danish audience."
    
    try:
        result = generator(prompt, max_length=100, num_return_sequences=1)
        generated_text = result[0]["generated_text"]
        return {"post": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {e}")

@router.get("/")
async def root():
    return {"message": "Welcome to the Danish Social Media Post Generator API!"}
