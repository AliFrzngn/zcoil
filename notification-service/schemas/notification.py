"""Notification schemas."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NotificationBase(BaseModel):
    """Base notification schema."""
    
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    type: str = Field(default="info", regex="^(info|success|warning|error)$")


class NotificationCreate(NotificationBase):
    """Schema for creating a notification."""
    
    user_id: int = Field(..., gt=0)


class NotificationUpdate(BaseModel):
    """Schema for updating a notification."""
    
    is_read: Optional[bool] = None


class NotificationResponse(NotificationBase):
    """Schema for notification response."""
    
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    """Schema for notification list response."""
    
    items: list[NotificationResponse]
    total: int
    page: int
    size: int
    pages: int


class NotificationFilters(BaseModel):
    """Schema for notification filters."""
    
    user_id: Optional[int] = None
    type: Optional[str] = None
    is_read: Optional[bool] = None
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)