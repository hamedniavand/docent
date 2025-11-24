import tiktoken
import logging
from typing import List, Dict
import uuid

logger = logging.getLogger(__name__)

class TextChunker:
    """Split text into chunks for embedding"""
    
    def __init__(self, chunk_size: int = 800, overlap: int = 100):
        """
        Args:
            chunk_size: Maximum tokens per chunk
            overlap: Tokens to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        # Use cl100k_base encoding (used by modern embeddings)
        try:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        except Exception:
            # Fallback to gpt2 if cl100k_base not available
            self.encoding = tiktoken.get_encoding("gpt2")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    def split_by_paragraphs(self, text: str) -> List[str]:
        """Split text by paragraphs"""
        # Split on double newlines first
        paragraphs = text.split('\n\n')
        
        # Further split on single newlines if paragraphs are empty
        result = []
        for para in paragraphs:
            if para.strip():
                result.append(para.strip())
            else:
                # Split on single newlines
                lines = para.split('\n')
                result.extend([line.strip() for line in lines if line.strip()])
        
        return result
    
    def chunk_text(self, text: str, document_id: int) -> List[Dict]:
        """
        Chunk text into smaller pieces
        Returns list of dicts with chunk_text, chunk_index, chunk_id, metadata
        """
        if not text or not text.strip():
            return []
        
        paragraphs = self.split_by_paragraphs(text)
        chunks = []
        current_chunk = []
        current_tokens = 0
        chunk_index = 0
        
        for para in paragraphs:
            para_tokens = self.count_tokens(para)
            
            # If single paragraph is too long, split it further
            if para_tokens > self.chunk_size:
                # Save current chunk if it exists
                if current_chunk:
                    chunk_text = "\n\n".join(current_chunk)
                    chunks.append(self._create_chunk(chunk_text, chunk_index, document_id))
                    chunk_index += 1
                    current_chunk = []
                    current_tokens = 0
                
                # Split long paragraph by sentences
                sentences = para.split('. ')
                temp_chunk = []
                temp_tokens = 0
                
                for sentence in sentences:
                    sent_tokens = self.count_tokens(sentence)
                    
                    if temp_tokens + sent_tokens > self.chunk_size and temp_chunk:
                        chunk_text = ". ".join(temp_chunk)
                        chunks.append(self._create_chunk(chunk_text, chunk_index, document_id))
                        chunk_index += 1
                        temp_chunk = [sentence]
                        temp_tokens = sent_tokens
                    else:
                        temp_chunk.append(sentence)
                        temp_tokens += sent_tokens
                
                # Add remaining sentences
                if temp_chunk:
                    chunk_text = ". ".join(temp_chunk)
                    chunks.append(self._create_chunk(chunk_text, chunk_index, document_id))
                    chunk_index += 1
                
                continue
            
            # Check if adding this paragraph exceeds chunk size
            if current_tokens + para_tokens > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = "\n\n".join(current_chunk)
                chunks.append(self._create_chunk(chunk_text, chunk_index, document_id))
                chunk_index += 1
                
                # Start new chunk with overlap
                # Keep last paragraph for overlap
                if self.overlap > 0 and current_chunk:
                    last_para = current_chunk[-1]
                    last_para_tokens = self.count_tokens(last_para)
                    if last_para_tokens < self.overlap:
                        current_chunk = [last_para, para]
                        current_tokens = last_para_tokens + para_tokens
                    else:
                        current_chunk = [para]
                        current_tokens = para_tokens
                else:
                    current_chunk = [para]
                    current_tokens = para_tokens
            else:
                current_chunk.append(para)
                current_tokens += para_tokens
        
        # Add final chunk
        if current_chunk:
            chunk_text = "\n\n".join(current_chunk)
            chunks.append(self._create_chunk(chunk_text, chunk_index, document_id))
        
        logger.info(f"Created {len(chunks)} chunks from document {document_id}")
        return chunks
    
    def _create_chunk(self, text: str, index: int, document_id: int) -> Dict:
        """Create chunk dict"""
        return {
            "chunk_text": text,
            "chunk_index": index,
            "chunk_id": f"doc_{document_id}_chunk_{index}_{uuid.uuid4().hex[:8]}",
            "token_count": self.count_tokens(text),
            "metadata": {
                "document_id": document_id,
                "chunk_index": index
            }
        }

def chunk_document_text(text: str, document_id: int, chunk_size: int = 800) -> List[Dict]:
    """
    Convenience function to chunk document text
    """
    chunker = TextChunker(chunk_size=chunk_size, overlap=100)
    return chunker.chunk_text(text, document_id)