"""Audit service for logging user actions."""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from .models import AuditLog

logger = logging.getLogger(__name__)


class AuditService:
    """Service for logging audit events."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def log_action(
        self,
        action: str,
        resource_type: str,
        user_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """Log an audit action."""
        try:
            audit_log = AuditLog(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details,
                metadata=metadata,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            self.db.add(audit_log)
            self.db.commit()
            self.db.refresh(audit_log)
            
            logger.info(f"Audit log created: {action} on {resource_type} by user {user_id}")
            return audit_log
            
        except Exception as e:
            logger.error(f"Failed to create audit log: {str(e)}")
            self.db.rollback()
            raise
    
    def log_user_login(self, user_id: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> AuditLog:
        """Log user login action."""
        return self.log_action(
            action="login",
            resource_type="user",
            user_id=user_id,
            details="User logged in",
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def log_user_logout(self, user_id: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> AuditLog:
        """Log user logout action."""
        return self.log_action(
            action="logout",
            resource_type="user",
            user_id=user_id,
            details="User logged out",
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def log_user_registration(self, user_id: str, email: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> AuditLog:
        """Log user registration action."""
        return self.log_action(
            action="register",
            resource_type="user",
            user_id=user_id,
            details=f"User registered with email: {email}",
            metadata={"email": email},
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def log_user_update(self, user_id: str, updated_fields: list, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> AuditLog:
        """Log user update action."""
        return self.log_action(
            action="update",
            resource_type="user",
            user_id=user_id,
            details=f"User updated fields: {', '.join(updated_fields)}",
            metadata={"updated_fields": updated_fields},
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def log_password_reset_request(self, user_id: str, email: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> AuditLog:
        """Log password reset request action."""
        return self.log_action(
            action="password_reset_request",
            resource_type="user",
            user_id=user_id,
            details=f"Password reset requested for email: {email}",
            metadata={"email": email},
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def log_password_reset_complete(self, user_id: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> AuditLog:
        """Log password reset completion action."""
        return self.log_action(
            action="password_reset_complete",
            resource_type="user",
            user_id=user_id,
            details="Password reset completed",
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def log_email_verification(self, user_id: str, email: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> AuditLog:
        """Log email verification action."""
        return self.log_action(
            action="email_verification",
            resource_type="user",
            user_id=user_id,
            details=f"Email verified: {email}",
            metadata={"email": email},
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def log_product_create(self, user_id: str, product_id: str, product_name: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> AuditLog:
        """Log product creation action."""
        return self.log_action(
            action="create",
            resource_type="product",
            user_id=user_id,
            resource_id=product_id,
            details=f"Product created: {product_name}",
            metadata={"product_name": product_name},
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def log_product_update(self, user_id: str, product_id: str, product_name: str, updated_fields: list, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> AuditLog:
        """Log product update action."""
        return self.log_action(
            action="update",
            resource_type="product",
            user_id=user_id,
            resource_id=product_id,
            details=f"Product updated: {product_name}",
            metadata={"product_name": product_name, "updated_fields": updated_fields},
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def log_product_delete(self, user_id: str, product_id: str, product_name: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> AuditLog:
        """Log product deletion action."""
        return self.log_action(
            action="delete",
            resource_type="product",
            user_id=user_id,
            resource_id=product_id,
            details=f"Product deleted: {product_name}",
            metadata={"product_name": product_name},
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def get_audit_logs(
        self,
        user_id: Optional[str] = None,
        action: Optional[str] = None,
        resource_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[AuditLog]:
        """Get audit logs with filtering."""
        query = self.db.query(AuditLog)
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if action:
            query = query.filter(AuditLog.action == action)
        if resource_type:
            query = query.filter(AuditLog.resource_type == resource_type)
        
        return query.order_by(AuditLog.created_at.desc()).offset(offset).limit(limit).all()
