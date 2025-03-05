from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline

router = APIRouter()


try:
    generator = pipeline("text-generation", model="openai-community/gpt2", tokenizer="openai-community/gpt2", truncation=True)
except Exception as e:
    # Log the error if needed, but for now, we can simply pass
    raise HTTPException(status_code=500, detail=f"Model load error: {e}")

class GenerationRequest(BaseModel):
    objective: str

@router.post("/generate")
async def generate_post(request: GenerationRequest):
    if generator is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Construct an English prompt based on user inputs.
    english_prompt = f"Create a social media post about: {request.objective}. "
    
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
    return {"message": "Welcome to the Social Media Post Generator API!"}
