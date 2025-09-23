"""Customer service business logic."""

from typing import List, Dict, Any
from fastapi import HTTPException, status
from backend.shared.utils import HTTPClient
from backend.shared.config import settings
from schemas.customer import CustomerProductResponse


class CustomerService:
    """Customer service for CRM operations."""
    
    def __init__(self):
        self.inventory_client = HTTPClient(settings.inventory_service_url)
    
    async def get_customer_products(self, customer_id: str) -> List[CustomerProductResponse]:
        """Get products associated with a customer."""
        try:
            # Call inventory service to get customer products
            response = await self.inventory_client.get(f"/api/v1/items/customer/{customer_id}")
            
            # Convert response to our schema
            products = []
            for item in response.get("items", []):
                products.append(CustomerProductResponse(**item))
            
            return products
            
        except HTTPException as e:
            # Re-raise HTTP exceptions
            raise e
        except Exception as e:
            # Handle unexpected errors
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to retrieve customer products: {str(e)}"
            )
    
    async def get_customer_product_details(self, customer_id: str, product_id: int) -> CustomerProductResponse:
        """Get specific product details for a customer."""
        try:
            # First get the product details
            response = await self.inventory_client.get(f"/api/v1/items/{product_id}")
            product_data = response
            
            # Verify the product belongs to the customer
            if product_data.get("customer_id") != customer_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Product does not belong to this customer"
                )
            
            return CustomerProductResponse(**product_data)
            
        except HTTPException as e:
            # Re-raise HTTP exceptions
            raise e
        except Exception as e:
            # Handle unexpected errors
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to retrieve product details: {str(e)}"
            )
    
    async def search_customer_products(
        self, 
        customer_id: str, 
        name: str = None, 
        category: str = None,
        brand: str = None
    ) -> List[CustomerProductResponse]:
        """Search products for a specific customer."""
        try:
            # Build query parameters
            params = {
                "customer_id": customer_id,
                "is_active": True  # Only show active products
            }
            
            if name:
                params["name"] = name
            if category:
                params["category"] = category
            if brand:
                params["brand"] = brand
            
            # Call inventory service
            response = await self.inventory_client.get("/api/v1/items/", params=params)
            
            # Convert response to our schema
            products = []
            for item in response.get("items", []):
                products.append(CustomerProductResponse(**item))
            
            return products
            
        except HTTPException as e:
            # Re-raise HTTP exceptions
            raise e
        except Exception as e:
            # Handle unexpected errors
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to search customer products: {str(e)}"
            )