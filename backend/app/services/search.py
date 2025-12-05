import logging
import time
import re
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.services.embeddings import get_embedding_service
from app.services.vector_db import get_vector_db
from app.models.models import Document, DocumentChunk, SearchHistory

logger = logging.getLogger(__name__)

class SearchService:
    """Semantic search service with filters and smart snippets"""
    
    def __init__(self):
        self.embedding_service = get_embedding_service()
        self.vector_db = get_vector_db()
    
    def extract_snippet(self, text: str, query: str, max_length: int = 200) -> str:
        """Extract the most relevant snippet from text based on query"""
        if len(text) <= max_length:
            return text
        
        # Find query words in text
        query_words = [w.lower() for w in query.split() if len(w) > 2]
        text_lower = text.lower()
        
        # Find best starting position (where most query words appear nearby)
        best_pos = 0
        best_score = 0
        
        for i in range(0, len(text) - max_length, 50):
            window = text_lower[i:i + max_length]
            score = sum(1 for word in query_words if word in window)
            if score > best_score:
                best_score = score
                best_pos = i
        
        # Extract snippet
        snippet = text[best_pos:best_pos + max_length]
        
        # Clean up snippet boundaries
        if best_pos > 0:
            snippet = "..." + snippet.lstrip()
        if best_pos + max_length < len(text):
            # Try to end at a sentence or word boundary
            last_period = snippet.rfind('.')
            last_space = snippet.rfind(' ')
            if last_period > max_length * 0.7:
                snippet = snippet[:last_period + 1]
            elif last_space > max_length * 0.8:
                snippet = snippet[:last_space] + "..."
            else:
                snippet = snippet + "..."
        
        return snippet
    
    def get_file_type(self, filename: str) -> str:
        """Extract file type from filename"""
        if '.' in filename:
            return filename.rsplit('.', 1)[1].lower()
        return 'unknown'
    
    def search(
        self, 
        query: str, 
        company_id: int, 
        user_id: int,
        db: Session,
        top_k: int = 5,
        file_type: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> Dict:
        """
        Perform semantic search with filters
        """
        start_time = time.time()
        filters_applied = {}
        
        try:
            # 1. Generate query embedding
            logger.info(f"Generating embedding for query: {query[:50]}...")
            query_embedding = self.embedding_service.generate_query_embedding(query)
            
            if query_embedding is None:
                return {
                    "success": False,
                    "error": "Failed to generate query embedding",
                    "results": [],
                    "search_time_ms": 0,
                    "filters_applied": {}
                }
            
            # 2. Search vector database with company filter
            logger.info(f"Searching vector DB for company {company_id}")
            
            # Get more results than needed to allow for filtering
            vector_results = self.vector_db.search(
                query_embedding=query_embedding,
                n_results=top_k * 3,  # Get extra for filtering
                where={"company_id": company_id}
            )
            
            # 3. Process results
            results = []
            
            if vector_results and vector_results.get('ids') and vector_results['ids'][0]:
                ids = vector_results['ids'][0]
                documents = vector_results.get('documents', [[]])[0]
                metadatas = vector_results.get('metadatas', [[]])[0]
                distances = vector_results.get('distances', [[]])[0]
                
                for i, chunk_id in enumerate(ids):
                    metadata = metadatas[i] if i < len(metadatas) else {}
                    doc_id = metadata.get('document_id')
                    
                    if doc_id:
                        doc = db.query(Document).filter(Document.id == doc_id).first()
                        if not doc:
                            continue
                        filename = doc.filename
                        created_at = doc.created_at
                        doc_file_type = self.get_file_type(filename)
                        
                        # Apply file type filter
                        if file_type and doc_file_type != file_type.lower():
                            continue
                        
                        # Apply date filters
                        if date_from and created_at < date_from:
                            continue
                        if date_to and created_at > date_to:
                            continue
                    else:
                        filename = metadata.get('filename', 'Unknown')
                        created_at = None
                        doc_file_type = self.get_file_type(filename)
                    
                    distance = distances[i] if i < len(distances) else 1.0
                    score = max(0, 1 - distance)
                    
                    chunk_text = documents[i] if i < len(documents) else ""
                    snippet = self.extract_snippet(chunk_text, query)
                    
                    results.append({
                        "document_id": doc_id,
                        "filename": filename,
                        "chunk_text": chunk_text,
                        "snippet": snippet,
                        "chunk_index": metadata.get('chunk_index', 0),
                        "score": round(score, 4),
                        "file_type": doc_file_type,
                        "created_at": created_at
                    })
            
            # Deduplicate
            seen = set()
            unique_results = []
            for r in results:
                key = f"{r['document_id']}-{r['chunk_index']}"
                if key not in seen:
                    seen.add(key)
                    unique_results.append(r)
            
            results = unique_results
            results.sort(key=lambda x: x['score'], reverse=True)
            results = results[:top_k]  # Limit to requested amount
            
            search_time_ms = round((time.time() - start_time) * 1000, 2)
            
            # Track filters applied
            if file_type:
                filters_applied['file_type'] = file_type
            if date_from:
                filters_applied['date_from'] = date_from.isoformat()
            if date_to:
                filters_applied['date_to'] = date_to.isoformat()
            
            # Log search history
            try:
                search_record = SearchHistory(
                    user_id=user_id,
                    company_id=company_id,
                    query_text=query,
                    results_meta={
                        "total_results": len(results),
                        "top_score": results[0]['score'] if results else 0,
                        "search_time_ms": search_time_ms,
                        "filters": filters_applied
                    }
                )
                db.add(search_record)
                db.commit()
            except Exception as e:
                logger.error(f"Failed to log search history: {e}")
            
            logger.info(f"Search completed: {len(results)} results in {search_time_ms}ms")
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "total_results": len(results),
                "search_time_ms": search_time_ms,
                "filters_applied": filters_applied
            }
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": [],
                "search_time_ms": round((time.time() - start_time) * 1000, 2),
                "filters_applied": {}
            }

_search_service = None

def get_search_service() -> SearchService:
    global _search_service
    if _search_service is None:
        _search_service = SearchService()
    return _search_service