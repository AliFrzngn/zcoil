"""Base model for inventory service."""

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from backend.shared.database import Base as SharedBase


class Base(SharedBase):
    """Base model with common fields."""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
