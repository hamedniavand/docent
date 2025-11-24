import logging
from typing import List, Optional
import random

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Mock embedding service for testing (generates random vectors)"""
    
    def __init__(self):
        self.embedding_dim = 768  # Standard embedding dimension
        logger.info("Using MOCK embedding service (random vectors)")
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate mock embedding (random vector)
        """
        try:
            # Generate random vector
            embedding = [random.random() for _ in range(self.embedding_dim)]
            logger.info(f"Generated mock embedding for text ({len(text)} chars)")
            return embedding
        except Exception as e:
            logger.error(f"Error generating mock embedding: {e}")
            return None
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """
        Generate embeddings for multiple texts
        """
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        
        logger.info(f"Generated {len(embeddings)} mock embeddings")
        return embeddings
    
    def generate_query_embedding(self, query: str) -> Optional[List[float]]:
        """
        Generate embedding for search query
        """
        return self.generate_embedding(query)

# Singleton instance
embedding_service = EmbeddingService()

def get_embedding_service() -> EmbeddingService:
    """Get embedding service instance"""
    return embedding_service