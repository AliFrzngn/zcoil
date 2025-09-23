"""Test configuration and fixtures for CRM service."""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from main import app


@pytest.fixture(scope="function")
def client():
    """Create a test client."""
    from shared.auth import get_current_customer
    
    def mock_get_current_customer():
        return {
            "user_id": "customer-123",
            "email": "customer@example.com",
            "role": "customer",
            "permissions": []
        }
    
    app.dependency_overrides[get_current_customer] = mock_get_current_customer
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


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