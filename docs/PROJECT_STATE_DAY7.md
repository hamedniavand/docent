# Docent - Complete Project State (Day 7)

**Last Updated**: 2025-11-24  
**Progress**: 7/30 Days (23%)  
**Live URL**: https://docent.hexoplus.ir  
**Repository**: https://github.com/hamedniavand/docent

---

## 🎯 Project Overview

AI-powered knowledge retention platform that helps companies capture, process, and retrieve organizational knowledge through intelligent document management and semantic search.

---

## 🏗️ Architecture

### Tech Stack
- **Backend**: FastAPI 0.104.1 (Python 3.11)
- **Database**: PostgreSQL 15
- **Vector DB**: ChromaDB 0.4.18
- **Frontend**: Vanilla JavaScript (embedded)
- **Deployment**: Docker Compose
- **Web Server**: Nginx with SSL (Let's Encrypt)
- **AI**: Google Gemini (embeddings) - currently using mock for testing

### Infrastructure
```
Internet → Nginx (SSL:443) → FastAPI (8000)
                            ↓
                    PostgreSQL (5432)
                            ↓
                    ChromaDB (vectors)
                            ↓
                File Storage (/opt/docent/data)
```

### Server Details
- **Host**: stock-server (Ubuntu)
- **Disk**: 9.8GB total, 7.0GB used (74%), 2.6GB free
- **Docker Containers**: 2 (backend, postgres)
- **Network**: docent-network (bridge)

---

## 📊 Database Schema (12 Tables)

### Core Tables
1. **system_admins** - Global administrators
2. **companies** - Multi-tenant companies
3. **users** - Company users with roles
4. **roles** - Custom role definitions per company
5. **departments** - Organizational structure

### Document Management
6. **documents** - Uploaded files metadata
7. **doc_chunks** - Processed text chunks for RAG

### Knowledge System
8. **case_templates** - Onboarding templates
9. **case_instances** - Active onboarding cases
10. **onboarding_paths** - Learning paths

### Analytics
11. **search_history** - Search queries and results
12. **activity_logs** - User actions tracking

---

## ✅ Completed Features (Days 1-7)

### Day 1-2: Infrastructure
- ✅ Ubuntu VPS setup
- ✅ Docker & Docker Compose
- ✅ SSL certificate (Let's Encrypt)
- ✅ Nginx reverse proxy
- ✅ Domain configuration

### Day 3: Database
- ✅ PostgreSQL container
- ✅ 12-table schema
- ✅ SQLAlchemy models
- ✅ Relationships & constraints
- ✅ Sample data seeding

### Day 4: Authentication
- ✅ JWT token-based auth
- ✅ Password hashing (bcrypt)
- ✅ Login/logout endpoints
- ✅ Protected routes
- ✅ User session management
- ✅ Login UI page

### Day 5: User Management
- ✅ User CRUD operations
- ✅ Role-based permissions
- ✅ User invite system
- ✅ Email integration (SendGrid)
- ✅ User management UI
- ✅ Search & pagination

### Day 6: Document Upload
- ✅ Single file upload
- ✅ Multiple file upload
- ✅ File type validation (PDF, DOCX, PPTX, XLSX, TXT)
- ✅ File size limits (50MB)
- ✅ Storage management (/opt/docent/data/storage)
- ✅ Document metadata tracking
- ✅ Download functionality
- ✅ Delete functionality
- ✅ Document list UI with search
- ✅ Drag & drop interface

### Day 7: Document Processing ⭐ NEW
- ✅ Text extraction from documents
  - PDF parsing (pdfplumber)
  - DOCX parsing (python-docx)
  - PPTX parsing (python-pptx)
  - XLSX parsing (openpyxl)
  - TXT parsing
- ✅ Text chunking
  - 800 tokens per chunk
  - 100 token overlap
  - Smart paragraph splitting
  - Token counting (tiktoken)
- ✅ Embedding generation
  - Mock embeddings (768 dimensions)
  - Ready for Google Gemini integration
- ✅ Vector storage
  - ChromaDB integration
  - Cosine similarity search
  - Metadata filtering
- ✅ Background processing
  - Non-blocking document processing
  - Status tracking (uploaded → processing → processed → error)
  - Progress monitoring
- ✅ Processing endpoints
  - POST /processing/process/{id}
  - POST /processing/process-all
  - GET /processing/status/{id}

---

## 🔌 API Endpoints (20 Total)

### Authentication
- `POST /auth/login` - User login
- `GET /auth/me` - Current user info
- `POST /auth/logout` - User logout
- `GET /auth/login-page` - Login UI

### Users
- `GET /users/` - List users (paginated, searchable)
- `POST /users/` - Create user
- `GET /users/{id}` - Get user details
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete/deactivate user
- `POST /users/invite` - Invite user via email
- `GET /users/company/{id}/roles` - Get company roles

### Documents
- `POST /documents/upload` - Upload single file
- `POST /documents/upload-multiple` - Upload multiple files
- `GET /documents/` - List documents (paginated, searchable)
- `GET /documents/{id}` - Get document details
- `GET /documents/{id}/download` - Download file
- `DELETE /documents/{id}` - Delete document
- `GET /documents/stats/company` - Document statistics

### Processing
- `POST /processing/process/{id}` - Process document
- `POST /processing/process-all` - Process all uploaded
- `GET /processing/status/{id}` - Get processing status

### Pages
- `GET /` - Landing page
- `GET /dashboard` - User dashboard
- `GET /users-management` - User management UI
- `GET /documents-management` - Document management UI

### System
- `GET /health` - Health check
- `GET /docs` - API documentation (Swagger)

---

## 📁 Project Structure
```
/opt/docent/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI application
│   │   ├── api/
│   │   │   ├── deps/
│   │   │   │   └── auth.py           # Auth dependencies
│   │   │   └── endpoints/
│   │   │       ├── auth.py           # Auth routes
│   │   │       ├── pages.py          # UI pages
│   │   │       ├── users.py          # User management
│   │   │       ├── documents.py      # Document upload/download
│   │   │       └── processing.py     # Document processing
│   │   ├── core/
│   │   │   ├── config.py             # Configuration
│   │   │   ├── database.py           # Database connection
│   │   │   └── security.py           # Security utilities
│   │   ├── models/
│   │   │   └── models.py             # SQLAlchemy models (12 tables)
│   │   ├── schemas/
│   │   │   ├── auth.py               # Auth schemas
│   │   │   ├── users.py              # User schemas
│   │   │   └── documents.py          # Document schemas
│   │   ├── services/
│   │   │   ├── email.py              # Email service (SendGrid)
│   │   │   ├── embeddings.py         # Embedding generation (mock)
│   │   │   ├── vector_db.py          # ChromaDB integration
│   │   │   └── document_processor.py # Document processing pipeline
│   │   └── utils/
│   │       ├── parsers.py            # Document text extraction
│   │       ├── chunking.py           # Text chunking
│   │       ├── storage.py            # File storage
│   │       └── disk_monitor.py       # Disk space monitoring
│   ├── requirements.txt              # Python dependencies
│   └── Dockerfile
├── docker-compose.yml                # Container orchestration
├── .env                              # Environment variables
├── .gitignore
├── README.md
└── docs/
    ├── DAY4_COMPLETE.md
    ├── DAY5_COMPLETE.md
    ├── DAY6_COMPLETE.md
    ├── DAY7_COMPLETE.md
    └── PROJECT_STATE_DAY7.md         # This file
```

---

## 🔐 Environment Variables
```bash
# Database
DATABASE_URL=postgresql://docent_user:***@postgres:5432/docent

# Security
SECRET_KEY=***
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Email (SendGrid)
SENDGRID_API_KEY=***
FROM_EMAIL=noreply@docent.com

# AI
GEMINI_API_KEY=*** (currently using mock)

# Storage
STORAGE_PATH=/opt/docent/data/storage
CHROMA_PATH=/opt/docent/data/chroma

# Processing
CHUNK_SIZE=800
CHUNK_OVERLAP=100
MAX_UPLOAD_SIZE_MB=50
```

---

## 👥 Test Accounts
```
System Admin:
  Email: hamed.niavand@gmail.com
  Password: admin123
  Access: All companies, global settings

Company Admin (Demo Corp):
  Email: admin@democorp.com
  Password: admin123
  Access: User management, documents, settings

Employee (Demo Corp):
  Email: employee@democorp.com
  Password: password123
  Access: View documents, search

Test User:
  Email: test.day7@democorp.com
  Password: test123
  Access: Basic employee
```

---

## 🧪 Testing Results

### Document Processing Test
- **Document**: handbook2.txt
- **Size**: 332 characters
- **Status**: ✅ Successfully processed
- **Chunks**: 1 chunk created
- **Embedding**: 768-dimensional vector (mock)
- **Vector DB**: Stored in ChromaDB
- **Summary**: Generated (first 500 chars)

### Database State
```sql
Documents: 3 total (1 processed, 2 uploaded)
Chunks: 1 chunk in doc_chunks table
Users: 7 users (1 system admin, 6 company users)
Roles: 3 roles (Admin, Department Lead, Employee)
```

---

## 🐛 Known Issues & Solutions

### 1. Google Gemini API Key
- **Issue**: API key expired/invalid
- **Current**: Using mock embeddings (random 768-dim vectors)
- **Solution**: Need valid Gemini API key from https://aistudio.google.com/app/apikey
- **Impact**: Low - mock works for testing, swap in real key before production

### 2. Disk Space
- **Status**: 74% used (2.6GB free of 9.8GB)
- **Monitoring**: Added disk_monitor.py utility
- **Action**: Clean Docker images regularly, monitor growth
- **Commands**:
```bash
  docker system prune -a --volumes -f
  sudo apt-get clean
  sudo journalctl --vacuum-size=50M
```

### 3. Storage Path
- **Fixed**: Documents now properly stored in /opt/docent/data/storage/company_1/
- **Structure**: company_{id}/{timestamp}_{uuid}.{ext}

### 4. ChromaDB Telemetry Warnings
- **Issue**: Harmless telemetry errors in logs
- **Impact**: None - doesn't affect functionality
- **Can ignore**: These are just logging warnings

---

## 🚀 Next Steps (Day 8-9)

### Day 8: AI Search (Planned)
- [ ] Search query processing
- [ ] Query embedding generation
- [ ] Vector similarity search
- [ ] Result ranking & relevance scoring
- [ ] Search UI with filters
- [ ] Search history tracking
- [ ] Estimated: 90-120 minutes

### Day 9: Search Enhancement
- [ ] Advanced filters (date, type, user)
- [ ] Multi-document search
- [ ] Search analytics
- [ ] Search suggestions
- [ ] Export search results

### Day 10-14: Onboarding System
- [ ] Case templates
- [ ] Interactive onboarding flows
- [ ] Progress tracking
- [ ] Knowledge verification

### Day 15-30: Advanced Features
- [ ] Real-time notifications
- [ ] Advanced analytics
- [ ] Mobile responsiveness
- [ ] Performance optimization
- [ ] Production hardening

---

## 📈 Progress Tracking
```
✅ Days 1-2: Infrastructure (100%)
✅ Day 3: Database (100%)
✅ Day 4: Authentication (100%)
✅ Day 5: User Management (100%)
✅ Day 6: Document Upload (100%)
✅ Day 7: Document Processing (100%)
⏳ Day 8: AI Search (0%)
⏳ Days 9-30: Remaining features (0%)

Overall: 23% Complete (7/30 days)
```

---

## 🔧 Common Commands

### Development
```bash
# Start system
cd /opt/docent
docker-compose up -d

# View logs
docker logs docent-backend -f
docker logs docent-postgres -f

# Restart backend
docker-compose restart backend

# Stop system
docker-compose down

# Rebuild after code changes
docker-compose build backend --no-cache
docker-compose up -d
```

### Database
```bash
# Access PostgreSQL
docker exec -it docent-postgres psql -U docent_user -d docent

# Run query
docker exec docent-postgres psql -U docent_user -d docent -c "SELECT COUNT(*) FROM documents;"

# Backup database
docker exec docent-postgres pg_dump -U docent_user docent > backup.sql
```

### Git
```bash
# Commit changes
git add .
git commit -m "Description"
git push origin main

# Check status
git status
git log --oneline -5
```

### Monitoring
```bash
# Disk usage
df -h /

# Container stats
docker stats --no-stream

# Check health
curl https://docent.hexoplus.ir/health
```

---

## 🔗 Important URLs

- **Live Site**: https://docent.hexoplus.ir
- **API Docs**: https://docent.hexoplus.ir/docs
- **Login**: https://docent.hexoplus.ir/auth/login-page
- **Dashboard**: https://docent.hexoplus.ir/dashboard
- **GitHub**: https://github.com/hamedniavand/docent
- **Gemini API**: https://aistudio.google.com/app/apikey

---

## 📞 Support & Resources

- **ChromaDB Docs**: https://docs.trychroma.com
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Docker Docs**: https://docs.docker.com

---

**Document Version**: 1.0  
**Last Session**: Day 7 - Document Processing Complete  
**Next Session**: Day 8 - AI Search Implementation
