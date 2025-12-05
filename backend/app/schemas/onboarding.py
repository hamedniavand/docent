from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

# Onboarding Path (Template)
class OnboardingStepSchema(BaseModel):
    title: str
    description: str
    content: Optional[str] = None  # Instructions or content
    document_ids: List[int] = []   # Related documents to read
    order: int

class OnboardingPathCreate(BaseModel):
    name: str
    description: Optional[str] = None
    department_id: Optional[int] = None
    steps: List[OnboardingStepSchema]

class OnboardingPathResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    department_id: Optional[int]
    steps_json: Dict
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class OnboardingPathListResponse(BaseModel):
    total: int
    paths: List[OnboardingPathResponse]

# User Progress
class UserProgressCreate(BaseModel):
    path_id: int
    user_id: int

class StepProgressUpdate(BaseModel):
    step_index: int
    completed: bool
    notes: Optional[str] = None

class UserProgressResponse(BaseModel):
    id: int
    user_id: int
    path_id: int
    path_name: str
    current_step: int
    total_steps: int
    completed_steps: List[int]
    percent_complete: float
    started_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True
