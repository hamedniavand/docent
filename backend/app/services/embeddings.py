import logging
from typing import List, Optional
import google.generativeai as genai
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Google Gemini embedding service"""
    
    def __init__(self):
        self.embedding_dim = 768
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            logger.info("Gemini API configured successfully")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {e}")
    
    def generate_embedding(self, text: str, task_type: str = "retrieval_document") -> Optional[List[float]]:
        """
        Generate embedding for text
        task_type: 'retrieval_document' for docs, 'retrieval_query' for search queries
        """
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type=task_type
            )
            embedding = result['embedding']
            logger.info(f"Generated embedding for text ({len(text)} chars)")
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
    def generate_embeddings_batch(self, texts: List[str], task_type: str = "retrieval_document") -> List[Optional[List[float]]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text, task_type)
            embeddings.append(embedding)
        logger.info(f"Generated {len(embeddings)} embeddings")
        return embeddings
    
    def generate_query_embedding(self, query: str) -> Optional[List[float]]:
        """Generate embedding for search query"""
        return self.generate_embedding(query, task_type="retrieval_query")

# Singleton instance
_embedding_service = None

def get_embedding_service() -> EmbeddingService:
    """Get embedding service instance"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service