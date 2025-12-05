# 🎓 Docent - Knowledge Retention Platform

![Progress](https://img.shields.io/badge/Progress-33%25-blue)
![Day](https://img.shields.io/badge/Day-10%20of%2030-green)
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

## 📊 Development Progress (10/30 Days)

### ✅ Completed

| Day | Phase | Features |
|-----|-------|----------|
| 1-2 | Infrastructure | VPS, Docker, SSL, Nginx, Domain |
| 3 | Database | PostgreSQL, 12 tables, SQLAlchemy models |
| 4 | Authentication | JWT tokens, login/logout, protected routes |
| 5 | User Management | CRUD, roles, invites, email integration |
| 6 | Document Upload | Single/multi upload, 50MB limit, drag & drop |
| 7 | Document Processing | Parse, chunk, embed, vector storage |
| 8 | AI Search | Semantic search, Gemini embeddings |
| 9 | Search UI | Search page, highlighting, history |
| **10** | **Search Filters** | **File type filters, smart snippets, date range** |

### �� Coming Up

| Day | Phase | Planned Features |
|-----|-------|------------------|
| 11 | Search Polish | Dashboard widget, UX improvements |
| 12-14 | Onboarding | Paths, chat interface, progress tracking |
| 15-17 | Case Studies | Templates, AI generation, export |
| 18-30 | Integrations & Polish | Google Drive, admin panels, testing |

## 🔍 Search API
```bash
# Semantic search with filters
POST /search/
{
  "query": "remote work policy",
  "top_k": 5,
  "file_type": "pdf",        # Optional filter
  "date_from": "2024-01-01"  # Optional filter
}

# Get available filters
GET /search/filters

# Search history
GET /search/history
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

## 📁 Key Pages

- `/auth/login-page` - Login
- `/dashboard` - Main dashboard
- `/search-page` - AI Search
- `/documents-management` - Document management
- `/users-management` - User management

## 🔌 API Endpoints (24 Total)

| Category | Endpoints |
|----------|-----------|
| Auth | POST /auth/login, GET /auth/me |
| Users | CRUD /users/, POST /users/invite |
| Documents | POST /documents/upload, GET /documents/ |
| Processing | POST /processing/process/{id} |
| **Search** | **POST /search/, GET /search/filters, GET /search/history** |

## 🔐 Test Credentials
```
Company Admin: admin@democorp.com / admin123
```

---

**Last Updated**: December 2024 | **Day 10 of 30** | **33% Complete**
