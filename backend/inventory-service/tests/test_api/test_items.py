"""Test items API endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_create_item(client, sample_product_data):
    """Test creating an item via API."""
    response = client.post("/api/v1/items/", json=sample_product_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_product_data["name"]
    assert data["sku"] == sample_product_data["sku"]
    assert data["price"] == sample_product_data["price"]


def test_create_item_duplicate_sku(client, sample_product_data):
    """Test creating an item with duplicate SKU."""
    # Create first item
    client.post("/api/v1/items/", json=sample_product_data)
    
    # Try to create second item with same SKU
    response = client.post("/api/v1/items/", json=sample_product_data)
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_get_item(client, sample_product):
    """Test getting an item by ID."""
    response = client.get(f"/api/v1/items/{sample_product.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_product.id
    assert data["name"] == sample_product.name


def test_get_item_not_found(client):
    """Test getting a non-existent item."""
    response = client.get("/api/v1/items/999")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_get_items(client, sample_product):
    """Test getting items with pagination."""
    response = client.get("/api/v1/items/")
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert len(data["items"]) == 1


def test_get_items_with_filters(client, sample_product):
    """Test getting items with filters."""
    # Filter by name
    response = client.get("/api/v1/items/?name=Test")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    
    # Filter by category
    response = client.get("/api/v1/items/?category=Electronics")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    
    # Filter by non-existent category
    response = client.get("/api/v1/items/?category=NonExistent")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0


def test_update_item(client, sample_product):
    """Test updating an item."""
    update_data = {"name": "Updated Product", "price": 199.99}
    response = client.put(f"/api/v1/items/{sample_product.id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price"] == 199.99


def test_delete_item(client, sample_product):
    """Test deleting an item."""
    response = client.delete(f"/api/v1/items/{sample_product.id}")
    
    assert response.status_code == 204
    
    # Verify item is deleted
    response = client.get(f"/api/v1/items/{sample_product.id}")
    assert response.status_code == 404


def test_get_customer_items(client, sample_product):
    """Test getting items for a customer."""
    response = client.get(f"/api/v1/items/customer/{sample_product.customer_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["customer_id"] == sample_product.customer_id


def test_update_quantity(client, sample_product):
    """Test updating item quantity."""
    response = client.patch(f"/api/v1/items/{sample_product.id}/quantity?quantity_change=50")
    
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 150  # 100 + 50


def test_get_low_stock_items(client):
    """Test getting low stock items."""
    response = client.get("/api/v1/items/low-stock/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "inventory-service"