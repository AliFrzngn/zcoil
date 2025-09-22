"""Test customer API endpoints."""

import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient


def test_get_my_items_success(client, mock_customer, mock_inventory_response):
    """Test getting my items successfully."""
    with patch('backend.crm_service.app.api.v1.endpoints.customers.get_current_customer') as mock_auth:
        mock_auth.return_value = mock_customer
        
        with patch('backend.crm_service.services.customer_service.CustomerService.get_customer_products') as mock_service:
            mock_service.return_value = [AsyncMock()]
            mock_service.return_value[0].name = "Test Product"
            mock_service.return_value[0].sku = "TEST-001"
            mock_service.return_value[0].price = 99.99
            
            response = client.get("/api/v1/customers/my-items")
            
            assert response.status_code == 200
            data = response.json()
            assert "items" in data
            assert "total" in data
            assert "customer_id" in data
            assert data["customer_id"] == "customer-123"


def test_get_my_items_unauthorized(client):
    """Test getting my items without authentication."""
    with patch('backend.crm_service.app.api.v1.endpoints.customers.get_current_customer') as mock_auth:
        from fastapi import HTTPException
        mock_auth.side_effect = HTTPException(status_code=401, detail="Unauthorized")
        
        response = client.get("/api/v1/customers/my-items")
        
        assert response.status_code == 401


def test_get_my_item_success(client, mock_customer, mock_product_details):
    """Test getting specific item successfully."""
    with patch('backend.crm_service.app.api.v1.endpoints.customers.get_current_customer') as mock_auth:
        mock_auth.return_value = mock_customer
        
        with patch('backend.crm_service.services.customer_service.CustomerService.get_customer_product_details') as mock_service:
            mock_product = AsyncMock()
            mock_product.name = "Test Product"
            mock_product.sku = "TEST-001"
            mock_product.price = 99.99
            mock_service.return_value = mock_product
            
            response = client.get("/api/v1/customers/my-items/1")
            
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "Test Product"
            assert data["sku"] == "TEST-001"


def test_get_my_item_not_found(client, mock_customer):
    """Test getting non-existent item."""
    with patch('backend.crm_service.app.api.v1.endpoints.customers.get_current_customer') as mock_auth:
        mock_auth.return_value = mock_customer
        
        with patch('backend.crm_service.services.customer_service.CustomerService.get_customer_product_details') as mock_service:
            from fastapi import HTTPException
            mock_service.side_effect = HTTPException(status_code=404, detail="Product not found")
            
            response = client.get("/api/v1/customers/my-items/999")
            
            assert response.status_code == 404


def test_get_my_item_wrong_customer(client, mock_customer):
    """Test getting item that doesn't belong to customer."""
    with patch('backend.crm_service.app.api.v1.endpoints.customers.get_current_customer') as mock_auth:
        mock_auth.return_value = mock_customer
        
        with patch('backend.crm_service.services.customer_service.CustomerService.get_customer_product_details') as mock_service:
            from fastapi import HTTPException
            mock_service.side_effect = HTTPException(status_code=403, detail="Product does not belong to this customer")
            
            response = client.get("/api/v1/customers/my-items/1")
            
            assert response.status_code == 403


def test_search_my_items_success(client, mock_customer, mock_inventory_response):
    """Test searching my items successfully."""
    with patch('backend.crm_service.app.api.v1.endpoints.customers.get_current_customer') as mock_auth:
        mock_auth.return_value = mock_customer
        
        with patch('backend.crm_service.services.customer_service.CustomerService.search_customer_products') as mock_service:
            mock_product = AsyncMock()
            mock_product.name = "Test Product"
            mock_product.sku = "TEST-001"
            mock_product.price = 99.99
            mock_service.return_value = [mock_product]
            
            response = client.get("/api/v1/customers/my-items/search/?name=Test&category=Electronics")
            
            assert response.status_code == 200
            data = response.json()
            assert "items" in data
            assert "total" in data
            assert "customer_id" in data
            assert len(data["items"]) == 1


def test_search_my_items_no_filters(client, mock_customer):
    """Test searching my items without filters."""
    with patch('backend.crm_service.app.api.v1.endpoints.customers.get_current_customer') as mock_auth:
        mock_auth.return_value = mock_customer
        
        with patch('backend.crm_service.services.customer_service.CustomerService.search_customer_products') as mock_service:
            mock_service.return_value = []
            
            response = client.get("/api/v1/customers/my-items/search/")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 0
            assert len(data["items"]) == 0


def test_search_my_items_service_error(client, mock_customer):
    """Test searching my items with service error."""
    with patch('backend.crm_service.app.api.v1.endpoints.customers.get_current_customer') as mock_auth:
        mock_auth.return_value = mock_customer
        
        with patch('backend.crm_service.services.customer_service.CustomerService.search_customer_products') as mock_service:
            from fastapi import HTTPException
            mock_service.side_effect = HTTPException(status_code=503, detail="Service unavailable")
            
            response = client.get("/api/v1/customers/my-items/search/")
            
            assert response.status_code == 503


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "crm-service"


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data