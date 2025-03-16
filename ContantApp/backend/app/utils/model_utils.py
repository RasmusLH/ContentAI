from typing import Dict, Any
from ..config import settings

def get_text_generation_params() -> Dict[str, Any]:
    """Centralize text generation parameters"""
    return {
        "model": settings.openai_model,
        "max_tokens": settings.max_tokens,
        "temperature": settings.temperature,
        "presence_penalty": settings.presence_penalty,
        "frequency_penalty": settings.frequency_penalty
    }

def get_image_generation_params() -> Dict[str, Any]:
    """Centralize image generation parameters"""
    return {
        "model": settings.openai_image_model,
        "n": 1,
        "size": "1024x1024",
        "quality": "standard",
        "response_format": "url"
    }
