from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============ TEMPLATES ============

class CaseTemplateCreate(BaseModel):
    name: str
    sections: List[str]
    description: Optional[str] = None


class CaseTemplateResponse(BaseModel):
    id: int
    name: str
    template_json: Dict[str, Any]
    company_id: Optional[int]
    created_by: Optional[int]
    is_default: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ CASE INSTANCES ============

class SectionData(BaseModel):
    section_name: str
    content: str


class CaseInstanceCreate(BaseModel):
    template_id: int
    title: str
    sections_data: List[SectionData]
    linked_document_ids: Optional[List[int]] = []


class CaseInstanceUpdate(BaseModel):
    title: Optional[str] = None
    sections_data: Optional[List[SectionData]] = None
    linked_document_ids: Optional[List[int]] = None


class CaseInstanceResponse(BaseModel):
    id: int
    template_id: int
    template_name: str
    company_id: int
    title: str
    data_json: Dict[str, Any]
    generated_summary: Optional[str]
    created_by: int
    creator_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class CaseInstanceListResponse(BaseModel):
    total: int
    cases: List[CaseInstanceResponse]
    page: int
    page_size: int


class CaseStatsResponse(BaseModel):
    total_cases: int
    cases_this_month: int
    by_template: Dict[str, int]
