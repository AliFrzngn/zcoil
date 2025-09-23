"""User schemas for validation and serialization."""

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from datetime import datetime
import re


class UserBase(BaseModel):
    """Base user schema."""
    
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=100, description="Username")
    full_name: Optional[str] = Field(None, max_length=255, description="Full name")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    bio: Optional[str] = Field(None, description="User bio")
    role: str = Field(default="customer", description="User role")
    
    @validator('full_name')
    def validate_full_name(cls, v):
        """Validate full name format."""
        if v is not None:
            v = v.strip()
            if len(v) > 255:
                raise ValueError('Full name must be less than 255 characters')
            # Check for dangerous characters
            if re.search(r'[<>"\']', v):
                raise ValueError('Full name contains invalid characters')
        return v
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format."""
        if v is not None:
            v = v.strip()
            # Remove all non-digit characters for validation
            digits_only = re.sub(r'\D', '', v)
            if len(digits_only) < 10 or len(digits_only) > 15:
                raise ValueError('Phone number must be between 10 and 15 digits')
            # Check for common patterns
            if not re.match(r'^[\+]?[1-9][\d]{0,15}$', digits_only):
                raise ValueError('Invalid phone number format')
        return v
    
    @validator('bio')
    def validate_bio(cls, v):
        """Validate bio content."""
        if v is not None:
            v = v.strip()
            if len(v) > 1000:
                raise ValueError('Bio must be less than 1000 characters')
            # Check for dangerous content
            if re.search(r'<script|javascript:|vbscript:', v, re.IGNORECASE):
                raise ValueError('Bio contains potentially dangerous content')
        return v
    
    @validator('role')
    def validate_role(cls, v):
        """Validate user role."""
        allowed_roles = {'admin', 'manager', 'customer'}
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        """Validate username format with enhanced security."""
        if not v or len(v.strip()) == 0:
            raise ValueError('Username cannot be empty')
        
        v = v.strip()
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if len(v) > 50:
            raise ValueError('Username must be less than 50 characters')
        
        # Check for dangerous characters
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, hyphens, and underscores')
        
        # Check for reserved usernames
        reserved_usernames = {'admin', 'root', 'administrator', 'api', 'www', 'mail', 'ftp', 'support', 'help'}
        if v.lower() in reserved_usernames:
            raise ValueError('This username is reserved and cannot be used')
        
        return v.lower()


class UserCreate(UserBase):
    """Schema for creating a user."""
    
    password: str = Field(..., min_length=8, description="Password")
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength with enhanced security."""
        if not v or len(v.strip()) == 0:
            raise ValueError('Password cannot be empty')
        
        v = v.strip()
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if len(v) > 128:
            raise ValueError('Password must be less than 128 characters')
        
        # Check for common weak passwords
        common_passwords = {'password', '123456', '123456789', 'qwerty', 'abc123', 'password123', 'admin', 'letmein'}
        if v.lower() in common_passwords:
            raise ValueError('This password is too common and not secure')
        
        # Check for password strength
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        
        # Check for sequential characters
        if any(v[i:i+3] in 'abcdefghijklmnopqrstuvwxyz' or v[i:i+3] in '0123456789' for i in range(len(v)-2)):
            raise ValueError('Password cannot contain sequential characters')
        
        return v


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response."""
    
    id: int
    is_active: bool
    is_verified: bool
    is_superuser: bool
    avatar_url: Optional[str] = None
    last_login: Optional[datetime] = None
    email_verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""
    
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password")


class UserRegister(UserCreate):
    """Schema for user registration."""
    
    confirm_password: str = Field(..., description="Confirm password")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Validate password confirmation."""
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


class Token(BaseModel):
    """Schema for authentication token."""
    
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Schema for token data."""
    
    sub: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    permissions: Optional[List[str]] = None


class UserFilter(BaseModel):
    """Schema for filtering users."""
    
    email: Optional[str] = None
    username: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)


class UserListResponse(BaseModel):
    """Schema for paginated user list response."""
    
    items: List[UserResponse]
    total: int
    page: int
    size: int
    pages: int


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    
    email: EmailStr = Field(..., description="Email address to reset password for")


class PasswordReset(BaseModel):
    """Schema for password reset."""
    
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password")
    
    @validator('new_password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v