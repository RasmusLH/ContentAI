from datetime import datetime, timedelta
from typing import Dict, Tuple
from fastapi import Request
import logging
from .error_handlers import APIError

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
        
        self._clean_old_requests(now)
        
        if client_ip in self.store:
            count, timestamp = self.store[client_ip]
            if now - timestamp < timedelta(minutes=1):
                if count >= self.requests_per_minute:
                    logger.warning(
                        "Rate limit exceeded",
                        extra={
                            "client_ip": client_ip,
                            "requests_count": count,
                            "limit": self.requests_per_minute
                        }
                    )
                    raise APIError(
                        message="Too many requests. Please try again later.",
                        status_code=429,
                        log_level="warning"
                    )
                self.store[client_ip] = (count + 1, timestamp)
            else:
                self.store[client_ip] = (1, now)
        else:
            self.store[client_ip] = (1, now)
            
        logger.debug(
            "Rate limit check passed",
            extra={
                "client_ip": client_ip,
                "current_count": self.store[client_ip][0]
            }
        )

rate_limiter = RateLimiter()
