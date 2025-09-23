"""File service for handling file uploads and storage."""

import os
import uuid
import hashlib
from typing import Optional, Dict, Any, BinaryIO
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
import aiofiles
import mimetypes
from pathlib import Path

from .models import FileUpload
from ..config import settings

# File upload configuration
UPLOAD_DIR = getattr(settings, 'UPLOAD_DIR', '/app/uploads')
MAX_FILE_SIZE = getattr(settings, 'MAX_FILE_SIZE', 10 * 1024 * 1024)  # 10MB
ALLOWED_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.rtf'],
    'spreadsheet': ['.xls', '.xlsx', '.csv'],
    'archive': ['.zip', '.rar', '.7z', '.tar', '.gz']
}

ALLOWED_MIME_TYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'image/webp',
    'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain', 'application/rtf',
    'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/csv', 'application/zip', 'application/x-rar-compressed', 'application/x-7z-compressed',
    'application/x-tar', 'application/gzip'
}


class FileService:
    """Service for handling file uploads and storage."""
    
    def __init__(self, db: Session):
        self.db = db
        self.upload_dir = Path(UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def _generate_filename(self, original_filename: str) -> str:
        """Generate a unique filename."""
        file_ext = Path(original_filename).suffix
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{file_ext}"
    
    def _get_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of a file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _validate_file_content(self, content: bytes, content_type: str) -> None:
        """Validate file content for malicious patterns."""
        # Check for common malicious file signatures
        malicious_signatures = [
            b'<script', b'javascript:', b'vbscript:', b'onload=',
            b'<?php', b'<?=', b'<iframe', b'<object', b'<embed',
            b'exec(', b'eval(', b'system(', b'shell_exec('
        ]
        
        content_lower = content.lower()
        for signature in malicious_signatures:
            if signature in content_lower:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="File contains potentially malicious content"
                )
        
        # Additional validation for specific file types
        if content_type.startswith('image/'):
            # Basic image file validation
            if not content.startswith((b'\xff\xd8\xff', b'\x89PNG', b'GIF8')):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid image file format"
                )
    
    def _validate_file(self, file: UploadFile) -> None:
        """Validate uploaded file with enhanced security checks."""
        # Check file size
        if hasattr(file, 'size') and file.size and file.size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE} bytes"
            )
        
        # Validate filename to prevent path traversal
        if not file.filename or '..' in file.filename or '/' in file.filename or '\\' in file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filename"
            )
        
        # Check content type
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file.content_type} is not allowed"
            )
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if not any(file_ext in extensions for extensions in ALLOWED_EXTENSIONS.values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File extension {file_ext} is not allowed"
            )
        
        # Additional security: Check for executable files
        dangerous_extensions = {'.exe', '.bat', '.cmd', '.scr', '.pif', '.com', '.vbs', '.js', '.jar', '.sh'}
        if file_ext in dangerous_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Executable files are not allowed"
            )
    
    async def upload_file(
        self,
        file: UploadFile,
        user_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        is_public: bool = False
    ) -> FileUpload:
        """Upload a file and save metadata to database."""
        try:
            # Validate file
            self._validate_file(file)
            
            # Generate unique filename
            filename = self._generate_filename(file.filename)
            
            # Create subdirectory based on file type
            file_type = file.content_type.split('/')[0]
            subdir = self.upload_dir / file_type
            subdir.mkdir(exist_ok=True)
            
            file_path = subdir / filename
            
            # Save file to disk with content validation
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                
                # Validate file content for malicious patterns
                self._validate_file_content(content, file.content_type)
                
                await f.write(content)
            
            # Get file size
            file_size = len(content)
            
            # Create database record
            file_upload = FileUpload(
                filename=filename,
                original_filename=file.filename,
                file_path=str(file_path),
                file_size=file_size,
                content_type=file.content_type,
                user_id=user_id,
                resource_type=resource_type,
                resource_id=resource_id,
                is_public="true" if is_public else "false"
            )
            
            self.db.add(file_upload)
            self.db.commit()
            self.db.refresh(file_upload)
            
            return file_upload
            
        except Exception as e:
            # Clean up file if database operation fails
            if 'file_path' in locals() and file_path.exists():
                file_path.unlink()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload file: {str(e)}"
            )
    
    def get_file(self, file_id: int) -> FileUpload:
        """Get file metadata by ID."""
        file_upload = self.db.query(FileUpload).filter(FileUpload.id == file_id).first()
        if not file_upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        return file_upload
    
    def get_file_path(self, file_id: int) -> str:
        """Get file path by ID."""
        file_upload = self.get_file(file_id)
        file_path = Path(file_upload.file_path)
        
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found on disk"
            )
        
        return str(file_path)
    
    def delete_file(self, file_id: int) -> bool:
        """Delete file and its metadata."""
        file_upload = self.get_file(file_id)
        file_path = Path(file_upload.file_path)
        
        # Delete file from disk
        if file_path.exists():
            file_path.unlink()
        
        # Delete database record
        self.db.delete(file_upload)
        self.db.commit()
        
        return True
    
    def get_user_files(
        self,
        user_id: str,
        resource_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[FileUpload]:
        """Get files uploaded by a user."""
        query = self.db.query(FileUpload).filter(FileUpload.user_id == user_id)
        
        if resource_type:
            query = query.filter(FileUpload.resource_type == resource_type)
        
        return query.order_by(FileUpload.created_at.desc()).offset(offset).limit(limit).all()
    
    def get_public_files(
        self,
        resource_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[FileUpload]:
        """Get public files."""
        query = self.db.query(FileUpload).filter(FileUpload.is_public == "true")
        
        if resource_type:
            query = query.filter(FileUpload.resource_type == resource_type)
        
        return query.order_by(FileUpload.created_at.desc()).offset(offset).limit(limit).all()
    
    def get_file_url(self, file_id: int, base_url: str = "http://localhost:80") -> str:
        """Get public URL for a file."""
        file_upload = self.get_file(file_id)
        
        if file_upload.is_public != "true":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="File is not public"
            )
        
        return f"{base_url}/files/{file_id}"