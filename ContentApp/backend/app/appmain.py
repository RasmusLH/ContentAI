from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
from .routes import api_router, auth_router
from .routes.health import router as health_router
from .database import connect_to_mongo, close_mongo_connection
from .utils.logging_config import setup_logging
from .utils.error_handlers import APIError, handle_api_error
import uuid
import traceback
from .config import settings

# Configure logging first
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="LinkedIn Post Generator", debug=True)

# Add CORS middleware first
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
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
    start_time = time.time()
    
    # Log request details before processing
    logger.info(f"Incoming {request.method} request to {request.url.path}",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.query_params),
            "client_host": request.client.host if request.client else None
        }
    )
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Log response details
        logger.info(f"Request completed in {duration:.2f}s",
            extra={
                "request_id": request_id,
                "duration": f"{duration:.2f}s",
                "status_code": response.status_code,
                "path": request.url.path
            }
        )
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}",
            extra={
                "request_id": request_id,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "path": request.url.path
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

@app.get("/favicon.ico")
async def favicon():
    from fastapi.responses import FileResponse
    # Adjust the path below if your favicon.ico is stored elsewhere
    return FileResponse("static/favicon.ico")

# Mount the routers
app.include_router(api_router)
app.include_router(auth_router)
app.include_router(health_router)

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
