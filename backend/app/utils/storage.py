import os
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional
import shutil

class FileStorage:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save_file(self, file_content: bytes, filename: str, company_id: int) -> dict:
        """
        Save uploaded file to storage
        Returns: dict with storage_path and file_size
        """
        # Create company directory
        company_dir = self.base_path / f"company_{company_id}"
        company_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_ext = Path(filename).suffix
        unique_filename = f"{timestamp}_{uuid.uuid4().hex[:8]}{file_ext}"
        
        # Full path
        file_path = company_dir / unique_filename
        
        # Write file
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Return relative path from base
        relative_path = str(file_path.relative_to(self.base_path))
        
        return {
            "storage_path": relative_path,
            "file_size": file_size,
            "full_path": str(file_path)
        }
    
    def get_file_path(self, storage_path: str) -> Path:
        """Get full file path from storage path"""
        return self.base_path / storage_path
    
    def delete_file(self, storage_path: str) -> bool:
        """Delete file from storage"""
        try:
            file_path = self.get_file_path(storage_path)
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def get_file_size(self, storage_path: str) -> Optional[int]:
        """Get file size in bytes"""
        try:
            file_path = self.get_file_path(storage_path)
            if file_path.exists():
                return os.path.getsize(file_path)
            return None
        except Exception:
            return None

def get_file_storage(base_path: str = "/opt/docent/data/storage") -> FileStorage:
    """Get file storage instance"""
    return FileStorage(base_path)

def validate_file_type(filename: str, allowed_types: list = None) -> tuple[bool, str]:
    """
    Validate file type
    Returns: (is_valid, mime_type)
    """
    if allowed_types is None:
        allowed_types = ['.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls', '.txt']
    
    file_ext = Path(filename).suffix.lower()
    
    if file_ext not in allowed_types:
        return False, ""
    
    # Map extensions to MIME types
    mime_types = {
        '.pdf': 'application/pdf',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.doc': 'application/msword',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.ppt': 'application/vnd.ms-powerpoint',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.xls': 'application/vnd.ms-excel',
        '.txt': 'text/plain'
    }
    
    return True, mime_types.get(file_ext, 'application/octet-stream')

def format_file_size(size_bytes: int) -> str:
    """Format file size to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"