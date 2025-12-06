from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.core.database import get_db
from app.api.deps.auth import require_active_user
from app.models.models import (
    OnboardingPath, User, SystemAdmin, 
    UserOnboardingProgress, Company
)
from app.schemas.onboarding import (
    OnboardingPathCreate, OnboardingPathResponse, OnboardingPathListResponse,
    UserProgressCreate, StepProgressUpdate, UserProgressResponse
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])

# ============ ONBOARDING PATHS ============

@router.post("/paths", response_model=OnboardingPathResponse, status_code=status.HTTP_201_CREATED)
def create_onboarding_path(
    path_data: OnboardingPathCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Create a new onboarding path (template)"""
    if isinstance(current_user, SystemAdmin):
        raise HTTPException(status_code=400, detail="System admins cannot create paths")
    
    steps_json = {
        "steps": [step.dict() for step in path_data.steps],
        "total_steps": len(path_data.steps)
    }
    
    new_path = OnboardingPath(
        company_id=current_user.company_id,
        department_id=path_data.department_id,
        name=path_data.name,
        steps_json=steps_json,
        created_by=current_user.id
    )
    
    db.add(new_path)
    db.commit()
    db.refresh(new_path)
    
    return OnboardingPathResponse(
        id=new_path.id,
        name=new_path.name,
        description=path_data.description,
        department_id=new_path.department_id,
        steps_json=new_path.steps_json,
        created_by=new_path.created_by,
        created_at=new_path.created_at
    )

@router.get("/paths", response_model=OnboardingPathListResponse)
def list_onboarding_paths(
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """List all onboarding paths for company"""
    if isinstance(current_user, SystemAdmin):
        raise HTTPException(status_code=400, detail="Use company-specific endpoint")
    
    paths = db.query(OnboardingPath).filter(
        OnboardingPath.company_id == current_user.company_id
    ).all()
    
    return OnboardingPathListResponse(
        total=len(paths),
        paths=[
            OnboardingPathResponse(
                id=p.id,
                name=p.name,
                description=p.steps_json.get("description"),
                department_id=p.department_id,
                steps_json=p.steps_json,
                created_by=p.created_by,
                created_at=p.created_at
            )
            for p in paths
        ]
    )

@router.get("/paths/{path_id}", response_model=OnboardingPathResponse)
def get_onboarding_path(
    path_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get specific onboarding path details"""
    path = db.query(OnboardingPath).filter(OnboardingPath.id == path_id).first()
    
    if not path:
        raise HTTPException(status_code=404, detail="Path not found")
    
    if not isinstance(current_user, SystemAdmin) and path.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return OnboardingPathResponse(
        id=path.id,
        name=path.name,
        description=path.steps_json.get("description"),
        department_id=path.department_id,
        steps_json=path.steps_json,
        created_by=path.created_by,
        created_at=path.created_at
    )

@router.delete("/paths/{path_id}")
def delete_onboarding_path(
    path_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Delete an onboarding path"""
    path = db.query(OnboardingPath).filter(OnboardingPath.id == path_id).first()
    
    if not path:
        raise HTTPException(status_code=404, detail="Path not found")
    
    if not isinstance(current_user, SystemAdmin) and path.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    db.delete(path)
    db.commit()
    
    return {"message": "Path deleted successfully"}

# ============ USER PROGRESS ============

@router.post("/progress/start", response_model=UserProgressResponse)
def start_onboarding(
    data: UserProgressCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Start onboarding for a user"""
    if isinstance(current_user, SystemAdmin):
        raise HTTPException(status_code=400, detail="System admins cannot start onboarding")
    
    path = db.query(OnboardingPath).filter(OnboardingPath.id == data.path_id).first()
    if not path:
        raise HTTPException(status_code=404, detail="Onboarding path not found")
    
    existing = db.query(UserOnboardingProgress).filter(
        UserOnboardingProgress.user_id == data.user_id,
        UserOnboardingProgress.path_id == data.path_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="User already started this onboarding")
    
    progress = UserOnboardingProgress(
        user_id=data.user_id,
        path_id=data.path_id,
        company_id=current_user.company_id,
        current_step=0,
        completed_steps=[]
    )
    
    db.add(progress)
    db.commit()
    db.refresh(progress)
    
    total_steps = path.steps_json.get("total_steps", len(path.steps_json.get("steps", [])))
    
    return UserProgressResponse(
        id=progress.id,
        user_id=progress.user_id,
        path_id=progress.path_id,
        path_name=path.name,
        current_step=progress.current_step,
        total_steps=total_steps,
        completed_steps=progress.completed_steps or [],
        percent_complete=0.0,
        started_at=progress.started_at,
        completed_at=progress.completed_at
    )

@router.get("/progress/me", response_model=List[UserProgressResponse])
def get_my_progress(
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get current user's onboarding progress"""
    if isinstance(current_user, SystemAdmin):
        raise HTTPException(status_code=400, detail="Not available for system admins")
    
    progress_list = db.query(UserOnboardingProgress).filter(
        UserOnboardingProgress.user_id == current_user.id
    ).all()
    
    results = []
    for progress in progress_list:
        path = db.query(OnboardingPath).filter(OnboardingPath.id == progress.path_id).first()
        if path:
            total_steps = path.steps_json.get("total_steps", len(path.steps_json.get("steps", [])))
            completed = len(progress.completed_steps or [])
            percent = (completed / total_steps * 100) if total_steps > 0 else 0
            
            results.append(UserProgressResponse(
                id=progress.id,
                user_id=progress.user_id,
                path_id=progress.path_id,
                path_name=path.name,
                current_step=progress.current_step,
                total_steps=total_steps,
                completed_steps=progress.completed_steps or [],
                percent_complete=round(percent, 1),
                started_at=progress.started_at,
                completed_at=progress.completed_at
            ))
    
    return results

@router.put("/progress/{progress_id}/step")
def update_step_progress(
    progress_id: int,
    data: StepProgressUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Mark a step as complete/incomplete"""
    progress = db.query(UserOnboardingProgress).filter(
        UserOnboardingProgress.id == progress_id
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    if not isinstance(current_user, SystemAdmin) and progress.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Create a NEW list to ensure SQLAlchemy detects the change
    completed = list(progress.completed_steps or [])
    
    if data.completed and data.step_index not in completed:
        completed.append(data.step_index)
        completed.sort()
    elif not data.completed and data.step_index in completed:
        completed.remove(data.step_index)
    
    # Assign a new list object to trigger SQLAlchemy change detection
    progress.completed_steps = list(completed)
    progress.current_step = max(completed) + 1 if completed else 0
    
    path = db.query(OnboardingPath).filter(OnboardingPath.id == progress.path_id).first()
    total_steps = path.steps_json.get("total_steps", 0) if path else 0
    
    if len(completed) >= total_steps and total_steps > 0:
        progress.completed_at = datetime.utcnow()
    else:
        progress.completed_at = None
    
    db.commit()
    
    return {
        "message": "Progress updated",
        "completed_steps": completed,
        "current_step": progress.current_step,
        "is_complete": progress.completed_at is not None
    }

@router.get("/progress/user/{user_id}", response_model=List[UserProgressResponse])
def get_user_progress(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get onboarding progress for a specific user (admin only)"""
    if not isinstance(current_user, SystemAdmin):
        user = db.query(User).filter(User.id == user_id).first()
        if not user or user.company_id != current_user.company_id:
            raise HTTPException(status_code=403, detail="Access denied")
    
    progress_list = db.query(UserOnboardingProgress).filter(
        UserOnboardingProgress.user_id == user_id
    ).all()
    
    results = []
    for progress in progress_list:
        path = db.query(OnboardingPath).filter(OnboardingPath.id == progress.path_id).first()
        if path:
            total_steps = path.steps_json.get("total_steps", len(path.steps_json.get("steps", [])))
            completed = len(progress.completed_steps or [])
            percent = (completed / total_steps * 100) if total_steps > 0 else 0
            
            results.append(UserProgressResponse(
                id=progress.id,
                user_id=progress.user_id,
                path_id=progress.path_id,
                path_name=path.name,
                current_step=progress.current_step,
                total_steps=total_steps,
                completed_steps=progress.completed_steps or [],
                percent_complete=round(percent, 1),
                started_at=progress.started_at,
                completed_at=progress.completed_at
            ))
    
    return results

@router.get("/stats")
def get_onboarding_stats(
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get onboarding statistics for dashboard"""
    if isinstance(current_user, SystemAdmin):
        raise HTTPException(status_code=400, detail="Not available for system admins")
    
    company_id = current_user.company_id
    
    total_paths = db.query(OnboardingPath).filter(
        OnboardingPath.company_id == company_id
    ).count()
    
    active_onboardings = db.query(UserOnboardingProgress).filter(
        UserOnboardingProgress.company_id == company_id,
        UserOnboardingProgress.completed_at == None
    ).count()
    
    completed_onboardings = db.query(UserOnboardingProgress).filter(
        UserOnboardingProgress.company_id == company_id,
        UserOnboardingProgress.completed_at != None
    ).count()
    
    return {
        "total_paths": total_paths,
        "active_onboardings": active_onboardings,
        "completed_onboardings": completed_onboardings
    }
