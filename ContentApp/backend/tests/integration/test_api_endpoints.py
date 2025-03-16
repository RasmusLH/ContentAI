import pytest
from fastapi.testclient import TestClient
from app.database import db
from datetime import datetime
from unittest.mock import patch
import json

async def test_generate_post(test_client: TestClient, auth_token: str, mock_openai_response):
    with patch('app.services.generation_service.GenerationService.generate_text') as mock_generate:
        mock_generate.return_value = "Test generated content"
        
        response = test_client.post(
            "/api/generate",
            headers={"Authorization": auth_token},
            data={
                "template": "tech-insight",
                "objective": "Test objective",
                "context": "Test context"
            }
        )
        
        assert response.status_code == 200
        assert "post" in response.json()
        assert response.json()["post"] == "Test generated content"

async def test_get_post_history(test_client: TestClient, auth_token: str, test_user):
    # Insert test posts
    test_posts = [
        {
            "user_id": test_user["_id"],
            "template": "tech-insight",
            "objective": "Test objective",
            "context": "Test context",
            "generated_content": "Test content",
            "created_at": datetime.utcnow()
        }
    ]
    await db.posts_collection.insert_many(test_posts)
    
    response = test_client.get(
        "/api/history",
        headers={"Authorization": auth_token}
    )
    
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 1
    assert posts[0]["objective"] == "Test objective"

async def test_delete_post(test_client: TestClient, auth_token: str, test_user):
    # Insert test post
    post = {
        "user_id": test_user["_id"],
        "template": "tech-insight",
        "objective": "Test objective",
        "content": "Test content"
    }
    result = await db.posts_collection.insert_one(post)
    post_id = str(result.inserted_id)
    
    response = test_client.delete(
        f"/api/posts/{post_id}",
        headers={"Authorization": auth_token}
    )
    
    assert response.status_code == 200
    assert (await db.posts_collection.count_documents({})) == 0

async def test_unauthorized_access(test_client: TestClient):
    response = test_client.get("/api/history")
    assert response.status_code == 401

async def test_get_post_history_with_search(test_client: TestClient, auth_token: str, test_user):
    # Insert test posts with searchable content
    test_posts = [
        {
            "user_id": test_user["_id"],
            "template": "tech-insight",
            "objective": "Searchable objective",
            "context": "Test context",
            "generated_content": "Test content",
            "created_at": datetime.utcnow()
        },
        {
            "user_id": test_user["_id"],
            "template": "tech-insight",
            "objective": "Different objective",
            "context": "Different context",
            "generated_content": "Different content",
            "created_at": datetime.utcnow()
        }
    ]
    await db.posts_collection.insert_many(test_posts)
    
    response = test_client.get(
        "/api/history?search=searchable",
        headers={"Authorization": auth_token}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["posts"]) == 1
    assert data["posts"][0]["objective"] == "Searchable objective"

async def test_pagination(test_client: TestClient, auth_token: str, test_user):
    # Insert multiple posts
    test_posts = []
    for i in range(15):  # Create 15 posts
        test_posts.append({
            "user_id": test_user["_id"],
            "template": "tech-insight",
            "objective": f"Test objective {i}",
            "context": "Test context",
            "generated_content": "Test content",
            "created_at": datetime.utcnow()
        })
    await db.posts_collection.insert_many(test_posts)
    
    # Test first page
    response = test_client.get(
        "/api/history?limit=10&skip=0",
        headers={"Authorization": auth_token}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["posts"]) == 10
    assert data["total"] == 15
    assert data["totalPages"] == 2
