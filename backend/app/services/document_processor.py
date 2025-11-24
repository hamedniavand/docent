import logging
from pathlib import Path
from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.models import Document, DocumentChunk
from app.utils.parsers import DocumentParser
from app.utils.chunking import chunk_document_text
from app.utils.storage import get_file_storage
from app.services.embeddings import get_embedding_service
from app.services.vector_db import get_vector_db
from app.core.config import settings
from datetime import datetime

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Process documents: parse, chunk, embed, store"""
    
    def __init__(self):
        self.parser = DocumentParser()
        self.embedding_service = get_embedding_service()
        self.vector_db = get_vector_db()
        self.storage = get_file_storage(settings.STORAGE_PATH)
    
    def process_document(self, document_id: int, db: Session) -> Dict:
        """
        Process a single document
        Returns: dict with status and details
        """
        try:
            # Get document from database
            document = db.query(Document).filter(Document.id == document_id).first()
            if not document:
                return {"success": False, "error": "Document not found"}
            
            # Update status
            document.status = "processing"
            db.commit()
            
            # Step 1: Parse document
            logger.info(f"Parsing document {document_id}: {document.filename}")
            file_path = self.storage.get_file_path(document.storage_path)
            
            parse_result = self.parser.parse_document(file_path, document.mime_type)
            
            if parse_result.get("error"):
                document.status = "error"
                db.commit()
                return {"success": False, "error": parse_result["error"]}
            
            text = parse_result["text"]
            
            if not text or len(text.strip()) < 50:
                document.status = "error"
                db.commit()
                return {"success": False, "error": "Insufficient text extracted"}
            
            # Step 2: Chunk text
            logger.info(f"Chunking document {document_id}")
            chunks = chunk_document_text(text, document_id, chunk_size=settings.CHUNK_SIZE)
            
            if not chunks:
                document.status = "error"
                db.commit()
                return {"success": False, "error": "No chunks created"}
            
            # Step 3: Generate embeddings
            logger.info(f"Generating embeddings for {len(chunks)} chunks")
            chunk_texts = [chunk["chunk_text"] for chunk in chunks]
            embeddings = self.embedding_service.generate_embeddings_batch(chunk_texts)
            
            # Filter out failed embeddings
            valid_chunks = []
            valid_embeddings = []
            for chunk, embedding in zip(chunks, embeddings):
                if embedding is not None:
                    valid_chunks.append(chunk)
                    valid_embeddings.append(embedding)
            
            if not valid_chunks:
                document.status = "error"
                db.commit()
                return {"success": False, "error": "Failed to generate embeddings"}
            
            # Step 4: Store in database
            logger.info(f"Storing {len(valid_chunks)} chunks in database")
            for chunk in valid_chunks:
                db_chunk = DocumentChunk(
                    document_id=document_id,
                    company_id=document.company_id,
                    chunk_text=chunk["chunk_text"],
                    chunk_index=chunk["chunk_index"],
                    chunk_id_for_vector=chunk["chunk_id"]
                )
                db.add(db_chunk)
            
            # Step 5: Store in vector database
            logger.info(f"Storing embeddings in vector database")
            chunk_ids = [chunk["chunk_id"] for chunk in valid_chunks]
            metadatas = [
                {
                    "document_id": document_id,
                    "company_id": document.company_id,
                    "chunk_index": chunk["chunk_index"],
                    "filename": document.filename
                }
                for chunk in valid_chunks
            ]
            
            success = self.vector_db.add_chunks(
                chunk_ids=chunk_ids,
                embeddings=valid_embeddings,
                texts=chunk_texts,
                metadatas=metadatas
            )
            
            if not success:
                document.status = "error"
                db.commit()
                return {"success": False, "error": "Failed to store in vector DB"}
            
            # Step 6: Generate summary (first 500 chars)
            summary = text[:500] + "..." if len(text) > 500 else text
            document.summary = summary
            
            # Update document status
            document.status = "processed"
            document.processed_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"Successfully processed document {document_id}")
            return {
                "success": True,
                "chunks_created": len(valid_chunks),
                "total_tokens": sum(chunk.get("token_count", 0) for chunk in valid_chunks)
            }
            
        except Exception as e:
            logger.error(f"Error processing document {document_id}: {e}")
            
            # Update status to error
            try:
                document = db.query(Document).filter(Document.id == document_id).first()
                if document:
                    document.status = "error"
                    db.commit()
            except:
                pass
            
            return {"success": False, "error": str(e)}

# Singleton
_processor = None

def get_document_processor() -> DocumentProcessor:
    """Get document processor instance"""
    global _processor
    if _processor is None:
        _processor = DocumentProcessor()
    return _processor