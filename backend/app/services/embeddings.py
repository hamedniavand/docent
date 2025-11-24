import logging
from typing import List, Optional
import google.generativeai as genai
from app.core.config import settings

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class EmbeddingService:
    """Generate embeddings using Google Gemini"""
    
    def __init__(self):
        self.model = "models/embedding-001"
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for a single text
        Returns: List of floats (embedding vector) or None on error
        """
        try:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """
        Generate embeddings for multiple texts
        Returns: List of embedding vectors (or None for failed ones)
        """
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        
        return embeddings
    
    def generate_query_embedding(self, query: str) -> Optional[List[float]]:
        """
        Generate embedding for search query
        """
        try:
            result = genai.embed_content(
                model=self.model,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            return None

# Singleton instance
embedding_service = EmbeddingService()

def get_embedding_service() -> EmbeddingService:
    """Get embedding service instance"""
    return embedding_service