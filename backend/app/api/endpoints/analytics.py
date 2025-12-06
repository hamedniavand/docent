from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, text
from typing import Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.models import (
    SystemAdmin,
    ActivityLog, User, Document, DocumentChunk, 
    SearchHistory, CaseInstance, Role
)
from app.schemas.analytics import (
    ActivityLogResponse, ActivityLogListResponse,
    SearchAnalytics, DocumentAnalytics, UserAnalytics,
    DashboardAnalytics, AnalyticsSummary
)
from app.api.deps.auth import require_active_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# ============ ACTIVITY LOGGING ============

def log_activity(db: Session, user_id: int, company_id: int, action: str, details: dict = None):
    """Helper function to log activity"""
    log = ActivityLog(
        user_id=user_id,
        company_id=company_id,
        action=action,
        details=details or {}
    )
    db.add(log)
    db.commit()
    return log


@router.get("/activity", response_model=ActivityLogListResponse)
def get_activity_logs(
    action: Optional[str] = None,
    user_id: Optional[int] = None,
    days: int = Query(7, ge=1, le=90),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get activity logs for the company"""
    since = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(ActivityLog).filter(
        ActivityLog.company_id == current_user.company_id,
        ActivityLog.timestamp >= since
    )
    
    if action:
        query = query.filter(ActivityLog.action.ilike(f"%{action}%"))
    
    if user_id:
        query = query.filter(ActivityLog.user_id == user_id)
    
    total = query.count()
    logs = query.order_by(desc(ActivityLog.timestamp)).offset((page - 1) * page_size).limit(page_size).all()
    
    # Add user names
    log_responses = []
    for log in logs:
        user = db.query(User).filter(User.id == log.user_id).first() if log.user_id else None
        log_responses.append(ActivityLogResponse(
            id=log.id,
            company_id=log.company_id,
            user_id=log.user_id,
            user_name=user.name if user else None,
            action=log.action,
            details=log.details or {},
            timestamp=log.timestamp
        ))
    
    return ActivityLogListResponse(
        total=total,
        logs=log_responses,
        page=page,
        page_size=page_size
    )


# ============ SEARCH ANALYTICS ============

@router.get("/search", response_model=SearchAnalytics)
def get_search_analytics(
    days: int = Query(30, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get search analytics"""
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)
    period_start = now - timedelta(days=days)
    
    # Total searches
    total = db.query(SearchHistory).filter(
        SearchHistory.company_id == current_user.company_id
    ).count()
    
    # Searches today
    today = db.query(SearchHistory).filter(
        SearchHistory.company_id == current_user.company_id,
        SearchHistory.timestamp >= today_start
    ).count()
    
    # Searches this week
    week = db.query(SearchHistory).filter(
        SearchHistory.company_id == current_user.company_id,
        SearchHistory.timestamp >= week_start
    ).count()
    
    # Top queries
    top_queries = db.query(
        SearchHistory.query_text,
        func.count(SearchHistory.id).label('count')
    ).filter(
        SearchHistory.company_id == current_user.company_id,
        SearchHistory.timestamp >= period_start
    ).group_by(SearchHistory.query_text).order_by(desc('count')).limit(10).all()
    
    # Searches by day
    searches_by_day = db.query(
        func.date(SearchHistory.timestamp).label('date'),
        func.count(SearchHistory.id).label('count')
    ).filter(
        SearchHistory.company_id == current_user.company_id,
        SearchHistory.timestamp >= period_start
    ).group_by(func.date(SearchHistory.timestamp)).order_by('date').all()
    
    return SearchAnalytics(
        total_searches=total,
        searches_today=today,
        searches_this_week=week,
        top_queries=[{"query": q, "count": c} for q, c in top_queries],
        searches_by_day=[{"date": str(d), "count": c} for d, c in searches_by_day]
    )


# ============ DOCUMENT ANALYTICS ============

@router.get("/documents", response_model=DocumentAnalytics)
def get_document_analytics(
    days: int = Query(30, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get document analytics"""
    period_start = datetime.utcnow() - timedelta(days=days)
    
    # Total documents
    total = db.query(Document).filter(
        Document.company_id == current_user.company_id
    ).count()
    
    # Processed documents
    processed = db.query(Document).filter(
        Document.company_id == current_user.company_id,
        Document.status == 'processed'
    ).count()
    
    # Total chunks
    chunks = db.query(DocumentChunk).filter(
        DocumentChunk.company_id == current_user.company_id
    ).count()
    
    # Documents by type
    docs = db.query(Document).filter(
        Document.company_id == current_user.company_id
    ).all()
    
    by_type = {}
    for doc in docs:
        ext = doc.filename.split('.')[-1].upper() if '.' in doc.filename else 'OTHER'
        by_type[ext] = by_type.get(ext, 0) + 1
    
    # Uploads by day
    uploads_by_day = db.query(
        func.date(Document.created_at).label('date'),
        func.count(Document.id).label('count')
    ).filter(
        Document.company_id == current_user.company_id,
        Document.created_at >= period_start
    ).group_by(func.date(Document.created_at)).order_by('date').all()
    
    # Most searched docs (from search history results_meta)
    # For now, return empty - would need to track doc hits in search
    most_searched = []
    
    return DocumentAnalytics(
        total_documents=total,
        processed_documents=processed,
        total_chunks=chunks,
        documents_by_type=by_type,
        uploads_by_day=[{"date": str(d), "count": c} for d, c in uploads_by_day],
        most_searched_docs=most_searched
    )


# ============ USER ANALYTICS ============

@router.get("/users", response_model=UserAnalytics)
def get_user_analytics(
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get user analytics"""
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    # Total users
    total = db.query(User).filter(
        User.company_id == current_user.company_id
    ).count()
    
    # Active users (logged in last 7 days)
    active = db.query(User).filter(
        User.company_id == current_user.company_id,
        User.last_login >= week_ago
    ).count()
    
    # Users by role
    users_with_roles = db.query(User, Role).join(
        Role, User.role_id == Role.id, isouter=True
    ).filter(User.company_id == current_user.company_id).all()
    
    by_role = {}
    for user, role in users_with_roles:
        role_name = role.name if role else "No Role"
        by_role[role_name] = by_role.get(role_name, 0) + 1
    
    # Recent logins
    recent_logins = db.query(User).filter(
        User.company_id == current_user.company_id,
        User.last_login.isnot(None)
    ).order_by(desc(User.last_login)).limit(10).all()
    
    # Most active users (by activity logs)
    active_users = db.query(
        User.id,
        User.name,
        func.count(ActivityLog.id).label('activity_count')
    ).join(ActivityLog, User.id == ActivityLog.user_id).filter(
        User.company_id == current_user.company_id,
        ActivityLog.timestamp >= week_ago
    ).group_by(User.id, User.name).order_by(desc('activity_count')).limit(10).all()
    
    return UserAnalytics(
        total_users=total,
        active_users=active,
        users_by_role=by_role,
        recent_logins=[{
            "user_id": u.id,
            "name": u.name,
            "last_login": str(u.last_login) if u.last_login else None
        } for u in recent_logins],
        most_active_users=[{
            "user_id": uid,
            "name": name,
            "activity_count": count
        } for uid, name, count in active_users]
    )


# ============ DASHBOARD SUMMARY ============

@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get quick analytics summary for dashboard"""
    # Handle SystemAdmin (no company_id)
    if isinstance(current_user, SystemAdmin):
        return AnalyticsSummary(
            total_searches=0,
            total_documents=0,
            total_users=0,
            total_cases=0,
            activity_count_today=0
        )
    
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    total_searches = db.query(SearchHistory).filter(
        SearchHistory.company_id == current_user.company_id
    ).count()
    
    total_documents = db.query(Document).filter(
        Document.company_id == current_user.company_id
    ).count()
    
    total_users = db.query(User).filter(
        User.company_id == current_user.company_id
    ).count()
    
    total_cases = db.query(CaseInstance).filter(
        CaseInstance.company_id == current_user.company_id
    ).count()
    
    activity_today = db.query(ActivityLog).filter(
        ActivityLog.company_id == current_user.company_id,
        ActivityLog.timestamp >= today_start
    ).count()
    
    return AnalyticsSummary(
        total_searches=total_searches,
        total_documents=total_documents,
        total_users=total_users,
        total_cases=total_cases,
        activity_count_today=activity_today
    )


# ============ FULL DASHBOARD ============

@router.get("/dashboard", response_model=DashboardAnalytics)
def get_dashboard_analytics(
    days: int = Query(30, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get comprehensive analytics dashboard data"""
    search_analytics = get_search_analytics(days=days, db=db, current_user=current_user)
    document_analytics = get_document_analytics(days=days, db=db, current_user=current_user)
    user_analytics = get_user_analytics(db=db, current_user=current_user)
    
    # Recent activity
    recent = db.query(ActivityLog).filter(
        ActivityLog.company_id == current_user.company_id
    ).order_by(desc(ActivityLog.timestamp)).limit(20).all()
    
    recent_activity = []
    for log in recent:
        user = db.query(User).filter(User.id == log.user_id).first() if log.user_id else None
        recent_activity.append(ActivityLogResponse(
            id=log.id,
            company_id=log.company_id,
            user_id=log.user_id,
            user_name=user.name if user else None,
            action=log.action,
            details=log.details or {},
            timestamp=log.timestamp
        ))
    
    return DashboardAnalytics(
        search=search_analytics,
        documents=document_analytics,
        users=user_analytics,
        recent_activity=recent_activity
    )
