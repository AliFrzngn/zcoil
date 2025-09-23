"""Authentication API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.shared.database import get_db
from ...schemas.user import UserLogin, UserRegister, Token, UserResponse
from ...services.auth_service import AuthService
from ...services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    user_service = UserService(db)
    user = user_service.create_user(user_data)
    return user


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """Login user and return access token."""
    auth_service = AuthService(db)
    
    user_data = auth_service.authenticate_user(login_data.email, login_data.password)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token_for_user(user_data)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=30 * 60  # 30 minutes
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Get current user information."""
    # This will be handled by the dependency injection
    pass


@router.post("/verify-email/{user_id}")
async def verify_email(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Verify user email."""
    user_service = UserService(db)
    user = user_service.verify_email(user_id)
    return {"message": "Email verified successfully"}


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Refresh access token."""
    auth_service = AuthService(get_db())
    access_token = auth_service.create_access_token_for_user(current_user)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=30 * 60  # 30 minutes
    )