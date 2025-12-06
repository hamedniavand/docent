from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ActivityLogCreate(BaseModel):
    action: str
    details: Optional[Dict[str, Any]] = {}


class ActivityLogResponse(BaseModel):
    id: int
    company_id: Optional[int]
    user_id: Optional[int]
    user_name: Optional[str] = None
    action: str
    details: Dict[str, Any]
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ActivityLogListResponse(BaseModel):
    total: int
    logs: List[ActivityLogResponse]
    page: int
    page_size: int


class SearchAnalytics(BaseModel):
    total_searches: int
    searches_today: int
    searches_this_week: int
    top_queries: List[Dict[str, Any]]
    searches_by_day: List[Dict[str, Any]]


class DocumentAnalytics(BaseModel):
    total_documents: int
    processed_documents: int
    total_chunks: int
    documents_by_type: Dict[str, int]
    uploads_by_day: List[Dict[str, Any]]
    most_searched_docs: List[Dict[str, Any]]


class UserAnalytics(BaseModel):
    total_users: int
    active_users: int
    users_by_role: Dict[str, int]
    recent_logins: List[Dict[str, Any]]
    most_active_users: List[Dict[str, Any]]


class DashboardAnalytics(BaseModel):
    search: SearchAnalytics
    documents: DocumentAnalytics
    users: UserAnalytics
    recent_activity: List[ActivityLogResponse]


class AnalyticsSummary(BaseModel):
    total_searches: int
    total_documents: int
    total_users: int
    total_cases: int
    activity_count_today: int
