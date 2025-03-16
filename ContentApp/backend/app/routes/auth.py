from fastapi import APIRouter, Depends, HTTPException, status
from ..services.auth_service import AuthService
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["auth"])
auth_service = AuthService()

class GoogleTokenRequest(BaseModel):
    token: str

@router.post("/google")
async def google_login(request: GoogleTokenRequest):
    # Verify Google token
    google_user = await auth_service.verify_google_token(request.token)
    
    # Get or create user
    user = await auth_service.get_or_create_user(google_user)
    
    # Create access token
    token = auth_service.create_token(str(user.id))
    
    return {
        "token": token,
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "picture": user.picture
        }
    }
