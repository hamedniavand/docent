from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.models import SystemAdmin, User
from typing import Union

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Union[SystemAdmin, User]:
    """
    Dependency to get current authenticated user from JWT token
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email = payload.get("email")
    user_type = payload.get("user_type")
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    
    # Check if system admin
    if user_type == "system_admin":
        user = db.query(SystemAdmin).filter(SystemAdmin.email == email).first()
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )
        return user
    
    # Check if company user
    user = db.query(User).filter(User.email == email).first()
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    return user

def require_system_admin(
    current_user: Union[SystemAdmin, User] = Depends(get_current_user)
) -> SystemAdmin:
    """
    Dependency to require system admin privileges
    """
    if not isinstance(current_user, SystemAdmin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System admin privileges required",
        )
    return current_user

def require_active_user(
    current_user: Union[SystemAdmin, User] = Depends(get_current_user)
) -> Union[SystemAdmin, User]:
    """
    Dependency to require any active authenticated user
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user