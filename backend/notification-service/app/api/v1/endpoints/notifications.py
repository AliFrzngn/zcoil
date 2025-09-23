"""Notification API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.shared.database import get_db
from backend.shared.auth import get_current_user
from ...schemas.notification import (
    NotificationCreate, 
    NotificationUpdate, 
    NotificationResponse, 
    NotificationListResponse,
    NotificationFilters
)
from ...services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new notification."""
    # Only admins can create notifications for other users
    if notification_data.user_id != current_user["user_id"] and current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    notification_service = NotificationService(db)
    notification = notification_service.create_notification(notification_data)
    
    return notification


@router.get("/", response_model=NotificationListResponse)
async def get_notifications(
    user_id: int = Query(None, description="Filter by user ID (admin only)"),
    type: str = Query(None, description="Filter by notification type"),
    is_read: bool = Query(None, description="Filter by read status"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get notifications."""
    filters = NotificationFilters(
        user_id=user_id,
        type=type,
        is_read=is_read,
        page=page,
        size=size
    )
    
    notification_service = NotificationService(db)
    
    # If user is admin/manager, they can see all notifications
    if current_user["role"] in ["admin", "manager"] and user_id is None:
        notifications, total = notification_service.get_all_notifications(filters)
    else:
        # Regular users can only see their own notifications
        filters.user_id = current_user["user_id"]
        notifications, total = notification_service.get_user_notifications(
            current_user["user_id"], 
            filters
        )
    
    pages = (total + size - 1) // size
    
    return NotificationListResponse(
        items=notifications,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific notification."""
    notification_service = NotificationService(db)
    notification = notification_service.get_notification(notification_id)
    
    # Check if user can access this notification
    if notification.user_id != current_user["user_id"] and current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return notification


@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: int,
    update_data: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update a notification."""
    notification_service = NotificationService(db)
    notification = notification_service.get_notification(notification_id)
    
    # Check if user can update this notification
    if notification.user_id != current_user["user_id"] and current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    notification = notification_service.update_notification(notification_id, update_data)
    
    return notification


@router.post("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Mark a notification as read."""
    notification_service = NotificationService(db)
    notification = notification_service.get_notification(notification_id)
    
    # Check if user can read this notification
    if notification.user_id != current_user["user_id"] and current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    notification = notification_service.mark_as_read(notification_id)
    
    return notification


@router.post("/read-all", response_model=dict)
async def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Mark all notifications as read for the current user."""
    notification_service = NotificationService(db)
    updated_count = notification_service.mark_all_as_read(current_user["user_id"])
    
    return {"message": f"Marked {updated_count} notifications as read"}


@router.get("/unread/count", response_model=dict)
async def get_unread_count(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get count of unread notifications for the current user."""
    notification_service = NotificationService(db)
    count = notification_service.get_unread_count(current_user["user_id"])
    
    return {"unread_count": count}


@router.delete("/{notification_id}", response_model=dict)
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a notification."""
    notification_service = NotificationService(db)
    notification = notification_service.get_notification(notification_id)
    
    # Check if user can delete this notification
    if notification.user_id != current_user["user_id"] and current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    notification_service.delete_notification(notification_id)
    
    return {"message": "Notification deleted successfully"}
