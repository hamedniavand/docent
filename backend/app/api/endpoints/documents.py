from app.models.models import SystemAdmin
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional, List
from app.core.database import get_db
from app.core.config import settings
from app.models.models import Document, User, ActivityLog
from app.schemas.documents import DocumentResponse, DocumentListResponse, DocumentStats
from app.api.deps.auth import require_active_user
from app.utils.storage import get_file_storage, validate_file_type, format_file_size
from datetime import datetime
from app.services.document_processor import get_document_processor
from typing import Optional, List 

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Upload a single document
    """
    # Validate file type
    is_valid, mime_type = validate_file_type(file.filename)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed: PDF, DOCX, PPTX, XLSX, TXT"
        )
    
    # Read file content
    file_content = await file.read()
    file_size = len(file_content)
    
    # Check file size (50MB limit)
    max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE_MB}MB"
        )
    
    # Save file to storage
    storage = get_file_storage(settings.STORAGE_PATH)
    storage_info = storage.save_file(file_content, file.filename, current_user.company_id)
    
    # Create document record
    document = Document(
        company_id=current_user.company_id,
        uploaded_by=current_user.id,
        filename=file.filename,
        mime_type=mime_type,
        storage_path=storage_info["storage_path"],
        status="uploaded",
        created_at=datetime.utcnow()
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Get uploader name
    uploader = db.query(User).filter(User.id == document.uploaded_by).first()
    uploader_name = uploader.name if uploader else "Unknown"
    
    # Log activity
    activity = ActivityLog(
        user_id=current_user.id,
        company_id=current_user.company_id,
        action="Document Uploaded",
        details={"filename": document.filename, "document_id": document.id, "size": storage_info["file_size"]}
    )
    db.add(activity)
    db.commit()
    
    # Auto-process document in background
    def process_task(doc_id=document.id):
        from app.core.database import SessionLocal
        db_task = SessionLocal()
        try:
            processor = get_document_processor()
            processor.process_document(doc_id, db_task)
        finally:
            db_task.close()
    
    background_tasks.add_task(process_task)
    
    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        mime_type=document.mime_type,
        storage_path=document.storage_path,
        status=document.status,
        summary=document.summary,
        uploaded_by=document.uploaded_by,
        uploader_name=uploader_name,
        company_id=document.company_id,
        created_at=document.created_at,
        processed_at=document.processed_at,
        file_size=storage_info["file_size"]
    )

@router.post("/upload-multiple", response_model=List[DocumentResponse])
async def upload_multiple_documents(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Upload multiple documents at once
    """
    uploaded_docs = []
    storage = get_file_storage(settings.STORAGE_PATH)
    
    for file in files:
        try:
            # Validate file type
            is_valid, mime_type = validate_file_type(file.filename)
            if not is_valid:
                continue  # Skip invalid files
            
            # Read file
            file_content = await file.read()
            file_size = len(file_content)
            
            # Check size
            max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
            if file_size > max_size:
                continue  # Skip large files
            
            # Save file
            storage_info = storage.save_file(file_content, file.filename, current_user.company_id)
            
            # Create record
            document = Document(
                company_id=current_user.company_id,
                uploaded_by=current_user.id,
                filename=file.filename,
                mime_type=mime_type,
                storage_path=storage_info["storage_path"],
                status="uploaded",
                created_at=datetime.utcnow()
            )
            
            db.add(document)
            db.commit()
            db.refresh(document)
            
            # Get uploader name
            uploader = db.query(User).filter(User.id == document.uploaded_by).first()
            uploader_name = uploader.name if uploader else "Unknown"
            
            uploaded_docs.append(DocumentResponse(
                id=document.id,
                filename=document.filename,
                mime_type=document.mime_type,
                storage_path=document.storage_path,
                status=document.status,
                summary=document.summary,
                uploaded_by=document.uploaded_by,
                uploader_name=uploader_name,
                company_id=document.company_id,
                created_at=document.created_at,
                processed_at=document.processed_at,
                file_size=storage_info["file_size"]
            ))
            
        except Exception as e:
            print(f"Error uploading {file.filename}: {e}")
            continue
    
    return uploaded_docs

@router.get("/", response_model=DocumentListResponse)
def list_documents(
    company_id: Optional[int] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    List documents with pagination and search
    """
    query = db.query(Document)
    
    # Filter by company
    if company_id:
        query = query.filter(Document.company_id == company_id)
    else:
        query = query.filter(Document.company_id == current_user.company_id)
    
    # Search by filename
    if search:
        query = query.filter(Document.filename.ilike(f"%{search}%"))
    
    # Get total
    total = query.count()
    
    # Paginate
    documents = query.order_by(Document.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    # Get storage instance
    storage = get_file_storage(settings.STORAGE_PATH)
    
    # Build response with uploader names and file sizes
    doc_responses = []
    for doc in documents:
        uploader = db.query(User).filter(User.id == doc.uploaded_by).first()
        uploader_name = uploader.name if uploader else "Unknown"
        
        # Get file size
        file_size = storage.get_file_size(doc.storage_path)
        
        doc_responses.append(DocumentResponse(
            id=doc.id,
            filename=doc.filename,
            mime_type=doc.mime_type,
            storage_path=doc.storage_path,
            status=doc.status,
            summary=doc.summary,
            uploaded_by=doc.uploaded_by,
            uploader_name=uploader_name,
            company_id=doc.company_id,
            created_at=doc.created_at,
            processed_at=doc.processed_at,
            file_size=file_size
        ))
    
    return DocumentListResponse(
        total=total,
        documents=doc_responses,
        page=page,
        page_size=page_size
    )

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Get document details
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check access
    if document.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Get uploader name
    uploader = db.query(User).filter(User.id == document.uploaded_by).first()
    uploader_name = uploader.name if uploader else "Unknown"
    
    # Get file size
    storage = get_file_storage(settings.STORAGE_PATH)
    file_size = storage.get_file_size(document.storage_path)
    
    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        mime_type=document.mime_type,
        storage_path=document.storage_path,
        status=document.status,
        summary=document.summary,
        uploaded_by=document.uploaded_by,
        uploader_name=uploader_name,
        company_id=document.company_id,
        created_at=document.created_at,
        processed_at=document.processed_at,
        file_size=file_size
    )

@router.get("/{document_id}/download")
def download_document(
    document_id: int,
    token: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Download document file
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check access
    if document.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Get file path
    storage = get_file_storage(settings.STORAGE_PATH)
    file_path = storage.get_file_path(document.storage_path)
    
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found in storage"
        )
    
    return FileResponse(
        path=str(file_path),
        filename=document.filename,
        media_type=document.mime_type
    )

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Delete document
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check access
    if document.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Delete file from storage
    storage = get_file_storage(settings.STORAGE_PATH)
    storage.delete_file(document.storage_path)
    
    # Delete database record
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}
    
@router.get("/stats/company")
def get_document_stats(
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Get document statistics for company
    """
    # Handle SystemAdmin vs User
    from app.models.models import SystemAdmin
    if isinstance(current_user, SystemAdmin):
        # System admin - could see all companies or return error
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System admins must specify a company_id parameter"
        )
    
    company_id = current_user.company_id
    
    # Total documents
    total = db.query(Document).filter(Document.company_id == company_id).count()
    
    # Calculate total size
    documents = db.query(Document).filter(Document.company_id == company_id).all()
    storage = get_file_storage(settings.STORAGE_PATH)
    
    total_size = 0
    by_type = {}
    
    for doc in documents:
        file_size = storage.get_file_size(doc.storage_path) or 0
        total_size += file_size
        
        # Count by type
        ext = doc.filename.split('.')[-1].upper() if '.' in doc.filename else 'OTHER'
        by_type[ext] = by_type.get(ext, 0) + 1
    
    # Recent uploads (last 7 days)
    from datetime import timedelta
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent = db.query(Document).filter(
        Document.company_id == company_id,
        Document.created_at >= seven_days_ago
    ).count()
    
    return DocumentStats(
        total_documents=total,
        total_size_mb=round(total_size / (1024 * 1024), 2),
        by_type=by_type,
        recent_uploads=recent
    )