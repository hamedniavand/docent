# Docent Project - Complete State (Day 7)

## System Overview
- Platform: AI-Powered Knowledge Retention System
- Stack: FastAPI + PostgreSQL + ChromaDB + React
- Deployment: Docker on Ubuntu VPS with SSL
- Domain: https://docent.hexoplus.ir
- Progress: Day 7/30 (23% complete)

## Infrastructure
- Server: stock-server (Ubuntu, 9.8GB disk, 74% used)
- SSL: Let's Encrypt via Certbot
- Reverse Proxy: Nginx
- Containers: docent-backend, docent-postgres
- Network: docent-network (bridge)

## Database Schema
[Include complete schema from models.py]

## Environment Variables
[Include sanitized .env structure]

## Current Features
✅ Days 1-7 Complete:
- Infrastructure & SSL
- Database & Models (12 tables)
- Authentication (JWT-based)
- User Management (invite, roles, CRUD)
- Document Upload (single/multi, 50MB limit)
- Document Processing (parse, chunk, embed, vector DB)
- Storage: /opt/docent/data/storage & /opt/docent/data/chroma

## API Endpoints (20 total)
[List all endpoints]

## Test Accounts
- System Admin: hamed.niavand@gmail.com / admin123
- Company Admin: admin@democorp.com / admin123
- Employee: employee@democorp.com / password123

## File Structure
backend/
  app/
    api/endpoints/ - auth, pages, users, documents, processing
    core/ - config, database, security
    models/ - SQLAlchemy models
    schemas/ - Pydantic schemas
    services/ - embeddings, vector_db, document_processor, email
    utils/ - parsers, chunking, storage, disk_monitor
  
## Recent Changes (Last Session)
- Implemented document processing pipeline
- Added mock embeddings (ready for Google Gemini)
- ChromaDB vector storage
- Background processing with FastAPI
- Text chunking (800 tokens with 100 overlap)
- Document parsing for PDF, DOCX, PPTX, XLSX, TXT

## Known Issues
- Google Gemini API key needs real key (currently using mock)
- Disk space: 2.6GB free (need to monitor)
- Storage path issue resolved in last session

## Next Steps (Day 8)
- AI-powered search
- Query embeddings
- Vector similarity search
- Search UI with ranked results
