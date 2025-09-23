"""Users API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.shared.database import get_db
from ...schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
    UserFilter
)
from ...services.user_service import UserService
from ...services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Create a new user (admin only)."""
    # Check if current user has admin permissions
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user_service = UserService(db)
    return user_service.create_user(user_data)


@router.get("/", response_model=UserListResponse)
async def get_users(
    email: str = Query(None, description="Filter by email"),
    username: str = Query(None, description="Filter by username"),
    role: str = Query(None, description="Filter by role"),
    is_active: bool = Query(None, description="Filter by active status"),
    is_verified: bool = Query(None, description="Filter by verified status"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Get users with filtering and pagination (admin/manager only)."""
    # Check if current user has appropriate permissions
    if current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    filters = UserFilter(
        email=email,
        username=username,
        role=role,
        is_active=is_active,
        is_verified=is_verified,
        page=page,
        size=size
    )
    
    user_service = UserService(db)
    users, total = user_service.get_users(filters)
    
    pages = (total + size - 1) // size
    
    return UserListResponse(
        items=users,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Get user by ID."""
    user_service = UserService(db)
    
    # Users can only view their own profile unless they're admin/manager
    if current_user["role"] not in ["admin", "manager"] and str(user_id) != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return user_service.get_user(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Update user."""
    user_service = UserService(db)
    
    # Users can only update their own profile unless they're admin
    if current_user["role"] != "admin" and str(user_id) != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Non-admin users cannot change certain fields
    if current_user["role"] != "admin":
        restricted_fields = ["role", "is_active", "is_verified", "is_superuser"]
        for field in restricted_fields:
            if hasattr(user_data, field) and getattr(user_data, field) is not None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Cannot modify {field}"
                )
    
    return user_service.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Delete user (admin only)."""
    # Only admins can delete users
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Prevent self-deletion
    if str(user_id) == current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    user_service = UserService(db)
    user_service.delete_user(user_id)