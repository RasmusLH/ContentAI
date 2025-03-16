import pytest # type: ignore
from unittest.mock import patch
from app.services.auth_service import AuthService
from app.database import db

async def test_google_login(test_client, mock_db):
    mock_google_info = {
        "sub": "12345",
        "email": "test@example.com",
        "name": "Test User",
        "picture": "http://example.com/pic.jpg"
    }
    
    with patch('app.services.auth_service.AuthService.verify_google_token') as mock_verify:
        mock_verify.return_value = mock_google_info
        
        response = test_client.post(
            "/api/auth/google",
            json={"token": "fake_google_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert data["user"]["email"] == "test@example.com"

async def test_invalid_token(test_client):
    response = test_client.post(
        "/api/auth/google",
        json={"token": "invalid_token"}
    )
    assert response.status_code == 401
