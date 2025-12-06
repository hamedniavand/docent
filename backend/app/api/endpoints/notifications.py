from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.models import User, SystemAdmin, Company, Document, SearchHistory, CaseInstance, UserOnboardingProgress, OnboardingPath
from app.schemas.notifications import (
    NotificationPreferences,
    NotificationPreferencesUpdate,
    NotificationPreferencesResponse
)
from app.api.deps.auth import require_active_user
from app.services.email import (
    send_weekly_digest,
    send_onboarding_reminder,
    send_document_processed_notification
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/preferences", response_model=NotificationPreferencesResponse)
def get_notification_preferences(
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get current user's notification preferences"""
    # SystemAdmin doesn't have notification preferences
    if isinstance(current_user, SystemAdmin):
        return NotificationPreferencesResponse(
            user_id=current_user.id,
            email_on_document_processed=True,
            email_on_new_case=True,
            email_weekly_digest=True,
            email_onboarding_reminders=True,
            updated_at=None
        )
    
    prefs = current_user.notification_preferences or {
        "email_on_document_processed": True,
        "email_on_new_case": True,
        "email_weekly_digest": True,
        "email_onboarding_reminders": True
    }
    
    return NotificationPreferencesResponse(
        user_id=current_user.id,
        email_on_document_processed=prefs.get("email_on_document_processed", True),
        email_on_new_case=prefs.get("email_on_new_case", True),
        email_weekly_digest=prefs.get("email_weekly_digest", True),
        email_onboarding_reminders=prefs.get("email_onboarding_reminders", True),
        updated_at=datetime.utcnow()
    )


@router.put("/preferences", response_model=NotificationPreferencesResponse)
def update_notification_preferences(
    data: NotificationPreferencesUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Update notification preferences"""
    # SystemAdmin doesn't have notification preferences
    if isinstance(current_user, SystemAdmin):
        raise HTTPException(status_code=400, detail="System admins do not have notification preferences")
    
    prefs = dict(current_user.notification_preferences or {
        "email_on_document_processed": True,
        "email_on_new_case": True,
        "email_weekly_digest": True,
        "email_onboarding_reminders": True
    })
    
    if data.email_on_document_processed is not None:
        prefs["email_on_document_processed"] = data.email_on_document_processed
    if data.email_on_new_case is not None:
        prefs["email_on_new_case"] = data.email_on_new_case
    if data.email_weekly_digest is not None:
        prefs["email_weekly_digest"] = data.email_weekly_digest
    if data.email_onboarding_reminders is not None:
        prefs["email_onboarding_reminders"] = data.email_onboarding_reminders
    
    # Update user
    current_user.notification_preferences = prefs
    db.commit()
    
    return NotificationPreferencesResponse(
        user_id=current_user.id,
        email_on_document_processed=prefs["email_on_document_processed"],
        email_on_new_case=prefs["email_on_new_case"],
        email_weekly_digest=prefs["email_weekly_digest"],
        email_onboarding_reminders=prefs["email_onboarding_reminders"],
        updated_at=datetime.utcnow()
    )


@router.post("/send-digest")
async def trigger_weekly_digest(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Manually trigger weekly digest for testing"""
    # Get company info
    company = db.query(Company).filter(Company.id == current_user.company_id).first()
    
    # Calculate stats for the week
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    searches = db.query(SearchHistory).filter(
        SearchHistory.company_id == current_user.company_id,
        SearchHistory.timestamp >= week_ago
    ).count()
    
    documents = db.query(Document).filter(
        Document.company_id == current_user.company_id,
        Document.created_at >= week_ago
    ).count()
    
    cases = db.query(CaseInstance).filter(
        CaseInstance.company_id == current_user.company_id,
        CaseInstance.created_at >= week_ago
    ).count()
    
    active_users = db.query(User).filter(
        User.company_id == current_user.company_id,
        User.last_login >= week_ago
    ).count()
    
    # Top queries
    from sqlalchemy import func, desc
    top_queries_result = db.query(SearchHistory.query_text).filter(
        SearchHistory.company_id == current_user.company_id,
        SearchHistory.timestamp >= week_ago
    ).group_by(SearchHistory.query_text).order_by(
        desc(func.count(SearchHistory.id))
    ).limit(5).all()
    
    top_queries = [q[0] for q in top_queries_result] if top_queries_result else ["No searches this week"]
    
    stats = {
        "searches": searches,
        "documents": documents,
        "cases": cases,
        "active_users": active_users,
        "top_queries": top_queries
    }
    
    # Send digest
    background_tasks.add_task(
        send_weekly_digest,
        to_email=current_user.email,
        to_name=current_user.name,
        company_name=company.name if company else "Your Company",
        stats=stats
    )
    
    return {"message": "Weekly digest queued", "stats": stats}


@router.post("/send-onboarding-reminders")
async def trigger_onboarding_reminders(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Send reminders to users with incomplete onboarding"""
    # Find incomplete onboarding progress
    incomplete = db.query(UserOnboardingProgress).filter(
        UserOnboardingProgress.company_id == current_user.company_id,
        UserOnboardingProgress.completed_at.is_(None)
    ).all()
    
    reminders_sent = 0
    
    for progress in incomplete:
        user = db.query(User).filter(User.id == progress.user_id).first()
        path = db.query(OnboardingPath).filter(OnboardingPath.id == progress.path_id).first()
        
        if not user or not path:
            continue
        
        # Check user preferences
        prefs = user.notification_preferences or {}
        if not prefs.get("email_onboarding_reminders", True):
            continue
        
        # Get total steps
        steps = path.steps_json.get("steps", []) if path.steps_json else []
        total_steps = len(steps)
        current_step = len(progress.completed_steps or [])
        
        if current_step < total_steps:
            background_tasks.add_task(
                send_onboarding_reminder,
                to_email=user.email,
                to_name=user.name,
                path_name=path.name,
                current_step=current_step,
                total_steps=total_steps,
                path_id=path.id
            )
            reminders_sent += 1
    
    return {"message": f"Sent {reminders_sent} onboarding reminders"}


@router.post("/test-email")
async def test_email(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Send a test email to current user"""
    background_tasks.add_task(
        send_document_processed_notification,
        to_email=current_user.email,
        to_name=current_user.name,
        document_name="Test Document.pdf",
        status="processed",
        chunks_count=15
    )
    
    return {"message": f"Test email queued to {current_user.email}"}
