"""File upload API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session

from backend.shared.database import get_db
from backend.shared.storage import FileService
from services.auth_service import AuthService

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    resource_type: str = Query(None, description="Resource type (e.g., 'product', 'user')"),
    resource_id: str = Query(None, description="Resource ID"),
    is_public: bool = Query(False, description="Make file public"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Upload a file."""
    file_service = FileService(db)
    
    file_upload = await file_service.upload_file(
        file=file,
        user_id=current_user["user_id"],
        resource_type=resource_type,
        resource_id=resource_id,
        is_public=is_public
    )
    
    return {
        "message": "File uploaded successfully",
        "file": file_upload.to_dict()
    }


@router.get("/{file_id}")
async def get_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Get file metadata."""
    file_service = FileService(db)
    file_upload = file_service.get_file(file_id)
    
    # Check if user has access to the file
    if file_upload.user_id != current_user["user_id"] and file_upload.is_public != "true":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return file_upload.to_dict()


@router.get("/{file_id}/download")
async def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Download a file."""
    file_service = FileService(db)
    file_upload = file_service.get_file(file_id)
    
    # Check if user has access to the file
    if file_upload.user_id != current_user["user_id"] and file_upload.is_public != "true":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    file_path = file_service.get_file_path(file_id)
    
    from fastapi.responses import FileResponse
    return FileResponse(
        path=file_path,
        filename=file_upload.original_filename,
        media_type=file_upload.content_type
    )


@router.get("/{file_id}/url")
async def get_file_url(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Get public URL for a file."""
    file_service = FileService(db)
    file_url = file_service.get_file_url(file_id)
    
    return {"url": file_url}


@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Delete a file."""
    file_service = FileService(db)
    file_upload = file_service.get_file(file_id)
    
    # Check if user owns the file
    if file_upload.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    success = file_service.delete_file(file_id)
    
    return {"message": "File deleted successfully"}


@router.get("/")
async def get_user_files(
    resource_type: str = Query(None, description="Filter by resource type"),
    limit: int = Query(100, ge=1, le=1000, description="Number of files to return"),
    offset: int = Query(0, ge=0, description="Number of files to skip"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(AuthService(get_db()).get_current_user)
):
    """Get files uploaded by the current user."""
    file_service = FileService(db)
    files = file_service.get_user_files(
        user_id=current_user["user_id"],
        resource_type=resource_type,
        limit=limit,
        offset=offset
    )
    
    return {
        "files": [file.to_dict() for file in files],
        "total": len(files)
    }


@router.get("/public/")
async def get_public_files(
    resource_type: str = Query(None, description="Filter by resource type"),
    limit: int = Query(100, ge=1, le=1000, description="Number of files to return"),
    offset: int = Query(0, ge=0, description="Number of files to skip"),
    db: Session = Depends(get_db)
):
    """Get public files."""
    file_service = FileService(db)
    files = file_service.get_public_files(
        resource_type=resource_type,
        limit=limit,
        offset=offset
    )
    
    return {
        "files": [file.to_dict() for file in files],
        "total": len(files)
    }