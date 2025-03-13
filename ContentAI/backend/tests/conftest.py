import pytest
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
from app.config import settings
from app.database import db
from app.appmain import app
import asyncio
from datetime import datetime, timedelta
from jose import jwt

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def mock_db() -> AsyncGenerator:
    # Create mock MongoDB client
    mock_client = AsyncMongoMockClient()
    db.client = mock_client
    db.posts_collection = mock_client[settings.mongodb_name]["posts"]
    db.prompts_collection = mock_client[settings.mongodb_name]["prompts"]
    db.users_collection = mock_client[settings.mongodb_name]["users"]
    yield mock_client
    mock_client.close()

@pytest.fixture
def test_client(mock_db) -> Generator:
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_openai_response():
    return {
        "choices": [
            {
                "message": {
                    "content": "Test generated content"
                }
            }
        ]
    }

@pytest.fixture
def auth_token() -> str:
    # Create a test JWT token
    expiration = datetime.utcnow() + timedelta(days=1)
    test_token = jwt.encode(
        {"sub": "test_user_id", "exp": expiration},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )
    return f"Bearer {test_token}"

@pytest.fixture
async def test_user(mock_db):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "google_id": "test123",
        "created_at": datetime.utcnow()
    }
    result = await db.users_collection.insert_one(user_data)
    user_data["_id"] = str(result.inserted_id)
    return user_data

@pytest.fixture
async def test_posts(mock_db, test_user):
    """Create test posts fixture"""
    test_posts = [
        {
            "user_id": test_user["_id"],
            "template": "tech-insight",
            "objective": "Test objective 1",
            "context": "Test context 1",
            "generated_content": "Test content 1",
            "created_at": datetime.utcnow()
        },
        {
            "user_id": test_user["_id"],
            "template": "tech-insight",
            "objective": "Test objective 2", 
            "context": "Test context 2",
            "generated_content": "Test content 2",
            "created_at": datetime.utcnow()
        }
    ]
    
    result = await db.posts_collection.insert_many(test_posts)
    post_ids = [str(id) for id in result.inserted_ids]
    
    return {
        "posts": test_posts,
        "ids": post_ids
    }
