"""Product schemas for validation and serialization."""

from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import datetime


class ProductBase(BaseModel):
    """Base product schema."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    sku: str = Field(..., min_length=1, max_length=100, description="Stock Keeping Unit")
    price: float = Field(..., gt=0, description="Product price")
    cost: Optional[float] = Field(None, ge=0, description="Product cost")
    quantity: int = Field(0, ge=0, description="Current quantity in stock")
    min_quantity: int = Field(0, ge=0, description="Minimum quantity threshold")
    max_quantity: Optional[int] = Field(None, gt=0, description="Maximum quantity")
    is_active: bool = Field(True, description="Whether product is active")
    category: Optional[str] = Field(None, max_length=100, description="Product category")
    brand: Optional[str] = Field(None, max_length=100, description="Product brand")
    weight: Optional[float] = Field(None, ge=0, description="Product weight")
    dimensions: Optional[str] = Field(None, max_length=100, description="Product dimensions")
    customer_id: Optional[str] = Field(None, max_length=100, description="Associated customer ID")
    
    @validator('max_quantity')
    def validate_max_quantity(cls, v, values):
        """Validate max_quantity is greater than min_quantity."""
        if v is not None and 'min_quantity' in values and v <= values['min_quantity']:
            raise ValueError('max_quantity must be greater than min_quantity')
        return v


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    sku: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    cost: Optional[float] = Field(None, ge=0)
    quantity: Optional[int] = Field(None, ge=0)
    min_quantity: Optional[int] = Field(None, ge=0)
    max_quantity: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None
    category: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    weight: Optional[float] = Field(None, ge=0)
    dimensions: Optional[str] = Field(None, max_length=100)
    customer_id: Optional[str] = Field(None, max_length=100)


class ProductResponse(ProductBase):
    """Schema for product response."""
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ProductFilter(BaseModel):
    """Schema for filtering products."""
    
    name: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    is_active: Optional[bool] = None
    customer_id: Optional[str] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, gt=0)
    min_quantity: Optional[int] = Field(None, ge=0)
    max_quantity: Optional[int] = Field(None, gt=0)
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)
    
    @validator('max_price')
    def validate_max_price(cls, v, values):
        """Validate max_price is greater than min_price."""
        if v is not None and 'min_price' in values and values['min_price'] is not None and v <= values['min_price']:
            raise ValueError('max_price must be greater than min_price')
        return v


class ProductListResponse(BaseModel):
    """Schema for paginated product list response."""
    
    items: List[ProductResponse]
    total: int
    page: int
    size: int
    pages: int