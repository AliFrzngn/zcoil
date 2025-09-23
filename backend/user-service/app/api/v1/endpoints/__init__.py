"""User service API endpoints."""

from .auth import router as auth_router
from .users import router as users_router
from .files import router as files_router
from .audit import router as audit_router

__all__ = ["auth_router", "users_router", "files_router", "audit_router"]