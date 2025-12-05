from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    # Filters
    file_type: Optional[str] = None  # pdf, docx, txt, etc.
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    
class SearchResult(BaseModel):
    document_id: int
    filename: str
    chunk_text: str
    snippet: str  # NEW: relevant portion
    chunk_index: int
    score: float
    file_type: str  # NEW
    created_at: Optional[datetime] = None  # NEW
    
class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_results: int
    search_time_ms: float
    filters_applied: dict  # NEW: show active filters