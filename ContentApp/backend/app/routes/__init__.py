from .auth import router as auth_router
from .api import router as api_router
from .health import router as health_router

__all__ = ['auth_router', 'api_router', 'health_router']
