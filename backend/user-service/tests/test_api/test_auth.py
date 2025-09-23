"""Test authentication API endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_register_user_success(client, mock_user_data):
    """Test successful user registration."""
    response = client.post("/api/v1/auth/register", json=mock_user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data
    assert data["email"] == mock_user_data["email"]
    assert data["username"] == mock_user_data["username"]
    assert "password" not in data  # Password should not be returned


def test_register_user_duplicate_email(client, mock_user_data):
    """Test registration with duplicate email."""
    # Create first user
    client.post("/api/v1/auth/register", json=mock_user_data)
    
    # Try to create second user with same email
    response = client.post("/api/v1/auth/register", json=mock_user_data)
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_login_success(client, mock_user_data, mock_jwt_token):
    """Test successful user login."""
    # Register user first
    client.post("/api/v1/auth/register", json=mock_user_data)
    
    # Login
    login_data = {
        "username": mock_user_data["username"],
        "password": mock_user_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


def test_get_current_user(client, mock_auth_headers, mock_current_user):
    """Test getting current user info."""
    response = client.get("/api/v1/auth/me", headers=mock_auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == mock_current_user["user_id"]
    assert data["email"] == mock_current_user["email"]


def test_get_current_user_unauthorized(client):
    """Test getting current user without authentication."""
    response = client.get("/api/v1/auth/me")
    
    assert response.status_code == 401


def test_refresh_token(client, mock_auth_headers, mock_jwt_token):
    """Test token refresh."""
    response = client.post("/api/v1/auth/refresh", headers=mock_auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_logout(client, mock_auth_headers):
    """Test user logout."""
    response = client.post("/api/v1/auth/logout", headers=mock_auth_headers)
    
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "user-service"
