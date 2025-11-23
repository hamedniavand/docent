from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class UserBase(BaseModel):
    email: EmailStr
    name: str
    is_active: bool = True

class SystemAdminResponse(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    company_id: int
    role_id: Optional[int]
    is_active: bool
    
    class Config:
        from_attributes = True

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    user_type: Optional[str] = None  # 'system_admin' or 'company_user'