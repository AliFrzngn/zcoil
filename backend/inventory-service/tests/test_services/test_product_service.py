"""Test product service."""

import pytest
from fastapi import HTTPException
from backend.inventory_service.services.product_service import ProductService
from backend.inventory_service.schemas.product import ProductCreate, ProductUpdate


def test_create_product(db_session, sample_product_data):
    """Test creating a product."""
    service = ProductService(db_session)
    product_data = ProductCreate(**sample_product_data)
    
    product = service.create_product(product_data)
    
    assert product.name == sample_product_data["name"]
    assert product.sku == sample_product_data["sku"]
    assert product.price == sample_product_data["price"]
    assert product.quantity == sample_product_data["quantity"]


def test_create_product_duplicate_sku(db_session, sample_product_data):
    """Test creating a product with duplicate SKU."""
    service = ProductService(db_session)
    product_data = ProductCreate(**sample_product_data)
    
    # Create first product
    service.create_product(product_data)
    
    # Try to create second product with same SKU
    with pytest.raises(HTTPException) as exc_info:
        service.create_product(product_data)
    
    assert exc_info.value.status_code == 400
    assert "already exists" in str(exc_info.value.detail)


def test_get_product(db_session, sample_product):
    """Test getting a product by ID."""
    service = ProductService(db_session)
    
    product = service.get_product(sample_product.id)
    
    assert product.id == sample_product.id
    assert product.name == sample_product.name


def test_get_product_not_found(db_session):
    """Test getting a non-existent product."""
    service = ProductService(db_session)
    
    with pytest.raises(HTTPException) as exc_info:
        service.get_product(999)
    
    assert exc_info.value.status_code == 404
    assert "not found" in str(exc_info.value.detail)


def test_update_product(db_session, sample_product):
    """Test updating a product."""
    service = ProductService(db_session)
    update_data = ProductUpdate(name="Updated Product", price=199.99)
    
    updated_product = service.update_product(sample_product.id, update_data)
    
    assert updated_product.name == "Updated Product"
    assert updated_product.price == 199.99
    assert updated_product.sku == sample_product.sku  # Unchanged


def test_update_product_duplicate_sku(db_session, sample_product):
    """Test updating a product with duplicate SKU."""
    service = ProductService(db_session)
    
    # Create another product
    another_product = service.create_product(ProductCreate(
        name="Another Product",
        sku="ANOTHER-001",
        price=50.00
    ))
    
    # Try to update first product with second product's SKU
    update_data = ProductUpdate(sku="ANOTHER-001")
    
    with pytest.raises(HTTPException) as exc_info:
        service.update_product(sample_product.id, update_data)
    
    assert exc_info.value.status_code == 400
    assert "already exists" in str(exc_info.value.detail)


def test_delete_product(db_session, sample_product):
    """Test deleting a product."""
    service = ProductService(db_session)
    
    result = service.delete_product(sample_product.id)
    
    assert result is True
    
    # Verify product is deleted
    with pytest.raises(HTTPException):
        service.get_product(sample_product.id)


def test_get_products_by_customer(db_session, sample_product):
    """Test getting products by customer ID."""
    service = ProductService(db_session)
    
    # Create another product for different customer
    service.create_product(ProductCreate(
        name="Other Product",
        sku="OTHER-001",
        price=50.00,
        customer_id="customer-456"
    ))
    
    customer_products = service.get_products_by_customer("customer-123")
    
    assert len(customer_products) == 1
    assert customer_products[0].customer_id == "customer-123"


def test_update_quantity(db_session, sample_product):
    """Test updating product quantity."""
    service = ProductService(db_session)
    
    # Add 50 items
    updated_product = service.update_quantity(sample_product.id, 50)
    assert updated_product.quantity == 150  # 100 + 50
    
    # Remove 25 items
    updated_product = service.update_quantity(sample_product.id, -25)
    assert updated_product.quantity == 125  # 150 - 25


def test_update_quantity_insufficient_stock(db_session, sample_product):
    """Test updating quantity with insufficient stock."""
    service = ProductService(db_session)
    
    with pytest.raises(HTTPException) as exc_info:
        service.update_quantity(sample_product.id, -200)  # Try to remove more than available
    
    assert exc_info.value.status_code == 400
    assert "Insufficient quantity" in str(exc_info.value.detail)


def test_get_low_stock_products(db_session):
    """Test getting low stock products."""
    service = ProductService(db_session)
    
    # Create products with different stock levels
    service.create_product(ProductCreate(
        name="Low Stock Product",
        sku="LOW-001",
        price=10.00,
        quantity=5,
        min_quantity=10
    ))
    
    service.create_product(ProductCreate(
        name="Normal Stock Product",
        sku="NORMAL-001",
        price=10.00,
        quantity=50,
        min_quantity=10
    ))
    
    low_stock_products = service.get_low_stock_products()
    
    assert len(low_stock_products) == 1
    assert low_stock_products[0].sku == "LOW-001"
