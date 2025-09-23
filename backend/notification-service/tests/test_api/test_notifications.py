"""Test notification API endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_send_notification_success(client, mock_notification_data):
    """Test sending notification successfully."""
    response = client.post("/api/v1/notifications/", json=mock_notification_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == mock_notification_data["title"]
    assert data["message"] == mock_notification_data["message"]
    assert data["user_id"] == mock_notification_data["user_id"]


def test_send_email_notification(client, mock_email_notification):
    """Test sending email notification."""
    response = client.post("/api/v1/notifications/email", json=mock_email_notification)
    
    assert response.status_code == 201
    data = response.json()
    assert data["channel"] == "email"
    assert data["recipient_email"] == mock_email_notification["recipient_email"]


def test_send_sms_notification(client, mock_sms_notification):
    """Test sending SMS notification."""
    response = client.post("/api/v1/notifications/sms", json=mock_sms_notification)
    
    assert response.status_code == 201
    data = response.json()
    assert data["channel"] == "sms"
    assert data["recipient_phone"] == mock_sms_notification["recipient_phone"]


def test_send_push_notification(client, mock_push_notification):
    """Test sending push notification."""
    response = client.post("/api/v1/notifications/push", json=mock_push_notification)
    
    assert response.status_code == 201
    data = response.json()
    assert data["channel"] == "push"
    assert data["device_token"] == mock_push_notification["device_token"]


def test_get_user_notifications(client, mock_notification_data):
    """Test getting notifications for a user."""
    # Send a notification first
    client.post("/api/v1/notifications/", json=mock_notification_data)
    
    # Get user notifications
    response = client.get(f"/api/v1/notifications/user/{mock_notification_data['user_id']}")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["user_id"] == mock_notification_data["user_id"]


def test_get_notification_by_id(client, mock_notification_data):
    """Test getting notification by ID."""
    # Send a notification first
    create_response = client.post("/api/v1/notifications/", json=mock_notification_data)
    notification_id = create_response.json()["id"]
    
    # Get the notification
    response = client.get(f"/api/v1/notifications/{notification_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == notification_id
    assert data["title"] == mock_notification_data["title"]


def test_mark_notification_as_read(client, mock_notification_data):
    """Test marking notification as read."""
    # Send a notification first
    create_response = client.post("/api/v1/notifications/", json=mock_notification_data)
    notification_id = create_response.json()["id"]
    
    # Mark as read
    response = client.patch(f"/api/v1/notifications/{notification_id}/read")
    
    assert response.status_code == 200
    data = response.json()
    assert data["is_read"] is True


def test_delete_notification(client, mock_notification_data):
    """Test deleting notification."""
    # Send a notification first
    create_response = client.post("/api/v1/notifications/", json=mock_notification_data)
    notification_id = create_response.json()["id"]
    
    # Delete the notification
    response = client.delete(f"/api/v1/notifications/{notification_id}")
    
    assert response.status_code == 204
    
    # Verify it's deleted
    response = client.get(f"/api/v1/notifications/{notification_id}")
    assert response.status_code == 404


def test_get_unread_notifications(client, mock_notification_data):
    """Test getting unread notifications for a user."""
    # Send a notification first
    client.post("/api/v1/notifications/", json=mock_notification_data)
    
    # Get unread notifications
    response = client.get(f"/api/v1/notifications/user/{mock_notification_data['user_id']}/unread")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(not notification["is_read"] for notification in data)


def test_bulk_mark_as_read(client, mock_notification_data):
    """Test bulk marking notifications as read."""
    # Send multiple notifications
    for i in range(3):
        notification_data = mock_notification_data.copy()
        notification_data["title"] = f"Test Notification {i}"
        client.post("/api/v1/notifications/", json=notification_data)
    
    # Bulk mark as read
    response = client.patch(
        f"/api/v1/notifications/user/{mock_notification_data['user_id']}/mark-all-read"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "All notifications marked as read"


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "notification-service"
