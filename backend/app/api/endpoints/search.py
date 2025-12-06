from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps.auth import require_active_user
from app.schemas.search import SearchRequest, SearchResponse, SearchResult
from app.services.search import get_search_service
from app.models.models import ActivityLog, User, SystemAdmin
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/", response_model=SearchResponse)
def search_documents(
    request: SearchRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Semantic search with filters"""
    if isinstance(current_user, SystemAdmin):
        raise HTTPException(
            status_code=400,
            detail="System admins must specify company_id"
        )
    
    company_id = current_user.company_id
    user_id = current_user.id
    
    search_service = get_search_service()
    result = search_service.search(
        query=request.query,
        company_id=company_id,
        user_id=user_id,
        db=db,
        top_k=request.top_k,
        file_type=request.file_type,
        date_from=request.date_from,
        date_to=request.date_to
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Search failed"))
    
    search_results = [
        SearchResult(
            document_id=r["document_id"],
            filename=r["filename"],
            chunk_text=r["chunk_text"],
            snippet=r["snippet"],
            chunk_index=r["chunk_index"],
            score=r["score"],
            file_type=r["file_type"],
            created_at=r["created_at"]
        )
        for r in result["results"]
    ]
    
    return SearchResponse(
        query=result["query"],
        results=search_results,
        total_results=result["total_results"],
        search_time_ms=result["search_time_ms"],
        filters_applied=result["filters_applied"]
    )

@router.get("/history")
def get_search_history(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get user's search history"""
    from app.models.models import ActivityLog, SearchHistory
    
    if isinstance(current_user, SystemAdmin):
        raise HTTPException(status_code=400, detail="Not available for system admins")
    
    history = db.query(SearchHistory).filter(
        SearchHistory.user_id == current_user.id
    ).order_by(SearchHistory.timestamp.desc()).limit(limit).all()
    
    return {
        "total": len(history),
        "history": [
            {
                "id": h.id,
                "query": h.query_text,
                "results_count": h.results_meta.get("total_results", 0) if h.results_meta else 0,
                "timestamp": h.timestamp
            }
            for h in history
        ]
    }

@router.get("/filters")
def get_available_filters(
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get available filter options for current company"""
    from app.models.models import ActivityLog, Document
    from sqlalchemy import func
    
    if isinstance(current_user, SystemAdmin):
        raise HTTPException(status_code=400, detail="Not available for system admins")
    
    company_id = current_user.company_id
    
    # Get unique file types
    docs = db.query(Document).filter(Document.company_id == company_id).all()
    
    file_types = set()
    for doc in docs:
        if '.' in doc.filename:
            ext = doc.filename.rsplit('.', 1)[1].lower()
            file_types.add(ext)
    
    return {
        "file_types": sorted(list(file_types)),
        "total_documents": len(docs)
    }