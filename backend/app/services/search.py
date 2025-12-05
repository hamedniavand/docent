import logging
import time
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.services.embeddings import get_embedding_service
from app.services.vector_db import get_vector_db
from app.models.models import Document, DocumentChunk, SearchHistory
from datetime import datetime

logger = logging.getLogger(__name__)

class SearchService:
    """Semantic search service"""
    
    def __init__(self):
        self.embedding_service = get_embedding_service()
        self.vector_db = get_vector_db()
    
    def search(
        self, 
        query: str, 
        company_id: int, 
        user_id: int,
        db: Session,
        top_k: int = 5
    ) -> Dict:
        """
        Perform semantic search
        Returns: dict with results, timing, and metadata
        """
        start_time = time.time()
        
        try:
            # 1. Generate query embedding
            logger.info(f"Generating embedding for query: {query[:50]}...")
            query_embedding = self.embedding_service.generate_query_embedding(query)
            
            if query_embedding is None:
                return {
                    "success": False,
                    "error": "Failed to generate query embedding",
                    "results": [],
                    "search_time_ms": 0
                }
            
            # 2. Search vector database with company filter
            logger.info(f"Searching vector DB for company {company_id}")
            vector_results = self.vector_db.search(
                query_embedding=query_embedding,
                n_results=top_k,
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
                        filename = doc.filename if doc else "Unknown"
                    else:
                        filename = metadata.get('filename', 'Unknown')
                    
                    distance = distances[i] if i < len(distances) else 1.0
                    score = max(0, 1 - distance)
                    
                    results.append({
                        "document_id": doc_id,
                        "filename": filename,
                        "chunk_text": documents[i] if i < len(documents) else "",
                        "chunk_index": metadata.get('chunk_index', 0),
                        "score": round(score, 4)
                    })
            
            # Deduplicate results by document_id + chunk_index
            seen = set()
            unique_results = []
            for r in results:
                key = f"{r['document_id']}-{r['chunk_index']}"
                if key not in seen:
                    seen.add(key)
                    unique_results.append(r)
            
            results = unique_results
            results.sort(key=lambda x: x['score'], reverse=True)
            search_time_ms = round((time.time() - start_time) * 1000, 2)
            
            # Log search history
            try:
                search_record = SearchHistory(
                    user_id=user_id,
                    company_id=company_id,
                    query_text=query,
                    results_meta={
                        "total_results": len(results),
                        "top_score": results[0]['score'] if results else 0,
                        "search_time_ms": search_time_ms
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
                "search_time_ms": search_time_ms
            }
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": [],
                "search_time_ms": round((time.time() - start_time) * 1000, 2)
            }

_search_service = None

def get_search_service() -> SearchService:
    global _search_service
    if _search_service is None:
        _search_service = SearchService()
    return _search_service
