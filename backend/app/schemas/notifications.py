from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationPreferences(BaseModel):
    email_on_document_processed: bool = True
    email_on_new_case: bool = True
    email_weekly_digest: bool = True
    email_onboarding_reminders: bool = True


class NotificationPreferencesUpdate(BaseModel):
    email_on_document_processed: Optional[bool] = None
    email_on_new_case: Optional[bool] = None
    email_weekly_digest: Optional[bool] = None
    email_onboarding_reminders: Optional[bool] = None


class NotificationPreferencesResponse(BaseModel):
    user_id: int
    email_on_document_processed: bool
    email_on_new_case: bool
    email_weekly_digest: bool
    email_onboarding_reminders: bool
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
