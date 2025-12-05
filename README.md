# 🎓 Docent - Knowledge Retention Platform

![Progress](https://img.shields.io/badge/Progress-27%25-blue)
![Day](https://img.shields.io/badge/Day-8%20of%2030-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## Overview

AI-powered multi-tenant SaaS for SME knowledge management, onboarding, and semantic search.

**Live Demo**: [https://docent.hexoplus.ir](https://docent.hexoplus.ir)

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI (Python 3.11) |
| Database | PostgreSQL 15 |
| Vector DB | ChromaDB |
| AI/Embeddings | Google Gemini |
| Frontend | Vanilla JS (embedded) |
| Deploy | Docker Compose + Nginx + SSL |

## 📊 Development Progress (8/30 Days)

### ✅ Completed

| Day | Phase | Features |
|-----|-------|----------|
| 1-2 | Infrastructure | VPS, Docker, SSL, Nginx, Domain |
| 3 | Database | PostgreSQL, 12 tables, SQLAlchemy models |
| 4 | Authentication | JWT tokens, login/logout, protected routes |
| 5 | User Management | CRUD, roles, invites, email integration |
| 6 | Document Upload | Single/multi upload, 50MB limit, drag & drop |
| 7 | Document Processing | Parse, chunk, embed, vector storage |
| **8** | **AI Search** | **Semantic search, Gemini embeddings, search history** |

### 🔜 Coming Up

| Day | Phase | Planned Features |
|-----|-------|------------------|
| 9-11 | Search Enhancement | Filters, ranking, deduplication, UI |
| 12-14 | Onboarding | Paths, chat interface, progress tracking |
| 15-17 | Case Studies | Templates, AI generation, export |
| 18-20 | Integrations | Google Drive, Sheets sync |
| 21-30 | Admin & Polish | Panels, testing, documentation |

## �� Search API
```bash
# Semantic search across documents
POST /search/
{
  "query": "remote work policy",
  "top_k": 5
}

# Response
{
  "query": "remote work policy",
  "results": [
    {
      "document_id": 12,
      "filename": "knowledge_base.txt",
      "chunk_text": "Remote work is available...",
      "score": 0.67
    }
  ],
  "search_time_ms": 435
}
```

## 🏗️ Architecture
```
User → Nginx (SSL:443) → FastAPI (:8000)
                              ↓
                     PostgreSQL (:5432)
                              ↓
                     ChromaDB (vectors)
                              ↓
                  Gemini API (embeddings)
```

## 🚀 Quick Start
```bash
git clone https://github.com/hamedniavand/docent.git
cd docent
cp .env.example .env
# Edit .env with your settings
docker-compose up -d
```

## 📁 Project Structure
```
docent/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/    # auth, users, documents, processing, search
│   │   ├── services/         # embeddings, vector_db, search
│   │   ├── models/           # SQLAlchemy (12 tables)
│   │   └── utils/            # parsers, chunking, storage
│   └── requirements.txt
├── docs/
├── docker-compose.yml
└── .env
```

## 🔌 API Endpoints (22 Total)

| Category | Endpoints |
|----------|-----------|
| Auth | POST /auth/login, GET /auth/me, POST /auth/logout |
| Users | GET/POST/PUT/DELETE /users/, POST /users/invite |
| Documents | POST /documents/upload, GET /documents/, DELETE /documents/{id} |
| Processing | POST /processing/process/{id}, GET /processing/status/{id} |
| **Search** | **POST /search/, GET /search/history** |

## 🔐 Test Credentials
```
System Admin: hamed.niavand@gmail.com / admin123
Company Admin: admin@democorp.com / admin123
```

---

**Last Updated**: December 2024 | **Day 8 of 30** | **27% Complete**
