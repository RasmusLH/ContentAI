from datetime import datetime, timedelta
from jose import jwt, JWTError # type: ignore
from google.oauth2 import id_token # type: ignore
from google.auth.transport import requests # type: ignore
from fastapi import HTTPException, status, Header
from ..config import settings
from ..models import User
from ..database import db
from ..utils.token_utils import create_token, verify_token, get_token_from_header  # Import utility functions
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
            logger.exception("Google token verification failed")
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
                user_dict["_id"] = str(result.inserted_id)
            else:
                user_dict["_id"] = str(user_dict["_id"])
            
            return User(**user_dict)
        except Exception as e:
            logger.exception("Error in get_or_create_user")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing user data"
            )

    def create_token(self, user_id: str) -> str:
        return create_token(user_id, self.jwt_secret, self.jwt_algorithm, self.jwt_expiration)

    def verify_token(self, token: str) -> str:
        return verify_token(token, self.jwt_secret, self.jwt_algorithm)

    def get_token_from_header(self, authorization: str = Header(None)) -> str:
        return get_token_from_header(authorization)
