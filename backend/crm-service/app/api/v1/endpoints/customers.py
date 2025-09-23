"""Customer API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from backend.shared.auth import get_current_customer
from ...schemas.customer import CustomerProductResponse, CustomerProductListResponse
from ...services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/my-items", response_model=CustomerProductListResponse)
async def get_my_items(
    current_customer: dict = Depends(get_current_customer)
):
    """Get products associated with the current customer."""
    customer_id = current_customer["user_id"]
    service = CustomerService()
    
    try:
        products = await service.get_customer_products(customer_id)
        
        return CustomerProductListResponse(
            items=products,
            total=len(products),
            customer_id=customer_id
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve customer items: {str(e)}"
        )


@router.get("/my-items/{product_id}", response_model=CustomerProductResponse)
async def get_my_item(
    product_id: int,
    current_customer: dict = Depends(get_current_customer)
):
    """Get specific product details for the current customer."""
    customer_id = current_customer["user_id"]
    service = CustomerService()
    
    try:
        product = await service.get_customer_product_details(customer_id, product_id)
        return product
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve product details: {str(e)}"
        )


@router.get("/my-items/search/", response_model=CustomerProductListResponse)
async def search_my_items(
    name: Optional[str] = Query(None, description="Search by product name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    brand: Optional[str] = Query(None, description="Filter by brand"),
    current_customer: dict = Depends(get_current_customer)
):
    """Search products for the current customer."""
    customer_id = current_customer["user_id"]
    service = CustomerService()
    
    try:
        products = await service.search_customer_products(
            customer_id=customer_id,
            name=name,
            category=category,
            brand=brand
        )
        
        return CustomerProductListResponse(
            items=products,
            total=len(products),
            customer_id=customer_id
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search customer items: {str(e)}"
        )