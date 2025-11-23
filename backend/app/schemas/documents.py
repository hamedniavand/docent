from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentUpload(BaseModel):
    company_id: int
    filename: str
    mime_type: str
    file_size: int

class DocumentResponse(BaseModel):
    id: int
    filename: str
    mime_type: str
    storage_path: str
    status: str
    summary: Optional[str]
    uploaded_by: int
    uploader_name: str
    company_id: int
    created_at: datetime
    processed_at: Optional[datetime]
    file_size: Optional[int] = None
    
    class Config:
        from_attributes = True

class DocumentListResponse(BaseModel):
    total: int
    documents: list[DocumentResponse]
    page: int
    page_size: int

class DocumentStats(BaseModel):
    total_documents: int
    total_size_mb: float
    by_type: dict
    recent_uploads: int