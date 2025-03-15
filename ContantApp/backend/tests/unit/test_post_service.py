import pytest # type: ignore
from datetime import datetime
from app.services.post_service import PostService
from app.models import StoredPost
from bson import ObjectId

async def test_create_post(mock_db):
    post_data = {
        "template": "tech-insight",
        "objective": "Test objective",
        "context": "Test context", 
        "generated_content": "Test content"
    }
    user_id = "test_user_id"
    
    post = await PostService.create_post(post_data, user_id)
    
    assert isinstance(post, StoredPost)
    assert post.user_id == user_id
    assert post.template == post_data["template"]
    assert post.created_at is not None

async def test_get_user_posts(mock_db):
    # Insert test posts
    test_posts = [
        {
            "user_id": "test_user",
            "template": "tech-insight",
            "objective": "Test 1",
            "context": "Context 1",
            "generated_content": "Content 1",
            "created_at": datetime.utcnow()
        },
        {
            "user_id": "test_user",
            "template": "tech-insight", 
            "objective": "Test 2",
            "context": "Context 2",
            "generated_content": "Content 2",
            "created_at": datetime.utcnow()
        }
    ]
    await mock_db.posts_collection.insert_many(test_posts)
    
    result = await PostService.get_user_posts("test_user", limit=10, skip=0)
    
    assert len(result["posts"]) == 2
    assert result["total"] == 2
    assert result["totalPages"] == 1

async def test_delete_post(mock_db):
    # Insert test post
    post_id = ObjectId()
    test_post = {
        "_id": post_id,
        "user_id": "test_user",
        "template": "tech-insight",
        "objective": "Test",
        "context": "Context",
        "generated_content": "Content"
    }
    await mock_db.posts_collection.insert_one(test_post)
    
    # Test deletion
    success = await PostService.delete_post(str(post_id), "test_user")
    assert success is True
    
    # Verify post was deleted
    post = await mock_db.posts_collection.find_one({"_id": post_id})
    assert post is None
