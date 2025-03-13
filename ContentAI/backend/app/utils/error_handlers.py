from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
import traceback
from openai import OpenAIError  # Updated import path

logger = logging.getLogger(__name__)

class APIError(Exception):
    def __init__(self, message: str, status_code: int = 500, details: Dict[str, Any] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

async def handle_api_error(error: APIError) -> JSONResponse:
    logger.error(f"API Error: {error.message}", extra={
        "status_code": error.status_code,
        "details": error.details,
        "traceback": traceback.format_exc()
    })
    return JSONResponse(
        status_code=error.status_code,
        content={"error": error.message, "details": error.details}
    )

def handle_openai_error(error: OpenAIError) -> APIError:
    error_map = {
        "invalid_request_error": (400, "Invalid request to OpenAI API"),
        "authentication_error": (401, "OpenAI API authentication failed"),
        "permission_error": (403, "Permission denied by OpenAI API"),
        "rate_limit_error": (429, "OpenAI API rate limit exceeded"),
        "api_error": (500, "OpenAI API error"),
    }
    
    # Get error type from new OpenAI error structure
    error_type = getattr(error, "type", None) or getattr(error, "code", "api_error")
    status_code, message = error_map.get(error_type, (500, "OpenAI API error"))
    
    return APIError(
        message=message,
        status_code=status_code,
        details={"openai_error": str(error)}
    )

def handle_database_error(error: Exception) -> APIError:
    logger.error(f"Database Error: {str(error)}", exc_info=True)
    return APIError(
        message="Database operation failed",
        status_code=500,
        details={"db_error": str(error)}
    )
