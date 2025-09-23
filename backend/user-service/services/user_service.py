"""User service business logic."""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
import secrets

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate, UserFilter
from backend.shared.email import EmailService
from backend.shared.audit import AuditService

# Password hashing context with stronger configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Increased from default 10
    bcrypt__min_rounds=10,
    bcrypt__max_rounds=15
)


class UserService:
    """User service for business logic."""
    
    def __init__(self, db: Session):
        self.db = db
        self.email_service = EmailService()
        self.audit_service = AuditService(db)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password with strong configuration."""
        # Additional validation for password strength
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(password) > 128:
            raise ValueError("Password must be less than 128 characters")
        
        return pwd_context.hash(password)
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        # Check if email already exists
        existing_user = self.db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username already exists
        existing_username = self.db.query(User).filter(User.username == user_data.username).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create new user
        hashed_password = self.get_password_hash(user_data.password)
        user_dict = user_data.dict(exclude={"password"})
        user_dict["hashed_password"] = hashed_password
        
        user = User(**user_dict)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user(self, user_id: int) -> User:
        """Get user by ID."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_users(self, filters: UserFilter) -> Tuple[List[User], int]:
        """Get users with filtering and pagination."""
        query = self.db.query(User)
        
        # Apply filters with proper parameterization
        if filters.email:
            # Sanitize email input to prevent SQL injection
            email_filter = filters.email.strip().replace('%', '\\%').replace('_', '\\_')
            query = query.filter(User.email.ilike(f"%{email_filter}%"))
        
        if filters.username:
            # Sanitize username input to prevent SQL injection
            username_filter = filters.username.strip().replace('%', '\\%').replace('_', '\\_')
            query = query.filter(User.username.ilike(f"%{username_filter}%"))
        
        if filters.role:
            query = query.filter(User.role == filters.role)
        
        if filters.is_active is not None:
            query = query.filter(User.is_active == filters.is_active)
        
        if filters.is_verified is not None:
            query = query.filter(User.is_verified == filters.is_verified)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (filters.page - 1) * filters.size
        users = query.offset(offset).limit(filters.size).all()
        
        return users, total
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """Update user."""
        user = self.get_user(user_id)
        
        # Check if email is being changed and if it already exists
        if user_data.email and user_data.email != user.email:
            existing_user = self.db.query(User).filter(
                and_(User.email == user_data.email, User.id != user_id)
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Check if username is being changed and if it already exists
        if user_data.username and user_data.username != user.username:
            existing_username = self.db.query(User).filter(
                and_(User.username == user_data.username, User.id != user_id)
            ).first()
            if existing_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Update fields
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        user = self.get_user(user_id)
        self.db.delete(user)
        self.db.commit()
        return True
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
    
    def update_last_login(self, user_id: int) -> User:
        """Update user's last login timestamp."""
        user = self.get_user(user_id)
        from datetime import datetime
        user.last_login = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def verify_email(self, user_id: int) -> User:
        """Mark user's email as verified."""
        user = self.get_user(user_id)
        user.is_verified = True
        user.email_verified_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        
        # Log audit event
        self.audit_service.log_email_verification(
            user_id=str(user_id),
            email=user.email
        )
        
        return user
    
    def send_verification_email(self, user_id: int) -> bool:
        """Send email verification email to user."""
        user = self.get_user(user_id)
        
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already verified"
            )
        
        # Generate verification token
        verification_token = secrets.token_urlsafe(32)
        
        # Store token in user metadata (in a real app, you'd use a separate table)
        # For now, we'll use a simple approach with proper escaping
        user.bio = f"verification_token:{verification_token}"
        self.db.commit()
        
        # Send verification email
        success = self.email_service.send_verification_email(
            to_email=user.email,
            verification_token=verification_token,
            user_name=user.full_name or user.username
        )
        
        return success
    
    def verify_email_with_token(self, verification_token: str) -> User:
        """Verify email using verification token."""
        # Find user with this verification token (properly escaped)
        escaped_token = verification_token.replace('%', '\\%').replace('_', '\\_')
        user = self.db.query(User).filter(
            User.bio.like(f"verification_token:{escaped_token}")
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification token"
            )
        
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already verified"
            )
        
        # Verify the email
        user.is_verified = True
        user.email_verified_at = datetime.utcnow()
        user.bio = None  # Clear the token
        self.db.commit()
        self.db.refresh(user)
        
        # Log audit event
        self.audit_service.log_email_verification(
            user_id=str(user.id),
            email=user.email
        )
        
        # Send welcome email
        self.email_service.send_welcome_email(
            to_email=user.email,
            user_name=user.full_name or user.username
        )
        
        return user
    
    def request_password_reset(self, email: str) -> bool:
        """Request password reset for user."""
        user = self.get_user_by_email(email)
        if not user:
            # Don't reveal if email exists or not
            return True
        
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        
        # Store token in user metadata (in a real app, you'd use a separate table)
        user.bio = f"reset_token:{reset_token}:{datetime.utcnow().isoformat()}"
        self.db.commit()
        
        # Send password reset email
        success = self.email_service.send_password_reset_email(
            to_email=user.email,
            reset_token=reset_token,
            user_name=user.full_name or user.username
        )
        
        # Log audit event
        self.audit_service.log_password_reset_request(
            user_id=str(user.id),
            email=user.email
        )
        
        return success
    
    def reset_password_with_token(self, reset_token: str, new_password: str) -> User:
        """Reset password using reset token."""
        # Find user with this reset token (properly escaped)
        escaped_token = reset_token.replace('%', '\\%').replace('_', '\\_')
        user = self.db.query(User).filter(
            User.bio.like(f"reset_token:{escaped_token}:%")
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token"
            )
        
        # Check if token is expired (1 hour)
        try:
            token_data = user.bio.split(":")
            token_time = datetime.fromisoformat(token_data[2])
            if datetime.utcnow() - token_time > timedelta(hours=1):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Reset token has expired"
                )
        except (IndexError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token format"
            )
        
        # Update password
        user.hashed_password = self.get_password_hash(new_password)
        user.bio = None  # Clear the token
        self.db.commit()
        self.db.refresh(user)
        
        # Log audit event
        self.audit_service.log_password_reset_complete(
            user_id=str(user.id)
        )
        
        return user