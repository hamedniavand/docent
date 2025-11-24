from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Document
from app.api.deps.auth import require_active_user
from app.services.document_processor import get_document_processor
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/processing", tags=["Document Processing"])

@router.post("/process/{document_id}")
async def process_document(
    document_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Process a document: extract text, chunk, embed, store
    """
    # Check document exists
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check access
    if document.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check if already processed
    if document.status == "processed":
        return {"message": "Document already processed", "document_id": document_id}
    
    # Add to background tasks (non-blocking)
    processor = get_document_processor()
    
    # Process in background
    def process_task():
        # Create new DB session for background task
        from app.core.database import SessionLocal
        db_task = SessionLocal()
        try:
            result = processor.process_document(document_id, db_task)
            logger.info(f"Background processing result: {result}")
        finally:
            db_task.close()
    
    background_tasks.add_task(process_task)
    
    return {
        "message": "Processing started",
        "document_id": document_id,
        "status": "processing"
    }

@router.get("/status/{document_id}")
def get_processing_status(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Get processing status of a document
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check access
    if document.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get chunk count
    from app.models.models import DocumentChunk
    chunk_count = db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document_id
    ).count()
    
    return {
        "document_id": document_id,
        "filename": document.filename,
        "status": document.status,
        "chunks_created": chunk_count,
        "summary": document.summary,
        "processed_at": document.processed_at
    }

@router.post("/process-all")
async def process_all_documents(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Process all uploaded (but not processed) documents
    """
    # Get all uploaded documents for this company
    documents = db.query(Document).filter(
        Document.company_id == current_user.company_id,
        Document.status == "uploaded"
    ).all()
    
    if not documents:
        return {"message": "No documents to process"}
    
    processor = get_document_processor()
    
    # Process each in background
    for doc in documents:
        def process_task(doc_id=doc.id):
            from app.core.database import SessionLocal
            db_task = SessionLocal()
            try:
                processor.process_document(doc_id, db_task)
            finally:
                db_task.close()
        
        background_tasks.add_task(process_task)
    
    return {
        "message": f"Processing {len(documents)} documents",
        "document_ids": [d.id for d in documents]
    }
    