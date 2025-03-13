from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
from .routes import api_router, auth_router
from .database import connect_to_mongo, close_mongo_connection
from .utils.logging_config import setup_logging
from .utils.error_handlers import APIError, handle_api_error
import uuid
import traceback

# Configure logging first
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="LinkedIn Post Generator", debug=True)

# Add CORS middleware first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False
)

# Add error handler
@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return await handle_api_error(exc)

# Update request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    logger.info(
        "Incoming request",
        extra={
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client_host": request.client.host if request.client else None,
            "headers": dict(request.headers)
        }
    )
    
    try:
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        
        logger.info(
            "Request completed",
            extra={
                "request_id": request_id,
                "duration": f"{duration:.2f}s",
                "status_code": response.status_code
            }
        )
        return response
    except Exception as e:
        logger.error(
            "Request failed",
            extra={
                "request_id": request_id,
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )
        raise

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "API is running"}

@app.get("/health")
async def health():
    # New health check endpoint to verify backend is reachable
    return {"status": "ok", "message": "Backend is running"}

@app.get("/favicon.ico")
async def favicon():
    from fastapi.responses import FileResponse
    # Adjust the path below if your favicon.ico is stored elsewhere
    return FileResponse("static/favicon.ico")

# Mount the routers
app.include_router(api_router)
app.include_router(auth_router)

# Debug endpoint
@app.get("/debug/routes")
async def debug_routes():
    routes = [
        {
            "path": route.path,
            "name": route.name,
            "methods": route.methods
        }
        for route in app.routes
    ]
    return {"routes": routes}
