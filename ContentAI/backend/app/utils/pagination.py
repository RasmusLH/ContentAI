from typing import Dict, Any, List, Tuple
from motor.motor_asyncio import AsyncIOMotorCollection

async def paginate_query(
    collection: AsyncIOMotorCollection,
    query: Dict[str, Any],
    limit: int,
    skip: int,
    sort: List[Tuple[str, int]] = None
) -> Dict[str, Any]:
    """
    Generic pagination utility for MongoDB queries
    """
    # Get total count
    total = await collection.count_documents(query)
    
    # Build cursor
    cursor = collection.find(query)
    if sort:
        cursor.sort(sort)
    cursor.skip(skip).limit(limit)
    
    # Get documents
    documents = await cursor.to_list(length=limit)
    
    # Convert _id to string
    for doc in documents:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
    
    total_pages = (total + limit - 1) // limit
    current_page = (skip // limit) + 1

    return {
        "posts": documents,
        "total": total,
        "page": current_page,
        "totalPages": max(1, total_pages)
    }
