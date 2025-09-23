"""User service business logic."""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from fastapi import HTTPException, status
from passlib.context import CryptContext

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate, UserFilter

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """User service for business logic."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password."""
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
        
        # Apply filters
        if filters.email:
            query = query.filter(User.email.ilike(f"%{filters.email}%"))
        
        if filters.username:
            query = query.filter(User.username.ilike(f"%{filters.username}%"))
        
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
        from datetime import datetime
        user.email_verified_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user