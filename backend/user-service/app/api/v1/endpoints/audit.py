"""Audit logging API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.shared.database import get_db
from backend.shared.audit import AuditService
from ...services.auth_service import AuthService

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/logs")
async def get_audit_logs(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    action: Optional[str] = Query(None, description="Filter by action"),
    resource_type: Optional[str] = Query(None, description="Filter by resource type"),
    limit: int = Query(100, ge=1, le=1000, description="Number of logs to return"),
    offset: int = Query(0, ge=0, description="Number of logs to skip"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Get audit logs."""
    # Only admins and managers can view audit logs
    if current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    audit_service = AuditService(db)
    logs = audit_service.get_audit_logs(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        limit=limit,
        offset=offset
    )
    
    return {
        "logs": [log.to_dict() for log in logs],
        "total": len(logs)
    }


@router.get("/logs/my")
async def get_my_audit_logs(
    action: Optional[str] = Query(None, description="Filter by action"),
    resource_type: Optional[str] = Query(None, description="Filter by resource type"),
    limit: int = Query(100, ge=1, le=1000, description="Number of logs to return"),
    offset: int = Query(0, ge=0, description="Number of logs to skip"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Get audit logs for the current user."""
    audit_service = AuditService(db)
    logs = audit_service.get_audit_logs(
        user_id=current_user["user_id"],
        action=action,
        resource_type=resource_type,
        limit=limit,
        offset=offset
    )
    
    return {
        "logs": [log.to_dict() for log in logs],
        "total": len(logs)
    }
