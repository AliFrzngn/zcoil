"""Test customer service."""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException

from backend.crm_service.services.customer_service import CustomerService


@pytest.mark.asyncio
async def test_get_customer_products_success(mock_inventory_response):
    """Test getting customer products successfully."""
    with patch('backend.crm_service.services.customer_service.HTTPClient') as mock_client_class:
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_inventory_response
        mock_client_class.return_value = mock_client
        
        service = CustomerService()
        products = await service.get_customer_products("customer-123")
        
        assert len(products) == 1
        assert products[0].name == "Test Product"
        assert products[0].sku == "TEST-001"
        assert products[0].price == 99.99


@pytest.mark.asyncio
async def test_get_customer_products_http_error():
    """Test getting customer products with HTTP error."""
    with patch('backend.crm_service.services.customer_service.HTTPClient') as mock_client_class:
        mock_client = AsyncMock()
        mock_client.get.side_effect = HTTPException(status_code=404, detail="Not found")
        mock_client_class.return_value = mock_client
        
        service = CustomerService()
        
        with pytest.raises(HTTPException) as exc_info:
            await service.get_customer_products("customer-123")
        
        assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_get_customer_products_service_unavailable():
    """Test getting customer products when service is unavailable."""
    with patch('backend.crm_service.services.customer_service.HTTPClient') as mock_client_class:
        mock_client = AsyncMock()
        mock_client.get.side_effect = Exception("Connection error")
        mock_client_class.return_value = mock_client
        
        service = CustomerService()
        
        with pytest.raises(HTTPException) as exc_info:
            await service.get_customer_products("customer-123")
        
        assert exc_info.value.status_code == 503
        assert "Failed to retrieve customer products" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_get_customer_product_details_success(mock_product_details):
    """Test getting customer product details successfully."""
    with patch('backend.crm_service.services.customer_service.HTTPClient') as mock_client_class:
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_product_details
        mock_client_class.return_value = mock_client
        
        service = CustomerService()
        product = await service.get_customer_product_details("customer-123", 1)
        
        assert product.name == "Test Product"
        assert product.sku == "TEST-001"
        assert product.customer_id == "customer-123"


@pytest.mark.asyncio
async def test_get_customer_product_details_wrong_customer(mock_product_details):
    """Test getting product details for wrong customer."""
    # Modify mock response to have different customer_id
    mock_product_details["customer_id"] = "customer-456"
    
    with patch('backend.crm_service.services.customer_service.HTTPClient') as mock_client_class:
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_product_details
        mock_client_class.return_value = mock_client
        
        service = CustomerService()
        
        with pytest.raises(HTTPException) as exc_info:
            await service.get_customer_product_details("customer-123", 1)
        
        assert exc_info.value.status_code == 403
        assert "does not belong to this customer" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_search_customer_products_success(mock_inventory_response):
    """Test searching customer products successfully."""
    with patch('backend.crm_service.services.customer_service.HTTPClient') as mock_client_class:
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_inventory_response
        mock_client_class.return_value = mock_client
        
        service = CustomerService()
        products = await service.search_customer_products(
            customer_id="customer-123",
            name="Test",
            category="Electronics"
        )
        
        assert len(products) == 1
        assert products[0].name == "Test Product"
        
        # Verify the correct parameters were passed
        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == "/api/v1/items/"
        assert call_args[1]["params"]["customer_id"] == "customer-123"
        assert call_args[1]["params"]["name"] == "Test"
        assert call_args[1]["params"]["category"] == "Electronics"
        assert call_args[1]["params"]["is_active"] is True


@pytest.mark.asyncio
async def test_search_customer_products_service_error():
    """Test searching customer products with service error."""
    with patch('backend.crm_service.services.customer_service.HTTPClient') as mock_client_class:
        mock_client = AsyncMock()
        mock_client.get.side_effect = Exception("Service error")
        mock_client_class.return_value = mock_client
        
        service = CustomerService()
        
        with pytest.raises(HTTPException) as exc_info:
            await service.search_customer_products("customer-123")
        
        assert exc_info.value.status_code == 503
        assert "Failed to search customer products" in str(exc_info.value.detail)
