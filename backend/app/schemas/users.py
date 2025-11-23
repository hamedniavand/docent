from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    company_id: int
    role_id: Optional[int] = None
    password: Optional[str] = None
    send_invite: bool = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None

class UserInvite(BaseModel):
    email: EmailStr
    name: str
    role_id: Optional[int] = None
    message: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    company_id: int
    role_id: Optional[int]
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime
    role_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    total: int
    users: list[UserResponse]
    page: int
    page_size: int

class RoleResponse(BaseModel):
    id: int
    name: str
    company_id: int
    permissions: dict
    
    class Config:
        from_attributes = True