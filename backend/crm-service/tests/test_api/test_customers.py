"""Test customer API endpoints."""

import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient


def test_get_my_items_success(client, mock_customer, mock_inventory_response):
    """Test getting my items successfully."""
    with patch('services.customer_service.CustomerService.get_customer_products') as mock_service:
        from schemas.customer import CustomerProductResponse
        from datetime import datetime
        
        mock_product = CustomerProductResponse(
            id=1,
            name="Test Product",
            description="A test product",
            sku="TEST-001",
            price=99.99,
            quantity=100,
            category="Electronics",
            brand="TestBrand",
            weight=1.5,
            dimensions="10x20x30",
            is_active=True,
            created_at=datetime.now(),
            updated_at=None
        )
        mock_service.return_value = [mock_product]
        
        response = client.get("/api/v1/customers/my-items")
        
        if response.status_code != 200:
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "customer_id" in data
        assert data["customer_id"] == "customer-123"


def test_get_my_items_unauthorized(client):
    """Test getting my items without authentication."""
        with patch('shared.auth.get_current_customer') as mock_auth:
        from fastapi import HTTPException
        mock_auth.side_effect = HTTPException(status_code=401, detail="Unauthorized")
        
        response = client.get("/api/v1/customers/my-items")
        
        assert response.status_code == 401


def test_get_my_item_success(client, mock_customer, mock_product_details):
    """Test getting specific item successfully."""
        with patch('shared.utils.HTTPClient') as mock_http_client:
        from schemas.customer import CustomerProductResponse
        from datetime import datetime
        
        # Mock the HTTP client response
        mock_response = {
            "id": 1,
            "name": "Test Product",
            "description": "A test product",
            "sku": "TEST-001",
            "price": 99.99,
            "quantity": 100,
            "category": "Electronics",
            "brand": "TestBrand",
            "weight": 1.5,
            "dimensions": "10x20x30",
            "is_active": True,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": None
        }
        
        mock_client_instance = mock_http_client.return_value
        mock_client_instance.get.return_value = mock_response
        
        response = client.get("/api/v1/customers/my-items/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Product"
        assert data["sku"] == "TEST-001"


def test_get_my_item_not_found(client, mock_customer):
    """Test getting non-existent item."""
        with patch('shared.auth.get_current_customer') as mock_auth:
        mock_auth.return_value = mock_customer
        
        with patch('services.customer_service.CustomerService.get_customer_product_details') as mock_service:
            from fastapi import HTTPException
            mock_service.side_effect = HTTPException(status_code=404, detail="Product not found")
            
            response = client.get("/api/v1/customers/my-items/999")
            
            assert response.status_code == 404


def test_get_my_item_wrong_customer(client, mock_customer):
    """Test getting item that doesn't belong to customer."""
        with patch('shared.auth.get_current_customer') as mock_auth:
        mock_auth.return_value = mock_customer
        
        with patch('services.customer_service.CustomerService.get_customer_product_details') as mock_service:
            from fastapi import HTTPException
            mock_service.side_effect = HTTPException(status_code=403, detail="Product does not belong to this customer")
            
            response = client.get("/api/v1/customers/my-items/1")
            
            assert response.status_code == 403


def test_search_my_items_success(client, mock_customer, mock_inventory_response):
    """Test searching my items successfully."""
    with patch('services.customer_service.CustomerService.search_customer_products') as mock_service:                                                                                                   
        from schemas.customer import CustomerProductResponse
        from datetime import datetime
        
        mock_product = CustomerProductResponse(
            id=1,
            name="Test Product",
            description="A test product",
            sku="TEST-001",
            price=99.99,
            quantity=100,
            category="Electronics",
            brand="TestBrand",
            weight=1.5,
            dimensions="10x20x30",
            is_active=True,
            created_at=datetime.now(),
            updated_at=None
        )
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
        with patch('shared.auth.get_current_customer') as mock_auth:
        mock_auth.return_value = mock_customer
        
        with patch('services.customer_service.CustomerService.search_customer_products') as mock_service:
            mock_service.return_value = []
            
            response = client.get("/api/v1/customers/my-items/search/")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total"] == 0
            assert len(data["items"]) == 0


def test_search_my_items_service_error(client, mock_customer):
    """Test searching my items with service error."""
        with patch('shared.auth.get_current_customer') as mock_auth:
        mock_auth.return_value = mock_customer
        
        with patch('services.customer_service.CustomerService.search_customer_products') as mock_service:
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