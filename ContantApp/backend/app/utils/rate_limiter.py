from datetime import datetime, timedelta
from typing import Dict, Tuple
from fastapi import HTTPException, Request
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, requests_per_minute: int = 30):
        self.requests_per_minute = requests_per_minute
        self.store: Dict[str, Tuple[int, datetime]] = {}
    
    def _clean_old_requests(self, now: datetime):
        expired = [
            key for key, (_, timestamp) in self.store.items()
            if now - timestamp > timedelta(minutes=1)
        ]
        for key in expired:
            del self.store[key]
    
    async def check_rate_limit(self, request: Request):
        client_ip = request.client.host if request.client else "unknown"
        now = datetime.utcnow()
        
        # Clean old entries
        self._clean_old_requests(now)
        
        # Check and update rate limit
        if client_ip in self.store:
            count, timestamp = self.store[client_ip]
            if now - timestamp < timedelta(minutes=1):
                if count >= self.requests_per_minute:
                    logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                    raise HTTPException(
                        status_code=429,
                        detail="Too many requests. Please try again later."
                    )
                self.store[client_ip] = (count + 1, timestamp)
            else:
                self.store[client_ip] = (1, now)
        else:
            self.store[client_ip] = (1, now)

rate_limiter = RateLimiter()
