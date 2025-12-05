# 🎓 Docent - Knowledge Retention Platform

![Progress](https://img.shields.io/badge/Progress-23%25-blue)
![Day](https://img.shields.io/badge/Day-7%20of%2030-green)
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
| Frontend | Vanilla JS (embedded) |
| AI | Google Gemini |
| Deploy | Docker Compose + Nginx + SSL |

## 📊 Development Progress (7/30 Days)

### ✅ Completed

| Day | Phase | Features |
|-----|-------|----------|
| 1-2 | Infrastructure | VPS, Docker, SSL, Nginx, Domain |
| 3 | Database | PostgreSQL, 12 tables, SQLAlchemy models |
| 4 | Authentication | JWT tokens, login/logout, protected routes |
| 5 | User Management | CRUD, roles, invites, email integration |
| 6 | Document Upload | Single/multi upload, 50MB limit, drag & drop |
| 7 | Document Processing | Parse, chunk, embed, vector storage |

### 🔜 Coming Up

| Day | Phase | Planned Features |
|-----|-------|------------------|
| 8-11 | AI Search | Semantic search, ranking, filters |
| 12-14 | Onboarding | Paths, chat interface, progress tracking |
| 15-17 | Case Studies | Templates, AI generation, export |
| 18-20 | Integrations | Google Drive, Sheets sync |
| 21-23 | Admin Panels | Company/user management UI |
| 24-30 | Polish | Testing, bug fixes, documentation |

## 🏗️ Architecture
```
User → Nginx (SSL:443) → FastAPI (:8000)
                              ↓
                     PostgreSQL (:5432)
                              ↓
                     ChromaDB (vectors)
                              ↓
                     File Storage (/data)
```

## 🚀 Quick Start
```bash
# Clone
git clone https://github.com/hamedniavand/docent.git
cd docent

# Configure
cp .env.example .env
# Edit .env with your settings

# Run
docker-compose up -d

# Access
open http://localhost:8000
```

## 📁 Project Structure
```
docent/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/    # Routes (auth, users, documents, processing)
│   │   ├── core/             # Config, database, security
│   │   ├── models/           # SQLAlchemy models (12 tables)
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic (embeddings, vector DB)
│   │   └── utils/            # Parsers, chunking, storage
│   ├── Dockerfile
│   └── requirements.txt
├── docs/                     # Documentation
├── scripts/                  # Setup & utility scripts
├── docker-compose.yml
└── .env                      # Environment variables
```

## 🔌 API Endpoints (20 Total)

<details>
<summary>Click to expand</summary>

### Authentication
- `POST /auth/login` - User login
- `GET /auth/me` - Current user info
- `POST /auth/logout` - Logout

### Users
- `GET /users/` - List users
- `POST /users/` - Create user
- `POST /users/invite` - Invite user

### Documents
- `POST /documents/upload` - Upload file
- `GET /documents/` - List documents
- `GET /documents/{id}/download` - Download

### Processing
- `POST /processing/process/{id}` - Process document
- `GET /processing/status/{id}` - Get status

</details>

## 📈 Current Stats

- **API Endpoints**: 20
- **Database Tables**: 12
- **Supported Formats**: PDF, DOCX, PPTX, XLSX, TXT
- **Max Upload**: 50MB

## 🔐 Test Credentials
```
System Admin: hamed.niavand@gmail.com / admin123
Company Admin: admin@democorp.com / admin123
```

## 📚 Documentation

- [Project State (Day 7)](docs/PROJECT_STATE_DAY7.md)
- [Quick Reference](docs/QUICK_REFERENCE.md)
- [Day 7 Complete](docs/DAY7_COMPLETE.md)

## 📄 License

Private - All rights reserved

---

**Last Updated**: December 2024 | **Day 7 of 30** | **23% Complete**
