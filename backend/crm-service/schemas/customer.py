"""Customer schemas for CRM service."""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CustomerProductResponse(BaseModel):
    """Schema for customer product response."""
    
    id: int
    name: str
    description: Optional[str] = None
    sku: str
    price: float
    quantity: int
    category: Optional[str] = None
    brand: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CustomerProductListResponse(BaseModel):
    """Schema for customer product list response."""
    
    items: List[CustomerProductResponse]
    total: int
    customer_id: str