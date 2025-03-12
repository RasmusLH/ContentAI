from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException, status
from ..config import settings
from ..models import User
from ..database import db
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.jwt_secret = settings.jwt_secret
        self.jwt_algorithm = settings.jwt_algorithm
        self.jwt_expiration = settings.jwt_expiration
        self.google_client_id = settings.google_client_id

    async def verify_google_token(self, token: str) -> dict:
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), self.google_client_id
            )
            return idinfo
        except Exception as e:
            logger.error(f"Google token verification failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token"
            )

    async def get_or_create_user(self, google_user_info: dict) -> User:
        try:
            # Check if user exists
            user_dict = await db.users_collection.find_one(
                {"google_id": google_user_info["sub"]}
            )
            
            if not user_dict:
                # Create new user
                user_dict = {
                    "google_id": google_user_info["sub"],
                    "email": google_user_info["email"],
                    "name": google_user_info["name"],
                    "picture": google_user_info.get("picture"),
                    "created_at": datetime.utcnow()
                }
                result = await db.users_collection.insert_one(user_dict)
                user_dict["_id"] = result.inserted_id
            
            return User(**user_dict)
        except Exception as e:
            logger.error(f"Error in get_or_create_user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing user data"
            )

    def create_token(self, user_id: str) -> str:
        expiration = datetime.utcnow() + timedelta(days=self.jwt_expiration)
        to_encode = {"sub": str(user_id), "exp": expiration}
        try:
            return jwt.encode(to_encode, self.jwt_secret, self.jwt_algorithm)
        except Exception as e:
            logger.error(f"Token creation failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create access token"
            )

    def verify_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
            return user_id
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
