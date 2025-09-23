"""Items API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.shared.database import get_db
from schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
    ProductFilter
)
from services.product_service import ProductService

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: ProductCreate,
    db: Session = Depends(get_db)
):
    """Create a new item."""
    service = ProductService(db)
    return service.create_product(item_data)


@router.get("/", response_model=ProductListResponse)
async def get_items(
    name: str = Query(None, description="Filter by product name"),
    category: str = Query(None, description="Filter by category"),
    brand: str = Query(None, description="Filter by brand"),
    is_active: bool = Query(None, description="Filter by active status"),
    customer_id: str = Query(None, description="Filter by customer ID"),
    min_price: float = Query(None, ge=0, description="Minimum price"),
    max_price: float = Query(None, gt=0, description="Maximum price"),
    min_quantity: int = Query(None, ge=0, description="Minimum quantity"),
    max_quantity: int = Query(None, gt=0, description="Maximum quantity"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db)
):
    """Get items with filtering and pagination."""
    filters = ProductFilter(
        name=name,
        category=category,
        brand=brand,
        is_active=is_active,
        customer_id=customer_id,
        min_price=min_price,
        max_price=max_price,
        min_quantity=min_quantity,
        max_quantity=max_quantity,
        page=page,
        size=size
    )
    
    service = ProductService(db)
    products, total = service.get_products(filters)
    
    pages = (total + size - 1) // size
    
    return ProductListResponse(
        items=products,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/{item_id}", response_model=ProductResponse)
async def get_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get item by ID."""
    service = ProductService(db)
    return service.get_product(item_id)


@router.put("/{item_id}", response_model=ProductResponse)
async def update_item(
    item_id: int,
    item_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update item."""
    service = ProductService(db)
    return service.update_product(item_id, item_data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Delete item."""
    service = ProductService(db)
    service.delete_product(item_id)


@router.get("/customer/{customer_id}", response_model=List[ProductResponse])
async def get_customer_items(
    customer_id: str,
    db: Session = Depends(get_db)
):
    """Get items associated with a customer."""
    service = ProductService(db)
    return service.get_products_by_customer(customer_id)


@router.patch("/{item_id}/quantity")
async def update_quantity(
    item_id: int,
    quantity_change: int = Query(..., description="Quantity change (positive or negative)"),
    db: Session = Depends(get_db)
):
    """Update item quantity."""
    service = ProductService(db)
    return service.update_quantity(item_id, quantity_change)


@router.get("/low-stock/", response_model=List[ProductResponse])
async def get_low_stock_items(
    threshold: int = Query(None, ge=0, description="Low stock threshold"),
    db: Session = Depends(get_db)
):
    """Get items with low stock."""
    service = ProductService(db)
    return service.get_low_stock_products(threshold)