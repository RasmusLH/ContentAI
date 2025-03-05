from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline

router = APIRouter()

try:
    # Remove truncation parameter here; we'll pass it during generation.
    generator = pipeline("text-generation", model="openai-community/gpt2", tokenizer="openai-community/gpt2")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Model load error: {e}")

class GenerationRequest(BaseModel):
    objective: str

@router.post("/generate")
async def generate_post(request: GenerationRequest):
    if generator is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    english_prompt = (
    "You are a professional LinkedIn content creator. "
    "Generate a compelling and engaging LinkedIn post based on the following context: "
    f"{request.objective}\n\n"
    "The post should include a clear headline, an informative body, and a strong call-to-action. "
    "Ensure the tone is professional, inspiring, and tailored to a business audience.\n\n"
    "Structure:\n"
    "Headline: An engaging title that captures the main idea.\n"
    "Introduction: A brief opening statement that sets the tone and context.\n"
    "Body: A detailed explanation of the product's features, benefits, and unique selling points.\n"
    "Call-to-Action: A clear closing statement encouraging readers to learn more or take action.\n\n"
    "Example:\n"
    "Unlock Your Full Potential with Our Innovative Solutions\n"
    "At [Company], we believe in empowering businesses to thrive in the digital age.\n"
    "Our cutting-edge software solutions are designed to streamline your operations and boost productivity.\n"
    "Discover the future of business with [Company]. Visit our website to learn more!\n\n"
    "Post:\n"
        )
    
    try:
        # Pass truncation=True and pad_token_id explicitly here.
        result = generator(
            english_prompt,
            max_length=150,
            num_return_sequences=1,
            truncation=True,
            pad_token_id=generator.tokenizer.eos_token_id
        )
        # The correct key is "generated_text"
        generated_text = result[0]["generated_text"]
        return {"post": generated_text}
    except Exception as e:
        # Log the full exception message for debugging.
        raise HTTPException(status_code=500, detail=f"Generation error: {e}")

@router.get("/")
async def root():
    return {"message": "Welcome to the Social Media Post Generator API!"}
