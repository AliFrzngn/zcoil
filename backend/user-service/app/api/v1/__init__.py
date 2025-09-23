"""API v1 module."""

from fastapi import APIRouter
from .endpoints import auth_router, users_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(users_router)