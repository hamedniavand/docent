# Docent - Knowledge Retention Platform

## Overview
AI-powered multi-tenant SaaS for SME knowledge management, onboarding, and semantic search.

**Live URL**: https://docent.hexoplus.ir  
**Progress**: Day 18/30 (60% Complete)

## Tech Stack
- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **Vector DB**: ChromaDB
- **AI**: Google Gemini (embeddings)
- **Deployment**: Docker Compose + Nginx + SSL

## Features Completed

### Days 1-7: Foundation
- ✅ Infrastructure & SSL setup
- ✅ Database schema (12 tables)
- ✅ JWT Authentication
- ✅ User Management & Roles
- ✅ Document Upload (PDF, DOCX, PPTX, XLSX, TXT)
- ✅ Document Processing Pipeline

### Days 8-11: AI Search
- ✅ Semantic search with embeddings
- ✅ Vector similarity search
- ✅ Search history tracking
- ✅ Search UI with results

### Days 12-14: Onboarding System
- ✅ Onboarding path creation
- ✅ Step-by-step progress tracking
- ✅ User onboarding assignment
- ✅ Progress visualization

### Days 15-16: Case Studies & Analytics
- ✅ Case study templates
- ✅ Case study creation & management
- ✅ Analytics dashboard
- ✅ Search & document analytics
- ✅ User engagement metrics

### Days 17-18: Activity & Notifications
- ✅ Activity logging (logins, uploads, searches)
- ✅ Email notification templates
- ✅ Notification preferences
- ✅ Weekly digest emails
- ✅ Settings page

## API Endpoints (30+)
- `/auth/*` - Authentication
- `/users/*` - User management
- `/documents/*` - Document CRUD
- `/processing/*` - Document processing
- `/search/*` - Semantic search
- `/onboarding/*` - Onboarding paths
- `/cases/*` - Case studies
- `/analytics/*` - Analytics & reporting
- `/notifications/*` - Email preferences

## Quick Start
```bash
cd /opt/docent
docker-compose up -d
```

## Test Accounts
- **System Admin**: hamed.niavand@gmail.com / admin123
- **Company Admin**: admin@democorp.com / admin123

## Server Info
- IP: 77.221.143.47
- Location: /opt/docent
- Domain: docent.hexoplus.ir

## Next Steps (Days 19-30)
- [ ] Real-time notifications
- [ ] Mobile responsiveness
- [ ] Advanced search filters
- [ ] Performance optimization
- [ ] Production hardening
