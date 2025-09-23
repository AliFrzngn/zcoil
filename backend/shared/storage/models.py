"""File storage models."""

from sqlalchemy import Column, String, Text, DateTime, Integer, BigInteger
from sqlalchemy.sql import func
from backend.shared.database import Base


class FileUpload(Base):
    """File upload model for tracking uploaded files."""
    
    __tablename__ = "file_uploads"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    content_type = Column(String(100), nullable=False)
    user_id = Column(String(100), nullable=True, index=True)
    resource_type = Column(String(100), nullable=True, index=True)
    resource_id = Column(String(100), nullable=True, index=True)
    is_public = Column(String(10), default="false", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<FileUpload(id={self.id}, filename='{self.filename}', user_id='{self.user_id}')>"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "filename": self.filename,
            "original_filename": self.original_filename,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "content_type": self.content_type,
            "user_id": self.user_id,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "is_public": self.is_public,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }