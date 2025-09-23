"""Test configuration and fixtures for User service."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from main import app


@pytest.fixture(scope="function")
def client():
    """Create a test client."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_user_data():
    """Mock user data for testing."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpassword123",
        "role": "user",
        "is_active": True
    }


@pytest.fixture
def mock_admin_data():
    """Mock admin user data for testing."""
    return {
        "email": "admin@example.com",
        "username": "admin",
        "full_name": "Admin User",
        "password": "adminpassword123",
        "role": "admin",
        "is_active": True
    }


@pytest.fixture
def mock_jwt_token():
    """Mock JWT token for testing."""
    return {
        "access_token": "mock.jwt.token",
        "token_type": "bearer"
    }


@pytest.fixture
def mock_current_user():
    """Mock current user for testing."""
    return {
        "user_id": "user-123",
        "email": "test@example.com",
        "username": "testuser",
        "role": "user",
        "permissions": ["read:profile", "update:profile"]
    }


@pytest.fixture
def mock_auth_headers():
    """Mock authentication headers for testing."""
    return {"Authorization": "Bearer mock.jwt.token"}
