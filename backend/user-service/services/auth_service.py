"""Authentication service."""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.shared.database import get_db
from backend.shared.config import settings
from backend.shared.auth import create_access_token, verify_token
from .user_service import UserService

# Security scheme
security = HTTPBearer()


class AuthService:
    """Authentication service."""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return user data."""
        user = self.user_service.authenticate_user(email, password)
        if not user:
            return None
        
        # Update last login
        self.user_service.update_last_login(user.id)
        
        return {
            "user_id": str(user.id),
            "email": user.email,
            "username": user.username,
            "role": user.role,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "permissions": self._get_user_permissions(user)
        }
    
    def create_access_token_for_user(self, user_data: Dict[str, Any]) -> str:
        """Create access token for user."""
        token_data = {
            "sub": user_data["user_id"],
            "email": user_data["email"],
            "role": user_data["role"],
            "permissions": user_data["permissions"]
        }
        
        expires_delta = timedelta(minutes=settings.jwt_access_token_expire_minutes)
        return create_access_token(token_data, expires_delta)
    
    def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
        """Get current user from JWT token."""
        token = credentials.credentials
        payload = verify_token(token)
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database to ensure they still exist and are active
        try:
            user = self.user_service.get_user(int(user_id))
            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User account is disabled"
                )
            
            return {
                "user_id": str(user.id),
                "email": user.email,
                "username": user.username,
                "role": user.role,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "permissions": self._get_user_permissions(user)
            }
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID in token"
            )
    
    def get_current_active_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
        """Get current active user."""
        user = self.get_current_user(credentials)
        if not user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return user
    
    def get_current_verified_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
        """Get current verified user."""
        user = self.get_current_active_user(credentials)
        if not user["is_verified"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not verified"
            )
        return user
    
    def _get_user_permissions(self, user) -> list:
        """Get user permissions based on role."""
        permissions = []
        
        if user.role == "admin":
            permissions = [
                "users:read", "users:write", "users:delete",
                "inventory:read", "inventory:write", "inventory:delete",
                "crm:read", "crm:write", "crm:delete",
                "notifications:read", "notifications:write"
            ]
        elif user.role == "manager":
            permissions = [
                "users:read", "users:write",
                "inventory:read", "inventory:write",
                "crm:read", "crm:write",
                "notifications:read", "notifications:write"
            ]
        elif user.role == "customer":
            permissions = [
                "inventory:read",
                "crm:read"
            ]
        
        return permissions