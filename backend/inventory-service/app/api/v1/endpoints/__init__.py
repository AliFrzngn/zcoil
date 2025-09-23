"""Inventory service API endpoints."""

from .items import router as items_router

__all__ = ["items_router"]