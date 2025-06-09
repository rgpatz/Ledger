from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from app.models import EngagementStatus # Re-use enum

# Client Contact schemas
class ClientContactBase(BaseModel):
    name: str
    email: EmailStr
    title: Optional[str] = None
    phone: Optional[str] = None
    is_primary: str = "no"  # "yes" or "no"

class ClientContactCreate(ClientContactBase):
    pass

class ClientContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    title: Optional[str] = None
    phone: Optional[str] = None
    is_primary: Optional[str] = None

class ClientContactRead(ClientContactBase):
    id: int
    client_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Client schemas
class ClientBase(BaseModel):
    name: str
    company: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None

class ClientCreate(ClientBase):
    contacts: List[ClientContactCreate] = []

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None

class ClientRead(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    contacts: List[ClientContactRead] = []

    class Config:
        from_attributes = True

# Engagement schemas (updated to work with clients)
class EngagementBase(BaseModel):
    engagement_name: str
    client_id: int
    client_name: str  # Keep for backward compatibility
    status: EngagementStatus = EngagementStatus.PROPOSED
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    scope_summary: Optional[str] = None
    project_lead: Optional[str] = None

class EngagementCreate(EngagementBase):
    pass

class EngagementUpdate(BaseModel): # All fields optional for update
    engagement_name: Optional[str] = None
    client_id: Optional[int] = None
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
    client: Optional[ClientRead] = None

    class Config:
        from_attributes = True 