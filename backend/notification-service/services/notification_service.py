"""Notification service business logic."""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from fastapi import HTTPException, status
from datetime import datetime

from models.notification import Notification
from schemas.notification import NotificationCreate, NotificationUpdate, NotificationFilters


class NotificationService:
    """Notification service for business logic."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_notification(self, notification_data: NotificationCreate) -> Notification:
        """Create a new notification."""
        notification = Notification(
            user_id=notification_data.user_id,
            title=notification_data.title,
            message=notification_data.message,
            type=notification_data.type
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        return notification
    
    def get_notification(self, notification_id: int) -> Notification:
        """Get a notification by ID."""
        notification = self.db.query(Notification).filter(
            Notification.id == notification_id
        ).first()
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        
        return notification
    
    def get_user_notifications(
        self, 
        user_id: int, 
        filters: NotificationFilters
    ) -> Tuple[List[Notification], int]:
        """Get notifications for a user with filtering."""
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        
        # Apply filters
        if filters.type:
            query = query.filter(Notification.type == filters.type)
        if filters.is_read is not None:
            query = query.filter(Notification.is_read == filters.is_read)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        notifications = query.order_by(
            Notification.created_at.desc()
        ).offset((filters.page - 1) * filters.size).limit(filters.size).all()
        
        return notifications, total
    
    def get_all_notifications(
        self, 
        filters: NotificationFilters
    ) -> Tuple[List[Notification], int]:
        """Get all notifications with filtering (admin only)."""
        query = self.db.query(Notification)
        
        # Apply filters
        if filters.user_id:
            query = query.filter(Notification.user_id == filters.user_id)
        if filters.type:
            query = query.filter(Notification.type == filters.type)
        if filters.is_read is not None:
            query = query.filter(Notification.is_read == filters.is_read)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        notifications = query.order_by(
            Notification.created_at.desc()
        ).offset((filters.page - 1) * filters.size).limit(filters.size).all()
        
        return notifications, total
    
    def update_notification(
        self, 
        notification_id: int, 
        update_data: NotificationUpdate
    ) -> Notification:
        """Update a notification."""
        notification = self.get_notification(notification_id)
        
        for field, value in update_data.dict(exclude_unset=True):
            setattr(notification, field, value)
        
        if update_data.is_read and not notification.is_read:
            notification.read_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(notification)
        
        return notification
    
    def mark_as_read(self, notification_id: int) -> Notification:
        """Mark a notification as read."""
        return self.update_notification(notification_id, NotificationUpdate(is_read=True))
    
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications as read for a user."""
        updated_count = self.db.query(Notification).filter(
            and_(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
        ).update({
            Notification.is_read: True,
            Notification.read_at: datetime.utcnow()
        })
        
        self.db.commit()
        return updated_count
    
    def delete_notification(self, notification_id: int) -> bool:
        """Delete a notification."""
        notification = self.get_notification(notification_id)
        
        self.db.delete(notification)
        self.db.commit()
        
        return True
    
    def get_unread_count(self, user_id: int) -> int:
        """Get count of unread notifications for a user."""
        return self.db.query(Notification).filter(
            and_(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
        ).count()
    
    def create_system_notification(
        self, 
        title: str, 
        message: str, 
        notification_type: str = "info"
    ) -> Notification:
        """Create a system-wide notification (for all users)."""
        # This would typically create notifications for all users
        # For now, we'll create a single system notification
        notification = Notification(
            user_id=0,  # System user ID
            title=title,
            message=message,
            type=notification_type
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        return notification
