from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    
class SearchResult(BaseModel):
    document_id: int
    filename: str
    chunk_text: str
    chunk_index: int
    score: float
    
class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_results: int
    search_time_ms: float
