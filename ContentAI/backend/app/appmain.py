from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
from .routes import api_router, auth_router
from .database import connect_to_mongo, close_mongo_connection

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    logger.info(f"Headers: {request.headers}")
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        logger.info(f"Request completed - Duration: {duration:.2f}s - Status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
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
