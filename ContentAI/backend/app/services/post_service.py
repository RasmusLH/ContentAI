from datetime import datetime
from typing import Dict, Any, List
from bson import ObjectId
from ..database import db
from ..models import StoredPost
from ..utils.pagination import paginate_query

class PostService:
    @staticmethod
    async def create_post(post_data: Dict[str, Any], user_id: str) -> StoredPost:
        post_data["user_id"] = user_id
        post_data["created_at"] = datetime.utcnow()
        result = await db.posts_collection.insert_one(post_data)
        post_data["_id"] = str(result.inserted_id)
        return StoredPost(**post_data)

    @staticmethod
    async def get_user_posts(user_id: str, limit: int = 10, skip: int = 0, search: str = None):
        query = {"user_id": user_id}
        if search:
            query["$or"] = [
                {"objective": {"$regex": search, "$options": "i"}},
                {"generated_content": {"$regex": search, "$options": "i"}}
            ]
        
        return await paginate_query(
            collection=db.posts_collection,
            query=query,
            limit=limit,
            skip=skip,
            sort=[("created_at", -1)]
        )

    @staticmethod
    async def delete_post(post_id: str, user_id: str) -> bool:
        result = await db.posts_collection.delete_one({
            "_id": ObjectId(post_id),
            "user_id": user_id
        })
        return result.deleted_count > 0
