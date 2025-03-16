from fastapi import APIRouter
from ..database import db

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy"}

@router.get("/db")
async def database_health_check():
    """Check database connectivity"""
    try:
        # Ping the database if client exists
        if db.client:
            await db.client.admin.command('ping')
            return {"status": "healthy", "database": "connected"}
        else:
            return {"status": "unhealthy", "database": "not connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)} 