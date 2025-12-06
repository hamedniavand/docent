from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from app.core.database import get_db
from app.core.security import get_password_hash, create_access_token
from app.models.models import User, Company, Role, ActivityLog
from app.schemas.users import (
    UserCreate, UserUpdate, UserInvite, UserResponse, 
    UserListResponse, RoleResponse
)
from app.api.deps.auth import require_active_user, require_system_admin
from app.services.email import send_invite_email
from datetime import datetime, timedelta
import secrets

router = APIRouter(prefix="/users", tags=["User Management"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Create a new user (Company Admin or System Admin only)
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Verify company exists
    company = db.query(Company).filter(Company.id == user_data.company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Create user
    hashed_password = get_password_hash(user_data.password) if user_data.password else None
    
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        company_id=user_data.company_id,
        role_id=user_data.role_id,
        hashed_password=hashed_password,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Send invite email if requested
    if user_data.send_invite and not user_data.password:
        # Generate invite token
        invite_token = create_access_token(
            data={"email": new_user.email, "type": "invite"},
            expires_delta=timedelta(days=7)
        )
        
        # Send email (async, don't block)
        try:
            await send_invite_email(
                to_email=new_user.email,
                to_name=new_user.name,
                company_name=company.name,
                invite_token=invite_token
            )
        except Exception as e:
            # Log error but don't fail user creation
            print(f"Failed to send invite email: {e}")
    
    # Get role name
    role_name = None
    if new_user.role_id:
        role = db.query(Role).filter(Role.id == new_user.role_id).first()
        role_name = role.name if role else None
    
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        name=new_user.name,
        company_id=new_user.company_id,
        role_id=new_user.role_id,
        is_active=new_user.is_active,
        last_login=new_user.last_login,
        created_at=new_user.created_at,
        role_name=role_name
    )

@router.get("/", response_model=UserListResponse)
def list_users(
    company_id: Optional[int] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    List users with pagination and search
    """
    query = db.query(User)
    
    # Filter by company if specified
    if company_id:
        query = query.filter(User.company_id == company_id)
    
    # Search by name or email
    if search:
        query = query.filter(
            or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )
    
    # Get total count
    total = query.count()
    
    # Paginate
    users = query.offset((page - 1) * page_size).limit(page_size).all()
    
    # Add role names
    user_responses = []
    for user in users:
        role_name = None
        if user.role_id:
            role = db.query(Role).filter(Role.id == user.role_id).first()
            role_name = role.name if role else None
        
        user_responses.append(UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            company_id=user.company_id,
            role_id=user.role_id,
            is_active=user.is_active,
            last_login=user.last_login,
            created_at=user.created_at,
            role_name=role_name
        ))
    
    return UserListResponse(
        total=total,
        users=user_responses,
        page=page,
        page_size=page_size
    )

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Get user by ID
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get role name
    role_name = None
    if user.role_id:
        role = db.query(Role).filter(Role.id == user.role_id).first()
        role_name = role.name if role else None
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        company_id=user.company_id,
        role_id=user.role_id,
        is_active=user.is_active,
        last_login=user.last_login,
        created_at=user.created_at,
        role_name=role_name
    )

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Update user details
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.role_id is not None:
        user.role_id = user_data.role_id
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
    
    db.commit()
    db.refresh(user)
    
    # Get role name
    role_name = None
    if user.role_id:
        role = db.query(Role).filter(Role.id == user.role_id).first()
        role_name = role.name if role else None
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        company_id=user.company_id,
        role_id=user.role_id,
        is_active=user.is_active,
        last_login=user.last_login,
        created_at=user.created_at,
        role_name=role_name
    )

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Deactivate user (soft delete)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = False
    db.commit()
    
    return {"message": "User deactivated successfully"}

@router.post("/invite", status_code=status.HTTP_202_ACCEPTED)
async def invite_user(
    invite_data: UserInvite,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Send invitation to a new user
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == invite_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Get company_id based on user type
    from app.models.models import SystemAdmin
    if isinstance(current_user, SystemAdmin):
        # System admin must specify company in invite
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="System admins must use the create user endpoint and specify company_id"
        )
    
    company_id = current_user.company_id
    
    # Get company
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Create user without password (will set on first login)
    new_user = User(
        email=invite_data.email,
        name=invite_data.name,
        company_id=company_id,
        role_id=invite_data.role_id,
        hashed_password=None,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate invite token
    invite_token = create_access_token(
        data={"email": new_user.email, "user_id": new_user.id, "type": "invite"},
        expires_delta=timedelta(days=7)
    )
    
    # Send invite email
    try:
        await send_invite_email(
            to_email=new_user.email,
            to_name=new_user.name,
            company_name=company.name,
            invite_token=invite_token,
            custom_message=invite_data.message
        )
    except Exception as e:
        print(f"Failed to send invite email: {e}")
    
    # Log activity
    activity = ActivityLog(
        user_id=current_user.id,
        company_id=company_id,
        action="User Invited",
        details={"invited_email": invite_data.email, "invited_name": invite_data.name}
    )
    db.add(activity)
    db.commit()
    
    return {"message": "Invitation sent successfully", "user_id": new_user.id}
    
@router.get("/company/{company_id}/roles", response_model=list[RoleResponse])
def get_company_roles(
    company_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """
    Get all roles for a company
    """
    roles = db.query(Role).filter(Role.company_id == company_id).all()
    return roles