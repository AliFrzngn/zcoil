"""API v1 module."""

from fastapi import APIRouter
from .endpoints import customers_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(customers_router)