from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from .config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    posts_collection: Collection = None
    prompts_collection: Collection = None

db = Database()

async def connect_to_mongo():
    try:
        db.client = AsyncIOMotorClient(settings.mongodb_url)
        # Test connection
        await db.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        
        # Initialize collections
        db.posts_collection = db.client[settings.mongodb_name]["posts"]
        db.prompts_collection = db.client[settings.mongodb_name]["prompts"]
        
        # Create indexes
        await db.posts_collection.create_index("created_at")
        await db.prompts_collection.create_index("template")
        
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    if db.client:
        db.client.close()
