from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from ..database import get_database

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy"}

@router.get("/db")
async def database_health_check(db: AsyncIOMotorClient = Depends(get_database)):
    """Check database connectivity"""
    try:
        # Ping the database
        await db.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)} 