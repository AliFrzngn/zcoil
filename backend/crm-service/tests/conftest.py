"""Test configuration and fixtures for CRM service."""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from backend.crm_service.main import app


@pytest.fixture(scope="function")
def client():
    """Create a test client."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_customer():
    """Mock customer data."""
    return {
        "user_id": "customer-123",
        "email": "customer@example.com",
        "role": "customer",
        "permissions": []
    }


@pytest.fixture
def mock_inventory_response():
    """Mock inventory service response."""
    return {
        "items": [
            {
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
        ]
    }


@pytest.fixture
def mock_product_details():
    """Mock product details response."""
    return {
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
        "customer_id": "customer-123",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": None
    }
