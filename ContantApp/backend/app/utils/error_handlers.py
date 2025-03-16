from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import logging
import traceback
from openai import OpenAIError

logger = logging.getLogger(__name__)

class APIError(Exception):
    def __init__(
        self, 
        message: str, 
        status_code: int = 500, 
        details: Optional[Dict[str, Any]] = None,
        log_level: str = "error"
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.log_level = log_level
        super().__init__(self.message)

async def handle_api_error(error: APIError) -> JSONResponse:
    # Get logging function based on level
    log_func = getattr(logger, error.log_level)
    
    log_func(
        f"API Error: {error.message}",
        extra={
            "status_code": error.status_code,
            "details": error.details,
            "error_type": error.__class__.__name__,
            "traceback": traceback.format_exc()
        }
    )
    
    return JSONResponse(
        status_code=error.status_code,
        content={"error": error.message, "details": error.details}
    )

def handle_openai_error(error: OpenAIError) -> APIError:
    error_types = {
        "invalid_request_error": (400, "Invalid request parameters"),
        "authentication_error": (401, "Authentication failed"),
        "permission_error": (403, "Permission denied"),
        "rate_limit_error": (429, "Rate limit exceeded"),
        "api_error": (500, "External API error"),
    }
    
    error_type = getattr(error, "type", None) or getattr(error, "code", "api_error")
    status_code, message = error_types.get(error_type, (500, "External service error"))
    
    return APIError(
        message=message,
        status_code=status_code,
        details={"service": "OpenAI", "error": str(error)},
        log_level="warning" if status_code == 429 else "error"
    )

def handle_database_error(error: Exception) -> APIError:
    logger.error(f"Database Error: {str(error)}", exc_info=True)
    return APIError(
        message="Database operation failed",
        status_code=500,
        details={"db_error": str(error)}
    )

async def handle_api_operation(
    operation_name: str,
    coroutine,
    error_msg: str = "Operation failed",
    status_code: int = 500
) -> Any:
    """Standardized error handling for API operations"""
    try:
        logger.info(f"Starting {operation_name}")
        result = await coroutine
        logger.info(
            f"Successfully completed {operation_name}",
            extra={"operation": operation_name}
        )
        return result
    except Exception as e:
        logger.error(
            f"{operation_name} failed",
            exc_info=True,
            extra={
                "operation": operation_name,
                "error_type": e.__class__.__name__,
                "error": str(e)
            }
        )
        raise APIError(
            message=error_msg,
            status_code=status_code,
            details={"operation": operation_name, "error": str(e)}
        )
