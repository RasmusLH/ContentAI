from datetime import datetime, timedelta
from jose import jwt, JWTError # type: ignore
from fastapi import HTTPException, status, Header
import logging

logger = logging.getLogger(__name__)

def create_token(user_id: str, secret: str, algorithm: str, expiration_days: int) -> str:
    expiration = datetime.utcnow() + timedelta(days=expiration_days)
    to_encode = {"sub": str(user_id), "exp": expiration}
    try:
        return jwt.encode(to_encode, secret, algorithm)
    except Exception as e:
        logger.exception("Token creation failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create access token"
        )

def verify_token(token: str, secret: str, algorithm: str) -> str:
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
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

def get_token_from_header(authorization: str = Header(None)) -> str:
    logger.info(f"Authorization header received: {authorization}")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    return authorization.split(" ")[1]
