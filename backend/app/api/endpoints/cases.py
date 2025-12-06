from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.models import CaseTemplate, CaseInstance, User, Document
from app.schemas.cases import (
    CaseTemplateCreate, CaseTemplateResponse,
    CaseInstanceCreate, CaseInstanceUpdate, CaseInstanceResponse,
    CaseInstanceListResponse, CaseStatsResponse
)
from app.api.deps.auth import require_active_user

router = APIRouter(prefix="/cases", tags=["Case Studies"])


# ============ TEMPLATES ============

@router.get("/templates", response_model=List[CaseTemplateResponse])
def list_templates(
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """List all available case templates (company + default)"""
    templates = db.query(CaseTemplate).filter(
        (CaseTemplate.company_id == current_user.company_id) | 
        (CaseTemplate.is_default == True)
    ).all()
    return templates


@router.post("/templates", response_model=CaseTemplateResponse, status_code=status.HTTP_201_CREATED)
def create_template(
    data: CaseTemplateCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Create a new case template for the company"""
    template = CaseTemplate(
        name=data.name,
        template_json={"sections": data.sections, "description": data.description},
        company_id=current_user.company_id,
        created_by=current_user.id,
        is_default=False
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    return template


@router.get("/templates/{template_id}", response_model=CaseTemplateResponse)
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get a specific template"""
    template = db.query(CaseTemplate).filter(CaseTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Check access (company template or default)
    if template.company_id and template.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return template


@router.delete("/templates/{template_id}")
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Delete a company template (cannot delete defaults)"""
    template = db.query(CaseTemplate).filter(CaseTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if template.is_default:
        raise HTTPException(status_code=400, detail="Cannot delete default templates")
    
    if template.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    db.delete(template)
    db.commit()
    return {"message": "Template deleted"}


# ============ CASE INSTANCES ============

@router.post("/", response_model=CaseInstanceResponse, status_code=status.HTTP_201_CREATED)
def create_case(
    data: CaseInstanceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Create a new case study"""
    # Verify template exists
    template = db.query(CaseTemplate).filter(CaseTemplate.id == data.template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Build data_json
    sections_dict = {s.section_name: s.content for s in data.sections_data}
    data_json = {
        "title": data.title,
        "sections": sections_dict,
        "linked_documents": data.linked_document_ids or []
    }
    
    case = CaseInstance(
        template_id=data.template_id,
        company_id=current_user.company_id,
        data_json=data_json,
        created_by=current_user.id
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    
    # Get creator name
    creator = db.query(User).filter(User.id == case.created_by).first()
    
    return CaseInstanceResponse(
        id=case.id,
        template_id=case.template_id,
        template_name=template.name,
        company_id=case.company_id,
        title=data_json.get("title", "Untitled"),
        data_json=case.data_json,
        generated_summary=case.generated_summary,
        created_by=case.created_by,
        creator_name=creator.name if creator else "Unknown",
        created_at=case.created_at
    )


@router.get("/", response_model=CaseInstanceListResponse)
def list_cases(
    template_id: Optional[int] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """List case studies for the company"""
    query = db.query(CaseInstance).filter(CaseInstance.company_id == current_user.company_id)
    
    if template_id:
        query = query.filter(CaseInstance.template_id == template_id)
    
    # Search in title (stored in data_json)
    if search:
        query = query.filter(CaseInstance.data_json['title'].astext.ilike(f"%{search}%"))
    
    total = query.count()
    cases = query.order_by(CaseInstance.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    # Build response with template names and creator names
    case_responses = []
    for case in cases:
        template = db.query(CaseTemplate).filter(CaseTemplate.id == case.template_id).first()
        creator = db.query(User).filter(User.id == case.created_by).first()
        
        case_responses.append(CaseInstanceResponse(
            id=case.id,
            template_id=case.template_id,
            template_name=template.name if template else "Unknown",
            company_id=case.company_id,
            title=case.data_json.get("title", "Untitled"),
            data_json=case.data_json,
            generated_summary=case.generated_summary,
            created_by=case.created_by,
            creator_name=creator.name if creator else "Unknown",
            created_at=case.created_at
        ))
    
    return CaseInstanceListResponse(
        total=total,
        cases=case_responses,
        page=page,
        page_size=page_size
    )


@router.get("/stats", response_model=CaseStatsResponse)
def get_case_stats(
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get case study statistics"""
    # Total cases
    total = db.query(CaseInstance).filter(CaseInstance.company_id == current_user.company_id).count()
    
    # Cases this month
    month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    this_month = db.query(CaseInstance).filter(
        CaseInstance.company_id == current_user.company_id,
        CaseInstance.created_at >= month_start
    ).count()
    
    # By template
    by_template = {}
    template_counts = db.query(
        CaseTemplate.name,
        func.count(CaseInstance.id)
    ).join(CaseInstance).filter(
        CaseInstance.company_id == current_user.company_id
    ).group_by(CaseTemplate.name).all()
    
    for name, count in template_counts:
        by_template[name] = count
    
    return CaseStatsResponse(
        total_cases=total,
        cases_this_month=this_month,
        by_template=by_template
    )


@router.get("/{case_id}", response_model=CaseInstanceResponse)
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Get a specific case study"""
    case = db.query(CaseInstance).filter(CaseInstance.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    if case.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    template = db.query(CaseTemplate).filter(CaseTemplate.id == case.template_id).first()
    creator = db.query(User).filter(User.id == case.created_by).first()
    
    return CaseInstanceResponse(
        id=case.id,
        template_id=case.template_id,
        template_name=template.name if template else "Unknown",
        company_id=case.company_id,
        title=case.data_json.get("title", "Untitled"),
        data_json=case.data_json,
        generated_summary=case.generated_summary,
        created_by=case.created_by,
        creator_name=creator.name if creator else "Unknown",
        created_at=case.created_at
    )


@router.put("/{case_id}", response_model=CaseInstanceResponse)
def update_case(
    case_id: int,
    data: CaseInstanceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Update a case study"""
    case = db.query(CaseInstance).filter(CaseInstance.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    if case.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Update data_json
    updated_json = dict(case.data_json)
    
    if data.title:
        updated_json["title"] = data.title
    
    if data.sections_data:
        sections_dict = {s.section_name: s.content for s in data.sections_data}
        updated_json["sections"] = sections_dict
    
    if data.linked_document_ids is not None:
        updated_json["linked_documents"] = data.linked_document_ids
    
    case.data_json = updated_json
    db.commit()
    db.refresh(case)
    
    template = db.query(CaseTemplate).filter(CaseTemplate.id == case.template_id).first()
    creator = db.query(User).filter(User.id == case.created_by).first()
    
    return CaseInstanceResponse(
        id=case.id,
        template_id=case.template_id,
        template_name=template.name if template else "Unknown",
        company_id=case.company_id,
        title=updated_json.get("title", "Untitled"),
        data_json=case.data_json,
        generated_summary=case.generated_summary,
        created_by=case.created_by,
        creator_name=creator.name if creator else "Unknown",
        created_at=case.created_at
    )


@router.delete("/{case_id}")
def delete_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Delete a case study"""
    case = db.query(CaseInstance).filter(CaseInstance.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    if case.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    db.delete(case)
    db.commit()
    return {"message": "Case deleted"}


@router.post("/{case_id}/generate-summary")
def generate_case_summary(
    case_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    """Generate AI summary for a case study"""
    case = db.query(CaseInstance).filter(CaseInstance.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    if case.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Build content from sections
    sections = case.data_json.get("sections", {})
    content_parts = [f"Title: {case.data_json.get('title', 'Untitled')}"]
    for section_name, section_content in sections.items():
        content_parts.append(f"\n{section_name}:\n{section_content}")
    
    full_content = "\n".join(content_parts)
    
    # Generate summary (for now, create a condensed version)
    # TODO: Integrate with Gemini for AI-powered summaries
    if len(full_content) > 500:
        summary = full_content[:500] + "..."
    else:
        summary = full_content
    
    # Add key points extraction (simple version)
    summary = f"**Case Study Summary**\n\n{summary}\n\n**Sections covered:** {', '.join(sections.keys())}"
    
    case.generated_summary = summary
    db.commit()
    
    return {"message": "Summary generated", "summary": summary}
