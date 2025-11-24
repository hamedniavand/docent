import chromadb
from typing import List, Dict, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class VectorDatabase:
    """Chroma vector database for storing document embeddings"""
    
    def __init__(self, persist_directory: str = None):
        if persist_directory is None:
            persist_directory = settings.CHROMA_PATH
        
        try:
            # Use simpler settings for Chroma
            self.client = chromadb.PersistentClient(path=persist_directory)
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"Vector DB initialized at {persist_directory}")
        except Exception as e:
            logger.error(f"Error initializing Vector DB: {e}")
            raise
    
    def add_chunks(
        self,
        chunk_ids: List[str],
        embeddings: List[List[float]],
        texts: List[str],
        metadatas: List[Dict]
    ) -> bool:
        """Add document chunks to vector database"""
        try:
            self.collection.add(
                ids=chunk_ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )
            logger.info(f"Added {len(chunk_ids)} chunks to vector DB")
            return True
        except Exception as e:
            logger.error(f"Error adding chunks to vector DB: {e}")
            return False
    
    def search(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict] = None
    ) -> Dict:
        """Search for similar chunks"""
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where
            )
            return results
        except Exception as e:
            logger.error(f"Error searching vector DB: {e}")
            return {"ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    def delete_by_document(self, document_id: int) -> bool:
        """Delete all chunks for a document"""
        try:
            results = self.collection.get(
                where={"document_id": document_id}
            )
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                logger.info(f"Deleted {len(results['ids'])} chunks for document {document_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error deleting document chunks: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        try:
            count = self.collection.count()
            return {
                "total_chunks": count,
                "collection_name": self.collection.name
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"total_chunks": 0, "collection_name": "unknown"}

# Singleton instance
_vector_db = None

def get_vector_db() -> VectorDatabase:
    """Get vector database instance (singleton)"""
    global _vector_db
    if _vector_db is None:
        _vector_db = VectorDatabase()
    return _vector_db