from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from app.models import EngagementStatus # Re-use enum

class EngagementBase(BaseModel):
    engagement_name: str
    client_name: str
    status: EngagementStatus = EngagementStatus.PROPOSED
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    scope_summary: Optional[str] = None
    project_lead: Optional[str] = None

class EngagementCreate(EngagementBase):
    pass

class EngagementUpdate(BaseModel): # All fields optional for update
    engagement_name: Optional[str] = None
    client_name: Optional[str] = None
    status: Optional[EngagementStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    scope_summary: Optional[str] = None
    project_lead: Optional[str] = None

class EngagementRead(EngagementBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic V1 syntax 