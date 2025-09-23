"""Authentication API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.shared.database import get_db
from schemas.user import UserLogin, UserRegister, Token, UserResponse, PasswordResetRequest, PasswordReset
from services.auth_service import AuthService
from services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["authentication"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Get auth service instance."""
    return AuthService(db)


def get_current_user_dependency(auth_service: AuthService = Depends(get_auth_service)) -> dict:
    """Get current user dependency."""
    return auth_service.get_current_user()


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
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get current user information."""
    # Get user details from database
    db = next(get_db())
    user_service = UserService(db)
    user = user_service.get_user(int(current_user["user_id"]))
    return user


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
    current_user: dict = Depends(get_current_user_dependency)
):
    """Refresh access token."""
    db = next(get_db())
    auth_service = AuthService(db)
    access_token = auth_service.create_access_token_for_user(current_user)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=30 * 60  # 30 minutes
    )


@router.post("/send-verification-email")
async def send_verification_email(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Send email verification email to user."""
    user_service = UserService(db)
    success = user_service.send_verification_email(user_id)
    
    if success:
        return {"message": "Verification email sent successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email"
        )


@router.post("/verify-email")
async def verify_email(
    verification_token: str,
    db: Session = Depends(get_db)
):
    """Verify email with verification token."""
    user_service = UserService(db)
    user = user_service.verify_email_with_token(verification_token)
    
    return {
        "message": "Email verified successfully",
        "user": user
    }


@router.post("/request-password-reset")
async def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Request password reset."""
    user_service = UserService(db)
    success = user_service.request_password_reset(request.email)
    
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/reset-password")
async def reset_password(
    request: PasswordReset,
    db: Session = Depends(get_db)
):
    """Reset password with reset token."""
    user_service = UserService(db)
    user = user_service.reset_password_with_token(request.token, request.new_password)
    
    return {
        "message": "Password reset successfully",
        "user": user
    }