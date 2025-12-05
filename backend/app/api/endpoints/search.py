from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps.auth import require_active_user
from app.schemas.search import SearchRequest, SearchResponse, SearchResult
from app.services.search import get_search_service
from app.models.models import User, SystemAdmin
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/", response_model=SearchResponse)
def search_documents(
    request: SearchRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Semantic search across company documents"""
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
        top_k=request.top_k
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Search failed"))
    
    search_results = [
        SearchResult(
            document_id=r["document_id"],
            filename=r["filename"],
            chunk_text=r["chunk_text"],
            chunk_index=r["chunk_index"],
            score=r["score"]
        )
        for r in result["results"]
    ]
    
    return SearchResponse(
        query=result["query"],
        results=search_results,
        total_results=result["total_results"],
        search_time_ms=result["search_time_ms"]
    )

@router.get("/history")
def get_search_history(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get user's search history"""
    from app.models.models import SearchHistory
    
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
