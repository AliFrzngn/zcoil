"""Test configuration and fixtures for Notification service."""

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
def mock_notification_data():
    """Mock notification data for testing."""
    return {
        "user_id": "user-123",
        "title": "Test Notification",
        "message": "This is a test notification",
        "notification_type": "info",
        "priority": "medium",
        "channel": "email",
        "is_read": False
    }


@pytest.fixture
def mock_email_notification():
    """Mock email notification data."""
    return {
        "user_id": "user-123",
        "title": "Email Test",
        "message": "Test email notification",
        "notification_type": "email",
        "priority": "high",
        "channel": "email",
        "recipient_email": "test@example.com",
        "subject": "Test Email Subject"
    }


@pytest.fixture
def mock_sms_notification():
    """Mock SMS notification data."""
    return {
        "user_id": "user-123",
        "title": "SMS Test",
        "message": "Test SMS notification",
        "notification_type": "sms",
        "priority": "high",
        "channel": "sms",
        "recipient_phone": "+1234567890"
    }


@pytest.fixture
def mock_push_notification():
    """Mock push notification data."""
    return {
        "user_id": "user-123",
        "title": "Push Test",
        "message": "Test push notification",
        "notification_type": "push",
        "priority": "medium",
        "channel": "push",
        "device_token": "mock-device-token"
    }


@pytest.fixture
def mock_notification_service():
    """Mock notification service for testing."""
    with patch('services.notification_service.NotificationService') as mock_service:
        yield mock_service
