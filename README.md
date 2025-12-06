# Docent - Knowledge Retention Platform

## Overview
AI-powered multi-tenant SaaS for SME knowledge management, onboarding, and semantic search.

**Live URL**: https://docent.hexoplus.ir  
**Progress**: Day 22/30 (73% Complete)

## Tech Stack
- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **Vector DB**: ChromaDB
- **AI**: Google Gemini (embeddings)
- **Deployment**: Docker Compose + Nginx + SSL

## Features Completed

### Core Features
- ✅ JWT Authentication & Authorization
- ✅ Multi-tenant Company Management
- ✅ User Management & Roles
- ✅ Document Upload (PDF, DOCX, PPTX, XLSX, TXT)
- ✅ Document Processing & Text Extraction
- ✅ AI-Powered Semantic Search
- ✅ Search History & Analytics

### Knowledge Management
- ✅ Case Studies with Templates
- ✅ Onboarding Paths & Progress Tracking
- ✅ Document Preview
- ✅ CSV Export for Analytics

### Analytics & Monitoring
- ✅ Activity Logging
- ✅ Search Analytics Dashboard
- ✅ User Engagement Metrics
- ✅ Document Statistics

### Notifications
- ✅ Email Notification System
- ✅ Notification Preferences
- ✅ Weekly Digest Emails

### Security & Performance
- ✅ Rate Limiting (Login Protection)
- ✅ Input Sanitization
- ✅ Security Headers (XSS, CSRF)
- ✅ Global Error Handling
- ✅ GZip Compression
- ✅ In-Memory Caching
- ✅ Request Logging

### UI/UX
- ✅ Mobile Responsive Design
- ✅ Toast Notifications
- ✅ Keyboard Shortcuts
- ✅ Help & Documentation Page

## API Endpoints (35+)
- `/auth/*` - Authentication
- `/users/*` - User Management
- `/documents/*` - Document CRUD
- `/processing/*` - Document Processing
- `/search/*` - Semantic Search
- `/onboarding/*` - Onboarding Paths
- `/cases/*` - Case Studies
- `/analytics/*` - Analytics & Reporting
- `/notifications/*` - Email Preferences

## Quick Start
```bash
cd /opt/docent
docker-compose up -d
```

## Demo Account
- **Email**: admin@democorp.com
- **Password**: admin123

## Keyboard Shortcuts
- `Ctrl+K` - Open Search
- `Ctrl+U` - Upload Document
- `Esc` - Close Modal

## Project Structure
```
/opt/docent/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/    # API routes
│   │   ├── core/             # Config, DB, Security
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── utils/            # Helpers
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Remaining (Days 23-30)
- [ ] Comprehensive Testing
- [ ] Bug Fixes
- [ ] Documentation
- [ ] Production Hardening
- [ ] Final Polish

## License
MIT
