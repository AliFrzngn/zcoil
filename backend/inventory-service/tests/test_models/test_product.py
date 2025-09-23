"""Test product model."""

import pytest
from models.product import Product


def test_product_creation():
    """Test product model creation."""
    product = Product(
        name="Test Product",
        sku="TEST-001",
        price=99.99,
        quantity=100,
        is_active=True
    )
    
    assert product.name == "Test Product"
    assert product.sku == "TEST-001"
    assert product.price == 99.99
    assert product.quantity == 100
    assert product.is_active is True


def test_product_to_dict():
    """Test product to_dict method."""
    product = Product(
        name="Test Product",
        sku="TEST-001",
        price=99.99,
        quantity=100,
        customer_id="customer-123"
    )
    
    product_dict = product.to_dict()
    
    assert product_dict["name"] == "Test Product"
    assert product_dict["sku"] == "TEST-001"
    assert product_dict["price"] == 99.99
    assert product_dict["quantity"] == 100
    assert product_dict["customer_id"] == "customer-123"
    assert "id" in product_dict
    assert "created_at" in product_dict


def test_product_repr():
    """Test product string representation."""
    product = Product(
        id=1,
        name="Test Product",
        sku="TEST-001"
    )
    
    repr_str = repr(product)
    assert "Product" in repr_str
    assert "id=1" in repr_str
    assert "name='Test Product'" in repr_str
    assert "sku='TEST-001'" in repr_str