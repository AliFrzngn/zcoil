"""Test configuration and fixtures."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from shared.database import Base, get_db
from main import app
from models.product import Product


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""
    return {
        "name": "Test Product",
        "description": "A test product",
        "sku": "TEST-001",
        "price": 99.99,
        "cost": 50.00,
        "quantity": 100,
        "min_quantity": 10,
        "max_quantity": 1000,
        "is_active": True,
        "category": "Electronics",
        "brand": "TestBrand",
        "weight": 1.5,
        "dimensions": "10x20x30",
        "customer_id": "customer-123"
    }


@pytest.fixture
def sample_product(db_session, sample_product_data):
    """Create a sample product in the database."""
    product = Product(**sample_product_data)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product