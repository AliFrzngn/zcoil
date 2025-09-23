"""API v1 module."""

from fastapi import APIRouter
from .endpoints import notifications

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(notifications.router)
