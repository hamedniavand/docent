from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class SystemAdmin(Base):
    __tablename__ = "system_admins"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    domain_restriction = Column(String, nullable=True)
    plan_limits = Column(JSON, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("User", back_populates="company")
    documents = relationship("Document", back_populates="company")
    departments = relationship("Department", back_populates="company")

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    permissions = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("User", back_populates="role")

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    company = relationship("Company", back_populates="departments")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    notification_preferences = Column(JSON, default={
        "email_on_document_processed": True,
        "email_on_new_case": True,
        "email_weekly_digest": True,
        "email_onboarding_reminders": True
    })
    created_at = Column(DateTime, default=datetime.utcnow)
    
    company = relationship("Company", back_populates="users")
    role = relationship("Role", back_populates="users")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    status = Column(String, default="pending")
    doc_metadata = Column(JSON, default={})  # Changed from metadata
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    
    company = relationship("Company", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document")
    

class DocumentChunk(Base):
    __tablename__ = "doc_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chunk_id_for_vector = Column(String, unique=True, nullable=False)
    chunk_metadata = Column(JSON, default={})  # Changed from metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="chunks")

class CaseTemplate(Base):
    __tablename__ = "case_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    name = Column(String, nullable=False)
    template_json = Column(JSON, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class CaseInstance(Base):
    __tablename__ = "case_instances"
    
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("case_templates.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    data_json = Column(JSON, nullable=False)
    generated_summary = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class OnboardingPath(Base):
    __tablename__ = "onboarding_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    name = Column(String, nullable=False)
    steps_json = Column(JSON, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class SearchHistory(Base):
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    query_text = Column(Text, nullable=False)
    results_meta = Column(JSON, default={})
    timestamp = Column(DateTime, default=datetime.utcnow)

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)
    details = Column(JSON, default={})
    timestamp = Column(DateTime, default=datetime.utcnow)
class UserOnboardingProgress(Base):
    __tablename__ = "user_onboarding_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    path_id = Column(Integer, ForeignKey("onboarding_paths.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    current_step = Column(Integer, default=0)
    completed_steps = Column(JSON, default=[])  # List of completed step indices
    progress_data = Column(JSON, default={})    # Additional progress data
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    user = relationship("User")
    path = relationship("OnboardingPath")