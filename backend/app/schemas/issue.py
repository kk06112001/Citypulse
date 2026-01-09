from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IssueCreate(BaseModel):
    title: str
    description: str
    category: str
    location: str
    image_url: Optional[str] = None


class IssueResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    location: str
    status: str
    image_url: Optional[str]
    citizen_id: int
    assigned_to: Optional[str]
    created_at: datetime

class AdminIssueResponse(IssueResponse):
    id: int
    title: str
    description: str
    category: str
    location: str
    status: str
    assigned_to: Optional[str]
    citizen_id: int
    citizen_email: Optional[str] = None  # optional, we'll populate
    created_at: datetime
    updated_at: datetime

class IssueAssign(BaseModel):
    assigned_to: str

class IssueStatusUpdate(BaseModel):
    status: str

    class Config:
        from_attributes = True